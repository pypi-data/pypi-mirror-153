#!/usr/bin/env python3
'''\
A layer of wrappers for an hdf5 database

database.py

Vera Del Favero

This database class will handle all access to the hdf5 databses
    we'll be using in this module
'''
######## Imports ########

import numpy as np
import time
import h5py
from os.path import join, isfile, isdir

######## Database Class ########

class Database(object):
    '''\
    This is a wrapper for hdf5 databases
        inteded to simplify calling and reduce clutter

    Inputs:
        fname (str): file name and location
        group (str): point to a particular group in the database

    Methods: 
        #### General ####

        change_group: change the group the object points to
        visit: visit each item in the databse
        merge: merge a similar database into this one
        shard: create a new databse with some data from the current database
        list_items: list databases and groups in a particular group within
            the hdf5 database
        scan: scan a particular group in the database and print it
            without changing the group we point to
        kind: determine if a particular item is a database or a group
        exists: determine if a particular item exists

        #### dset methods Methods ####

        dset_init: initialize new dataset in the hdf5 database
        dset_size: return the size of the dataset
        dset_compression: return the compression of the dataset
        dset_shape: return the shape of the dataset
        dset_dtype: return the dtype of the dataset
        dset_fields: return the fields for a dataset stored with fields
        dset_value: return the value of a dataset, 
            for a given field and set of indicies
        dset_sum: return the sum of a given dataset for some field 
            on some indicies
        dset_min: return the mix of a given dataset for some field 
            on some indicies
        dset_max: return the max of a given dataset for some field 
            on some indicies
        dset_set: set the values of a dataset, with some intelligence
        dset_rm: remove a given dataset (this does not free the disk space)
        dset_copy: copy a given dataset
        dset_recompress: copy a dataset to a temporary location and
            copy it back, changing the compression.
            WARNING: This is extraordinarily inneficient, and should only
            be used for testing

        #### attr methods ####

        attr_exists: check if attribute exists
        attr_value: return attribute value
        attr_set: set a given attribute
        attr_list: list attributes for a given dataset or group
        attr_dict: return the dictionary of attributes for a given dataset
            or group
        attr_set_dict: set each attribute from a given dictionary

    '''

    def __init__(
                 self, 
                 fname,
                 group = '/',
                 retries = 10,
                 sleep = 5,
                ):
        '''\
        Point to and ensure the existence of the database
    
        Inputs:
            fname (str): file name and location
            group (str): point to a particular group in the database

        '''
        # Assign attributes
        self.fname = fname
        if group is None:
            group = '/'
        self.group = group
        self.retries = retries
        self.sleep = sleep

        # Assert the existence of the database
        try:
            # First write a new database if one doesn't already exist
            with h5py.File(self.fname, 'w-') as F:
                if not (group is '/'):
                    F.create_group(group)
            return
        except:
            pass

        # Otherwise try to load the existing database
        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r+') as F:
                    load = True
                    if (not (group is '/')) and (not (group in F)):
                        F.create_group(group)
            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)


    def change_group(
                     self,
                     group = '/',
                    ):
        '''\
        Recreate the database with new group

        Inputs:
            group: New group
        '''

        # Check if group startswith /
        if group.startswith("/"):
            # group is to be interpreted global
            pass
        else:
            # Group is to be interpreted local
            group = join(self.group, group)

        # Create a new database object and assign it to this group
        self = Database(self.fname, group)

    def visit(self, fn = print):
        '''\
        Visit the database
        
        Inputs:
            fn: function to visit every item in database with
        '''
        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r') as F:
                    load = True
                    group_obj = F[self.group]
                    F.visit(fn)
            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)

    def merge(self, fname_head):
        '''\
        Merge another similar database (the head) into this one (the origin)

            Inputs:
                fname_head: the file name and location for the head node
        '''

        # Initialize two database objects
        Origin = h5py.File(self.fname, 'r+')
        Head = h5py.File(fname_head, 'r')

        # Make use of visit functionality to recursively copy database
        def visit_function(parcel):
            item = Head[parcel]
            # If the group or dataset is not in origin, copy it
            if not (item.name in Origin):
                print("found it!")
                Head.copy(item.name, Origin[item.parent.name])
            # If the group or dataset has attributes, copy them
            attrs = dict(item.attrs)
            # For each attr in the dict
            for key in list(attrs.keys()):
                # Copy it
                Origin[item.parent.name].attrs[key] = attrs[key]

        try:
            Head.visit(visit_function)

        finally:
            Origin.close()
            Head.close()

    def shard(self, fname_head, names = None, compression = "default"):
        '''\
        Create a smaller database with less data

        option to compress data differently
        
        Inputs:
            fname_head: file name and location for desired shard database
            names: list of items for copying
            compression: file compression option for database
        '''
        # Make sure we don't delete everything
        if self.fname == fname_head:
            raise Exception("shard name cannot be origin name")

        # Create objects for current database (origin)
        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r') as Origin:
                    # and new database (head)
                    with h5py.File(fname_head, 'w') as Head:
                        load = True
                        # If names is not given, assume all data is to be copied
                        if names is None:
                            names = self.list_items(kind = "dset")
                        print("creating shard with members: ", names)


                        # Make sure the group exists in the new dataset
                        if not self.group == "/":
                            Head.create_group(self.group)

                        # Copy group attributes
                        group_attrs = self.attr_list('.')
                        for item in group_attrs:
                            Head[self.group].attrs[item] = Origin[self.group].attrs[item]

                        # Loop through each dataset
                        for item in names:
                            # Find the data
                            dset = Origin[self.group][item]
                            # Check compression
                            if compression =="default" or dset.size <= 1:
                                # Default copy behavior includes attrs
                                Origin.copy(dset.name, Head[self.group])
                            else:
                                # Copy data
                                Head[self.group].create_dataset(
                                                                item,
                                                                data=dset[...],
                                                                dtype=dset.dtype,
                                                                compression=compression
                                                               )
                                # copy attrs
                                for jtem in dset.attrs:
                                    Head[self.group][item].attrs[jtem] = dset.attrs[jtem]
    
            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)

            print("Shard successful!")

    def list_items(self, path="./", kind = None):
        '''\
        Return list of groups in current group
        
        Inputs:
            path: Path to group inside database.
                can be relative or absolute
            kind: list only datasets or only groups
        '''
        # Open File
        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r') as F:
                    load = True
                    # Find your place in the file
                    group_obj = F[self.group][path]
                    # Initialize list of items
                    items = []
                    # Go through current 'directory'
                    for item in group_obj:
                        # Keep track of what you want to append
                        append = False
                    
                        if kind is None:
                            # If kind is None, always append item
                            append = True

                        elif kind == "group":
                            # If kind is group, append it only if it is a group
                            if type(group_obj[item]) == h5py._hl.group.Group:
                                append = True

                        elif kind == "dset":
                            # If kind is dset, append only if it is a dset
                            if type(group_obj[item]) == h5py._hl.dataset.Dataset:
                                append = True

                        if append:
                            items.append(item)

            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)

        return items

    def scan(self, path="./", kind=None):
        '''\
        Return basic information about the objects in the current group

        This is really useful when exploring an unknown database
        Inputs:
            path: Path to group inside database.
                can be relative or absolute
            kind: list only datasets or only groups
        '''
        # Create temporary database object pointing at path
        db_scan = Database(self.fname, self.group)
        db_scan.change_group(path)
        # Read items in scanned pointer database
        items = db_scan.list_items(kind=kind)
        # Check each item
        for item in items:
            # Item information
            item_dict = {}
            # Name each item
            item_dict["name"] = item
            # Figure out if it is a dset or grou
            item_dict["kind"] = db_scan.kind(item)
            # List attributes
            item_dict["attrs"] = db_scan.attr_list(item)
            # Dset only things
            if item_dict["kind"] == "dset":
                # Return the shape of the dset
                item_dict["shape"] = db_scan.dset_shape(item)
                # Return the dtype of the dset
                item_dict["dtype"] = db_scan.dset_dtype(item)
                # Return the compression of the dset
                item_dict["compression"] = db_scan.dset_compression(item)
                # Return the fields of the dset
                item_dict["fields"] = db_scan.dset_fields(item)

            # Print item_dict
            print(item_dict)


    def create_group(self, item, clean = True):
        '''\
        Create a new group
        '''
        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r+') as F:
                    load = True
                    group_obj = F[self.group]
                    if not item in group_obj:
                        group_obj.create_group(item)
                    else:
                        if clean:
                            raise RuntimeError("item %s already exists!"%(item))
                        if type(group_obj[item]) != h5py._hl.group.Group:
                            raise RuntimeError("item %s already exists, and is not a group!"%(item))
    
            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)

        return Database(self.fname, join(self.group, item))

    def kind(self, item):
        '''\
        Return the kind of item, be it a group or dset
        '''
        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r') as F:
                    load = True
                    group_obj = F[self.group]
                    if not (item in group_obj):
                        raise RuntimeError("kind: No such object %s"%(join(self.group, item)))
                    elif type(group_obj[item]) == h5py._hl.group.Group:
                        return "group"
                    elif type(group_obj[item]) == h5py._hl.dataset.Dataset:
                        return "dset"

            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)

    def exists(self, item, kind=None):
        '''\
        Check if item exists
        '''

        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r') as F:
                    load = True
                    group_obj = F[self.group]
                    if not (item in group_obj):
                        return False
                    elif kind is None:
                        return True
                    elif kind == self.kind(item):
                        return True
                    else: return False

            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)


    def dset_init(self, item, shape, dtype, compression=None ):
        '''\
        Initialize a new dataset

        Inputs:
            item: name of dataset
            shape: shape of dataset
            dtype: dtype of dataset
            compression: desired compression of data
        '''
        # Make the syntax a little more forgiving
        if not type(shape) is tuple:
            shape = tuple([shape])

        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r+') as F:
                    load = True
                    group_obj = F[self.group]
                    group_obj.create_dataset(item, shape, compression=compression, dtype=dtype)

            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)


    def dset_size(self, item):
        '''\
        Return the size of a dataset

        Inputs:
            item: the dataset we would like to know the size of
        '''
        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r') as F:
                    load = True
                    group_obj = F[self.group]
                    value = group_obj[item].size

            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)

        return value

    def dset_compression(self, item):
        '''\
        Return the compression of a dataset

        Inputs:
            item: the dataset we would like to know the size of
        '''
        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r') as F:
                    load = True
                    group_obj = F[self.group]
                    value = group_obj[item].compression

            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)

        return value

    def dset_shape(self, item):
        '''\
        Return the sum of a dataset

        Inputs:
            item: the dataset we would like to know the size of
        '''
        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r') as F:
                    load = True
                    group_obj = F[self.group]
                    value = group_obj[item].shape

            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)

        return value

    def dset_dtype(self, item):
        '''\
        Return the dtype of a dataset

        Inputs:
            item: the dataset we would like to know the size of
        '''
        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r') as F:
                    load = True
                    group_obj = F[self.group]
                    value = group_obj[item].dtype

            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)

        return value

    def dset_fields(self, item):
        '''\
        Return the fields of a dataset with an informative dtype

        Inputs:
            item: the dataset we would like to know the size of
        '''
        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r') as F:
                    load = True
                    group_obj = F[self.group]
                    value = group_obj[item].dtype.fields

            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)

        return value

    def dset_value(self, item, field = None, samples = None):
        '''\
        Return the values of a dataset

        Inputs:
            item: the dataset we would like to know the size of
            field: the field of interest for a complex data type
            samples: an array of indexes pointing to which part of the set
                we would like to analyze

        '''

        # Check usage
        if (field is None) and not (self.dset_fields(item) is None):
            raise ValueError("User did not specify a field.")

        # Otherwise open the file, and get the values
        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r') as F:
                    load = True
                    # Define the group
                    group_obj = F[self.group]

                    # find the appropriate samples
                    if samples is None:
                        value = group_obj[item][...]
                    else:
                        value = group_obj[item][samples]

                    # Find the appropriate field
                    if not (field is None):
                        value = value[field]

            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)

        return value


    def dset_sum(self, item, field = None, samples = None):
        '''\
        Return the sum of a dataset

        Inputs:
            item: the dataset we would like to know the size of
            field: the field of interest for a complex data type
            samples: an array of indexes pointing to which part of the set
                we would like to analyze
        '''
        
        # Check usage
        if (field is None) and not (self.dset_fields(item) is None):
            raise ValueError("User did not specify a field.")

        if field is None:
            attr_name = "sum"
        else:
            attr_name = "%s_sum"%(field)

        # Check if the sum was already computed
        if self.attr_exists(item, attr_name):
            value = self.attr_value(item, attr_name)
        else:
            value = None

        # Case 1: precomputed sum
        if (not (value is None)) & (samples is None):
            return value

        # Case 2: calculate sum
        else:
            # Find the data
            data = self.dset_value(item, field = field, samples = samples)

            # Calcualte the sum
            value = np.sum(data)

        # Only save the sum if using the whole dataset
        if (samples is None):
            # Save the value for next time
            self.attr_set(item, attr_name, value)

        return value

    def dset_min(self, item, field = None, samples = None):
        '''\
        Return the minimum value of a dataset

        Inputs:
            item: the dataset we would like to know the size of
            field: the field of interest for a complex data type
            samples: an array of indexes pointing to which part of the set
                we would like to analyze
        '''

        # Check usage
        if (field is None) and not (self.dset_fields(item) is None):
            raise ValueError("User did not specify a field.")

        # Find the right attribute
        if field is None:
            attr_name = "min"
        else:
            attr_name = "%s_min"%(field)

        # Case 1: Check if the min was already computed
        if (samples is None) & self.attr_exists(item, attr_name):
            value = self.attr_value(item, attr_name)
 
        # Case 2: calculate min
        else:
            # Find the data
            data = self.dset_value(item, field = field, samples = samples)

            # Calcualte the minimum
            value = np.min(data)

        # Save the minimum if using the whole dataset
        if (samples is None):
            # Save the value for next time
            self.attr_set(item, attr_name, value)
        # Also save the minimum if it doesn't exist
        elif not (self.attr_exists(item, attr_name)):
            self.attr_set(item, attr_name, value)
        # Also save the minimum if it is less than the saved minimum
        elif self.attr_value(item, attr_name) > value:
            self.attr_set(item, attr_name, value)
        # Also return the saved value if it is less than the calculated value
        # Not sure if I really want this behavior.
        # It could be misleading
        else:
            value = self.attr_value(item, attr_name)

        return value

    def dset_max(self, item, field = None, samples = None):
        '''\
        Return the maximum value of a dataset
        '''

        # Check usage
        if (field is None) and not (self.dset_fields(item) is None):
            raise ValueError("User did not specify a field.")

        # Find the right attribute
        if field is None:
            attr_name = "max"
        else:
            attr_name = "%s_max"%(field)

        # Case 1: Check if the max was already computed
        if (samples is None) & self.attr_exists(item, attr_name):
            value = self.attr_value(item, attr_name)
 
        # Case 2: calculate max
        else:
            # Find the data
            data = self.dset_value(item, field = field, samples = samples)

            # Calcualte the minimum
            value = np.max(data)

        # Save the maximum if using the whole dataset
        if (samples is None):
            # Save the value for next time
            self.attr_set(item, attr_name, value)
        # Also save the maximum if it doesn't exist
        elif not (self.attr_exists(item, attr_name)):
            self.attr_set(item, attr_name, value)
        # Also save the maximum if it is greater than the saved value
        elif self.attr_value(item, attr_name) < value:
            self.attr_set(item, attr_name, value)
        # Return the saved value if it is greater than the calculated value
        # Not sure if I really want this behavior.
        # It could be misleading
        else:
            value = self.attr_value(item, attr_name)

        return value

    def dset_set(self, item, data, samples=None, fields=None, compression=None):
        '''\
        Create a new dataset or update the existing one

        Inputs:
            item: the dataset we would like to know the size of
            data: the data belonging to the dataset

            samples: an array of indexes pointing to which part of the set
                we would like to analyze
            fields: fields for complex datatype
            compression: Desired data compression
        '''

        if not (fields is None):
            raise NotImplementedError(
                "Reading from fields is fine, but we're not writing them yet!"
               )

        # Guarentee existence
        if not self.exists(item):
            if samples is None:
                self.dset_init(item, data.shape, data.dtype, compression=compression)
            else:
                raise Exception(
                    "Cannot initialize database for incomplete dataset!"
                   )
        else:
            if not (compression is None):
                raise KeyError("Can only set compression for new datasets")

        # Provide values
        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r+') as F:
                    load = True
                    group_obj = F[self.group]
                    if (samples is None):
                        group_obj[item][...] = data
                    else:
                        group_obj[item][samples] = data
            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)


    def dset_rm(self, item):
        '''\
        Remove a dataset
        '''
        if self.exists(item):
            n_try = 0
            load = False
            while (not load) and (n_try < self.retries):
                try:
                    with h5py.File(self.fname, 'r+') as F:
                        load = True
                        group_obj = F[self.group]
                        del group_obj[item]
                except OSError:
                    n_try += 1
                    #If the resource is busy, try again!
                    time.sleep(np.random.random()*self.sleep)

        else:
            raise Warning("Couldn't find %s to delete it!"%item)

    def dset_copy(self, item, copy, compression="default", dtype="default"):
        '''\
        Copy a dataset

        Inputs:
            item: the name of the item we would like to copy
            copy: the destination of the copy
            compression: the desired compression level of the copy
            dtype: the desired datatype for the new data
        '''
        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, "r+") as F:
                    load = True
                    # Locate database
                    dset = F[self.group][item]
                    # Simple copy or recompress
                    if compression =="default" and dtype == "default":
                        # Default copy behavior includes attrs
                        F.copy(dset.name, F[self.group], name=copy)
                    else:
                        # Check which dtype to use
                        if dtype == "default":
                            dtype = dset.dtype
                        # Copy data
                        F[self.group].create_dataset(
                                                 copy,
                                                 data=dset[...],
                                                 dtype=dtype,
                                                 compression=compression,
                                                    )
                        for jtem in dset.attrs:
                            F[self.group][copy].attrs[jtem] = dset.attrs[jtem]
            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)

    
    def dset_recompress(self, dset, compression="gzip", dtype="default", alias="TEMP"):
        '''\
        Compress and copy data, and recopy it back to the same name

        This is actually much less useful than it sounds,
            and should only be used for testing
        '''
        self.dset_copy(dset, alias, compression="default", dtype="default")
        self.dset_rm(dset)
        self.dset_copy(alias, dset, compression=compression, dtype=dtype)
        self.dset_rm(alias)


    def attr_exists(self, item, attr):
        '''\
        Check if given attribute exists

        Inputs:
            item: the dataset or group the attribute would belong to
            attr: the name of the attribute
        '''

        n_try = 0
        load = False
        if not self.exists(item):
            raise Exception ("There is no such group %s"%item)
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r') as F:
                    load = True
                    group_obj = F[self.group]
                    truth = attr in group_obj[item].attrs
            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)

        return truth

    def attr_value(self, item, attr):
        '''\
        Get the value of an attribute

        Inputs:
            item: the dataset or group the attribute would belong to
            attr: the name of the attribute
        '''

        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r') as F:
                    load = True
                    group_obj = F[self.group]
                    value = group_obj[item].attrs[attr]
            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)

        return value

    def attr_set(self, item, attr, value):
        '''\
        Set a value for an attribute

        Inputs:
            item: the dataset or group the attribute would belong to
            attr: the name of the attribute
            value: the value of the attribute
        '''

        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, 'r+') as F:
                    load = True
                    group_obj = F[self.group]
                    group_obj[item].attrs[attr] = value
            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)


    def attr_list(self, item):
        '''\
        List the attributes of a given item

        Inputs:
            item: the dataset or group the attribute would belong to
        '''
        n_try = 0
        load = False
        while (not load) and (n_try < self.retries):
            try:
                with h5py.File(self.fname, "r") as F:
                    load = True
                    group_obj = F[self.group]
                    attrs = list(group_obj[item].attrs)

            except OSError:
                n_try += 1
                #If the resource is busy, try again!
                time.sleep(np.random.random()*self.sleep)

        return attrs

    def attr_dict(self, item):
        '''\
        return a dictionary with all of the attributes for a given item

        Inputs:
            item: the dataset or group the attribute would belong to
        '''
        # Load all the keys
        keys = self.attr_list(item)
        # Initialize dictionary
        attrs = {}
        # Loop through each attr
        for key in keys:
            attrs[key] = self.attr_value(item, key)
        return attrs

    def attr_set_dict(self, item, attrs):
        '''\
        set each attribute from the dictionary

        Inputs:
            item: the dataset or group the attribute would belong to
            attrs: the dictionary of attributes
        '''
        # Loop through each attribute
        for key in attrs:
            # Set it
            self.attr_set(item, key, attrs[key])


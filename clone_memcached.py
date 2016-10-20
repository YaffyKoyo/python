#!/usr/bin/env python

'''
This is a fake memcached client.

Overview
========
Cachedog use python native socket APIs to access memcached server. 
It is inspired by python-memcached. This stuff is aim to be familiar
with Python language, for the author is a beginner for python.

Commands
========
Standard Protocol:
	command <key> <flags> <expiration time> <bytes>
	<value>

The "standard protocol stuff" of memcached involves running a command against an "item".
An item consists of:

1. A key (arbitrary string up to 250 bytes in length. No space or newlines for ASCII mode)
2. A 32bit "flag" value
3. An expiration time, in seconds. Can be up to 30 days. After 30 days, is treated as a unix
   timestamp of an exact date.
4. A 64bit "CAS" value, which is kept unique.
5. Arbitrary data

CAS is optional (can be disabled entirely with -C, and there are more fields that internally
make up an item, but these are what your client interacts with.

Full command list can be found here: https://code.google.com/p/memcached/wiki/NewCommands

Usage summary
=============
You must know it... :)

TODO
====
add compress
add log
add multi-servers

Release note
============
0.1.0
Can access ONLY one server
Basic memcached command supported
Can log command history
'''
import os
import sys
import time
import socket
import logging


# try:
# 	import cPickle as pickle
# except ImportError:
# 	import pickle

#from binascii import crc32

# try:
#     from threading import local
# except ImportError:
#     class local():
#         pass

__author__ = 'xishvai <xishvai@gmail.com>'
__version__ = '0.1.0'
__license__ = 'Python Software Foundation License'


SERVER_MAX_KEY_LENGTH = 250  # ordinary value
# assume not larger than 1M, you can change it as you need.
SERVER_MAX_VALUE_LENGTH = 1024 * 1024

MAX_DATA_LENGTH = 1024 * 1024

LOCALHOST = '127.0.0.1'
DEFAULT_PORT = 11211
DEFAULT_ADDRESS = (LOCALHOST, DEFAULT_PORT)


class Noreply:
    pass


class Client:

    def __init__(self, url):
        self.url = url
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cmdlog = []
        self.cmd = None

        try:
            a_url, a_port = self.url.split(':')
            addr = (a_url, int(a_port))
            self.sock.connect(addr)
        except socket.error, msg:
            print('Connecting %s error' % msg[1])
            sys.exit(1)

    #
    # constants & exception & tools
    #
    _FLAG_INTEGER = 1 << 0
    _FLAG_LONG = 1 << 1
    _FLAG_PICKLE = 1 << 2
    _FLAG_COMPRESS = 1 << 3

    class MemcachedKeyError(Exception):
        pass

    class MemcachedKeyNoneError(MemcachedKeyError):
        pass

    class MemcachedKeyTypeError(MemcachedKeyError):
        pass

    class MemcachedKeyLengthError(MemcachedKeyError):
        pass

    class MemcachedKeyCharacterError(MemcachedKeyError):
        pass

    class MemcachedStringEncodingError(MemcachedKeyError):
        pass

    #
    # Storage Commands: (set,add,replace,append,prepend,cas)
    #
    def set(self, key, value, flags=0, expired=0):
        '''
        Most common command. Store this data, possibly overwriting any existing data.
        New items are at the top of the LRU.
        '''

        self.cmd = '%s %s %d %d %d\r\n%s\r\n' % (
            'set', key, flags, expired, len(value), value)
        self.cmdlog.append(self.cmd)

        self.sock.sendall(self.cmd.encode())
        data = self.sock.recv(MAX_DATA_LENGTH)
        return data

    def add(self, key, value, flags=0, expired=0):
        '''
        Store this data, only if it does not already exist. New items are at the top of
        the LRU. If an item already exists and an add fails, it promotes the item to the
        front of the LRU anyway.
        '''

        self.cmd = '%s %s %d %d %d\r\n%s\r\n' % (
            'add', key, flags, expired, len(value), value)
        self.cmdlog.append(self.cmd)

        self.sock.sendall(self.cmd.encode())
        data = self.sock.recv(MAX_DATA_LENGTH)
        return data

    def replace(self, key, value, flags=0, expired=0):
        '''
        Store this data, but only if the data already exists. Almost never used,
        and exists for protocol completeness (set, add, replace, etc)
        '''

        self.cmd = '%s %s %d %d %d\r\n%s\r\n' % (
            'replace', key, flags, expired, len(value), value)
        self.cmdlog.append(self.cmd)

        self.sock.sendall(self.cmd.encode())
        data = self.sock.recv(MAX_DATA_LENGTH)
        return data

    def append(self, key, value, flags=0, expired=0):
        '''
        Add this data after the last byte in an existing item. This does not allow
        you to extend past the item limit. Useful for managing lists.
        '''

        self.cmd = '%s %s %d %d %d\r\n%s\r\n' % (
            'append', key, flags, expired, len(value), value)
        self.cmdlog.append(self.cmd)

        self.sock.sendall(self.cmd.encode())
        data = self.sock.recv(MAX_DATA_LENGTH)
        return data

    def prepend(self, key, value, flsgs=0, expired=0):
    	'''
    	Same as append, but adding new data before existing data.
    	'''

        self.cmd = '%s %s %d %d %d\r\n%s\r\n' % (
            'prepend', key, flags, expired, len(value), value)
        self.cmdlog.append(self.cmd)

        self.sock.sendall(self.cmd.encode())
        data = self.sock.recv(MAX_DATA_LENGTH)
        return data

    def cas(self, key, value, flags=0, expired=0, cas_value=0):
    	'''
    	Check And Set (or Compare And Swap). An operation that stores data, but only if
    	no one else has updated the data since you read it last. Useful for resolving race
    	conditions on updating cache data.
    	'''

        self.cmd = '%s %s %d %d %d %d\r\n%s\r\n' % (
            'cas', key, flags, expired, cas_value, len(value), value)
        self.cmdlog.append(self.cmd)

        self.sock.sendall(self.cmd.encode())
        data = self.sock.recv(MAX_DATA_LENGTH)
        return data

    #
    # Retrieval Commands: (get,gets,delete,incr/decr)
    #
    def get(self, key):
        '''
        Command for retrieving data. Takes one or more keys and returns all found items.
        '''

        self.cmd = '%s %s\r\n' % ('get', key)
        self.cmdlog.append(self.cmd)
        self.sock.sendall(self.cmd.encode())
        data = self.sock.recv(MAX_DATA_LENGTH)
        return data

    def gets(self,key):
        '''
        An alternative get command for using with CAS. Returns a CAS identifier
        (a unique 64bit number) with the item. Return this value with the cas command.
        If the item's CAS value has changed since you gets'ed it, it will not be stored.
        '''

        self.cmd = '%s %s\r\n' % ('gets', key)
        self.cmdlog.append(self.cmd)
        self.sock.sendall(self.cmd.encode())
        data = self.sock.recv(MAX_DATA_LENGTH)
        return data        

    def delete(self, key):
        '''Removes an item from the cache, if it exists.'''

        self.cmd = '%s %s\r\n' % ('delete', key)
        self.cmdlog.append(self.cmd)
        self.sock.sendall(self.cmd.encode())
        data = self.sock.recv(MAX_DATA_LENGTH)
        return data

    def incr(self, key):
    	'''
    	Increment and Decrement. If an item stored is the string representation of a 64bit
    	integer, you may run incr or decr commands to modify that number. You may only incr
    	by positive values, or decr by positive values. They does not accept negative values.

		If a value does not already exist, incr/decr will fail.
    	'''

        pass

    def decr(self, key):
    	'''
    	Increment and Decrement. If an item stored is the string representation of a 64bit
    	integer, you may run incr or decr commands to modify that number. You may only incr
    	by positive values, or decr by positive values. They does not accept negative values.

		If a value does not already exist, incr/decr will fail.
    	'''
        pass

    #
    # Statistics: (stats,stats items,stats slabs,stats sizes,flush_all)
    #
    def stats(self):
        '''ye 'ole basic stats command.'''

        self.cmd = '%s\r\n' % 'stats'
        self.cmdlog.append(self.cmd)

        self.sock.sendall(self.cmd.encode())
        data = self.sock.recv(MAX_DATA_LENGTH)
        return data

    def stats_items(self):
        '''Returns some information, broken down by slab, about items stored in memcached.'''

        self.cmd = '%s\r\n' % 'stats items'
        self.cmdlog.append(self.cmd)

        self.sock.sendall(self.cmd.encode())
        data = self.sock.recv(MAX_DATA_LENGTH)
        return data

    def stats_slabs(self):
        '''
        Returns more information, broken down by slab, about items stored in memcached.
        More centered to performance of a slab rather than counts of particular items.
        '''

        self.cmd = '%s\r\n' % 'stats slabs'
        self.cmdlog.append(self.cmd)

        self.sock.sendall(self.cmd.encode())
        data = self.sock.recv(MAX_DATA_LENGTH)
        return data

    def stats_sizes(self):
        '''
        A special command that shows you how items would be distributed if slabs were broken
        into 32byte buckets instead of your current number of slabs. Useful for determining
        how efficient your slab sizing is.

		WARNING this is a development command. As of 1.4 it is still the only command which
		will lock your memcached instance for some time. If you have many millions of stored
		items, it can become unresponsive for several minutes. Run this at your own risk. It
		is roadmapped to either make this feature optional or at least speed it up.
        '''

        self.cmd = '%s\r\n' % 'stats sizes'
        self.cmdlog.append(self.cmd)

        self.sock.sendall(self.cmd.encode())
        data = self.sock.recv(MAX_DATA_LENGTH)
        return data

    def flush_all(self):
    	# flush_all([timeout])
    	# lazy delete
        '''
        Invalidate all existing cache items. Optionally takes a parameter, which means to invalidate
        all items after N seconds have passed.

		This command does not pause the server, as it returns immediately. It does not free up or
		flush memory at all, it just causes all items to expire.
        '''

        self.cmd = '%s\r\n' % 'flush_all'
        self.cmdlog.append(self.cmd)

        self.sock.sendall(self.cmd.encode())
        data = self.sock.recv(MAX_DATA_LENGTH)
        return data

    def stats_reset(self):
    	pass

    # stats cachedump slab_id limit_num

if __name__ == '__main__':
    mc = Client('127.0.0.1:11211')
    mc.set('xs', 'xishvai')
    mc.set('yj', 'yangjun')
    data = mc.get('xs')
    print('get xs = ', data)

    data1 = mc.get('yj')
    print('get yj = ', data1)

    mc.replace('yj', 'youngsmart')
    print('get yj = ', mc.get('yj'))

    mc.add('xs', 'xishvai')  # NOT_STORED
    mc.delete('yj')

    mc.get('yj')

    mc.flush_all()
    print('get xs = ', mc.get('xs'))

    # for s in mc.cmdlog:
    #     print(s, ' ')
    # print('stats = ', mc.stats())
    # print('stats items= ', mc.stats_items())
    # print('stats slabs= ', mc.stats_slabs())
    # print('stats sizes= ', mc.stats_sizes())
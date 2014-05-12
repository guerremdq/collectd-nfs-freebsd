#!/usr/bin/env python
# Collectd
# Facundo Guerrero < guerremdq@gmail.com >
# FreeBSD cacti NFS stats parser
import os
import collectd

STATS_FILE = '/tmp/nfs_stats_output_collectd'


def generate_stats():

    nfs_command = '/usr/bin/nfsstat -s|/usr/bin/head -n8 |/usr/bin/tail -n6'
    stats_file = open(STATS_FILE, "w")
    stats = os.popen(nfs_command)
    stats_file.write(stats.read())


def clean():
    os.remove(STATS_FILE)


def read(data=None):

    generate_stats()

    f = open(STATS_FILE, "ro")
    a = dict()

    while True:
        line1 = f.readline().split()
        line2 = f.readline().split()
        if not line2:
            break
        i = 0
        for x in line1:
            a[line1[i]] = line2[i]
            i = i + 1
    f.close()
    send_stats(a)
    clean()


def send_stats(data=None):
    order = ("Getattr Setattr Lookup Access Readlink Read Write Create Mkdir Symlink Mknod Remove Rmdir Rename Link Readdir RdirPlus Fsstat Fsinfo PathConf Commit")
    for x in order.split():
        dispatch_stat(data[x], x.lower())


def dispatch_stat(result, name):
    """Read a key from info response data and dispatch a value"""
    if result is None:
        collectd.warning('nfs plugin: Value not found for %s' % name)
        return
    value = int(result)
    collectd.info('Sending value[counter]: %s=%s' % (name, value))

    val = collectd.Values(plugin='nfs')
    val.type = 'counter'
    val.type_instance = name
    val.values = [value]
    #print val
    val.dispatch()


collectd.register_read(read)
collectd.register_shutdown(clean)

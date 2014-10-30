# sockstat module for ganglia 3.1.x and above
# Copyright (C) Wang Jian <lark@linux.net.cn>, 2009

import os, sys
import time

last_poll_time = 0
sockstats = {
    'tcp_total': 0,
    'tcp_established': 0,
    'tcp_orphan': 0,
    'tcp_timewait': 0,
    'udp_total': 0 }

def metric_update():
    global sockstats

    f = open('/proc/net/sockstat', 'r')

    for l in f:
        line = l.split()
        if (line[0] == 'TCP:'):
            sockstats['tcp_total'] = int(line[2])
            sockstats['tcp_orphan'] = int(line[4])
            sockstats['tcp_established'] = int(line[2]) - int(line[4])
            sockstats['tcp_timewait'] = int(line[6])
            continue

        if (line[0] == 'UDP:'):
            sockstats['udp_total'] = int(line[2])
            continue

    f.close()

def metric_read(name):
    global last_poll_time
    global sockstats
    now_time = time.time()

    '''time skewed'''
    if now_time < last_poll_time:
        last_poll_time = now_time
        return 0

    '''we cache statistics for 2 sec, it's enough for polling all 3 counters'''
    if (now_time - last_poll_time) > 2:
        metric_update()
        last_poll_time = now_time

    return sockstats[name]

descriptors = [{
        'name': 'tcp_total',
        'call_back': metric_read,
        'time_max': 20,
        'value_type': 'uint',
        'units': 'Sockets',
        'slope': 'both',
        'format': '%u',
        'description': 'Total TCP sockets',
        'groups': 'network',
    },
    {
        'name': 'tcp_established',
        'call_back': metric_read,
        'time_max': 20,
        'value_type': 'uint',
        'units': 'Sockets',
        'slope': 'both',
        'format': '%u',
        'description': 'TCP established sockets',
        'groups': 'network',
    },
    {
        'name': 'tcp_timewait',
        'call_back': metric_read,
        'time_max': 20,
        'value_type': 'uint',
        'units': 'Sockets',
        'slope': 'both',
        'format': '%u',
        'description': 'TCP timewait sockets',
        'groups': 'network',
    },
    {
        'name': 'udp_total',
        'call_back': metric_read,
        'time_max': 20,
        'value_type': 'uint',
        'units': 'Sockets',
        'slope': 'both',
        'format': '%u',
        'description': 'Total UDP sockets',
        'groups': 'network',
    }]

def metric_init(params):
    return descriptors

def metric_cleanup():
    pass

# for unit testing
if __name__ == '__main__':
    metric_init(None)
    for d in descriptors:
        v = d['call_back'](d['name'])
        print '%s = %d' % (d['name'], v)
    print "----"

    while 1:
        time.sleep(1)
        for d in descriptors:
            v = d['call_back'](d['name'])
            print '%s = %d' % (d['name'], v)
        print "----"

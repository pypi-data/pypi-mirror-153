#!/usr/bin/python3

import json
import os
import sys
import glob

criteria = {'time':'', 'type':''}

for arg in sys.argv[1:]:
    if ':' in arg:
        n = arg.find(':')
        k = arg[:n]
        v = arg[n+1:]
        criteria[k] = v

matched = False

for filebeat_fn in glob.glob('/tmp/gluu-filebeat*'):
    if os.path.exists(filebeat_fn):
        with open(filebeat_fn) as f:
            for l in f:
                jl = json.loads(l)
                if not matched and jl['fields']['type'] == criteria['type'] and jl['@timestamp'] > criteria['time']:
                    matched = True

                if matched:
                    print(l, end=' ')

        if not matched:
            with open(filebeat_fn) as f:
                for l in f:
                    print(l, end=' ')

# -*- coding: UTF-8 -*-
# Copyright (c) 2018, Thomas Hartmann
#
# This file is part of the obob_condor Project, see: https://gitlab.com/obob/obob_condor
#
#    obob_condor is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    obob_condor is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with obob_subjectdb. If not, see <http://www.gnu.org/licenses/>.
import datetime
import sys
import os
import socket
import subprocess
import six

os.chdir('{{ working_directory }}')

sys.path.append(os.getcwd())

requested_ram = {{ requested_ram }} / 1024

from obob_condor.job import JobItem

def get_classad(classad, clusterid, procid):
    if isinstance(clusterid, six.string_types):
        clusterid = int(clusterid)

    if isinstance(procid, six.string_types):
        procid = int(procid)

    if clusterid == 0:
        return None

    output = subprocess.check_output(('/usr/bin/condor_q', '%d.%d' % (clusterid, procid), '-autoformat', classad)).decode('utf-8')

    return output

if __name__ == '__main__':
    condor_classadd = os.environ.get('_CONDOR_JOB_AD', None)

    job_info = {
        'ClusterId': 0,
        'ProcId': 0,
        'requested_ram': requested_ram,
    }

    if condor_classadd:
        classad_dict = dict()
        with open(condor_classadd, 'rt') as classad_file:
            for line in classad_file:
                if ' = ' in line:
                    (key, val) = line.split(' = ')
                    classad_dict[key.strip()] = val.strip()

        job_info['ClusterId'] = int(classad_dict['ClusterId'])
        job_info['ProcId'] = int(classad_dict['ProcId'])

    job_item = JobItem(sys.argv[1])

    job_object = job_item.make_object()

    job_started = datetime.datetime.now()

    print('Running on: %s' % (socket.gethostname(), ))
    print('Now running %s' % (job_item, ))
    print('Parameters: %s' % (job_item.args, ))
    print('Keyword Parameters: %s' % (job_item.kwargs, ))
    print('\nThe job has the ID: %d.%d' % (job_info['ClusterId'], job_info['ProcId']))

    print(f'Starting Job at {job_started}\n##########')
    job_object.run_private()
    job_stopped = datetime.datetime.now()
    print(f'##########\nJob stopped at {job_stopped}')
    print(f'Execution took {job_stopped - job_started}')
    mem_used_raw = get_classad('MemoryUsage', job_info['ClusterId'], job_info['ProcId'])
    if mem_used_raw.startswith('undefined'):
        mem_used = 0
    else:
        mem_used = int(mem_used_raw) / 1024

    if mem_used < 0.5:
        mem_used = requested_ram

    mem_toomuch = 100 * (requested_ram - mem_used) / mem_used

    print('Your job asked for %.2fGB of RAM' % (requested_ram, ))
    print('Your job used a maximum of %.2fGB of RAM' % (mem_used, ))
    print('You overestimated you memory usage by %.2f%%.' % (mem_toomuch,  ))
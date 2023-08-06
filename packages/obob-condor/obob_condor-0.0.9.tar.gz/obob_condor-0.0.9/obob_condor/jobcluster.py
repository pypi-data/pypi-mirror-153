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

import getpass
import humanfriendly
import six
import sys
import os
import os.path
import obob_condor.job
import subprocess
import logging
import glob
import jinja2
import uuid
import numpy
import itertools
import copy
import collections
import inspect
import shutil

from obob_condor.job import JobItem

if sys.version_info >= (3, 6):
    import pathlib
else:
    import pathlib2 as pathlib

class JobCluster(object):
    """
    This is the main class, the *controller* of obob_condor. It collects all the jobs and takes care of submitting them
    to the cluster. It also contains information about how much RAM the jobs need, how many CPUs are requested etc.

    Parameters
    ----------
    required_ram : :class:`str`, :class:`float`, :class:`int`, optional
        The amount of RAM required to run one Job in megabytes. A string like "2G" or "200M" will be converted accordingly.
    adjust_mem : :class:`bool`, optional
        If True, the job will be restarted automatically if it gets killed by condor because it uses too much RAM.
    request_cpus : :class:`int`, optional
        The number of CPUs requested
    jobs_dir ::class:`str`, optional
        Folder to put all the jobs in. This one needs to be on the shared filesystem (so somewhere under /mnt/obob)
    inc_jobsdir ::class:`str`, optional
        If this is set to True (default), jobs_dir is the parent folder for all the jobs folders. Each time a job is
        submitted, a new folder is created in the jobs_dir folder that contains all the necessary files and a folder
        called "log" containing the log files. If jobs_dir is set to False, the respective files are put directly
        under jobs_dir. In this case, jobs_dir must either be empty or not exist at all to avoid any side effects.
    owner ::class:`str`, optional
        Username the job should run under. If you submit your jobs from one of the bombers, you do not need to set this.
        If you have set up your local machine to submit jobs and your local username is different from your username
        on the cluster, set owner to that username.
    python_bin ::class:`str`, optional
        The path to the python interpreter that should run the jobs. If you do not set it, it gets chosen automatically.
        If the python interpreter you are using when submitting the jobs is on /mnt/obob/ that one will be used.
        If the interpreter you are using is **not** on /mnt/obob/ the default one at /mnt/obob/obob_mne will be used.
    working_directory ::class:`str`, optional
        The working directory when the jobs run.
    singularity_image ::class:`str`, optional
        Set this to a singularity image to have the jobs execute in it. Can be a link to a local file or to some online
        repository.
    """

    _default_python_env = '/mnt/obob/obob_mne/bin/python'
    _obob_condor_runner = 'obob_condor.runner'
    _condor_submit = '/usr/bin/condor_submit'
    _runner_template = 'runner.py'
    _submit_template = 'submit.sub'

    def __init__(self, required_ram='2G', adjust_mem=True, request_cpus=1, jobs_dir='jobs',
                 inc_jobsdir=True, owner=None, python_bin=None, working_directory=None,
                 singularity_image=None):
        self.required_ram = required_ram
        self.adjust_mem = adjust_mem
        self.request_cpus = request_cpus
        self.jobs_dir = jobs_dir
        self.inc_jobsdir = inc_jobsdir
        self.owner = owner
        self.python_bin = python_bin
        self.working_directory = working_directory
        self._condor_output_folder = None
        self._singularity_image = singularity_image

        self._jobs = list()

        self._jinja_env = jinja2.Environment(loader=jinja2.PackageLoader('obob_condor', 'jinja2_templates'),
                                             trim_blocks=True, lstrip_blocks=True)

    def add_job(self, job, *args, **kwargs):
        """
        Add one job to the JobCluster. All further arguments will be passed on to the Job.

        Parameters
        ----------
        job : child of :class:`obob_condor.Job`
            The job class to be added.

        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.
        """

        if not obob_condor.job.Job in inspect.getmro(job):
            raise TypeError('Job must be a subclass of obob_condor.Job')

        kwargs = collections.OrderedDict(kwargs)
        args_permuted = [idx for (idx, cur_arg) in enumerate(args) if isinstance(cur_arg, PermuteArgument)]
        kwargs_permuted = [idx for (idx, cur_key) in enumerate(kwargs.keys()) if
                           isinstance(kwargs[cur_key], PermuteArgument)]

        if not args_permuted and not kwargs_permuted:
            self._jobs.append(JobItem(job, *args, **kwargs))
        else:
            all_kwargs_as_array = numpy.array([kwargs[cur_key] for (idx, cur_key) in enumerate(kwargs.keys()) if idx in kwargs_permuted])
            all_args_as_array = numpy.hstack((numpy.array(args)[args_permuted], all_kwargs_as_array))
            all_args_permutations = itertools.product(*[x.args for x in all_args_as_array])
            for cur_perm_args in all_args_permutations:
                new_args = numpy.array(args)
                new_kwargs = copy.deepcopy(kwargs)
                cur_perm_args_list = list(cur_perm_args)
                if args_permuted:
                    new_args[args_permuted] = cur_perm_args_list[0:len(args_permuted)]
                    del cur_perm_args_list[0:len(args_permuted)]

                if kwargs_permuted:
                    for idx, cur_kwarg_idx in enumerate(kwargs_permuted):
                        new_kwargs[list(new_kwargs.keys())[cur_kwarg_idx]] = cur_perm_args_list[idx]

                self.add_job(job, *new_args, **new_kwargs)

    def run_local(self):
        """
        Runs the added jobs locally.

        """

        self._remove_notrunning_jobs()
        self._prepare_jobs_directory()
        self._generate_runner_file()
        submit_fname = self._generate_submit_file()

        submit_dict = dict()
        queue_glob = None
        with open(submit_fname, 'rt') as submit_file:
            for line in submit_file:
                if ' = ' in line:
                    (key, val) = line.split(' = ')
                    submit_dict[key.strip()] = val.strip()
                elif line.startswith('queue'):
                    queue_glob = line.rsplit(' ', 1)[1]

        for idx, cur_file in enumerate(sorted(glob.glob(queue_glob))):
            with open(os.path.join(self.condor_output_folder, 'log', 'out.%d' % (idx,)), 'wt') as out, \
                    open(os.path.join(self.condor_output_folder, 'log', 'err.%d' % (idx,)), 'wt') as err:
                this_args = submit_dict['arguments'].replace('$(filename)', os.path.abspath(cur_file))[2:-1].split(' ')

                subprocess.call([submit_dict['executable'],  this_args[0], this_args[1]], cwd=self.working_directory, stderr=err, stdout=out)

    def submit(self, do_submit=True):
        """
        Runs the added jobs on the cluster.

        Parameters
        ----------
        do_submit : :class:`bool`, optional
            Set this to false to not actually submit but prepare all files.

        """

        self._remove_notrunning_jobs()
        self._prepare_jobs_directory()
        self._generate_runner_file()
        submit_fname = self._generate_submit_file()

        if do_submit:
            output = subprocess.check_output([self._condor_submit, submit_fname], stderr=subprocess.STDOUT, cwd=self.working_directory)
            print('Submit output:\n%s\n' % (output, ))
        else:
            logging.info('Not actually submitting')

    def _remove_notrunning_jobs(self):
        new_job_list = []
        for cur_job in self._jobs:
            cur_job_object = cur_job.make_object()
            if cur_job_object.shall_run_private():
                new_job_list.append(cur_job)

        self._jobs = new_job_list

    def _generate_submit_file(self):

        template = self._jinja_env.get_template(self._submit_template)
        submit_context = {
            'executable': self.executable,
            'arguments': self.arguments,
            'jobs_dir': self.condor_output_folder,
            'required_mem': int(self.required_ram / 1024 / 1024),
            'request_cpus': self.request_cpus,
            'owner': self.owner,
            'uuid': str(uuid.uuid4()),
            'python_home': self.python_home,
        }

        submit_rendered = template.render(submit_context)
        submit_fname = os.path.join(self.condor_output_folder, 'condor', 'submit.sub')
        with open(submit_fname, 'wt') as submit_file:
            submit_file.write(submit_rendered)

        return submit_fname

    def _generate_runner_file(self):
        template = self._jinja_env.get_template(self._runner_template)
        runner_context = {
            'requested_ram': int(self.required_ram / 1024 / 1024),
            'working_directory': self.working_directory
        }

        runner_rendered = template.render(runner_context)
        with open(self.runner_filename, 'wt') as runner_file:
            runner_file.write(runner_rendered)

    def _prepare_jobs_directory(self):
        final_jobs_dir = None
        if self.inc_jobsdir:
            pathlib.Path(self.jobs_dir).mkdir(exist_ok=True)

            jobs_idx = 1
            while os.path.exists(os.path.join(self.jobs_dir, '%03d' % (jobs_idx, ))):
                jobs_idx = jobs_idx + 1

            final_jobs_dir = os.path.join(self.jobs_dir, '%03d' % (jobs_idx, ))
        else:
            final_jobs_dir = self.jobs_dir
            if os.path.exists(final_jobs_dir):
                raise ValueError('The jobs folder already exists. Please choose another one')

        pathlib.Path(final_jobs_dir).mkdir(exist_ok=True)

        json_folder = os.path.join(final_jobs_dir, 'condor')
        pathlib.Path(json_folder).mkdir(exist_ok=True)
        log_folder = os.path.join(final_jobs_dir, 'log')
        pathlib.Path(log_folder).mkdir(exist_ok=True)

        idx = 1
        for cur_job in self._jobs:
            cur_job.to_json(os.path.join(json_folder, 'job%03d.json.gzip' % (idx, )))
            idx = idx + 1

        self._condor_output_folder = os.path.abspath(final_jobs_dir)

        shutil.copytree(os.path.split(inspect.getsourcefile(inspect.getmodule(JobItem)))[0], os.path.join(json_folder, 'obob_condor'))

        return final_jobs_dir

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        if not owner:
            owner = getpass.getuser()
        self._owner = owner

    @property
    def required_ram(self):
        return self._required_ram

    @required_ram.setter
    def required_ram(self, required_ram):
        if isinstance(required_ram, six.string_types):
            required_ram = humanfriendly.parse_size(required_ram)

        if not isinstance(required_ram, (int, float)):
            raise TypeError('required_ram must be either a string or a number.')

        self._required_ram = required_ram

    @property
    def python_bin(self):
        return self._python_bin

    @python_bin.setter
    def python_bin(self, python_bin):
        if not python_bin:
            python_bin = sys.executable
            if not python_bin.startswith('/mnt/obob/'):
                logging.warning('Your current python distribution is not on /mnt/obob.\n'
                                'Using the default one in /mnt/obob/obob_mne now.\n'
                                'If you want to use a different one, please specify it explicitly in the constructor.')

                python_bin = self._default_python_env

        if not os.path.isfile(python_bin):
            raise ValueError('The python interpreter does not exist.')

        if not 'Python' in str(subprocess.check_output([python_bin, '-V'], stderr=subprocess.STDOUT)):
            raise ValueError('Cannot execute the python interpreter or it is not a python interpreter')

        self._python_bin = python_bin

    @property
    def singularity_command(self):
        return '/usr/bin/singularity'

    @property
    def singularity_arguments(self):
        return f'exec -S /home/{self.owner} -B /var/lib/condor -B /mnt --no-home --writable-tmpfs {self._singularity_image} ' \
               f'{self.python_bin} {self.runner_filename}'

    @property
    def executable(self):
        if self._singularity_image is not None:
            return self.singularity_command
        else:
            return self.python_bin

    @property
    def arguments(self):
        if self._singularity_image is not None:
            return self.singularity_arguments
        else:
            return self.runner_filename

    @property
    def python_home(self):
        return os.path.dirname(os.path.dirname(self.python_bin))

    @property
    def working_directory(self):
        return self._working_directory

    @working_directory.setter
    def working_directory(self, working_directory):
        if not working_directory:
            working_directory = os.getcwd()

        if not os.path.isdir(working_directory):
            raise ValueError('working_directory is not a valid directory.')

        if not working_directory.startswith('/mnt/obob/'):
            logging.warning('working_directory is not on the storage. This will not work on the real cluster!')

        self._working_directory = working_directory

    @property
    def condor_output_folder(self):
        return self._condor_output_folder

    @property
    def n_jobs(self):
        return len(self._jobs)

    @property
    def runner_filename(self):
        return os.path.join(self.condor_output_folder, 'condor', 'runner.py')


class PermuteArgument(object):
    """
    This is a container for to-be-permuted arguments. See the example in the introductions for details.
    """
    def __init__(self, args):
        self.args = args


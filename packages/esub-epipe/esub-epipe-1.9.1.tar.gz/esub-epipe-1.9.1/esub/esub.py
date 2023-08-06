#! /usr/bin/env python

# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

# System imports
from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

# package import
import argparse
import math
import os
import sys
import collections
from esub import utils
from ekit import logger as logger_utils


LOGGER = logger_utils.init_logger(__name__)
TIMEOUT_MESSAGE = 'Maximum number of pending jobs reached, ' \
                  'will sleep for 30 minutes and retry'


def starter_message():
    print(' ')
    print("                   ______   ")
    print("________________  ____  /_  ")
    print("_  _ \\_  ___/  / / /_  __ \\ ")
    print("/  __/(__  )/ /_/ /_  /_/ / ")
    print("\\___//____/ \\__,_/ /_.___/  ")
    print(' ')


def main(args=None):
    """
    Main function of esub.

    :param args: Command line arguments that are parsed
    """

    if args is None:
        args = sys.argv[1:]

    # initializing parser
    description = "This is esub an user friendly and flexible tool to " \
                  "submit jobs to a cluster or run them locally"
    parser = argparse.ArgumentParser(description=description, add_help=True)

    # deault for resources
    resources = dict(main_memory=1000,
                     main_time=4,
                     main_time_per_index=None,
                     main_scratch=2000,
                     watchdog_memory=1000,
                     watchdog_time=4,
                     watchdog_scratch=2000,
                     merge_memory=1000,
                     merge_time=4,
                     merge_scratch=2000)

    # parse all the submitter arguments
    parser.add_argument('exec', type=str,
                        help='path to the executable (python file '
                        'containing functions main, watchdog, merge)')
    parser.add_argument('--mode', type=str, default='run',
                        choices=('run', 'jobarray', 'mpi',
                                 'run-mpi', 'run-tasks'),
                        help='The mode in which to operate. '
                        'Choices: run, jobarray, mpi, run-mpi, '
                        'run-tasks')
    parser.add_argument('--job_name', type=str, default='job',
                        help='Individual name for this job. CAUTION: '
                             'Multiple jobs with same name'
                             'can confuse system!')
    parser.add_argument('--source_file', type=str, default='source_esub.sh',
                        help='Optionally provide a source file which '
                        'gets executed on the computing '
                        'node before your jobs are started.'
                        'Useful for loading modules, '
                        'declaring environemental variables and so on')
    parser.add_argument('--main_memory', type=float,
                        default=resources['main_memory'],
                        help='Memory allocated per core for main '
                        'job in MB. Default: 1000 MB')
    parser.add_argument('--main_time', type=float,
                        default=resources['main_time'],
                        help='Job run time limit in hours for'
                        ' main job. Default 4h')
    parser.add_argument('--main_time_per_index', type=float,
                        default=resources['main_time_per_index'],
                        help='Job run time limit in hours for main '
                             'job per index, overwrites main_time if set.')
    parser.add_argument('--main_scratch', type=float,
                        default=resources['main_scratch'],
                        help='Local scratch memory allocated '
                        'for main job in MB. Default 2000 MB')
    parser.add_argument('--watchdog_memory', type=float,
                        default=resources['watchdog_memory'],
                        help='Memory allocated per core '
                             'for watchdog job in MB. Default: 1000 MB')
    parser.add_argument('--watchdog_time', type=float,
                        default=resources['watchdog_time'],
                        help='Job run time limit in hours '
                        'for watchdog job. Default: 4h')
    parser.add_argument('--watchdog_scratch', type=float,
                        default=resources['watchdog_scratch'],
                        help='Local scratch memory allocated '
                        'for watchdog job. Default: 2000 MB')
    parser.add_argument('--merge_memory', type=float,
                        default=resources['merge_memory'],
                        help='Memory allocated per core for '
                        'merge job in MB. Default: 1000 MB')
    parser.add_argument('--merge_time', type=float,
                        default=resources['merge_time'],
                        help='Job run time limit in hours '
                        'for merge job. Default: 4h')
    parser.add_argument('--merge_scratch', type=float,
                        default=resources['merge_scratch'],
                        help='Local scratch memory allocated '
                        'for merge job. Default: 2000 MB')
    parser.add_argument('--function', type=str, default='main',
                        help='The functions that should be executed. '
                        'Choices: main, watchdog, merge, '
                        'rerun_missing, check_missing, all, '
                        'or a list separated by whitespaces.')
    parser.add_argument('--main_name', type=str, default='main',
                        help='Name of the main function in the executable.')
    parser.add_argument('--tasks', type=str, default='0',
                        help='Task string from which the indices are parsed. '
                             'Either single index, list of '
                             'indices (format 0,1,2 ), a range '
                             'looking like int1 > int2 or path '
                             'to a text file that holds '
                             'a string in the format of the '
                             'beforementioned formats.')
    parser.add_argument('--n_cores', type=int, default=-1,
                        help='The number of cores to '
                        'request for the main function (DEPRECATED).')
    parser.add_argument('--n_jobs', type=int, default=1,
                        help='The number of jobs to '
                        'request for the main function.')
    parser.add_argument('--max_njobs', type=int, default=-1,
                        help='The maximal number of jobs that are allowed '
                        'to run at the same time.')
    parser.add_argument('--dependency', type=str, default='',
                        help='A dependency string that gets added to the '
                             'dependencies (example after(<jobid>).')
    parser.add_argument('--system', type=str, default='bsub',
                        choices=('bsub', 'slurm'),
                        help='Type of the system. '
                        'Default is bsub (IBMs LSF system).'
                        'Support for slurm is expermimental!')
    parser.add_argument('--log_dir', type=str,
                        default=os.path.join(os.getcwd(), 'esub_logs'),
                        help='Directory where to write the logs to. '
                        'By default uses the current working directory.')
    parser.add_argument('--test', action='store_true',
                        default=False,
                        help='Test mode. Will not submit '
                        'the jobs but only print.')
    parser.add_argument('--discard_output', action='store_true',
                        default=False,
                        help='If True all stdout/stderr is '
                        'written to /dev/null.')
    parser.add_argument('--batchsize', type=int,
                        default=100000,
                        help='The maximum length of a jobarray. If requesting'
                        ' a larger jobarray it will automatically get '
                        'split into smaller ones. Default: 100000')
    parser.add_argument('--additional_args', type=str, default='',
                        help='Can pass comma-separated, additional, '
                        'cluster-specific arguemnts. e.g. '
                        '--additional_args="-C knl,--exclusive" to request '
                        'only KNL nodes and to not share nodes with other '
                        'users. The availablility of such arguments depends '
                        'on the cluster you are using.')
    parser.add_argument('--additional_bsub_args', type=str, default='',
                        help='Additional arguments for the LSF system. '
                        'Example: \'-R "span[ptile=100]"\' to request that '
                        'all 100 cores are on the same computing node')
    parser.add_argument('--esub_verbosity', type=int,
                        default=3, choices=(0, 1, 2, 3, 4),
                        help='esub verbosity. From 0-4 with 4 being '
                        'the most verbose. Default is 3 (info).')
    parser.add_argument('--main_n_cores_per_job', type=int,
                        default=1,
                        help='Number of cores per job for the main function. '
                        'Default: 1')
    parser.add_argument('--watchdog_n_cores', type=int,
                        default=1,
                        help='Number of cores per job for the watchdog. '
                        'fuction. Default: 1')
    parser.add_argument('--merge_n_cores', type=int,
                        default=1,
                        help='Number of cores per job for the merge. '
                        'Default: 1')
    parser.add_argument('--mpi_merge', action='store_true',
                        default=False,
                        help='If True merge function is run as an MPI job. '
                        'Otherwise as a normal job with merge_cores.')
    parser.add_argument('--mpi_watchdog', action='store_true',
                        default=False,
                        help='If True watchdog function is run as an MPI job. '
                        'Otherwise as a normal job with watchdog_cores.')

    args, function_args = parser.parse_known_args(args)

    logger_utils.set_logger_level(LOGGER, args.esub_verbosity)

    if args.n_cores > -1:
        LOGGER.warning(
            "DEPRECATION WARNING: The n_cores option will be dropped in a "
            "future version. Use n_jobs instead.")
        args.n_jobs = args.n_cores

    # Make log directory if non existing
    log_dir = args.log_dir
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
        LOGGER.debug('Created log directory {}'.format(log_dir))

    mode = args.mode
    add_args = args.additional_args
    main_name = args.main_name
    job_name = args.job_name
    source_file = args.source_file
    tasks = args.tasks
    exe = args.exec
    n_jobs = args.n_jobs
    main_n_cores = args.main_n_cores_per_job
    watchdog_n_cores = args.watchdog_n_cores
    merge_n_cores = args.merge_n_cores
    function = args.function
    system = args.system
    if system == 'slurm':
        LOGGER.warning(
            "Support for slurm is experimental and only some basic features "
            "of esub-epipe are supported!")
    ext_dependencies = args.dependency

    # Make sure that executable exits
    if os.path.isfile(exe):
        if not os.path.isabs(exe):
            exe = os.path.join(os.getcwd(), exe)
            LOGGER.debug(f"Using executable file at {exe}")
    else:
        raise FileNotFoundError(
            'Did not find {}. Please specify a valid path for '
            'executable'.format(exe))

    starter_message()

    # Set path to log file and to file storing finished main job ids
    path_log = utils.get_path_log(log_dir, job_name)
    LOGGER.debug(f"Using log file at {path_log}")

    path_finished = utils.get_path_finished_indices(log_dir, job_name)
    LOGGER.debug(f"Storing finished indices at {path_finished}")
    LOGGER.info("Running in run mode {}".format(mode))

    # importing the functions from the executable
    executable = utils.import_executable(exe)

    # check if required function exists. Otherwise skip it
    if ',' in function:
        function = function.split(',')
    else:
        function = [function]
    if (len(function) == 1) and (function[0] == 'all'):
        function = 'all'
    if function == 'all':
        function = ['main', 'rerun_missing', 'watchdog', 'merge']
    for func in function:
        if func == 'rerun_missing':
            continue
        elif func == 'main':
            if not hasattr(executable, main_name):
                LOGGER.warning(
                    "Did not find main function {} in the executable. "
                    "Skipping it...".format(main_name))
                function.remove(func)
        else:
            if not hasattr(executable, func):
                LOGGER.warning(
                    "Did not find function {} in the executable. "
                    "Skipping it...".format(func))
                function.remove(func)
    if len(function) == 0:
        LOGGER.warning("No function to run found. Exiting.")
        sys.exit(0)

    # run setup if implemented
    if hasattr(executable, 'setup'):
        LOGGER.info('Running setup function from executable')
        getattr(executable, 'setup')(function_args)

    # get resources from executable if implemented
    res_update = dict()
    if hasattr(executable, 'resources'):
        LOGGER.info(
            'Running resources function from executable. '
            'Updating resource requirements.')
        res_update = getattr(executable, 'resources')(function_args)

    # overwrite with non-default command-line input
    for res_name, res_default_val in resources.items():
        res_cmd_line = getattr(args, res_name)
        if res_cmd_line != res_default_val:
            res_update[res_name] = res_cmd_line
            LOGGER.debug(
                f'Overriding default resource {res_name}: '
                f'{res_default_val} -> {res_cmd_line}')
    resources.update(res_update)

    if resources['main_time_per_index'] is not None:
        n_indices = len(utils.get_indices(tasks))
        resources['main_time'] = resources['main_time_per_index'] * \
            math.ceil(n_indices / n_jobs)
        LOGGER.debug(
            f"main_time_per_index is set -> Overriding "
            f"main_time to {resources['main_time']}h")
    del resources['main_time_per_index']

    # check if log files should be overwritten
    overwrite_log = (function == 'all') | (function == 'main')

    # CASE 1 : run locally
    if (mode == 'run') | (mode == 'run-mpi') | (mode == 'run-tasks'):
        LOGGER.info("Running locally!")

        # adding function and tasks arguments
        if function == 'all':
            LOGGER.debug("Running all functions sspecified in executable")
        else:
            LOGGER.debug(
                "Running the function(s) {} "
                "specified in executable".format(', '.join(function)))

        # getting index list
        indices = utils.get_indices(tasks)
        LOGGER.info("Running on tasks: {}".format(indices))

        # loop over functions
        for f in function:

            LOGGER.info(f"Running function {f}")
            indices_use = indices

            # check if function is specified
            if f == 'main' or f == 'rerun_missing':
                function_found = hasattr(executable, main_name)
            else:
                function_found = hasattr(executable, f)

            if not function_found:
                LOGGER.warning(
                    "The requested function {} is missing in the executable. "
                    "Skipping...".format(f))
                continue

            if f == 'main':
                # resetting missing file
                LOGGER.debug("Resetting file holding finished indices")
                utils.robust_remove(path_finished)

            if f == 'rerun_missing':
                indices_use = utils.check_indices(
                    indices, path_finished, executable,
                    function_args, verbosity=args.esub_verbosity)
                if len(indices_use) > 0:
                    LOGGER.info("Rerunning tasks: {}".format(indices_use))
                    f = 'main'
                else:
                    LOGGER.info('All indices are finished, nothing to re-run.')
                    continue

            if f == 'check_missing':
                indices_use = utils.check_indices(
                    indices, path_finished, executable, function_args,
                    check_indices_file=False, verbosity=args.esub_verbosity)
                if len(indices_use) > 0:
                    LOGGER.info("Rerunning tasks: {}".format(indices_use))
                    f = 'main'
                else:
                    LOGGER.info('All indices are finished, nothing to re-run.')
                    continue

            if f == 'main':
                if mode == 'run':
                    for index in getattr(executable, main_name)(indices,
                                                                function_args):
                        LOGGER.info(
                            "##################### Starting Task {} "
                            "#####################".format(index))
                        utils.write_index(index, path_finished)
                        LOGGER.info(
                            "##################### Finished Task {} "
                            "#####################".format(index))

                elif mode == 'run-mpi':
                    LOGGER.info(
                        "##################### Starting MPI job"
                        "#####################")
                    utils.run_local_mpi_job(
                        exe, main_n_cores, function_args, LOGGER,
                        main_name, args.esub_verbosity)
                    LOGGER.info(
                        "##################### Finished MPI job"
                        "#####################")

                elif mode == 'run-tasks':
                    LOGGER.info(
                        "##################### Starting parallel tasks {} "
                        "#####################".format(tasks))
                    dones = utils.run_local_tasks(
                        executable, n_jobs, function_args, tasks, main_name)
                    for index in dones:
                        utils.write_index(index, path_finished)
                        LOGGER.info(
                            "##################### Finished Task {} "
                            "#####################".format(index))

            else:
                getattr(executable, f)(indices_use, function_args)

    # CASE 2 and 3 : running jobs on cluster (MPI or jobarray)
    elif (mode == 'jobarray') | (mode == 'mpi') | (mode == 'tasks'):
        # Add dependencies to functions
        if (function == 'all') & (mode == 'jobarray'):
            function = ['main', 'watchdog', 'rerun_missing', 'merge']
            LOGGER.info(
                "Submitting all functions specified in executable "
                "to queuing system. Watchdog running along "
                "main. Trying to rerun jobs after main finished. "
                "Merge running at the end.")
        elif (function == 'all') & ((mode == 'mpi') | (mode == 'tasks')):
            function = ['main', 'watchdog', 'merge']
            LOGGER.info(
                "Submitting all functions specified in executable "
                "to queuing system. Watchdog running along "
                "main. Merge running at the end.")
        else:
            LOGGER.info(
                "Submitting the function(s) {} specified in "
                "executable to queuing system".
                format(', '.join(function)))

        jobids = collections.OrderedDict()
        for ii, f in enumerate(function):
            if (f == 'main') or (f == 'rerun_missing') or (
                    f == 'check_missing'):
                function_found = hasattr(executable, main_name)
            else:
                function_found = hasattr(executable, f)

            if not function_found:
                LOGGER.warning(
                    "The requested function {} is missing in the executable. "
                    "Skipping...".format(f))
                continue

            if f == 'main':
                # resetting missing file
                LOGGER.debug("Resetting file holding finished indices")
                utils.robust_remove(path_finished)
                n_jobs_use = n_jobs
                n_cores_use = main_n_cores
                mode_ = mode
            elif f == 'watchdog':
                n_jobs_use = 1
                n_cores_use = watchdog_n_cores
                if args.mpi_watchdog:
                    mode_ = 'mpi'
                else:
                    mode_ = 'jobarray'
            elif f == 'merge':
                n_jobs_use = 1
                n_cores_use = merge_n_cores
                if args.mpi_merge:
                    mode_ = 'mpi'
                else:
                    mode_ = 'jobarray'
            else:
                # reruns
                n_jobs_use = 1
                n_cores_use = main_n_cores
                mode_ = mode

            LOGGER.debug(
                f"Submitting function {f} broken down "
                f"into {n_jobs_use} job(s)")

            # reset logs
            LOGGER.debug('Resetting log files')
            stdout_log, stderr_log = utils.get_log_filenames(
                log_dir, job_name, f)
            utils.robust_remove(stdout_log)
            utils.robust_remove(stderr_log)

            # the current job depends at most on the previous one
            # (e.g., rerun_missing does not need to wait for the
            # watchdog to finish)
            dependency = utils.get_dependency_string(
                f, jobids, ext_dependencies, system,
                verbosity=args.esub_verbosity)

            jobid = utils.submit_job(tasks, mode_, exe, log_dir, function_args,
                                     function=f,
                                     source_file=source_file,
                                     n_jobs=n_jobs_use,
                                     n_cores=n_cores_use,
                                     job_name=job_name,
                                     dependency=dependency,
                                     system=system,
                                     main_name=main_name,
                                     test=args.test,
                                     add_args=add_args,
                                     batchsize=args.batchsize,
                                     max_njobs=args.max_njobs,
                                     add_bsub=args.additional_bsub_args,
                                     discard_output=args.discard_output,
                                     verbosity=args.esub_verbosity,
                                     main_mode=mode,
                                     main_n_cores=main_n_cores,
                                     **resources)
            jobids[f] = jobid

            LOGGER.info(
                "Submitted job for function {}. "
                "Got jobid(s) {}".format(f, jobid))

        jobid_str = ''
        for jobid_list in jobids.values():
            if isinstance(jobid_list, int):
                jobid_str += f'{str(jobid_list)} '
            elif isinstance(jobid_list, list):
                for id in jobid_list:
                    jobid_str += f'{str(id)} '
            else:
                pass
        if len(jobid_str) == 0:
            jobid_str = 'None'

        LOGGER.info("Submission finished")
        print(f"Submitted jobids: {jobid_str}")

        # write to log
        if overwrite_log:
            utils.write_to_log(
                path_log, 'esub arguments: \n{}'.format(args), mode='w')
            utils.write_to_log(
                path_log, 'function arguments: \n{}'.format(function_args))

        for fun, jobid in jobids.items():
            utils.write_to_log(path_log, 'Job id {}: {}'.format(fun, jobid))


if __name__ == '__main__':
    main()

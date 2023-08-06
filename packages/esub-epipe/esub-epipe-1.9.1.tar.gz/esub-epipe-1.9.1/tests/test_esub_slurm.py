# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import os
import shutil
import shlex
import subprocess


def check_slurm_file():
    pass


def run_exec_example(test_dir, log_dir, mode='run', tasks_string=None,
                     extra_esub_args=''):

    # path to example file
    path_example = 'example/exec_example.py'

    # build command
    cmd = 'esub {} --mode={} --output_directory={}' \
        ' --log_dir={} --esub_verbosity=4 {}'.format(
            path_example,
            mode, test_dir,
            log_dir,
            extra_esub_args)
    if tasks_string is not None:
        cmd += ' --tasks={}'.format(tasks_string)

    # main function
    subprocess.call(shlex.split(cmd))
    check_slurm_file()

    subprocess.call(shlex.split(cmd + ' --function=main'))
    check_slurm_file()

    # watchdog
    subprocess.call(shlex.split(cmd + ' --function=watchdog'))
    check_slurm_file()

    # merge
    subprocess.call(shlex.split(cmd + ' --function=merge'))
    check_slurm_file()

    # all functions
    subprocess.call(shlex.split(cmd + ' --function=all'))
    check_slurm_file()


def test_esub_jobarray():

    # create directory for test output
    cwd = os.getcwd()
    path_testdir = 'esub_test_dir_submit_slurm'
    path_logdir = f'{cwd}/esub_test_dir_submit_slurm_log'
    if not os.path.isdir(path_testdir):
        os.mkdir(path_testdir)

    extra = '--test --main_memory=50000 --main_time_per_index=100 '\
            '--main_scratch=100000 --watchdog_memory=2400 --watchdog_time=50 '\
            '--watchdog_scratch=90000 --merge_time=30 --merge_memory=98000 '\
            '--merge_scratch=100000 --n_jobs=100 --system=slurm ' \
            '--additional_args=\"-C knl, --exclusive\"'
    # test with no tasks provided
    run_exec_example(path_testdir, path_logdir, mode='jobarray',
                     extra_esub_args=extra,
                     tasks_string='"1 > 3"')

    # remove directory for test output
    shutil.rmtree(path_testdir)

    # check that log directory was created and remove it then
    assert os.path.isdir(path_logdir)
    shutil.rmtree(path_logdir)
    subprocess.call('rm submit.slurm', shell=1)


def test_esub_mpi():

    # create directory for test output
    cwd = os.getcwd()
    path_testdir = 'esub_test_dir_mpi_slurm'
    path_logdir = f'{cwd}/esub_test_dir_mpi_slurm_log'
    if not os.path.isdir(path_testdir):
        os.mkdir(path_testdir)

    extra = '--test --main_memory=50000 --main_time=50 '\
            '--main_scratch=100000 --watchdog_memory=2400 --watchdog_time=50 '\
            '--watchdog_scratch=90000 --merge_time=30 --merge_memory=98000 '\
            '--merge_scratch=100000 --n_jobs=100 --system=slurm'
    # test with no tasks provided
    run_exec_example(path_testdir, path_logdir, mode='mpi',
                     extra_esub_args=extra,
                     tasks_string='"1 > 3"')

    # remove directory for test output
    shutil.rmtree(path_testdir)

    # check that log directory was created and remove it then
    assert os.path.isdir(path_logdir)
    shutil.rmtree(path_logdir)
    subprocess.call('rm submit.slurm', shell=1)

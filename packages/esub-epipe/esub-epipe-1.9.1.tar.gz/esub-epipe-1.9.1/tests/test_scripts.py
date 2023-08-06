# Copyright (C) 2019 ETH Zurich,
# Institute for Particle Physics and Astrophysics
# Author: Dominik Zuercher

import shutil
import shlex
import os
import subprocess


def test_check_logs():
    # setup mock esub_logs directory with log files
    path_testdir = 'esub_logs_check_logs'
    if not os.path.isdir(path_testdir):
        os.mkdir(path_testdir)

    # with unfinished jobs
    content = """2020-04-30 15:28:43.830214    Job id main: 120454427
2020-04-30 15:28:43.846407    Job id rerun_missing: 120454429
2020-04-30 15:28:43.849466    Job id merge: 120454431
    """

    with open('{}/job.log'.format(path_testdir), 'w+') as f:
        f.write(content)

    cmd = \
        'python esub/scripts/check_logs.py --dirpath_logs={}'.format(
            path_testdir)

    subprocess.call(shlex.split(cmd))

    # without unfinished jobs
    content = """2020-04-30 15:28:43.830214    Job id main: 120454427
2020-04-30 15:28:43.846407    Job id rerun_missing: 120454429
2020-04-30 15:28:43.849466    Job id merge: 120454431
2020-04-30 15:39:58.714086    First index is done
2020-04-30 15:54:44.332060    Found 0 missing indices
2020-04-30 15:54:44.358573    All indices finished
2020-04-30 15:55:32.758560    Running merge
2020-04-30 16:29:01.424964    Finished running merge
    """

    with open('{}/job.log'.format(path_testdir), 'w+') as f:
        f.write(content)

    cmd = \
        'python esub/scripts/check_logs.py --dirpath_logs={}'.format(
            path_testdir)

    subprocess.call(shlex.split(cmd))

    shutil.rmtree(path_testdir)


def test_send_cmd():
    # setup mock esub_logs directory with log files
    path_testdir = 'esub_logs_send_cmd'
    if not os.path.isdir(path_testdir):
        os.mkdir(path_testdir)

    # with unfinished jobs
    content = """2020-04-30 15:28:43.830214    Job id main: 120454427
2020-04-30 15:28:43.846407    Job id rerun_missing: 120454429
2020-04-30 15:28:43.849466    Job id merge: 120454431
    """

    with open('{}/job.log'.format(path_testdir), 'w+') as f:
        f.write(content)

    cmd = 'python esub/scripts/send_cmd.py --dirpath_logs={} ' \
        '--cmd=echo --log_filter=job'.format(
            path_testdir)

    # without unfinished jobs
    content = """2020-04-30 15:28:43.830214    Job id main: 120454427
2020-04-30 15:28:43.846407    Job id rerun_missing: 120454429
2020-04-30 15:28:43.849466    Job id merge: 120454431
2020-04-30 15:39:58.714086    First index is done
2020-04-30 15:54:44.332060    Found 0 missing indices
2020-04-30 15:54:44.358573    All indices finished
2020-04-30 15:55:32.758560    Running merge
2020-04-30 16:29:01.424964    Finished running merge
    """

    with open('{}/job.log'.format(path_testdir), 'w+') as f:
        f.write(content)

    cmd = 'python esub/scripts/send_cmd.py --dirpath_logs={} ' \
        '--cmd=echo --log_filter=job'.format(
            path_testdir)

    subprocess.call(shlex.split(cmd))
    shutil.rmtree(path_testdir)

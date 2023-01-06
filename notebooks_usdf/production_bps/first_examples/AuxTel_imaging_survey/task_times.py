#!/usr/bin/env python3

import glob
import os
import shutil
import sys
import time
from collections import Counter, defaultdict

import numpy as np

# input arg check
try:
    logjob = sys.argv[1]
except IndexError:
    print('Usage: python task_times.py [LOGFILE/jobdir]')
    raise SystemExit
try:
    errorlog = sys.argv[2]
except IndexError:
    errorlog = None

# concatenate BPS error reports into one large error log
jobdir = ''
templog = f'/tmp/task_times_{time.time()}.log'
if os.path.isdir(logjob):
    jobdir = os.path.join(logjob, '')  # extra '' adds trailing slash if missing
    logjob = templog  # reassign logjob to temporary storage location
    # allow to specify RUN directory above 'jobs/logs', for brevity
    jobdirs = [
        os.path.join(jobdir, 'jobs/'),  # HTCondor
        os.path.join(jobdir, 'logs/'),  # parsl
        jobdir,
    ]
    for jd in jobdirs:
        if os.path.exists(jd):
            break
    if os.path.exists(jd):
        jobdir = jd
    else:
        raise FileNotFoundError(f"input path not found: '{jobdir}'")
    concat_cmd = (f'find {jobdir} -maxdepth 3 -type f -name \*err '  # noqa: W605
                  f'-print0 | xargs -0 -P24 cat >> {templog}')
    print('\nConcatenating BPS log files... ', end='')
    try:
        shutil.copyfile(f"{jobdir}/../quantumGraphGeneration.out", templog)
    except FileNotFoundError:
        pass
    _ = os.system(concat_cmd)
    print('done!')

# read log file
if os.path.isfile(logjob):
    with open(logjob) as f:
        log = f.readlines()
else:
    raise FileNotFoundError(f"input path not found: '{logjob}'")

# clean up temp log file
try:
    os.remove(templog)
except FileNotFoundError:
    pass

# defaults
startup = 'QuantumGraph not yet generated...'
total_quanta = 0
tasks = defaultdict(int)

# # LSK disabled below on 2022-09-30: does not work with parsl
# # This was a work around for a restarted BPS run with a log file
# # containing multiple instances of 'QuantumGraph contains...'.
# # If necessary, this functionality can be added back in in the future.
# #
# # generate startup string, total_quanta and total tasks dict for BPS runs
# if os.path.isdir(jobdir):
#     subs = glob.glob(os.path.join(jobdir, '*', '*', '*.sub'))
#     subs = [x for x in subs if ('mergeExecutionButler' not in x) and ('pipetaskInit' not in x)]
#     task_bases = [os.path.basename(os.path.dirname(os.path.dirname(x))) for x in subs]
#     tasks = Counter(task_bases)
#     total_quanta = len(task_bases)
#     startup = f'QuantumGraph contains {total_quanta} quanta for {len(tasks)} tasks.'

# parse log line by line
time_results = defaultdict(list)
skipped = defaultdict(list)
errorlines = ""
for line in log:
    if ('QuantumGraph contains' in line) and ('not yet generated' in startup):
        startup = ('QuantumGraph' + line.split('QuantumGraph')[1]).split('tasks')[0] + 'tasks.'
        total_quanta = int(startup.split('contains ')[1].split(' quanta')[0])
    if ('Execution of task' in line) and ('failed' not in line):
        task = line.split("Execution of task '")[1].split("'")[0]
        time = float(line.split(' ')[-2])
        time_results[task].append(time)
    if 'processing will continue for remaining tasks.' in line:
        try:
            task = line.split('label=')[1].split(')')[0]
        except IndexError:
            task = "unknown"
        time_results[task].append(np.nan)
        if errorlog:
            errorlines += line
    if '}>, skipping this task.' in line:
        task = line.split('label=')[1].split(')')[0]
        skipped[task].append(1)
if len(errorlines) > 0:
    with open(errorlog, "w") as errlog:
        errlog.write(errorlines)

# parse time_results dict, sort into desired order
parsed_results = dict()
total_time, total_pass, total_fail, total_incomp = 0, 0, 0, 0
for task in set(list(time_results.keys()) + list(tasks.keys()) + list(skipped.keys())):
    times = time_results[task]
    task_time = np.nansum(times)
    task_pass = np.sum(~np.isnan(times))
    task_fail = np.sum(np.isnan(times))
    if task not in tasks:
        tasks[task] = task_pass + task_fail + np.sum(skipped[task])
    task_incomp = int(tasks[task]) - task_pass - task_fail
    total_time += task_time
    total_pass += task_pass
    total_fail += task_fail
    total_incomp += task_incomp
    parsed_results[task] = [task_time, task_pass, task_fail, task_incomp]
else:
    parsed_results = dict(sorted(parsed_results.items(), key=lambda item: item[1], reverse=True))
    parsed_results['total'] = [total_time, total_pass, total_fail, total_incomp]

# print results
horiz_sep = '-'
vert_sep = ' '  # ¦
print('\n' + startup + '\n')
for task, task_results in dict(task=['time', 'pass', 'fail', 'incomp'], **parsed_results).items():
    task_time, task_pass, task_fail, task_incomp = task_results
    try:
        task_time_pc = f"{f' (~{100*task_time/total_time:0.0f}%)'}" if task != 'total' else ''
    except TypeError:
        task_time_str = task_time
    else:
        task_time_sec = f'{task_time:.2f}'
        task_time_str = task_time_sec + 's' + task_time_pc
    if task == 'total':
        print(80*horiz_sep)
    print(f'{task:31s} {vert_sep} '
          f'{task_time_str:19s} {vert_sep} '
          f'{str(task_pass):6s} {vert_sep} '
          f'{str(task_fail):6s} {vert_sep} '
          f'{str(task_incomp):6s}')
    if task == 'task':
        print(80*horiz_sep)
# generate custom status report
status = "Quantum execution numbers not available."
if total_quanta > 0:
    total_pass_pc = f'~{100*total_pass/total_quanta:0.0f}%' if total_pass < total_quanta else '100%'
    status = f'Executed {total_pass} quanta out of a total of {total_quanta} quanta ({total_pass_pc}).'
print('\n' + status + '\n')

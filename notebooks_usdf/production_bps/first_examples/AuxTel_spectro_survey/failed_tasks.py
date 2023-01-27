#!/usr/bin/env python3

import os
import sys
import numpy as np

def extract_failures(job_dir):
    # read log files
    process = "processStar"
    logdir = os.path.join(job_dir, 'logs')
    list_all_logs = os.listdir(logdir)
    list_process_err = [ log for log in list_all_logs if process in log and '.stderr' in log ]

    log_id=''
    exec_list=[]
    except_list=[]
    h, t = os.path.split(job_dir)
    hh, th = os.path.split(h)
    run_id=f'{th}-{t}'
    file_out=f'tracebacks_{process}_{run_id}.txt'
    with open(file_out, 'w') as res:
        res.write(f'Identification of {process} failures for job {run_id}')
    num_failed=0
    for log in list_process_err:
        info_lines=[]
        error_lines=[]
        old_log_id = log_id
        log_id=f'{process}-{(log.split(".")[0]).split("_")[-2]}'
        with open(os.path.join(logdir,log)) as f:
            lines = f.readlines()
            prev_line=''
            loc=-1
            deb_traceback, end_traceback = 0, 0
            traceback=''
            exception=''
            for line in lines:
                loc+=1
                deb_line=line.split(' ')[0]
                if deb_line == "INFO" : info_lines.append(line)
                elif deb_line == "ERROR" :
                    error_lines.append(line)
                    if f"Execution of task '{process}'" in line and 'failed' in line:
                        sentences = line.split('. ')
                        exception = (sentences[-1].split('Exception '))[-1]
                elif deb_line == 'Traceback' :
                    deb_traceback=loc
                    #print(f'{deb_traceback} > {line}')
                #if 'Task' in line f'label={process}' in line and 'failed' in line:
                elif exception != '' and line == exception :
                    old_traceback = traceback
                    traceback=''
                    end_traceback = loc
                    #print(f'{end_traceback} > {line}')
                    for l in lines[deb_traceback:end_traceback+1]:
                        traceback=traceback+'\t'+l
                    if traceback != old_traceback:
                        num_failed+=1
                        exec_list.append(log_id)
                        except_list.append(exception)
                        with open(file_out, 'a') as res:
                            res.write(f'\n{log_id}:\n{traceback}')


    with open(file_out, 'a') as res:
        res.write(f'\n\nNumber of identified failures in {process} = {num_failed}')
    '''
    with open(file_out, 'r') as res:
        print(res.read())
    '''
    return exec_list, except_list
    
# input arg check
try:
    jobdir = os.path.abspath(os.path.join(sys.argv[1],'.'))
except IndexError:
    print('Usage: python failed_tasks.py [jobdir]')
    raise SystemExit
    
if os.path.isdir(jobdir):
    execs, excepts = extract_failures(jobdir)
    #print(execs)
    print('Identified errors during this run:')
    for err in set(excepts) : print(f'\t{err[:-1]}')
else:
    raise FileNotFoundError(f"input path not found: '{jobdir}'")

import os
import re
import time

import psutil
import sys

from BaseColor.base_colors import hyellow, hcyan, hred


def cpu_sta(interval=1.0):
    while True:
        try:
            cpu_percent = psutil.cpu_percent(interval=interval)
            virtual_memory = psutil.virtual_memory()
            memory_percent = virtual_memory.percent
            print(f"\rCPU: {cpu_percent}%; MEM: {memory_percent}%", end='')

        except KeyboardInterrupt:
            print()
            break
        except Exception as E:
            print(f"Error: {E}")


def cmd_res_format(cmd_list, sn=0, sorted_reverse=False):
    nl = list()
    for line in cmd_list:
        match_res = re.findall(r'\S+ + (\d+) +([.\d]+) +([.\d]+) +[^a-zA-Z+]+[a-zA-Z+]+[^a-zA-Z+/]+(.*)', line)
        if match_res:
            pid, cpu, mem, cmd_str = match_res[0]
            # nl.append(f'{pid}  {hyellow(cpu)}  {hcyan(mem)}    {cmd_str}')
            nl.append([
                int(pid),
                float(cpu),
                float(mem),
                cmd_str,
            ])
    nl = sorted(nl, key=lambda x: x[sn], reverse=sorted_reverse)
    nl_str = [f"{x[0]}  {hyellow(x[1])}  {hcyan(x[2])}  {x[3]}" for x in nl]
    return nl_str


def clear():
    os.system('clear')


def sorted_num(sorted_by: str):
    sorted_num_map = {
        'pid': 0,
        'cpu': 1,
        'mem': 2,
        'name': 3,
    }
    sn = 0
    if sorted_by:
        sn = sorted_num_map.get(sorted_by.strip().lower()) or 0
    return sn


def cmd_sta(cmd, interval=1.0, detail=False, sorted_by=None, sorted_reverse=False):
    sor = sorted_num(sorted_by=sorted_by)
    while True:
        try:
            with os.popen(f'ps aux | grep {cmd}') as ops:
                cmd_res = ops.read()
            cmd_res_l = [x.strip() for x in cmd_res.split('\n') if x and x.strip() and ' grep' not in x]
            if not detail:
                cmd_res_l = cmd_res_format(cmd_res_l, sor, sorted_reverse)
            out_str = '\n'.join(cmd_res_l)
            clear()
            print(f"\r{out_str}", end='')

        except KeyboardInterrupt:
            print()
            break
        except Exception as Err:
            print(f"Error: {Err}")
        finally:
            time.sleep(interval)


def get_cmd_pid(cmd):
    with os.popen(f"ps aux | grep '{cmd}'") as ops:
        cmd_res = ops.read()
    cmd_res_l = [x.strip() for x in cmd_res.split('\n') if x and x.strip() and ' grep' not in x]
    pid_list = []
    for cmd_line in cmd_res_l:
        match_res = re.findall(r'\S+ + (\d+) +([.\d]+) +([.\d]+) +[^a-zA-Z+]+[a-zA-Z+]+[^a-zA-Z+/]+(.*)', cmd_line)
        if match_res:
            pid, cpu, mem, cmd_str = match_res[0]
            pid_list.append(pid)
    return pid_list


def stop_pre_cmd_by_cmd_name(cmd):
    cmd_pid_list = get_cmd_pid(cmd)
    if cmd_pid_list:
        print(f"command [ {hred(cmd)} ] still running, trying to stop it")
        for pid in get_cmd_pid(cmd):
            try:
                os.kill(int(pid), 9)
                return True
            except Exception as STE:
                print(f"Error in stopping command: {STE}")
                return False
    return True


def run_cmd(cmd):
    try:
        if stop_pre_cmd_by_cmd_name(cmd):
            with os.popen(cmd) as osp:
                print(osp.read())
            return True
    except Exception as RCE:
        print(f"Error in running cmd: {RCE}")
    return False


if __name__ == "__main__":
    if len(sys.argv) == 2:
        argv_cmd = sys.argv[1]
        argv_interval = 1
        argv_detail = False
    elif len(sys.argv) == 3:
        argv_cmd = sys.argv[1]
        argv_interval = sys.argv[2]
        argv_detail = False
    elif len(sys.argv) == 4:
        argv_cmd = sys.argv[1]
        argv_interval = sys.argv[2]
        argv_detail = True
    else:
        print("command string is required! Use this script like: \n    $ cmd_aux.py cmd_xxx [interval(float)]")
        sys.exit(1)
    try:
        cmd_sta(argv_cmd, float(argv_interval), argv_detail)
        # cmd_sta('celery')
    except KeyboardInterrupt:
        print("\n exit")
    except Exception as E:
        print(f"\n Error: {E}")


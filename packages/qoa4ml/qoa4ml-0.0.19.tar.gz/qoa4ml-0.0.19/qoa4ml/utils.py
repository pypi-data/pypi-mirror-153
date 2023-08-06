from concurrent.futures import thread
import json, psutil, time, os
from qoa4ml.reports import Qoa_Client
from threading import Thread

def load_config(file_path:str)->dict:
    """
    file_path: file path to load config
    """
    with open(file_path, "r") as f:
        return json.load(f)

def to_json(file_path:str, conf:dict):
    """
    file_path: file path to save config
    """
    with open(file_path, "w") as f:
        json.dump(conf, f)
    
def get_cpu(key:str = None):
    if key == "cpu time":
        return psutil.cpu_times().user
    if key == "percentage":
        pass
    return psutil.cpu_percent()

def get_mem(key:str = None):
    if key == "percentage":
        return psutil.virtual_memory().percent
    if key == "free":
        return psutil.virtual_memory().free
    if key == "total":
        return psutil.virtual_memory().total
    if key == "active":
        return psutil.virtual_memory().active
    if key == "available":
        return psutil.virtual_memory().available
    if key == "used":
        pass
    return psutil.virtual_memory().used

def get_proc_cpu(pid = None):
    if pid == None:
        pid = os.getpid()
    process = psutil.Process(pid)
    child_list = process.children()
    cpu_usage = process.cpu_percent()
    for child in child_list:
        cpu_usage += child.cpu_percent()
    return cpu_usage

def get_proc_mem(pid = None):
    if pid == None:
        pid = os.getpid()
    process = psutil.Process(pid)
    child_list = process.children()
    cpu_usage = process.memory_percent()
    for child in child_list:
        cpu_usage += child.memory_percent()
    return cpu_usage



sys_monitor_flag = False
proc_monitor_flag = False

def system_report(client:Qoa_Client, metrics: dict, interval:int):
    try:
        client.add_metric(metrics['cpu_stat'])
        client.add_metric(metrics['mem_stat'])
    except Exception as e:
        print("Unable to add system metric: ", e)
    metric_list = []
    while sys_monitor_flag:
        try:
            for metric_name in metrics['cpu_stat']:
                metric = client.get_metric(metric_name)
                metric.set(get_cpu(metrics['cpu_stat'][metric_name]["key"]))
                metric_list.append(metric_name)
        except Exception as e:
            print("Unable to report CPU stat: ", e)
        try:
            for metric_name in metrics['mem_stat']:
                metric = client.get_metric(metric_name)
                metric.set(get_mem(metrics['mem_stat'][metric_name]["key"]))
                metric_list.append(metric_name)
        except Exception as e:
            print("Unable to report memory stat: ", e)
        try:
            client.report(metrics=metric_list)
        except Exception as e:
            print("Unable to send system report: ", e)
        time.sleep(interval)


def sys_monitor(client:Qoa_Client, metrics: dict, interval:int):
    sub_thread = Thread(target=system_report, args=(client, metrics, interval))
    sub_thread.start()

def process_report(client:Qoa_Client, pid:int, metrics: dict, interval:int):
    try:
        client.add_metric(metrics['proc_cpu'])
        client.add_metric(metrics['proc_mem'])
    except Exception as e:
        print("Unable to add system metric: ", e)
    metric_list = []
    while sys_monitor_flag:
        try:
            for metric_name in metrics['proc_cpu']:
                metric = client.get_metric(metric_name)
                metric.set(get_proc_cpu(pid=pid))
                metric_list.append(metric_name)
        except Exception as e:
            print("Unable to report CPU stat: ", e)
        try:
            for metric_name in metrics['proc_mem']:
                metric = client.get_metric(metric_name)
                metric.set(get_proc_mem(pid=pid))
                metric_list.append(metric_name)
        except Exception as e:
            print("Unable to report memory stat: ", e)
        try:
            client.report(metrics=metric_list)
        except Exception as e:
            print("Unable to send system report: ", e)
        time.sleep(interval)


def process_monitor(client:Qoa_Client, pid:int, metrics: dict, interval:int):
    sub_thread = Thread(target=process_report, args=(client, pid, metrics, interval))
    sub_thread.start()

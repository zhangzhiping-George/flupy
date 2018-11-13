#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import xlwt
import logging.handlers
import json
from urlparse import urlparse
import httplib
import time
import traceback
import sys
import multiprocessing
import subprocess
import os

# get server list from cmdb
SERVER_URL = 'http://172.18.17.72:18842/api/v1.0/Server/?page=1&size=10000'
SERVER_DATA = {}
SERVER_DATA_UUID = []
# get machine type list from cmdb
MACHINE_TYPE_URL = 'http://172.18.17.72:18842/api/v1.0/MachineType?page=1' \
                   '&size=10000'
MACHINE_TYPE_DATA = {}
# get cpu, memory and disk of server from monitor
MONITOR_URL = 'http://172.18.17.76:18889/v1/server/server_basic_features/'
# cpu, memory, disks
ALL_DATA = multiprocessing.Manager().list()
# date
TODAY_DATE = time.strftime('%Y-%m-%d', time.localtime(time.time()))

report_file = '/usr/local/lowload/cmd_report.data'  
LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
log_path = 'cmd_compute.log'
fh = logging.handlers.RotatingFileHandler(log_path, "a", 81920000, 10)
fh.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-2s %(levelname)-4s %'
                              '(message)s')
fh.setFormatter(formatter)
LOG.addHandler(fh)

def http_json_call(url, method='GET', data=None):
    http_client = None
    try:
        result = urlparse(url)
        host = result.hostname
        port = 80 if not result.port else result.port
        path = result.path +('?'+result.query if result.query else '')
        headers = {"Content-type": "application/json"}
        http_client = httplib.HTTPConnection(host, port=port, timeout=30)   
        if method in ['POST', 'PUT', 'PATCH','DELETE']:
            http_client.request(method, path, json.dumps(data), headers)
        else:
            http_client.request(method, path, headers=headers)
        response = http_client.getresponse()
        body = response.read()
        if response.status > 300:
            return response.status, response.getheaders(), body
        return response.status, response.getheaders(), \
            json.loads(body) if len(body) > 0 else None,
    except Exception:
        logging.exception('http request except; url: %s; method: %s; \
                          data: %s' % (url, method, data))
        return 400, False, False
    finally:
        if http_client:
            http_client.close()

def get_datas_url(url):
    LOG.info(url)
    status, headers, res_datas = http_json_call(url)
    if status == 200:
        if res_datas.has_key('Data'):
            if not res_datas['Data']:
                LOG.warning("Invalid values: ", res_datas)
                return False
        elif res_datas.has_key('data'):
            if not res_datas['data']:
                LOG.warning("Invalid values: ", res_datas)
                return False
        else:
            LOG.warning("Invalid values: ", res_datas)
        return res_datas
    else:
        LOG.error('the result are, status: %s, headers: %s, res_datas: %s'
                  % (status, headers, res_datas))
        LOG.warning("Invalid url:%s " % url)
        return False

def compute_avg(src):
    numerator = 0
    denominator = 0
    avg_value = 0
    for val in src:
        if val['value'] >= 0:
            numerator += val['value']
            denominator += 1
    if denominator:
        avg_value = float(numerator)/denominator
        return avg_value
    else:
        return -1
    
def compute_latest(src):
    latest_value = 0
    src.reverse()
    for val in src:
        if val['value'] >= 0:
            latest_value = val['value']
            break
        else:
            latest_value = -1
    return latest_value

def compute_sum(src):
    sum_value = 0
    count = 0
    for val in src:
        if val['value'] >= 0:
            sum_value += val['value']
            count += 1
    if count:
        return sum_value
    else:
        return -1

def get_all_datas(server):
    try:
        LOG.info('The server info are: %s' % server)
        # import pdb
        # pdb.set_trace()
	if server['HostType']==1 or server['HostType']=='1':
        return;
        global ALL_DATA, TODAY_DATE, MONITOR_URL
        all_data = {'Uuid': server['Uuid'], 'Ip': server['Ip'], 'Os_name': server['OsName'], 'cpu_value': -1, 'mem_use_value': -1, 'disk_all': -1, 'disk_use': -1, 'part_all': -1, 'part_use': -1, 'net_in': -1, 'net_out': -1, 'MachineTypeId': server['MachineTypeId'], 'IdcName': server['IdcName'], 'HostType': server['HostType']}
        # compute cpu and mem
        url_all = MONITOR_URL + server['Uuid'].upper() + '/10000,11001,11002/' + TODAY_DATE + '/' + TODAY_DATE
        datas_all = get_datas_url(url_all)
        if datas_all['data'][0]['feature_data']:
            values_cpu = datas_all['data'][0]['feature_data'][-5:]
            all_data['cpu_value'] = compute_avg(values_cpu)
        if datas_all['data'][2]['feature_data']:
            values_mem = datas_all['data'][2]['feature_data'][-5:]
            all_data['mem_use_value'] = compute_avg(values_mem)
        elif datas_all['data'][1]['feature_data']:
            values_mem = datas_all['data'][1]['feature_data'][-5:]
            all_data['mem_use_value'] = compute_avg(values_mem)
        # compute disk and part
        disk_all = 13600
        disk_use = 13700
        part_all = 12000
        part_use = 12100
        temp = 0
        part_use_tmp = []
        part_all_tmp = []
        while temp < 64:#?
            url_tmp = MONITOR_URL + server['Uuid'].upper() + '/%s,%s/%s/%s' % ((part_use + temp), (part_all + temp), TODAY_DATE, TODAY_DATE)
            part_datas = get_datas_url(url_tmp)
            if part_datas['data'][0]['feature_data'] and part_datas['data'][1]['feature_data']:
                values_part_use = part_datas['data'][0]['feature_data'][-5:]
                values_part_all = part_datas['data'][1]['feature_data'][-5:]
                part_use_tmp.append(compute_latest(values_part_use))
                part_all_tmp.append(compute_latest(values_part_all))
                temp += 1
            else:
                break
        all_data['part_all'] = part_all_tmp if (part_all_tmp) else -1
        all_data['part_use'] = part_use_tmp if (part_use_tmp) else -1

        temp2 = 0
        disk_use_tmp = []
        disk_all_tmp = []
        while temp2 < 20:
            url_tmp = MONITOR_URL + server['Uuid'].upper() + '/%s,%s/%s/%s' % ((disk_use + temp2), (disk_all + temp2), TODAY_DATE, TODAY_DATE)
            disk_datas = get_datas_url(url_tmp)
            if disk_datas['data'][0]['feature_data'] and disk_datas['data'][1]['feature_data']:
                values_disk_use = disk_datas['data'][0]['feature_data'][-5:]
                values_disk_all = disk_datas['data'][1]['feature_data'][-5:]
                disk_use_tmp.append(compute_latest(values_disk_use))
                disk_all_tmp.append(compute_latest(values_disk_all))
                temp2 += 1
            else:
                break
        all_data['disk_all'] = disk_all_tmp if (disk_all_tmp) else -1
        all_data['disk_use'] = disk_use_tmp if (disk_use_tmp) else -1

        # compute net
        net_in = 14010
        net_out = 14020
        temp3 = 0
        net_in_tmp = []
        net_out_tmp = []
        while temp3 < 10:
            url_tmp = MONITOR_URL + server['Uuid'].upper() + '/%s,%s/%s/%s' % ((net_in + temp3), (net_out + temp3), TODAY_DATE, TODAY_DATE)
            net_datas = get_datas_url(url_tmp)
            if net_datas['data'][0]['feature_data'] and net_datas['data'][1]['feature_data']:
                values_part_use = net_datas['data'][0]['feature_data'][-5:]
                values_part_all = net_datas['data'][1]['feature_data'][-5:]
                net_in_tmp.append(compute_sum(values_part_use))
                net_out_tmp.append(compute_sum(values_part_all))
                temp3 += 1
            else:
                break
        all_data['net_in'] = net_in_tmp if net_in_tmp else -1
        all_data['net_out'] = net_out_tmp if net_out_tmp else -1
        ALL_DATA.append(all_data)
    except Exception:
        LOG.error(traceback.format_exc(sys.exc_info()))

def save_to_excel():
    global ALL_DATA
    wb = xlwt.Workbook()
    ws = wb.add_sheet('sheet1')
    ws.write(0, 0, 'Uuid')
    ws.write(0, 1, 'Ip')
    ws.write(0, 2, 'MachineTypeId')
    ws.write(0, 3, 'Cpu_usage')
    ws.write(0, 4, 'Mem_used')
    ws.write(0, 5, 'Disk_all')
    ws.write(0, 6, 'Disk_used')
    ws.write(0, 7, 'Part_all')
    ws.write(0, 8, 'Part_used')
    ws.write(0, 9, 'Net_in')
    ws.write(0, 10, 'Net_out')
    ws.write(0, 11, 'Os_name')
    ws.write(0, 12, 'IdcName')
    ws.write(0, 13, 'HostType')
    i = 1
    for data in ALL_DATA:
        ws.write(i, 0, data['Uuid'])
        ws.write(i, 1, data['Ip'])
        ws.write(i, 2, data['MachineTypeId'])
        ws.write(i, 3, data['cpu_value'])
        ws.write(i, 4, data['mem_use_value'])
        ws.write(i, 5, str(data['disk_all']))
        ws.write(i, 6, str(data['disk_use']))
        ws.write(i, 7, str(data['part_all']))
        ws.write(i, 8, str(data['part_use']))
        ws.write(i, 9, str(data['net_in']))
        ws.write(i, 10, str(data['net_out']))
        ws.write(i, 11, data['Os_name'])
        ws.write(i, 12, data['IdcName'])
        ws.write(i, 13, data['HostType'])
        i += 1
    wb.save('monitor_svr_data_report.xls')

if __name__ == '__main__':
    try:
        # get server list
        SERVER_DATA = get_datas_url(SERVER_URL)
        if not SERVER_DATA:
            sys.exit(-1)
        # LOG.info('the server list info are: %s' % SERVER_DATA)
        # MACHINE_TYPE_DATA = get_datas_url(MACHINE_TYPE_URL)
        # if not MACHINE_TYPE_DATA:
        #     sys.exit(-1)
        # LOG.info('the machine type list info are: %s' % MACHINE_TYPE_DATA)
        # a = 2
        # for i in SERVER_DATA['Data']:
        #     if a > 0:
        #         get_all_datas(i)
        #         a -= 1
        LOG.info('data are: %s' % ALL_DATA)

        pool = multiprocessing.Pool()
        pool.map(get_all_datas, SERVER_DATA['Data'])

        # for i in SERVER_DATA['Data']:
        #     get_all_datas(i)
        # save to excel
        save_to_excel()
        LOG.info('compute complete')
    except Exception:
        LOG.error(traceback.format_exc(sys.exc_info()))

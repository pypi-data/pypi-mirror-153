#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
import pathlib
import os
import requests
import functools
import tqdm
import logging
from pprint import pformat
from pyocs import pyocs_software
from pyocs.pyocs_demand import PyocsDemand

class Yadiredo:
    API_ENDPOINT = 'https://cloud-api.yandex.net/v1/disk/public/resources/?public_key={}&path=/{}&offset={}'
    _logger = logging.getLogger(__name__)

    def __init__(self):
        self._logger.setLevel(level=logging.INFO)  # 控制打印级别

    def download_file(self, target_path, url):
        # self._logger.info(url)
        r = requests.get(url, stream=True, allow_redirects=True)
        if r.status_code != 200:
            r.raise_for_status()  # Will only raise for 4xx codes, so...
            raise RuntimeError("请求网站时出现错误!")
        file_size = int(r.headers.get('Content-Length', 0))

        path = pathlib.Path(target_path).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        desc = "(Unknown total file size)" if file_size == 0 else ""
        r.raw.read = functools.partial(r.raw.read, decode_content=True)  # Decompress if needed
        with tqdm.tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
            with path.open("wb") as f:
                shutil.copyfileobj(r_raw, f)


    def try_as_file(self, j, current_path):
        if 'file' in j:
            file_save_path = os.path.join(current_path, j['name'])
            self._logger.info(f' processing, file save path: ./{file_save_path}')
            self.download_file(file_save_path, j['file'])
            return True
        return False


    def get_burn_info_with_upload(self, ocs):
        sw = pyocs_software.PyocsSoftware()
        ddr_info_str = PyocsDemand(ocs).get_ddr_info()
        if not ddr_info_str:
            raise RuntimeError("无法获取DDR信息，请确认订单状态")

        ddr_info_dict = eval(ddr_info_str)

        burn_place_hold_nums = ddr_info_str.count('refDec')
        burn_place_hold_itemNo = ddr_info_dict['categoryDescp']
        flash_list1 = ['EMMC FLASH', 'NAND FLASH']
        flash_list2 = ['NOR FLASH']
        if 1 == burn_place_hold_nums:
            if ddr_info_dict['refDec'] is None:
                burn_place_hold_type = ''
                burn_type = sw.sw_burn_type["离线烧录"]
            else:
                burn_place_hold = '【' + ddr_info_dict['refDec'] + '】,' + ddr_info_dict['supplierNo'] + ',' + \
                                ddr_info_dict['itemNo'] + ',' + ddr_info_dict['categoryDescp'] + ',' + ddr_info_dict['capacity']
                burn_place_hold_type = ddr_info_dict['refDec']
                if burn_place_hold_itemNo in flash_list1:
                    burn_type = sw.sw_burn_type["在线烧录"]
                elif burn_place_hold_itemNo in flash_list2:
                    burn_type = sw.sw_burn_type["离线烧录"]
        elif 2 == burn_place_hold_nums:
            if ddr_info_dict['refDec'] is None or ddr_info_dict['refDec1'] is None:
                burn_place_hold_type = ''
                burn_type = sw.sw_burn_type["离线烧录"]
            else:
                categoryDescp = [ddr_info_dict['categoryDescp'], ddr_info_dict['categoryDescp1']]

                if categoryDescp.count('DDR') == 1:#刚好有一个是DDR，那就用非DDR的那个
                    if categoryDescp[0] == 'DDR':
                        burn_place_hold_type = ddr_info_dict['refDec1']
                        burn_place_hold_itemNo = ddr_info_dict['categoryDescp1']
                    else:
                        burn_place_hold_type = ddr_info_dict['refDec']
                        burn_place_hold_itemNo = ddr_info_dict['categoryDescp']
                    if burn_place_hold_itemNo in flash_list1:
                        burn_type = sw.sw_burn_type["在线烧录"]
                    elif burn_place_hold_itemNo in flash_list2:
                        burn_type = sw.sw_burn_type["离线烧录"]
                else:
                    self._logger.info("订单录入的烧录位号有两种，请手动设置，详情如下：")
                    burn_place_hold = '【' + ddr_info_dict['refDec'] + '】,' + ddr_info_dict['supplierNo'] + ',' + \
                                    ddr_info_dict['itemNo'] + ',' + ddr_info_dict['categoryDescp'] + ',' + ddr_info_dict['capacity']
                    burn_place_hold_option = ddr_info_dict['refDec']
                    burn_place_hold1 = '【' + ddr_info_dict['refDec1'] + '】,' + ddr_info_dict['supplierNo1'] + ',' + \
                                    ddr_info_dict['itemNo1'] + ',' + ddr_info_dict['categoryDescp1'] + ',' + ddr_info_dict['capacity1']
                    burn_place_hold_option1 = ddr_info_dict['refDec1']
                    burn_place_hold_str = '请输入烧录位号选项' + '(' + burn_place_hold_option + ', ' + burn_place_hold_option1 + '): '
                    burn_place_hold_type = input(burn_place_hold_str)
                    burn_place_hold_type = burn_place_hold_type.upper()
                    burn_type = input("请输入烧录类型选项(1,2)：")
        elif 3 == burn_place_hold_nums:
            if ddr_info_dict['refDec'] is None or ddr_info_dict['refDec1'] is None or ddr_info_dict['refDec2'] is None:
                burn_place_hold_type = ''
                burn_type = sw.sw_burn_type["离线烧录"]
            else:
                categoryDescp = [ddr_info_dict['categoryDescp'], ddr_info_dict['categoryDescp1'], ddr_info_dict['categoryDescp2']]

                if categoryDescp.count('DDR') == 2:#刚好有两个是DDR，那就用非DDR的那个
                    if categoryDescp[0] != 'DDR':
                        burn_place_hold_type=ddr_info_dict['refDec']
                        burn_place_hold_itemNo = ddr_info_dict['categoryDescp']
                    elif categoryDescp[1] != 'DDR':
                        burn_place_hold_type = ddr_info_dict['refDec1']
                        burn_place_hold_itemNo = ddr_info_dict['categoryDescp1']
                    else:
                        burn_place_hold_type = ddr_info_dict['refDec2']
                        burn_place_hold_itemNo = ddr_info_dict['categoryDescp2']
                    if burn_place_hold_itemNo in flash_list1:
                        burn_type = sw.sw_burn_type["在线烧录"]
                    elif burn_place_hold_itemNo in flash_list2:
                        burn_type = sw.sw_burn_type["离线烧录"]
                else:
                    self._logger.info("订单录入的烧录位号有两种，请手动设置，详情如下：")
                    burn_place_hold = '【' + ddr_info_dict['refDec'] + '】,' + ddr_info_dict['supplierNo'] + ',' + \
                                    ddr_info_dict['itemNo'] + ',' + ddr_info_dict['categoryDescp'] + ',' + ddr_info_dict['capacity']
                    burn_place_hold_option = ddr_info_dict['refDec']
                    burn_place_hold1 = '【' + ddr_info_dict['refDec1'] + '】,' + ddr_info_dict['supplierNo1'] + ',' + \
                                    ddr_info_dict['itemNo1'] + ',' + ddr_info_dict['categoryDescp1'] + ',' + ddr_info_dict['capacity1']
                    burn_place_hold_option1 = ddr_info_dict['refDec1']
                    burn_place_hold2 = '【' + ddr_info_dict['refDec2'] + '】,' + ddr_info_dict['supplierNo2'] + ',' + \
                                    ddr_info_dict['itemNo2'] + ',' + ddr_info_dict['categoryDescp2'] + ',' + ddr_info_dict['capacity2']
                    burn_place_hold_option2 = ddr_info_dict['refDec2']
                    burn_place_hold_str = '请输入烧录位号选项' + '(' + burn_place_hold_option + ', ' + burn_place_hold_option1 + burn_place_hold_option2 + '): '
                    burn_place_hold_type = input(burn_place_hold_str)
                    burn_place_hold_type = burn_place_hold_type.upper()
                    burn_type = input("请输入烧录类型选项(1,2)：")
        else:
            log.error("存储器信息异常")
        return burn_place_hold_type, burn_type

    def init_reset_env(self,target_path, source_path, is_init=True):
        current_path = os.path.join(target_path, source_path)
        if pathlib.Path(current_path).exists():
            # self._logger.info("clean env ...")
            shutil.rmtree(current_path)
        if is_init:
            current_path = os.path.join(target_path, source_path)
            pathlib.Path(current_path).mkdir(parents=True, exist_ok=True)


    def list_all_files(self, target_path):
        files = []
        list = os.listdir(target_path) #列出文件夹下所有的目录与文件
        for i in range(0,len(list)):
            path = os.path.join(target_path,list[i])
            if os.path.isdir(path):
                files.extend(self.list_all_files(path))
            if os.path.isfile(path):
                files.append(path)
        return files


    def unpack_rename_upload_yandex_software(self, target_path, source_path, ocs):
        #unpack
        for it in pathlib.Path(target_path).iterdir():
            zip_file_path = pathlib.Path(target_path).joinpath(it.name)
            shutil._unpack_zipfile(zip_file_path, target_path)

        #rename
        files = self.list_all_files(target_path)
        zip_old_name = None
        zip_new_name = None
        zip_new_path = None
        for fi in files:
            if '.xml' in fi:
                zip_new_name = fi.split('/')[-1].replace('.xml', '')
            if '.zip' in fi:
                zip_old_name = fi.split('/')[-1].replace('.zip', '')

        if zip_old_name and zip_new_name:
            for fi in files:
                if '.zip' in fi:
                    zip_new_path = fi.replace(zip_old_name, zip_new_name)
                    shutil.move(fi, zip_new_path)

        #upload
        if zip_new_path:
            # copy .xml file
            xml_new_path = None
            for fi in files:
                if '.xml' in fi:
                    xml_new_path = zip_new_path.replace('.zip', '.xml')
                    shutil.copy(fi, xml_new_path)

            self._logger.info(f'uploading {zip_new_path} ...')

            if not ocs:
                ocs = zip_new_name[2:8]
                self._logger.info(f'ocs : {ocs}')

            sw = pyocs_software.PyocsSoftware()
            demand = pyocs_software.PyocsDemand(ocs)
            task_type = demand.get_task_type()
            if (task_type=='虚拟软件任务' or task_type == '生产软件任务'):
                test_type='5' #默认E测
            else:
                test_type='100' #不用测试

            burn_place_hold_type, burn_type = self.get_burn_info_with_upload(ocs)

            ret = sw.upload_software_to_ocs(ocs_num=ocs, zip_path=zip_new_path, xml_path=xml_new_path,
                 test_type='6', burn_place_hold=burn_place_hold_type,  
                 burn_type=burn_type, message="upload yandex SW.")

            if ret:
                self._logger.info(f'upload yandex software succeed to {ocs}')
                self.init_reset_env(target_path, source_path, is_init=False)
            else:
                self._logger.info(f'upload yandex software failure to {ocs}')


    def download_path(self, target_path, public_key, source_path, offset=0):
        # self._logger.info('getting "{}" at offset {}'.format(source_path, offset))
        current_path = os.path.join(target_path, source_path)
        pathlib.Path(current_path).mkdir(parents=True, exist_ok=True)
        jsn = requests.get(self.API_ENDPOINT.format(public_key, source_path, offset)).json()

        # first try to treat the actual json as a single file description
        if self.try_as_file(jsn, current_path):
            return

        # otherwise treat it as a directory
        try:
            emb = jsn['_embedded']
        except KeyError:
            log.error(pformat(jsn))
            return
        items = emb['items']
        for i in items:
            # each item can be a file...
            if self.try_as_file(i, current_path):
                continue
            # ... or a directory
            else:
                subdir_path = os.path.join(source_path, i['name'])
                self.download_path(target_path, public_key, subdir_path)

        # check if current directory has more items
        last = offset + emb['limit']
        if last < emb['total']:
            self.download_path(target_path, public_key, source_path, last)


    def yandex_download_upload(self, url, ocs=None):
        target_path = 'temp_yandex_sw'
        source_path = ''
        d = Yadiredo()
        d.init_reset_env(target_path, source_path)
        d.download_path(target_path, url, source_path)
        d.unpack_rename_upload_yandex_software(target_path, source_path, ocs)

if __name__ == '__main__':
    d = Yadiredo()
    d.yandex_download_upload('https://disk.yandex.ru/d/k_1RjGmY8rfKTA')
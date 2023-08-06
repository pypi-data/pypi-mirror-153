import json
import requests
from requests.exceptions import RequestException
import re
import time
import random
import os
import logging
from lxml import etree
import sys
print(sys.path)
sys.path.append(".")
import time
import jenkins
from openpyxl import load_workbook
from pyocs.pyocs_software import PyocsSoftware
from pyocs.pyocs_demand import PyocsDemand
from pyocs.pyocs_request import PyocsRequest
from pyocs import pyocs_login
from pyocs.pyocs_list import PyocsList
from pyocs import pyocs_login
from pyocs.pyocs_request import PyocsRequest
import logging
from urllib.parse import urlencode
from lxml import etree
from colorama import Fore, Back, Style
from pyocs.pyocs_jenkins import PyocsJenkins
import platform
import My_pyocs_fun
mypyocs = My_pyocs_fun.child_pyocs()

new_ocs_url = "http://ocs.gz.cvte.cn/tv/Tasks/index/ContractTask//SearchId:2091062/range:all"
find_old_keliaohao_ocs_url = "http://ocs.gz.cvte.cn/tv/Tasks/index/range:all/"
auto_build_url = "http://tvci.gz.cvte.cn/job/yangpingbu/job/Sample_Compile/build"
reuse_stock_software_url = "http://tvci.gz.cvte.cn/job/Utility_Tools/job/reuse_stock_software/build"
_ocs_base_link = 'https://ocs.gz.cvte.cn'
_ocs_find_old_sw_url = _ocs_base_link + "/tv/pop/selectors/common_view/Controller:FirmwareAttachments/" \
                                            "Parameters:accountId/input_id:old_fw_id/input_name:old_fw_name/inputtype:1"

customer_order = "01-202005-132"
customer_liaohao="R41-63S2T2B00000A1C"
member = "林祥纳 陈潮雄 陈嘉艺"

ocs_status="待录入需求"

list_xpath = '//td[@class="Task_col_id"]|//td[@class="Task_col_sw_user_id"]|//td[@class="Task_col_status"]|//td[@class="Task_col_subject"]/a|//td[@class="Task_col_rd_dept_id"]|//td[@class="Contract_col_account_prod_name"]'

#用vscode运行时，用这个
dirPath = os.getcwd()+'/customers/customer_jinpin/atuo_do_daice_sw'
#window下运行的
#dirPath = os.getcwd()
print("dirPath",dirPath)
class atuo_do_daice_sw:
    _ocs_link_Prefix = _ocs_base_link + '/tv/Tasks/view/'
    _ocs_base_link = 'https://ocs.gz.cvte.cn'
    _ocs_find_old_sw_url = _ocs_base_link + "/tv/pop/selectors/common_view/Controller:FirmwareAttachments/" \
                                            "Parameters:accountId/input_id:old_fw_id/input_name:old_fw_name/inputtype:1"
    _logger = logging.getLogger(__name__)
    def __init__(self):
        self._logger.setLevel(level=logging.DEBUG)  # 控制打印级别
    def get_new_order_searchid(self,advanced_search,condition):
        #根据摘要里的条件获取search_id
        searchid = PyocsSoftware().get_searchid_from_advanced_search(advanced_search, condition)
        return searchid


    def change_list_to_2D_list(self,new_ocs_list):
        new_ocs_order_list = list()
        i = 0
        parse_list_width = 6 
        for j in range(0,len(new_ocs_list),parse_list_width):
            new_ocs_order_list.append(new_ocs_list[j:j+parse_list_width])
            i=i+1
        return i,new_ocs_order_list

    def parse_string_from_ocs_info(self,ocs_subjest_info,string_pattern):
        pattern = re.compile(string_pattern, re.S)
        print(pattern)
        items = re.findall(pattern, ocs_subjest_info)
        print(items)
        return items


    def submit_atuo_reuse(self,src_ocs_number,dst_ocs_number):
        jenkins_server = jenkins.Jenkins
        account = pyocs_login.PyocsLogin().get_account_from_json_file()
        jenkins_server = jenkins.Jenkins('http://tvci.gz.cvte.cn/', username=account['Username'], password=account['Password'],
                                    timeout=30)
        print(jenkins_server)
        data = {
            'SRC_OCS_NUMBER': int(src_ocs_number),
            'DST_OCS_NUMBER': int(dst_ocs_number),
        }
        #print(data)
        r_jenkins=jenkins_server.build_job("Utility_Tools/reuse_stock_software" ,data)

    #还需要加功能，判断订单返回的可用软件列表不为空才应用
    #同一料号还有占空比不一样的情况（较少）
    #找旧软件应该要尽量找已经测试通过的
    def check_if_reuse_old(self,new_ocs_info_list,count_nums):
        #如果没有单要处理，old_ocs_number没有赋值会导致最后return错误
        old_ocs_number = 0
        escape_flag=0
        for i in range(0,count_nums):
            dst_ocs_number = str(new_ocs_info_list[i][0])
            print("dst_ocs_number",dst_ocs_number)
            pd_dst = PyocsDemand(ocs_number=dst_ocs_number)
            print("产品型号",pd_dst.get_product_name())
            dst_product_name = pd_dst.get_product_name()
            dst_pwm = pd_dst.get_pwm()
            dst_port_info = pd_dst.get_port_info()
            #每个新的单重新赋值，归零可以引用的旧软件OCS,以免用了旧的值
            old_ocs_number = 0
            self._logger.info("ocs_number not found",old_ocs_number)
            #现在是不重复reuse.但是后面做获取禁用软件信息申请解禁。还要可以继续reuse
            string_pattern_liaohao='\u5ba2\u6599\u53f7(.*?)）'
            #string_pattern_liaohao='\u5ba2\u6599\u53f7(.*?)，'
            string_pattern_model_size='E(\d\d)'
            ocs_subjest_info  = u"[B.NEW][金品]TP.ATM30.PB818C配ST3751A07-2（中国，SY202005150001，客料号R41-920CN230C0AWA1C，客批号TCL海外电子01-202005-101）"
            ocs_subjest_info  = new_ocs_info_list[i][3]
            #if '[虚拟]' in ocs_subjest_info:
                #continue
            string_model_size  = do_daice_task.parse_string_from_ocs_info(new_ocs_info_list[i][5],string_pattern_model_size)
            string_liaohao=do_daice_task.parse_string_from_ocs_info(ocs_subjest_info,string_pattern_liaohao)
            #一开始string_liaohao是list类型，要剃干净，没有一点多余的字符才行
            string_liaohao =str(string_liaohao)
            string_liaohao = string_liaohao[2:-2]
            print("after split",string_liaohao)
            liaohao_advanced_search = {
                "0":{"search_field_name":"Task.subject","search_field_id":"554","search_field_type":"5","search_field_rel_obj":"null","search_opr":"TDD_OPER_INC","input1":string_liaohao,"input2":"null","offset":"null"}
                }
            new_order_condition = ""
            search_id_liaohao = do_daice_task.get_new_order_searchid(liaohao_advanced_search,new_order_condition)
            #print(search_id)
            xpath_result_liaohao = PyocsList().get_single_data_list(list_xpath,search_id_liaohao)
            temp_list=do_daice_task.change_list_to_2D_list(xpath_result_liaohao[1])
            ocs_list_liaohao = temp_list[1]
            count_nums = temp_list[0]
            #print(temp_list)
            #print(count_nums)
            if(new_ocs_info_list[i][4] != "MT7601") and (new_ocs_info_list[i][4] != "6M60") and (new_ocs_info_list[i][4] != "MT9602") :
                for j in range(count_nums-1,-1,-1):
                    #print("j:",j)
                    if(escape_flag ==1 ):
                        escape_flag=0
                        break
                    #现在是找ocs上有未被禁用软件的订单
                    if ocs_list_liaohao[j][2] != "软件审核不通过" and ocs_list_liaohao[j][2] != "软件测试不通过" and ocs_list_liaohao[j][2] != "待录入需求":
                        if do_daice_task.get_enable_software_can_be_reuse_with_ocs(ocs_list_liaohao[j][0]) == None:
                            continue
                        else:
                            print("ocs_list_liaohao[j][0]",ocs_list_liaohao[j][0])
                            #print("get_enable_software_reuse_ocs_with_ocs",PyocsSoftware().get_enable_software_reuse_ocs_with_ocs(ocs_list_liaohao[j][0]))
                            old_ocs_string_model_size  = do_daice_task.parse_string_from_ocs_info(ocs_list_liaohao[j][5],string_pattern_model_size)
                            #print(old_ocs_string_model_size)
                            old_backup_ocs_number = str(ocs_list_liaohao[j][0])
                            pd_old = PyocsDemand(ocs_number=old_backup_ocs_number)
                            print("产品型号",pd_old.get_product_name())
                            old_product_name = pd_old.get_product_name()
                            old_pwm = pd_old.get_pwm()
                            old_port_info = pd_old.get_port_info()
                            #if  old_ocs_string_model_size == string_model_size:
                            if  (dst_product_name == old_product_name) and (dst_pwm == old_pwm) and (dst_port_info == old_port_info):
                                old_ocs_number= ocs_list_liaohao[j][0]
                                #break
                            print("old_ocs_number",old_ocs_number)
                            if old_ocs_number!=0:
                                dst_ocs_link = self._ocs_link_Prefix + old_ocs_number
                                print("dst_ocs_link",dst_ocs_link)
                                response = PyocsRequest().pyocs_request_get(dst_ocs_link)
                                html = etree.HTML(response.text)
                                file_list = mypyocs.get_all_software_list_name_from_html(html)
                                for tmp_list in file_list:
                                    #pd_old = PyocsDemand(ocs_number=old_ocs_number)
                                    print("tmp_list",str(tmp_list))
                                    print("get_software_confirm_status(tmp_list)",pd_old.get_software_confirm_status(tmp_list))
                                    print("get_test_result_from_ocs(tmp_list)",pd_old.get_test_result_from_ocs(tmp_list))
                                    if ("代测" in pd_old.get_software_confirm_status(tmp_list)) :
                                        mypyocs.reuse_old_sw_from_src_to_dst_by_fw_id(str(tmp_list),dst_ocs_number, os.getcwd())
                                        #return直接退出查找了
                                        #return old_ocs_number
                                        escape_flag = 1
                                        break
                                        #直接return 了 ，意味着只处理一个
                                        #一个找不到，退出继续找
                                        #都找到了就结束
                                        #return old_ocs_number
                                print("old_file_list",file_list)
                                #do_daice_task.submit_atuo_reuse(old_ocs_number,dst_ocs_number)
        return old_ocs_number

    def get_enable_software_can_be_reuse_with_ocs(self, ocs, exclude_bin=True):
        """获取订单上的启用状态下的软件以及对应的信息字典
        Args:
            html: 某个ocs订单的html页面
        Returns:
            启用状态下的非烧录 bin 或者不符合 CVTE 规范的软件以及对应的信息字典
        """
        active_software_info_list = []
        _ocs_base_link = 'https://ocs.gz.cvte.cn'
        _ocs_link_Prefix = _ocs_base_link + '/tv/Tasks/view/'
        src_ocs_link = _ocs_link_Prefix + str(ocs)
        response = PyocsRequest().pyocs_request_get(src_ocs_link)
        html = etree.HTML(response.text)
        enable_software_name_xpath = \
            '//a[contains(@href, "/tv/Attachments/download_attachment")]/text()'
        enable_software_name_list = html.xpath(enable_software_name_xpath)
        for sw_name in enable_software_name_list:
            if not PyocsSoftware().is_sw_locked(sw_name=sw_name, html=html):
                active_software_info_list.append(sw_name)
        print("active_software_info_list",active_software_info_list)
        if active_software_info_list:
            enable_reuse_software_info = active_software_info_list[0]
            enable_reuse_ocs_list = re.findall(r'\d+', enable_reuse_software_info)
            return active_software_info_list
        else:
            return None



class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

sys.stdout = Logger(stream=sys.stdout)
sys.stdout = Logger(stream=sys.stderr)

sys_time=time.strftime('time:%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
print(sys_time)
do_daice_task = atuo_do_daice_sw()
pyocs_job = PyocsSoftware()

#金品 且待录入需求的订单#\u91d1\u54c1
#韩科\u97e9\u79d1
new_order_advanced_search = {
    "0":{"search_field_name":"Task.account_id","search_field_id":"560","search_field_type":"19","search_field_rel_obj":"Accounts","search_opr":"TDD_OPER_INC","input1":"\u97e9\u79d1","input2":"null","offset":"null"},
    "1":{"search_field_name":"Task.status","search_field_id":"584","search_field_type":"19","search_field_rel_obj":"Enums","search_opr":"TDD_OPER_INC","input1":ocs_status,"input2":"null","offset":"null"}
    }


new_order_condition = "(1 and 2)"



logging.basicConfig(filename=os.path.join(os.getcwd()+'/customers/customer_hanke/atuo_do_daice_sw/','hanke_daice_log.txt'),level=logging.DEBUG)
logging.debug('this is a message')
search_id_new_order = do_daice_task.get_new_order_searchid(new_order_advanced_search,new_order_condition)
print(search_id_new_order)
#改为林祥纳的虚拟单测试 3736585
xpath_result = PyocsList().get_single_data_list(list_xpath,search_id_new_order)
#print(xpath_result)
new_ocs_list = xpath_result[1]
print(new_ocs_list)
#count_ocs_numbers = PyocsList().get_ocs_id_list(search_id)
temp_list=do_daice_task.change_list_to_2D_list(new_ocs_list)
new_ocs_info_list = temp_list[1]
count_nums = temp_list[0]
#print(count_nums)
print("new_ocs_info_list[0]",new_ocs_info_list[0])
do_daice_task.check_if_reuse_old(new_ocs_info_list,count_nums)






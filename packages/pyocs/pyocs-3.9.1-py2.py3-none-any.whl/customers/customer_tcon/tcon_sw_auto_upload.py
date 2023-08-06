import os
import sys
FILE_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJ_HOME_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1,PROJ_HOME_PATH)
# print(PROJ_HOME_PATH)

from pyocs.pyocs_login import PyocsLogin
from pyocs.pyocs_demand import PyocsDemand
from pyocs.pyocs_request import PyocsRequest
from pyocs.pyocs_software import PyocsSoftware
import requests
import pandas as pd
from lxml import etree

import poplib
import smtplib
import telnetlib
import email
import email.policy
from email.parser import Parser
from email.header import Header
from email.header import decode_header
from email.utils import parseaddr
from email.mime.text import MIMEText

from log import logUtils
loger = logUtils("tcon_sw_auto_upload").log

#KB 表格样式：
#['软件名', '软件下载OCS', 'TCON型号', '配屏', 'PMIC型号', 'GAMMA IC', 'SOC/主芯片', '位号', '烧录方式']

'''
脚本说明：
过滤器1：http://ocs.gz.cvte.cn/tv/Tasks/index/ContractTask/SearchId:3315961/range:all
过滤器2：http://ocs.gz.cvte.cn/tv/Tasks/index/ContractTask/direction:desc/sort:Task.update_time/SearchId:3969425/range:all
1、从过滤器1中，遍历待上传软件的订单，拿订单（目标订单）的TCON型号
2、将型号信息作为一个摘要信息，补充到过滤器2中，然后通过拼接出来的过滤器2捞到符合条件的订单，再根据TCON要求的属性，逐一查找所有属性都能匹配上的订单（源订单）
3、调用pyocs copy 接口，将源订单的软件上传到目标订单中
'''
account  = PyocsLogin().get_account_from_json_file()
username = account['Username']
password = account['Password']

def print_to_file(something_need_to_print_to_file):
    # w+:打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件
    # a+:打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
    f = open(FILE_DIR_PATH + "/log.txt", 'w+')
    print(something_need_to_print_to_file, file=f)
    print("log has save to " + FILE_DIR_PATH + "/log.txt")

def upload_sw(ocs_id,sw_name):
    if not sw_name:
        return False
    sw = PyocsSoftware()
    sw_dict = sw.find_old_sw_id_by_name(old_sw_name=sw_name)
    if not sw_dict:
        return False
    sw_id = list(sw_dict.keys())[0]
    burn_place_hold_type, burn_type = get_burn_info_with_upload(ocs_id)

    return sw.upload_old_sw_by_id(ocs_num=ocs_id, old_sw_id=sw_id, burn_place_hold=burn_place_hold_type, burn_type=burn_type)

def get_ocs_info(ocs_id):
    ret = {
        'SOC/主芯片':'',
        '配屏':'',
        'TCON型号':'',
        'PMIC型号':'',
        'GAMMA IC':'',
        '客户特殊需求':''
    }
    ocs_task = PyocsDemand(ocs_id)

    ret['SOC/主芯片'] = ocs_task.get_chip_name() if ocs_task.get_chip_name() else '无'
    ret['配屏'] = ocs_task.get_panel_info().split('型号')[-1]
    ret['TCON型号'] = ocs_task.get_product_name_and_version().split('<')[0].rstrip('ABCDEFGHIJKLMNOPQ')#删掉型号后面可能存在的字母
    ret['PMIC型号'] = ocs_task.get_pmic_type()
    ret['GAMMA IC'] = ocs_task.get_gamma_type()
    ret['客户特殊需求'] = ocs_task.get_customer_special_requirement()

    return ret

#return type:DataFrame
def get_kb_table(url):
    account = PyocsLogin().get_account_from_json_file()
    url_html = requests.get(url, auth=(username, password))
    return pd.read_html(url_html.text)[0]

def get_kb_url(tcon_type):
    url = 'https://kb.cvte.com/pages/viewpage.action?pageId=174495337'
    url_html = requests.get(url, auth=(username, password))
    html_xpath = "//a[contains(text(),'" + tcon_type + "')]/@href"
    ret = etree.HTML(url_html.text).xpath(html_xpath)
    ret = ret[0] if ret else ''
    return "https://kb.cvte.com" + ret

def get_full_match_sw(kb_table,ocs_info):
    #若KB上的TCON表格中没有 '客户特殊需求' 列，则不比较此列，直接del掉此列
    if '客户特殊需求' not in kb_table.columns:
        del ocs_info['客户特殊需求']
    for i in range(0,len(kb_table['软件名'])-1):
        FULL_MATCH_FLAG = True
        for j in range(0,len(ocs_info)):
            col_name = list(ocs_info.keys())[j]
            if kb_table.loc[i,col_name] != ocs_info[col_name]:
                print("第 " + str(i) + " 行发现不匹配项====> " + str(col_name) + ":" + str(kb_table.loc[i,col_name]))
                FULL_MATCH_FLAG = False
                break
        if FULL_MATCH_FLAG:
            return kb_table.loc[i,'软件名']
    return ''

def upload_tcon_sw(ocs_id):
    ocs_info = get_ocs_info(ocs_id)
    print(ocs_info)
    specail_tcon_kb_url = get_kb_url(ocs_info['TCON型号'])
    print(specail_tcon_kb_url)
    if specail_tcon_kb_url == "https://kb.cvte.com":
        return False
    tcon_sw_info_table = get_kb_table(specail_tcon_kb_url)
    tcon_sw_name = get_full_match_sw(tcon_sw_info_table,ocs_info)
    return upload_sw(ocs_id,tcon_sw_name)

#获取待上传软件的TCON 订单的searchid
def get_searchid_of_need_to_upload_sw():
    advanced_search = {
    "0":{"search_field_name":"Task.rd_dept_id","search_field_id":"546","search_field_type":"19",
        "search_field_rel_obj":"Depts","search_opr":"TDD_OPER_EQUAL",
        "input1":"TCON","input2":'null',"offset":'null'},
    "1":{"search_field_name":"Task.status","search_field_id":"584","search_field_type":"19",
        "search_field_rel_obj":"Enums","search_opr":"TDD_OPER_EQUAL",
        "input1":"待录入需求","input2":'null',"offset":'null'}
    }
    condition = "1 and 2"
    searchid = PyocsSoftware().get_searchid_from_advanced_search(advanced_search, condition)
    return searchid

#获取状态为已完成，且TCON型号为：tcon_type的TCON 订单的searchid
def get_searchid_of_specified_tcon(tcon_type):
    advanced_search = {
    "0":{"search_field_name":"Task.rd_dept_id","search_field_id":"546","search_field_type":"19",
        "search_field_rel_obj":"Depts","search_opr":"TDD_OPER_EQUAL",
        "input1":"TCON","input2":'null',"offset":'null'},
    "1":{"search_field_name":"Task.status","search_field_id":"584","search_field_type":"19",
        "search_field_rel_obj":"Enums","search_opr":"TDD_OPER_EQUAL",
        "input1":"已完成","input2":'null',"offset":'null'},
    "2":{"search_field_name":"Task.plan_end_date","search_field_id":"548","search_field_type":"9",
        "search_field_rel_obj":"null","search_opr":"TDD_OPER_AFTER",
        "input1":"2022-01-01","input2":'null',"offset":'null'},
    "3":{"search_field_name":"Task.subject","search_field_id":"554","search_field_type":"5",
        "search_field_rel_obj":"null","search_opr":"TDD_OPER_INC",
        "input1":tcon_type,"input2":'null',"offset":'null'}
    }
    condition = "1 and 2 and 3 and 4"
    searchid = PyocsSoftware().get_searchid_from_advanced_search(advanced_search, condition)
    return searchid

def get_single_data_list(list_xpath, search_id):
    url = 'http://ocs-api.gz.cvte.cn/tv/Tasks/index/ContractTask/limit:200/direction:desc/sort:Task.update_time/SearchId:'
    url += search_id + '/range:all'
    # print(url)
    request = PyocsRequest()
    r = request.pyocs_request_get(url)
    html = etree.HTML(r.text)
    single_data_nodes = html.xpath(list_xpath)
    single_data_list = []
    for node in single_data_nodes:
        single_data_list.append(node.text)
    return len(single_data_list), single_data_list

def get_ocs_id_list(search_id):
    xpath = '//td[@class="Task_col_id"]'
    ocs_number, ocs_list = get_single_data_list(xpath, search_id)

    return ocs_number, ocs_list

def get_ocs_list_by_searchid(searchid):
    page = 1
    ocsList = []
    while True:
        searchidPara = str(searchid) + "/page:" + str(page)
        (count1tmp,list1tmp) = get_ocs_id_list(searchidPara)
        if count1tmp == 0:
            break
        ocsList = ocsList + list1tmp
        page = page + 1
    return ocsList

def send_email(mail_sender,mail_sender_passwd,mail_receivers,mail_text,mail_subject):
    ret = False
    message = MIMEText(mail_text, 'plain')
    #发件人
    message['From'] = Header(mail_sender)
    #收件人
    message['To'] =  Header(mail_receivers)
    #主题
    Subject = mail_subject
    message['Subject'] = Header(Subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect('smtp.cvte.com')
        smtpObj.login(mail_sender, mail_sender_passwd) #邮箱账号
        smtpObj.sendmail(mail_sender, mail_receivers, message.as_string())
        smtpObj.quit();
        ret = True
    except smtplib.SMTPException:
        ret = False

if __name__ == '__main__':
    # upload_tcon_sw('729683')
    url_prefix = 'http://ocs.gz.cvte.cn/tv/Tasks/view/'
    searchid1 = get_searchid_of_need_to_upload_sw()
    need_to_upload_sw_ocs_list = get_ocs_list_by_searchid(searchid1)

    #脚本上传了软件的ocs list
    processed_ocs_list = list()
    #脚本没查到相同配置的ocs list
    unprocessed_ocs_set = set()

    loger.info("待处理的订单List : " + ' '.join(need_to_upload_sw_ocs_list))

    for ocs1 in need_to_upload_sw_ocs_list:
        loger.info("开始处理订单 : " + ocs1)
        need_to_upload_sw_ocs_info = get_ocs_info(ocs1)
        searchid2 =get_searchid_of_specified_tcon(need_to_upload_sw_ocs_info['TCON型号'])
        specified_tcon_ocs_list = get_ocs_list_by_searchid(searchid2)
        if not specified_tcon_ocs_list:
            loger.info("未在已完成订单中找到相同TCON型号的订单，准备处理下一个订单\n")
            unprocessed_ocs_set.add(url_prefix + ocs1)
            continue
        loger.info("在已完成订单中找到的相同TCON型号的订单：" + ' '.join(specified_tcon_ocs_list))
        loger.info("正在查询跟 " + ocs1 + " 完全匹配的订单...")
        for ocs2 in specified_tcon_ocs_list:
            specified_tcon_ocs_info = get_ocs_info(ocs2)
            if specified_tcon_ocs_info == need_to_upload_sw_ocs_info:
                loger.info("已查询到完全匹配的订单：" + ocs2 + " ,正在引用软件...")
                PyocsSoftware().reuse_old_sw_from_src_to_dst(src_ocs=ocs2, dst_ocs=ocs1, workspace=os.getcwd())
                processed_ocs_list.append(url_prefix + ocs1 + '    --->此单引用的软件来源于：' + url_prefix + ocs2)
                break
            else:
                loger.info(ocs2 + " 与订单：" + ocs1 + " 的信息不匹配")
                unprocessed_ocs_set.add(url_prefix + ocs1)

    #邮件通知处理结果
    mail_sender = username + '@cvte.com'
    mail_receivers = username + '@cvte.com'
    mail_sender_passwd = password
    mail_subject = '【TCON 软件自动上传】'
    str1 = '\n'.join(processed_ocs_list) if processed_ocs_list else '无'
    str2 = '\n'.join(unprocessed_ocs_set) if unprocessed_ocs_set else '无'
    mail_text1 = '已自动上传软件订单如下：\n' + str1 + '\n\n'
    mail_text2 = '需手动上传软件的订单如下：\n' + str2 + '\n'
    mail_text = mail_text1 + mail_text2
    send_email(mail_sender,mail_sender_passwd,mail_receivers,mail_text,mail_subject)
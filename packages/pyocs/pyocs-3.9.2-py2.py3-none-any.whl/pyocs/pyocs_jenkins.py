import jenkins
import sys
from pathlib import Path
import os
from pyocs import pyocs_login
from pyocs import pyocs_software
import base64
import logging
import pkgutil
from pyocs.pyocs_filesystem import PyocsFileSystem
import pprint
from pyocs.pyocs_demand import PyocsDemand
from pyocs.pyocs_request import PyocsRequest
import json
import requests

class PyocsJenkins:

    jenkins_server = jenkins.Jenkins
    jenkins_prefix = "https://tvgateway.gz.cvte.cn/bff-tv-cloudbuild"
    registered_url_prefix = "http://tsc.gz.cvte.cn/v1/statistics/8750123?user="
    jenkins_real_url = ''
    special_jenkins_project_name = {
        'HISI350': 'HISI35X'
    }
    jenkins_param_dict = {
        "BASELINE_VERSION": "baselineVersion",
        "CUSTOMER_ID": "customerId",
        "MODEL_ID": "modelId",
        "BUILD_CMD": "buildCmd",
        "AUTO_MAKE_BIN": "autoMakeBin",
        "UPLOAD_OCS": "uploadOcs",
        "TEST_TYPE": "testType",
        "UPLOAD_OCS_MSG_0": "uploadOcsMess",
        "UPLOAD_SPECIFIC_OCS": "uploadSpecificOcs",
        "SET_PREUPLOAD": "setPreupload",
        "NATIVE_UPLOAD_OCS": "emmcNativeUploadOcs",
        "UPLOAD_MYOU" : "uploadMyou",
        "UPLOAD_MYOU_MSG": "uploadMyouMess",
        "OTA_BASE_BACKUP": "otaBaseBackup",
        "OTA_URL": "otaUrl",
        "OTA_SKIP_REF": "otaSkipRef",
        "SEND_CUSTOMER_EMAIL": "sendCustomerEmail",
        "EMAIL_CC": "emailCc",
        "EMAIL_TITLE": "emailTitle",
        "CHERRY_PICK": "cherryPick",
        "JIRA_KEY": "jiraKey",
        "JIRA_MSG": "jiraMess",
        "ASSIGN_NODE": "assignNode"
    }
    def __init__(self):
        pass
        # self.jenkins_server = self._create_jenkins_server()

    # jenkins采用的账号即为域账号，直接利用Pyocs_Login模块中读取json的方式
    def _create_jenkins_server(self):
        account = pyocs_login.PyocsLogin().get_account_from_json_file()
        self.jenkins_server = jenkins.Jenkins(self.jenkins_real_url, username=account['Username'], password=account['Password'],
                                 timeout=30)

    @staticmethod
    def _get_current_base_name(cur_dir: str):
        """
        #name:get_current_base_name
        #function:获得当前代码的代码名和分支名
        #return:代码名_B_分支名
        """
        repo_dir = Path(str(cur_dir) + '/.repo')
        git_mnt_dir = Path(str(cur_dir) + '/.git')
        repo_file = Path(str(cur_dir) + '/.repo/manifests.git/config')
        git_mnt_file = Path(str(cur_dir) + '/.git/config')
        url_line = ''
        branch_line = ''
        if repo_dir.exists():
            with open(str(repo_file), 'r') as f:
                for line in f.readlines():
                    if "url" in line:
                        url_line = line	 # 获得当前代码名所在行
                    if "merge" in line and "refs" not in line:
                        branch_line = line	 # 获得当前代码分支所在行
            split_list = url_line.split('/')
            project_name = split_list[-3]
            split_list = branch_line.split(' = ')
            branch_name = split_list[1].strip()
            #code_name = project_name.upper()+'_B_'+branch_name  # (大写)代码名_B_(小写)分支名
            #logging.info(code_name)
            return project_name, branch_name
        elif git_mnt_dir.exists():
            with open(str(git_mnt_file), 'r') as f:
                for line in f.readlines():
                    if "url" in line:
                        url_line = line	 # 获得当前代码名所在行
                    if "merge" in line:
                        branch_line = line	 # 获得当前代码分支所在行
            split_list = url_line.split('/')
            project_name = split_list[-4]
            split_list = branch_line.split(' = ')
            branch_name = split_list[1].strip()
            if "/" in branch_name:
                branch_name = branch_name.split('/')
                branch_name = branch_name[-1].strip()
            return project_name, branch_name
        else:
            print("此目录非repo或者.git仓库，请移步代码仓库的根目录下执行")

    @staticmethod
    def _is_monitor_base(cur_dir: str):
        """
        #name:get_current_base_name
        #function:获得当前代码的代码名和分支名
        #return:代码名_B_分支名
        """
        repo_dir = Path(str(cur_dir) + '/.repo')
        git_mnt_dir = Path(str(cur_dir) + '/.git')
        repo_file = Path(str(cur_dir) + '/.repo/manifests.git/config')
        git_mnt_file = Path(str(cur_dir) + '/.git/config')
        code_url = ''
        if repo_dir.exists():
            with open(str(repo_file), 'r') as f:
                for line in f.readlines():
                    if "url" in line:
                        code_url = line	 # 获得当前代码名所在行
        elif git_mnt_dir.exists():
            with open(str(git_mnt_file), 'r') as f:
                for line in f.readlines():
                    if "url" in line:
                        code_url = line	 # 获得当前代码名所在行
        if 'Monitor' in code_url or 'NT68468' in code_url or 'NT68811' in code_url or 'NT68870' in code_url:
            ret = True
        else:
            ret = False
        return ret

    @staticmethod
    def _get_customer_name(cur_dir: str, model_id: str):
        """
        #name:get_customer_name
        #function:获得当前MODEL_ID的客户名
        #return:CUSTOMER_XX
        """
        str_model_id = model_id

        if 'CS' in str_model_id or 'CP' in str_model_id:
            code_customer_path = '/customers/customer/'
            customer_dir = Path(str(cur_dir) + code_customer_path)
            str_grep_cmd = "grep -rIsl " + model_id + " " + str(customer_dir)
            logging.info(str_grep_cmd)
            file_name = os.popen(str_grep_cmd).read()
            logging.info(file_name)
            if 'customer_' not in file_name:
                raise RuntimeError("未找到此MODEL_ID，请确认输入")
        else:
            raise RuntimeError("请输入正确的modleid")
        split_list = file_name.split("/")
        customer_file_name = split_list[len(split_list)-1].strip()  #  得到customer_xx.h
        customer_name = customer_file_name.split(".")[0].upper()  #  得到CUSTOMER_XX
        return customer_name

    def _get_jenkins_build_list(self):
        build_list = []
        jobs = self.jenkins_server.get_all_jobs()
        # jobs = server.get_jobs(5)
        for job in jobs:
            if(('CLOUD_BUILD' in job['fullname']) & ('CB_S_' in job['fullname'])):
                build_list.append(job['fullname'])
        return build_list

    def _get_jenkins_project_name(self, project: str, branch: str):
        build_list = self._get_jenkins_build_list()
        for build_job in build_list:
            build_name = build_job.split('/')[-1]
            branch_name = build_name.split('_B_')[-1]
            project_name = build_name.split('_B_')[0].split('_S_')[-1]
            if project == project_name and branch == branch_name:
                return build_job
        return ""

    def get_log_of_current_model_id(self,model_id):
        """
        根据传入的model id，从最近十个log中查找对应的log信息并返回[what]字段的信息
        :param :model_id
        :return:sw_comment_default
        """
        i=-1
        info = [[]]
        ocs_id = model_id.split('_',1)[0]
        sw_comment_default = ""

        code_root_dir = PyocsFileSystem.get_current_code_root_dir()
        customer_dir = code_root_dir + '/customers'
        cur_path = os.getcwd()  # 获得当前路径
        #如果不在customer 路径下，则直接返回空字符串
        if cur_path == customer_dir:
            r = os.popen('git log')
        else:
            return sw_comment_default        

        commit_text_num = 10 #待获取的前commit_text_num组commit信息
        commit_text_ocs_line = 3 #commit 信息中的model ID字段
        commit_text_what_line = 4#commit 信息中的[what]字段
        commit_separation_text = 'commit'

        tmp = commit_text_num
        #获取前 commit_text_num 组commit信息
        while True:
            new_line = r.readline().strip()  # 去除首尾空格
            if tmp > -1:
                if new_line != "":
                    if new_line.find(commit_separation_text) == -1:  # 没找到commit，说明仍属于当前commit log
                        info[i].append(new_line.strip('\r\n'))
                    else:  # 新的一段commit开始了
                        tmp = tmp - 1
                        i = i + 1
                        info.append([])
                        info[i].append(new_line.strip('\r\n'))  # 插入commit行
            else:
                break

        # 以ocs ID为关键字，在前n组commit 信息中查找最近一次提交的commit信息
        for k in range(commit_text_num):
            try:
                if info[k][commit_text_ocs_line].find(ocs_id) != -1:
                    sw_comment_default = info[k][commit_text_what_line][info[k][commit_text_what_line].find('[what]') + 6:]
                    break
            except IndexError:
                return ''
        return sw_comment_default

    def get_param_from_interaction(self, model_id, build_cmd_param_dict):
        """
        从Linux命令行用交互的方式获取编译参数，此函数适用于Linux命令行环境
        :param model_id:
        :return:
        """
        code_root_dir = PyocsFileSystem.get_current_code_root_dir()
        is_mnt = self._is_monitor_base(code_root_dir)
        customer_dir = code_root_dir + '/customers'
        project, branch = self._get_current_base_name(cur_dir=code_root_dir)
        if project in self.special_jenkins_project_name:
            project = self.special_jenkins_project_name[project]
        print('方案：' + project)
        print('分支：' + branch)

        test_type_tuple = ("N", "A", "B", "C", "D", "E", "F")
        if is_mnt:
            compile_param_dict = {
                'projectName': project,
                'branchName': branch,
                'CUSTOMER_ID': 'CUSTOMER_CVTE',
                'MODEL_ID': '',
                'BASELINE_VERSION': '',
                # 'BUILD_CMD': 'make ocs',
                'UPLOAD_OCS': 'True',
                'TEST_TYPE': 'N',
                'UPLOAD_OCS_MSG_0': 'update software',
                'PROJ_SEL': ''
            }
        else:
            compile_param_dict = {
                'projectName': project,
                'branchName': branch,
                'CUSTOMER_ID': 'CUSTOMER_CVTE',
                'MODEL_ID': '',
                'BASELINE_VERSION': '',
                # 'BUILD_CMD': 'make ocs',
                'UPLOAD_OCS': 'True',
                'TEST_TYPE': 'N',
                'UPLOAD_OCS_MSG_0': 'update software',
                'AUTO_MAKE_BIN': '',
                'NATIVE_UPLOAD_OCS': ''
            }

        compile_param_dict.update(build_cmd_param_dict)# 合并两个参数表
        customer_name = self._get_customer_name(cur_dir=code_root_dir, model_id=model_id)
        print("CUSTOMER_ID：" + customer_name)
        print("MODEL_ID：" + model_id)
        task_type = None
        ocs_number = str(model_id).split("_")[0][2:]  # 从modleid截取OCS号
        if ocs_number.isdigit():  # 如果符合内部命名规则则去做测试类型提醒
            sw = pyocs_software.PyocsSoftware()
            current_test_type = sw.get_test_type_from_ocs(ocs_number)
            py_demand = PyocsDemand(ocs_number)
            task_type = py_demand.get_task_type()
            if current_test_type is None:
                current_test_type = "当前OCS为样机或无软件"
            print("OCS最新软件测试类型：" + current_test_type)
        if is_mnt:
            mnt_prj_dick = {'RTD2270-acer':              {'1': 'ID_SCALER_RL6230_AcerNew_Project', '2': 'ID_SCALER_RL6336_AcerNew_Project'},
                            'RTD2281CL-vsc':             {'1': 'ID_SCALER_CVT_HKC_RL6336_Project', '2': 'ID_SCALER_CVT_GW_RL6336_Project'},
                            'RTD1959-mnt2556':           {'1': 'ID_SCALER_RL6432_Project', '2': 'ID_SCALER_RL6463_Project'},
                            'RTD2513-rtd2513_autobuild': {'1': 'ID_SCALER_RL6463_Project'},
                            'NT68676-68676_autobuild':   {'1': 'ID_SCALER_NT68676_Demo_Board'}
            }
            while 1:
                mnt_match = project + '-' + branch
                if mnt_match == 'RTD2270-acer':
                    print("Keil工程选项：\n"
                        "1 : ID_SCALER_RL6230_AcerNew_Project\n"
                        "2 : ID_SCALER_RL6336_AcerNew_Project"
                    )
                elif mnt_match == 'RTD2281CL-vsc':
                    print("Keil工程选项：\n"
                        "1 : ID_SCALER_CVT_HKC_RL6336_Project\n"
                        "2 : ID_SCALER_CVT_GW_RL6336_Project"
                    )
                elif mnt_match == 'RTD1959-mnt2556':
                    print("Keil工程选项：\n"
                        "1 : ID_SCALER_RL6432_Project\n"
                        "2 : ID_SCALER_RL6463_Project"
                    )
                elif mnt_match == 'RTD2513-rtd2513_autobuild':
                    print("Keil工程选项：\n"
                        "1 : ID_SCALER_RL6463_Project"
                    )
                elif mnt_match == 'NT68676-68676_autobuild':
                    print("Keil工程选项：\n"
                        "1 : ID_SCALER_NT68676_Demo_Board"
                    )
                else:
                    print('该方案Keil工程编译选项为空，请添加！！！')
                    break
                ret = input("请输入编译工程：")
                if ret:
                    pri_sel = mnt_prj_dick[mnt_match][str(ret)]
                    compile_param_dict['PROJ_SEL'] = pri_sel
                    break
                else:
                    print('请选择编译工程！！！')
                    continue
        if (task_type == '意向订单任务'):
            compile_param_dict['TEST_TYPE'] = "N"
        else :
            while 1:
                test_type = input("请输入测试类型（N、A、B、C、D、E、F），默认为N ：")
                if not test_type:
                    compile_param_dict['TEST_TYPE'] = "N"
                    break
                if any(test_type in tmp for tmp in test_type_tuple):
                    compile_param_dict['TEST_TYPE'] = test_type
                    break
                print("输入错误，请重新输入!")

        sw_comment_default = self.get_log_of_current_model_id(model_id)
        if not sw_comment_default:
            while 1:
                sw_comment = input("请输入软件备注信息：")
                if not sw_comment:
                    print("不要忘记软件备注信息哦")
                    continue
                else:
                    break
        else:
            sw_comment = input("请输入软件备注信息 ("+sw_comment_default +"):")
            if not sw_comment:
                sw_comment = sw_comment_default

        compile_param_dict['CUSTOMER_ID'] = customer_name
        compile_param_dict['MODEL_ID'] = model_id
        if is_mnt:
            baseline_version = 'Monitor方案没有基线'
        else:
            baseline_version = PyocsFileSystem.get_baseline_version(customer_dir=customer_dir, customer_id=customer_name)
        print('基线版本：' + baseline_version)
        baseline_name = baseline_version
        compile_param_dict['BASELINE_VERSION'] = baseline_name
        compile_param_dict['UPLOAD_OCS_MSG_0'] = sw_comment
        if is_mnt is False:
            while 1:
                ret = input("请确认是否做BIN（Y，N），默认为N：")
                if not ret:
                    compile_param_dict['AUTO_MAKE_BIN'] = 'False'
                    compile_param_dict['NATIVE_UPLOAD_OCS'] = 'False'
                    break
                elif ret is 'Y' or ret is 'y':
                    compile_param_dict['AUTO_MAKE_BIN'] = 'True'
                    compile_param_dict['NATIVE_UPLOAD_OCS'] = 'True'
                    break
                elif ret is 'N' or ret is 'n':
                    compile_param_dict['AUTO_MAKE_BIN'] = 'False'
                    compile_param_dict['NATIVE_UPLOAD_OCS'] = 'False'
                    break
                else:
                    print('输入错误，请重新输入！！！')
                    continue
        pp = pprint.PrettyPrinter(indent=4)
        print("构建参数如下：")
        print("=======================================")
        pp.pprint(compile_param_dict)
        print("=======================================")
        return compile_param_dict

    """
    #传入model_id ,创建jenkins编译任务
    """
    def create_jenkins_job(self, model_id, build_cmd_param_dict):
        compile_param = self.get_param_from_interaction(model_id, build_cmd_param_dict)
        compile_param_new = {}
        for key, value in compile_param.items():
            if key in self.jenkins_param_dict.keys():
                compile_param_new[self.jenkins_param_dict[key]] = value
            else:
                compile_param_new[key] = value
        master = self.get_jenkins_master(compile_param["projectName"], compile_param["branchName"])
        self._create_jenkins_job(compile_param=compile_param_new, master=master)

    def get_last_build_url(self, project_name):
        server = self.jenkins_server
        last_build_number = server.get_job_info(project_name)['lastBuild']['number']
        build_info = server.get_build_info(project_name, last_build_number)
        return build_info['url']

    def _create_jenkins_job(self, compile_param, master):
        '''
        使用api的方式触发编译
        :param compile_param: 编译参数
        :param job: JOB URI
        :param project_name: 方案名
        :param branch_name: 分支名
        :return:
        '''
        account = pyocs_login.PyocsLogin().get_account_from_json_file()
        #拿到中文名字
        if "userCn" not in account:
            if account["Username"] == "ocs_tsc":
                account["userCn"] = "公共账号"
            else:
                token = requests.get(
                    "http://tvdevops.gz.cvte.cn/commonservice/noauth/v1/token/get_token?appId=2618d6a0-a887-44b0-869f-9c8eb9ce1073&appSecret=6e009a75-3f5e-49b5-adea-945c02c557be&tokenName=ITAPI")
                headers = {
                    "x-iac-token": json.loads(token.text)["data"]
                }
                ret = requests.get(
                    "https://itapis.cvte.com/wuli-service/user/search/" + account["Username"],
                    headers=headers)
                for item in json.loads(ret.text)["data"]:
                    if item["alias"] == account["Username"]:
                        account["userCn"] = item['userCn']
                        break
        fields = {
            "userAccount": account["Username"],
            "userName": account["userCn"],
            "masterName": master,
            "params": compile_param
        }
        ret = PyocsRequest().pyocs_request_post_json(
            self.jenkins_prefix + "/api/v1.0/build-trigger/start-build",
            json=fields, timeout=300)
        if ret.status_code == 200:
            ret_dict = json.loads(ret.text)
            if ret_dict["httpStatus"] == 200:
                print("提交编译成功，jenkins 编译链接： " + str(ret_dict["data"]))
            else:
                print("提交编译失败，返回信息：")
                print(ret_dict)
            self.jenkins_registered(account["Username"])
        else:
            print("提交失败：")
            print(ret.text)

    @staticmethod
    def get_jenkins_mail_signature():
        ret = pkgutil.get_data("pyocs.resource", "mailsignature").decode("utf8")
        return ret

    def get_jenkins_master(self, project_name: str, branch: str):
        fields = {
            'projectName': project_name,
            'branchName': branch
        }
        header = {
            'Content-Type': 'application/json'
        }
        ret = PyocsRequest().pyocs_request_post_json_with_headers(self.jenkins_prefix + "/api/v1.0/build-trigger/get-code-assign-master",
                                                             json=fields, headers=header)
        ret_dict = json.loads(ret.text)
        return ret_dict["data"]["masterName"]

    def jenkins_registered(self, user_name):
        ret = PyocsRequest().pyocs_request_post(self.registered_url_prefix + user_name, data=None)
        return ret.status_code == 200

from pyocs import pyocs_login
import requests
import base64

import json
url = "https://tvgateway.gz.cvte.cn/bff-tv-jenkins/api/v1.0/build/build-job"

class Pyocs_Jenkins():

    @staticmethod
    def create_jenkins_job(master, jobUri, jobName, params):
        """
        用来创建jenkins任务的通用接口，由于jenkins 认证需要有token，你需要在.account.json 中加入你的token：
        格式："jenkins_token": "{'tvci':'your token'}"
        示例：
        {
            "Username": "<username>",
            "Password": "<password>",
            "jenkins_token": "{'tvci':'your jenkins token'}"
        }
        token 获取方式：jenkins中点击用户名->设置->添加新的API Token

        :param master:
        :param jobUri:
        :param jobName:
        :param params:
        :return:
        """
        payload = json.dumps({
            "masterName": master,
            "jobUri": jobUri,
            "jobName": jobName,
            "params": params
        })

        user_info = pyocs_login.PyocsLogin.get_account_from_json_file()
        tokens = json.loads(json.dumps(eval(user_info["jenkins_token"])))
        authorization = user_info["Username"] + ":" + tokens[master]

        headers = {
            'Content-Type': 'application/json',
            'Authorization': base64.b64encode(authorization.encode())
        }
        ret = requests.request("POST", url, headers=headers, data=payload)
        if ret.status_code == 200 and json.loads(json.dumps(eval(ret.text)))["message"] == "success":
            print("提交成功:")
            print(ret.text)
        else:
            print("提交失败：")
            print(ret.text)

if __name__ == '__main__':
    master = "tvci"
    jobUri = "yangpingbu/"
    jobName = "Sample_Compile"
    params = {
        "OCS_NUMBER": "742342",
        "AUTO_MAKE_BIN": "True",
        "COMPILE_SOFTWARE": "True"
    }
    Pyocs_Jenkins.create_jenkins_job(master, jobUri, jobName, params)
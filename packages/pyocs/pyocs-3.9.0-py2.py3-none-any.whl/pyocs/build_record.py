import requests
import json
create_build_record_url = "https://tvgateway.gz.cvte.cn/httppyocs/api/v1/pyocs/create_build_record"
check_build_record_url = "https://tvgateway.gz.cvte.cn/httppyocs/api/v1/pyocs/get_record_by_ocs?ocsNo="
update_build_record_url = "https://tvgateway.gz.cvte.cn/httppyocs/api/v1/pyocs/update_build_record"
class BuildRecord:
    _instance = None
    client = None

    # 单例模式
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(BuildRecord, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        pass

    @staticmethod
    def create_build_record(ocs_num, prj_name):
        fields = json.dumps({
            "branch": "string",
            "buildFlag": 0,
            "changeId": "string",
            "data1": "string",
            "data2": "string",
            "data3": "string",
            "data4": "string",
            "data5": "string",
            "jenkinsUrl": "string",
            "ocsNo": ocs_num,
            "optUser": "string",
            "project": prj_name,
            "recordCount": 0,
            "recordDesc": "string",
            "recordType": 0
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", create_build_record_url, headers=headers, data=fields)
        return response.text

    @staticmethod
    def check_build_record(ocs_num):
        response = requests.request("GET", check_build_record_url + str(ocs_num))
        return response.text

    @staticmethod
    def update_build_record(ocs_num, buildFlag, recordType, recordDesc):
        """
        :param ocs_num: ocs 号
        :param buildFlag: 取值0: 编译成功 取值1: 编译失败
        :param recordType:
        取值1: 外部系统网络请求    ==> 排查系统配合原因
        取值2: OCS参数解析         ==> xpath定位解析规则
        取值3: 方案规则            ==> OCS参数缺失 / 规则有逻辑问题
        取值4: 创建订单            ==> 订单文件编辑格式问题
        取值5: 软件编译报错        ==> 比较复杂, 后续规范项目Jenkins任务的pipeline收集
        :param recordDesc:具体问题描述
        :return:接口返回值
        """
        fields = json.dumps({
            "ocsNo": ocs_num,
            "buildFlag": buildFlag,
            "recordDesc": recordDesc,
            "recordType": recordType
        })
        print(fields)
        headers = {
            'Content-Type': 'application/json'
        }
        data_check_ret = json.loads(BuildRecord.check_build_record(ocs_num))["data"]
        if data_check_ret:
            response = requests.request("PUT", update_build_record_url, headers=headers, data=fields)
            return response.text
        else:
            print("配置管理埋点----》无此订单信息：" + str(ocs_num))
            return None

if __name__ == "__main__":
    print(BuildRecord.update_build_record(123456, 1, 1, "接口测试1"))
    #print(BuildRecord.check_build_record("123457"))
需求
1、识别每天新建的需求未提供的订单，url :  http://ocs.gz.cvte.cn/tv/Tasks/index/ContractTask//SearchId:2091062/range:all
2、找到每个订单的摘要里的客料号
3、根据客料号在全部订单里，http://ocs.gz.cvte.cn/tv/Tasks/index/range:all/ 输入摘要找到相同客料号的订单（返回的订单列表不为空），从返回的订单列表里找到最新的一个相同机型的订单。非自身的订单
4、获取那个订单的ID
5、如果是和自身相同的订单，则说明只有一个，用http://tvci.gz.cvte.cn/job/yangpingbu/job/Sample_Compile/build 来提交自动编译
6、如果有和自身不同的订单，（非审核，测试不通过，且非为待处理需求）http://tvci.gz.cvte.cn/job/Utility_Tools/job/reuse_stock_software/build


附加功能：禁用的，打出禁用信息邮件给相应工程师。链接+禁用理由。申请解禁


#1、抓取所有待录入需求的软件信息
#2、根据料号找到库存软件
#3、从后往前找相同机型的待上传软件和已完成的软件，获取OCS号(后续加是否禁用，禁用则获取禁用软件链接和禁用理由，发邮件给工程师申请解禁)
#
#4、找到有可用的ocs号，则提交reuse库存软件
#5、没有库存软件，则提交自动编译（后续加判断是否支持自动编译以及是否要做bin）
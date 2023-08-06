===================================
    惠迪 v56 需求表自动生成软件
===================================
文件介绍
1、auto_git_commit.py--->自动提交代码(包括自动填写git log 、git add 、git commit 、git reset 、git pull 、git cherry-pick、git push)
2、auto_jenkins.py---->自动提交jenkins 编译
3、customer_data.py---->modeID 生成逻辑。客户需求分析。logo、屏、遥控器、等等
4、excel_deal.py---->excel表分析处理数据
5、v56huidi_auto_modeid.py--->主函数逻辑



如下 123步 可以让你在服务器任何文件路径下执行 v56huidi_auto_modeid.py

	1、在服务器根目录 建立 Tools文件夹。将HUIDI56文件夹放入Tools中

	2、@FDK11:~$vim .bashrc 在文件最后输入如下内容，并保存
	export PATH=~/Tools/HUIDI56:$PATH

	3、source .bashrc


修改 excel_deal.py中 workbook=openpyxl.load_workbook("/disk2/zhaoxinan/Toolszxn/AUTOMODEID/HUIDI56/惠迪-软件需求表.xlsx") 
文件路径为需求表的绝对路径,方便脚本执行时能找到文件 例如：XXXXX/Tools/HUIDI56/惠迪-软件需求表.xlsx")

每次更新需求表，要将最新的需求表保存在HUIDI56文件夹下


======================================
Git自动提交操作篇。目前还用不了。后续有用
======================================

由于modeID修改是在customer仓库。
所以后续执行脚本在v56fae/customer 仓库下执行。示例 ：@FDK11:~$v56huidi_auto_modeid.py 24

wirte_modeid_in_customer.py 中 customer_cy_56_path = "/disk2/zhaoxinan/56fae/customers/customer/customer_huidi/customer_huidi.h"
这个路径是customer_huidi.h的绝对路径，脚本需要查找并进行文件操作，改成自己的customer_huidi.h文件路径。


======================================
Jenkins 自动提交编译。目前还用不了。后续有用
======================================

修改 auto_jenkins.py 里面的域账户域密码即可。

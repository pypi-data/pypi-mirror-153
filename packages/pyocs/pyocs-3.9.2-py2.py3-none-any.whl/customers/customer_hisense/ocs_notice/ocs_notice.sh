#!/bin/bash

cd /home/user/code/codes/ocs_notice
FILE_PATH="/home/user/code/codes/ocs_notice/result/"
TODAY=`date +"%Y-%m-%d"`
weekdate=`date +%w`
rundata="4,5"

datafile=$FILE_PATH$TODAY

if [ ! -f $datafile ];then
	touch $datafile
fi

sendmail=0

if echo $rundata | grep $weekdate;then
	sendmail=1
	echo "need send mail..."
else
	sendmail=0
	echo "not need send mail..."
fi

python3 Gui_OCS_Notice_NotUI.py $sendmail $datafile

exit 0

#!/bin/bash

com_list1=`ls   -l  cpd-*.com  |  awk    '{printf("%s \n", $NF) }'`             
num_com_list1=`ls   -l  cpd-*.com  |  awk    '{printf("%s \n", $NF) }' |  wc  -l  `
log_com_list2=`ls   -l  cpd-*.log  |  sed  's/.log/.com/g'   | awk    '{printf("%s \n", $NF) }'`              
num_log_com_list2=`ls   -l  cpd-*.log  |  sed  's/.log/.com/g'   | awk    '{printf("%s \n", $NF) }'  | wc  -l `

list_concat12=`  echo  "$com_list1      $log_com_list2"  ` 
list_concat122=`  echo  "$com_list1      $log_com_list2   $log_com_list2 "    `
list_concat21=`  echo  "$log_com_list2      $com_list1   "    `
list_concat211=`  echo  "$log_com_list2      $com_list1    $com_list1  "    `

intersection12=` for  inf in  $list_concat12 ; do echo  "$inf"; done     |  sort   |  uniq    -d     `
num_intersection12=` for  inf in  $list_concat12 ; do echo  "$inf"; done     |  sort   |  uniq   -d     |    wc   -l  `

union12=` for  inf in  $list_concat12 ; do echo  "$inf"; done     |  sort   |  uniq       `
num_union12=` for  inf in  $list_concat12 ; do echo  "$inf"; done     |  sort   |  uniq       |    wc   -l  `

set_1diff2=` for  inf in  $list_concat122 ; do echo  "$inf"; done     |  sort   |  uniq   -u `
num_set_1diff2=` for  inf in  $list_concat122 ; do echo  "$inf"; done     |  sort   |  uniq   -u       |    wc   -l    `

set_2diff1=` for  inf in  $list_concat211 ; do echo  "$inf"; done     |  sort   |  uniq   -u `
num_set_2diff1=` for  inf in  $list_concat211 ; do echo  "$inf"; done     |  sort   |  uniq   -u       |    wc   -l     `

set_1symdiff2=` for  inf in  $list_concat12 ; do echo  "$inf"; done     |  sort   |  uniq    -u    `
num_set_1symdiff2=` for  inf in  $list_concat12 ; do echo  "$inf"; done     |  sort   |  uniq   -u     |    wc   -l  `


echo  " "
echo "com_list1: "
echo "$com_list1"
echo "num_com_list1= $num_com_list1"

echo  " "
echo "log_com_list2: "
echo "$log_com_list2"
echo "num_log_com_list2= $num_log_com_list2"

echo  " "
echo  "intersection12: "
echo  "$intersection12"
echo  "num_intersection12= $num_intersection12 "

echo  " "
echo  "union12: "
echo  "$union12"
echo  "num_union12= $num_union12"

echo  " "
echo  "set_1diff2: "
echo  "$set_1diff2"
echo  "num_set_1diff2= $num_set_1diff2"

echo  " "
echo  "set_2diff1: "
echo  "$set_2diff1"
echo  "num_set_2diff1= $num_set_2diff1"

echo  " "
echo  "set_1symdiff2: "
echo  "$set_1symdiff2"
echo  "num_set_1symdiff2= $num_set_1symdiff2"

echo -e "\nBegin removing set_1diff2: the difference set from 1 to 2."
for  inf in  $set_1diff2;
do
	echo "remove file: ${inf}"
	rm   -f   ${inf} ; 
done;
echo -e "End of removing set_1diff2.\n"

echo  "End of program!"


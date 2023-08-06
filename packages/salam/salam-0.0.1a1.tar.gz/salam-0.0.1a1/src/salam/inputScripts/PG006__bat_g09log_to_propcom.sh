#!/bin/bash

if [ $# -eq 1 ]; then
	model_file=$1
	#----------------------------------------------------------
	for  inf  in  cpd*.log
	do
		tmp_file_name=${inf%.log}.tmp
		/usr/local/bin/obabel    -ig09   ${inf}     -ocom     -O${tmp_file_name}
	done
	
	#----------------------------------------------------------
	for  inf1  in  cpd*.tmp
	do
		sed -i '1, 5 d'   ${inf1}
	done
	
	#----------------------------------------------------------
	for  inf2   in  cpd*.tmp
	do
		com_file_name=${inf2%.tmp}.com
		cp   ${model_file}     ${com_file_name}
		cat    ${inf2}    >>   ${com_file_name}  
	done
	
	#----------------------------------------------------------
	for  inf3   in  cpd*.com
	do
		sed  -i "s/^%chk=..*$/%chk=${inf3%.com}.chk/"  ${inf3}
	done
	
	#----------------------------------------------------------
	rm -f  cpd*.tmp 2> /dev/null 
	
	mkdir  log-files   2> /dev/null
	mkdir  com-files   2> /dev/null

	mv    cpd*.log     log-files/     2> /dev/null   
	mv    cpd*.com     com-files/     2> /dev/null 

else
	echo 'Error input parameter!'
	echo 'This script can creat gaussian com file from a model computation file and *.log files in current dir.'
	echo 'Usage : ./bat-g09log-to-tadfcom.sh   "model-comput-file-com"  '
	exit 1

fi

#END



#!/bin/bash

#while  getopts  ":r:"   $OPT; 
#	do
#		case  $OPT in
#		r)	echo "The opt in r."
#			echo "OPTARG: $OPTARG"
#			echo "OPTIND: $OPTIND"
#			;;
#		*) 	echo "wrong option."
#			;;
#		esac
#	done


compute_ratio=1
Generation="G"


if [ $# -eq 2 ]; then
	compute_ratio=$1
	Generation=$2
elif [ $# -eq 1 ]; then
	compute_ratio=$1
else
	echo "compute_ratio and  Generation not defined, default values will be used."
fi


echo  "compute_ratio = $compute_ratio"
echo  "Generation = ${Generation}"



num_of_comfile=`ls -l   cpd*.com |  wc  -l `
echo  "num_of_comfile= $num_of_comfile"

num_pbs_jobs=` echo  "$num_of_comfile * $compute_ratio "  |  bc   |   awk   '{printf("%.0f", $NF  )}' `
echo  "num_pbs_jobs = $num_pbs_jobs"

com_list=`ls   cpd*.com `

restrict_com_list=` ls -l   cpd*.com   |    awk   '{print  $NF }'   |   head   -$[ $num_pbs_jobs + 0]    `



bat_qsub_jobs() {

	for  inf  in  $restrict_com_list
	do
	
		newname=`echo  ${inf} |  sed 's/.com//g'  |  sed  's/cpd-//g'  `  
		echo ${newname}  
		logfile=${inf%.com}.log
		
		if [ -f "./${logfile}" ]; then
			num_normal_term=` grep "Normal termination"    -c     ./${logfile} `
			if [ ${num_normal_term} == 1 ]; then
				echo "${logfile} exit, do not qsub!  num_normal_term = ${num_normal_term}"
			else
				echo "${logfile} exit, num_normal_term = ${num_normal_term}.  qsub again!"
		        	/home/tucy/bin/Modify_g09_pbs_2.sh    $inf     ${Generation}-prop-${newname}    g16.pbs.sh 
		        	/usr/local/torque/bin/qsub  g16.pbs.sh
			fi
		else
			/home/tucy/bin/Modify_g09_pbs_2.sh    $inf     ${Generation}-prop-${newname}    g16.pbs.sh 
			/usr/local/torque/bin/qsub  g16.pbs.sh
		fi
	
	done
}


bat_qsub_jobs



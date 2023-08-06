#!/bin/bash

logfiles=`ls  cpd*.log`

if [ !  -d  ./finished/  ]; then
mkdir  ./finished/   2>/dev/null
fi 

if [ !  -d  ./modification/  ]; then
mkdir  ./modification/    2>/dev/null
fi

for  inf  in  ${logfiles}
do
nb_normal_termi=` grep "Normal termination" --color -c   ${inf} `
comfile=${inf%.log}.com
chkfile=${inf%.log}.chk

if [ $nb_normal_termi == 2  ]; then
cp  ${comfile}  ./finished/
cp  ${inf}      ./finished/

elif [ $nb_normal_termi == 1 ];  then
cp  ${comfile}   ./modification/
cp  ${inf}       ./modification/
cp  ${chkfile}   ./modification/  2>/dev/null 
echo "${inf} opt failed!"

else [ $nb_normal_termi == 0 ] 
#rm  -f  ${inf}   2>/dev/null 
#rm  -f  ${chkfile}  2>/dev/null
echo "${inf} opt freq failed!"

fi

done


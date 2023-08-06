#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 14:21:51 2021

This is the global drive script of the so-called 
SALAM algorithm (Self-consistent generation Algorithm for vitual compound Library of high-Abundance target Materials)
for machine learning and mutation driven molecular property optimization.


@author: tucy
"""


# import sys 
# import os
# main_wkdir = os.getcwd()
# sys.path.append(main_wkdir)


import os
import time
import subprocess
import datetime

from module_MD.Metrics import percentage_lt_criticval
from module_MD.Metrics import accumulate_optmols 
from module_MD.Metrics import accumulate_optmols_S1En
from module_MD.Metrics import accumulate_optmols_intersection
# from module_MD.Metrics import get_allfrags_via_bricsdecompose
from module_MD.Metrics import get_num_replaceable_aromatic_CHs
from module_MD.Metrics import get_paras_dic
from module_MD.Metrics import convert_str_to_list
from module_MD.Metrics import sort_mols_by_SAScores
from module_MD.Metrics import plot_muation_diagram


import pandas as pd
from matplotlib import pyplot as plt

import argparse

parser = argparse.ArgumentParser(description="manual to this script: ")

parser.add_argument('--inp', 
                    type=str, 
                    default='./salam_paras.inp', 
                    required=False, 
                    metavar='--input_filename', 
                    help='The input filename which stores the parameters for running of the program.')

parser.add_argument('--output', 
                    type=str, 
                    default='./SALAM.log', 
                    required=False, 
                    metavar='--output_filename', 
                    help='The output filename which stores the result of the program.')

parser.add_argument('--restart_maxminpicker', type=bool, default=False )
parser.add_argument('--restart_generation', type=int, default=-1)
parser.add_argument('--restart_optjob', type=bool, default=False )
parser.add_argument('--restart_propjob', type=bool, default=False )


args = parser.parse_args()

print("input: ", args.inp, " ; the type is ", type(args.inp) )
INPUT_FILE = args.inp

print("output: ", args.output, " ; the type is ", type(args.output) )
OUTPUT_FILE = args.output

print("restart_maxminpicker: ", args.restart_maxminpicker, " ; the type is ", type(args.restart_maxminpicker) )
RESTART_MAXMINPICKER = bool(args.restart_maxminpicker)

print("restart_generation: ", args.restart_generation, " ; the type is ", type(args.restart_generation) )
RESTART_GENERATION = args.restart_generation

print("restart_optjob: ", args.restart_optjob, " ; the type is ", type(args.restart_optjob) )
RESTART_OPTJOB = bool(args.restart_optjob)

print("restart_propjob: ", args.restart_propjob, " ; the type is ", type(args.restart_propjob) )
RESTART_PROPJOB = bool(args.restart_propjob)


#------- get parameters via calling get_paras_dic -----------------------------
PARAS_DIC = get_paras_dic(filename=INPUT_FILE)

SLEEP_SECONDS = int( PARAS_DIC['SLEEP_SECONDS'] )

# GXXXX = 'G%04d'%PARAS_DIC['MUTATION_GENERATION']
# PXXXX = 'P%04d'%PARAS_DIC['MUTATION_GENERATION']
# OXXXX = 'O%04d'%PARAS_DIC['MUTATION_GENERATION']
# GXXXXPLUSONE = 'G%04d'%(PARAS_DIC['MUTATION_GENERATION'] +1)


#-----------------------------------------------------------------------------
SALAM_LOG = OUTPUT_FILE                          #  "./SALAM.log"  # the output log for SALAM.py 
module_name = 'moduleMD'
src_dir = 'src/'

TERMINO_HYDROGEN_SUBS =  convert_str_to_list(str1=PARAS_DIC['TERMINO_HYDROGEN_SUBS']) 

TERMINO_HYDROGEN_SUBS_CMD_PARA = "  "
for i in range(len(TERMINO_HYDROGEN_SUBS)): 
    TERMINO_HYDROGEN_SUBS_CMD_PARA += "  --termino_hydrogen_subs='%s' "% TERMINO_HYDROGEN_SUBS[i]


MAX_SUBPOS              =  int( PARAS_DIC['MAX_SUBPOS'] )
SUBSTI_NUMBER_CARBON    =  int( PARAS_DIC['SUBSTI_NUMBER_CARBON'] )
SAMPLE_NUMBER_CARBON    =  int( PARAS_DIC['SAMPLE_NUMBER_CARBON'] )
SUBSTI_NUMBER_HYDROGEN  =  int( PARAS_DIC['SUBSTI_NUMBER_HYDROGEN'] )
SAMPLE_NUMBER_HYDROGEN  =  int( PARAS_DIC['SAMPLE_NUMBER_HYDROGEN'] )

mutation_ctl_para_names = [ 'max_subpos', 'substi_number_carbon', 'sample_number_carbon', 'substi_number_hydrogen', 'sample_number_hydrogen' ]
mutation_ctl_para_values = [ MAX_SUBPOS, SUBSTI_NUMBER_CARBON, SAMPLE_NUMBER_CARBON, SUBSTI_NUMBER_HYDROGEN, SAMPLE_NUMBER_HYDROGEN ]

MUTATION_CONTROL_CMD_PARA = "  "
for name1, value1 in zip(mutation_ctl_para_names, mutation_ctl_para_values): 
    MUTATION_CONTROL_CMD_PARA += "   --%s=%d   "%(name1, value1)


#-----------------------------------------------------------------------------
PROG_LIST0 = [
            'PG001__Generate_G0000.py',
            'PG002__MaxMinPicker.py',
            'PG003__bat_sdf_to_gscom.py',
            'PG004__bat_qsub_jobs_opt.py',
            'PG005__optimization_analysis_completeness.py',
            'PG006__bat_g09log_to_propcom.py',
            'PG007__bat_qsub_jobs_prop.py',
            'PG008__property_analysis_completeness.py',
            'PG009__property_analysis_summary.py',
            'PG010__featurizers_train_evaluate.py',
            'PG011__predict_opt_molecules.py',
            'PG012__Generate_Gnew.py',    
            # 'PG012a__Generate_Gnew_Debranch.py',
            'PG013__MurckoScaffold.py',
            'PG014__Energy_Sieve.py',
            'PG015__Map-mols-by-FPSimilarity.py'
            ]

PROG_LIST = [ './' + src_dir + x  for x in PROG_LIST0]


#--------- definitions for functions ------------------------------------------
#------------------------------------------------------------------------------
def call_cmd_via_subprocess_run(cmd,
                                loop_time_limit=10000,
                                sleep_seconds=SLEEP_SECONDS
                                ):
    loop_time = 0
    returncode = -9999
    print("calling call_cmd_via_subprocess_run.")
    while( (returncode != 0)  and (loop_time < loop_time_limit) ):
        try:
            print("loop_time = ", loop_time)
            cmd_CompletedProcess = subprocess.run(args=cmd,
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE,
                                                  shell=True,
                                                  check=True
                                                  )
            #cmd = cmd_CompletedProcess.args
            returncode = cmd_CompletedProcess.returncode
            stdoutput = cmd_CompletedProcess.stdout.decode()
            
            print("Normal call.")
            #print("cmd = ", cmd)
            print("in correct branch: loop_time = ", loop_time, " , returncode = ", returncode)
            print("stdout is: ")
            print(stdoutput)

            
        except subprocess.CalledProcessError as e:
            returncode = e.returncode
            stderr = e.stderr.decode()
            print("subprocess.CalledProcessError")
            print("stderr : ", stderr)
        
            print("in error branch:  loop_time = ", loop_time, " , returncode = ", returncode)
            print("sleep for a while, and retry.")
            time.sleep(sleep_seconds)
            
            #loop_time += 1
            
        # except subprocess.TimeoutExpired as t:
        #     returncode = t.returncode
        #     stderr = t.stderr.decode()
            
        #     print("subprocess.TimeoutExpired")
        #     print("stderr : ", stderr)
        
        loop_time += 1
        print("outside try:  loop_time = ", loop_time, " , returncode = ", returncode)
        

def run_PG001():
    #------- run PG001 with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[0],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[0]  +   "  '      1>  "   +  SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
    
    call_prog_with_para1 =  "python   " +  PROG_LIST[0]   +  "      1>>  "    +   SALAM_LOG
    os.system( call_prog_with_para1 )
    #------- end run PG001  PG001__Generate_G0000.py------------------------------------------------------------------


def run_PG002():
    #------- run PG002 with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[1],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[1]  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
    
    call_prog_with_para2 =  "python   " +  PROG_LIST[1]  \
        +   "   --GXXXX=%s"%GXXXX  \
            +  "   --PXXXX=%s"%PXXXX  \
                +  "   --OXXXX=%s"%OXXXX   \
                    +  "    --pickmols_size=%d"% int( PARAS_DIC['PICKMOLS_SIZE'] ) \
                        +  "      1>>    "    +   SALAM_LOG
    
    os.system( call_prog_with_para2 )
    #------- end run PG002  PG002__MaxMinPicker.py------------------------------------------------------------------
    

def run_PG003():
    #------- run PG003 with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[2],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[2]  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
    
    call_prog_with_para3 =  "python   " +  PROG_LIST[2]  \
        +   "   --GXXXX=%s"%GXXXX  \
            +  "   --PXXXX=%s"%PXXXX  \
                +  "   --OXXXX=%s"%OXXXX   \
                    +  "   --gs_opt_method=%s"%PARAS_DIC['GS_OPT_METHOD']  \
                        + "  --remote_wkdir=%s"%PARAS_DIC['REMOTE_WKDIR']   \
                            + "   --num_serviers=%d"% int( PARAS_DIC['NUM_SERVIERS'] )  \
                            +   "      1>>    "    +   SALAM_LOG
                        
    os.system( call_prog_with_para3 )
    #------- end run PG003  PG003__bat_sdf_to_gscom.py------------------------------------------------------------------





def update_acc_computedmols(acc_computedmols='./project/G0002/acc_computedmols_opt.csv',
                            old_acc_computedmols='./project/G0001/acc_computedmols_opt.csv',
                            new_computedmols='./project/G0001/P0001rev.sdf'):
    
    return 0
    
    


def cpdnames_checker(acc_computedmols='./project/G0001/acc_computedmols_opt.csv',
                    computingmols='./project/G0001/computingmols_opt.csv'):
    print("### Begin cpdnames_checker. Check whether computing_mols were in acc_computed_mols.")
    
    #  acc_computedmols_opt.csv 应该是这样一个逗号分割值文件， 包括两列， smiles 和 filepath 仅仅用首次（最原始的）被计算过的
    #  文件路径（字符串, 不包括文件名后缀）。  例如， 
    #  c1ccc(O)cc1， ‘./project/G0000/pick_mols/com-files/cpd-00016’
    #  
    #  类似地，computingmols_opt.csv 应该由 对应的 P0001.sdf 生成， 其结构为，
    #  c1ccc(O)cc1， ‘./project/G0001/pick_mols/com-files/cpd-00098’
    #
    #  计算两者的交集，获得对应的已计算过的cpdnames含路径，  将交集中的文件 (log) 拷贝到新的要计算的 opt_jobs 工作目录下，
    #  使用系统拷贝命令， cp   filepath1   to  filepath2.   
    #  
    #  主要是第一个csv文件，需要持续更新， 以便不漏过新增的分子。   
    
    
    print("### End of cpdnames_checker")
    
    return 0
    

    

def run_PG004():
    #------- run PG004 with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[3],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[3]  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
    
    call_prog_with_para4 =  "python   " +  PROG_LIST[3]  \
        +   "   --GXXXX=%s"%GXXXX  \
            +  "   --PXXXX=%s"%PXXXX  \
                +  "   --OXXXX=%s"%OXXXX   \
                    + "  --remote_wkdir=%s"%PARAS_DIC['REMOTE_WKDIR']   \
                        + "   --num_serviers=%d"% int( PARAS_DIC['NUM_SERVIERS'] )  \
                        + "      1>>    "    +   SALAM_LOG
                    
    os.system( call_prog_with_para4 )
    #------- end run PG004  PG004__bat_qsub_jobs_opt.py------------------------------------------------------------------    


def run_PG005(call_manner=1):
    #------- run PG005 with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[4],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[4]  +   "  '      1>>    "    +   SALAM_LOG
    retcode = os.system( call_echo_run_prog_to_salam_log )
    print("retcode = ", retcode)
    
    call_prog_with_para5 =  "python   " +  PROG_LIST[4]  \
                            +   "   --GXXXX=%s"%GXXXX  \
                                +  "   --PXXXX=%s"%PXXXX  \
                                    +  "   --OXXXX=%s"%OXXXX   \
                                        + "  --remote_wkdir=%s"%PARAS_DIC['REMOTE_WKDIR']   \
                                            + "   --num_serviers=%d"% int( PARAS_DIC['NUM_SERVIERS'] )  \
                                            +  "   --pbs_job_incompleteness_tolerance=%f"% float( PARAS_DIC['PBS_JOB_INCOMPLETENESS_TOLERANCE_OPT'] )  \
                                              + "   --sleep_seconds=%d"% int( PARAS_DIC['OPT_SLEEP_SECONDS'] )  \
                                                  + "      1>>    "    \
                                                      +   SALAM_LOG
    
    if (call_manner == 1): 
        call_cmd_via_subprocess_run(cmd=call_prog_with_para5,
                                    loop_time_limit=10000,
                                    sleep_seconds=SLEEP_SECONDS
                                    )              
    elif (call_manner == 2):
        retcode =  os.system( call_prog_with_para5 )
        print("retcode = ", retcode)
        
    else:
        print("call_manner must be 1 or 2. 1 for subprocess.run, 2 for os.system")
        
    #------- end run PG005 PG005__optimization_analysis_completeness.py------------------------------------------------------------------
    

def run_PG006():    
    #------- run PG006 with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[5],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[5]  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
    
    call_prog_with_para6 =  "python   " +  PROG_LIST[5]  \
        +   "   --GXXXX=%s"%GXXXX  \
            +  "   --PXXXX=%s"%PXXXX  \
                +  "   --OXXXX=%s"%OXXXX   \
                    +  "   --calc_prop=%s"%PARAS_DIC['CALC_PROP']    \
                        + "   --prop_calc_method=%s"%PARAS_DIC['PROP_CALC_METHOD']  \
                            + "  --remote_wkdir=%s"%PARAS_DIC['REMOTE_WKDIR']   \
                                + "   --num_serviers=%d"% int( PARAS_DIC['NUM_SERVIERS'] )  \
                                + "      1>>    "    +   SALAM_LOG
                        
    os.system( call_prog_with_para6 )
    #------- end run PG006 PG006__bat_g09log_to_propcom.py------------------------------------------------------------------
    

def run_PG007():
    #------- run PG007 with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[6],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[6]  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
    
    call_prog_with_para7 =  "python   " +  PROG_LIST[6]  \
        +   "   --GXXXX=%s"%GXXXX  \
            +  "   --PXXXX=%s"%PXXXX  \
                +  "   --OXXXX=%s"%OXXXX   \
                    + "  --remote_wkdir=%s"%PARAS_DIC['REMOTE_WKDIR']   \
                        + "   --num_serviers=%d"% int( PARAS_DIC['NUM_SERVIERS'] )  \
                        + "      1>>    "    +   SALAM_LOG
                    
    os.system( call_prog_with_para7 )
    #------- end run PG007 PG007__bat_qsub_jobs_prop.py------------------------------------------------------------------
    

def run_PG008(call_manner=1):
    #------- run PG008 with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[7],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[7]  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
    
    call_prog_with_para8 =  "python   " +  PROG_LIST[7]  \
        +  "   --GXXXX=%s"%GXXXX  \
            +  "   --PXXXX=%s"%PXXXX  \
                +  "   --OXXXX=%s"%OXXXX   \
                    +  "   --pbs_job_incompleteness_tolerance=%f"% float( PARAS_DIC['PBS_JOB_INCOMPLETENESS_TOLERANCE_PROP'] ) \
                        +  "   --sleep_seconds=%d"% int( PARAS_DIC['PROP_SLEEP_SECONDS'] ) \
                            + "  --remote_wkdir=%s"%PARAS_DIC['REMOTE_WKDIR']   \
                                + "   --num_serviers=%d"% int( PARAS_DIC['NUM_SERVIERS'] )  \
                                + "      1>>    "    +   SALAM_LOG
                                
    if (call_manner == 1): 
        call_cmd_via_subprocess_run(cmd=call_prog_with_para8,
                                    loop_time_limit=100000,
                                    sleep_seconds=SLEEP_SECONDS
                                    )              
    elif (call_manner == 2):
        os.system( call_prog_with_para8 )
    else:
        print("call_manner must be 1 or 2. 1 for subprocess.run, 2 for os.system")
    #------- end run PG008  PG008__property_analysis_completeness.py------------------------------------------------------------------   


def run_PG009(call_manner=1):
    #------- run PG009 with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[8],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[8]  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
    
    call_prog_with_para9 =  "python   " +  PROG_LIST[8]  \
        +  "   --GXXXX=%s"%GXXXX  \
            +  "   --PXXXX=%s"%PXXXX  \
                +  "   --OXXXX=%s"%OXXXX   \
                    + "   --analyzed_property=%s"%PARAS_DIC['ANALYZED_PROPERTY']  \
                        +  "   --pbs_job_incompleteness_tolerance=%f"% float( PARAS_DIC['PBS_JOB_INCOMPLETENESS_TOLERANCE_PROP'] ) \
                            +  "   --sleep_seconds=%d"%SLEEP_SECONDS  \
                                + "      1>>    "    +   SALAM_LOG
                                
    if (call_manner == 1): 
        call_cmd_via_subprocess_run(cmd=call_prog_with_para9,
                                    loop_time_limit=100000,
                                    sleep_seconds=SLEEP_SECONDS
                                    )              
    elif (call_manner == 2):
        os.system( call_prog_with_para9 )
    else:
        print("call_manner must be 1 or 2. 1 for subprocess.run, 2 for os.system")
    #------- end run PG009  PG009__property_analysis_summary.py------------------------------------------------------------------



def run_PG010(call_manner=1):
    #------- run PG010 with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[9],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[9]  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
    
    call_prog_with_para10 =  "python   " +  PROG_LIST[9]  \
        +   "   --GXXXX=%s"%GXXXX  \
            +  "   --PXXXX=%s"%PXXXX  \
                +  "   --OXXXX=%s"%OXXXX   \
                    + "   --analyzed_property=%s"%PARAS_DIC['ANALYZED_PROPERTY']  \
                        + "      1>>    "    +   SALAM_LOG
                    
    if (call_manner == 1): 
        call_cmd_via_subprocess_run(cmd=call_prog_with_para10,
                                    loop_time_limit=10000,
                                    sleep_seconds=SLEEP_SECONDS
                                    )              
    elif (call_manner == 2):
        os.system( call_prog_with_para10 )
    else:
        print("call_manner must be 1 or 2. 1 for subprocess.run, 2 for os.system")
    #------- end run PG010  PG010__featurizers_train_evaluate.py------------------------------------------------------------------ 
    

def run_PG011(call_manner=1):    
    #------- run PG011 with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[10],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[10]  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
    
    call_prog_with_para11 =  "python   " +  PROG_LIST[10]  \
        +   "   --GXXXX=%s"%GXXXX  \
            +  "   --PXXXX=%s"%PXXXX  \
                +  "   --OXXXX=%s"%OXXXX   \
                    +  "   --prop_tendency=%s"%PARAS_DIC['PROP_TENDENCY']  \
                        + "      1>>    "    +   SALAM_LOG
                    
    if (call_manner == 1): 
        call_cmd_via_subprocess_run(cmd=call_prog_with_para11,
                                    loop_time_limit=10000,
                                    sleep_seconds=SLEEP_SECONDS
                                    )              
    elif (call_manner == 2):
        os.system( call_prog_with_para11 )
    else:
        print("call_manner must be 1 or 2. 1 for subprocess.run, 2 for os.system")
    #------- end run PG011  PG011__predict_opt_molecules.py------------------------------------------------------------------
    

def run_PG012(call_manner=1):
    #------- run PG012 with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[11],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[11]  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )

    call_prog_with_para12 =  "python   " +  PROG_LIST[11]  \
        +   "   --GXXXX=%s"%GXXXX  \
            +  "   --PXXXX=%s"%PXXXX  \
                +  "   --OXXXX=%s"%OXXXX   \
                    +  "   --GXXXXPLUSONE=%s"%GXXXXPLUSONE  \
                        + "   --carbon_sub=%s"%PARAS_DIC['CARBON_SUB']   \
                            + TERMINO_HYDROGEN_SUBS_CMD_PARA \
                                + MUTATION_CONTROL_CMD_PARA \
                                    + "  --is_substi_carbon=%d  "% int( PARAS_DIC['IS_SUBSTI_CARBON'] )   \
                                        + "  --is_substi_hydrogen=%d  "% int( PARAS_DIC['IS_SUBSTI_HYDROGEN'] )   \
                                            + "  --parent_optmols_size=%d   "% int( PARAS_DIC['PARENT_OPTMOLS_SIZE'] )  \
                                                + "      1>>    "    +   SALAM_LOG
                            
                            
    if (call_manner == 1): 
        call_cmd_via_subprocess_run(cmd=call_prog_with_para12,
                                    loop_time_limit=10000,
                                    sleep_seconds=SLEEP_SECONDS
                                    )              
    elif (call_manner == 2):
        os.system( call_prog_with_para12 )
    else:
        print("call_manner must be 1 or 2. 1 for subprocess.run, 2 for os.system")
    #------- end run PG012 PG012__Generate_Gnew.py------------------------------------------------------------------


def run_PG012a(call_manner=1):
    #------- run PG012a with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[12],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[12]  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )

    call_prog_with_para12a =  "python   " +  PROG_LIST[12]  \
        +   "   --GXXXX=%s"%GXXXX  \
            +  "   --PXXXX=%s"%PXXXX  \
                +  "   --OXXXX=%s"%OXXXX   \
                    +  "   --GXXXXPLUSONE=%s"%GXXXXPLUSONE \
                        + "  --N_PATT='%s' "%(PARAS_DIC['N_PATT'])  \
                            + "  --CR_PATT='%s' "%(PARAS_DIC['CR_PATT'])  \
                                + "      1>>    "    +   SALAM_LOG
                        # +  "--N_PATT=%s"%N_PATT \
                        #     +  "--CR_PATT=%s"%CR_PATT \
                            
                            
    if (call_manner == 1): 
        call_cmd_via_subprocess_run(cmd=call_prog_with_para12a,
                                    loop_time_limit=10000,
                                    sleep_seconds=SLEEP_SECONDS
                                    )              
    elif (call_manner == 2):
        os.system( call_prog_with_para12a )
    else:
        print("call_manner must be 1 or 2. 1 for subprocess.run, 2 for os.system")
    #------- end run PG012a  PG012a__Generate_Gnew_Debranch.py------------------------------------------------------------------



def run_PG013(call_manner=1):
    #------- run PG013 with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[12],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[12]  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
    
    call_prog_with_para13 =  "python   " +  PROG_LIST[12]  \
        +   "   --GXXXX=%s"%GXXXX  \
            +  "   --PXXXX=%s"%PXXXX  \
                +  "   --OXXXX=%s"%OXXXX   \
                    +  "   --num_high_freqs=%d   "% int(PARAS_DIC['NUM_HIGH_FREQS'])   \
                        + "      1>>    "    +   SALAM_LOG
                    
    if (call_manner == 1): 
        call_cmd_via_subprocess_run(cmd=call_prog_with_para13,
                                    loop_time_limit=10000,
                                    sleep_seconds=SLEEP_SECONDS
                                    )              
    elif (call_manner == 2):
        os.system( call_prog_with_para13 )
    else:
        print("call_manner must be 1 or 2. 1 for subprocess.run, 2 for os.system")
    #------- end run PG013  PG013__MurckoScaffold.py------------------------------------------------------------------ 
    


def run_PG014(call_manner=1):
    #------- run PG014 with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[13],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[13]  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
    
    call_prog_with_para14 =  "python   " +  PROG_LIST[13]  \
        +   "   --GXXXX=%s"%GXXXX  \
            +  "   --PXXXX=%s"%PXXXX  \
                +  "   --OXXXX=%s"%OXXXX   \
                    +  "   --energy_tendency=%s  "%  PARAS_DIC['ENERGY_TENDENCY']   \
                        +  "   --energy_threshold1=%f   "% float(PARAS_DIC['ENERGY_THRESHOLD1'])   \
                            +  "   --energy_threshold2=%f   "% float(PARAS_DIC['ENERGY_THRESHOLD2'])   \
                                +  "   --stokes_shift=%f   "% float(PARAS_DIC['STOKES_SHIFT'])   \
                                    + "      1>>    "    +   SALAM_LOG
                    
    if (call_manner == 1): 
        call_cmd_via_subprocess_run(cmd=call_prog_with_para14,
                                    loop_time_limit=10000,
                                    sleep_seconds=SLEEP_SECONDS
                                    )              
    elif (call_manner == 2):
        os.system( call_prog_with_para14 )
    else:
        print("call_manner must be 1 or 2. 1 for subprocess.run, 2 for os.system")
    #------- end run PG014  PG014__Energy_Sieve.py------------------------------------------------------------------ 


def run_PG015(call_manner=1):
    #------- run PG015 with paras -----------------------------------------------------------
    print("### Run  %s   1>    %s \n"%(PROG_LIST[14],  SALAM_LOG) )
    
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   PROG_LIST[14]  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
    
    call_prog_with_para15 =  "python   " +  PROG_LIST[14]  \
                            +   "   --GXXXX=%s"%GXXXX  \
                                + "      1>>    "    +   SALAM_LOG
                    
    if (call_manner == 1): 
        call_cmd_via_subprocess_run(cmd=call_prog_with_para15,
                                    loop_time_limit=10000,
                                    sleep_seconds=SLEEP_SECONDS
                                    )              
    elif (call_manner == 2):
        os.system( call_prog_with_para15 )
    else:
        print("call_manner must be 1 or 2. 1 for subprocess.run, 2 for os.system")
    #------- end run PG015  PG015__Map-mols-by-FPSimilarity.py------------------------------------------------------------------ 



def run_evaluate_abundance(call_manner=1):
        print("### Run  run_evaluate_abundance   1>>    %s \n" %SALAM_LOG )
        call_echo_run_prog_to_salam_log = "echo  '### run "  +   "run_evaluate_abundance"  +   "  '      1>>    "    +   SALAM_LOG
        os.system( call_echo_run_prog_to_salam_log )
        
        GXXXX_df_ECFP_csv_path = './project/'  +  GXXXX    +  '/'  + GXXXX   +  '_df_ECFP.csv'

        call_prog_with_para_eva_abu = 'test -s  '   +   GXXXX_df_ECFP_csv_path  +  '   ' 
        
        #print("\nTest if file %s exist?\n" % GXXXX_df_ECFP_csv_path)
        print("\nTest if file %s exist and not empty?\n" % GXXXX_df_ECFP_csv_path)
        if (call_manner == 1): 
            call_cmd_via_subprocess_run(cmd=call_prog_with_para_eva_abu,
                                        loop_time_limit=1000,
                                        sleep_seconds=SLEEP_SECONDS
                                        ) 
        elif (call_manner == 2):
            os.system( call_prog_with_para_eva_abu )
        else:
            print("call_manner must be 1 or 2. 1 for subprocess.run, 2 for os.system")
        
        abundance = percentage_lt_criticval(filename=GXXXX_df_ECFP_csv_path, 
                                            critical_value=0.15
                                            )
        
        abundances.append(abundance)
        
        with open(SALAM_LOG, 'a+') as salam_log:
            print("\nGeneration = %4d , abundance = %10.4f\n" %(MUTATION_GENERATION, abundance) )
            salam_log.write("\n Generation = %4d , abundance = %10.4f\n" %(MUTATION_GENERATION, abundance) )
            
            if (len(abundances) >= 2):
                print("The varation on abundances is: %10.4f\n"%(abundances[-1]  -  abundances[-2] ) )
                salam_log.write("The varation on abundances is: %10.4f\n"%(abundances[-1]  -  abundances[-2] ) )
            else:
                print('')
            
            salam_log.write("\n### End of run_evaluate_abundance.\n")
            

def run_accumulate_optmols( ):
    print("### Run  run_accumulate_optmols   1>>    %s \n" %SALAM_LOG )
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   "run_accumulate_optmols"  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
        
    num_acc_optmol = accumulate_optmols(mutation_generation=MUTATION_GENERATION, 
                                        old_acc_optmols_smi_path='./project/G%04d/acc_optmols.smi'%( MUTATION_GENERATION -1 ),
                                        new_mols_path='./project/G%04d/G%04d_df_ECFP.csv'%( MUTATION_GENERATION , MUTATION_GENERATION ),
                                        acc_optmols_smi_path='./project/G%04d/acc_optmols.smi'%( MUTATION_GENERATION ), 
                                        column_names=[ 'smiles', 'prop_preds' ], 
                                        critical_value=0.15,
                                        is_write_sdf=False, 
                                        outdir_path = './project/G%04d/acc_optmols/'%( MUTATION_GENERATION )
                                        )
    
    num_acc_optmols.append(num_acc_optmol)

    with open(SALAM_LOG, 'a+') as salam_log:
        print("\nGeneration = %4d , num_acc_optmol = %10d\n" %(MUTATION_GENERATION, num_acc_optmol) )
        salam_log.write("\n Generation = %4d , num_acc_optmol = %10d\n" %(MUTATION_GENERATION, num_acc_optmol) )
        
        if (len(num_acc_optmols) >= 2):
            print("The varation on num_acc_optmol is: %10d\n"%(num_acc_optmols[-1]  -  num_acc_optmols[-2] ) )
            salam_log.write("The varation on num_acc_optmol is: %10d\n"%(num_acc_optmols[-1]  -  num_acc_optmols[-2] ) )
        else:
            print('')
        
        salam_log.write("\n### End of run_accumulate_optmols.\n")    



def run_sort_mols_by_SAScores():
    #----- call sort_mols_by_SAScores ---------------------------------------------
    print("### Run  sort_mols_by_SAScores   1>>    %s \n" %SALAM_LOG )
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   "sort_mols_by_SAScores"  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
    
    print("MUTATION_GENERATION_LIMIT = ", int( PARAS_DIC['MUTATION_GENERATION_LIMIT'] ) )
    print("After minus 1, the current value of MUTATION_GENERATION = ", MUTATION_GENERATION )

    # os.path.exists, os.path.isfile
    if os.path.isfile('./project/G%04d/acc_optmols.smi'%(MUTATION_GENERATION) ):
        sort_mols_by_SAScores(mutation_generation= (MUTATION_GENERATION),
                              acc_optmols_smi_path='./project/G%04d/acc_optmols.smi'%(MUTATION_GENERATION), 
                              column_names=[ 'mols', 'smiles' ], 
                              outdir_path='./project/G%04d/acc_optmols_sortedbysas/'%(MUTATION_GENERATION),
                              is_write_sdf=True, 
                              new_sdf_path='./project/G%04d/acc_optmols_sortedbysas.sdf'%(MUTATION_GENERATION),
                              ascending=True
                              )
    else:
        print("\n!!! required acc_optmols.smi does not exist. Skip transformation.\n")
    
    print("### End of sort_mols_by_SAScores   1>>    %s \n" %SALAM_LOG )
    call_echo_run_prog_to_salam_log = "echo  '### End of "  +   "sort_mols_by_SAScores"  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )



def run_accumulate_optmols_S1En( ):
    print("### Run  run_accumulate_optmols_S1En   1>>    %s \n" %SALAM_LOG )
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   "run_accumulate_optmols_S1En"  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )

    num_acc_optmol_S1En_R, num_acc_optmol_S1En_G, num_acc_optmol_S1En_B = accumulate_optmols_S1En(mutation_generation=MUTATION_GENERATION, 
                                                                        old_acc_optmols_smi_paths=[ './project/G%04d/acc_optmols--S1En-%s.smi'%( MUTATION_GENERATION -1, color ) for color in ["R", "G", "B"] ],
                                                                        new_mols_path='./project/G%04d/G%04d_df_ECFP--S1En.csv'%( MUTATION_GENERATION, MUTATION_GENERATION),
                                                                        acc_optmols_smi_paths=[ './project/G%04d/acc_optmols--S1En-%s.smi'%( MUTATION_GENERATION, color ) for color in ["R", "G", "B"] ],
                                                                        column_names=[ 'compoundnames', 'smiles', 'prop_preds' ], 
                                                                        critical_values=[ float(PARAS_DIC['ENERGY_THRESHOLD1']) + float(PARAS_DIC['STOKES_SHIFT']),
                                                                                         float(PARAS_DIC['ENERGY_THRESHOLD2']) + float(PARAS_DIC['STOKES_SHIFT']) ],
                                                                        )

    num_acc_optmol_S1En_RGB = [num_acc_optmol_S1En_R, num_acc_optmol_S1En_G, num_acc_optmol_S1En_B]
    
    num_acc_optmols_S1En.append(num_acc_optmol_S1En_RGB)

    with open(SALAM_LOG, 'a+') as salam_log:
        print("\nGeneration = %4d , num_acc_optmol_S1En_RGB = "%(MUTATION_GENERATION), num_acc_optmol_S1En_RGB )
        salam_log.write("\n Generation = %4d , num_acc_optmol_S1En_RGB = %5d %5d %5d" \
                        %(MUTATION_GENERATION, num_acc_optmol_S1En_R, num_acc_optmol_S1En_G, num_acc_optmol_S1En_B) ) 
        
        if (len(num_acc_optmols_S1En) >= 2):
            print("\nThe varation on num_acc_optmol_S1En_R is: %10d\n"%(num_acc_optmols_S1En[-1][0]  -  num_acc_optmols_S1En[-2][0] ) )
            print("\nThe varation on num_acc_optmol_S1En_G is: %10d\n"%(num_acc_optmols_S1En[-1][1]  -  num_acc_optmols_S1En[-2][1] ) )
            print("\nThe varation on num_acc_optmol_S1En_B is: %10d\n"%(num_acc_optmols_S1En[-1][2]  -  num_acc_optmols_S1En[-2][2] ) )
            salam_log.write("\nThe varation on num_acc_optmol_S1En is: %10d\n"%(num_acc_optmols_S1En[-1][0]  -  num_acc_optmols_S1En[-2][0] ) )
            salam_log.write("\nThe varation on num_acc_optmol_S1En is: %10d\n"%(num_acc_optmols_S1En[-1][1]  -  num_acc_optmols_S1En[-2][1] ) )
            salam_log.write("\nThe varation on num_acc_optmol_S1En is: %10d\n"%(num_acc_optmols_S1En[-1][2]  -  num_acc_optmols_S1En[-2][2] ) )
        else:
            print('')
        
        salam_log.write("\n### End of run_accumulate_optmols_S1En.\n")  



def run_accumulate_optmols_intersection( ):
    print("### Run  run_accumulate_optmols_intersection   1>>    %s \n" %SALAM_LOG )
    call_echo_run_prog_to_salam_log = "echo  '### run "  +   "run_accumulate_optmols_intersection"  +   "  '      1>>    "    +   SALAM_LOG
    os.system( call_echo_run_prog_to_salam_log )
        
    num_acc_optmol_INTERSECTION = accumulate_optmols_intersection(mutation_generation=MUTATION_GENERATION, 
                                                                    acc_optmols_smi_path1='./project/G%04d/acc_optmols.smi'%( MUTATION_GENERATION ),
                                                                    acc_optmols_smi_path2='./project/G%04d/acc_optmols--S1En-B.smi'%( MUTATION_GENERATION ),
                                                                    acc_optmols_smi_path3='./project/G%04d/acc_optmols--INTERSCTION-B.smi'%( MUTATION_GENERATION ), 
                                                                    is_write_sdf=False, 
                                                                    outdir_path='./project/G%04d/acc_optmols--INTERSCTION/'%( MUTATION_GENERATION )
                                                                    )
    
    num_acc_optmols_INTERSECTIONs.append(num_acc_optmol_INTERSECTION)

    with open(SALAM_LOG, 'a+') as salam_log:
        print("\nGeneration = %4d , num_acc_optmol_INTERSECTION = %10d\n" %(MUTATION_GENERATION, num_acc_optmol_INTERSECTION ) )
        salam_log.write("\n Generation = %4d , num_acc_optmol_INTERSECTION = %10d\n" %(MUTATION_GENERATION, num_acc_optmol_INTERSECTION ) )
        
        if (len(num_acc_optmols_S1En) >= 2):
            print("The varation on num_acc_optmol_S1En is: %10d\n"%(num_acc_optmols_INTERSECTIONs[-1]  -  num_acc_optmols_INTERSECTIONs[-2] ) )
            salam_log.write("The varation on num_acc_optmols_INTERSECTIONs is: %10d\n"%(num_acc_optmols_INTERSECTIONs[-1]  -  num_acc_optmols_INTERSECTIONs[-2]) )
        else:
            print('')
        
        salam_log.write("\n### End of run_accumulate_optmols_intersection.\n")  



#------------------------------------------------------------------------------
#------- main begin here ------------------------------------------------------
#------------------------------------------------------------------------------

start_t0 = datetime.datetime.now()

print("\n### Begin of program: SALAM.\n" )

call_echo_begin_program_salam_to_salam_log = "echo -e  '### Begin of program: SALAM.\n'      1>    "    +   SALAM_LOG
retcode = os.system( call_echo_begin_program_salam_to_salam_log )
print("retcode = ", retcode)

abundances = []
num_replaceable_aromaticCHs = []
num_acc_optmols = []
num_acc_optmols_S1En = []
num_acc_optmols_INTERSECTIONs = []


#-------loop over PG002 ~ PG011 ---------------------------------------------------------
print("### loop over PG002 ~ PG015. ")
print("Initial MUTATION_GENERATION = %4d\n"% int( PARAS_DIC['MUTATION_GENERATION'] ) )
print("MUTATION_GENERATION_LIMIT = %4d\n"% int(  PARAS_DIC['MUTATION_GENERATION_LIMIT'] ) )

MUTATION_GENERATION = int( PARAS_DIC['MUTATION_GENERATION'] )

while ( MUTATION_GENERATION  < int( PARAS_DIC['MUTATION_GENERATION_LIMIT'] )):
    print("### --------------------- MUTATION_GENERATION = %4d -------------------------\n"%MUTATION_GENERATION )
    retcode = os.system( "echo  '### --------------------- MUTATION_GENERATION =  %4d"%MUTATION_GENERATION  +  "   '      1>>    "    +   SALAM_LOG )
    print("retcode = ", retcode)
    
    GXXXX = 'G%04d'%MUTATION_GENERATION
    PXXXX = 'P%04d'%MUTATION_GENERATION
    OXXXX = 'O%04d'%MUTATION_GENERATION
    GXXXXPLUSONE = 'G%04d'%(MUTATION_GENERATION +1)

    # GXXXX_sdf_path = './project/'  +  GXXXX    +  '/'  + GXXXX   +  '.sdf'
    # all_frags = get_allfrags_via_bricsdecompose(filename=GXXXX_sdf_path)
    # # for frag in all_frags:
    # #     print( frag )

    GXXXX_sdf_path = './project/'  +  GXXXX    +  '/'  + GXXXX   +  '.sdf' 
    num_replaceable_aromaticCH = get_num_replaceable_aromatic_CHs(filename=GXXXX_sdf_path,
                                                                 patt_str='c[H]'
                                                                 )
    num_replaceable_aromaticCHs.append( num_replaceable_aromaticCH )


    if (MUTATION_GENERATION < RESTART_GENERATION):
        print("\nSkip all PGs, since MUTATION_GENERATION < RESTART_GENERATION.\n")
        
        # run_PG002()                                      #  './PG002__MaxMinPicker.py'
        # run_PG003()                                      #  './PG003__bat_sdf_to_com_gs.py'
        # run_PG004()                                      #  './PG004__bat_qsub_jobs_opt.py'
        
        #time.sleep( SLEEP_SECONDS )                      #  sleep before opt_analysis 
        # run_PG005(call_manner=1)                         #  './PG005__optimization_analysis.py'
        # run_PG006()                                      #  './PG006__bat_g09log_to_tadfcom.py'
        # run_PG007()                                      #  './PG007__bat_qsub_jobs_tadf.py'
        
        # time.sleep( SLEEP_SECONDS )                      #  sleep before prop_analysis 
        
        # run_PG008(call_manner=1)                        #  './PG008__property_analysis_completeness.py'
        # run_PG09(call_manner=2)                        #  './PG009__property_analysis_summary.py'
        # run_PG010(call_manner=2)                         #  './PG010__featurizers_train_evaluate.py'
        
        # run_PG011(call_manner=2)                         #  './PG011__predict_opt_molecules.py'
        # time.sleep( SLEEP_SECONDS )         

        # run_PG012(call_manner=2)                         #  './PG012__Generate_Gnew.py'
        # time.sleep( SLEEP_SECONDS )                      #  sleep before evaluate_abundance
        
        # run_PG013(call_manner=2)                         #   './PG013__MurckoScaffold.py'
        # time.sleep( SLEEP_SECONDS ) 
        
        # run_PG014(call_manner=2)                         #  './PG014__Energy_Sieve.py'
        # time.sleep( SLEEP_SECONDS ) 
        
        # run_PG015(call_manner=2)                         #  './PG015__Map-mols-by-FPSimilarity.py'
        # time.sleep( SLEEP_SECONDS )
                              
    elif (MUTATION_GENERATION == RESTART_GENERATION):
        if (RESTART_MAXMINPICKER == True):
            run_PG002()                                      #  './PG002__MaxMinPicker.py'
        else:
            print("(MUTATION_GENERATION == RESTART_GENERATION), & (RESTART_MAXMINPICKER == False), skip run_PG002()")
        
        run_PG003()                                      #  './PG003__bat_sdf_to_com_gs.py'
        
        if (RESTART_OPTJOB == True):
            run_PG004()                                      #  './PG004__bat_qsub_jobs_opt.py'
        else:
            print("(MUTATION_GENERATION == RESTART_GENERATION), & (RESTART_OPTJOB == False), skip run_PG004()")
        
        time.sleep( SLEEP_SECONDS )                      #  sleep before opt_analysis 
        run_PG005(call_manner=1)                         #  './PG005__optimization_analysis.py'

        run_PG006()                                      #  './PG006__bat_g09log_to_tadfcom.py'
        
        if (RESTART_OPTJOB == True) or (RESTART_PROPJOB == True):
            run_PG007()                                      #  './PG007__bat_qsub_jobs_tadf.py'
        else:
            print("(MUTATION_GENERATION == RESTART_GENERATION), & ( (RESTART_OPTJOB == False) & (RESTART_PROPJOB == False) ), skip run_PG007()" )
            
        time.sleep( SLEEP_SECONDS )                      #  sleep before prop_analysis 
        
        run_PG008(call_manner=1)                        #  './PG008__property_analysis_completeness.py'
        run_PG009(call_manner=2)                        #  './PG009__property_analysis_summary.py'
        run_PG010(call_manner=2)                         #  './PG010__featurizers_train_evaluate.py'
        
        run_PG011(call_manner=2)                         #  './PG011__predict_opt_molecules.py'
        time.sleep( SLEEP_SECONDS )                      #  sleep before evaluate_abundance
        
        run_PG012(call_manner=2)                         #  './PG012__Generate_Gnew.py'
        time.sleep( SLEEP_SECONDS )

        run_PG013(call_manner=2)                         #   './PG013__MurckoScaffold.py'
        time.sleep( SLEEP_SECONDS )                    
        
        run_PG014(call_manner=2)                         #  './PG014__Energy_Sieve.py'
        time.sleep( SLEEP_SECONDS ) 

        run_PG015(call_manner=2)                         #  './PG015__Map-mols-by-FPSimilarity.py'
        time.sleep( SLEEP_SECONDS )
    
    else:
        # run_PG002()                                      #  './PG002__MaxMinPicker.py'
        # run_PG003()                                      #  './PG003__bat_sdf_to_com_gs.py'
        # run_PG004()                                      #  './PG004__bat_qsub_jobs_opt.py'
        
        # time.sleep( SLEEP_SECONDS )                      #  sleep before opt_analysis 
        # run_PG005(call_manner=1)                         #  './PG005__optimization_analysis.py'
        # run_PG006()                                      #  './PG006__bat_g09log_to_tadfcom.py'
        # run_PG007()                                      #  './PG007__bat_qsub_jobs_tadf.py'
        
        # time.sleep( SLEEP_SECONDS )                      #  sleep before prop_analysis 
        
        # run_PG008(call_manner=1)                        #  './PG008__property_analysis_completeness.py'
        # run_PG009(call_manner=2)                        #  './PG009__property_analysis_summary.py'
        # run_PG010(call_manner=2)                         #  './PG010__featurizers_train_evaluate.py'
        
        # run_PG011(call_manner=2)                         #  './PG011__predict_opt_molecules.py'
    
        # time.sleep( SLEEP_SECONDS )                      #  sleep before evaluate_abundance
        
        # run_PG012(call_manner=2)                         #  './PG012__Generate_Gnew.py'        
        # time.sleep( SLEEP_SECONDS )                   
        
        # run_PG013(call_manner=2)                         #   './PG013__MurckoScaffold.py'
        # time.sleep( SLEEP_SECONDS ) 
        
        # run_PG014(call_manner=2)                         #  './PG014__Energy_Sieve.py'
        # time.sleep( SLEEP_SECONDS ) 
        
        run_PG015(call_manner=2)                         #  './PG015__Map-mols-by-FPSimilarity.py'
        time.sleep( SLEEP_SECONDS )
    
    
    # run_evaluate_abundance(call_manner=2)            #  by call method: percentage_lt_criticval() in Metrics module
    # if (len(abundances) > 0) and ( abs( abundances[-1] - float(PARAS_DIC['ABUNANCE_LIMIT']) ) < 0.01):
    #     print("\nThe abundance has converged to ABUNANCE_LIMIT.\n")
    #     os.system("echo  '\nThe abundance has converged to ABUNANCE_LIMIT.\n'      1>>    "    +   SALAM_LOG)
    #     break
    # time.sleep( SLEEP_SECONDS )         
    
    # run_accumulate_optmols()
    # if ( (len(num_acc_optmols) > 0) and (num_acc_optmols[-1]  >= int(PARAS_DIC['NUM_ACC_OPTMOLS_LIMIT'])) ):
    #     print("\nThe num_acc_optmol has converged to NUM_ACC_OPTMOLS_LIMIT.\n")
    #     os.system("echo  '\nThe num_acc_optmol has converged to NUM_ACC_OPTMOLS_LIMIT.\n'      1>>    "    +   SALAM_LOG)
    #     break    
    # time.sleep( SLEEP_SECONDS )
    
    # run_accumulate_optmols_S1En( )
    # time.sleep( SLEEP_SECONDS )        

    MUTATION_GENERATION += 1
        


#------------------------------------------------------------------------------
MUTATION_GENERATION -= 1

# #----- call sort_mols_by_SAScores ---------------------------------------------
# run_sort_mols_by_SAScores()

# #------ call accumulate_optmols_intersection -----------------------------------
# run_accumulate_optmols_intersection( )


#-----------------------------------------------------------------------------


if len(num_replaceable_aromaticCHs) > 0:
    print("-"*60)
    print("\nnum_replaceable_aromaticCHs:")
    for i, num_replaceable_aromaticCH in zip( range(len(num_replaceable_aromaticCHs)),  num_replaceable_aromaticCHs):
        print("%8d %10.4f"%(i, num_replaceable_aromaticCH))
else:
    print("\nlen(num_replaceable_aromaticCHs) > 0 is False.")


if (len(abundances) > 0):
    print("-"*60)
    print("muation_generation, abundance are:")
    for i, abundance in zip( range(len(abundances)),  abundances):
        print("%8d %10.4f"%(i, abundance))
else:
    print("\nlen(abundances) > 0 is False.")


if (len(num_acc_optmols) > 0):
    print("-"*60)
    print("muation_generation, num_acc_optmols are:")
    for i, num_acc_optmol in zip( range(len(num_acc_optmols)),  num_acc_optmols):
        print("%8d %10d"%(i, num_acc_optmol))
else:
    print("\nlen(num_acc_optmols) > 0 is False.")


if (len(num_acc_optmols_S1En) > 0):
    print("-"*60)
    print("muation_generation, num_acc_optmols_S1En_R num_acc_optmols_S1En_G num_acc_optmols_S1En_B  are:")
    for i, num_acc_optmol_S1En in zip( range(len(num_acc_optmols_S1En)),  num_acc_optmols_S1En):
        print("%8d %8d %8d %8d"%(i, num_acc_optmol_S1En[0], num_acc_optmol_S1En[1], num_acc_optmol_S1En[2]))
else:
    print("\nlen(num_acc_optmols_S1En) > 0 is False.")


# #---- plot generation Vs abundance, aromaticCHs, num_acc_optmols pictures ----------------
# df_generation_abundance_aromaticCHs_numaccoptmols = pd.DataFrame(data=zip( range(len(abundances)),  abundances, num_replaceable_aromaticCHs, num_acc_optmols), 
#                                                                   columns=["generation", "abundance", "aromaticCH", "num_acc_optmols"]
#                                                                   )

# fig, ax = plt.subplots(1, 1, figsize=(12, 8), sharey=False)
# df_generation_abundance_aromaticCHs_numaccoptmols.plot(
#                                                         title='abundance vs generation',
#                                                         #kind='scatter', 
#                                                         kind='line', linestyle='-',
#                                                         x='generation', 
#                                                         y='abundance', 
#                                                         color='g', 
#                                                         alpha=0.95, 
#                                                         ax=ax,
#                                                         xlabel='generation', 
#                                                         ylabel='abundance'
#                                                         )

# ax.legend(ncol=1, fontsize='x-large', shadow=True)
# ax.grid(True)
# fig.show()


# fig1, ax1 = plt.subplots(1, 1, figsize=(12, 8), sharey=False)
# df_generation_abundance_aromaticCHs_numaccoptmols.plot(
#                                                         title='aromaticCH vs generation',
#                                                         #kind='scatter', 
#                                                         kind='line', linestyle='-',
#                                                         x='generation', 
#                                                         y='aromaticCH', 
#                                                         color='r', 
#                                                         alpha=0.95, 
#                                                         ax=ax1, 
#                                                         xlabel='generation',
#                                                         ylabel='aromaticCH'
#                                                         )

# ax1.legend(ncol=1, fontsize='x-large', shadow=True)
# ax1.grid(True)
# fig1.show()

# fig2, ax2 = plt.subplots(1, 1, figsize=(12, 8), sharey=False)
# df_generation_abundance_aromaticCHs_numaccoptmols.plot(
#                                                         title='num_acc_optmols vs generation',
#                                                         #kind='scatter', 
#                                                         kind='line', linestyle='-',
#                                                         x='generation', 
#                                                         y='num_acc_optmols', 
#                                                         color='b', 
#                                                         alpha=0.95, 
#                                                         ax=ax2, 
#                                                         xlabel='generation',
#                                                         ylabel='num_acc_optmols'
#                                                         )

# ax2.legend(ncol=1, fontsize='x-large', shadow=True)
# ax2.grid(True)
# fig2.show()


#----- plot_muation_diagram --------------------------------------------------
plot_muation_diagram(filename='./project/mutation_diagram.csv',
                     figname='./project/muation-diagram.png',
                     molsPerRow=3,
                     subImgSize=(800, 800),
                     num_of_mols=None
                     )



print("\n### End of program: SALAM.\n" )

call_echo_end_program_salam_to_salam_log = "echo -e '\n### END of program: SALAM.\n'      1>>    "    +   SALAM_LOG
retcode = os.system( call_echo_end_program_salam_to_salam_log )
print("retcode = ", retcode)


end_t0 = datetime.datetime.now()
elapsed_sec0 = (end_t0 - start_t0).total_seconds()
print("\nTotal running time of SALAM is : " + "{:.2f}".format(elapsed_sec0/60.) + " min ")

retcode = os.system( "echo  '\nTotal running time of SALAM is :  " +  "{:.2f}".format(elapsed_sec0/60.) + " min   '  "  +  "     1>>    "    +   SALAM_LOG )
print("retcode = ", retcode)

print("\n### Normal termination of program: SALAM!\n")


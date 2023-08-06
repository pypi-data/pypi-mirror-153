#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 21:50:49 2021

This module is used to specify the metrics used for evaluation of the properties of molecules of library.

@author: tucy
"""

import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import BRICS
from module_MD.OrganoMetalics_Enumeration import find_CH_aromatic_idxs

from module_MD.SA_Score import sascorer
from rdkit.Chem import Draw
from rdkit.Chem import PandasTools
import matplotlib.pyplot as plt

import re

import subprocess
from module_MD.D_Pi_A_Enumeration import write_mols_paralell

from rdkit import DataStructs
import matplotlib.image as mpimg # mpimg 用于读取图片


#-----------------------------------------------------------------------------

def convert_str_to_list(str1="[ '*F',  '*C#N',  '*OC',  '*N(C)C'  ]"):
    # convert a str, "[ '*F',  '*C#N',  '*OC',  '*N(C)C'  ]"  to a list, ['*F', '*C#N', '*OC', '*N(C)C']
    print( "type(str1) = ", type(str1) )
    print( str1 )
    
    str1_list =  str1.strip().replace('[', '').replace(']', '').split(sep=',')
    
    list1 =  [ x.strip().replace('"', '').replace("'", '')  for x in  str1_list ]
    
    print("len(list1) = ", len(list1))

    print("type(list1) = ", type(list1))
    print(list1)
    
    return list1


def get_paras_dic( filename='./salam_paras.inp' ):
    print("input file path is:")
    print(filename)
    print("# Begin parsing paras.\n")
    paras_dic = {}
    #comment_pattern = re.compile(r'#(.*?)', re.MULTILINE|re.DOTALL)
    comment_pattern = re.compile(r'^#(.*?)')
    blankline_pattern = re.compile(r'^(\s*?)$')
    # line_no = 1
    with open(filename, 'r', encoding='UTF-8') as fr:
        for line in fr:   
            comment_result = comment_pattern.findall(line)
            blankline_result = blankline_pattern.findall(line)
            
            if ((len(comment_result) > 0) or (len(blankline_result) > 0)):
                # print(line_no, " COMMENT LINE FOUND ", line)
                print(line, end='')
            else:
                # print(line_no, "  ", line)
                print(line, end='')
                values = line.strip().split('=')  #通过：分割字符串变成一个列表    
                # print("values: ", values)    
                new_values = [ val.strip() for val in values]
                print(new_values)   
                #paras_dic[values[0]] = values[1]
                paras_dic[new_values[0]] = new_values[1]
            
            # line_no += 1
    
    print('-'*60)
    print("paras_dic.items():")
    print(paras_dic.items() )
    
    print("\n# End of parsing paras.\n")

    return paras_dic


#GXXXX_df_ECFP_csv_path = './project/'  +  GXXXX    +  '/'  + GXXXX   +  '_df_ECFP.csv'

def percentage_lt_criticval(filename='./project/G0000/G0000_df_ECFP.csv', 
                            critical_value=0.15):
    
    df_ECFP = pd.read_csv(filename)
    print("df_ECFP.head():\n")
    print(df_ECFP.head())
    
    df_ECFP['prop_preds_is_lower_than_threshold'] = df_ECFP['prop_preds'].apply( lambda x: True if (x <= critical_value) else False )
    
    #df_ECFP_prop_low = df_ECFP.loc[ df_ECFP['prop_preds'] <= critical_value ] 
    
    #total_num = len(df_ECFP['prop_preds'])
    total_num = df_ECFP.shape[0]
    passed_num = df_ECFP['prop_preds_is_lower_than_threshold'].sum()
    
    if ( total_num >= 1):
        percentage = passed_num / float( total_num )
    else:
        print("The 1st shape of the dataframe,  df_ECFP.shape[0] must >= 1.\n")
        exit(-1)
    
    return percentage


def percentage_lt_criticval_df(df, 
                               colname='prop_preds',
                               critical_value=0.15):
    
    print("df.head():\n")
    print(df.head())
    
    df[ '%s_is_lower_than_threshold'%colname ] = df[ colname ].apply( lambda x: True if (x <= critical_value) else False )
    
    #total_num = len(df_ECFP['prop_preds'])
    total_num = df.shape[0]
    passed_num = df[ '%s_is_lower_than_threshold'%colname ].sum()
    
    if ( total_num >= 1):
        percentage = passed_num / float( total_num )
    else:
        print("The 1st shape of the dataframe,  df.shape[0] must >= 1.\n")
        exit(-1)
    
    return percentage



def getmaxminidxs_lt_le_gt_ge_criticval_df(df, 
                                           colname='prop_preds',
                                           critical_value=0.15,
                                           ascending=True):
    df_ = df.copy(deep=True)
    print("df_.head():\n")
    print(df_.head())
    
    df_[ '%s_is_lt_tsd'%colname ] = df_[ colname ].apply( lambda x: True if (x < critical_value) else False )
    df_[ '%s_is_le_tsd'%colname ] = df_[ colname ].apply( lambda x: True if (x <= critical_value) else False )
    df_[ '%s_is_gt_tsd'%colname ] = df_[ colname ].apply( lambda x: True if (x > critical_value) else False )
    df_[ '%s_is_ge_tsd'%colname ] = df_[ colname ].apply( lambda x: True if (x >= critical_value) else False )
    
    print("df_.head():\n")
    print(df_.head())
    
    lt_num = df_[ '%s_is_lt_tsd'%colname ].sum()
    le_num = df_[ '%s_is_le_tsd'%colname ].sum()
    gt_num = df_[ '%s_is_gt_tsd'%colname ].sum()
    ge_num = df_[ '%s_is_ge_tsd'%colname ].sum()
    
    
    print("lt_num = %8d, le_num = %8d, gt_num = %8d, ge_num = %8d"%(lt_num, le_num, gt_num, ge_num) )
    if (lt_num * le_num * gt_num * ge_num == 0):
        print("Warning: one of lt_num, le_num, gt_num, ge_num = 0. Use with careness.")
    
    if ( ascending==True ):
        lt_idxmax = lt_num
        le_idxmax = le_num
        gt_idxmin = le_num + 1
        ge_idxmin = lt_num + 1
        print("order is ascending. Return, lt_idxmax, le_idxmax, gt_idxmin, ge_idxmin")
        return lt_idxmax, le_idxmax, gt_idxmin, ge_idxmin
    
    else:
        lt_idxmin = ge_num + 1
        le_idxmin = gt_num + 1
        gt_idxmax = gt_num
        ge_idxmax = ge_num
        print("order is descending. Return, lt_idxmin, le_idxmin, gt_idxmax, ge_idxmax")
        return lt_idxmin, le_idxmin, gt_idxmax, ge_idxmax



def get_allfrags_via_bricsdecompose(filename='./project/G0000/G0000.sdf'):
    #----- generating fragments from dataset of mols by BRICSDecompose -----------
    mols = Chem.SDMolSupplier( filename )
    print("len(mols) = ", len(mols))
    
    allfrags = set()
    for mol in mols:
        pieces = BRICS.BRICSDecompose(mol)
        allfrags.update(pieces)
    
    print("len(allfrags) = ", len(allfrags) )
    
    return list( sorted(allfrags) )


def get_num_replaceable_aromatic_CHs(filename='./project/G0000/G0000.sdf', 
                                     patt_str="c[H]"
                                     ):
    #----- compute number of replaceable aromatic CHs from dataset of mols -----------
    mols = Chem.SDMolSupplier( filename )
    
    print("len(mols) = ", len(mols))
    
    num_replaceable_aromatic_CHs = []
    for mol in mols:
        mol = Chem.AddHs(mol)
        Xatom_label_idxs, H_Xatom_label_idxs = find_CH_aromatic_idxs(mol, 
                                                                     patt=Chem.MolFromSmarts( patt_str ) 
                                                                     )
        #print( "len(Xatom_label_idxs) = ",  len(Xatom_label_idxs) )
        num_replaceable_aromatic_CHs.append( len(Xatom_label_idxs) )
        
    
    print("sum(num_replaceable_aromatic_CHs) = ", sum(num_replaceable_aromatic_CHs) )
    print("len(num_replaceable_aromatic_CHs) = ", len(num_replaceable_aromatic_CHs) )
    
    if len(mols) == 0:
        ave_num_replaceable_aromatic_CHs = 0.
    else:
        ave_num_replaceable_aromatic_CHs = sum( num_replaceable_aromatic_CHs )/float(len(mols))
    
    print("ave_num_replaceable_aromatic_CHs = ", ave_num_replaceable_aromatic_CHs)
    
    return  ave_num_replaceable_aromatic_CHs


def compute_plot_SAScore_vs_generation(filename='./project/G0000/G0000_df_ECFP.csv',
                                        column_names=[ 'compoundnames', 'smiles', 'prop_preds' ], 
                                        figname='./foo--sascores.png',
                                        GXXXX='G0000'
                                        ):
    
    df = pd.read_csv(filename, 
                     usecols=column_names
                     #names=['new_compoundnames', 'new_mols', 'new_smiles', 'new_prop_preds']
                     )

    #df = pd.read_csv('./SA_Score/Compounds_smiles.csv', sep=',')
    
    print( "\ndf.head()" )
    print( df.head() )
    print( "\ndf.describe()" )
    print( df.describe() )
    print( "\ndf.columns" )
    print( df.columns )
    
    #将smiles转换为RDKit 的Mol对象
    
    PandasTools.AddMoleculeColumnToFrame(frame=df, smilesCol='smiles')
    
    print( "\ndf.head()" )
    print( df.head() )
    print( "\ndf.describe()" )
    print( df.describe() )
    print( "\ndf.columns" )
    print( df.columns )
    
    
    df['calc_SA_score'] = df.ROMol.map(sascorer.calculateScore)
    
    # x = df.compoundnames
    # y = df.calc_SA_score
    # #with mpl.style.context('seaborn'):
    # plt.plot(x, y, '-')
    # plt.xlabel('compoundnames')
    # plt.ylabel('calculated SA scores')
    # plt.title('SA scores for compounds')
    
    # (id_max, id_min) = (df.calc_SA_score.idxmax(), df.calc_SA_score.idxmin())
    # sa_mols = [df.ROMol[id_max], df.ROMol[id_min]]
    # Draw.MolsToGridImage(sa_mols, subImgSize=(340,200),
    #                      legends=['SA-score: {:.2f}'.format(df.calc_SA_score[i]) for i in [id_max, id_min]])
    
    print( "\ndf.head()" )
    print( df.head() )
    print( "\ndf.describe()" )
    print( df.describe() )
    print( "\ndf.columns" )
    print( df.columns )
    
    #df['calc_SA_score'].plot( ) 

    fig1, ax1 = plt.subplots(1, 1, figsize=(12, 8), sharey=False)
    
    df['calc_SA_score'].plot(kind='hist',
                             title='distribution of calc_SA_score in %s'%GXXXX,
                             #color='r', 
                             ax=ax1, 
                             ) 
    
    # df_generation_abundance_aromaticCHs.plot(
    #                                         title='aromaticCH vs generation',
    #                                         #kind='scatter', 
    #                                         kind='line', linestyle='-',
    #                                         x='generation', 
    #                                         y='aromaticCH', 
    #                                         color='r', 
    #                                         alpha=0.95, 
    #                                         ax=ax1, 
    #                                         xlabel='generation',
    #                                         ylabel='aromaticCH'
    #                                         )
    
    ax1.legend(ncol=1, fontsize='x-large', shadow=True)
    ax1.grid(True)
    #fig1.show()
    fig1.savefig(figname)

    
    return df['calc_SA_score'].tolist()


def compute_plot_prop_masscenter_vs_generation(filenames=[ './project/%s/%s_df_ECFP.csv'%(GXXXX, GXXXX) for GXXXX in ['G0000', 'G0001', 'G0002', 'G0003', 'G0004', 'G0005'] ],
                                                column_names=[ 'compoundnames', 'prop_preds' ], 
                                                figname='./foo--prop_masscenter.png',
                                                ):
    prop_means = []
    for i in range(len(filenames)):
        df = pd.read_csv(filenames[i], 
                         usecols=column_names
                         #names=['new_compoundnames', 'new_mols', 'new_smiles', 'new_prop_preds']
                         )
        
        prop_mean = df['prop_preds'].mean()
        print( i, prop_mean )
        
        prop_means.append( prop_mean )


    fig1, ax1 = plt.subplots(1, 1, figsize=(12, 8), sharey=False)
    
    plt.plot(range(len(prop_means)),
             prop_means,
             linestyle='-',
             color='r', 
             alpha=0.95, 
             label='prop_masscenter'
            )
    
    plt.legend(ncol=1, fontsize='x-large', shadow=True)
    ax1.grid(True)
    #fig1.show()
    plt.xlabel('generation' )
    plt.ylabel('prop_masscenter')
    plt.title('prop_masscenter vs generation')
    fig1.savefig(figname)

    
    return prop_means



def plot_abundance_anvCHs_vs_generation(filename='./abundance-vs-anvCHs.txt',
                                        sep=',',
                                        figname='./foo--abundance-anvCHs-vs-generation.png'
                                        ):
    df = pd.read_csv(filename, 
                     sep=sep,
                     #usecols=[ 'generation', 'abundance', 'anvCHs' ],
                     #names=[ 'generation', 'abundance', 'anvCHs' ],
                     )
    
    print("df.head()\n", df.head())
    print("df.columns:\n", df.columns)
    
    colnames = df.columns.tolist()
    colnames = colnames[1:]
    
    #print("colnames :\n", colnames)
    
    fig1, axs = plt.subplots(1, int(len(colnames)/2), figsize=(20, 6), sharey=False )
    
    for i in range( int(len(colnames)/2) ):
        df.plot(
                x='generation', 
                y=colnames[2*i], 
                title='%s and %s vs generation'%(colnames[2*i], colnames[2*i+1]),
                #kind='scatter', 
                kind='line', 
                linestyle='-',            #  linestyle=   '-',  '--', '-.', ':' 
                color='r', 
                alpha=0.95, 
                xlabel='generation',
                #ylabel='%s'%colnames[2*i],
                ax=axs[i]
                )
        
        axs[i].set_xlim([-0.5, 10.5])
        axs[i].set_ylim([-0.05, 1.05])
        axs[i].legend(loc='upper left')
        axs[i].grid(True)
        
        
        axs_i_twinx = axs[i].twinx()
        
        df.plot(
                x='generation', 
                y=colnames[2*i+1], 
                #title='%s vs generation'%colnames[2*i+1],
                #kind='scatter', 
                kind='line', 
                linestyle='-',
                color='b', 
                alpha=0.95, 
                #xlabel='generation',
                #ylabel='%s'%colnames[2*i+1],
                #ax=axs[i], 
                ax=axs_i_twinx
                )
        
        axs_i_twinx.set_ylim([0,20])
        axs_i_twinx.legend(loc='upper right')
        
    
    #axs.legend(loc='best')
    #axs.grid(True)
    #fig1.show()
    fig1.savefig(figname)



def compute_anvCHs_derivative_vs_generation(filename='./abundance-vs-anvCHs.txt',
                                            sep=',',
                                            xcolname='generation',
                                            ycolname='anvCHs1',
                                            ):
    df = pd.read_csv(filename, 
                     sep=sep,
                     )
    
    # print("df.head()\n", df.head())
    # print("df.columns:\n", df.columns)
    
    xs = df[xcolname].tolist()
    ys = df[ycolname].tolist()

    ds = []
    ds.append(np.NaN)

    for i in range(len(xs) - 1):    
        d = ( ys[i+1] - ys[i] )/ ( xs[i+1] - xs[i] )
        ds.append(d)

    ds[0] = ds[1]
    
    print("generation, anvCHs, anvCHs_derivative")
    for x, y, d in zip(xs, ys, ds):
        print("%d %10.4f %10.4f" %(x, y, d) )
    
    
    return xs, ys, ds
    
    
def plot_anvCHs_derivative_vs_generation(filename='./abundance-vs-anvCHs.txt',
                                         sep=',',
                                         ycolnames=['anvCHs1', 'anvCHs2', 'anvCHs3'],
                                         figname='./foo--anvCHs-derivative-vs-generation.png'
                                         ):

    xs, ys1, ds1 = compute_anvCHs_derivative_vs_generation(filename='./abundance-vs-anvCHs.txt',
                                                            sep=sep, 
                                                            xcolname='generation',
                                                            ycolname=ycolnames[0],
                                                            )
        
    xs, ys2, ds2 = compute_anvCHs_derivative_vs_generation(filename='./abundance-vs-anvCHs.txt',
                                                            sep=sep, 
                                                            xcolname='generation',
                                                            ycolname=ycolnames[1],
                                                            )

    xs, ys3, ds3 = compute_anvCHs_derivative_vs_generation(filename='./abundance-vs-anvCHs.txt',
                                                            sep=sep, 
                                                            xcolname='generation',
                                                            ycolname=ycolnames[2],
                                                            )

    new_df = pd.DataFrame(data=zip(xs, ds1, ds2, ds3), 
                          columns=(['generation', 'anvCHs1', 'anvCHs2', 'anvCHs3']))
    
    fig1, axs = plt.subplots(1, 3, figsize=(20, 6), sharey=False )
    
    for i, colname in zip( range(3), ['anvCHs1', 'anvCHs2', 'anvCHs3']) :
        new_df.plot(
                x='generation', 
                y=colname, 
                title='anvCHs_derivative vs generation',
                #kind='scatter', 
                kind='line', 
                linestyle='--',            #  linestyle=   '-',  '--', '-.', ':' 
                color='b', 
                alpha=0.95, 
                xlabel='generation',
                #ylabel='%s'%colnames[2*i],
                ax=axs[i]
                )
        
        axs[i].set_xlim([-0.5, 10.5])
        axs[i].set_ylim([-4.5, 0.5])
        axs[i].legend(loc='best')
        axs[i].grid(True)
    
    fig1.savefig(figname)


def compute_abundance_derivative_vs_generation(filename='./abundance-vs-anvCHs.txt',
                                                sep=',',
                                                xcolname='generation',
                                                ycolname='abundance',
                                                ):
    df = pd.read_csv(filename, 
                     sep=sep,
                     )
    
    # print("df.head()\n", df.head())
    # print("df.columns:\n", df.columns)
    
    xs = df[xcolname].tolist()
    ys = df[ycolname].tolist()

    ds = []
    ds.append(np.NaN)

    for i in range(len(xs) - 1):    
        d = ( ys[i+1] - ys[i] )/ ( xs[i+1] - xs[i] )
        ds.append(d)

    ds[0] = ds[1]
    
    print("generation, anvCHs1, anvCHs1_derivative")
    for x, y, d in zip(xs, ys, ds):
        print("%d %10.4f %10.4f" %(x, y, d) )
    
    
    return xs, ys, ds
    
    
def plot_abundance_derivative_vs_generation(filename='./abundance-vs-anvCHs.txt',
                                            sep=',', 
                                            ycolnames=['abundance1', 'abundance2', 'abundance3'],
                                            figname='./foo--abundance-derivative-vs-generation.png'
                                            ):

    xs, ys1, ds1 = compute_anvCHs_derivative_vs_generation(filename='./abundance-vs-anvCHs.txt',
                                                            sep=sep, 
                                                            xcolname='generation',
                                                            ycolname=ycolnames[0],
                                                            )
        
    xs, ys2, ds2 = compute_anvCHs_derivative_vs_generation(filename='./abundance-vs-anvCHs.txt',
                                                            sep=sep, 
                                                            xcolname='generation',
                                                            ycolname=ycolnames[1],
                                                            )

    xs, ys3, ds3 = compute_anvCHs_derivative_vs_generation(filename='./abundance-vs-anvCHs.txt',
                                                            sep=sep, 
                                                            xcolname='generation',
                                                            ycolname=ycolnames[2],
                                                            )

    new_df = pd.DataFrame(data=zip(xs, ds1, ds2, ds3), 
                          columns=(['generation', 'abundance1_deriv', 'abundance2_deriv', 'abundance3_deriv']))
    
    fig1, axs = plt.subplots(1, 3, figsize=(20, 6), sharey=False )
    
    for i, colname in zip( range(3), ['abundance1_deriv', 'abundance2_deriv', 'abundance3_deriv']) :
        new_df.plot(
                x='generation', 
                y=colname, 
                title='abundance_derivative vs generation',
                #kind='scatter', 
                kind='line', 
                linestyle='--',            #  linestyle=   '-',  '--', '-.', ':' 
                color='r', 
                alpha=0.95, 
                xlabel='generation',
                #ylabel='%s'%colnames[2*i],
                ax=axs[i]
                )
        
        axs[i].set_xlim([-0.5, 10.5])
        #axs[i].set_ylim([-4.5, 0.5])
        axs[i].legend(loc='best')
        axs[i].grid(True)
    
    fig1.savefig(figname)


#-----------------------------------------------------------------------------------------------
def accumulate_optmols(mutation_generation=1, 
                       old_acc_optmols_smi_path='./project/G%04d/acc_optmols.smi'%( 0 ),
                       new_mols_path='./project/G%04d/G%04d_df_ECFP.csv'%( 1, 1 ),
                       acc_optmols_smi_path='./project/G%04d/acc_optmols.smi'%( 1 ), 
                       column_names=[ 'smiles', 'prop_preds' ], 
                       critical_value=0.15,
                       is_write_sdf=False, 
                       outdir_path='./project/G%04d/acc_optmols/'%( 1 )
                       ):
    '''
    This function can accumulate the optimal mols by calculating the union of two sets of optmols (items are SMILES), 
    acc_optmols = old_acc_optmols.union( new_mols )
    The resultant acc_optmols smi file is written to acc_optmols.smi, 
    if desired (set is_write_sdf=True), the sdf file is also written to acc_optmols.sdf.
    

    Parameters
    ----------
    mutation_generation : int, optional
        DESCRIPTION. The default is 1. mutation_generation must be >= 0  integer,
                     if mutation_generation = 0, the acc_optmols = new_mols
    old_acc_optmols_smi_path : TYPE, optional
        DESCRIPTION. The default is './project/G%04d/acc_optmols.smi'%( 0 ).
    new_mols_path : TYPE, optional
        DESCRIPTION. The default is './project/G%04d/G%04d_df_ECFP.csv'%( 1, 1 ).
    acc_optmols_smi_path : TYPE, optional
        DESCRIPTION. The default is './project/G%04d/acc_optmols.smi'%( 1 ).
    column_names : TYPE, optional
        DESCRIPTION. The default is [ 'smiles', 'prop_preds' ].
    critical_value : TYPE, optional
        DESCRIPTION. The default is 0.15.
    is_write_sdf : TYPE, optional
        DESCRIPTION. The default is False.
    outdir_path : TYPE, optional
        DESCRIPTION. The default is './project/G%04d/acc_optmols/'%( 1 ).

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''

    df = pd.read_csv(new_mols_path, 
                     usecols=column_names
                     )
    
    print( "\ndf.head()" )
    print( df.head() )
    print( "\ndf.describe()" )
    print( df.describe() )
    print( "\ndf.columns" )
    print( df.columns )
    
    try:
        idx_max = df.loc[df['prop_preds'].le(critical_value), 'prop_preds'].idxmax()
        print("idx_max = ", idx_max)
    except Exception as e:
        print(e)
        print("No mols exist whose prop_preds satisfy the condition: ", "prop_preds  <= ", critical_value)
        print("Set idx_max =  0")
        idx_max =  0
        

    if idx_max > 0:
        new_optmols_smis = df['smiles'].tolist()[ : idx_max ]
    else:
        print("!!! Warning, new_optmols_smis is an empty set.")
        new_optmols_smis = []
        
    new_optmols_smis = set( new_optmols_smis )
    print("\nlength of new_optmols_smis is : ", len(new_optmols_smis))

    if mutation_generation > 0:
        print("mutation_generation = %4d > 0"%mutation_generation )
    
        old_acc_optmols_suppl = Chem.SmilesMolSupplier( old_acc_optmols_smi_path, titleLine=False)
        # print("length of old_acc_optmols_suppl is : ", len(old_acc_optmols_suppl))
        old_acc_optmols = [x for x in old_acc_optmols_suppl if x is not None]
        # print("length of old_acc_optmols is : ", len(old_acc_optmols))
        old_acc_optmols_smis =  [ Chem.MolToSmiles( mol ) for mol in old_acc_optmols ]
        old_acc_optmols_smis = set(old_acc_optmols_smis)

    else:
        print("mutation_generation = %4d = 0"%mutation_generation )
        print("set old_acc_optmols_smis as empty set.")    
        old_acc_optmols_smis = set( )
        
    print("length of old_acc_optmols_smis is : ", len(old_acc_optmols_smis))    
    
    acc_optmols_smis = old_acc_optmols_smis.union( new_optmols_smis )
    acc_optmols_smis = list( acc_optmols_smis )
    acc_optmols_smis.sort()
    
    print("length of acc_optmols_smis is : ", len(acc_optmols_smis))

    with open(acc_optmols_smi_path, 'w') as fr:
        for smi in acc_optmols_smis:
            fr.write(smi + '\n')

    
    if is_write_sdf == True:
        #---- write molecules to SD File -------------------------------        
        print("\nWrite to sdf file.\n")
        
        All_mols = [ Chem.MolFromSmiles( smi ) for smi in acc_optmols_smis if Chem.MolFromSmiles(smi) is not None]
        
        cpd_names = [ "cpd-%05d" % (i+1) for i in range(len(All_mols)) ]
        for mol, cpd_name in zip(All_mols, cpd_names):
            mol.SetProp("_Name", cpd_name )

        call_mkdir_acc_optmols = 'mkdir   ' +  outdir_path  +  '    2>>/dev/null  '
        status, output = subprocess.getstatusoutput( call_mkdir_acc_optmols )
        print("mkdir  ./project/GXXXX/acc_optmols;    status, output = ", status, output)        

        print("call write_mols_paralell(), the separate acc_optmols are written to dir:  %s"%outdir_path )
        write_mols_paralell(All_mols, cpd_names, outfile_path=outdir_path)

        print("cat cpd*.sdf to acc_optmols.sdf")
        status, output = subprocess.getstatusoutput( 'rm  -f   ./project/' +  'G%04d'%mutation_generation  +  '/acc_optmols.sdf   2>>/dev/null ' )
        print("status, output = ", status, output)
        cat_sdfs_to_onefile = 'cat   '  +  outdir_path  + 'cpd*.sdf  >>  '  +  './project/' + 'G%04d'%mutation_generation  + '/acc_optmols.sdf   '
        status, output = subprocess.getstatusoutput( cat_sdfs_to_onefile )
        print("status, output = ", status, output)

    else:
        print("\nDo not write to sdf file.\n")

   
    return len( acc_optmols_smis )



def accumulate_optmols_S1En(mutation_generation=1, 
                            old_acc_optmols_smi_paths=[ './project/G%04d/acc_optmols--S1En-%s.smi'%( 0, color ) for color in ["R", "G", "B"] ],
                            new_mols_path='./project/G%04d/G%04d_df_ECFP--S1En.csv'%( 1, 1 ),
                            acc_optmols_smi_paths=[ './project/G%04d/acc_optmols--S1En-%s.smi'%( 1, color ) for color in ["R", "G", "B"] ],
                            column_names=[ 'compoundnames', 'smiles', 'prop_preds' ], 
                            critical_values=[ 2.70, 3.00 ],
                            ):
    '''
    This function can accumulate the optimal mols by calculating the union of two sets of optmols (items are SMILES), 
    acc_optmols = old_acc_optmols.union( new_mols )
    The resultant acc_optmols smi file is written to acc_optmols.smi, 
    if desired (set is_write_sdf=True), the sdf file is also written to acc_optmols.sdf.
    

    Parameters
    ----------
    mutation_generation : int, optional
        DESCRIPTION. The default is 1. mutation_generation must be >= 0  integer,
                     if mutation_generation = 0, the acc_optmols = new_mols
    old_acc_optmols_smi_path : TYPE, optional
        DESCRIPTION. The default is './project/G%04d/acc_optmols--S1En.smi'%( 0 ).
    new_mols_path : TYPE, optional
        DESCRIPTION. The default is './project/G%04d/G%04d_df_ECFP--S1En.csv'%( 1, 1 ).
    acc_optmols_smi_path : TYPE, optional
        DESCRIPTION. The default is './project/G%04d/acc_optmols--S1En.smi'%( 1 ).
    column_names : TYPE, optional
        DESCRIPTION. The default is [ 'smiles', 'prop_preds' ].
    critical_values : TYPE, optional
        DESCRIPTION. The default is [2.70, 3.00].

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''

    print("Call accumulate_optmols_S1En():\n")    

    df = pd.read_csv(new_mols_path, 
                     usecols=column_names
                     )
    
    print( "\ndf.head()" )
    print( df.head() )
    print( "\ndf.describe()" )
    print( df.describe() )
    print( "\ndf.columns" )
    print( df.columns )

    #--- define  gt_idxmax_B for blue color. energy > ENERGY_THRESHOLD2 = 2.80 ev -------
    #--- if gt_idxmax_B > 0, the indexs for blue mols are  [0 : gt_idmax_B]
    #--- then, le_idxmin_G is the ending index for green color. 
    lt_idxmin_G, le_idxmin_G, gt_idxmax_B, ge_idxmax_B = getmaxminidxs_lt_le_gt_ge_criticval_df(df, 
                                                                                                colname='prop_preds',
                                                                                                critical_value=critical_values[1],
                                                                                                ascending=False)
    
    #--- define  lt_idxmin_R for red color. energy < ENERGY_THRESHOLD1 = 2.30 ev -------
    #--- if lt_idxmin_R > 0, the indexs for red mols are  [lt_idmin_R : ]
    #--- then, ge_idxmax_G is the starting index for green color. 
    lt_idxmin_R, le_idxmin_R, gt_idxmax_G, ge_idxmax_G = getmaxminidxs_lt_le_gt_ge_criticval_df(df, 
                                                                                                colname='prop_preds',
                                                                                                critical_value=critical_values[0],
                                                                                                ascending=False)
    
    if (gt_idxmax_B > 0):
        optimal_smis_B = df.smiles.tolist()[0 : gt_idxmax_B]
        optimal_cpdnames_B = df.compoundnames.tolist()[0 : gt_idxmax_B]
        prop_preds_S1En_B = df.prop_preds.tolist()[0 : gt_idxmax_B]
        print("-"*60)
        print("-#-Blue mols, the optimal_cpdname, optimal_smis and prop_preds_S1En are:")
        for cpdname, smi, S1En in zip(optimal_cpdnames_B, optimal_smis_B, prop_preds_S1En_B):
            print(cpdname, " , ", smi, " , %8.4f"%S1En )    
    else:
        optimal_smis_B = set()
        print("-#-Blue mols is empty!")
    
    
    if (le_idxmin_G < df.shape[0]) and (ge_idxmax_G < df.shape[0]) and (le_idxmin_G < ge_idxmax_G):
        optimal_smis_G = df.smiles.tolist()[le_idxmin_G : ge_idxmax_G]
        optimal_cpdnames_G = df.compoundnames.tolist()[le_idxmin_G : ge_idxmax_G]
        prop_preds_S1En_G = df.prop_preds.tolist()[le_idxmin_G : ge_idxmax_G]
        print("-"*60)
        print("-#-Green mols, the optimal_cpdname, optimal_smis and prop_preds_S1En are:")
        for cpdname, smi, S1En in zip(optimal_cpdnames_G, optimal_smis_G, prop_preds_S1En_G):
            print(cpdname, " , ", smi, " , %8.4f"%S1En )    
    else:
        optimal_smis_G = set()
        print("-#-Green mols is empty!")
    
    
    if (lt_idxmin_R < df.shape[0]):
        optimal_smis_R = df.smiles.tolist()[lt_idxmin_R : ]
        optimal_cpdnames_R = df.compoundnames.tolist()[lt_idxmin_R : ]
        prop_preds_S1En_R = df.prop_preds.tolist()[lt_idxmin_R : ]
        print("-"*60)
        print("-#-Red mols, the optimal_cpdname, optimal_smis and prop_preds_S1En are:")
        for cpdname, smi, S1En in zip(optimal_cpdnames_R, optimal_smis_R, prop_preds_S1En_R):
            print(cpdname, " , ", smi, " , %8.4f"%S1En )    
    else:
        optimal_smis_R = set()
        print("-#-Red mols is empty!")
    
    
    print("-#-Size of Blue, Green, Red mols are: ", len(optimal_smis_B), len(optimal_smis_G), len(optimal_smis_R))


    new_optmols_smis_all = [ optimal_smis_R, optimal_smis_G, optimal_smis_B ]
    acc_optmols_smis_all = []
    for  i in range(3):
        print("-#- ", i)
        new_optmols_smis = set( new_optmols_smis_all[i] )
        print("\nlength of new_optmols_smis_S1En is : ", len(new_optmols_smis))
    
        if mutation_generation > 0:
            print("mutation_generation = %4d > 0"%mutation_generation )
            
            try:
                old_acc_optmols_suppl = Chem.SmilesMolSupplier( old_acc_optmols_smi_paths[i], titleLine=False)
                old_acc_optmols = [x for x in old_acc_optmols_suppl if x is not None]
                old_acc_optmols_smis =  [ Chem.MolToSmiles( mol ) for mol in old_acc_optmols ]
                old_acc_optmols_smis = set(old_acc_optmols_smis)
            except Exception as e:
                print(e)
                print("*** Set old_acc_optmols_smis an empty set.")
                old_acc_optmols_smis = set()
    
        else:
            print("mutation_generation = %4d "%mutation_generation )
            print("set old_acc_optmols_smis_S1En as empty set.")    
            old_acc_optmols_smis = set( )
            
        print("length of old_acc_optmols_smis_S1En is : ", len(old_acc_optmols_smis))    
        
        acc_optmols_smis = old_acc_optmols_smis.union( new_optmols_smis )
        acc_optmols_smis = list( acc_optmols_smis )
        acc_optmols_smis.sort()
        
        print("length of acc_optmols_smis_S1En is : ", len(acc_optmols_smis))
    
        with open(acc_optmols_smi_paths[i], 'w') as fr:
            #fr.write("#smiles\n" )
            for smi in acc_optmols_smis:
                fr.write(smi + '\n')

        acc_optmols_smis_all.append(acc_optmols_smis)
   
    return len( acc_optmols_smis_all[0] ), len( acc_optmols_smis_all[1] ), len( acc_optmols_smis_all[2] )



def sort_mols_by_SAScores(mutation_generation=1,
                          acc_optmols_smi_path='./project/G0001/acc_optmols.smi', 
                          column_names=[ 'mols', 'smiles' ], 
                          outdir_path='./project/G0001/acc_optmols_sortedbysas/',
                          is_write_sdf=True, 
                          new_sdf_path='./project/G0001/acc_optmols_sortedbysas.sdf',
                          ascending=True
                          ):
    
    acc_optmols_suppl = Chem.SmilesMolSupplier( acc_optmols_smi_path, titleLine=False)
    print("length of acc_optmols_suppl is : ", len(acc_optmols_suppl))
    acc_optmols = [x for x in acc_optmols_suppl if x is not None]
    print("length of acc_optmols is : ", len(acc_optmols))
    acc_optmols_smis =  [ Chem.MolToSmiles( mol ) for mol in acc_optmols ]
    
    
    df = pd.DataFrame(data=zip(acc_optmols, acc_optmols_smis), 
                          columns=column_names
                          )

    df['SAscores'] = df.mols.map(sascorer.calculateScore)

    print( "\ndf.columns" )
    print( df.columns )
    print( "\ndf.describe()" )
    print( df.describe() )    
    # print( "\ndf.head()" )
    # print( df.head() )
    
    # (id_max, id_min) = (df.calc_SA_score.idxmax(), df.calc_SA_score.idxmin())

    df.sort_values(by="SAscores", ascending=ascending, inplace=True)

    print('# The optimal 16 molecules are: ')
    print( df.head(16) )

    if (is_write_sdf == True):
        #---- write molecules to SD File -------------------------------        
        print("\nWrite to sdf file.\n")
        
        All_mols = df['mols'].tolist()
        
        cpd_names = [ "cpd-%05d" % (i+1) for i in range(len(All_mols)) ]
        for mol, cpd_name in zip(All_mols, cpd_names):
            mol.SetProp("_Name", cpd_name )

        call_mkdir_acc_optmols_sorted = 'mkdir   ' +  outdir_path  +  '    2>/dev/null  '
        status, output = subprocess.getstatusoutput( call_mkdir_acc_optmols_sorted )
        print("mkdir  ./project/GXXXX/acc_optmols_sortedbysas/;    status, output = ", status, output)        

        print("call write_mols_paralell(), the separate acc_optmols are written to dir:  %s"%outdir_path )
        write_mols_paralell(All_mols, cpd_names, outfile_path=outdir_path)

        print("cat cpd*.sdf to acc_optmols.sdf")
        status, output = subprocess.getstatusoutput( 'rm  -f   ./project/' +  'G%04d'%mutation_generation  +  '/acc_optmols_sortedbysas.sdf   2>/dev/null ' )
        print("status, output = ", status, output)
        cat_sdfs_to_onefile = 'cat   '  +  outdir_path  + 'cpd*.sdf  >>  '  +  './project/' + 'G%04d'%mutation_generation  + '/acc_optmols_sortedbysas.sdf   '
        status, output = subprocess.getstatusoutput( cat_sdfs_to_onefile )
        print("status, output = ", status, output)

    else:
        print("\nDo not write to sdf file.\n")


    return df



def accumulate_optmols_intersection(mutation_generation=0, 
                                    acc_optmols_smi_path1='./project/G%04d/acc_optmols.smi'%( 0 ),
                                    acc_optmols_smi_path2='./project/G%04d/acc_optmols--S1En-B.smi'%( 0 ),
                                    acc_optmols_smi_path3='./project/G%04d/acc_optmols--INTERSCTION-B.smi'%( 0 ), 
                                    is_write_sdf=False, 
                                    outdir_path='./project/G%04d/acc_optmols--INTERSCTION-B/'%( 0 )
                                    ):


    acc_optmols_suppl1 = Chem.SmilesMolSupplier( acc_optmols_smi_path1, titleLine=False)
    acc_optmols1 = [x for x in acc_optmols_suppl1 if x is not None]
    acc_optmols_smis1 =  [ Chem.MolToSmiles( mol ) for mol in acc_optmols1 ]
    acc_optmols_smis1 = set(acc_optmols_smis1)
        
    print("length of acc_optmols_smis1 is : ", len(acc_optmols_smis1))    
    
    acc_optmols_suppl2 = Chem.SmilesMolSupplier( acc_optmols_smi_path2, titleLine=False)
    acc_optmols2 = [x for x in acc_optmols_suppl2 if x is not None]
    acc_optmols_smis2 =  [ Chem.MolToSmiles( mol ) for mol in acc_optmols2 ]
    acc_optmols_smis2 = set(acc_optmols_smis2)
    
    print("length of acc_optmols_smis2 is : ", len(acc_optmols_smis2))    
    
    acc_optmols_smis = acc_optmols_smis1.intersection( acc_optmols_smis2 )
    acc_optmols_smis = list( acc_optmols_smis )
    acc_optmols_smis.sort()
    
    print("length of acc_optmols_smis (the intersection set) is : ", len(acc_optmols_smis))

    with open(acc_optmols_smi_path3, 'w') as fr:
        for smi in acc_optmols_smis:
            fr.write(smi + '\n')

    
    if is_write_sdf == True:
        #---- write molecules to SD File -------------------------------        
        print("\nWrite to sdf file.\n")
        
        All_mols = [ Chem.MolFromSmiles( smi ) for smi in acc_optmols_smis if Chem.MolFromSmiles(smi) is not None]
        
        cpd_names = [ "cpd-%05d" % (i+1) for i in range(len(All_mols)) ]
        for mol, cpd_name in zip(All_mols, cpd_names):
            mol.SetProp("_Name", cpd_name )

        call_mkdir_acc_optmols = 'mkdir   ' +  outdir_path  +  '    2>>/dev/null  '
        status, output = subprocess.getstatusoutput( call_mkdir_acc_optmols )
        print("mkdir  ./project/GXXXX/acc_optmols--INTERSCTION-B;    status, output = ", status, output)        

        print("call write_mols_paralell(), the separate acc_optmols--INTERSCTION-B are written to dir:  %s"%outdir_path )
        write_mols_paralell(All_mols, cpd_names, outfile_path=outdir_path)

        print("cat cpd*.sdf to acc_optmols--INTERSCTION-B.sdf")
        status, output = subprocess.getstatusoutput( 'rm  -f   ./project/' +  'G%04d'%mutation_generation  +  '/acc_optmols--INTERSCTION-B.sdf   2>>/dev/null ' )
        print("status, output = ", status, output)
        cat_sdfs_to_onefile = 'cat   '  +  outdir_path  + 'cpd*.sdf  >>  '  +  './project/' + 'G%04d'%mutation_generation  + '/acc_optmols--INTERSCTION-B.sdf   '
        status, output = subprocess.getstatusoutput( cat_sdfs_to_onefile )
        print("status, output = ", status, output)

    else:
        print("\nDo not write to sdf file.\n")

   
    return len( acc_optmols_smis )




#----------------------- maps by FPSimilarity ----------------------------------
def get_intersection_plus_smiles(smis1=['CCOC', 'CCO', 'COC', 'COOC'], 
                                 smis2=['CNCCOC', 'CCOOC', 'CNCCO', 'CNCOC']
                                 ):
    #--- assume size of list1 <= list2 ------------------------------
    #--- further assume elements in list are unique. ------------------------
    print('-'*60)
    
    exchange_flag = False
    if len(smis1) > len(smis2):
        print("len(smis1) > len(smis2), exchange each other.")
        smis1, smis2 = smis2, smis1
        exchange_flag = True
    
    smis1_set = set(smis1)
    smis2_set = set(smis2)
    
    intersection_smis_set = smis1_set.intersection(smis2_set)
    intersection_smis = list(intersection_smis_set)
    intersection_smis.sort()
    
    smis1_dif_smis2_set = smis1_set.difference(smis2_set)
    smis1_dif_smis2 = list(smis1_dif_smis2_set)
    smis1_dif_smis2.sort()
    
    smis2_dif_smis1_set = smis2_set.difference(smis1_set)
    smis2_dif_smis1 = list(smis2_dif_smis1_set)
    smis2_dif_smis1.sort()
    
    print("len(smis1) = ", len(smis1) )
    print("len(smis2) = ", len(smis2) )
    print("len(set(smis1()) = ", len(set(smis1)) )
    print("len(set(smis2)) = ", len(set(smis2)) )
    print("len(intersection_smis) = ", len(intersection_smis) )
    print("len(smis1_dif_smis2) = ", len(smis1_dif_smis2) )
    print("len(smis2_dif_smis1) = ", len(smis2_dif_smis1) )
    # print("len(smis1_dif_smis2 + intersection_smis) = ", len(smis1_dif_smis2 + intersection_smis) )
    # print("len(smis2_dif_smis1 + intersection_smis) = ", len(smis2_dif_smis1 + intersection_smis) )
    
    print("\nsmis1:\n", smis1)
    print("smis2:\n", smis2)
    print("intersection_smis:\n", intersection_smis)
    print("smis1_dif_smis2:\n", smis1_dif_smis2)
    print("smis2_dif_smis1:\n", smis2_dif_smis1)
    
    smis1_rev  =  intersection_smis + smis1_dif_smis2
    smis2_rev  =  intersection_smis + smis2_dif_smis1
    
    return intersection_smis, smis1_rev, smis2_rev, exchange_flag



def compute_similarity_matrix(smis1=['CCOC', 'CCO'], 
                              smis2=['CNCCOC', 'CCOOC', 'CNCCO', 'CNCOC'],
                              fpSize=2048
                              ):
    #--- assume number of rows <= number of columns ------------------------------
    print('-'*60)
    
    if len(smis1) > len(smis2):
        print("exchange smis1, smis2")
        smis1, smis2 = smis2, smis1
    
    print("smis1:\n", smis1)
    print("smis2:\n", smis2)
    
    ms1 = [Chem.MolFromSmiles(smi) for smi in smis1]
    ms2 = [Chem.MolFromSmiles(smi) for smi in smis2]
    
    #Chem.RDKFingerprint(x, fpSize=2048)  #  Returns an RDKit topological fingerprint for a molecule
    fps1 = [Chem.RDKFingerprint(x, fpSize=fpSize) for x in ms1]
    fps2 = [Chem.RDKFingerprint(x, fpSize=fpSize) for x in ms2]
    
    n1 = len(fps1)
    n2 = len(fps2)
    
    arr_sim = np.zeros(shape=(n1, n2), 
                       dtype=np.float64
                       )  
    
    for i in range(n1):
        for j in range(n2):
            tempt_sim = DataStructs.FingerprintSimilarity(fps1[i], fps2[j])
            arr_sim[i][j] = tempt_sim
    
    mat_sim = np.matrix(data=arr_sim,
                        dtype=arr_sim.dtype)
    
    print("\nmat_sim:\n", mat_sim)
    
    return mat_sim



def map_molslibs_by_similarity(smis1=['CCOC', 'CCO'], 
                               smis2=['CNCCOC', 'CCOOC', 'CNCCO', 'CNCOC'],
                               fpSize=2048,
                               is_return_max_app_sim=False
                               ):
    #--- assume number of rows <= number of columns ------------------------------
    #--- assume size of list1 <= list2 ------------------------------
    #--- further assume elements in list are unique. ------------------------
    #------------------------------------------------------------------------------
    # A[[i, j], :] = A[[j, i], :] # 实现了第i行与第j行的互换
    #-----------------------------------------------------------------------------
    if len(smis1) > len(smis2):
        print("len(smis1) > len(smis2), exchange each other.")
        smis1, smis2 = smis2, smis1
    
    n1 = len(smis1)
    n2 = len(smis2)
    
    mat_sim = compute_similarity_matrix(smis1=smis1, 
                                        smis2=smis2,
                                        fpSize=fpSize
                                        )
    
    ms1_indexs = list( range(n1) )
    ms2_indexs = list( range(n2) )

    #--- transform matrix by similarity maxium rule. --------------------------
    print('/'*60)
    print("\nBegin transform mat_sim.")
    for i in range(n1 - 1):
        print('-'*60)
        print("row (or column) index = %4d"%i)
        # print("\nmat_sim, original:\n", mat_sim)
        
        max_index = np.unravel_index(mat_sim[i:n1, i:n2].argmax(), mat_sim[i:n1, i:n2].shape)
            
        # print("\nmat_sim[i:n1, i:n2]:\n", mat_sim[i:n1, i:n2])
        # print("\nmax_index: \n", max_index)
        max_row_index = max_index[0] + i
        max_column_index = max_index[1] + i
        print("max_row_index = ", max_row_index, "; max_column_index = ", max_column_index )
        print("max_value = ", mat_sim[max_row_index, max_column_index])
    
        if (max_row_index != i):
            mat_sim[[i, max_row_index], :] = mat_sim[[max_row_index, i], :]
            # print("\nmat_sim, after row_exchange: %4d <--> %4d\n"%(i, max_row_index), mat_sim)
            
            # print("Before exchange row: ", ms1_indexs[i], ms1_indexs[max_row_index])
            tempt_row_index  = ms1_indexs[i]
            ms1_indexs[i] = ms1_indexs[max_row_index]
            ms1_indexs[max_row_index] = tempt_row_index
            # print("After exchange row: ", ms1_indexs[i], ms1_indexs[max_row_index])
    
        if (max_column_index != i):
            mat_sim[: , [i, max_column_index] ] = mat_sim[: , [max_column_index, i]]
            # print("\nmat_sim, after column_exchange: %4d <--> %4d\n"%(i, max_column_index), mat_sim)
            
            # print("Before exchange column: ", ms2_indexs[i], ms2_indexs[max_column_index])
            tempt_column_index  = ms2_indexs[i]
            ms2_indexs[i] = ms2_indexs[max_column_index]
            ms2_indexs[max_column_index] = tempt_column_index
            # print("After exchange column: ", ms2_indexs[i], ms2_indexs[max_column_index])
    
    print("\nEnd transform mat_sim.")
    print('\\'*60)
        
    new_smis1 = [smis1[idx] for idx in ms1_indexs]
    new_smis2 = [smis2[idx] for idx in ms2_indexs]

    print("Restrict the size of new_smis2 by the size of new_smis1.")
    new_smis2 = new_smis2[:len(new_smis1)]

    print('-'*60)
    print("\nms1_indexs:", ms1_indexs)
    print("ms2_indexs:", ms2_indexs)
    print("smis1:\n", smis1)
    print("smis2:\n", smis2)    
    print("new_smis1:\n", new_smis1)
    print("new_smis2:\n", new_smis2)
    print("\nmat_sim:\n", mat_sim)

    if (is_return_max_app_sim == False):
        return new_smis1, new_smis2, mat_sim
    else:
        diag_sim = np.diag(mat_sim)
        if (diag_sim.shape[0] > 0):
            max_app_sim = diag_sim.sum()/diag_sim.shape[0]
        else:
            print("diag_sim.shape[0] <= 0")
            exit(-1)
        print("diag_sim:\n", diag_sim)
        print("diag_sim.shape = ", diag_sim.shape)
        print("max_app_sim = ", max_app_sim)    
        
        return new_smis1, new_smis2, mat_sim, max_app_sim
        


def get_centroid_series(smis=[ 'CCCNCCO', 'CCNCCO', 'CC' ],
                        is_return_arranged_smis=False
                        ):
    
    mat_sim = compute_similarity_matrix(smis1=smis, 
                                        smis2=smis,
                                        fpSize=2048
                                        )

    n1 = len(smis)
    n2 = n1
    ms1_indexs = list( range(n1) )

    #--- transform matrix by similarity maximum rule. --------------------------
    print('/'*60)
    print("Compute a series of similarity mass centers.")
    print("\nBegin transform mat_sim.")
    print("mat_sim: \n", mat_sim)
    for i in range(n1 - 1):
        print('-'*60)
        print("row (or column) index = %4d"%i)
        print("exchange before, mat_sim[i:n1, i:n2] : \n", mat_sim[i:n1, i:n2])
        mat_sim_row_means = mat_sim[i:n1, i:n2].mean(axis=1)
        print("mat_sim_row_means:\n", mat_sim_row_means)
        row_max_idx = mat_sim_row_means.argmax() + i
        print("row_max_idx = ", row_max_idx)
        print("Centriod mol: ", smis[row_max_idx])
        
        if row_max_idx != i:
            mat_sim[[i, row_max_idx], :] = mat_sim[[row_max_idx, i], :]
            mat_sim[: , [i, row_max_idx] ] = mat_sim[: , [row_max_idx, i]]
            ms1_indexs[i], ms1_indexs[row_max_idx] = ms1_indexs[row_max_idx], ms1_indexs[i]
        
        print("exchange after, mat_sim[i:n1, i:n2] : \n", mat_sim[i:n1, i:n2])
        print("ms1_indexs:\n", ms1_indexs)
    
    print("\nEnd transform mat_sim.")
    
    centriod_smis = [smis[idx] for idx in ms1_indexs]
    print("\ncentriod_smis:\n", centriod_smis)

    #--------- is return arranged smis by shifting the middle ones to the middle of the series.
    if (is_return_arranged_smis == True):
        print('\\'*60)
        print("len(ms1_indexs) = ", len(ms1_indexs))
        print("len(ms1_indexs)/2 = ", int(len(ms1_indexs)/2) )
        print("ms1_indexs:\n", ms1_indexs)
        # mid_idx = int( len(ms1_indexs)/2 )
        new_middle_idxs = []
        
        mol_0 = Chem.MolFromSmiles( smis[ ms1_indexs[0] ])
        fp_0 = Chem.RDKFingerprint(mol_0, fpSize=2048)
        for i, j in zip(range(0, len(ms1_indexs), 2), range(1, len(ms1_indexs), 2)):
            print(i, j, " : ", ms1_indexs[i], ms1_indexs[j])
            mol_a = Chem.MolFromSmiles( smis[ ms1_indexs[i] ])
            mol_b = Chem.MolFromSmiles( smis[ ms1_indexs[j] ])
            fp_a = Chem.RDKFingerprint(mol_a, fpSize=2048)
            fp_b = Chem.RDKFingerprint(mol_b, fpSize=2048)
            sim_a0 = DataStructs.FingerprintSimilarity( fp_a,  fp_0)
            sim_b0 = DataStructs.FingerprintSimilarity( fp_b,  fp_0)
            print("sim_a0 = ", sim_a0)
            print("sim_b0 = ", sim_b0)
            if sim_a0 > sim_b0:
                ms1_indexs[i], ms1_indexs[j] = ms1_indexs[j], ms1_indexs[i]
                
            print("append, ", ms1_indexs[i], "; insert ", ms1_indexs[j])
            new_middle_idxs.append(ms1_indexs[i])
            new_middle_idxs.insert(0, ms1_indexs[j])
            print("new_middle_idxs:\n", new_middle_idxs)
        
        if len(ms1_indexs) % 2 == 1:
            print("append, ", ms1_indexs[-1])
            new_middle_idxs.append(ms1_indexs[-1])
            print("new_middle_idxs:\n", new_middle_idxs)
    
        print("Final new_middle_idxs:\n", new_middle_idxs)
        new_smis = [ smis[idx] for idx in new_middle_idxs]
        print("new_smis:\n", new_smis)
        
        mat_sim_final = compute_similarity_matrix(smis1=[ centriod_smis[0]  ], 
                                                  smis2=new_smis,
                                                  fpSize=2048
                                                  )
    
    else:

        mat_sim_final = compute_similarity_matrix(smis1=[ centriod_smis[0]  ], 
                                                  smis2=centriod_smis,
                                                  fpSize=2048
                                                  )

    
    mat_sim_row_means_final = mat_sim_final.mean(axis=1)
    print("mat_sim_row_means_final:\n", mat_sim_row_means_final)
    max_ave_sim = mat_sim_row_means_final[0]
    print("\nmax_nave_sim = %10.3f"%max_ave_sim)

    # mat_sim_row_means_global = mat_sim.mean(axis=1)
    # print("mat_sim_row_means_global:\n", mat_sim_row_means_global)
    # global_row_max_idx = mat_sim_row_means_global.argmax()
    # ave_sim = mat_sim_row_means_global[global_row_max_idx]
    # print("\nave_sim = %10.4f"%ave_sim)


    if (is_return_arranged_smis == False):
        return centriod_smis, max_ave_sim
    else:
        return centriod_smis, max_ave_sim, new_smis

    

def get_centroid(smis=[ 'CCCNCCO', 'CCNCCO', 'CC' ]
                 ):
    
    mat_sim = compute_similarity_matrix(smis1=smis, 
                                        smis2=smis,
                                        fpSize=2048
                                        )

    print("mat_sim: \n", mat_sim)
    mat_sim_row_means = mat_sim.mean(axis=1)
    print("mat_sim_row_means:\n", mat_sim_row_means)
    row_max_idx = mat_sim_row_means.argmax()
    print("row_max_idx = ", row_max_idx)
    
    centriod_smi = smis[row_max_idx]
    max_ave_sim = mat_sim_row_means[row_max_idx]
    
    print("\ncentriod_smi: \n", smis[row_max_idx])
    print("\nmax_ave_sim = %10.3f"%max_ave_sim)

    return centriod_smi, max_ave_sim
    
    
def draw_mols_and_show(smis,
                       figname='foo--mols.png',
                       molsPerRow=3,
                       subImgSize=(800, 800),
                       num_of_mols=None
                       ):
    #-----------------------------------------------------------------------------------------
    if (num_of_mols is None):
        mols1 = [Chem.MolFromSmiles(smi) for smi in smis]
    elif (num_of_mols > 0):
        mols1 = [Chem.MolFromSmiles(smi) for smi in smis[ : num_of_mols] ]
    else:
        print("parameter num_of_mols must be larger than 0 or equal to None. Check it.")
        exit(-1)
    
    img1 = Draw.MolsToGridImage(mols1, 
                                molsPerRow=molsPerRow, 
                                subImgSize=subImgSize, 
                                returnPNG=False)
    
    img1.save(figname)
 
    lena1 = mpimg.imread(figname)    # 读取和代码处于同一目录下的 lena.png  # 此时 lena 就已经是一个 np.array 了，可以对它进行任意处理
    # print("lena1.shape = ", lena1.shape)       #(512, 512, 3)
    plt.imshow(lena1) # 显示图片
    plt.axis('off') # 不显示坐标轴
    plt.show()
    


def load_mols_in_sdf(sdf_path='./data/Pick_mols.sdf'):
    #-------- loading  sdf file ---------------------------------------------------
    sdsuppl = Chem.SDMolSupplier(sdf_path)
    mols = [x for x in sdsuppl if x is not None]
    smiles = [Chem.MolToSmiles(mol) for mol in mols]
    print("-"*60)  
    print( "number of molecules is ", len(mols) )
    
    return mols, smiles


def plot_muation_diagram(filename='./project/mutation_diagram.csv',
                         figname='foo--muation-diagram.png',
                         molsPerRow=3,
                         subImgSize=(800, 800),
                         num_of_mols=None
                         ):
    
    df = pd.read_csv(filename)
    # mutation_generation, centriod_smi1, len_smis1, inner_max_ave_sim1, inter_max_app_sim
    
    print( "\ndf.head()" )
    print( df.head() )
    print( "\ndf.describe()" )
    print( df.describe() )
    print( "\ndf.columns" )
    print( df.columns )    
    
    # mutation_generations = df['mutation_generation'].tolist()
    centriod_smis = df['centriod_smi1'].tolist()
    len_smis = df['len_smis1'].tolist()
    inner_max_ave_sims = df['inner_max_ave_sim1'].tolist()
    inter_max_app_sims = df['inter_max_app_sim'].tolist()
    
    legends_ = [ "(%5d, %6.3f, %6.3f)"%(ele1, ele2, ele3) for ele1, ele2, ele3 in zip(len_smis, inner_max_ave_sims, inter_max_app_sims) ]
    
    #-----------------------------------------------------------------------------------------
    if (num_of_mols is None):
        mols1 = [Chem.MolFromSmiles(smi) for smi in centriod_smis]
    elif (num_of_mols > 0):
        mols1 = [Chem.MolFromSmiles(smi) for smi in centriod_smis[ : num_of_mols] ]
    else:
        print("parameter num_of_mols must be larger than 0 or equal to None. Check it.")
        exit(-1)
    
    img1 = Draw.MolsToGridImage(mols1, 
                                molsPerRow=molsPerRow, 
                                subImgSize=subImgSize, 
                                legends=legends_,
                                returnPNG=False)
    
    img1.save(figname)
 
    lena1 = mpimg.imread(figname)    # 读取和代码处于同一目录下的 lena.png  # 此时 lena 就已经是一个 np.array 了，可以对它进行任意处理
    # print("lena1.shape = ", lena1.shape)       #(512, 512, 3)
    plt.imshow(lena1) # 显示图片
    plt.axis('off') # 不显示坐标轴
    plt.show()


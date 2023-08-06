#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 09:45:41 2021

Sidechain-Core Enumeration:

#1. OrganoMetals2P2_Enumeration(ligandA_smis, ligandB_smis, metal_smis=['[Cu]', '[Ag]'], verbse=False)
Return the combinational molecular library as a list of rdkit molecules,
organometals

Examples of args:
    ligandA_smis = ['C1=CC=[N+]4C2=C1C=CC3=C2[N+](=CC=C3)[*]4', 
                    'NCCCC1=CC=[N+]4C2=C1C=CC3=C2[N+](=CC=C3)[*]4']
    
    ligandB_smis = ['C1=CC=[P]4C2=C1C=CC3=C2[P](=CC=C3)[Po]4', 
                    'NCCCC1=CC=[N+]4C2=C1C=CC3=C2[P](=CC=C3)[Po]4'] 
    
    metal_smis=['[Cu]', '[Ag]']

Note: 1. Frag ligandA must have only 1 position label by [#0],
         ([#0] is dicoordinated to N^N, P^P, N^P, where N should be set as [N+] or [n+]
           if N has formally 4 bonds);
      2. Frag ligandB must replace the [#0] atom in ligandA from the [Po] ending, 
         ([Po] is dicoordinated to N^N, P^P, N^P, where N should be set as [N+] or [n+]
          if N has formally 4 bonds);
      3. metal must replace the [Po] atom in ligandA_Po_ligandB to form ligandA_Metal_ligandB,
         (that is organometal molecule)

By restrict that the frags have 1 and only 1 attaching points, 
we make things simple and controlable.


#2. OrganoMetals2P1_Enumeration(ligandA_smis, ligandB_smis, metal_smis=['[Cu]', '[Ag]'], verbse=False)
Return: 
    organometals

Examples of args:
    ligandA_smis = ['C1=CC=[N+]4C2=C1C=CC3=C2[N+](=CC=C3)[*]4', 
                    'NCCCC1=CC=[N+]4C2=C1C=CC3=C2[N+](=CC=C3)[*]4', 
                    'OCCCC1=CC=[P]4C2=C1C=CC3=C2[P](=CC=C3)[*]4']    

    ligandB_smis = ['C1=CC=C[N]1[Po]', 'NCCCC1=CC=C[N]1[Po]', 'OCCCC1=CC=C[N]1[Po]'] 
    
    metal_smis=['[Cu]', '[Ag]']

Note: 1. If finally N atom does not have 4 bonds coordinated, do not change [N] -> [N+] 

#3. set_dative_bonds(mol, fromAtoms=(7,8))

#4. set_dative_bonds_batch(organometals, fromAtoms=(7,8))

#5. draw_mols(mols, nb_mols=9, file_name='./foo-gridimage-mols.png', molsPerRow=9, size=(400, 400))


@author: tucy
"""

from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
from rdkit import RDLogger
from module_MD.D_Pi_A_Enumeration import delete_repeated_smiles_of_mols
from tqdm import tqdm
from joblib import Parallel, delayed
import time
import subprocess
#from module_MD.D_Pi_A_Enumeration import D_A_Enumeration_new
from module_MD.D_Pi_A_Enumeration import D_A_Enumeration_new_FullSubstitute
from module_MD.D_Pi_A_Enumeration import replace_dummy_by_Po_label
from module_MD.D_Pi_A_Enumeration import find_label_atom_idxs
from module_MD.D_Pi_A_Enumeration import find_label_atom_idx
from module_MD.D_Pi_A_Enumeration import delete_label_atoms_new
#import numpy as np
import sys 



RDLogger.DisableLog('rdApp.*') 



#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def is_transition_metal(at):
    n = at.GetAtomicNum()
    return (n>=22 and n<=29) or (n>=40 and n<=47) or (n>=72 and n<=79)

def set_dative_bonds(mol, fromAtoms=(7,8)):
    """ convert some bonds to dative

    Replaces some single bonds between metals and atoms with atomic numbers in fromAtoms
    with dative bonds. The replacement is only done if the atom has "too many" bonds.

    Returns the modified molecule.

    """
    pt = Chem.GetPeriodicTable()
    rwmol = Chem.RWMol(mol)
    rwmol.UpdatePropertyCache(strict=False)
    __metals = [at for at in rwmol.GetAtoms() if is_transition_metal(at)]
    #print("metals are: ", __metals)
    
    for metal in __metals:
        #print("metal.GetNeighbors() are: ", metal.GetNeighbors() )
        for nbr in metal.GetNeighbors():
            if nbr.GetAtomicNum() in fromAtoms and \
               nbr.GetExplicitValence() > pt.GetDefaultValence(nbr.GetAtomicNum()) and \
               rwmol.GetBondBetweenAtoms(nbr.GetIdx(), metal.GetIdx()).GetBondType() == Chem.BondType.SINGLE:
                  rwmol.RemoveBond(nbr.GetIdx(), metal.GetIdx())
                  rwmol.AddBond(nbr.GetIdx(), metal.GetIdx(), Chem.BondType.DATIVE)
                  
    return rwmol


def OrganoMetals2P2_Enumeration(ligandA_smis, ligandB_smis, metal_smis=['[Cu+]', '[Ag+]'], verbse=False):
    ligandAs = [Chem.MolFromSmiles(smi) for smi in ligandA_smis]
    ligandBs = [Chem.MolFromSmiles(smi) for smi in ligandB_smis]
    metals = [Chem.MolFromSmiles(smi) for smi in metal_smis]
    
    ligandAs_Po_ligandBs = []
    for ligandA in ligandAs:
        for ligandB in ligandBs:
            Po_idx = 0
            for i in range( ligandB.GetNumAtoms() ) :
                #print( i, ligandB.GetAtomWithIdx(i).GetSymbol() ) 
                if ligandB.GetAtomWithIdx(i).GetSymbol() == 'Po':
                    Po_idx = i
            
            #print("Po_idx = ", Po_idx)
            
            ligandA_Po_ligandB = Chem.ReplaceSubstructs(ligandA, 
                                                        Chem.MolFromSmarts('[#0]'), 
                                                        ligandB, 
                                                        replacementConnectionPoint=Po_idx )
            ligandAs_Po_ligandBs.append(ligandA_Po_ligandB[0])
    
    
    organometals = []
    for metal in metals:
        for ligandA_Po_ligandB in ligandAs_Po_ligandBs:
            ligandA_metal_ligandB = Chem.ReplaceSubstructs(ligandA_Po_ligandB, 
                                                           Chem.MolFromSmarts('[Po]'), 
                                                           metal)
            organometals.append(ligandA_metal_ligandB[0])
            
    
            
    for mol in organometals:
        Chem.SanitizeMol(mol)
    
    if verbse:
        print("# info on OrganoMetals2P2_Enumeration( )")
        print("\n# ligandAs :")
        for mol in ligandAs:
            print(Chem.MolToSmiles(mol))         
        
        print("\n# ligandBs :")
        for mol in ligandBs:
            print(Chem.MolToSmiles(mol)) 
                 
        print("\nThe product organometals molecules are: ")
        print("-"*80)
        for mol in organometals:
            print(Chem.MolToSmiles(mol)) 

        print("-"*80)
        print("# The lens of ligandAs, ligandBs, metals, organometals are:")  
        print(len(ligandAs), len(ligandBs), len(metals),  len(organometals) )  

    return delete_repeated_smiles_of_mols(organometals)


def OrganoMetals2P2_Enumeration_diagonalonly(ligandA_smis, metal_smis=['[Cu+]', '[Ag+]'], verbse=False):
    ligandAs = [Chem.MolFromSmiles(smi) for smi in ligandA_smis]
    ligandBs = [Chem.MolFromSmiles(smi) for smi in ligandA_smis]
    metals = [Chem.MolFromSmiles(smi) for smi in metal_smis]
    
    ligandAs_Po_ligandBs = []
    for ligandA in ligandAs:
        for ligandB in ligandBs:
            if Chem.MolToSmiles(ligandA) == Chem.MolToSmiles(ligandB):
                print(Chem.MolToSmiles(ligandA))
                print(Chem.MolToSmiles(ligandB))
                replace_dummy_by_Po_label(ligandB, original_label_symbol='*', final_label_symbol='Po', reverse=False)
                print(Chem.MolToSmiles(ligandB))
                Po_idx = 0
                for i in range( ligandB.GetNumAtoms() ) :
                    #print( i, ligandB.GetAtomWithIdx(i).GetSymbol() ) 
                    if ligandB.GetAtomWithIdx(i).GetSymbol() == 'Po':
                        Po_idx = i
                
                #print("Po_idx = ", Po_idx)
                
                ligandA_Po_ligandB = Chem.ReplaceSubstructs(ligandA, 
                                                            Chem.MolFromSmarts('[#0]'), 
                                                            ligandB, 
                                                            replacementConnectionPoint=Po_idx )
                ligandAs_Po_ligandBs.append(ligandA_Po_ligandB[0])
    
    
    organometals = []
    for metal in metals:
        for ligandA_Po_ligandB in ligandAs_Po_ligandBs:
            ligandA_metal_ligandB = Chem.ReplaceSubstructs(ligandA_Po_ligandB, 
                                                           Chem.MolFromSmarts('[Po]'), 
                                                           metal)
            organometals.append(ligandA_metal_ligandB[0])
            
    
            
    for mol in organometals:
        Chem.SanitizeMol(mol)
    
    if verbse:
        print("# info on OrganoMetals2P2_Enumeration_diagonalonly( )")
        print("\n# ligandAs :")
        for mol in ligandAs:
            print(Chem.MolToSmiles(mol))         
        
        print("\n# ligandBs :")
        for mol in ligandBs:
            print(Chem.MolToSmiles(mol)) 
                 
        print("\nThe product organometals molecules are: ")
        print("-"*80)
        for mol in organometals:
            print(Chem.MolToSmiles(mol)) 

        print("-"*80)
        print("# The lens of ligandAs, ligandBs, metals, organometals are:")  
        print(len(ligandAs), len(ligandBs), len(metals),  len(organometals) )  

    return delete_repeated_smiles_of_mols(organometals)



def OrganoMetals2P1_Enumeration(ligandA_smis, ligandB_smis, metal_smis=['[Cu+]', '[Ag+]'], verbse=False):
    ligandAs = [Chem.MolFromSmiles(smi) for smi in ligandA_smis]
    ligandBs = [Chem.MolFromSmiles(smi) for smi in ligandB_smis]
    metals = [Chem.MolFromSmiles(smi) for smi in metal_smis]
    
    organometals = OrganoMetals2P2_Enumeration(ligandA_smis, ligandB_smis, metal_smis=metal_smis, verbse=False)
    
    if verbse:
        print("# info on OrganoMetals2P1_Enumeration( )")
        print("\n# ligandAs :")
        for mol in ligandAs:
            print(Chem.MolToSmiles(mol))         
        
        print("\n# ligandBs :")
        for mol in ligandBs:
            print(Chem.MolToSmiles(mol)) 
                 
        print("\nThe product organometals molecules are: ")
        print("-"*80)
        for mol in organometals:
            print(Chem.MolToSmiles(mol)) 

        print("-"*80)
        print("# The lens of ligandAs, ligandBs, metals, organometals are:")  
        print(len(ligandAs), len(ligandBs), len(metals),  len(organometals) )  

    return delete_repeated_smiles_of_mols(organometals)


def set_dative_bonds_batch(organometals, fromAtoms=(7,8)):
    if len(organometals) < 1:
        print("Error! length of list must greater than 0")
        exit(1)
    
    organometals_rev = []
    organometals__ = []
    for mol in organometals:
        rwmol = Chem.RWMol(mol)
        rwmol1 = set_dative_bonds(rwmol, fromAtoms=fromAtoms)
        newmol = Chem.ReplaceSubstructs(Chem.Mol(rwmol1), 
                               Chem.MolFromSmarts('[n+]'), 
                               Chem.MolFromSmarts('[n]'),
                               True
                               )
        organometals__.append(newmol[0])
    
    organometals__smis = [Chem.MolToSmiles(mol) for mol in  organometals__]
    organometals__smis_list = list( set(organometals__smis) )
    organometals_rev = [Chem.MolFromSmiles(smi) for smi in  organometals__smis_list]
    
    return organometals_rev


def draw_mols(mols, nb_mols=9, file_name='./foo-gridimage-mols.png', molsPerRow=9, size=(400, 400)):
    # Compute2DCoords for dipection
    for mol in mols[:nb_mols]:
        AllChem.Compute2DCoords(mol)
    
    # View the enumerated molecules: ---------------------------------------------
    img = Draw.MolsToGridImage(
                               mols[:nb_mols], 
                               molsPerRow=molsPerRow, 
                               subImgSize=size,
                               legends=None
                               ) 
    img.save(file_name)



def write_mols_sequential(mols, outname='data/All_mols_sequential.sdf'):
    #------------ sequential write mols------------------------------------------------------
    start = time.time()
    
    mols_w = Chem.SDWriter(outname)
    for m in tqdm(mols): 
        m_temp = Chem.AddHs(m)
        AllChem.EmbedMolecule(m_temp, randomSeed=38)
        mols_w.write(m_temp)
        
    end = time.time()
    
    print('-'*60)
    print("write_mols_to_sdf run in sequential.")
    print('{:.4f} s'.format(end-start))


def write_mol_to_sdf(mol, cpd_name):
    outname='data/OM_Separated_Mols/mol_%s.sdf'% cpd_name 
    #print(outname)
    one_w = Chem.SDWriter(outname)
    m_temp = Chem.AddHs(mol)
    AllChem.EmbedMolecule(m_temp, randomSeed=38)
    m_temp.SetProp("_Name", cpd_name)
    one_w.write(m_temp)


def write_mols_paralell(mols, cpd_names):
    #-------  paralell write mols-----------------------------------------------------------
    start = time.time()
    
    (status0, output0) = subprocess.getstatusoutput("rm -f  ./data/OM_Separated_Mols/mol_cpd-*.sdf   ./data/OM_Separated_Mols/All_mols_new.sdf ")
    
    Parallel(n_jobs=-1)(delayed(write_mol_to_sdf)(mol, cpd_name) \
                        for mol, cpd_name in zip(mols, cpd_names) )
    
    end = time.time()
    
    print('-'*60)
    print("write_mol_to_sdf run in paralell.")
    print('{:.4f} s'.format(end-start))
    
    print("The final sdf file is:  ./data/OM_Separated_Mols/All_mols_new.sdf")
    
    (status, output) = subprocess.getstatusoutput("cat  ./data/OM_Separated_Mols/mol_cpd-*.sdf   >>   ./data/OM_Separated_Mols/All_mols_new.sdf")
    
    print( "Merge separate mols to one file. The status of command is ", status)



def find_Xatom_idxs(mol, atom_symbol="Cl"):
    Xatom_label_idxs = []
    patt = Chem.MolFromSmarts('c~[%s]'%atom_symbol)
    print("-"*80)
    print("#Original smiles:")
    print("%s\n" % Chem.MolToSmiles(mol) )
    #print( mol.HasSubstructMatch(patt) )
    
    if mol.HasSubstructMatch(patt) == True:
        hit_at = mol.GetSubstructMatches(patt)
        
        #print("len(hit_at) = %d \n" % len(hit_at) )
        
        if (len(hit_at) == 2) or (len(hit_at) == 4) :
            #for ele in hit_at:
            #    print(ele)
            
            for ele in hit_at:
                #hit_at_labels = [mol.GetAtomWithIdx(i).GetSymbol() for i in ele ]
        
                #for i, symbol in zip(ele, hit_at_labels):
                #    print(i, symbol)
            
                atom_idxs = [i for i in ele if mol.GetAtomWithIdx(i).GetSymbol() == atom_symbol ]
            
                #print("atom_idxs: ", atom_idxs)
                
                Xatom_label_idxs.append(atom_idxs[0])
        
        elif len(hit_at) == 1:
            #print(hit_at)
        
            #hit_at_labels = [mol.GetAtomWithIdx(i).GetSymbol() for i in hit_at[0] ]
        
            #for i, symbol in zip(hit_at[0], hit_at_labels):
            #    print(i, symbol)
        
            atom_idxs = [i for i in hit_at[0] if mol.GetAtomWithIdx(i).GetSymbol() == atom_symbol ]
        
            #print("atom_idxs: ", atom_idxs)
            
            Xatom_label_idxs.append(atom_idxs[0])
        
        else :
            print("Warning! hit_at = %d is not equal to 1 or 2.\n" % len(hit_at) )
            
    
    #print("len(Xatom_label_idxs) = %d " % len(Xatom_label_idxs) )
    #print("Xatom_label_idxs: ", Xatom_label_idxs )
    
    return Xatom_label_idxs


#------------------------------------------------------------------------------
def replace_Xatom_by_dummy(mol, 
                           original_label_symbol='Cl', 
                           original_label_idxs=[], 
                           final_label_symbol='*', 
                           replace_label_AtomicNum=0, 
                           is_sanitizemol=False):
    
    rwmol = Chem.RWMol(mol)
    rwmol.UpdatePropertyCache(strict=False)
    
    
    if len(original_label_idxs) > 0:
    #     print("No Xatoms exist for replacement!")
    # else:
        for ele in original_label_idxs:
            #print(ele)
            rwmol.GetAtomWithIdx(ele).SetAtomicNum(replace_label_AtomicNum)
            #print("%s\n" % Chem.MolToSmiles(rwmol) )
            #Draw.ShowMol(rwmol, size=(800, 800))
            
        if is_sanitizemol == True:
            try:
                Chem.SanitizeMol(rwmol )
            except Exception:
                print("!!! AtomValenceException occurs!")
                #AllChem.AddHs(rwmol)
                print("The failed smiles is:\n %s" % Chem.MolToSmiles(rwmol) )
                Draw.ShowMol(rwmol, 
                             size=(800, 800), 
                             title="SanitizeMol Failed mol"
                             )
                
                atom_idxs_valences = []
                for idx in original_label_idxs:
                    atom_valence = rwmol.GetAtomWithIdx(idx).GetExplicitValence()
                    print(idx, atom_valence)
                    
                    atom_idxs_valences.append([idx, atom_valence])
                
                high_valence_atom_idxs = []
                low_valence_atom_idxs = []
                for atom_idx, atom_valence in  atom_idxs_valences:
                    if atom_valence > 4:
                        high_valence_atom_idxs.append(atom_idx)
                    elif atom_valence < 4:
                        low_valence_atom_idxs.append(atom_idx)
                        
                #print("High_valence_atom_idxs = %d, Low_valence_atom_idxs = %d \n" %( len(high_valence_atom_idxs), len(low_valence_atom_idxs) ) )
                
                
                #------------- test if len(high_valence_atom_idxs) == 2 &  len(low_valence_atom_idxs) == 0
                if (len(high_valence_atom_idxs) == 2) &  (len(low_valence_atom_idxs) == 0 ):
                    #print("Case 1: len(high_valence_atom_idxs) == 2 &  len(low_valence_atom_idxs) == 0:")
                    #print("The bond_type between high_valence_atoms: ",  rwmol.GetBondBetweenAtoms(high_valence_atom_idxs[0], high_valence_atom_idxs[1]).GetBondType()  )
                    
                    rwmol.RemoveBond(high_valence_atom_idxs[0], high_valence_atom_idxs[1])
                    rwmol.AddBond(high_valence_atom_idxs[0], high_valence_atom_idxs[1], Chem.BondType.SINGLE)
                    
                    #print( rwmol.GetBondBetweenAtoms(high_valence_atom_idxs[0], high_valence_atom_idxs[1]) )

                    # rwmol.replaceBond(unsigned int 	idx,
                    #                   Bond* 	bond,
                    #                   bool 	preserveProps = false 
                    #                   )		
                    
                    #print("After modification. The bond_type between high_valence_atoms: ",  rwmol.GetBondBetweenAtoms(high_valence_atom_idxs[0], high_valence_atom_idxs[1]).GetBondType()  )
                
                #------------- test if len(high_valence_atom_idxs) == 1 &  len(low_valence_atom_idxs) == 1
                # if (len(high_valence_atom_idxs) == 1) &  (len(low_valence_atom_idxs)) == 1:
                #     print("Case 2: (len(high_valence_atom_idxs) == 1) &  (len(low_valence_atom_idxs) == 1):")
                    

                    
                
                #print("The final smiles is:\n %s" % Chem.MolToSmiles(rwmol) )
                Draw.ShowMol(rwmol, 
                             size=(800, 800), 
                             title="Repaired mol"
                             )
                
                
        #print("#After replace_Xatom_by_dummy: ")
        
        #print("%s\n" % Chem.MolToSmiles(rwmol) )
    
    return Chem.Mol(rwmol)


#------------------------------------------------------------------------------
def accumulation_sub1_sub2(mol, ligandB_smis_hindrances, ligandB_smis_donoracceptors, atom_symbol1="Cl", atom_symbol2="Br"):

    onemol_sub1_sub2_mols = []
    Cl_Xatom_label_idxs = find_Xatom_idxs(mol, atom_symbol=atom_symbol1)

    newmol = replace_Xatom_by_dummy(mol, 
                           original_label_symbol=atom_symbol1, 
                           original_label_idxs=Cl_Xatom_label_idxs, 
                           final_label_symbol='*', 
                           replace_label_AtomicNum=0)
    
    
    ligandA_smis = [  Chem.MolToSmiles(newmol) ]

    OM_1sub_mols = D_A_Enumeration_new_FullSubstitute(ligandA_smis, ligandB_smis=ligandB_smis_hindrances, verbse=False)
    
    print("len(OM_1sub_mols) = %8d \n" % len(OM_1sub_mols) )
    
    
    for mol1 in OM_1sub_mols:
        Br_Xatom_label_idxs = find_Xatom_idxs(mol1, atom_symbol=atom_symbol2)

        newmol1 = replace_Xatom_by_dummy(mol1, 
                                       original_label_symbol=atom_symbol2, 
                                       original_label_idxs=Br_Xatom_label_idxs, 
                                       final_label_symbol='*', 
                                       replace_label_AtomicNum=0
                                       )
        
        
        ligandA_smis1 = [  Chem.MolToSmiles(newmol1) ]
    
        OM_1sub_2sub_mols = D_A_Enumeration_new_FullSubstitute(ligandA_smis1, ligandB_smis=ligandB_smis_donoracceptors, verbse=False)
        
        # for ele in OM_1sub_2sub_mols:
        #     print(Chem.MolToSmiles(ele))
        
        print("len(OM_1sub_2sub_mols) = %8d \n" % len(OM_1sub_2sub_mols) )
        
        onemol_sub1_sub2_mols += OM_1sub_2sub_mols
        
    
    onemol_sub1_sub2_mols_rev = []
    
    for mol in onemol_sub1_sub2_mols:
        
        Xatoms_symbols = ["Cl", "Br",  "I", "At", "Li", "Na"]
        
        newmol2 = mol
        
        for xatom_symbol in  Xatoms_symbols:
            x_Xatom_label_idxs = find_Xatom_idxs(newmol2, atom_symbol=xatom_symbol)
    
            newmol2 = replace_Xatom_by_dummy(newmol2, 
                                               original_label_symbol=xatom_symbol, 
                                               original_label_idxs=x_Xatom_label_idxs, 
                                               final_label_symbol='H', 
                                               replace_label_AtomicNum=1
                                               )
            
        onemol_sub1_sub2_mols_rev.append(newmol2)

    
    return onemol_sub1_sub2_mols_rev
    


#------------------------------------------------------------------------------
def find_CH_aromatic_idxs(mol, patt=Chem.MolFromSmarts('c[H]') ):
    Xatom_label_idxs = []
    H_Xatom_label_idxs = []
    #patt = Chem.MolFromSmarts('c[H]')
    # print("-"*80)
    # print("#Original smiles:")
    # print("%s\n" % Chem.MolToSmiles(mol) )
    # print( mol.HasSubstructMatch(patt) )
    
    if mol.HasSubstructMatch(patt) == True:
        hit_at = mol.GetSubstructMatches(patt)
        
        #print("len(hit_at) = %d \n" % len(hit_at) )
        
        if len(hit_at) > 0:
            
            #print("hit_at:\n",  hit_at)
            
            for ele in hit_at:
                # hit_at_labels = [mol.GetAtomWithIdx(i).GetSymbol() for i in ele ]
        
                # for i, symbol in zip(ele, hit_at_labels):
                #     print(i, symbol)
            
                atom_idxs = [i for i in ele if mol.GetAtomWithIdx(i).GetSymbol() == 'C' ]
                H_atom_idxs = [i for i in ele if mol.GetAtomWithIdx(i).GetSymbol() == 'H' ]
                Xatom_label_idxs.append(atom_idxs[0])
                H_Xatom_label_idxs.append(H_atom_idxs[0])
                
        
        else :
            print("Warning! hit_at = %d .\n" % len(hit_at) )
            
    
    #print("len(Xatom_label_idxs) = %d " % len(Xatom_label_idxs) )
    #print("Xatom_label_idxs: ", Xatom_label_idxs )
    
    #print("len(H_Xatom_label_idxs) = %d " % len(H_Xatom_label_idxs) )
    #print("H_Xatom_label_idxs: ", H_Xatom_label_idxs )
    
    
    Xatom_label_idxs = list(set(Xatom_label_idxs))
    
    #print("len(Xatom_label_idxs) = %d " % len(Xatom_label_idxs) )
    #print("Xatom_label_idxs: ", Xatom_label_idxs )
    
    
    return Xatom_label_idxs, H_Xatom_label_idxs



def comb_number_restriction(subpos_number, 
                            substi_number,
                            comb_number): 
    
    from scipy.special import comb
    
    if (subpos_number >= substi_number) & (substi_number == 1):
        comb_number = int( comb(subpos_number, 1) )
        
    elif (subpos_number >= substi_number) & (substi_number == 2):
        comb_number = int( comb(subpos_number, 1) + comb(subpos_number, 2) )
        
    elif (subpos_number >= substi_number) & (substi_number == 3):
        comb_number = int( comb(subpos_number, 1) + comb(subpos_number, 2) + comb(subpos_number, 3) )
        
    elif (subpos_number >= substi_number) & (substi_number == 4):
        comb_number = int( comb(subpos_number, 1) + comb(subpos_number, 2) + comb(subpos_number, 3) \
                          + comb(subpos_number, 4) )
            
    elif (subpos_number >= substi_number) & (substi_number == 5):
        comb_number = int( comb(subpos_number, 1) + comb(subpos_number, 2) + comb(subpos_number, 3) \
                          + comb(subpos_number, 4) + comb(subpos_number, 5))
            
    elif (subpos_number >= substi_number) & (substi_number == 6):
        comb_number = int( comb(subpos_number, 1) + comb(subpos_number, 2) + comb(subpos_number, 3) \
                          + comb(subpos_number, 4) + comb(subpos_number, 5) + comb(subpos_number, 6))
            
    elif (subpos_number >= substi_number) & (substi_number == 7):
        comb_number = int( comb(subpos_number, 1) + comb(subpos_number, 2) + comb(subpos_number, 3)\
                          + comb(subpos_number, 4) + comb(subpos_number, 5) + comb(subpos_number, 6) \
                             + comb(subpos_number, 7) )
            
    elif (subpos_number >= substi_number) & (substi_number == 8):
        comb_number = int( comb(subpos_number, 1) + comb(subpos_number, 2) + comb(subpos_number, 3) \
                          + comb(subpos_number, 4) + comb(subpos_number, 5) + comb(subpos_number, 6) \
                             + comb(subpos_number, 7) + comb(subpos_number, 8) )
        
    elif (subpos_number >= substi_number) & (substi_number == 9):
                comb_number = int( comb(subpos_number, 1) + comb(subpos_number, 2) + comb(subpos_number, 3) \
                          + comb(subpos_number, 4) + comb(subpos_number, 5) + comb(subpos_number, 6) \
                             + comb(subpos_number, 7) + comb(subpos_number, 8)  + comb(subpos_number, 9) )
        
    elif (subpos_number >= substi_number) & (substi_number == 10):
                comb_number = int( comb(subpos_number, 1) + comb(subpos_number, 2) + comb(subpos_number, 3) \
                          + comb(subpos_number, 4) + comb(subpos_number, 5) + comb(subpos_number, 6) \
                             + comb(subpos_number, 7) + comb(subpos_number, 8)  + comb(subpos_number, 9) \
                                 + comb(subpos_number, 10) )

    # else:
    #     print("Condition failed: (subpos_number >= substi_number)")
    #     print("Do not restrict on number of molecules.")


    return comb_number


#------------------------------------------------------------------------------
def mutations_CH_aromatic(mol, 
                          patt=Chem.MolFromSmarts('c[H]'), 
                          substitute_atom="N", 
                          substitute_atomnum=7, 
                          substi_number=0, 
                          sample_number=0, 
                          is_showmol=False,
                          max_subpos=16):
    '''
    This function can find all aromatic c[H] unit in mol, and make the following mutations:
        CH --> N
    If the number of idxs for substitution is N, then the size of returned list of molecules is 2**(N) - 1. 
    
    Note: 
    1. the substitute_atom should be element in the V or III maingroups: 
        substitute_atom = N, P, As, Te, Bi.    substitute_atomnum = 7, 15, 33, 51, 83
        
        substitute_atom = B, Al, Ga, In, Tl.    substitute_atomnum = 5, 13, 31, 49, 81
        
    2. Cautions: the mol should not contain Pb atom, since in the realization of the code, the Pb element has been used.
        Wish, this shortcoming could be overcome in the futrue. 
        
    Parameters
    ----------
    mol : Chem.RdMol
        DESCRIPTION.
    patt : TYPE, optional
        DESCRIPTION. The default is Chem.MolFromSmarts('c[H]').
    substitute_atom : TYPE, optional
        DESCRIPTION. The default is "N".
    substitute_atomnum : TYPE, optional
        DESCRIPTION. The default is 7.
    substi_number : Int, optional
        DESCRIPTION. The default is 0, where all subsitution is possible. 
        1, only single subsitution,
        2, single or double subsitutions,
        3, single or double or triple subsitutions. 
    sample_number : Int, optional
        DESCRIPTION. The default is 0, where all sample gets returned.  

    Returns
    -------
    mutation_mols : list of mols
        DESCRIPTION.

    '''
    import numpy as np
    #from scipy.special import comb
    
    #print("Original mol:\n", Chem.MolToSmiles(mol))
    if is_showmol == True:
        Draw.ShowMol(mol, 
                     size=(800, 800), 
                     title="Original mol"
                     )
    
    mol = Chem.AllChem.AddHs(mol)
    #print("Original mol after AddHs:\n ", Chem.MolToSmiles(mol))
    
    Xatom_label_idxs, H_Xatom_label_idxs = find_CH_aromatic_idxs(mol, 
                                                                 patt=patt)
    
    #Xatom_label_idxs_rev = Xatom_label_idxs
    #print("1st Aviable substitute positions is %d" % len(Xatom_label_idxs))
    #print(Xatom_label_idxs)
    
    #print("Is len(Xatom_label_idxs) > max_subpos:  ",  len(Xatom_label_idxs) > max_subpos )
    if len(Xatom_label_idxs) > max_subpos:
        Xatom_label_idxs_rev = np.random.choice(Xatom_label_idxs, max_subpos, replace=False)

        Xatom_label_idxs = Xatom_label_idxs_rev.tolist()
    
    #print("2nd Aviable substitute positions is %d" % len(Xatom_label_idxs))
    #print(Xatom_label_idxs)        

    
    mutation_mol_tmp1 = replace_Xatom_by_dummy(mol, 
                                               original_label_symbol='c', 
                                               original_label_idxs=Xatom_label_idxs, 
                                               final_label_symbol='Pb', 
                                               replace_label_AtomicNum=82,
                                               #is_sanitizemol=False
                                               is_sanitizemol=True
                                               )
    
    
    
    rwmol = Chem.RWMol(mutation_mol_tmp1)
    rwmol.UpdatePropertyCache(strict=False)
    if is_showmol == True:
        Draw.ShowMol(rwmol, 
                     size=(800, 800), 
                     title="Intermediate Pb labeled mol"
                     )
    

    patt1 = Chem.MolFromSmarts('[Pb][H]') 
    hit_at1 = rwmol.GetSubstructMatches(patt1)
    
    
    #print("Removing termino H atoms adjacent to Pb atoms.")
    del_times = 1
    while len(hit_at1) > 0:
        
        #print("len(hit_at1) = ", len(hit_at1))
        #print(hit_at1[0])
    
        Pb_idx =  hit_at1[0][0]
        H_idx = hit_at1[0][1]
        
        rwmol.RemoveBond(Pb_idx, H_idx)
        rwmol.RemoveAtom(H_idx)
        
        #print("RemoveBond and RemoveAtom, del_times = %d" % del_times)
        #Draw.ShowMol(rwmol, size=(800, 800))
        #print(Chem.MolToSmiles(rwmol.GetMol()))
        
        del_times += 1
        hit_at1 = rwmol.GetSubstructMatches(patt1)
        
        
    
    
    mutation_mol = Chem.RemoveHs(Chem.Mol(rwmol) )
    
    if is_showmol == True:
        Draw.ShowMol(mutation_mol, 
                     size=(800, 800), 
                     title="Intermediate Pb labeled mol after removing H atoms"
                     )
    
    Pb_idxs = [i for i in range( mutation_mol.GetNumAtoms() ) if mutation_mol.GetAtomWithIdx(i).GetSymbol() == "Pb" ]
    mutation_mol = replace_Xatom_by_dummy(mutation_mol, 
                                        original_label_symbol='[Pb]', 
                                        original_label_idxs=Pb_idxs, 
                                        final_label_symbol='*', 
                                        replace_label_AtomicNum=0,
                                        is_sanitizemol=False
                                        #is_sanitizemol=True
                                        ) 
    
    #print("Template mol: \n", Chem.MolToSmiles(mutation_mol))
    
    if is_showmol == True:
        Draw.ShowMol(mutation_mol, 
                     size=(800, 800), 
                     title="Intermediate * labeled mol" 
                     )
    
    
    # dummy_idxs_new = [i for i in range( mutation_mol.GetNumAtoms() ) if mutation_mol.GetAtomWithIdx(i).GetSymbol() == "*" ]
    
    # for dummy_idx in dummy_idxs_new:
    #     dummy_atom_new =  mutation_mol.GetAtomWithIdx(dummy_idx)
    #     nbrs = dummy_atom_new.GetNeighbors()
    #     #dummy_nbrs = [nbr for nbr in nbrs if nbr.GetSymbol() == "*"]
        
    #     #print(dummy_idx, dummy_atom_new.GetSymbol() )
    #     for nbr in nbrs: 
    #     #for nbr in dummy_nbrs: 
            
    #         print( nbr.GetSymbol(),  mutation_mol.GetBondBetweenAtoms(nbr.GetIdx(), dummy_idx).GetBondType() )
            
    #         #print(  mutation_mol.GetBondBetweenAtoms(nbr.GetIdx(), dummy_idx).GetBondType() == Chem.BondType.SINGLE )
    #         #print(  mutation_mol.GetBondBetweenAtoms(nbr.GetIdx(), dummy_idx).GetBondType() == Chem.BondType.DOUBLE )
        #dummy_nbrs = [atom if atom.GetSymbol() == "*" for atom in nbrs]
    
    
    
    Dummy_idxs = [i for i in range( mutation_mol.GetNumAtoms() ) if mutation_mol.GetAtomWithIdx(i).GetSymbol() == "*" ]
    
    #print("Dummy_idxs: \n", Dummy_idxs)

    from itertools import combinations
    idxs_lists = sum([list(map(list, combinations(Dummy_idxs, i))) for i in range(len(Dummy_idxs) + 1)], [])
    
    #print('result_list =', idxs_lists)
    
    
    mutation_mols_tmp = []
    
    #print( sys._getframe().f_lineno )
    
    for idx_list in idxs_lists[:]:
        mutation_mol_rev = replace_Xatom_by_dummy(mutation_mol, 
                                                   original_label_symbol='*', 
                                                   original_label_idxs=idx_list, 
                                                   final_label_symbol=substitute_atom, 
                                                   replace_label_AtomicNum=substitute_atomnum, 
                                                   is_sanitizemol=False
                                                   )     
        
        mutation_mols_tmp.append(mutation_mol_rev)
    
    
    # print('-'*60)
    # for mol in mutation_mols_tmp:
    #     print(Chem.MolToSmiles(mol))
    
    mutation_mols = []
    #print( sys._getframe().f_lineno )
    
    mol_index = 1
    for mutation_mol1 in mutation_mols_tmp[1:]:
        Dummy_idxs1 = [i for i in range( mutation_mol1.GetNumAtoms() ) if mutation_mol1.GetAtomWithIdx(i).GetSymbol() == "*" ]
        
        mutation_mol_rev1 = replace_Xatom_by_dummy(mutation_mol1, 
                                                   original_label_symbol='*', 
                                                   original_label_idxs=Dummy_idxs1, 
                                                   final_label_symbol='Pb', 
                                                   replace_label_AtomicNum=82
                                                   )
        
        rwmol = Chem.RWMol(mutation_mol_rev1)
        rwmol.UpdatePropertyCache(strict=False)
        
        Pb_idxs = find_label_atom_idxs(rwmol, atom_symbol='Pb')
        
        #print("Pb_idxs = ", Pb_idxs)
        
        for Pb_idx in Pb_idxs:
            #Pb_atom = rwmol.GetAtomWithIdx(Pb_idx)
            H_idx = rwmol.AddAtom(Chem.Atom(1))
            rwmol.AddBond(Pb_idx, H_idx, Chem.BondType.SINGLE)
            #nbrs = dummy_atom.GetNeighbors()
            
        mutation_mol_rev2 = Chem.Mol(rwmol)
        
        
        #mutation_mol_rev3 = AllChem.RemoveHs( AllChem.AddHs(mutation_mol_rev2) )
        
        
        Pb_idxs1 = [i for i in range( mutation_mol_rev2.GetNumAtoms() ) if mutation_mol_rev2.GetAtomWithIdx(i).GetSymbol() == "Pb" ]
        mutation_mol_rev3 = replace_Xatom_by_dummy(mutation_mol_rev2, 
                                                   original_label_symbol='[Pb]', 
                                                   original_label_idxs=Pb_idxs1, 
                                                   final_label_symbol='C', 
                                                   replace_label_AtomicNum=6, 
                                                   #is_sanitizemol=False
                                                   ) 
        
        
        mutation_mol_rev4 = Chem.MolFromSmiles( Chem.MolToSmiles(mutation_mol_rev3) )
        
        #print("Molecule %d\n" % mol_index) 
        #print( Chem.MolToSmiles(mutation_mol_rev4) )
        if is_showmol == True:
            Draw.ShowMol(mutation_mol_rev4, 
                         size=(800, 800), 
                         title='Molecule_%d'%mol_index 
                         )
        
        AllChem.SanitizeMol(mutation_mol_rev4)
        mutation_mols.append(mutation_mol_rev4)
        
        mol_index += 1
        
    
    #rwmol.ReplaceAtom(4, Chem.Atom(7))

    comb_number = len(mutation_mols)
    subpos_number = len(Dummy_idxs)

    comb_number = comb_number_restriction(subpos_number, 
                                          substi_number,
                                          comb_number
                                          )
        
        
    mutation_mols = mutation_mols[:comb_number]
    

    if (sample_number >= 1) & (len(mutation_mols) >= sample_number):
        sample_indexs = np.random.choice(len(mutation_mols), sample_number, replace=False)
        
        mutation_mols = [mutation_mols[idx] for idx in sample_indexs]
        
    # else:
    #     print("Condition failed:  (sample_number >= 1) & (len(mutation_mols) >= sample_number) ")
    #     print("Do not do random sampling.")

    # print('-'*60)
    # print("The number of possible substitution positions is %d." % len(Dummy_idxs))
    # print("The number of possible combinations is %d." % ( pow(2, len(Dummy_idxs)) - 1) )
    # print("len(mutation_mols) = %d \n" % len(mutation_mols) )
    # print("The smiles of resultant molecules: ")
    # for mol in mutation_mols:
    #     print(Chem.MolToSmiles(mol))
        
    return mutation_mols



#------------------------------------------------------------------------------
def mutations_CH_aromatic_termino_H(mol, 
                                    patt=Chem.MolFromSmarts('c[H]'), 
                                    substitute_group=Chem.MolFromSmiles('*F'), 
                                    substi_number=0, 
                                    sample_number=0, 
                                    is_showmol=False,
                                    max_subpos=16
                                    ):
    '''
     This function can substitute the terminal H of the aromatic CH groups of molecule, 
     the substitution group is a smile whose substituent site is labelled by *, 
     e.g.   '*F'  for  -F, or  '*OC' for -OMe. 
     
     And, the return is the mutation_mols.
     
    Parameters
    ----------
    mol : TYPE
        DESCRIPTION.
    patt : TYPE, optional
        DESCRIPTION. The default is Chem.MolFromSmarts('c[H]').
    substitute_group : TYPE, optional
        DESCRIPTION. The default is Chem.MolFromSmiles('*F').
    substi_number : TYPE, optional
        DESCRIPTION. The default is 0.
    sample_number : TYPE, optional
        DESCRIPTION. The default is 0.
    is_showmol : TYPE, optional
        DESCRIPTION. The default is False.
    max_subpos : TYPE, optional
        DESCRIPTION. The default is 16.

    Returns
    -------
    mutation_mols : TYPE
        DESCRIPTION.

    '''

    import numpy as np
    #from scipy.special import comb
    
    #print("Original mol:\n", Chem.MolToSmiles(mol))
    if is_showmol == True:
        Draw.ShowMol(mol, 
                     size=(800, 800), 
                     title="Original mol"
                     )
    
    mol = Chem.AllChem.AddHs(mol)
    #print("Original mol after AddHs:\n ", Chem.MolToSmiles(mol))
    
    Xatom_label_idxs, H_Xatom_label_idxs = find_CH_aromatic_idxs(mol, 
                                                                 patt=patt)
    
    #Xatom_label_idxs_rev = Xatom_label_idxs
    #print("1st Aviable substitute positions is %d" % len(Xatom_label_idxs))
    #print(Xatom_label_idxs)
    
    #print("Is len(Xatom_label_idxs) > max_subpos:  ",  len(Xatom_label_idxs) > max_subpos )
    if len(Xatom_label_idxs) > max_subpos:
        Xatom_label_idxs_rev = np.random.choice(Xatom_label_idxs, max_subpos, replace=False)

        Xatom_label_idxs = Xatom_label_idxs_rev.tolist()
    
    #print("2nd Aviable substitute positions is %d" % len(Xatom_label_idxs))
    #print(Xatom_label_idxs)        

    
    mutation_mol_tmp1 = replace_Xatom_by_dummy(mol, 
                                               original_label_symbol='c', 
                                               original_label_idxs=Xatom_label_idxs, 
                                               final_label_symbol='Pb', 
                                               replace_label_AtomicNum=82,
                                               #is_sanitizemol=False
                                               is_sanitizemol=True
                                               )
    
    
    rwmol = Chem.RWMol(mutation_mol_tmp1)
    rwmol.UpdatePropertyCache(strict=False)
    
    if is_showmol == True:
        Draw.ShowMol(rwmol, 
                     size=(800, 800), 
                     title="Intermediate Pb labeled mol"
                     )
    

    patt1 = Chem.MolFromSmarts('[Pb][H]') 
    hit_at1 = rwmol.GetSubstructMatches(patt1)
    
    
    #print("Removing termino H atoms adjacent to Pb atoms.")
    del_times = 1
    while len(hit_at1) > 0:
        
        #print("len(hit_at1) = ", len(hit_at1))
        #print(hit_at1[0])
    
        Pb_idx =  hit_at1[0][0]
        H_idx = hit_at1[0][1]
        
        rwmol.RemoveBond(Pb_idx, H_idx)
        rwmol.RemoveAtom(H_idx)
        
        #print("RemoveBond and RemoveAtom, del_times = %d" % del_times)
        #Draw.ShowMol(rwmol, size=(800, 800))
        #print(Chem.MolToSmiles(rwmol.GetMol()))
        
        del_times += 1
        hit_at1 = rwmol.GetSubstructMatches(patt1)
        
    
    
    mutation_mol = Chem.RemoveHs(Chem.Mol(rwmol) )
    
    if is_showmol == True:
        Draw.ShowMol(mutation_mol, 
                     size=(800, 800), 
                     title="Intermediate Pb labeled mol after removing H atoms"
                     )
    
    Pb_idxs = [i for i in range( mutation_mol.GetNumAtoms() ) if mutation_mol.GetAtomWithIdx(i).GetSymbol() == "Pb" ]
    
    # for Pb_idx in Pb_idxs:
    #     Pb_atom =  mutation_mol.GetAtomWithIdx(Pb_idx)
    #     nbrs = Pb_atom.GetNeighbors()
    #     print(Pb_idx, Pb_atom.GetSymbol() )
    #     for nbr in nbrs: 
    #         print( nbr.GetSymbol(),  mutation_mol.GetBondBetweenAtoms(nbr.GetIdx(), Pb_idx).GetBondType() )
    #         #print(  mutation_mol.GetBondBetweenAtoms(nbr.GetIdx(), dummy_idx).GetBondType() == Chem.BondType.SINGLE )
            
    
    #print("Pb_idxs: \n", Pb_idxs)

    from itertools import combinations
    idxs_lists = sum([list(map(list, combinations(Pb_idxs, i))) for i in range(len(Pb_idxs) + 1)], [])
    
    #print('result_list =', idxs_lists)
    
    
    mutation_mols_tmp = []
    
    #print("mutation_mol: \n", Chem.MolToSmiles(mutation_mol) )
    #Draw.ShowMol(mutation_mol, size=(800, 800), title="mutation_mol")
    
    for idx_list in idxs_lists[:]:
        
        mutation_mol_rev1 = replace_Xatom_by_dummy(mutation_mol, 
                                                   original_label_symbol='Pb', 
                                                   original_label_idxs=idx_list, 
                                                   final_label_symbol='C', 
                                                   replace_label_AtomicNum=6
                                                   )
        
        #print("mutation_mol_rev1: \n", Chem.MolToSmiles(mutation_mol_rev1) )
        #Draw.ShowMol(mutation_mol_rev1, size=(800, 800), title="mutation_mol_rev1")
        
        rwmol1 = Chem.RWMol(mutation_mol_rev1)
        rwmol1.UpdatePropertyCache(strict=False)
        
        C_idxs = list( set(Pb_idxs).intersection( set(idx_list) )   ) 
        
        # print("Pb_idxs = ", Pb_idxs)
        # print("idx_list = ", idx_list)
        # print("C_idxs = ", C_idxs)
        
        if len(C_idxs) > 0:
            for C_idx in C_idxs:
                #Pb_atom = rwmol.GetAtomWithIdx(Pb_idx)
                H_idx = rwmol1.AddAtom(Chem.Atom(1))
                rwmol1.AddBond(C_idx, H_idx, Chem.BondType.SINGLE)
        
        mutation_mol_rev2 = Chem.Mol(rwmol1)
        
        #print("mutation_mol_rev2: \n", Chem.MolToSmiles(mutation_mol_rev2) )
        #Draw.ShowMol(mutation_mol_rev2, size=(800, 800), title="mutation_mol_rev2")
        
        
        dummy_idx_subgrp = find_label_atom_idx(substitute_group, atom_symbol='*')
        
        mutation_mol_star_substitute_group = Chem.ReplaceSubstructs(mutation_mol_rev2, 
                                                                    Chem.MolFromSmarts('[#82]'), 
                                                                    substitute_group, 
                                                                    replaceAll=True,
                                                                    replacementConnectionPoint=dummy_idx_subgrp 
                                                                    )
        
        #print("mutation_mol_star_substitute_group[0]: \n", Chem.MolToSmiles(mutation_mol_star_substitute_group[0])  )
        #Draw.ShowMol(mutation_mol_star_substitute_group[0], size=(800, 800), title="mutation_mol_star_substitute_group[0]")

        dummy_idxs_mutation_mol = find_label_atom_idxs( mutation_mol_star_substitute_group[0], atom_symbol='*')
        
        mutation_mol_rev3 = replace_Xatom_by_dummy(mutation_mol_star_substitute_group[0], 
                                                   original_label_symbol='*', 
                                                   original_label_idxs=dummy_idxs_mutation_mol, 
                                                   final_label_symbol='C', 
                                                   replace_label_AtomicNum=6
                                                   )
        
        #print("mutation_mol_rev3: \n", Chem.MolToSmiles(mutation_mol_rev3) )
        #Draw.ShowMol(mutation_mol_rev3, size=(800, 800), title="mutation_mol_rev3")

        mutation_mols_tmp.append( mutation_mol_rev3 )    

    
    mutation_mols = []
    
    mutation_mols_tmp.reverse()
    
    mol_index = 1
    for mutation_mol1 in mutation_mols_tmp[1:]:

        #mutation_mol1 = AllChem.RemoveAllHs(mutation_mol)
        AllChem.SanitizeMol(mutation_mol1)
        
        mutation_mol2 = Chem.MolFromSmiles( Chem.MolToSmiles( mutation_mol1 ) ) 
        #print("Molecule %d\n" % mol_index) 
        #print( Chem.MolToSmiles(mutation_mol2) )
        if is_showmol == True:
            Draw.ShowMol(mutation_mol2, 
                         size=(800, 800), 
                         title='Molecule_%d'%mol_index 
                         )
        
        mutation_mols.append( mutation_mol2 )
        
        mol_index += 1
        
    
    comb_number = len(mutation_mols)
    subpos_number = len(Pb_idxs)
    
    comb_number = comb_number_restriction(subpos_number, 
                                          substi_number,
                                          comb_number
                                          )
        
        
    mutation_mols = mutation_mols[:comb_number]
    

    if (sample_number >= 1) & (len(mutation_mols) >= sample_number):
        sample_indexs = np.random.choice(len(mutation_mols), sample_number, replace=False)
        
        mutation_mols = [mutation_mols[idx] for idx in sample_indexs]
        

    # print('-'*60)
    # print("The number of possible substitution positions is %d." % len(Pb_idxs))
    # print("The number of possible combinations is %d." % ( pow(2, len(Pb_idxs)) - 1) )
    # print("len(mutation_mols) = %d \n" % len(mutation_mols) )
    # print("The smiles of resultant molecules: ")
    # for mol in mutation_mols:
    #     print(Chem.MolToSmiles(mol))


    return mutation_mols


#----------------------------------------------------------------------------------------
def mutual_mutations_mol(BASE_MOL,
                         CARBON_SUB='N',
                         TERMINO_HYDROGEN_SUB='*F',
                         MAX_SUBPOS=16,
                         SUBSTI_NUMBER_CARBON=0,
                         SAMPLE_NUMBER_CARBON=0,  
                         SUBSTI_NUMBER_HYDROGEN=0,
                         SAMPLE_NUMBER_HYDROGEN=0,                     
                         ):


    mols_N = []
    mols_N +=  [ BASE_MOL ]
    mutation_mols_N = mutations_CH_aromatic(BASE_MOL, 
                                          patt=Chem.MolFromSmarts('c[H]'), 
                                          substitute_atom=CARBON_SUB,
                                          substitute_atomnum=7, 
                                          substi_number=SUBSTI_NUMBER_CARBON, 
                                          sample_number=SAMPLE_NUMBER_CARBON, 
                                          # is_showmol=True, 
                                          max_subpos=MAX_SUBPOS
                                          )
    
    mols_N +=  mutation_mols_N   
    # print("The length of mols_N is : ", len(mols_N))
    mols_N  =  delete_repeated_smiles_of_mols(mols_N)
    # print("After delete_repeated_smiles_of_mols, the length of mols_N is : ", len(mols_N))
     
    All_mols = []
    for tmp_mol1 in mols_N:
        All_mols += [ tmp_mol1 ]
        mutation_mols1 = mutations_CH_aromatic_termino_H(tmp_mol1, 
                                                        patt=Chem.MolFromSmarts('c[H]'), 
                                                        substitute_group=Chem.MolFromSmiles( TERMINO_HYDROGEN_SUB ), 
                                                        substi_number=SUBSTI_NUMBER_HYDROGEN, 
                                                        sample_number=SAMPLE_NUMBER_HYDROGEN, 
                                                        # is_showmol=True,
                                                        max_subpos=MAX_SUBPOS
                                                        )
        
        All_mols +=  mutation_mols1    
        
        
    # print("The length of All_mols is : ", len(All_mols ))
    All_mols = delete_repeated_smiles_of_mols(All_mols )
    # print("After delete_repeated_smiles_of_mols, the length of All_mols is : ", len(All_mols ))
    
    All_mols_smis = [ Chem.MolToSmiles(mol) for mol in All_mols ]
    All_mols_smis = list( set(All_mols_smis) )
    sorted( All_mols_smis )
    
    All_mols = [ Chem.MolFromSmiles(smi) for smi in  All_mols_smis ]
    
    # print("\nThe smiles for All_mols are:")
    # for i, smi in zip(range(len(All_mols_smis)), All_mols_smis):
    #     print(i, " ", smi)
    
    
    return All_mols


def mutual_mutations_mols(BASE_MOLS,
                          CARBON_SUB='N',
                          TERMINO_HYDROGEN_SUB='*F',
                          MAX_SUBPOS=16,
                          SUBSTI_NUMBER_CARBON=0,
                          SAMPLE_NUMBER_CARBON=0,  
                          SUBSTI_NUMBER_HYDROGEN=0,
                          SAMPLE_NUMBER_HYDROGEN=0,                     
                          ):

    All_mols_global = []
    
    for BASE_MOL, i in zip(BASE_MOLS, range(len(BASE_MOLS))):

        print("Treat BASE_MOL %d"%i)                
        
        mols_N = []
        mols_N +=  [ BASE_MOL ]
        mutation_mols_N = mutations_CH_aromatic(BASE_MOL, 
                                                patt=Chem.MolFromSmarts('c[H]'), 
                                                substitute_atom=CARBON_SUB,
                                                substitute_atomnum=7, 
                                                substi_number=SUBSTI_NUMBER_CARBON, 
                                                sample_number=SAMPLE_NUMBER_CARBON, 
                                                # is_showmol=True, 
                                                max_subpos=MAX_SUBPOS
                                                )
        
        mols_N +=  mutation_mols_N   
        # print("The length of mols_N is : ", len(mols_N))
        mols_N  =  delete_repeated_smiles_of_mols(mols_N)
        # print("After delete_repeated_smiles_of_mols, the length of mols_N is : ", len(mols_N))
         
        All_mols = []
        for tmp_mol1 in mols_N:
            All_mols += [ tmp_mol1 ]
            mutation_mols1 = mutations_CH_aromatic_termino_H(tmp_mol1, 
                                                             patt=Chem.MolFromSmarts('c[H]'), 
                                                             substitute_group=Chem.MolFromSmiles( TERMINO_HYDROGEN_SUB ), 
                                                             substi_number=SUBSTI_NUMBER_HYDROGEN, 
                                                             sample_number=SAMPLE_NUMBER_HYDROGEN, 
                                                             # is_showmol=True,
                                                             max_subpos=MAX_SUBPOS
                                                             )
            
            All_mols +=  mutation_mols1    
            
            
        # print("The length of All_mols is : ", len(All_mols ))
        All_mols = delete_repeated_smiles_of_mols(All_mols )
        print("After delete_repeated_smiles_of_mols, the length of All_mols is : ", len(All_mols ))
        
        All_mols_smis = [ Chem.MolToSmiles(mol) for mol in All_mols ]
        All_mols_smis = list( set(All_mols_smis) )
        sorted( All_mols_smis )
        
        All_mols = [ Chem.MolFromSmiles(smi) for smi in  All_mols_smis ]
        
        # print("\nThe smiles for All_mols are:")
        # for i, smi in zip(range(len(All_mols_smis)), All_mols_smis):
        #     print(i, " ", smi)
    
    
        All_mols_global += All_mols


    All_mols_global = delete_repeated_smiles_of_mols( All_mols_global )
    print("After delete_repeated_smiles_of_mols, the length of All_mols_global is : ", len(All_mols_global))
    
    All_mols_global_smis = [ Chem.MolToSmiles(mol) for mol in All_mols_global ]
    All_mols_global_smis = list( set(All_mols_global_smis) )
    sorted( All_mols_global_smis )
    
    All_mols_global = [ Chem.MolFromSmiles(smi) for smi in  All_mols_global_smis ]

    # print("\nThe smiles for All_mols_global are:")
    # for i, smi in zip(range(len(All_mols_global_smis)), All_mols_global_smis):
    #     print(i, " ", smi)

    
    return All_mols_global


#-----------------------------------------------------------------------------
def get_dummylabels_heavyatomnum(mols, dummylabels, isReturnMasIndex=False):
    import re
    dummylabels1_nums = []
    heavyatoms_nums = []
    for mol1 in mols:
        heavyatoms_num = mol1.GetNumAtoms()
        #dummylabels0_pattern = re.compile( str(dummylabels[0]) + '*', re.MULTILINE|re.DOTALL )
        dummylabels1_pattern = re.compile( str(dummylabels[1]) + '*', re.MULTILINE|re.DOTALL )
        mol_smi = Chem.MolToSmiles( mol1 )
        #dummylabels0_num = dummylabels0_pattern.findall(mol_smi)
        dummylabels1_num = dummylabels1_pattern.findall(mol_smi)
        #print("len(dummylabels0_num) = ", len(dummylabels0_num) )
        
        print("len(dummylabels1_num) = ", len(dummylabels1_num),  ",  heavyatoms_num = ", heavyatoms_num)
        
        dummylabels1_nums.append( len(dummylabels1_num) )
        heavyatoms_nums.append( heavyatoms_num )
        
    dummylabels1_mums_max_idx = dummylabels1_nums.index(max(dummylabels1_nums))
    heavyatoms_nums_max_idx = heavyatoms_nums.index(max(heavyatoms_nums))
    
    if isReturnMasIndex == False:
        return dummylabels1_nums, heavyatoms_nums
    else:
        return dummylabels1_nums, heavyatoms_nums, dummylabels1_mums_max_idx, heavyatoms_nums_max_idx

#------------------------------------------------------------------------------
def debranch_CR_aromatic(mol, 
                          patt=Chem.MolFromSmarts('[a&R]-[A&!#1]'), 
                          dummylabels=(11111, 22222),
                          substi_atom="H", 
                          substi_atomnum=1, 
                          debranch_number=0, 
                          sample_number=0, 
                          is_showmol=False,
                          max_debranchpos=10
                        ):
    '''
      This function can do the flowing transformation: 
      C-R  -->  C-* + *-R
      where C is an aromatic atom in a ring, R is a substitution group 
      (begined with noaromatic atom) connected with the aromatic C atom via a single bond.
      Only, the C-* part is retained, and the *-R part gets discard.
     
      And, the return is the mutation_mols.
     
    Parameters
    ----------
    mol : TYPE
        DESCRIPTION.
    patt : TYPE, optional
        DESCRIPTION. The default is Chem.MolFromSmarts('[a&R]-A').
    debranch_number : TYPE, optional
        DESCRIPTION. The default is 0.
    sample_number : TYPE, optional
        DESCRIPTION. The default is 0.
    is_showmol : TYPE, optional
        DESCRIPTION. The default is False.
    max_debranchpos : TYPE, optional
        DESCRIPTION. The default is 10.

    Returns
    -------
    mutation_mols : TYPE
        DESCRIPTION.

    '''

    import numpy as np
#    from scipy.special import comb
    from itertools import combinations
    
    mol_origin = mol
    #mol = Chem.AllChem.AddHs(mol)
    #print("Original mol after AddHs:\n ", Chem.MolToSmiles(mol))


    #---- user defined labels ----------------------------------- 
    bondatoms_idxs = mol.GetSubstructMatches( patt )
    if (len(bondatoms_idxs) >= 1):
        print("matched bonds:\n", bondatoms_idxs)
        
        if len(bondatoms_idxs) > max_debranchpos:
            bis_idxs = np.random.choice( len(bondatoms_idxs), max_debranchpos, replace=False)
            bis_idxs = bis_idxs.tolist()
            bondatoms_idxs_new = [ bondatoms_idxs[idx] for idx in bis_idxs ]
            print("len(bondatoms_idxs_new)", len(bondatoms_idxs_new))
            bondatoms_idxs = bondatoms_idxs_new
        else:
            print("len(bondatoms_idxs) > max_debranchpos is False.")
        

        print("The restricted matched bonds:\n", bondatoms_idxs)
        print("len(bondatoms_idxs) = %d:\n" % len(bondatoms_idxs) )
        
        bonds = []
        labels = []
        for bondatoms_idx in bondatoms_idxs:
            bond_tmp = mol.GetBondBetweenAtoms(bondatoms_idx[0], bondatoms_idx[1])
            if bond_tmp.GetBeginAtomIdx() == bondatoms_idx[0]:
                labels.append( dummylabels )
            else:
                dummylabels_reverse = (dummylabels[1], dummylabels[0])
                labels.append(  dummylabels_reverse )
            bonds.append(bond_tmp.GetIdx())
        
        
        print("bond indexs:")
        print(bonds)
        
        print("labels:")
        print(labels)
        
        #--- correlate bonds, labels, via a dict --------------------------
        bonds_labels_dict = dict(map(lambda x,y:[x, y], bonds, labels))
        
        print("bonds_labels_dict:")
        print( bonds_labels_dict )
        
        mutation_mols = []

        bond_idxs_lists = sum([list(map(list, combinations(bonds, i))) for i in range(len(bonds) + 1)], [])

        print("len(bond_idxs_lists) = ", len(bond_idxs_lists))
        
        # for bond_idxs_list in bond_idxs_lists:
        #     print(bond_idxs_list)

        print(" ")
        for bond_idxs_list in bond_idxs_lists[1:]:
            print("-"*80)
            #print("bond_idxs_list = " ) 
            print( bond_idxs_list )
            labels_tmp = [ bonds_labels_dict[x]  for x in bond_idxs_list]
            #print("labels_tmp = ", labels_tmp)
            
            nm = Chem.FragmentOnBonds(mol, bond_idxs_list, dummyLabels=labels_tmp)
            #print("Fragemetal mol with dummylabels:\n", Chem.MolToSmiles(nm, True) )
            
            mols = list(  Chem.GetMolFrags(nm, asMols=True) )
            
            #dummylabels1_nums, heavyatoms_nums = get_dummylabels_heavyatomnum(mols, dummylabels, isReturnMasIndex=False)
            dummylabels1_nums, heavyatoms_nums, dummylabels1_mums_max_idx, heavyatoms_nums_max_idx = get_dummylabels_heavyatomnum(mols, dummylabels, isReturnMasIndex=True)
            
            print("Largest Fragement mol according to heavyatoms_nums_max_idx:")
            print(heavyatoms_nums_max_idx, "   ", Chem.MolToSmiles( mols[heavyatoms_nums_max_idx]) )
            
            print("Largest Fragement mol according to dummylabels1_mums_max_idx:")
            print(dummylabels1_mums_max_idx, "   ", Chem.MolToSmiles( mols[dummylabels1_mums_max_idx]) )
            
            #mol_chosen = mols[0]
            mol_chosen = mols[heavyatoms_nums_max_idx]
            
            dummy_idxs = [i for i in range( mol_chosen.GetNumAtoms() ) if mol_chosen.GetAtomWithIdx(i).GetSymbol() == '*' ]
            mol_rev = replace_Xatom_by_dummy(mol_chosen, 
                                              original_label_symbol='*', 
                                              original_label_idxs=dummy_idxs, 
                                              final_label_symbol=substi_atom, 
                                              replace_label_AtomicNum=substi_atomnum, 
                                              is_sanitizemol=False
                                              )
            
            #print("After replacing * by H atom, mol_rev:")
            #print(Chem.MolToSmiles( mol_rev) )
            
            mol_rev1 = AllChem.RemoveAllHs( mol_rev )
            #print("After RemoveAllHs, mol_rev1:")
            print(Chem.MolToSmiles( mol_rev1))
            
            
            #mutation_mols += [ mols[0],  mol_rev, mol_rev1 ]
            mutation_mols += [ mol_rev1 ]
            

        #------ restrict on return how many samples ---------------------------
        comb_number = len(mutation_mols)
        subpos_number = len(bonds)
        
        comb_number = comb_number_restriction(subpos_number, 
                                              debranch_number,
                                              comb_number
                                              )
            
            
        mutation_mols = mutation_mols[:comb_number]
        
    
        if (sample_number >= 1) & (len(mutation_mols) >= sample_number):
            sample_indexs = np.random.choice(len(mutation_mols), sample_number, replace=False)
            
            mutation_mols = [mutation_mols[idx] for idx in sample_indexs]  
        
        
        print('-'*60)
        print("The number of possible debranch positions is %d." % len(bonds))
        print("The number of possible combinations is %d." % ( pow(2, len(bonds)) - 1) )
        
            
    else:
        print("len(bondatoms_idxs) >= 1 failed.")
        mutation_mols = [ mol ]
        

    print('-'*60)
    print("With restriction on max_debranchpos, debranch_number, sample_number")
    print("len(mutation_mols) = %d \n" % len(mutation_mols) )
    print("The smiles of resultant molecules: ")
    for mol in mutation_mols:
        print(Chem.MolToSmiles(mol))    


    #print("Original mol:\n", Chem.MolToSmiles(mol))
    if is_showmol == True:
        Draw.ShowMol(mol_origin, 
                      size=(800, 800), 
                      title="Original mol"
                      )

        for mol, i in zip( mutation_mols, range(len(mutation_mols)) ):
            Draw.ShowMol(mol, 
                          size=(800, 800), 
                          title="mol #%8d"%( i + 1)
                          )


    return mutation_mols


#-----------------------------------------------------------------------------
def mutations_N_to_CH_aromatic(mol, 
                               patt=Chem.MolFromSmarts('[n&R]'), 
                               substitute_group=Chem.MolFromSmarts('C-[H]'),
                               substi_site_symbol='C',
                               substi_number=0, 
                               sample_number=0, 
                               is_showmol=False,
                               max_subpos=10
                               ):
    '''
     This function can do the flowing transformation: 
     N  -->  C-H
     where N is an aromatic atom in a ring, 
     replaced by aromatic C-H atoms.
     
     And, the return is the mutation_mols.
     
    Parameters
    ----------
    mol : TYPE
        DESCRIPTION.
    patt : TYPE, optional
        DESCRIPTION. The default is Chem.MolFromSmarts('[n&R]-A').
    substi_number : TYPE, optional
        DESCRIPTION. The default is 0.
    sample_number : TYPE, optional
        DESCRIPTION. The default is 0.
    is_showmol : TYPE, optional
        DESCRIPTION. The default is False.
    max_subpos : TYPE, optional
        DESCRIPTION. The default is 10.

    Returns
    -------
    mutation_mols : TYPE
        DESCRIPTION.

    '''

    import numpy as np
    #from scipy.special import comb
    from itertools import combinations
    
    mol_origin = mol
    #mol = Chem.AllChem.AddHs(mol)
    #print("Original mol after AddHs:\n ", Chem.MolToSmiles(mol))

    # if is_showmol == True:
    #     Draw.ShowMol(mol_origin, 
    #                  size=(800, 800), 
    #                  title="Original mol"
    #                  )

    #---- user defined labels ----------------------------------- 
    natom_idxs = mol.GetSubstructMatches( patt )
    natom_idxs = [ x[0] for x in natom_idxs]
    
    if (len(natom_idxs) >= 1):
        print("matched bonds:\n", natom_idxs)
        
        if len(natom_idxs) > max_subpos:
            n_idxs = np.random.choice( len(natom_idxs), max_subpos, replace=False)
            n_idxs = n_idxs.tolist()
            natom_idxs_new = [ natom_idxs[idx] for idx in n_idxs ]
            print("len(natom_idxs_new)", len(natom_idxs_new))
            natom_idxs = natom_idxs_new
            natom_idxs.sort()
        else:
            print("len(natom_idxs) > max_subpos is False.")
        

        print("The restricted matched atoms:\n", natom_idxs)
        print("len(natom_idxs) = %d:\n" % len(natom_idxs) )
        
        
        print("matched atom, ExplicitValence, GetIsAromatic")
        for natom_idx_1 in natom_idxs:
            print( natom_idx_1, mol.GetAtomWithIdx(natom_idx_1).GetExplicitValence(), mol.GetAtomWithIdx(natom_idx_1).GetIsAromatic(),  )
        
        
        
        mutation_mols = []

        atom_idxs_lists = sum([list(map(list, combinations(natom_idxs, i))) for i in range(len(natom_idxs) + 1)], [])

        print("len(atom_idxs_lists) = ", len(atom_idxs_lists))
        
        for atom_idxs_list in atom_idxs_lists:
            print(atom_idxs_list)

        print(" ")
        for atom_idxs_list in atom_idxs_lists[1:]:
            # print("-"*80)
            # print("atom_idxs_list = " ) 
            # print( atom_idxs_list )
            
            #mol = AllChem.AddHs( mol )
            
            mol_rev = replace_Xatom_by_dummy(mol, 
                                             original_label_symbol='N', 
                                             original_label_idxs=atom_idxs_list, 
                                             final_label_symbol='*', 
                                             replace_label_AtomicNum=0, 
                                             #is_sanitizemol=True
                                             )

            
            # print("dummy atom ExplicitValence")
            # for i in range(mol_rev.GetNumAtoms()):
            #     #print(i, mol_rev.GetAtomWithIdx(i).GetExplicitValence() )
            #     if mol_rev.GetAtomWithIdx(i).GetSymbol() == '*':
            #         print(i, mol_rev.GetAtomWithIdx(i).GetExplicitValence() )
            
                    
            dummy_idx_subgrp = find_label_atom_idx(substitute_group, atom_symbol=substi_site_symbol)
        
            mol_rev1 = Chem.ReplaceSubstructs(mol_rev, 
                                              query=Chem.MolFromSmarts('[#0]'), 
                                              replacement=substitute_group, 
                                              replaceAll=True,
                                              replacementConnectionPoint=dummy_idx_subgrp
                                              )
            
            
            if mol_rev1[0] is not None:
                mol_rev2 = mol_rev1[0]
                Chem.SanitizeMol(mol_rev2)
                mol_rev3 = Chem.MolFromSmiles( Chem.CanonSmiles(  Chem.MolToSmiles(mol_rev2) ) ) 
                mutation_mols += [  mol_rev3 ]
                     

        #------ restrict on return how many samples ---------------------------
        comb_number = len(mutation_mols)
        subpos_number = len(natom_idxs)
    
        comb_number = comb_number_restriction(subpos_number, 
                                              substi_number,
                                              comb_number
                                              )
            
            
        mutation_mols = mutation_mols[:comb_number]
        
    
        if (sample_number >= 1) & (len(mutation_mols) >= sample_number):
            sample_indexs = np.random.choice(len(mutation_mols), sample_number, replace=False)
            
            mutation_mols = [mutation_mols[idx] for idx in sample_indexs]  
        
        
        print('-'*60)
        print("The number of possible substitution positions is %d." % len(natom_idxs))
        print("The number of possible combinations is %d." % ( pow(2, len(natom_idxs)) - 1) )
        
            
    else:
        print("len(natom_idxs) >= 1 failed.")
        mutation_mols = [ mol ]
        

    print('-'*60)
    print("With restriction on max_subpos, substi_number, sample_number")
    print("len(mutation_mols) = %d \n" % len(mutation_mols) )
    print("The smiles of resultant molecules: ")
    for mol in mutation_mols:
        print(Chem.MolToSmiles(mol))    


    #print("Original mol:\n", Chem.MolToSmiles(mol))
    if is_showmol == True:
        Draw.ShowMol(mol_origin, 
                     size=(800, 800), 
                     title="Original mol"
                     )

        for mol1, i in zip( mutation_mols, range(len(mutation_mols)) ):
            Draw.ShowMol(mol1, 
                         size=(800, 800), 
                         title="mol #%8d"%( i + 1)
                         )


    return mutation_mols





#*********************************************************************************
#-----__main__ function begins here ----------------------------------------------
#---------------------------------------------------------------------------------
if __name__ == '__main__':

    print("Begins")
    print("-"*80)

    
#     #---- test on OrganoMetals2P2_Enumeration( )------------------------------   
#     ligandA_smis = [
#                     'C1=CC=[N+]4C2=C1C=CC3=C2[N+](=CC=C3)[*]4', \
#                     'C1=CC=[N+]4C2=C1C=C(C3=C2[N+](=C(C(=C3[I])[Br])[Cl])[*]4)[At]', \
#                     'C1(=C(C(=[N+]4C2=C1C(=C(C3=C2[N+](=C(C(=C3[I])[Br])[Cl])[*]4)[At])[At])[Cl])[Br])[I]', \
#                     # 'C1=CC=[N+]4C2=C1C5=C(C3=C2[N+](=CC=C3)[*]4)C=CC=C5', \
#                     # 'C1(=C(C(=[N+]4C2=C1C5=C(C3=C2[N+](=CC=C3)[*]4)C=CC(=C5[At])[Li])[Cl])[Br])[I]', \
#                     # 'C1(=C(C(=[N+]4C2=C1C5=C(C3=C2[N+](=C(C(=C3[I])[Br])[Cl])[*]4)C(=C(C(=C5[At])[Li])[Li])[At])Cl)Br)I'
#                     ]
        
    
#     ligandB_smis = [
#                     'C1=[N+]3[N](C=C1)[B-]([N]2C=CC=[N+]2[Po]3)([H])[H]', \
#                     'C1=[N+]3[N](C=C1)[B-]([N]2C=CC=[N+]2[Po]3)(C)C', \
#                     'C1=[N+]3[N](C=C1)[B-]([N]2C=CC=[N+]2[Po]3)([N]4C=CC=[N]4)[N]5C=CC=[N]5', \
#                     # 'C1=[N+]3[N](C=C1)[B-]([N]2C=CC=[N+]2[Po]3)(C4=CC=CC=C4)C5=CC=CC=C5', \
#                     # '[B-]2(C1=[N+](C=CC=C1)[Po][N+]3=C2C=CC=C3)([H])[H]', \
#                     # '[B-]2(C1=[N+](C=CC=C1)[Po][N+]3=C2C=CC=C3)(C)C'
#                     ]
    
#     organometal_smis = ligandA_smis + ligandB_smis
#     organometal_mols = [Chem.MolFromSmiles(smi) for smi in organometal_smis]
#     draw_mols(organometal_mols, len(organometal_mols), './images/OM/foo--organometalic-mols-frags.png', molsPerRow=4, size=(800, 800))
    
#     organometal_neutrals = OrganoMetals2P2_Enumeration(ligandA_smis, 
#                                                         ligandB_smis, 
#                                                         metal_smis=['[Cu+]', '[Ag+]'], 
#                                                         #verbse=True,
#                                                         )
    
#     organometal_cations = OrganoMetals2P2_Enumeration_diagonalonly(ligandA_smis, 
#                                                                     metal_smis=['[Cu+]', '[Ag+]'], 
#                                                                     verbse=False)
    
#     organometals = organometal_cations  +  organometal_neutrals
    
    
    
#     #organometals_rev = set_dative_bonds_batch(organometals, fromAtoms=(7, 8))
    
#     draw_mols(organometal_neutrals, 
#               16, 
#               './images/OM/foo--organometalic-mols-2P2-neutrals.png', 
#               molsPerRow=4, 
#               size=(800, 800))
    
#     draw_mols(organometal_cations, 
#               16, 
#               './images/OM/foo--organometalic-mols-2P2-cations.png', 
#               molsPerRow=4, 
#               size=(800, 800))

    
# # =============================================================================
# #     draw_mols(organometals_rev, 
# #           9, 
# #           './images/OM/foo--organometalic-mols-2P2-dativebonds.png', 
# #           molsPerRow=3, 
# #           size=(800, 800))
# # =============================================================================
    
#     #Draw.ShowMol(organometals[0], size=(600, 600))
#     #Draw.ShowMol(organometals_dativebonds[0], size=(600, 600))
    

# #---- test on OrganoMetals2P1_Enumeration( )------------------------------
#     # ligandA_smis = ['C15=CC=CC=C1OC2=C(C=CC=C2)[P](C3=CC=CC=C3)(C4=CC=CC=C4)[*][P]5(C6=CC=CC=C6)C7=CC=CC=C7',\
#     #                 'C1=CC=[N+]4C2=C1C=CC3=C2[N+](=CC=C3)[*]4', \
#     #                 'NCCCC1=CC=[N+]4C2=C1C=CC3=C2[N+](=CC=C3)[*]4', \
#     #                     'OCCCC1=CC=[P]4C2=C1C=CC3=C2[P](=CC=C3)[*]4']
    
#     # ligandB_smis = ['C1=CC=C[N]1[Po]', \
#     #                 'NCCCC1=CC=C[N]1[Po]', \
#     #                     'OCCCC1=CC=C[N]1[Po]'] 
    

    
#     # organometals2P1 = OrganoMetals2P1_Enumeration(ligandA_smis, 
#     #                                             ligandB_smis, 
#     #                                             metal_smis=['[Cu]', '[Ag]'],
#     #                                             #verbse=True,
#     #                                             )
    
#     # #organometals2P1_rev = set_dative_bonds_batch(organometals2P1, fromAtoms=(7, 8))
    
#     # draw_mols(organometals2P1, 
#     #           16, 
#     #           './images/OM/foo--organometalic-mols-2P1.png', 
#     #           molsPerRow=4, 
#     #           size=(800, 800)
#     #           )
    
# # =============================================================================
# #     draw_mols(organometals2P1_rev, 
# #               9, 
# #               './images/OM/foo--organometalic-mols-2P1-dativebonds.png', 
# #               molsPerRow=3, 
# #               size=(800, 800)
# #               )
# # =============================================================================
    


#     #all_mols = organometals  + organometals2P1
#     all_mols = organometals 
#     #all_mols = organometal_cations
#     #all_mols = organometal_neutrals
    
#     cpd_names = [ "cpd-%05d" % (i+1) for i in range(len(all_mols)) ]
#     for mol, cpd_name in zip(all_mols, cpd_names):
#         mol.SetProp("_Name", cpd_name )
    
# # =============================================================================
# #     print('-'*60)
# #     print(Chem.MolToMolBlock(all_mols[0]) )
# # =============================================================================

#     print('-'*60)
#     print("len(organometal_cation) is ",  len(organometal_cations))
#     print("len(organometal_neutrals) is ",  len(organometal_neutrals))
#     #print("len(organometals2P1) is ",  len(organometals2P1))
#     print("len(all_mols) is ",  len(all_mols))
    
    
#     # print("*"*60)
#     # print("Begin paralell write molcules.")
#     # write_mols_paralell(all_mols, cpd_names)
    
    
    
#     #--------------------------------------------------------------------------
#     #--------  treating substitutions 
#     #print("Chem.MolToSmiles(all_mols[0]) is  %s \n", Chem.MolToSmiles(all_mols[0]) )
#     #D_A_Enumeration_new()
    
    
#     print("\n# Is c-X bond exist?")
    
#     OM_FullSubstitution_mols = []
    
    
#     ligandB_smis_hindrances = [
#                 '[Po]C', 
#                 #'[Po]CC', \
#                 '[Po]CCC', \
#                 #'[Po]CCCC', \
#                 #'[Po]CCCCC', \
#                 '[Po]CCCCCC' 
#                 ] 

    
#     ligandB_smis_donoracceptors = [ \
#                 '[Po]F', \
#                 'C(#N)[Po]', \
#                 #'[N+](=O)([O-])[Po]', \
#                 'CN(C)[Po]', \
#                 'O([Po])C', \
#                 #'S(C)[Po]'
#                 ]
    
        
#     sub1s_list = ["Cl", "Br"]
#     sub2s_list = ["Cl", "Br", "I", "At", "Li", "Na"]
    
#     for mol in all_mols[:]:
#         for sub1 in sub1s_list:
#             for sub2 in sub2s_list:
#                 if sub1 == sub2:
#                     onemol_sub1_sub2_mols_combin = []
#                 else:
#                     onemol_sub1_sub2_mols_combin = accumulation_sub1_sub2(mol, 
#                                                             ligandB_smis_hindrances, 
#                                                             ligandB_smis_donoracceptors, 
#                                                             atom_symbol1=sub1, 
#                                                             atom_symbol2=sub2)
                    
#                 OM_FullSubstitution_mols += onemol_sub1_sub2_mols_combin
        
        
       
#     print('*'*80)    
#     print("len(OM_FullSubstitution_mols) = %8d \n" % len(OM_FullSubstitution_mols) )

#     OM_FullSubstitution_mols = delete_repeated_smiles_of_mols(OM_FullSubstitution_mols)

#     print("len(OM_FullSubstitution_mols) = %8d \n" % len(OM_FullSubstitution_mols) )

#     print('*'*80)
#     for mol in OM_FullSubstitution_mols[:30]:
#         print(Chem.MolToSmiles(mol))
        

#     # for mol in OM_FullSubstitution_mols[:30]:
#     #     Draw.ShowMol(mol, size=(800, 800))



#-----------------------------------------------------------------------------
#--- test on mutations_CH_aromatic() -----------------------------------------
#-----------------------------------------------------------------------------

    print("\n", '*'*80)
    print("Test on mutations_CH_aromatic()")
    #mol = Chem.MolFromSmiles('C1=CC=CC(=C1)CCCC(C)C')
    
    #------- problemetic mol.  -----------------------
    #mol = Chem.MolFromSmiles( 'C1=CC=CC2=C1C=C[N]2' )
    
    mol = Chem.MolFromSmiles( 'C1=CC=CC2=C1C=CN2' )
    
    #mol = Chem.MolFromSmiles( 'C1=CC=CC2=C1C=CO2' )
    #mol = Chem.MolFromSmiles( 'C1=CC=CC2=C1C=CS2' )
    #mol = Chem.MolFromSmiles( 'C1=CC=CC2=C1C=C[Se]2' )
    #mol = Chem.MolFromSmiles( 'C1=CC=CC(=C1)CCC2=COC=C2' )
    
    #mol = Chem.MolFromSmiles( 'C1=CC=CC3=C1C2=C(C=CC=C2)O3' )
    #mol = Chem.MolFromSmiles( 'C1=CC=CC3=C1C2=C(C=CC=C2)N3' )
    #mol = Chem.MolFromSmiles( 'C1=CC=NC3=C1C2=C(C=CC=C2)O3' )
    #mol = Chem.MolFromSmiles( 'C1=NC=NC3=C1C2=C(C=CC=C2)N3' )
    #mol = Chem.MolFromSmiles( 'C1=C3C(=[N]C=[N]1)C2=C[N]=C[N]=C2O3' )
    #mol = Chem.MolFromSmiles( 'C1=C3C(=[N]C=[N]1)C2=C[N]=CC=C2O3' )
    #mol = Chem.MolFromSmiles( 'C1=CC=C2C(=C1)C3=CC=CC=C3O2' )
    
    
    #mol = OM_FullSubstitution_mols[0]
    
    
    mutation_mols = mutations_CH_aromatic(mol, 
                                          patt=Chem.MolFromSmarts('c[H]'), 
                                          substitute_atom="N",
                                          substitute_atomnum=7, 
                                          substi_number=0, 
                                          sample_number=0, 
                                          #is_showmol=True, 
                                          #max_subpos=3
                                          )
    
    
    # mutation_mols =  mutations_CH_aromatic(mol, 
    #                                       patt=Chem.MolFromSmarts('c[H]'), 
    #                                       substitute_atom="N", 
    #                                       substitute_atomnum=7, 
    #                                       substi_number=0, 
    #                                       sample_number=0
    #                                       )
    
    # mutation_mols =  mutations_CH_aromatic(mol, 
    #                                       patt=Chem.MolFromSmarts('c[H]'), 
    #                                       substitute_atom="N", 
    #                                       substitute_atomnum=7, 
    #                                       substi_number=3, 
    #                                       sample_number=0
    #                                       )





#-----------------------------------------------------------------------------
#--- test on mutations_CH_aromatic_termino_H() -----------------------------------------
#-----------------------------------------------------------------------------

    print("\n", '*'*80)
    print("Test on mutations_CH_aromatic_termino_H()")
    
    #mol = Chem.MolFromSmiles('C1=CC=CC(=C1)CCCC(C)C')
    
    #mol = Chem.MolFromSmiles( 'C1=CC=CC2=C1C=C[N]2' )
    
    #mol = Chem.MolFromSmiles( 'C1=CC=CC2=C1C=CN2' )
    
    #mol = Chem.MolFromSmiles( 'C1=CC=CC3=C1C2=C(C=CC=C2)O3' )
    
    mol = mutation_mols[8]


    mutation_mols1 = mutations_CH_aromatic_termino_H(mol, 
                                                    patt=Chem.MolFromSmarts('c[H]'), 
                                                    substitute_group=Chem.MolFromSmiles('*F'), 
                                                    substi_number=0, 
                                                    sample_number=0, 
                                                    is_showmol=True,
                                                    max_subpos=16
                                                    )
    
    
    
    #all_mols = [ mol ] + mutation_mols
    all_mols = mutation_mols1

    
    # for mol in all_mols[:]:
    #     Draw.ShowMol(mol, size=(800, 800))
    

    #indexs1 = np.random.choice(20, 10, replace=False)
    #indexs2 = np.random.randint(0, 20, size=10)



#-----------------------------------------------------------------------------
#--- test on mutations_CH_aromatic_termino_H() -----------------------------------------
#-----------------------------------------------------------------------------

    print("\n", '*'*80)
    print("Test on debranch_CR_aromatic()" )
    
    #mol = Chem.MolFromSmiles('C1=CC=CC(=C1)CCCC(C)C')
    
    #mol = Chem.MolFromSmiles( 'C1=CC=CC2=C1C=C[N]2' )
    
    #mol = Chem.MolFromSmiles( 'C1=CC=CC2=C1C=CN2' )
    
    #mol = Chem.MolFromSmiles( 'C1=CC=CC3=C1C2=C(C=CC=C2)O3' )
    #mol = Chem.MolFromSmiles( 'C1=CC=CC3=C1C2=C(C=CC=C2)N3' )
    #mol = Chem.MolFromSmiles( 'C1=CC=CC3=C1C2=C(C=CC=C2)[NH]3' )
    mol = Chem.MolFromSmiles( 'C1=C(C=CC3=C1C2=C(C=CC(=C2)C)[N]3C(C4=C[N]=CC=C4)C)C' )
    
    #mol = Chem.MolFromSmiles( 'C1(=C(C(=C(C(=C1CC)C)C#N)C2=CC=CC=C2)N(C)C)' )
    #mol = Chem.MolFromSmiles( 'C1=C(C(=C(C(=C1CC(C2=CC=CC=C2)C3=CC=CC=C3)CC4=CC=CC=C4)C#N)C5=CC(=CC=C5)C6=CC=CC=C6)N(C)C' )
    #mol = Chem.MolFromSmiles( 'C1=CC(=CC(=C1)CCC(C2=CC(=[N]C=C2)CC)[N]3C=C(C(=C3)CC)CC)CC' )
    #mol = Chem.MolFromSmiles( 'CC(C1=CC(=[N]C=C1)CC)[N]2C=C(C(=C2)CC)CC' )

    mutation_mols = debranch_CR_aromatic(mol, 
                                         patt=Chem.MolFromSmarts('[a&R]-[A&!#1,a&!#1]'),      #patt=Chem.MolFromSmarts('[a&R]-[A&!#1,a&!#1]'),  
                                         dummylabels=(11111, 22222),
                                         substitute_atom="F", 
                                         substitute_atomnum=9, 
                                         debranch_number=0, 
                                         sample_number=0, 
                                         is_showmol=True,   #False,
                                         max_debranchpos=10
                                        )
    
    
    
    all_mols = [ mol ] + mutation_mols
    #all_mols = mutation_mols

    
    # for mol in all_mols[:]:
    #     Draw.ShowMol(mol, size=(800, 800))


#-----------------------------------------------------------------------------
#--- test on mutations_N_to_CH_aromatic() -----------------------------------------
#-----------------------------------------------------------------------------

    print("\n", '*'*80)
    print("Test on mutations_N_to_CH_aromatic()")

    #mol = Chem.MolFromSmiles('C2(=[N]C1=C([N]=C(N1)CC)[N]=N2)CC')
    #mol = Chem.MolFromSmiles( 'C1=C(C=CC3=C1C2=C(C=CC(=C2)C)[N]3C(C4=C[N]=CC=C4)C)C' )
    #mol = Chem.MolFromSmiles( 'C1=C(C)[N]=CC3=C1C2=C(C=CC(=[N]2)C)[N]3C(C4=CN=CC=C4)CN5C(CCC5)C[N]' )
    mol = Chem.MolFromSmiles( 'C2=C(CC1CC[N]=C1)N=CC4=C2C3=C(C=CC(=N3)C)[N]4C(C5=CN=CC=C5)CN6C(CNC6)CN' )
    
    mutation_mols = mutations_N_to_CH_aromatic(mol, 
                                                patt=Chem.MolFromSmarts('[n&R&H0,N&R&H0,N&R&H1]'), 
                                                #patt=Chem.MolFromSmarts('[n&R&H0,N&R&H0]'),  
                                                #patt=Chem.MolFromSmarts('[n&R&H0]'),  
                                                #patt=Chem.MolFromSmarts('[n&R]'),  
                                                #patt=Chem.MolFromSmarts('[n&R&H0,N&R]'), 
                                                substitute_group=Chem.MolFromSmarts('C-[H]'),
                                                substi_site_symbol='C',
                                                substi_number=1, 
                                                sample_number=0, 
                                                is_showmol=True,
                                                #is_showmol=False,
                                                max_subpos=10
                                                )
    
    
    
    all_mols = [ mol ] + mutation_mols
    #all_mols = mutation_mols


    # for mol in all_mols[:]:
    #     Draw.ShowMol(mol, size=(800, 800))
    
    
    # for mol in all_mols[:]:
    #     print( Chem.MolToSmiles(mol) )
    




    print("\nFinished!")
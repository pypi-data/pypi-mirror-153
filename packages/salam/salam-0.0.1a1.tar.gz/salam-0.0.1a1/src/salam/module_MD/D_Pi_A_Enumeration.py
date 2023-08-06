#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 10:14:03 2021

Sidechain-Core Enumeration:

#1. D_Pi_A_Enumeration(cores1_smis, chains_smis, cores2_smis, verbse=False)
Return the combinational molecular library as a list of rdkit molecules,
cores1_chains_cores2

Examples of args:
    cores1_smis = ['*[n+]1cc[nH]c1', '[n+]1c(*)c[nH]c1', '[n+]1cc[nH]c1(*)']
    chains_smis = ['C[Po]', 'CC[Po]', 'CCC[Po]'] 
    cores2_smis = ['[n+]1ccccc1C(=O)O', 'c1cnccc1C(=O)O', 'c1ccncc1C(=O)O']

Note: 1. Frag core1 must have only 1 position label by [#0];
      2. Frag chain must replace the [#0] atom in core1 from left ending, 
         and the right ending is labeled by [Po] atom;
      3. Frag core2 must replace the [Po] atom in core1_chain to form core1_chain_core2.

By restrict that the frags have 1 and only 1 attaching points, 
we make things simple and controlable.

#2. Cores_Chains_Enumeration(cores_smis, chains_smis, verbse=False)
Return:
    cores_chains

Examples of args:
    cores_smis = ['*[n+]1cc[nH]c1', '[n+]1c(*)c[nH]c1', '[n+]1cc[nH]c1(*)']
    chains_smis = ['C[Po]', 'CC[Po]', 'CCC[Po]'] 


#3. Cores_Chains_Enumeration_FullSubstitute(cores_smis, chains_smis, verbse=False)
Return: full subsitituted version of molecules. 
    cores_chains

Examples of args:
    cores_smis = ['*[n+]1c(*)c[nH]c1(*)', 'n1cc(*)[nH]c1(*)']
    chains_smis = ['CN', 'CCN', 'CCCN'] 
    
#4. D_A_Enumeration_new(ligandA_smis, ligandB_smis, verbse=False)

#5. D_Pi_A_Enumeration_new(ligandA_smis, pi_bridge_smis, ligandB_smis, verbse=False)

#6. D_A_D_Enumeration_new(donor_smis, acceptorAsPiBridge_smis, verbse=False)

#7. D_Pi_A_Enumeration_new_exchange_pibridge_dummy_po(ligandA_smis, pi_bridge_smis, ligandB_smis, verbse=False)

#8. D_A_D_Enumeration_new_exchange_acceptoraspibridge_dummy_po(donor_smis, acceptorAsPiBridge_smis, verbse=False)


@author: tucy
"""

from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
from rdkit import RDLogger
import numpy as np

import subprocess
import time
from joblib import Parallel, delayed
from tqdm import tqdm

RDLogger.DisableLog('rdApp.*') 


#-----------------------------------------------------------------------------
def delete_repeated_smiles_of_mols(mols):
    '''
    delete the repeated smiles within a list of molecules.
    
    Parameters
    ----------
    mols : list of rdkit mols
        DESCRIPTION.

    Returns
    -------
    mols_rev : list of rdkit mols
        DESCRIPTION.

    '''
    mols_smis = [Chem.MolToSmiles(mol) for mol in  mols]
    mols_smis_list = list( set(mols_smis) )
    mols_rev = [Chem.MolFromSmiles(smi) for smi in  mols_smis_list]    
    return mols_rev


def find_label_atom_idx(ligand, atom_symbol='*'):
    atom_idx = 0
    for i in range( ligand.GetNumAtoms() ) :
        #print( i, ligand.GetAtomWithIdx(i).GetSymbol() ) 
        if ligand.GetAtomWithIdx(i).GetSymbol() == atom_symbol:
            atom_idx = i
    return atom_idx


def find_label_atom_idxs(ligand, atom_symbol='*'):
    atom_idxs = []
    for i in range( ligand.GetNumAtoms() ) :
        #print( i, ligand.GetAtomWithIdx(i).GetSymbol() ) 
        if ligand.GetAtomWithIdx(i).GetSymbol() == atom_symbol:
            #atom_idx = i
            atom_idxs.append(i)
    return atom_idxs



def delete_label_atom(mol, delete_atom_symbol='Po'):
    rwmol = Chem.RWMol(mol)
    rwmol.UpdatePropertyCache(strict=False)
    
    Po_idx = find_label_atom_idx(rwmol, atom_symbol=delete_atom_symbol)
    #print("Po_idx = ", Po_idx)
    
    Po_atom = rwmol.GetAtomWithIdx(Po_idx)

    nbrs = Po_atom.GetNeighbors()
    #print("Po_atom.GetNeighbors() are: ", Po_atom.GetNeighbors() )
    if len(nbrs) >= 2:
        left_atom_idx = nbrs[0].GetIdx()
        right_atom_idx = nbrs[1].GetIdx()
        rwmol.RemoveBond(left_atom_idx, Po_idx)
        rwmol.RemoveBond(right_atom_idx, Po_idx)
        rwmol.AddBond(left_atom_idx, right_atom_idx, Chem.BondType.SINGLE)
        rwmol.RemoveAtom(Po_idx)
        
    return Chem.Mol(rwmol)


def delete_label_atoms(mol, delete_atom_symbol='Po'):
    rwmol = Chem.RWMol(mol)
    rwmol.UpdatePropertyCache(strict=False)
    
    Po_idxs = find_label_atom_idxs(rwmol, atom_symbol=delete_atom_symbol)
    #print("Po_idx = ", Po_idx)
    
    for Po_idx in Po_idxs:
        Po_atom = rwmol.GetAtomWithIdx(Po_idx)
    
        nbrs = Po_atom.GetNeighbors()
        #print("Po_atom.GetNeighbors() are: ", Po_atom.GetNeighbors() )
        if len(nbrs) >= 2:
            left_atom_idx = nbrs[0].GetIdx()
            right_atom_idx = nbrs[1].GetIdx()
            rwmol.RemoveBond(left_atom_idx, Po_idx)
            rwmol.RemoveBond(right_atom_idx, Po_idx)
            rwmol.AddBond(left_atom_idx, right_atom_idx, Chem.BondType.SINGLE)
            rwmol.RemoveAtom(Po_idx)
        
    return Chem.Mol(rwmol)


def delete_label_atoms_new(mol, delete_atom_symbol='Po'):
    rwmol = Chem.RWMol(mol)
    rwmol.UpdatePropertyCache(strict=False)
    
    Po_idxs = find_label_atom_idxs(rwmol, atom_symbol=delete_atom_symbol)
    
    if (len(Po_idxs) >= 1):
        for i in range( len(Po_idxs) ):
            rwmol = delete_label_atom(rwmol, delete_atom_symbol='Po')
        
    return Chem.Mol(rwmol)



# =============================================================================
# def delete_label_atoms(mol, delete_atom_symbol='Po'):
#     rwmol = Chem.RWMol(mol)
#     rwmol.UpdatePropertyCache(strict=False)
#     
#     Po_idxs = find_label_atom_idxs(rwmol, atom_symbol=delete_atom_symbol)
#     print("atline133  Po_idxs = ", Po_idxs)
# 
#     for Po_idx in Po_idxs:
#         Po_atom = rwmol.GetAtomWithIdx(Po_idx)
#         nbrs = Po_atom.GetNeighbors()
#         #print("Po_atom.GetNeighbors() are: ", Po_atom.GetNeighbors() )
#         if len(nbrs) >= 2:
#             left_atom_idx = nbrs[0].GetIdx()
#             right_atom_idx = nbrs[1].GetIdx()
#             rwmol.RemoveBond(left_atom_idx, Po_idx)
#             rwmol.RemoveBond(right_atom_idx, Po_idx)
#             rwmol.AddBond(left_atom_idx, right_atom_idx, Chem.BondType.SINGLE)
#             rwmol.RemoveAtom(Po_idx)
#         
#     return Chem.Mol(rwmol)
# =============================================================================


def exchange_dummy_and_Po_label_idx(mol, label_atom1_symbol='*', label_atom2_symbol='Po'):
    label_atom1_idx = find_label_atom_idx(mol, atom_symbol=label_atom1_symbol)
    label_atom2_idx = find_label_atom_idx(mol, atom_symbol=label_atom2_symbol)
    
    if label_atom1_symbol == '*' and label_atom2_symbol == 'Po':    
        label_atom1_AtomicNum = 0
        label_atom2_AtomicNum = 84
    else:
        label_atom1_AtomicNum = 84
        label_atom2_AtomicNum = 0
    
    #print("label_atom1_symbol, label_atom2_symbol, label_atom1_idx, label_atom2_idx, label_atom2_AtomicNum, label_atom1_AtomicNum : ")
    #print(label_atom1_symbol, label_atom2_symbol, label_atom1_idx, label_atom2_idx, label_atom1_AtomicNum, label_atom2_AtomicNum)
    
    mol.GetAtomWithIdx(label_atom1_idx).SetAtomicNum(label_atom2_AtomicNum)
    mol.GetAtomWithIdx(label_atom2_idx).SetAtomicNum(label_atom1_AtomicNum)
    Chem.SanitizeMol(mol)


def replace_dummy_by_Po_label(mol, original_label_symbol='*', final_label_symbol='Po', reverse=False):
    original_label_idx = find_label_atom_idx(mol, atom_symbol=original_label_symbol)
    
    if reverse == False:    
        replace_label_AtomicNum = 84
    else:
        replace_label_AtomicNum = 0
    
    mol.GetAtomWithIdx(original_label_idx).SetAtomicNum(replace_label_AtomicNum)
    Chem.SanitizeMol(mol)


def draw_mols(mols, nb_mols=9, file_name='./foo-gridimage-mols.png', molsPerRow=4, size=(400, 400), legends=None):
    # Compute2DCoords for dipection
    for mol in mols[:nb_mols]:
        AllChem.Compute2DCoords(mol)
    
    # View the enumerated molecules: ---------------------------------------------
    img = Draw.MolsToGridImage(
                               mols[:nb_mols], 
                               molsPerRow=molsPerRow, 
                               subImgSize=size,
                               legends=legends,
                               ) 
    img.save(file_name)
    
    img.close()


#------------------------------------------------------------------------------
def D_Pi_A_Enumeration(cores1_smis, chains_smis, cores2_smis, verbse=False):
    cores1 = [Chem.MolFromSmiles(smi) for smi in cores1_smis]
    chains = [Chem.MolFromSmiles(smi) for smi in chains_smis] 
    # [Te] or [Po] divalent element for subsquent substitution 
    cores2 = [Chem.MolFromSmiles(smi) for smi in cores2_smis]
    
    cores1_chains = []
    for core1 in cores1:
        for chain in chains:
            core1_chain = Chem.ReplaceSubstructs(core1, Chem.MolFromSmarts('[#0]'), chain)
            cores1_chains.append(core1_chain[0])
    
    cores1_chains_cores2 = []
    
    for core2  in cores2:
        for core1_chain in cores1_chains: 
            core1_chain_core2 = Chem.ReplaceSubstructs(core1_chain, Chem.MolFromSmarts('[Po]'), core2)
            cores1_chains_cores2.append(core1_chain_core2[0])    
    
    for mol in cores1_chains_cores2:
        Chem.SanitizeMol(mol)
    
    if verbse:
        print("# info on D_Pi_A_Enumeration( )")
        print("\n# cores1 :")
        for mol in cores1:
            print(Chem.MolToSmiles(mol))         
        
        print("\n# chains :")
        for mol in chains:
            print(Chem.MolToSmiles(mol)) 
            
        print("\n# cores2 :")
        for mol in cores2:
            print(Chem.MolToSmiles(mol)) 
            
        print("\n# cores1_chains :")
        for mol in cores1_chains:
            print(Chem.MolToSmiles(mol)) 
        
        print("\nThe product cores1_chains_cores2 molecules are: ")
        print("-"*80)
        for mol in cores1_chains_cores2:
            print(Chem.MolToSmiles(mol)) 

        print("-"*80)
        print("# The lens of cores1, chains, cores2, cores1_chains, cores1_chains_cores2 are:")  
        print(len(cores1), len(chains), len(cores2), len(cores1_chains), len(cores1_chains_cores2) )  

    return delete_repeated_smiles_of_mols(cores1_chains_cores2) 


def Cores_Chains_Enumeration(cores_smis, chains_smis, verbse=False):
    cores = [Chem.MolFromSmiles(smi) for smi in cores_smis]
    chains = [Chem.MolFromSmiles(smi) for smi in chains_smis] 
    
    cores_chains = []
    for core1 in cores:
        for chain in chains:
            core1_chain = Chem.ReplaceSubstructs(core1, Chem.MolFromSmarts('[#0]'), chain)
            cores_chains.append(core1_chain[0])
    
    for mol in cores_chains:
        Chem.SanitizeMol(mol)
    
    if verbse:
        print("# info on Cores_Chains_Enumeration( )")
        print("\n# cores :")
        for mol in cores:
            print(Chem.MolToSmiles(mol))         
        
        print("\n# chains :")
        for mol in chains:
            print(Chem.MolToSmiles(mol)) 
                 
        print("\nThe product cores_chains molecules are: ")
        print("-"*80)
        for mol in cores_chains:
            print(Chem.MolToSmiles(mol)) 

        print("-"*80)
        print("# The lens of cores, chains, cores_chains are:")  
        print(len(cores), len(chains), len(cores_chains) )  

    return delete_repeated_smiles_of_mols(cores_chains) 


def Cores_Chains_Enumeration_FullSubstitute(cores_smis, chains_smis, verbse=False):
    cores = [Chem.MolFromSmiles(smi) for smi in cores_smis]
    chains = [Chem.MolFromSmiles(smi) for smi in chains_smis] 
    
    cores_chains = []
    for core in cores:
        for chain in chains:
            core_chain = Chem.ReplaceSubstructs(core, Chem.MolFromSmarts('[#0]'), chain, True)
            cores_chains.append(core_chain[0])
    
    for mol in cores_chains:
        Chem.SanitizeMol(mol)
    
    if verbse:
        print("# info on Cores_Chains_Enumeration_FullSubstitute( )")
        print("\n# cores :")
        for mol in cores:
            print(Chem.MolToSmiles(mol))         
        
        print("\n# chains :")
        for mol in chains:
            print(Chem.MolToSmiles(mol)) 
                 
        print("\nThe product core_chains molecules are: ")
        print("-"*80)
        for mol in cores_chains:
            print(Chem.MolToSmiles(mol)) 

        print("-"*80)
        print("# The lens of cores, chains, core_chains are:")  
        print(len(cores), len(chains), len(cores_chains) )  

    return delete_repeated_smiles_of_mols(cores_chains) 


#------------------------------------------------------------------------------
def D_A_Enumeration_new(ligandA_smis, ligandB_smis, verbse=False):
    '''
    This function can return the combined chemical compound library on condition that 
    Donors and Acceptors are given via args ligandA_smis and ligandB_smis, and 
    the substitution position of Donor is labeled by [*], meanwhile Acceptor by [Po].

    Parameters
    ----------
    ligandA_smis : list of smiles.
        DESCRIPTION.
    ligandB_smis : list of smiles.
        DESCRIPTION.
    verbse : logical, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    DA_mols : list of rdkit mol. 
        DESCRIPTION.

    '''
    ligandAs = [Chem.MolFromSmiles(smi) for smi in ligandA_smis]
    ligandBs = [Chem.MolFromSmiles(smi) for smi in ligandB_smis]
    
    ligandAs_Po_ligandBs = []
    
    for ligandA in ligandAs:
        for ligandB in ligandBs:
            
            Po_idx = find_label_atom_idx(ligandB, atom_symbol='Po')
            
            ligandA_Po_ligandB = Chem.ReplaceSubstructs(ligandA, 
                                                        Chem.MolFromSmarts('[#0]'), 
                                                        ligandB, 
                                                        replacementConnectionPoint=Po_idx )
            ligandAs_Po_ligandBs.append(ligandA_Po_ligandB[0])
    
    DA_mols = []
    
    for mol in ligandAs_Po_ligandBs:
        mol_rev = delete_label_atom(mol, delete_atom_symbol='Po')
        DA_mols.append(mol_rev)
    

    for mol in DA_mols:
        Chem.SanitizeMol(mol)
    
    if verbse:
        print("# info on DA_Enumeration_new( )")
        print("\n# ligandAs :")
        for mol in ligandAs:
            print(Chem.MolToSmiles(mol))         
        
        print("\n# ligandBs :")
        for mol in ligandBs:
            print(Chem.MolToSmiles(mol))
                 
        print("\n#The product D_A molecules are: ")
        print("-"*80)
        for mol in DA_mols:
            print(Chem.MolToSmiles(mol)) 

        print("-"*80)
        print("# The lens of ligandAs, ligandBs, DA_mols are:")  
        print(len(ligandAs), len(ligandBs), len(DA_mols) )  

    return delete_repeated_smiles_of_mols(DA_mols)


def D_A_Enumeration_new_FullSubstitute(ligandA_smis, ligandB_smis, verbse=False):
    '''
    This function can return the combined chemical compound library on condition that 
    Donors and Acceptors are given via args ligandA_smis and ligandB_smis, and 
    the substitution position of Donor is labeled by [*], meanwhile Acceptor by [Po].

    Parameters
    ----------
    ligandA_smis : list of smiles.
        DESCRIPTION.
    ligandB_smis : list of smiles.
        DESCRIPTION.
    verbse : logical, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    DA_mols : list of rdkit mol. 
        DESCRIPTION.

    '''
    ligandAs = [Chem.MolFromSmiles(smi) for smi in ligandA_smis]
    ligandBs = [Chem.MolFromSmiles(smi) for smi in ligandB_smis]
    
    ligandAs_Po_ligandBs = []
    
    for ligandA in ligandAs:
        for ligandB in ligandBs:
            
            Po_idx = find_label_atom_idx(ligandB, atom_symbol='Po')
            
            ligandA_Po_ligandB = Chem.ReplaceSubstructs(ligandA, 
                                                        Chem.MolFromSmarts('[#0]'), 
                                                        ligandB, 
                                                        replaceAll=True,
                                                        replacementConnectionPoint=Po_idx )
            ligandAs_Po_ligandBs.append(ligandA_Po_ligandB[0])
    
    DA_mols = []
    
    for mol in ligandAs_Po_ligandBs:
        #mol_rev = delete_label_atoms(mol, delete_atom_symbol='Po')
        mol_rev = delete_label_atoms_new(mol, delete_atom_symbol='Po')
        DA_mols.append(mol_rev)
    

    for mol in DA_mols:
        Chem.SanitizeMol(mol)
    
    if verbse:
        print("# info on DA_Enumeration_new( )")
        print("\n# ligandAs :")
        for mol in ligandAs:
            print(Chem.MolToSmiles(mol))         
        
        print("\n# ligandBs :")
        for mol in ligandBs:
            print(Chem.MolToSmiles(mol))
                 
        print("\n#The product D_A molecules are: ")
        print("-"*80)
        for mol in DA_mols:
            print(Chem.MolToSmiles(mol)) 

        print("-"*80)
        print("# The lens of ligandAs, ligandBs, DA_mols are:")  
        print(len(ligandAs), len(ligandBs), len(DA_mols) )  

    return delete_repeated_smiles_of_mols(DA_mols)





def D_Pi_A_Enumeration_new(ligandA_smis, pi_bridge_smis, ligandB_smis, verbse=False):
    '''
    This function can return the combined chemical compound library on condition that 
    Donors, Pi_bridges and Acceptors are given via args ligandA_smis, pi_bridge_smis and ligandB_smis, 
    and the substitution position of 
    Donor is labeled by [*], 
    Pi_bridge by [Po]--pi-bridge--[*],
    meanwhile Acceptor by [Po].

    Parameters
    ----------
    ligandA_smis : list of smiles.
        DESCRIPTION.
    pi_bridge_smis : list of smiles.
        DESCRIPTION.
    ligandB_smis : list of smiles.
        DESCRIPTION.
    verbse : logical, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    DPiA_mols : list of rdkit mol. 
        DESCRIPTION.

    '''
    ligandAs = [Chem.MolFromSmiles(smi) for smi in ligandA_smis]
    pi_bridges = [Chem.MolFromSmiles(smi) for smi in pi_bridge_smis]
    ligandBs = [Chem.MolFromSmiles(smi) for smi in ligandB_smis]
    
    #---- create ligandAs_pi_bridges provided ligandAs ('*') and pi_bridges ('Po'---'*'), 
    #-----ligandAs_pi_bridges also have label atom [*] for further substitution
    ligandAs_Po_pi_bridges = []
    
    for ligandA in ligandAs:
        for pi_bridge in pi_bridges:
            Po_idx = find_label_atom_idx(pi_bridge, atom_symbol='Po')
            
            ligandA_Po_pi_bridge = Chem.ReplaceSubstructs(ligandA, 
                                                        Chem.MolFromSmarts('[#0]'), 
                                                        pi_bridge, 
                                                        replacementConnectionPoint=Po_idx )
            ligandAs_Po_pi_bridges.append(ligandA_Po_pi_bridge[0])
    
    ligandAs_pi_bridges = []
    
    for mol in ligandAs_Po_pi_bridges:
        mol_rev = delete_label_atom(mol, delete_atom_symbol='Po')
        ligandAs_pi_bridges.append(mol_rev)
    
    #---- create DPiA_mols provided ligandAs_Po_pi_bridges ('*') and ligandBs ('Po')
    ligandAs_pi_bridges_Po_ligandBs = []
    
    for ligandA_pi_bridge in ligandAs_pi_bridges:
        for ligandB in ligandBs:
            Po_idx = find_label_atom_idx(ligandB, atom_symbol='Po')
            
            ligandA_pi_bridge_Po_ligandB = Chem.ReplaceSubstructs(ligandA_pi_bridge, 
                                                        Chem.MolFromSmarts('[#0]'), 
                                                        ligandB, 
                                                        replacementConnectionPoint=Po_idx )
            ligandAs_pi_bridges_Po_ligandBs.append(ligandA_pi_bridge_Po_ligandB[0])
    
    DPiA_mols = []
    
    for mol in ligandAs_pi_bridges_Po_ligandBs:
        mol_rev = delete_label_atom(mol, delete_atom_symbol='Po')
        DPiA_mols.append(mol_rev)
    
    #----- Sanitize mols ------
    for mol in DPiA_mols:
        Chem.SanitizeMol(mol)
    
    if verbse:
        print("# info on D_Pi_A_Enumeration_new( )")
        print("\n# ligandAs :")
        for mol in ligandAs:
            print(Chem.MolToSmiles(mol))      
            
        print("\n# pi_bridges :")
        for mol in pi_bridges:
            print(Chem.MolToSmiles(mol))
        
        print("\n# ligandBs :")
        for mol in ligandBs:
            print(Chem.MolToSmiles(mol))
                 
        print("\n#The product D_Pi_A molecules are: ")
        print("-"*80)
        for mol in DPiA_mols:
            print(Chem.MolToSmiles(mol)) 

        print("-"*80)
        print("# The lens of ligandAs, ligandBs, pi_bridges, DPiA_mols are:")  
        print(len(ligandAs), len(ligandBs), len(pi_bridges), len(DPiA_mols) )  

    return delete_repeated_smiles_of_mols(DPiA_mols) 


def D_A_D_Enumeration_new(donor_smis, acceptorAsPiBridge_smis, verbse=False):
    '''
    This function can return the combined chemical compound library on condition that 
    Donors, acceptorAsPiBridge are given via args donor_smis, acceptorAsPiBridge_smis, 
    and the substitution position of 
    1st Donor is labeled by [*], 
    Pi_bridge by [Po]--pi-bridge--[*]

    Parameters
    ----------
    donor_smis : list of smiles.
        DESCRIPTION.
    acceptorAsPiBridge_smis : list of smiles.
        DESCRIPTION.
    verbse : logical, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    DPiA_mols : list of rdkit mol. 
        DESCRIPTION.

    '''
    
    donors_2 = [ Chem.MolFromSmiles(smi) for smi in donor_smis ]
    for donor in donors_2:
        replace_dummy_by_Po_label(donor, original_label_symbol='*', final_label_symbol='Po')
        
    donor_2_smis = [Chem.MolToSmiles(mol)  for mol in donors_2]    
    DAD_mols = D_Pi_A_Enumeration_new(donor_smis, acceptorAsPiBridge_smis, donor_2_smis, verbse=verbse)
    
    return DAD_mols


def D_Pi_A_Enumeration_new_exchange_pibridge_dummy_po(ligandA_smis, pi_bridge_smis, ligandB_smis, verbse=False):
    pi_bridges_exchange = [Chem.MolFromSmiles(smi) for smi in pi_bridge_smis]
    for mol in pi_bridges_exchange:
        exchange_dummy_and_Po_label_idx(mol, label_atom1_symbol='*', label_atom2_symbol='Po')
    pi_bridge_smis_exchange = [ Chem.MolToSmiles(mol)  for mol in  pi_bridges_exchange]
    
    return D_Pi_A_Enumeration_new(ligandA_smis, pi_bridge_smis_exchange, ligandB_smis, verbse=verbse)


def D_A_D_Enumeration_new_exchange_acceptoraspibridge_dummy_po(donor_smis, acceptorAsPiBridge_smis, verbse=False):
    acceptorAsPiBridges_exchange = [Chem.MolFromSmiles(smi) for smi in acceptorAsPiBridge_smis]
    for mol in acceptorAsPiBridges_exchange:
        exchange_dummy_and_Po_label_idx(mol, label_atom1_symbol='*', label_atom2_symbol='Po')
    acceptorAsPiBridge_smis_exchange = [ Chem.MolToSmiles(mol)  for mol in  acceptorAsPiBridges_exchange]
    
    return D_A_D_Enumeration_new(donor_smis, acceptorAsPiBridge_smis_exchange, verbse=verbse)


def D3_A_Enumeration_new(ligandA_smis, ligandB_smis, verbse=False):
    '''
    This function can return the combined chemical compound library on condition that 
    Donors and Acceptors are given via args ligandA_smis and ligandB_smis, and 
    the substitution position of Donor is labeled by [*], meanwhile Acceptor by three [Po].

    Parameters
    ----------
    ligandA_smis : list of smiles.
        DESCRIPTION.
    ligandB_smis : list of smiles.
        DESCRIPTION.
    verbse : logical, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    D3A_mols : list of rdkit mol. 
        DESCRIPTION.

    '''
    ligandAs = [Chem.MolFromSmiles(smi) for smi in ligandA_smis]
    ligandBs = [Chem.MolFromSmiles(smi) for smi in ligandB_smis]
    
    D3_dummy_A_mols = []
    for ligandB in ligandBs:
        for ligandA in ligandAs:
            dummy_idx = find_label_atom_idx(ligandA, atom_symbol='*')
            D3_dummy_A = Chem.ReplaceSubstructs(ligandB, 
                                                Chem.MolFromSmarts('[Po]'), 
                                                ligandA, 
                                                replaceAll=True,
                                                replacementConnectionPoint=dummy_idx, 
                                                )
        
            D3_dummy_A_mols.append(D3_dummy_A[0])
    
    D3A_mols = []
    
    for mol in D3_dummy_A_mols:
        mol_rev1 = delete_label_atom(mol, delete_atom_symbol='*')
        mol_rev2 = delete_label_atom(mol_rev1, delete_atom_symbol='*')
        mol_rev3 = delete_label_atom(mol_rev2, delete_atom_symbol='*')
        D3A_mols.append(mol_rev3)
    

    for mol in D3A_mols:
        Chem.SanitizeMol(mol)
    
    if verbse:
        print("# info on D3_A_Enumeration_new( )")
        print("\n# ligandAs :")
        for mol in ligandAs:
            print(Chem.MolToSmiles(mol))         
        
        print("\n# ligandBs :")
        for mol in ligandBs:
            print(Chem.MolToSmiles(mol))
                 
        print("\n#The product D3_A molecules are: ")
        print("-"*80)
        #print("len(D3A_mols) is ", len(D3A_mols))
        for mol in D3A_mols:
            print(Chem.MolToSmiles(mol)) 

        print("-"*80)
        print("# The lens of ligandAs, ligandBs, D3A_mols are:")  
        print(len(ligandAs), len(ligandBs), len(D3A_mols) )  

    return delete_repeated_smiles_of_mols(D3A_mols)



#-----------------------------------------------------------------------------
def try_embedmolecule(mol):
    mol1 = Chem.AddHs(mol)
    conf_idx = AllChem.EmbedMolecule(mol1,
                                     #maxAttempts=0,
                                     randomSeed=38,
                                     )
                                     
    nb_try_EmbedMolecule = 1
    while conf_idx == -1 :
        print("nb_try_EmbedMolecule is ", nb_try_EmbedMolecule)
        print("AllChem.EmbedMolecule failed!")
        print("conf_idx is ", conf_idx)
        print("reset randomSeed and try")
        seednum = np.random.randint(1, 100000)        
        conf_idx = AllChem.EmbedMolecule(mol1,
                                 #maxAttempts=0,
                                 randomSeed=seednum,
                                 )
        nb_try_EmbedMolecule += 1
    
    print("The final conf_idx is ", conf_idx)
    
    print("nb_try_EmbedMolecule = ", nb_try_EmbedMolecule)
    
    return mol1, nb_try_EmbedMolecule


#-----------------------------------------------------------------------------
def write_mol_to_sdf(mol, cpd_name, outfile_path='./project/G0000/separate_mols/'):
    
    outname=  outfile_path + '%s.sdf'%(cpd_name)
    #print(outname)
    one_w = Chem.SDWriter(outname)
    m_temp = Chem.AddHs(mol)
    m1_temp, nb_try_EmbedMolecule = try_embedmolecule(m_temp)
    m1_temp.SetProp("_Name", cpd_name)
    one_w.write(m1_temp)


def write_mols_paralell(mols, cpd_names, outfile_path='./project/G0000/separate_mols/'):
    #-------  paralell write mols-----------------------------------------------------------
    print("The outfile_path is : %s" % outfile_path )
    
    start = time.time()
    
    rm_GXXXX_separate_mols_sdf = 'rm -f   '  +  outfile_path + 'cpd-*.sdf  '
    (status0, output0) = subprocess.getstatusoutput( rm_GXXXX_separate_mols_sdf )
    
    Parallel(n_jobs=-1)(delayed(write_mol_to_sdf)(mol, cpd_name, outfile_path) \
                        for mol, cpd_name in zip( tqdm(mols), cpd_names) )
    
    end = time.time()
    
    print('-'*60)
    print("write_mol_to_sdf run in paralell.")
    print('{:.4f} s'.format(end-start))




#_________________________________________________________________________________
#*********************************************************************************
#-----__main__ function begins here ----------------------------------------------
if __name__ == '__main__':

    print("Begins")
    print("-"*80)
    
# =============================================================================
#     #---- test on D_Pi_A_Enumeration( )    
#     cores1_smis = ['n1c(*)c[nH]c1','n1cc(*)[nH]c1', 'n1cc[nH]c1(*)', 'n1ccn(*)c1']
#     chains_smis = ['C[Po]', 'CC[Po]', 'CCC[Po]'] 
#     cores2_smis = ['c1ncccc1C(=O)O', 'c1cnccc1C(=O)O', 'c1ccncc1C(=O)O']
#     D_Pi_A_mols = D_Pi_A_Enumeration(cores1_smis, chains_smis, cores2_smis, verbse=True)
#     draw_mols(D_Pi_A_mols, 16, './images/foo025--D-Pi-A-mols.png', molsPerRow=4, size=(400, 400))
#     
#     #---- test on Cores_Chains_Enumeration( )
#     cores_smis = ['n1c(*)c[nH]c1','n1cc(*)[nH]c1', 'n1cc[nH]c1(*)', 'n1ccn(*)c1']
#     chains_smis = ['CN', 'CCN', 'CCCN'] 
#     cores_chains_mols = Cores_Chains_Enumeration(cores_smis, chains_smis, verbse=True)
#     draw_mols(cores_chains_mols, 9, './images/foo025--cores-chains-mols.png', molsPerRow=3, size=(400, 400))
#     
#     #---- test on Cores_Chains_Enumeration_FullSubstitute( )
#     cores_smis = ['*[n+]1c(*)c[nH]c1(*)', 'n1cc(*)[nH]c1(*)']
#     chains_smis = ['CN', 'CCN', 'CCCN'] 
#     cores_chains_mols = Cores_Chains_Enumeration_FullSubstitute(cores_smis, chains_smis, verbse=True)
#     draw_mols(cores_chains_mols, 9, './images/foo025--cores-chains-fullsubs-mols.png', molsPerRow=3, size=(400, 400))
#
# =============================================================================     

# =============================================================================
#     #---- test on D_A_Enumeration_new()
#     ligandA_smis = ['C1=CC=CC2=C1[N](C3=C2C=CC=C3)[*]', \
#                     'C1=CC(=CC2=C1[N](C3=C2C=C(C=C3)C)[*])C', \
#                     'C1=CC(=CC2=C1[N](C3=C2C=C(C=C3)C(C)(C)C)[*])C(C)(C)C']
#     ligandB_smis = ['C1=CC=CC=C1[S](C2=CC=C(C=C2)[Po])(=O)=O', \
#                     'C1=CC=CC=C1C(C2=CC=C(C=C2)[Po])=O', \
#                     'C1=CC(=CC=C1C(C2=CC=C(C=C2)[Po])=O)C(C3=CC=CC=C3)=O'] 
#     
#     DA_mols = D_A_Enumeration_new(ligandA_smis, ligandB_smis, verbse=True)
#     
#     draw_mols(DA_mols, 9, './images/foo001--DA-mols-new.png', molsPerRow=3, size=(400, 400))
#     
# 
#     #---- test on D_Pi_A_Enumeration_new()
#     ligandA_smis = ['C1=CC=CC2=C1[N](C3=C2C=CC=C3)[*]', \
#                     'C1=CC(=CC2=C1[N](C3=C2C=C(C=C3)C)[*])C', \
#                     'C1=CC(=CC2=C1[N](C3=C2C=C(C=C3)C(C)(C)C)[*])C(C)(C)C']
#         
#     pi_bridge_smis = ['C1=CC(=CC=C1[Po])[*]', \
#                       'C1=C(C=CC3=C1C(C2=CC(=CC=C2C3(C)C)[*])(C)C)[Po]']
#         
#     ligandB_smis = ['C1=CC=CC=C1[S](C2=CC=C(C=C2)[Po])(=O)=O', \
#                     'C1=CC=CC=C1C(C2=CC=C(C=C2)[Po])=O', \
#                     'C1=CC(=CC=C1C(C2=CC=C(C=C2)[Po])=O)C(C3=CC=CC=C3)=O'] 
#     
#     DPiA_mols = D_Pi_A_Enumeration_new(ligandA_smis, pi_bridge_smis, ligandB_smis, verbse=True) 
#     
#     draw_mols(DPiA_mols, len(DPiA_mols), './images/foo001--DPiA-mols-new.png', molsPerRow=3, size=(400, 400))
# 
# =============================================================================

# =============================================================================
#     #---- test on D_A_D_Enumeration_new(donor_smis, acceptorAsPiBridge_smis, verbse=False)
#     donor_smis = ['C1=CC=CC2=C1[N](C3=C2C=CC=C3)[*]', \
#               'C1=CC(=CC2=C1[N](C3=C2C=C(C=C3)C)[*])C', \
#               'C1=CC(=CC2=C1[N](C3=C2C=C(C=C3)C(C)(C)C)[*])C(C)(C)C']
#     
#     acceptorAsPiBridge_smis = ['C1=CC(=CC=C1[S](C2=CC=C(C=C2)[Po])(=O)=O)[*]', \
#                             'C1=CC(=CC=C1C(C2=CC=C(C=C2)[Po])=O)C(C3=CC=C(C=C3)[*])=O',  \
#                             'C1=C(C=C(C=C1C#N)[*])[Po]']
#     
#     DAD_mols = D_A_D_Enumeration_new(donor_smis, acceptorAsPiBridge_smis, verbse=True)
# 
#     draw_mols(DAD_mols , 
#               len(DAD_mols), 
#               './images/foo001--DAD_mols-new.png', 
#               molsPerRow=3, 
#               size=(400, 400))
# =============================================================================

# =============================================================================
#     #--- test on replace_dummy_by_Po_label()
#     
#     donors = [ Chem.MolFromSmiles(smi) for smi in donor_smis ]
#     
#     for mol in donors:
#         print(Chem.MolToSmiles(mol))
# 
#     for donor in donors:
#         replace_dummy_by_Po_label(donor, original_label_symbol='*', final_label_symbol='Po')
#     
#     for mol in donors:
#         print(Chem.MolToSmiles(mol))
# =============================================================================
        
# =============================================================================
#     #----- test on exchange_dummy_and_Po_label_idx() 
#     mol = Chem.MolFromSmiles('C1=C(CCCCO)C(=CC=C1[Po])[*]')
#     molold = Chem.MolFromSmiles('C1=C(CCCCO)C(=CC=C1[Po])[*]')
#     exchange_dummy_and_Po_label_idx(mol, label_atom1_symbol='*', label_atom2_symbol='Po')
#     
#     draw_mols([molold, mol], 2, './foo001--exchange-dummy-Po.png', molsPerRow=2, size=(600, 600))
# =============================================================================
#
# =============================================================================
#     atom_idxs = find_label_atom_idxs(Chem.MolFromSmiles('C1(=NC(=NC(=N1)[Po])[Po])[Po]'), atom_symbol='Po')
#     print('atom_idxs = ', atom_idxs )
#     
#     dummy_atom_idx = find_label_atom_idx(Chem.MolFromSmiles('C1(=NC(=NC(=N1)[Po])[Po])[Po]'), atom_symbol='Po')
#     print('dummy_atom_idxs = ', dummy_atom_idx )
# =============================================================================

# =============================================================================
#     #---- test on D3_A_Enumeration_new(donor_smis, acceptor_3Po_smis, verbse=False)
#     donor_smis = ['C1=CC=CC2=C1[N](C3=C2C=CC=C3)[*]', \
#               'C1=CC(=CC2=C1[N](C3=C2C=C(C=C3)C)[*])C', \
#               'C1=CC(=CC2=C1[N](C3=C2C=C(C=C3)C(C)(C)C)[*])C(C)(C)C']
#     
#     acceptor_3Po_smis = ['C1(=NC(=NC(=N1)[Po])[Po])[Po]', \
#                          'C1(=NC(=CC(=N1)[Po])[Po])[Po]',  \
#                              'C1(=NC(=C(C=N1)[Po])[Po])[Po]']
#     
#     D3A_mols = D3_A_Enumeration_new(donor_smis, acceptor_3Po_smis, verbse=True)
# 
#     draw_mols(D3A_mols , 
#               len(D3A_mols), 
#               './images/foo001--D3A_mols-new.png', 
#               molsPerRow=3, 
#               size=(400, 400))
# =============================================================================


    
    print("\nFinished!")
    

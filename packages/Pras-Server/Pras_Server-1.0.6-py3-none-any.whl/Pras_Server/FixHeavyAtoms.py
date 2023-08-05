__doc__ = """
This program requires python 3.6 or higher.

print(functionName.__doc__) to see the 

documentation for the function or usage.

Send enquiries to osita@protein-science.com
"""
import os
import string
import itertools
from .CheckPDBatoms import checkpdbAtoms

def atomType(name):
    """
    This function returns the
    format for writing the atom
    name to a PDB file
    
    Arguments
    ----------
    name: the standard PDB atom name
    
    Returns
    -------
    string: the atom name and format 
            for writing to a PDB file 
    """
    if len(name) == 1:
        name = " %s  " % name
    elif len(name) == 2:
        name = " %s " % name
    elif len(name) == 3:
        name = " %s" % name
    elif len(name) == 4:
        name = "%s" % name
    return name 

def insertRes(res):
    """
    This function returns the
    letter for residue insertion
    to be written to a PDB file
    
    Arguments
    ----------
    res: the res name + res No + insertion
         as concatenated by PRAS when reading
         input PDB file
    
    Returns
    -------
    string: the insertion code/letter if it 
            exists else a blank space 
    """
    if res[-1].isalpha():
        return res[-1]
    else:
        return " "

def fixheavyAtoms(pdb_pras,rotamer,mutation,pdb_faspr):
    """
    This function steps over each residue of a chain and 
    writes to a PDB file the atoms. No hydrogen atoms are
    added. To add hydrogen atoms use PRAS.py instead
    
    Arguments (this function takes 4 compulsory arguments)
    ----------
    pdb_pras:  the syntactically correct PDB file to repair/analyze

    rotamer:   by default, atoms with the highest occupancy are
               written to PDB file in the case of rotamers.
               If you want low occupancy instead, supply "no" or any 
               string as the argument, otherwise supply "" as argument.

    mutation:  when there is point mutation, two residues with unequal
               occupany (i.e. the residue atoms) are given same residue number. 
               By default the residue with the highest occupancy is
               written to PDB file. If you want low occupancy instead supply "no" 
               or any string as the argument, otherwise supply "" as argument.

    pdb_faspr: the PDB file obtained from FASPR (by running the same PDB supplied to PRAS). 
               FASPR is a free and open source side-chain packer, thanks to Huang et al.
               You can obtain it at https://github.com/tommyhuangthu/FASPR
               
               Note that if there are no missing atoms that require flexible
               chi to fix then FASPR is not required. If there are such
               atoms and you do not supply FASPR PDB file, PRAS will use
               the default or most probable chi from Dunbrack 2011 rotamer
               library to fix the atom. So in any case PRAS will run but will
               notify you if FASPR PDB is not supplied.

               Although FASPR is more accurate than most state-of-the-art side-chain packers,
               it is not infinitely accurate and sometimes the default chi from PRAS is the 
               right conformation for the amino acid residue side-chain. It is adviced that
               you compare both methods when necessary.

               Be mindful of the fact that FASPR may be less flexible with reading
               PDB files and has no mechanism to use lower conformers in the case
               of rotamers/mutation. To avoid manual editing, pass the PDB through PRAS first.

    Returns
    -------
    None: repaired PDB file without hydrogen atoms will be written.
          Ensure you have write permission in the directory where you
          run the program
    """
    try:
        os.remove('out_no_h.pdb') 
    except:
        pass

    nchain = checkpdbAtoms(pdb_pras,rotamer,mutation,pdb_faspr)
    chains = list(itertools.chain(*[i[-1] for i in nchain]))
    
    number = 1
    for n in range(len(nchain)):
        resn,atom,atmpos,resNo,resseq,sg_coord,chain = nchain[n]
        x = list(zip(resn,atom,atmpos))
        res_pos,atom_name = atmpos,atom

        #write output
        with open('out_no_h.pdb', 'a')  as f:            
            for k,l in enumerate (res_pos): #steps over each residue
                atm = atom_name[k]
                for i,j in enumerate(l):
                    f.write("%6s%5s %4s %-4s%1s%4s%1s   %8.3f%8.3f%8.3f%6.2f%6.2f" \
                    %('ATOM  ',str(number)[-5:],atomType(atm[i]),resseq[k],\
                    chains[n],str(resNo[k])[-4:],insertRes(resn[k]),\
                    l[i][0],l[i][1],l[i][2],1.00,0.00)+'\n')
                    number+=1

        # if there are more than 1 chain
        # write TER at the end and if the last chain
        # write TER and then END                    
        with open('out_no_h.pdb', 'a')  as f:
            if n != len(nchain)-1:
                f.write('{:4s}' '{:2s}' '{:5d}''{:s}' '{:4s}''{:s}''{:3s}'
                 '{:2s}''{:4d}\n'.format\
                    ('TER',' ',number,' ',' ', ' ',resseq[len(x)-1],
                        ' '+chains[n],resNo[len(x)-1]))
            else:
                f.write('{:4s}' '{:2s}' '{:5d}''{:s}' '{:4s}''{:s}'
                    '{:3s}' '{:2s}''{:4d}\n'.format\
                    ('TER',' ',number,' ',' ', ' ',resseq[len(x)-1],
                    ' '+chains[n],resNo[len(x)-1]))
                f.write('END')
                f.close()

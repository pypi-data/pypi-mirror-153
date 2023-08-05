__doc__ = """
This program requires python 3.6 or higher.

print(functionName.__doc__) to see the

documentation for the function or usage.

Send enquiries to osita@protein-science.com
"""
import os
import sys
import itertools
from .MissingHydrogenAtoms import *
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

def repairPDB(pdb_pras,rotamer,mutation,pdb_faspr):
    """
    This function steps over each residue of a chain and obtains from
    MissingHydrogenAtoms.py all atoms of the residue to be wrttien to a new PDB file.

    If the residue is not the last and the next residue is not PRO the returned list
    will contain a backbone H otherwise it will have no backbone H.

    For Cys residue, SG_coords are used to check for disulfide bonds.
    If disulfide bond exists it obtains no HG, otherwise it obtains HG

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
    None: repaired and hydrogenated PDB file will be written.
          Ensure you have write permission in the directory where you
          run the program
    """
    try:
        os.remove('out_with_h.pdb')
    except:
        pass

    nchains = checkpdbAtoms(pdb_pras,rotamer,mutation,pdb_faspr)
    chains = list(itertools.chain(*[i[-1] for i in nchains]))

    # atom numbering starts from the first chain
    number=1
    for n in range(len(nchains)):
        resn,atom,atmpos,resNo,resseq,sg_coord,chain = nchains[n]
        x = list(zip(resn,atom,atmpos))
        res_pos,h_pos,atom_name = [],[],[]

        # steps over the residues and if the next residue is not PRO
        # it returns backbone H but if PRO or the last residue in the
        # chain it does not return backbone H. The H is later added
        # to residue i+1
        for i,j in  enumerate(x):
            if j[0].startswith('ARG'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name = arginine_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name = arginine_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('ALA'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=alanine_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=alanine_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('ASP'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=aspartate_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=aspartate_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('ASN'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=asparagine_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=asparagine_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('GLU'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=glutamate_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=glutamate_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('GLN'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=glutamine_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=glutamine_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('GLY'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=glycine_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=glycine_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('HIS') or any(j[0].startswith(hs) for hs in ['HSD','HSP','HSE']):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=histidine_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=histidine_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('ILE'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=isoleucine_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=isoleucine_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('LEU'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=leucine_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=leucine_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('LYS'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=lysine_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=lysine_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('MET'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=metheonine_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=metheonine_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('PRO'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=proline_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=proline_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('TRP'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=tryptophan_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=tryptophan_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('VAL'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=valine_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=valine_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('PHE'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=phenylalanine_h(x[i],i,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=phenylalanine_h(x[i])
                    res_pos.extend([apos]);atom_name.extend([name])

                    """
                    The remaining residues (SER, THR, TYR and free CYS) have what we regard as
                    class6 H-atoms with rotational freedom. These H-atoms are optimized with a
                    potential energy function that may affect the computational time. You can go
                    to PotentialEnergy.py and look for "optimize()" function and decrease/increase
                    the rotation interval. Currently, it is set to 45 degrees but in the online PRAS
                    server it is set to a much lower value.

                    If you are not interested in the optimization, go to MissingHydrogenAtoms.py
                    locate SER, THR, TYR and CYS and comment the lines as appropriate
                    """
            elif j[0].startswith('SER'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=serine_h(x[i],i,resNo[i],atom,atmpos,resNo,resseq,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=serine_h(x[i],i,resNo[i],atom,atmpos,resNo,resseq)
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('THR'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=threonine_h(x[i],i,resNo[i],atom,atmpos,resNo,resseq,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=threonine_h(x[i],i,resNo[i],atom,atmpos,resNo,resseq)
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('TYR'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    apos,hpos,name=tyrosine_h(x[i],i,resNo[i],atom,atmpos,resNo,resseq,x[(i+1)%len(x)])
                    res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    apos,name=tyrosine_h(x[i],i,resNo[i],atom,atmpos,resNo,resseq)
                    res_pos.extend([apos]);atom_name.extend([name])

            elif j[0].startswith('CYS'):
                if x[(i+1)% len(x)][0][:3] != 'PRO' and x[i] != x[-1]:
                    if checkDisulfide(x[i][2][5],sg_coord) == 'is_bond':
                        apos,hpos,name=isDisulfide(x[i],i,x[(i+1)%len(x)])
                        res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                    else:
                        apos,hpos,name=notDisulfide(x[i],i,resNo[i],atom,atmpos,resNo,resseq,x[(i+1)%len(x)])
                        res_pos.extend([apos]);h_pos.extend([hpos]);atom_name.extend([name])
                else:
                    if checkDisulfide(x[i][2][5],sg_coord) == 'is_bond':
                        apos,name=isDisulfide(x[i],i)
                        res_pos.extend([apos]);atom_name.extend([name])
                    else:
                        apos,name=notDisulfide(x[i],i,resNo[i],atom,atmpos,resNo,resseq)
                        res_pos.extend([apos])
                        atom_name.extend([name])

        # Histidine protonation
        # comment next code line if you want all HIS side-chain neutral. See explanation online at www.protein-science.com
        # this code line randomly protonates 20% of all HIS residues
        res_pos, atom_name = prot_his(x,res_pos,atom_name,n)

        # Add backbone hydrogen.
        # It belongs to resi i+1
        for i,j in enumerate(h_pos):
            res_pos[h_pos[i][1]+1].extend([h_pos[i][0]])
            atom_name[h_pos[i][1]+1].extend('H')

        # Add n-terminal hydrogen, if proline only two H
        # If not PRO, three H
        if x[0][0][:3] == 'PRO':
            res_pos[0].extend(ntermini_pro(x[0],resn[0][:3]))
            atom_name[0].extend(['H1','H2'])
        else:
            res_pos[0].extend(ntermini_notpro(x[0],resn[0][:3]))
            atom_name[0].extend(['H1','H2','H3'])

        # steps over each residue
        # then steps over each residue atom
        # and writes to a PDB file
        with open('out_with_h.pdb', 'a')  as f:
            for k,l in enumerate (res_pos):
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
        with open('out_with_h.pdb', 'a')  as f:
            if n != len(nchains)-1:
                f.write('{:4s}' '{:2s}' '{:5d}''{:s}' '{:4s}''{:s}''{:3s}' '{:2s}''{:4d}\n'.format\
                    ('TER',' ',number,' ',' ', ' ',resseq[len(x)-1],' '+chains[n],resNo[len(x)-1]))
            else:
                f.write('{:4s}' '{:2s}' '{:5d}''{:s}' '{:4s}''{:s}''{:3s}' '{:2s}''{:4d}\n'.format\
                    ('TER',' ',number,' ',' ', ' ',resseq[len(x)-1],' '+chains[n],resNo[len(x)-1]))
                f.write('END')
                f.close()

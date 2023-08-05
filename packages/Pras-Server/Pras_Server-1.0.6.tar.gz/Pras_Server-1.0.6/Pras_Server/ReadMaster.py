__doc__ = """
This program requires python 3.6 or higher.

print(functionName.__doc__) to see the

documentation for the function or usage.

Send enquiries to osita@protein-science.com
"""
import copy
import itertools

heay_atoms = ['N', 'CA', 'C', 'O', 'CB', 'CG', 'OD1', 'OD2', 'OXT', 'CD',   'CE',\
              'NZ', 'OG', 'CG1', 'CG2', 'CD1', 'CD2', 'OG1', 'CE2', 'CE3', 'NE1',\
              'CZ2', 'CZ3', 'CH2', 'NE', 'CZ', 'NH1', 'NH2', 'ND2', 'NE2', 'OE1',\
              'SG', 'OE2', 'ND1', 'CE1', 'SD', 'OH']

class Atom:
  """
  This class provides a way to grab the atom attributes
  of a PDB atom line once the instance is initiated
  """
  def __init__(self):
    self.pos = ""
    self.type = ""
    self.chain_id = " "
    self.res_type = ""
    self.res_num = ""
    self.res_insert = ""
    self.alt_conform = " "
    self.occupancy = 0.0
    self.num = 0
    self.rot = ""

def readAtom(line):
  """
  This function is used to populate the Atom class attributes

  Arguments
  ----------
  line: a PDB structure file atom line

  Returns
  -------
  An string: the Atom class object
  """
  atom = Atom()
  atom.num = int(line[6:11])
  atom.alt_conform = line[16].strip(" ")
  atom.type = line[12:16].strip(" ")
  atom.res_type = line[17:21].strip(" ")
  atom.chain_id = line[21]
  atom.res_num = int(line[22:26])
  atom.res_insert = line[26]
  atom.ocpancy = float(line[54:60])
  if atom.res_insert == " ":
    atom.res_insert = ""
  x = float(line[30:38])
  y = float(line[38:46])
  z = float(line[46:54])
  atom.pos = [x,y,z]
  atom.rot = ""
  return atom

class Residue:
  """
  This class provides a way to grab attributes of residues.
  The regular methods provide a way to append the atoms
  belonging to the residue
  """
  def __init__(self,_type="",_chain_id="",_num="",_insert="", occupancy=""):
    self._atom    = []
    self._pos     = []
    self._ocpancy = []
    self.num      = _num
    self.rtype    = _type
    self.insert   = _insert
    self.chain_id = _chain_id
    self.occupancy= occupancy

  def atoms(self):
    return self._atom

  def appendAtom(self,atom):
    # no rotamer, append the atom
    if not atom.type in self._atom:
      self._atom.append(atom.type)
      self._pos.append(atom.pos)
      self._ocpancy.append(atom.ocpancy)

    if atom.type in self._atom and not atom.rot:
    # there is rotamer, use highest occupancy
      if atom.ocpancy > self._ocpancy[-1]:
        self._atom[-1]    = atom.type
        self._pos[-1]     = atom.pos
        self._ocpancy[-1] = atom.ocpancy

    if atom.type in self._atom and atom.rot:
    # there is rotamer, use lowest occupancy
      if atom.ocpancy < self._ocpancy[-1]:
        self._atom[-1]    = atom.type
        self._pos[-1]     = atom.pos
        self._ocpancy[-1] = atom.ocpancy

  def __str__(self):
    return str(["%s%s%s,  %s ,  %s , %s , %s, %s" % (self.rtype, \
    self.num,self.insert,self._pos,self._atom,self.num,self.chain_id,self.occupancy)])

  def __getitem__(self,i):
    return [(self.rtype+str(self.num)+self.insert, self._atom,self._pos,\
      self.num,self.chain_id,self.occupancy)[i]]

  def __len__(self):
    return len(["%s%s%s,  %s , %s , %s" % (self.rtype, \
    self.num,self.insert,self._pos,self.num,self.chain_id)])

class Chain():
  """
  This class provides a way to grab the residues of a chain.
  The regular methods provide a way to append the residues and
  atoms belonging to the residue
  """
  _chain = []
  def insertAtom(self,i,atom,):
    self._chain[i].appendAtom(atom)

  def appendResidue(self,res,ocpancy,mutation):
    # list is initially empty
    if not self._chain:
      self._chain.append(res)

    # now list is not empty, check for mutation
    if res[0][0][3:] != self._chain[-1][0][0][3:]:
      self._chain.append(res)

    # now mutation exists, chose based on occupancy and argument
    if res[0][0][3:] == self._chain[-1][0][0][3:] and not mutation:
      if ocpancy > self._chain[0][-1][0]:
        self._chain[-1] = res

    if res[0][0][3:] == self._chain[-1][0][0][3:] and mutation:
      if ocpancy < self._chain[0][-1][0]:
        self._chain[-1] = res

  def __len__(self):
    return len(self._chain)

  def __getitem__(self,i):
    return self._chain[i]

class Chains():
  """
  This class provides a way to grab all chains of the PDB file.
  The regular method initiates the repair for rotamer & point mutation
  """
  def __init__(self, fname,rotamer,mutation,faspr):

    self.all_chains = []
    self.readPDB(fname,rotamer,mutation,faspr)

  def readPDB(self, fname,rotamer,mutation,faspr):
    """
    This function reads the PDB file content.
    It begings the repair for romaters & point mutation

    Arguments
    ----------
    fname    :the PDB file to be read
    rotamer:  a string, by default the atom
              with highest occupancy is taken
              except a string value is passed
              to this argument

    mutation: a string, by default the
              residue with highest occupancy
              is taken except a string value is passed
              to this argument

    faspr:    the PDB file obtained from FASPR
              (by running the same PDB supplied to PRAS).

    Returns
    -------
    None:     stops reading when line starts with
              END or ENDMDL
    """
    res_num, res_insert, res_type  = -1, " ", " "
    if not fname:
      fname = faspr
    for line in open(fname, 'r').readlines():
      if line.startswith("ATOM") and line[12:16].strip(" ") in heay_atoms:
        atom = readAtom(line)
        atom.rot = rotamer
        if (res_num!=atom.res_num) or (res_insert!=atom.res_insert) or\
                    (res_num==atom.res_num and res_type!=atom.res_type):
          residue = Residue(atom.res_type,atom.chain_id,atom.res_num,\
                            atom.res_insert,atom.ocpancy)

          # first create Chain instance that will contain atoms of residues
          # append only res_type,chain_id, res_num,res_insert,and ocpancy
          # if same resi num exists check occupancy and decide which to keep
          chain = Chain()
          chain.appendResidue(residue,atom.ocpancy,mutation)
          res_num = atom.res_num
          res_insert = atom.res_insert
          res_type = atom.res_type

        # now add the atoms of the residue until next PDB line becomes next-
        # residue and the above process is repeated
        if (res_type==atom.res_type and res_type==chain._chain[-1][0][0][:3]):
          chain.insertAtom(-1, atom)

      if line.startswith(("TER")):
        if chain._chain:
          self.all_chains.append(chain._chain.copy())
          chain._chain.clear()
          res_num = -1
      if line.startswith(("END", "ENDMDL")):
        return
  def __str__(self):
    chains = [[list(itertools.chain(*[i for i in res]))\
     for res in res2] for res2 in self.all_chains]
    return str(chains)

  def __len__(self):
    return len(self.all_chains)

  def __getitem__(self,i):
    return self.all_chains[i]

def getChains(fname,rotamer,mutation,faspr):
  """
  This function initiates the reading of PDB file.

  Arguments
  ----------
  fname    : the PDB file to be read

  rotamer:   supply "no" if you need to generate lower occupancy conformers,
             if not supply "". PRAS uses atoms with highest occupancy
             by default.

  mutation:  supply "no" if you need to generate lower occupancy conformers,
             if not supply "". PRAS uses the residue with highest
             occupancy by default if two residues are given same residue number

  faspr:    the PDB file obtained from FASPR
            (by running the same PDB supplied to PRAS).

  Returns
  -------
  A list of list: each index is a chain in the PDB file
  """
  f_data = Chains(fname,rotamer,mutation,faspr)
  chains = [[] for i in range(len(f_data))]
  for i in range(len(f_data)):
    z = f_data[i]
    """[0]=resn+resNo+res_insert,[1]=atm_pos,[2]=atm_name,[3]=resn_No"""
    chains[i].append(list(itertools.chain(*[z[j][0] for j in range(len(z))])))
    chains[i].append(list(itertools.chain(*[z[j][1] for j in range(len(z))])))
    chains[i].append(list(itertools.chain(*[z[j][2] for j in range(len(z))])))
    chains[i].append(list(itertools.chain(*[z[j][3] for j in range(len(z))])))
    chains[i].append(z[0][-2])

  return((chains))

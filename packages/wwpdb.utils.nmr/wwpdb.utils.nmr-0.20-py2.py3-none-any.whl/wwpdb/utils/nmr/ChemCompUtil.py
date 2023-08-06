##
# File: ChemCompUtil.py
# Date: 18-Feb-2022
#
# Updates:
# 27-Apr-2022  M. Yokochi - enable to use cached data for standard residues
##
""" Wrapper class for retrieving chemical component dictionary.
    @author: Masashi Yokochi
"""
import os
import sys
import pickle

try:
    from wwpdb.utils.config.ConfigInfo import getSiteId
    from wwpdb.utils.config.ConfigInfoApp import ConfigInfoAppCommon
    from wwpdb.utils.nmr.io.ChemCompIo import ChemCompReader
    from wwpdb.utils.nmr.AlignUtil import monDict3
    cICommon = ConfigInfoAppCommon(getSiteId())
    CC_CVS_PATH = cICommon.get_site_cc_cvs_path()
except ImportError:
    from nmr.io.ChemCompIo import ChemCompReader
    from nmr.AlignUtil import monDict3
    CC_CVS_PATH = os.path.dirname(__file__) + '/ligand_dict'  # need to setup 'ligand_dict' CCD resource for NMR restraint processing


def load_dict_from_pickle(file_name):
    """ Load cached dictionary from pickle file.
    """

    if os.path.exists(file_name):

        with open(file_name, 'rb') as ifp:
            return pickle.load(ifp)

    return {}


def write_dict_as_pickle(obj, file_name):
    """ Write dictionary as pickle file.
    """

    if isinstance(obj, dict):

        with open(file_name, 'wb') as ofp:
            pickle.dump(obj, ofp)


class ChemCompUtil:
    """ Wrapper class for retrieving chemical component dictionary.
    """

    def __init__(self, verbose=False, log=sys.stderr):

        # pickle file name of cached dictionary for standard residues
        self.__cacheFile = os.path.dirname(__file__) + '/chem_comp_util/std_chem_comp.pkl'

        self.__ccR = ChemCompReader(verbose, log)
        self.__ccR.setCachePath(CC_CVS_PATH)

        self.lastCompId = None
        self.lastStatus = False
        self.lastChemCompDict = None
        self.lastAtomList = None
        self.lastBonds = None

        # taken from wwpdb.apps.ccmodule.io.ChemCompIo
        _chemCompAtomDict = [
            ('_chem_comp_atom.comp_id', '%s', 'str', ''),
            ('_chem_comp_atom.atom_id', '%s', 'str', ''),
            ('_chem_comp_atom.alt_atom_id', '%s', 'str', ''),
            ('_chem_comp_atom.type_symbol', '%s', 'str', ''),
            ('_chem_comp_atom.charge', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_align', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_aromatic_flag', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_leaving_atom_flag', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_stereo_config', '%s', 'str', ''),
            ('_chem_comp_atom.model_Cartn_x', '%s', 'str', ''),
            ('_chem_comp_atom.model_Cartn_y', '%s', 'str', ''),
            ('_chem_comp_atom.model_Cartn_z', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_model_Cartn_x_ideal', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_model_Cartn_y_ideal', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_model_Cartn_z_ideal', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_component_atom_id', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_component_comp_id', '%s', 'str', ''),
            ('_chem_comp_atom.pdbx_ordinal', '%s', 'str', ' ')
        ]

        atomId = next(d for d in _chemCompAtomDict if d[0] == '_chem_comp_atom.atom_id')
        self.ccaAtomId = _chemCompAtomDict.index(atomId)

        aromaticFlag = next(d for d in _chemCompAtomDict if d[0] == '_chem_comp_atom.pdbx_aromatic_flag')
        self.ccaAromaticFlag = _chemCompAtomDict.index(aromaticFlag)

        leavingAtomFlag = next(d for d in _chemCompAtomDict if d[0] == '_chem_comp_atom.pdbx_leaving_atom_flag')
        self.ccaLeavingAtomFlag = _chemCompAtomDict.index(leavingAtomFlag)

        typeSymbol = next(d for d in _chemCompAtomDict if d[0] == '_chem_comp_atom.type_symbol')
        self.ccaTypeSymbol = _chemCompAtomDict.index(typeSymbol)

        cartnX = next(d for d in _chemCompAtomDict if d[0] == '_chem_comp_atom.model_Cartn_x')
        cartnY = next(d for d in _chemCompAtomDict if d[0] == '_chem_comp_atom.model_Cartn_y')
        cartnZ = next(d for d in _chemCompAtomDict if d[0] == '_chem_comp_atom.model_Cartn_z')
        self.ccaCartnX = _chemCompAtomDict.index(cartnX)
        self.ccaCartnY = _chemCompAtomDict.index(cartnY)
        self.ccaCartnZ = _chemCompAtomDict.index(cartnZ)

        # taken from wwpdb.apps.ccmodule.io.ChemCompIo
        _chemCompBondDict = [
            ('_chem_comp_bond.comp_id', '%s', 'str', ''),
            ('_chem_comp_bond.atom_id_1', '%s', 'str', ''),
            ('_chem_comp_bond.atom_id_2', '%s', 'str', ''),
            ('_chem_comp_bond.value_order', '%s', 'str', ''),
            ('_chem_comp_bond.pdbx_aromatic_flag', '%s', 'str', ''),
            ('_chem_comp_bond.pdbx_stereo_config', '%s', 'str', ''),
            ('_chem_comp_bond.pdbx_ordinal', '%s', 'str', '')
        ]

        atomId1 = next(d for d in _chemCompBondDict if d[0] == '_chem_comp_bond.atom_id_1')
        self.ccbAtomId1 = _chemCompBondDict.index(atomId1)

        atomId2 = next(d for d in _chemCompBondDict if d[0] == '_chem_comp_bond.atom_id_2')
        self.ccbAtomId2 = _chemCompBondDict.index(atomId2)

        aromaticFlag = next(d for d in _chemCompBondDict if d[0] == '_chem_comp_bond.pdbx_aromatic_flag')
        self.ccbAromaticFlag = _chemCompBondDict.index(aromaticFlag)

        self.__cachedDict = load_dict_from_pickle(self.__cacheFile)
        self.__failedCompId = []

    def updateChemCompDict(self, compId):
        """ Update CCD information for a given comp_id.
            @return: True for successfully update CCD information or False for the case a given comp_id does not exist in CCD
        """

        if compId is None:
            return False

        compId = compId.upper()

        if compId in self.__failedCompId:
            return False

        if compId != self.lastCompId:
            self.lastStatus = False if '_' in compId else self.__ccR.setCompId(compId)
            self.lastCompId = compId

            if self.lastStatus:
                if compId in self.__cachedDict:
                    self.lastChemCompDict = self.__cachedDict[compId]['chem_comp']
                    self.lastAtomList = self.__cachedDict[compId]['chem_comp_atom']
                    self.lastBonds = self.__cachedDict[compId]['chem_comp_bond']
                else:
                    self.lastChemCompDict = self.__ccR.getChemCompDict()
                    self.lastAtomList = self.__ccR.getAtomList()
                    self.lastBonds = self.__ccR.getBonds()
                    self.__cachedDict[compId] = {'chem_comp': self.lastChemCompDict,
                                                 'chem_comp_atom': self.lastAtomList,
                                                 'chem_comp_bond': self.lastBonds}

            else:
                self.__failedCompId.append(compId)

        return self.lastStatus

    def write_std_dict_as_pickle(self):
        """ Write dictionary for standard residues as pickle file.
        """

        for compId in monDict3:
            self.updateChemCompDict(compId)

        write_dict_as_pickle(self.__cachedDict, self.__cacheFile)

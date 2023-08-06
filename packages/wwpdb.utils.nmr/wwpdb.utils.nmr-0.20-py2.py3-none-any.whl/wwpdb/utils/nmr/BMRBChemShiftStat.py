##
# File: BMRBChemShiftStat.py
# Date: 20-Sep-2019
#
# Updates:
# 26-Feb-2020  M. Yokochi - load csv resource files if pickle is not available
# 04-Mar-2020  M. Yokochi - support lazy import of others (non-standard residues, DAOTHER-5498)
# 16-Apr-2020  M. Yokochi - fix ambiguity code of atom name starts with 'Q' (e.g. LYZ:QZ)
# 20-Nov-2020  M. Yokochi - fix statics extraction for HEM, HEB, HEC from CSV (DAOTHER-6366)
# 25-Jun-2021  M. Yokochi - add getAtomLikeNameSet() (DAOTHER-6830)
# 13-Oct-2021  M. Yokochi - code revision according to PEP8 using Pylint (DAOTHER-7389, issue #5)
# 03-Dec-2021  M. Yokochi - optimize loading performance of other chemical shift statistics (DAOTHER-7514)
# 04-Feb-2022  M. Yokochi - add getPseudoAtoms() (NMR restraint remediation)
# 14-Feb-2022  M. Yokochi - add getSimilarCompIdFromAtomIds() (NMR restraint remediation)
# 25-Feb-2022  M. Yokochi - add peptideLike() (NMR restraint remediation)
##
""" Wrapper class for retrieving BMRB chemical shift statistics.
    @author: Masashi Yokochi
"""
import sys
import os
import csv
import re
import copy
import pickle
import collections

try:
    from wwpdb.utils.nmr.AlignUtil import emptyValue
    from wwpdb.utils.nmr.ChemCompUtil import ChemCompUtil
except ImportError:
    from nmr.AlignUtil import emptyValue
    from nmr.ChemCompUtil import ChemCompUtil


def load_stat_from_pickle(file_name):
    """ Load BMRB chemical shift statistics from pickle file if possible.
    """

    if os.path.exists(file_name):

        with open(file_name, 'rb') as ifp:
            return pickle.load(ifp)

    return []


def write_stat_as_pickle(obj, file_name):
    """ Write BMRB chemical shift statistics as pickle file.
    """

    if isinstance(obj, list):

        with open(file_name, 'wb') as ofp:
            pickle.dump(obj, ofp)


class BMRBChemShiftStat:
    """ Wrapper class for retrieving BMRB chemical shift statistics.
    """

    def __init__(self, verbose=False, log=sys.stderr, ccU=None):
        self.__verbose = verbose
        self.__lfh = log

        # lazy import of others (non-standard residues)
        self.lazy_others = True

        # directory
        self.stat_dir = os.path.dirname(__file__) + '/bmrb_cs_stat/'

        # statistics objects
        self.aa_filt = []
        self.aa_full = []

        self.dna_filt = []
        self.dna_full = []

        self.rna_filt = []
        self.rna_full = []

        self.others = []
        self.extras = []

        self.__aa_comp_ids = set()
        self.__dna_comp_ids = set()
        self.__rna_comp_ids = set()
        self.__oth_comp_ids = set()
        self.__ext_comp_ids = set()

        self.__std_comp_ids = set()
        self.__all_comp_ids = set()
        self.__not_comp_ids = set()

        self.aa_threshold = 0.1
        self.na_threshold = 0.3

        self.max_count_th = 10

        # CCD accessing utility
        self.__ccU = ChemCompUtil(self.__verbose, self.__lfh) if ccU is None else ccU

        if not self.loadStatFromPickleFiles():
            self.loadStatFromCsvFiles()
    # """
    # def isOk(self):
    #     """ Return whether all BMRB chemical shift statistics are available.
    #     """

    #     return len(self.aa_filt) > 0 and len(self.aa_full) > 0 and len(self.dna_filt) > 0 and len(self.dna_full) > 0 and \
    #         len(self.rna_filt) > 0 and len(self.rna_full) and (len(self.others) > 0 or self.lazy_others)
    # """
    def hasCompId(self, comp_id):
        """ Return whether a given comp_id has BMRB chemical shift statistics.
        """

        if comp_id in emptyValue:
            return False

        if comp_id in self.__std_comp_ids:
            return True

        self.loadOtherStatFromCsvFiles(comp_id)

        return comp_id in self.__all_comp_ids

    def peptideLike(self, comp_id):
        """ Return whether a given comp_id is peptide-like component.
        """

        if comp_id in emptyValue:
            return False

        if comp_id in self.__aa_comp_ids:
            return True

        if comp_id in self.__dna_comp_ids or comp_id in self.__rna_comp_ids:
            return False

        if self.__ccU.updateChemCompDict(comp_id):
            ctype = self.__ccU.lastChemCompDict['_chem_comp.type']

            if 'PEPTIDE' in ctype:
                return True

            if 'DNA' in ctype or 'RNA' in ctype or 'SACCHARIDE' in ctype:
                return False

        peptide_like = len(self.getBackBoneAtoms(comp_id, True, True, False, False))
        nucleotide_like = len(self.getBackBoneAtoms(comp_id, True, False, True, False))
        carbohydrate_like = len(self.getBackBoneAtoms(comp_id, True, False, False, True))

        return peptide_like > nucleotide_like and peptide_like > carbohydrate_like

    def getTypeOfCompId(self, comp_id):
        """ Return type of a given comp_id.
            @return: array of bool: peptide, nucleotide, carbohydrate
        """

        if comp_id in emptyValue:
            return False, False, False

        if comp_id in self.__aa_comp_ids:
            return True, False, False

        if comp_id in self.__dna_comp_ids or comp_id in self.__rna_comp_ids:
            return False, True, False

        if self.__ccU.updateChemCompDict(comp_id):
            ctype = self.__ccU.lastChemCompDict['_chem_comp.type']

            if 'PEPTIDE' in ctype:
                return True, False, False

            if 'DNA' in ctype or 'RNA' in ctype:
                return False, True, False

            if 'SACCHARIDE' in ctype:
                return False, False, True

        peptide_like = len(self.getBackBoneAtoms(comp_id, True, True, False, False))
        nucleotide_like = len(self.getBackBoneAtoms(comp_id, True, False, True, False))
        carbohydrate_like = len(self.getBackBoneAtoms(comp_id, True, False, False, True))

        return peptide_like > nucleotide_like and peptide_like > carbohydrate_like,\
            nucleotide_like > peptide_like and nucleotide_like > carbohydrate_like,\
            carbohydrate_like > peptide_like and carbohydrate_like > nucleotide_like

    def getSimilarCompIdFromAtomIds(self, atom_ids):
        """ Return the most similar comp_id including atom_ids.
            @return: the most similar comp_id, otherwise None
        """

        aa_bb = set(['C', 'CA', 'CB', 'H', 'HA', 'HA2', 'HA3', 'N'])
        dn_bb = set(["C1'", "C2'", "C3'", "C4'", "C5'", "H1'", "H2'", "H2''", "H3'", "H4'", "H5'", "H5''", "H5'1", "H5'2", 'P'])
        rn_bb = set(["C1'", "C2'", "C3'", "C4'", "C5'", "H1'", "H2'", "H3'", "H4'", "H5'", "H5''", "HO2'", "H5'1", "H5'2", "H2'1", "HO'2", 'P', "O2'"])
        ch_bb = set(['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'H61', 'H62'])

        length = len(atom_ids)
        atom_id_set = set(atom_ids)

        match = [len(atom_id_set & aa_bb),
                 len(atom_id_set & dn_bb),
                 len(atom_id_set & rn_bb),
                 len(atom_id_set & ch_bb)]

        max_match = max(match)
        comp_id = None

        if max_match > 0:
            position = match.index(max_match)
            if position == 0:
                max_score = 0
                for _comp_id in self.__aa_comp_ids:
                    _atom_id_set = set(i['atom_id'] for i in self.__get(_comp_id))
                    conflict = len(atom_id_set - _atom_id_set)
                    unmapped = len(_atom_id_set - atom_id_set)
                    score = length - conflict - unmapped
                    if score > max_score:
                        max_score = score
                        comp_id = _comp_id
                if comp_id is not None:
                    return comp_id

            elif position == 1:
                max_score = 0
                for _comp_id in self.__dna_comp_ids:
                    _atom_id_set = set(i['atom_id'] for i in self.__get(_comp_id))
                    conflict = len(atom_id_set - _atom_id_set)
                    unmapped = len(_atom_id_set - atom_id_set)
                    score = length - conflict - unmapped
                    if score > max_score:
                        max_score = score
                        comp_id = _comp_id
                if comp_id is not None:
                    return comp_id

            elif position == 2:
                max_score = 0
                for _comp_id in self.__rna_comp_ids:
                    _atom_id_set = set(i['atom_id'] for i in self.__get(_comp_id))
                    conflict = len(atom_id_set - _atom_id_set)
                    unmapped = len(_atom_id_set - atom_id_set)
                    score = length - conflict - unmapped
                    if score > max_score:
                        max_score = score
                        comp_id = _comp_id
                if comp_id is not None:
                    return comp_id

            if position == 0:
                comp_id = None
                max_score = 0
                for _comp_id in self.__all_comp_ids:
                    if self.getTypeOfCompId(_comp_id)[0]:
                        _atom_id_set = set(i['atom_id'] for i in self.__get(_comp_id))
                        conflict = len(atom_id_set - _atom_id_set)
                        unmapped = len(_atom_id_set - atom_id_set)
                        score = length - conflict - unmapped
                        if score > max_score:
                            max_score = score
                            comp_id = _comp_id
                if comp_id is not None:
                    return comp_id

            elif position in (1, 2):
                max_score = 0
                for _comp_id in self.__all_comp_ids:
                    if self.getTypeOfCompId(_comp_id)[1]:
                        _atom_id_set = set(i['atom_id'] for i in self.__get(_comp_id))
                        conflict = len(atom_id_set - _atom_id_set)
                        unmapped = len(_atom_id_set - atom_id_set)
                        score = length - conflict - unmapped
                        if score > max_score:
                            max_score = score
                            comp_id = _comp_id
                if comp_id is not None:
                    return comp_id

            else:
                max_score = 0
                for _comp_id in self.__all_comp_ids:
                    if self.getTypeOfCompId(_comp_id)[2]:
                        _atom_id_set = set(i['atom_id'] for i in self.__get(_comp_id))
                        conflict = len(atom_id_set - _atom_id_set)
                        unmapped = len(_atom_id_set - atom_id_set)
                        score = length - conflict - unmapped
                        if score > max_score:
                            max_score = score
                            comp_id = _comp_id
                if comp_id is not None:
                    return comp_id

        else:
            max_score = 0
            for _comp_id in self.__all_comp_ids:
                peptide_like, nucleotide_like, carbohydrate_like = self.getTypeOfCompId(_comp_id)
                if not(peptide_like or nucleotide_like or carbohydrate_like):
                    _atom_id_set = set(i['atom_id'] for i in self.__get(_comp_id))
                    conflict = len(atom_id_set - _atom_id_set)
                    unmapped = len(_atom_id_set - atom_id_set)
                    score = length - conflict - unmapped
                    if score > max_score:
                        max_score = score
                        comp_id = _comp_id

        return comp_id

    def hasEnoughStat(self, comp_id, primary=True):
        """ Return whether a given comp_id has enough chemical shift statistics.
        """

        if comp_id in emptyValue:
            return False

        if comp_id in self.__std_comp_ids:
            return True

        self.loadOtherStatFromCsvFiles(comp_id)

        if comp_id not in self.__all_comp_ids:
            return False

        if primary:
            if any(i for i in self.others if i['comp_id'] == comp_id and i['primary']):
                return True
        else:
            if any(i for i in self.others if i['comp_id'] == comp_id and 'secondary' in i and i['secondary']):
                return True

        return False

    def get(self, comp_id, diamagnetic=True):
        """ Return BMRB chemical shift statistics for a given comp_id.
        """

        if comp_id in emptyValue:
            return []

        if comp_id in self.__aa_comp_ids:

            if diamagnetic:
                return [i for i in self.aa_filt if i['comp_id'] == comp_id]

            return [i for i in self.aa_full if i['comp_id'] == comp_id]

        if comp_id in self.__dna_comp_ids:

            if diamagnetic:
                return [i for i in self.dna_filt if i['comp_id'] == comp_id]

            return [i for i in self.dna_full if i['comp_id'] == comp_id]

        if comp_id in self.__rna_comp_ids:

            if diamagnetic:
                return [i for i in self.rna_filt if i['comp_id'] == comp_id]

            return [i for i in self.rna_full if i['comp_id'] == comp_id]

        self.loadOtherStatFromCsvFiles(comp_id)

        if comp_id not in self.__all_comp_ids:
            return []

        return [i for i in self.others if i['comp_id'] == comp_id]

    def __get(self, comp_id, diamagnetic=True):
        """ Return atom list for a given comp_id.
        """

        if comp_id in emptyValue:
            return []

        if comp_id in self.__aa_comp_ids:

            if diamagnetic:
                return [i for i in self.aa_filt if i['comp_id'] == comp_id]

            return [i for i in self.aa_full if i['comp_id'] == comp_id]

        if comp_id in self.__dna_comp_ids:

            if diamagnetic:
                return [i for i in self.dna_filt if i['comp_id'] == comp_id]

            return [i for i in self.dna_full if i['comp_id'] == comp_id]

        if comp_id in self.__rna_comp_ids:

            if diamagnetic:
                return [i for i in self.rna_filt if i['comp_id'] == comp_id]

            return [i for i in self.rna_full if i['comp_id'] == comp_id]

        self.loadOtherStatFromCsvFiles(comp_id)

        if comp_id not in self.__all_comp_ids:
            self.__appendExtraFromCcd(comp_id)

        if comp_id in self.__oth_comp_ids:
            return [i for i in self.others if i['comp_id'] == comp_id]

        if comp_id in self.__ext_comp_ids:
            return [i for i in self.extras if i['comp_id'] == comp_id]

        return []

    def getMaxAmbigCodeWoSetId(self, comp_id, atom_id):
        """ Return maximum ambiguity code of a given atom that does not require declaration of ambiguity set ID.
            @return: one of (1, 2, 3), 0 for not found
        """

        if comp_id in emptyValue:
            return 0

        if comp_id not in self.__std_comp_ids:
            self.loadOtherStatFromCsvFiles(comp_id)

        if comp_id not in self.__all_comp_ids:
            self.__appendExtraFromCcd(comp_id)

        try:

            d = next(i['desc'] for i in self.__get(comp_id) if i['atom_id'] == atom_id)

            if 'geminal' in d:
                return 2

            if d == 'aroma-opposite':
                return 3

            return 1

        except StopIteration:
            return 0

    def getGeminalAtom(self, comp_id, atom_id):
        """ Return geminal or aromatic opposite atom of a given atom.
        """

        if comp_id in emptyValue:
            return None

        if comp_id not in self.__std_comp_ids:
            self.loadOtherStatFromCsvFiles(comp_id)

        if comp_id not in self.__all_comp_ids:
            self.__appendExtraFromCcd(comp_id)

        cs_stat = self.__get(comp_id)

        try:

            d = next(i['desc'] for i in cs_stat if i['atom_id'] == atom_id)

            if d == 'methyl-geminal' and atom_id[0] == 'H':
                return next(i['atom_id'] for i in cs_stat
                            if i['desc'] == d and i['atom_id'] != atom_id and i['atom_id'][:-2] == atom_id[:-2] and i['atom_id'][-1] == atom_id[-1])

            if 'geminal' in d or d == 'aroma-opposite':

                if not atom_id.endswith("'"):
                    return next(i['atom_id'] for i in cs_stat
                                if i['desc'] == d and i['atom_id'] != atom_id and i['atom_id'][:-1] == atom_id[:-1])

                if atom_id.endswith("''"):
                    return next(i['atom_id'] for i in cs_stat
                                if i['desc'] == d and i['atom_id'] != atom_id and i['atom_id'] == atom_id[:-1])

                return next(i['atom_id'] for i in cs_stat
                            if i['desc'] == d and i['atom_id'] != atom_id and i['atom_id'] == atom_id + "'")

            return None

        except StopIteration:
            return None

    def getAllAtoms(self, comp_id, excl_minor_atom=False, primary=False):
        """ Return all atoms of a given comp_id.
        """

        if comp_id in emptyValue:
            return []

        if comp_id not in self.__std_comp_ids:
            self.loadOtherStatFromCsvFiles(comp_id)

        if comp_id not in self.__all_comp_ids:
            self.__appendExtraFromCcd(comp_id)

        cs_stat = self.__get(comp_id)

        if comp_id in self.__std_comp_ids or primary:
            return [i['atom_id'] for i in cs_stat if
                    (not excl_minor_atom or (excl_minor_atom and i['primary']))]

        return [i['atom_id'] for i in cs_stat if
                (not excl_minor_atom or 'secondary' not in i or (excl_minor_atom and i['secondary']))]

    def getBackBoneAtoms(self, comp_id, excl_minor_atom=False, polypeptide_like=False, polynucleotide_like=False, carbohydrates_like=False):
        """ Return backbone atoms of a given comp_id.
        """

        if comp_id in emptyValue:
            return []

        if comp_id not in self.__std_comp_ids:
            self.loadOtherStatFromCsvFiles(comp_id)

        if comp_id not in self.__all_comp_ids:
            self.__appendExtraFromCcd(comp_id)

        if polypeptide_like is False and polynucleotide_like is False and carbohydrates_like is False:
            polypeptide_like, polynucleotide_like, carbohydrates_like = self.getTypeOfCompId(comp_id)

        cs_stat = self.__get(comp_id)

        if comp_id in self.__aa_comp_ids:
            return [i['atom_id'] for i in cs_stat
                    if i['atom_id'] in ('C', 'CA', 'CB', 'H', 'HA', 'HA2', 'HA3', 'N') and (not excl_minor_atom or (excl_minor_atom and i['primary']))]

        if comp_id in self.__dna_comp_ids:
            return [i['atom_id'] for i in cs_stat
                    if i['atom_id'] in ("C1'", "C2'", "C3'", "C4'", "C5'",
                                        "H1'", "H2'", "H2''", "H3'", "H4'",
                                        "H5'", "H5''",
                                        'P') and (not excl_minor_atom or (excl_minor_atom and i['primary']))]

        if comp_id in self.__rna_comp_ids:
            return [i['atom_id'] for i in cs_stat
                    if i['atom_id'] in ("C1'", "C2'", "C3'", "C4'", "C5'",
                                        "H1'", "H2'", "H3'", "H4'", "H5'", "H5''", "HO2'",
                                        'P') and (not excl_minor_atom or (excl_minor_atom and i['primary']))]

        if polypeptide_like:
            return [i['atom_id'] for i in cs_stat
                    if i['atom_id'] in ('C', 'CA', 'CB', 'H', 'HA', 'HA2', 'HA3', 'N') and (not excl_minor_atom or (excl_minor_atom and i['primary']))]

        if polynucleotide_like:
            return [i['atom_id'] for i in cs_stat
                    if i['atom_id'] in ("C1'", "C2'", "C3'", "C4'", "C5'", "H1'", "H2'", "H2''", "H3'", "H4'", "H5'", "H5''",
                                        'P') and (not excl_minor_atom or 'secondary' not in i or (excl_minor_atom and i['secondary']))]

        if carbohydrates_like:
            return [i['atom_id'] for i in cs_stat
                    if i['atom_id'] in ('C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'H61', 'H62') and (not excl_minor_atom or 'secondary' not in i or (excl_minor_atom and i['secondary']))]

        return []

    def getAromaticAtoms(self, comp_id, excl_minor_atom=False, primary=False):
        """ Return aromatic atoms of a given comp_id.
        """

        if comp_id in emptyValue:
            return []

        if comp_id not in self.__std_comp_ids:
            self.loadOtherStatFromCsvFiles(comp_id)

        if comp_id not in self.__all_comp_ids:
            self.__appendExtraFromCcd(comp_id)

        cs_stat = self.__get(comp_id)

        if comp_id in self.__std_comp_ids or primary:
            return [i['atom_id'] for i in cs_stat
                    if 'aroma' in i['desc'] and (not excl_minor_atom or (excl_minor_atom and i['primary']))]

        return [i['atom_id'] for i in cs_stat
                if 'aroma' in i['desc'] and (not excl_minor_atom or 'secondary' not in i or (excl_minor_atom and i['secondary']))]

    def getMethylAtoms(self, comp_id, excl_minor_atom=False, primary=False):
        """ Return atoms in methyl group of a given comp_id.
        """

        if comp_id in emptyValue:
            return []

        if comp_id not in self.__std_comp_ids:
            self.loadOtherStatFromCsvFiles(comp_id)

        if comp_id not in self.__all_comp_ids:
            self.__appendExtraFromCcd(comp_id)

        cs_stat = self.__get(comp_id)

        if comp_id in self.__std_comp_ids or primary:
            return [i['atom_id'] for i in cs_stat
                    if 'methyl' in i['desc'] and (not excl_minor_atom or (excl_minor_atom and i['primary']))]

        return [i['atom_id'] for i in cs_stat
                if 'methyl' in i['desc'] and (not excl_minor_atom or 'secondary' not in i or (excl_minor_atom and i['secondary']))]

    def getRepresentativeMethylProtons(self, comp_id, excl_minor_atom=False, primary=False):
        """ Return representative protons in methyl group of a given comp_id.
        """

        if comp_id in emptyValue:
            return []

        ends_w_num = [a for a in self.getMethylAtoms(comp_id, excl_minor_atom, primary) if a.startswith('H') and a[-1].isdigit()]
        ends_w_alp = [a for a in self.getMethylAtoms(comp_id, excl_minor_atom, primary) if a.startswith('H') and not a[-1].isdigit()]

        atm_list = []

        if len(ends_w_num) > 0:
            atm_list.extend([a for a in ends_w_num if a.endswith('1')])

        if len(ends_w_alp) > 0:
            min_len = min([len(a) for a in ends_w_alp])
            atm_list.extend([a for a in ends_w_alp if len(a) == min_len])

        return atm_list

    def getNonRepresentativeMethylProtons(self, comp_id, excl_minor_atom=False, primary=False):
        """ Return non-representative protons in methyl group of a given comp_id.
        """

        if comp_id in emptyValue:
            return []

        rep_list = self.getRepresentativeMethylProtons(comp_id, excl_minor_atom, primary)

        return [a for a in self.getMethylAtoms(comp_id, excl_minor_atom, primary) if a.startswith('H') and a not in rep_list]

    def getSideChainAtoms(self, comp_id, excl_minor_atom=False, polypeptide_like=False, polynucleotide_like=False, carbohydrates_like=False):
        """ Return sidechain atoms of a given comp_id.
        """

        if comp_id in emptyValue:
            return []

        if comp_id not in self.__std_comp_ids:
            self.loadOtherStatFromCsvFiles(comp_id)

        if comp_id not in self.__all_comp_ids:
            self.__appendExtraFromCcd(comp_id)

        if polypeptide_like is False and polynucleotide_like is False and carbohydrates_like is False:
            polypeptide_like, polynucleotide_like, carbohydrates_like = self.getTypeOfCompId(comp_id)

        bb_atoms = self.getBackBoneAtoms(comp_id, excl_minor_atom, polypeptide_like, polynucleotide_like, carbohydrates_like)

        try:
            if polypeptide_like:
                bb_atoms.remove('CB')
        except ValueError:
            pass

        cs_stat = self.__get(comp_id)

        if comp_id in self.__std_comp_ids or polypeptide_like:
            return [i['atom_id'] for i in cs_stat
                    if i['atom_id'] not in bb_atoms and (not excl_minor_atom or (excl_minor_atom and i['primary']))]

        return [i['atom_id'] for i in cs_stat
                if i['atom_id'] not in bb_atoms and (not excl_minor_atom or 'secondary' not in i or (excl_minor_atom and i['secondary']))]

    def getPseudoAtoms(self, comp_id, excl_minor_atom=False, primary=False):
        """ Return all pseudo atoms of a give comp_id.
        """

        if comp_id in emptyValue:
            return []

        if comp_id not in self.__std_comp_ids:
            self.loadOtherStatFromCsvFiles(comp_id)

        if comp_id not in self.__all_comp_ids:
            self.__appendExtraFromCcd(comp_id)

        cs_stat = self.__get(comp_id)

        if comp_id in self.__std_comp_ids or primary:
            return [i['atom_id'] for i in cs_stat
                    if (('methyl' in i['desc'] and i['atom_id'][0] == 'H') or 'geminal' in i['desc'] or i['desc'] == 'aroma-opposite')
                    and (not excl_minor_atom or (excl_minor_atom and i['primary']))]

        return [i['atom_id'] for i in cs_stat
                if (('methyl' in i['desc'] and i['atom_id'][0] == 'H') or 'geminal' in i['desc'] or i['desc'] == 'aroma-opposite')
                and (not excl_minor_atom or 'secondary' not in i or (excl_minor_atom and i['secondary']))]

    def loadStatFromCsvFiles(self):
        """ Load all BMRB chemical shift statistics from CSV files.
        """

        csv_files = (self.stat_dir + 'aa_filt.csv', self.stat_dir + 'aa_full.csv',
                     self.stat_dir + 'dna_filt.csv', self.stat_dir + 'dna_full.csv',
                     self.stat_dir + 'rna_filt.csv', self.stat_dir + 'rna_full.csv',
                     self.stat_dir + 'others.csv')

        if any(not os.path.exists(csv_file) for csv_file in csv_files):
            return False

        self.aa_filt = self.loadStatFromCsvFile(self.stat_dir + 'aa_filt.csv', self.aa_threshold)
        self.aa_full = self.loadStatFromCsvFile(self.stat_dir + 'aa_full.csv', self.aa_threshold)

        self.dna_filt = self.loadStatFromCsvFile(self.stat_dir + 'dna_filt.csv', self.na_threshold)
        self.dna_full = self.loadStatFromCsvFile(self.stat_dir + 'dna_full.csv', self.na_threshold)

        self.rna_filt = self.loadStatFromCsvFile(self.stat_dir + 'rna_filt.csv', self.na_threshold)
        self.rna_full = self.loadStatFromCsvFile(self.stat_dir + 'rna_full.csv', self.na_threshold)

        if not self.lazy_others:
            self.others = self.loadStatFromCsvFile(self.stat_dir + 'others.csv', self.aa_threshold, self.na_threshold)

        self.__updateCompIdSet()

        return True

    def loadOtherStatFromCsvFiles(self, comp_id_interest=None):
        """ Load all BMRB chemical shift statistics from CSV files.
        """

        if not self.lazy_others:
            return True

        if comp_id_interest is None:
            self.others = self.loadStatFromCsvFile(self.stat_dir + 'others.csv', self.aa_threshold, self.na_threshold)
            self.__updateCompIdSet()

        elif comp_id_interest not in self.__all_comp_ids and comp_id_interest not in self.__not_comp_ids:
            stat = self.loadStatFromCsvFile(self.stat_dir + 'others.csv', self.aa_threshold, self.na_threshold, comp_id_interest)
            if len(stat) > 0:
                self.others.extend(stat)
                self.__updateCompIdSet()
            else:
                self.__not_comp_ids.add(comp_id_interest)

        return True

    def loadStatFromCsvFile(self, file_name, primary_th, secondary_th=None, comp_id_interest=None):
        """ Load BMRB chemical shift statistics from a given CSV file.
        """

        atm_list = []

        with open(file_name, 'r', encoding='utf-8') as ifp:
            reader = csv.DictReader(ifp)

            for row in reader:

                comp_id = row['comp_id']

                if comp_id_interest is not None and comp_id != comp_id_interest:
                    continue

                if not self.__ccU.updateChemCompDict(comp_id):
                    continue

                _atom_id = row['atom_id']

                # methyl proton group
                if _atom_id.startswith('M'):
                    _atom_id = re.sub(r'^M', 'H', _atom_id)

                    for i in range(1, 4):
                        _row = {}
                        _row['comp_id'] = comp_id
                        _row['atom_id'] = _atom_id + str(i)

                        if not self.__checkAtomNomenclature(_row['atom_id']):
                            continue

                        _row['count'] = int(row['count'])
                        _row['avg'] = float(row['avg'])
                        try:
                            _row['std'] = float(row['std'])
                        except ValueError:
                            _row['std'] = None
                        _row['min'] = float(row['min'])
                        _row['max'] = float(row['max'])
                        _row['desc'] = 'methyl'
                        _row['primary'] = False
                        _row['norm_freq'] = None

                        atm_list.append(_row)

                elif comp_id == 'HEM' and re.match(r'^HM[A-D]$', _atom_id) is not None:  # others.csv dependent code

                    for i in ['', 'A', 'B']:
                        _row = {}
                        _row['comp_id'] = comp_id
                        _row['atom_id'] = _atom_id + i

                        if not self.__checkAtomNomenclature(_row['atom_id']):
                            continue

                        _row['count'] = int(row['count'])
                        _row['avg'] = float(row['avg'])
                        try:
                            _row['std'] = float(row['std'])
                        except ValueError:
                            _row['std'] = None
                        _row['min'] = float(row['min'])
                        _row['max'] = float(row['max'])
                        _row['desc'] = 'methyl'
                        _row['primary'] = False
                        _row['norm_freq'] = None

                        atm_list.append(_row)

                elif comp_id == 'HEB' and (re.match(r'^HM[A-D]1$', _atom_id) is not None or _atom_id == 'HBB1'):  # others.csv dependent code

                    for i in range(1, 4):
                        _row = {}
                        _row['comp_id'] = comp_id
                        _row['atom_id'] = _atom_id[:-1] + str(i)

                        if not self.__checkAtomNomenclature(_row['atom_id']):
                            continue

                        _row['count'] = int(row['count'])
                        _row['avg'] = float(row['avg'])
                        try:
                            _row['std'] = float(row['std'])
                        except ValueError:
                            _row['std'] = None
                        _row['min'] = float(row['min'])
                        _row['max'] = float(row['max'])
                        _row['desc'] = 'methyl'
                        _row['primary'] = False
                        _row['norm_freq'] = None

                        atm_list.append(_row)

                elif comp_id == 'HEC' and (re.match(r'^HM[A-D]$', _atom_id) is not None or re.match(r'^HB[BC]$', _atom_id) is not None):  # others.csv dependent code

                    for i in range(1, 4):
                        _row = {}
                        _row['comp_id'] = comp_id
                        _row['atom_id'] = _atom_id + str(i)

                        if not self.__checkAtomNomenclature(_row['atom_id']):
                            continue

                        _row['count'] = int(row['count'])
                        _row['avg'] = float(row['avg'])
                        try:
                            _row['std'] = float(row['std'])
                        except ValueError:
                            _row['std'] = None
                        _row['min'] = float(row['min'])
                        _row['max'] = float(row['max'])
                        _row['desc'] = 'methyl'
                        _row['primary'] = False
                        _row['norm_freq'] = None

                        atm_list.append(_row)

                # geminal proton group
                elif _atom_id.startswith('Q'):
                    _atom_id = re.sub(r'^Q', 'H', _atom_id)

                    for i in range(1, 4):
                        _row = {}
                        _row['comp_id'] = comp_id
                        _row['atom_id'] = _atom_id + str(i)

                        if not self.__checkAtomNomenclature(_row['atom_id']):
                            continue

                        _row['count'] = int(row['count'])
                        _row['avg'] = float(row['avg'])
                        try:
                            _row['std'] = float(row['std'])
                        except ValueError:
                            _row['std'] = None
                        _row['min'] = float(row['min'])
                        _row['max'] = float(row['max'])
                        _row['desc'] = 'methyl'
                        _row['primary'] = False
                        _row['norm_freq'] = None

                        atm_list.append(_row)

                elif not((comp_id == 'HEM' and re.match(r'^HM[A-D][AB]$', _atom_id) is not None)
                         or (comp_id == 'HEB' and (re.match(r'^HM[A-D][23]$', _atom_id) is not None or re.match(r'^HBB[23]', _atom_id) is not None))
                         or (comp_id == 'HEC' and (re.match(r'^HM[A-D][123]$', _atom_id) is not None or re.match(r'^HB[BC][123]$', _atom_id) is not None))):
                    _row = {}
                    _row['comp_id'] = comp_id
                    _row['atom_id'] = _atom_id

                    if not self.__checkAtomNomenclature(_row['atom_id']):
                        continue

                    _row['count'] = int(row['count'])
                    _row['avg'] = float(row['avg'])
                    try:
                        _row['std'] = float(row['std'])
                    except ValueError:
                        _row['std'] = None
                    _row['min'] = float(row['min'])
                    _row['max'] = float(row['max'])
                    _row['desc'] = 'isolated'
                    _row['primary'] = False
                    _row['norm_freq'] = None

                    atm_list.append(_row)

        comp_ids = set(i['comp_id'] for i in atm_list)

        if secondary_th is not None:  # extract rest of atoms for non-standard residues

            for comp_id in comp_ids:

                if self.__ccU.updateChemCompDict(comp_id):

                    for a in self.__ccU.lastAtomList:

                        if a[self.__ccU.ccaLeavingAtomFlag] == 'Y' or a[self.__ccU.ccaTypeSymbol] not in ('H', 'C', 'N', 'P'):
                            continue

                        if not any(i for i in atm_list if i['comp_id'] == comp_id and i['atom_id'] == a[self.__ccU.ccaAtomId]):

                            _row = {}
                            _row['comp_id'] = comp_id
                            _row['atom_id'] = a[self.__ccU.ccaAtomId]
                            _row['desc'] = 'isolated'
                            _row['primary'] = False
                            _row['norm_freq'] = None
                            _row['count'] = 0

                            atm_list.append(_row)

        self.__detectMethylProtonFromAtomNomenclature(comp_ids, atm_list)
        self.__detectGeminalProtonFromAtomNomenclature(comp_ids, atm_list)

        self.__detectGeminalCarbon(comp_ids, atm_list)
        self.__detectGeminalNitrogen(comp_ids, atm_list)

        self.__detectMajorResonance(comp_ids, atm_list, primary_th, secondary_th)

        return atm_list

    def __appendExtraFromCcd(self, comp_id):
        """ Append atom list as extra residue for a given comp_id.
        """

        if comp_id in emptyValue:
            return

        if comp_id in self.__all_comp_ids or comp_id in self.__ext_comp_ids or not self.__ccU.updateChemCompDict(comp_id):
            return

        atm_list = []

        for a in self.__ccU.lastAtomList:

            if a[self.__ccU.ccaLeavingAtomFlag] == 'Y' or a[self.__ccU.ccaTypeSymbol] not in ('H', 'C', 'N', 'P'):
                continue

            _row = {}
            _row['comp_id'] = comp_id
            _row['atom_id'] = a[self.__ccU.ccaAtomId]
            _row['desc'] = 'isolated'
            _row['primary'] = False
            _row['norm_freq'] = None

            atm_list.append(_row)

        self.__ext_comp_ids.add(comp_id)

        if len(atm_list) == 0:
            return

        comp_ids = [comp_id]

        self.__detectMethylProtonFromAtomNomenclature(comp_ids, atm_list)
        self.__detectGeminalProtonFromAtomNomenclature(comp_ids, atm_list)

        self.__detectGeminalCarbon(comp_ids, atm_list)
        self.__detectGeminalNitrogen(comp_ids, atm_list)

        self.extras.extend(atm_list)

    def __checkAtomNomenclature(self, atom_id):
        """ Check atom nomenclature.
        """

        if any(a[self.__ccU.ccaAtomId] for a in self.__ccU.lastAtomList
               if a[self.__ccU.ccaAtomId] == atom_id and a[self.__ccU.ccaLeavingAtomFlag] != 'Y'):
            return True

        if self.__verbose:
            self.__lfh.write(f"+BMRBChemShiftStat.__checkAtomNomenclature() ++ Error  - Invalid atom nomenclature {atom_id}, comp_id {self.__ccU.lastCompId}\n")

        return False

    def __detectMethylProtonFromAtomNomenclature(self, comp_ids, atm_list):
        """ Detect methyl proton from atom nomenclature.
        """

        for comp_id in comp_ids:
            _list = [i for i in atm_list if i['comp_id'] == comp_id]

            h_list = [i for i in _list if i['atom_id'].startswith('H') and i['desc'] == 'isolated']

            if self.__ccU.updateChemCompDict(comp_id):
                c_h_bonds = collections.Counter([b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                                 if b[self.__ccU.ccbAtomId1].startswith('C') and b[self.__ccU.ccbAtomId2].startswith('H')])

                for k, v in c_h_bonds.items():
                    if v == 3:

                        for i in _list:
                            if i['atom_id'] == k:
                                i['desc'] = 'methyl'

                        for i in h_list:
                            atom_id = i['atom_id']
                            if any(b for b in self.__ccU.lastBonds
                                   if b[self.__ccU.ccbAtomId1] == k and b[self.__ccU.ccbAtomId2] == atom_id):
                                i['desc'] = 'methyl'

            else:
                h_1 = [i['atom_id'][:-1] for i in h_list if i['atom_id'].endswith('1')]
                h_2 = [i['atom_id'][:-1] for i in h_list if i['atom_id'].endswith('2')]
                h_3 = [i['atom_id'][:-1] for i in h_list if i['atom_id'].endswith('3')]
                h_4 = [i['atom_id'][:-1] for i in h_list if i['atom_id'].endswith('4')]

                h_common = set(h_1) & set(h_2) & set(h_3) - set(h_4)

                for h in h_common:
                    for i in h_list:
                        atom_id = i['atom_id']
                        if atom_id in (h + '1', h + '2', h + '3'):
                            i['desc'] = 'methyl'

    def __detectGeminalProtonFromAtomNomenclature(self, comp_ids, atm_list):
        """ Detect geminal proton from atom nomenclature.
        """

        for comp_id in comp_ids:
            _list = [i for i in atm_list if i['comp_id'] == comp_id]

            h_list = [i for i in _list if i['atom_id'].startswith('H') and i['desc'] == 'isolated']

            if self.__ccU.updateChemCompDict(comp_id):
                aro_list = [a[self.__ccU.ccaAtomId] for a in self.__ccU.lastAtomList
                            if a[self.__ccU.ccaAromaticFlag] == 'Y']

                for i in _list:
                    if i['atom_id'] in aro_list:
                        i['desc'] = 'aroma'

                for aro in aro_list:
                    for i in h_list:
                        atom_id = i['atom_id']
                        if any(b for b in self.__ccU.lastBonds
                               if b[self.__ccU.ccbAtomId1] == aro and b[self.__ccU.ccbAtomId2] == atom_id):
                            i['desc'] = 'aroma'

                leaving_atom_list = [a[self.__ccU.ccaAtomId] for a in self.__ccU.lastAtomList
                                     if a[self.__ccU.ccaLeavingAtomFlag] == 'Y']

                cn_h_bonds = collections.Counter([b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                                  if b[self.__ccU.ccbAtomId2].startswith('H') and b[self.__ccU.ccbAtomId2] not in leaving_atom_list])

                h_list = [i for i in _list if i['atom_id'].startswith('H') and i['desc'] == 'isolated']

                for k, v in cn_h_bonds.items():
                    if v == 2:
                        for i in h_list:
                            atom_id = i['atom_id']
                            if any(b for b in self.__ccU.lastBonds
                                   if b[self.__ccU.ccbAtomId1] == k and b[self.__ccU.ccbAtomId2] == atom_id):
                                i['desc'] = 'geminal'

                h_list = [i for i in _list if i['atom_id'].startswith('H') and i['desc'] == 'aroma']

                hvy_c_list = []

                pair = 0
                for h_1 in h_list:
                    if h_1['atom_id'][-1] in ('1', '2', '3'):
                        hvy_1 = next(b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                     if b[self.__ccU.ccbAtomId2] == h_1['atom_id'])
                        for h_2 in h_list:
                            if h_2['atom_id'][-1] in ('1', '2', '3') and h_list.index(h_1) < h_list.index(h_2):
                                hvy_2 = next(b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                             if b[self.__ccU.ccbAtomId2] == h_2['atom_id'])
                                if hvy_1[:-1] == hvy_2[:-1]:
                                    hvy_1_c = set(b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                                  if b[self.__ccU.ccbAromaticFlag] == 'Y' and b[self.__ccU.ccbAtomId2] == hvy_1) |\
                                        set(b[self.__ccU.ccbAtomId2] for b in self.__ccU.lastBonds
                                            if b[self.__ccU.ccbAromaticFlag] == 'Y' and b[self.__ccU.ccbAtomId1] == hvy_1)
                                    hvy_2_c = set(b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                                  if b[self.__ccU.ccbAromaticFlag] == 'Y' and b[self.__ccU.ccbAtomId2] == hvy_2) |\
                                        set(b[self.__ccU.ccbAtomId2] for b in self.__ccU.lastBonds
                                            if b[self.__ccU.ccbAromaticFlag] == 'Y' and b[self.__ccU.ccbAtomId1] == hvy_2)
                                    set_hvy_c = hvy_1_c & hvy_2_c
                                    if len(set_hvy_c) == 1:
                                        for hvy_c in set_hvy_c:
                                            hvy_c_list.append(hvy_c)
                                        pair += 1

                if pair > 0 and pair % 2 == 0:
                    hvy_c_set_in_ring = set()
                    for hvy_c_1 in hvy_c_list:
                        for hvy_c_2 in hvy_c_list:
                            if hvy_c_1 < hvy_c_2:
                                hvy_set_1 = set(b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                                if b[self.__ccU.ccbAromaticFlag] == 'Y' and b[self.__ccU.ccbAtomId2] == hvy_c_1) |\
                                    set(b[self.__ccU.ccbAtomId2] for b in self.__ccU.lastBonds
                                        if b[self.__ccU.ccbAromaticFlag] == 'Y' and b[self.__ccU.ccbAtomId1] == hvy_c_1)
                                hvy_set_2 = set(b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                                if b[self.__ccU.ccbAromaticFlag] == 'Y' and b[self.__ccU.ccbAtomId2] == hvy_c_2) |\
                                    set(b[self.__ccU.ccbAtomId2] for b in self.__ccU.lastBonds
                                        if b[self.__ccU.ccbAromaticFlag] == 'Y' and b[self.__ccU.ccbAtomId1] == hvy_c_2)

                                in_ring = False
                                for hvy_1 in hvy_set_1:
                                    if in_ring:
                                        break
                                    for hvy_2 in hvy_set_2:
                                        if in_ring:
                                            break
                                        if any(b for b in self.__ccU.lastBonds
                                               if b[self.__ccU.ccbAromaticFlag] == 'Y' and b[self.__ccU.ccbAtomId1] == hvy_1 and b[self.__ccU.ccbAtomId2] == hvy_2) or\
                                           any(b for b in self.__ccU.lastBonds
                                               if b[self.__ccU.ccbAromaticFlag] == 'Y' and b[self.__ccU.ccbAtomId1] == hvy_2 and b[self.__ccU.ccbAtomId2] == hvy_1):
                                            in_ring = True
                                if in_ring:
                                    hvy_c_set_in_ring.add(hvy_c_1)
                                    hvy_c_set_in_ring.add(hvy_c_2)

                    for h_1 in h_list:
                        if h_1['atom_id'][-1] in ('1', '2', '3'):
                            hvy_1 = next(b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                         if b[self.__ccU.ccbAtomId2] == h_1['atom_id'])
                            for h_2 in h_list:
                                if h_2['atom_id'][-1] in ('1', '2', '3') and h_list.index(h_1) < h_list.index(h_2):
                                    hvy_2 = next(b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                                 if b[self.__ccU.ccbAtomId2] == h_2['atom_id'])
                                    if hvy_1[:-1] == hvy_2[:-1]:
                                        hvy_1_c = set(b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                                      if b[self.__ccU.ccbAromaticFlag] == 'Y' and b[self.__ccU.ccbAtomId2] == hvy_1) |\
                                            set(b[self.__ccU.ccbAtomId2] for b in self.__ccU.lastBonds
                                                if b[self.__ccU.ccbAromaticFlag] == 'Y' and b[self.__ccU.ccbAtomId1] == hvy_1)
                                        hvy_2_c = set(b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                                      if b[self.__ccU.ccbAromaticFlag] == 'Y' and b[self.__ccU.ccbAtomId2] == hvy_2) |\
                                            set(b[self.__ccU.ccbAtomId2] for b in self.__ccU.lastBonds
                                                if b[self.__ccU.ccbAromaticFlag] == 'Y' and b[self.__ccU.ccbAtomId1] == hvy_2)
                                        if len(hvy_1_c & hvy_2_c & hvy_c_set_in_ring) > 0:
                                            h_1['desc'] = 'aroma-opposite'
                                            h_2['desc'] = 'aroma-opposite'
                                            for i in _list:
                                                if i['atom_id'] == hvy_1 or i['atom_id'] == hvy_2:
                                                    i['desc'] = 'aroma-opposite'

            else:
                h_1 = [i['atom_id'][:-1] for i in h_list if i['atom_id'].endswith('1')]
                h_2 = [i['atom_id'][:-1] for i in h_list if i['atom_id'].endswith('2')]
                h_3 = [i['atom_id'][:-1] for i in h_list if i['atom_id'].endswith('3')]

                c_list = [i for i in _list if i['atom_id'].startswith('C')]

                c_1 = ['H' + i['atom_id'][1:-1] for i in c_list if i['atom_id'].endswith('1')]
                c_2 = ['H' + i['atom_id'][1:-1] for i in c_list if i['atom_id'].endswith('2')]
                c_3 = ['H' + i['atom_id'][1:-1] for i in c_list if i['atom_id'].endswith('3')]

                n_list = [i for i in _list if i['atom_id'].startswith('N')]

                n_1 = ['H' + i['atom_id'][1:-1] for i in n_list if i['atom_id'].endswith('1')]
                n_2 = ['H' + i['atom_id'][1:-1] for i in n_list if i['atom_id'].endswith('2')]
                n_3 = ['H' + i['atom_id'][1:-1] for i in n_list if i['atom_id'].endswith('3')]

                h_common = set(h_1) & set(h_2) - set(h_3)
                cn_common = set(c_1) & set(c_2) | set(c_1) & set(n_2) | set(n_1) & set(c_2)

                for h in h_common:
                    for i in h_list:
                        atom_id = i['atom_id']
                        if atom_id in (h + '1', h + '2'):
                            atom_id = 'N' + i['atom_id'][1:]
                            if not any(n for n in n_list if n['atom_id'] == atom_id):
                                i['desc'] = 'aroma' if h in cn_common and i['avg'] > 5.0 else 'geminal'

                h_common = set(h_2) & set(h_3) - set(h_1)
                cn_common = set(c_2) & set(c_3) | set(c_2) & set(n_3) | set(n_2) & set(c_3)

                for h in h_common:
                    for i in h_list:
                        atom_id = i['atom_id']
                        if atom_id in (h + '2', h + '3'):
                            atom_id = 'N' + i['atom_id'][1:]
                            if not any(n for n in n_list if n['atom_id'] == atom_id):
                                i['desc'] = 'aroma' if h in cn_common and i['avg'] > 5.0 else 'geminal'

                h_list = [i for i in _list if i['atom_id'].startswith('H') and i['desc'] == 'isolated']

                for h in h_list:
                    if h['avg'] > 5.0:
                        atom_id = 'C' + h['atom_id'][1:]
                        if any(c for c in c_list if c['atom_id'] == atom_id and c['avg'] > 95.0 and c['avg'] < 170.0):
                            h['desc'] = 'aroma'

                h_list = [i for i in _list if i['atom_id'].startswith('H') and i['desc'] == 'isolated']

                h_c = [i['atom_id'][:-1] for i in h_list if i['atom_id'].endswith("'") and not i['atom_id'].endswith("''")]
                h_cc = [i['atom_id'][:-2] for i in h_list if i['atom_id'].endswith("''")]

                c_c = ['H' + i['atom_id'][1:-1] for i in c_list if i['atom_id'].endswith("'") and not i['atom_id'].endswith("''")]
                c_cc = ['H' + i['atom_id'][1:-2] for i in c_list if i['atom_id'].endswith("''")]

                h_common = set(h_c) & set(h_cc) & set(c_c) - set(c_cc)

                for h in h_common:
                    for i in h_list:
                        atom_id = i['atom_id']
                        if atom_id in (h + "'", h + "''"):
                            atom_id = 'N' + i['atom_id'][1:]
                            if not any(n for n in n_list if n['atom_id'] == atom_id):
                                i['desc'] = 'geminal'

                h_list = [i for i in _list if i['atom_id'].startswith('H') and i['desc'] == 'aroma']

                h_1 = [i['atom_id'][:-1] for i in h_list if i['atom_id'].endswith('1')]
                h_2 = [i['atom_id'][:-1] for i in h_list if i['atom_id'].endswith('2')]
                h_3 = [i['atom_id'][:-1] for i in h_list if i['atom_id'].endswith('3')]

                h_common = set(h_1) & set(h_2)

                if len(h_common) > 0 and len(h_common) % 2 == 0:
                    for h in h_common:
                        for i in h_list:
                            atom_id = i['atom_id']
                            if atom_id in (h + '1', h + '2'):
                                i['desc'] = 'aroma-opposite'

                h_common = set(h_2) & set(h_3)

                if len(h_common) > 0 and len(h_common) % 2 == 0:
                    for h in h_common:
                        for i in h_list:
                            atom_id = i['atom_id']
                            if atom_id in (h + '2', h + '3'):
                                i['desc'] = 'aroma-opposite'

    def __detectGeminalCarbon(self, comp_ids, atm_list):
        """ Detect geminal carbon from atom nomenclature.
        """

        for comp_id in comp_ids:
            _list = [i for i in atm_list if i['comp_id'] == comp_id]

            if self.__ccU.updateChemCompDict(comp_id):
                methyl_c_list = [i['atom_id'] for i in _list if i['atom_id'].startswith('C') and i['desc'] == 'methyl']

                for methyl_c_1 in methyl_c_list:
                    for methyl_c_2 in methyl_c_list:
                        if methyl_c_list.index(methyl_c_1) < methyl_c_list.index(methyl_c_2):
                            hvy_1_c = set(b[self.__ccU.ccbAtomId2] for b in self.__ccU.lastBonds
                                          if b[self.__ccU.ccbAtomId1] == methyl_c_1 and not b[self.__ccU.ccbAtomId2].startswith('H')) |\
                                set(b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                    if b[self.__ccU.ccbAtomId2] == methyl_c_1 and not b[self.__ccU.ccbAtomId1].startswith('H'))
                            hvy_2_c = set(b[self.__ccU.ccbAtomId2] for b in self.__ccU.lastBonds
                                          if b[self.__ccU.ccbAtomId1] == methyl_c_2 and not b[self.__ccU.ccbAtomId2].startswith('H')) |\
                                set(b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                    if b[self.__ccU.ccbAtomId2] == methyl_c_2 and not b[self.__ccU.ccbAtomId1].startswith('H'))
                            hvy_common = hvy_1_c & hvy_2_c
                            if len(hvy_common) > 0:
                                for hvy_c in hvy_common:
                                    v = len([b for b in self.__ccU.lastBonds
                                             if b[self.__ccU.ccbAtomId1] == hvy_c and b[self.__ccU.ccbAtomId2] in methyl_c_list]) +\
                                        len([b for b in self.__ccU.lastBonds
                                             if b[self.__ccU.ccbAtomId2] == hvy_c and b[self.__ccU.ccbAtomId1] in methyl_c_list])

                                    if v == 2:
                                        for i in _list:
                                            if i['atom_id'] == methyl_c_1 or i['atom_id'] == methyl_c_2:
                                                i['desc'] = 'methyl-geminal'

                                                for methyl_h in [b[self.__ccU.ccbAtomId2] for b in self.__ccU.lastBonds
                                                                 if b[self.__ccU.ccbAtomId1] == methyl_c_1 and b[self.__ccU.ccbAtomId2].startswith('H')]:
                                                    for j in _list:
                                                        if j['atom_id'] == methyl_h:
                                                            j['desc'] = 'methyl-geminal'

                                                for methyl_h in [b[self.__ccU.ccbAtomId2] for b in self.__ccU.lastBonds
                                                                 if b[self.__ccU.ccbAtomId1] == methyl_c_2 and b[self.__ccU.ccbAtomId2].startswith('H')]:
                                                    for j in _list:
                                                        if j['atom_id'] == methyl_h:
                                                            j['desc'] = 'methyl-geminal'

            else:
                methyl_list = ['C' + i['atom_id'][1:-1] for i in _list
                               if i['atom_id'].startswith('H') and i['desc'] == 'methyl' and i['atom_id'].endswith('1')]

                methyl_1 = [i[:-1] for i in methyl_list if i.endswith('1')]
                methyl_2 = [i[:-1] for i in methyl_list if i.endswith('2')]
                methyl_3 = [i[:-1] for i in methyl_list if i.endswith('3')]

                c_list = [i for i in _list if i['atom_id'].startswith('C')]

                for c in c_list:
                    if c['atom_id'] in methyl_list:
                        c['desc'] = 'methyl'
                    elif c['avg'] > 95.0 and c['avg'] < 170.0:
                        c['desc'] = 'aroma'

                methyl_common = set(methyl_1) & set(methyl_2) - set(methyl_3)

                for m in methyl_common:
                    for c in c_list:
                        atom_id = c['atom_id']
                        if atom_id in (m + '1', m + '2'):
                            c['desc'] = 'methyl-geminal'
                            for h in [i for i in _list if i['atom_id'].startswith('H') and i['desc'] == 'methyl' and i['atom_id'].startswith('H' + atom_id[1:])]:
                                h['desc'] = 'methyl-geminal'

                aroma_list = ['C' + i['atom_id'][1:] for i in _list
                              if i['atom_id'].startswith('H') and i['desc'] == 'aroma']

                for c in c_list:
                    if c['atom_id'] in aroma_list:
                        c['desc'] = 'aroma'

                aroma_opposite_list = ['C' + i['atom_id'][1:] for i in _list
                                       if i['atom_id'].startswith('H') and i['desc'] == 'aroma-opposite']

                for c in c_list:
                    if c['atom_id'] in aroma_opposite_list:
                        c['desc'] = 'aroma-opposite'

    def __detectGeminalNitrogen(self, comp_ids, atm_list):
        """ Detect geminal nitrogen from atom nomenclature.
        """

        for comp_id in comp_ids:
            _list = [i for i in atm_list if i['comp_id'] == comp_id]

            geminal_n_list = ['N' + i['atom_id'][1:-1] for i in _list
                              if i['atom_id'].startswith('H') and i['desc'] == 'geminal' and i['atom_id'].endswith('1')]

            if self.__ccU.updateChemCompDict(comp_id):
                for geminal_n_1 in geminal_n_list:
                    for geminal_n_2 in geminal_n_list:
                        if geminal_n_list.index(geminal_n_1) < geminal_n_list.index(geminal_n_2):
                            hvy_1_c = set(b[self.__ccU.ccbAtomId2] for b in self.__ccU.lastBonds
                                          if b[self.__ccU.ccbAtomId1] == geminal_n_1 and not b[self.__ccU.ccbAtomId2].startswith('H')) |\
                                set(b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                    if b[self.__ccU.ccbAtomId2] == geminal_n_1 and not b[self.__ccU.ccbAtomId1].startswith('H'))
                            hvy_2_c = set(b[self.__ccU.ccbAtomId2] for b in self.__ccU.lastBonds
                                          if b[self.__ccU.ccbAtomId1] == geminal_n_2 and not b[self.__ccU.ccbAtomId2].startswith('H')) |\
                                set(b[self.__ccU.ccbAtomId1] for b in self.__ccU.lastBonds
                                    if b[self.__ccU.ccbAtomId2] == geminal_n_2 and not b[self.__ccU.ccbAtomId1].startswith('H'))
                            hvy_common = hvy_1_c & hvy_2_c
                            if len(hvy_common) > 0:
                                for hvy_c in hvy_common:
                                    v = len([b for b in self.__ccU.lastBonds
                                             if b[self.__ccU.ccbAtomId1] == hvy_c and b[self.__ccU.ccbAtomId2] in geminal_n_list]) +\
                                        len([b for b in self.__ccU.lastBonds
                                             if b[self.__ccU.ccbAtomId2] == hvy_c and b[self.__ccU.ccbAtomId1] in geminal_n_list])

                                    if v == 2:
                                        for i in _list:
                                            if i['atom_id'] == geminal_n_1 or i['atom_id'] == geminal_n_2:
                                                i['desc'] = 'geminal'

            else:
                geminal_n_1 = [i[:-1] for i in geminal_n_list if i.endswith('1')]
                geminal_n_2 = [i[:-1] for i in geminal_n_list if i.endswith('2')]
                geminal_n_3 = [i[:-1] for i in geminal_n_list if i.endswith('3')]

                n_list = [i for i in _list if i['atom_id'].startswith('N')]

                for n in n_list:
                    if n['avg'] > 125.0:
                        n['desc'] = 'aroma'
                        atom_id = 'H' + n['atom_id'][1:]
                        try:
                            h = next(i for i in _list if i['atom_id'] == atom_id and i['desc'] == 'isolated')
                            h['desc'] = 'aroma'
                        except StopIteration:
                            pass

                geminal_common = set(geminal_n_1) & set(geminal_n_2) - set(geminal_n_3)

                for g in geminal_common:
                    for n in n_list:
                        atom_id = n['atom_id']
                        if atom_id in (g + '1', g + '2'):
                            n['desc'] = 'geminal'

    def __detectMajorResonance(self, comp_ids, atm_list, primary_th, secondary_th=None):
        """ Detect major resonance based on count of assignments.
        """

        for comp_id in comp_ids:
            _list = [i for i in atm_list if i['comp_id'] == comp_id]

            max_count = max([i['count'] for i in _list])

            for i in _list:
                i['norm_freq'] = float(f"{float(i['count']) / max_count:.3f}")
                if max_count >= self.max_count_th:
                    if i['count'] > max_count * primary_th:
                        i['primary'] = True
                    if (secondary_th is not None) and i['count'] > max_count * secondary_th:
                        i['secondary'] = True

    def writeStatAsPickleFiles(self):
        """ Write all BMRB chemical shift statistics as pickle files.
        """

        write_stat_as_pickle(self.aa_filt, self.stat_dir + 'aa_filt.pkl')
        write_stat_as_pickle(self.aa_full, self.stat_dir + 'aa_full.pkl')

        write_stat_as_pickle(self.dna_filt, self.stat_dir + 'dna_filt.pkl')
        write_stat_as_pickle(self.dna_full, self.stat_dir + 'dna_full.pkl')

        write_stat_as_pickle(self.rna_filt, self.stat_dir + 'rna_filt.pkl')
        write_stat_as_pickle(self.rna_full, self.stat_dir + 'rna_full.pkl')

        self.loadOtherStatFromCsvFiles()

        write_stat_as_pickle(sorted(self.others, key=lambda k: k['comp_id']), self.stat_dir + 'others.pkl')

    def loadStatFromPickleFiles(self):
        """ Load all BMRB chemical shift statistics from pickle files if possible.
        """

        pickle_files = (self.stat_dir + 'aa_filt.pkl', self.stat_dir + 'aa_full.pkl',
                        self.stat_dir + 'dna_filt.pkl', self.stat_dir + 'dna_full.pkl',
                        self.stat_dir + 'rna_filt.pkl', self.stat_dir + 'rna_full.pkl',
                        self.stat_dir + 'others.pkl')

        for pickle_file in pickle_files:
            if not os.path.exists(pickle_file):
                return False

        self.aa_filt = load_stat_from_pickle(self.stat_dir + 'aa_filt.pkl')
        self.aa_full = load_stat_from_pickle(self.stat_dir + 'aa_full.pkl')

        self.dna_filt = load_stat_from_pickle(self.stat_dir + 'dna_filt.pkl')
        self.dna_full = load_stat_from_pickle(self.stat_dir + 'dna_full.pkl')

        self.rna_filt = load_stat_from_pickle(self.stat_dir + 'rna_filt.pkl')
        self.rna_full = load_stat_from_pickle(self.stat_dir + 'rna_full.pkl')

        self.others = load_stat_from_pickle(self.stat_dir + 'others.pkl')

        self.__updateCompIdSet()

        return True

    def __updateCompIdSet(self):
        """ Update set of comp_id having BMRB chemical shift statistics.
        """

        self.__aa_comp_ids = set(i['comp_id'] for i in self.aa_filt)
        self.__dna_comp_ids = set(i['comp_id'] for i in self.dna_filt)
        self.__rna_comp_ids = set(i['comp_id'] for i in self.rna_filt)

        self.__all_comp_ids |= self.__aa_comp_ids
        self.__all_comp_ids |= self.__dna_comp_ids
        self.__all_comp_ids |= self.__rna_comp_ids

        self.__std_comp_ids = copy.copy(self.__all_comp_ids)

        self.__oth_comp_ids = set(i['comp_id'] for i in self.others)

        self.__all_comp_ids |= self.__oth_comp_ids

    def getAtomLikeNameSet(self, excl_minor_atom=False, primary=False, minimum_len=1):
        """ Return atom like names of all standard residues.
        """

        name_set = set()

        name_set.add('HN')
        name_set.add('QR')
        name_set.add('O')

        for comp_id in self.__std_comp_ids:

            name_list = self.getAllAtoms(comp_id, excl_minor_atom, primary)
            methyl_list = self.getMethylAtoms(comp_id, excl_minor_atom, primary)

            for name in name_list:

                if len(name) < minimum_len:
                    continue

                name_set.add(name)

                ambig_code = self.getMaxAmbigCodeWoSetId(comp_id, name)

                if name in methyl_list:
                    _name = name[:-1]
                    if _name[0] == 'H':
                        name_set.add('M' + _name[1:])
                        if ambig_code == 2:
                            name_set.add('QQ' + _name[1])
                        name_set.add(_name + '#')
                        name_set.add(_name + '%')
                        name_set.add(_name + '*')
                    elif ambig_code == 2:
                        name_set.add(_name + '#')
                        name_set.add(_name + '%')
                        name_set.add(_name + '*')

                elif ambig_code >= 2:
                    geminal_name = self.getGeminalAtom(comp_id, name)
                    _name = name[:-1]
                    if _name[0] == 'H':
                        name_set.add('Q' + _name[1:])
                        if geminal_name[:-1].isdigit():
                            name_set.add(_name + '#')
                            name_set.add(_name + '%')
                            name_set.add(_name + '*')
                            name_set.add(_name + 'X')
                            name_set.add(_name + 'Y')

            if self.__ccU.updateChemCompDict(comp_id):

                for a in self.__ccU.lastAtomList:

                    if a[self.__ccU.ccaLeavingAtomFlag] == 'Y':
                        continue

                    name = a[self.__ccU.ccaAtomId]

                    if len(name) < minimum_len:
                        continue

                    name_set.add(name)

        return name_set

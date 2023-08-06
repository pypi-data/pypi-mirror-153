##
# File: NEFTranslator.py
# Date:  02-May-2019  K. Baskaran
#
# Updates:
# 29-Jul-2019  M. Yokochi - support NEFTranslator v1.3.0 and integration into OneDep environment
# 28-Aug-2019  M. Yokochi - report all empty data error as UserWarning
# 11-Oct-2019  K. Baskaran & M. Yokochi - add functions to detect missing mandatory tag (v1.4.0)
# 05-Nov-2019  M. Yokochi - revise error messages for missing mandatory saveframe/loop tags
# 28-Nov-2019  M. Yokochi - implement bi-directional translation, which enables to convert NMR-STAR to NEF (v2.0.0)
# 29-Nov-2019  M. Yokochi - support index pointer from loop to their parent saveframe in NMR-STAR (v2.0.1)
# 11-Dec-2019  M. Yokochi - relax 'smaller-than' and 'larger-than' constraints, which include 'equal-to' constraint (v2.0.2)
# 05-Feb-2020  M. Yokochi - add 'circular-shift' to relax dihedral angle constraint range error (v2.0.3)
# 05-Feb-2020  M. Yokochi - convert 'HN' in amino acids to 'H' while NEF->NMR-STAR translation (v2.0.3)
# 05-Feb-2020  M. Yokochi - rescue NEF atom_id w/o wild card notation in methyl group (v2.0.3)
# 05-Feb-2020  M. Yokochi - relax NEF atom_id that ends with [xy] in methyne/methyl group (v2.0.3)
# 26-Feb-2020  M. Yokochi - additional support for abnormal NEF atom nomenclature, e.g. HDy% in ASN, HEy% in GLN, seen in CCPN_2mtv_docr.nef (v2.0.4)
# 04-Mar-2020  M. Yokochi - support 'default' of key items and 'default-from' of data items (v2.0.4)
# 05-Mar-2020  M. Yokochi - support alternative enumeration definition, 'enum-alt' (v2.0.5, DAOTHER-5485)
# 05-Mar-2020  M. Yokochi - bidirectional convert between restraint_origin (NEF) and Content_type (NMR-STAR) (v2.0.6, DAOTHER-5485)
# 06-Mar-2020  M. Yokochi - fix ambiguity_code mapping from NEF atom nomenclature (v2.0.7)
# 17-Mar-2020  M. Yokochi - fill default value for mandatory saveframe tag (v2.0.8, DAOTHER-5508)
# 18-Mar-2020  M. Yokochi - convert NEF atom nomenclature in dihedral angle/RDC restraint (v2.0.9)
# 18-Mar-2020  M. Yokochi - remove invalid NMR-STAR's Details tag in restraint (v2.0.9)
# 03-Apr-2020  M. Yokochi - remove dependency of lib/atomDict.json and lib/codeDict.json (v2.1.0)
# 03-Apr-2020  M. Yokochi - fill _Atom_chem_shift.Original_PDB_* items (v2.1.0)
# 03-Apr-2020  M. Yokochi - synchronize with coordinates' auth_asym_id and auth_seq_id for NEF deposition (v2.2.0)
# 06-Apr-2020  M. Yokochi - fix crash when sequence alignment is not available. (v2.2.1)
# 10-Apr-2020  M. Yokochi - fix crash in case of format issue (v2.2.2)
# 10-Apr-2020  M. Yokochi - fix typo in alternative enumeration definition (v2.2.2)
# 22-Apr-2020  M. Yokochi - convert comp_id in capital letters (v2.2.3, DAOTHER-5600)
# 22-Apr-2020  M. Yokochi - fix None type object is not iterable error (v2.2.4, DAOTHER-5602)
# 24-Apr-2020  M. Yokochi - fix type mismatch if 'default' value is set (v2.2.5, DAOTHER-5609)
# 24-Apr-2020  M. Yokochi - fix type mismatch if 'default-from' is 'self' (v2.2.5, DAOTHER-5609)
# 24-Apr-2020  M. Yokochi - revise error message in validate_file() (v2.2.6, DAOTHER-5611)
# 25-Apr-2020  M. Yokochi - add 'excl_missing_data' option of check_data() for NMR separated deposition (v2.2.7, DAOTHER-5611)
# 25-Apr-2020  M. Yokochi - fill default value if Entity_assembly_ID is blank (v2.2.8, DAOTHER-5611)
# 28-Apr-2020  M. Yokochi - do not throw ValueError for 'range-float' data type (v2.2.9, DAOTHER-5611)
# 28-Apr-2020  M. Yokochi - extract sequence from CS/MR loop with gap (v2.2.10, DAOTHER-5611)
# 29-Apr-2020  M. Yokochi - support diagnostic message of PyNMRSTAR v2.6.5.1 or later (v2.2.11, DAOTHER-5611)
# 30-Apr-2020  M. Yokochi - fix pseudo atom mapping in ligand (v2.2.12, DAOTHER-5611)
# 14-May-2020  M. Yokochi - revise error message for missing mandatory content (v2.2.13, DAOTHER-5681 and 5682)
# 06-Jun-2020  M. Yokochi - be compatible with pynmrstar v3 (v2.3.0, DAOTHER-5765)
# 19-Jun-2020  M. Yokochi - do not generate invalid restraints include self atom (v2.3.1)
# 26-Jun-2020  M. Yokochi - support bidirectional conversion between _nef_covalent_links and _Bond (v2.4.0)
# 30-Jun-2020  M. Yokochi - skip third party loops and items gracefully (v2.5.0, DAOTHER-5896)
# 30-Jun-2020  M. Yokochi - support bidirectional conversion between _nef_peak and _Peak_row_format (v2.5.0, DAOTHER-5896)
# 08-Jul-2020  M. Yokochi - add support for _Gen_dist_constraint.Distance_val, _RDC_constraint.RDC_val, and _RDC_constraint.RDC_val_err (v2.6.0, DAOTHER-5926)
# 17-Aug-2020  M. Yokochi - add support for residue variant (v2.7.0, DAOTHER-5906)
# 14-Sep-2020  M. Yokochi - add support for pseudo atom in NMR-STAR (v2.8.0, DAOTHER-6128)
# 17-Sep-2020  M. Yokochi - do not convert atom name between NEF and NMR-STAR, which ends with apostrophe (v2.8.0, DAOTHER-6128)
# 18-Sep-2020  M. Yokochi - bug fix release for negative sequence numbers (v2.8.1, DAOTHER-6128)
# 28-Sep-2020  M. Yokochi - fix chain_code mapping in NEF MR loops in case that there is no CS assignment (v2.8.2, DAOTHER-6128)
# 29-Sep-2020  M. Yokochi - sort numeric string in a list of chain_id while NMR-STAR to NEF conversion (v2.8.3, DAOTHER-6128)
# 06-Sep-2020  M. Yokochi - improve stability against the presence of undefined chain_id in loops (v2.8.4, DAOTHER-6128)
# 12-Oct-2020  M. Yokochi - add support for spectral peak conversion from NMR-STAR canonical loops to NEF (v2.9.0, DAOTHER-6128)
# 11-Nov-2020  M. Yokochi - fix crash while translation due to invalid seq_id (v2.9.1)
# 11-Nov-2020  M. Yokochi - append _nef_sequence.index even if _Chem_comp_assembly.NEF_index does not exist (v2.9.2, DAOTHER-6128)
# 19-Nov-2020  M. Yokochi - add support for HEM, HEB, HEC methyl groups (v2.9.3, DAOTHER-6366)
# 25-Jan-2021  M. Yokochi - add 'positive-int-as-str' value type to simplify code for Entity_assembly_ID, and chain_code (v2.9.4)
# 04-Feb-2021  M. Yokochi - support 3 letter chain code (v2.9.5, DAOTHER-5896, DAOTHER-6128, BMRB entry: 16812, PDB ID: 6kae)
# 10-Mar-2021  M. Yokochi - block NEF deposition missing '_nef_sequence' category and turn off salvage routine for the case (v2.9.6, DAOTHER-6694)
# 10-Mar-2021  M. Yokochi - add support for audit loop in NEF (v2.9.7, DAOTHER-6327)
# 25-Mar-2021  M. Yokochi - fix crash during NMR-STAR to NEF atom name conversion (v2.9.8, DAOTHER-6128,
#                           bmrb_id: 15879, pdb_id: 2k6r, comp_id: DNS, nef_atom_id: Hx%, Hy% point to [H11A, H12, H13],
#                           [H21, H22, H23], respectively, but SHOULD NOT to H10, H11, H[ABCDE][23])
# 14-May-2021  M. Yokochi - add support for PyNMRSTAR v3.1.1 (DAOTHER-6693)
# 14-May-2021  M. Yokochi - remove empty loop for Entity_deleted_atom category in NMR-STAR to NEF conversion (v2.10.0)
# 23-Jun-2021  M. Yokochi - fix error in handling lower/upper linear limits (v2.10.1, DAOTHER-6963)
# 28-Jun-2021  M. Yokochi - revise error message for sequence mismatch in a loop (v2.10.2, DAOTHER-7103)
# 29-Jun-2021  M. Yokochi - add support for PyNMRSTAR v3.2.0 (v2.10.3, DAOTHER-7107)
# 16-Sep-2021  M. Yokochi - report an empty loop case of CS/MR data as an error (v2.10.4, D_1292117503, DAOTHER-7318)
# 13-Oct-2021  M. Yokochi - code revision according to PEP8 using Pylint (v2.11.0, DAOTHER-7389, issue #5)
# 14-Oct-2021  M. Yokochi - remove unassigned chemical shifts, clear incompletely assigned spectral peaks (v2.11.1, DAOTHER-7389, issue #3)
# 19-Oct-2021  M. Yokochi - add NMR-STAR format normalizer for conventional CS deposition using a single file (v3.0.0, DAOTHER-7344, 7355, 7389 issue #4, 7407)
# 27-Oct-2021  M. Yokochi - utilize Auth_asym_ID* tag for chain_id if Entity_assembly_ID* is not available (v3.0.1, DAOTHER-7421)
# 28-Oct-2021  M. Yokochi - use simple dictionary for return messaging, instead of JSON dump/load (v3.0.2)
# 28-Oct-2021  M. Yokochi - resolve case-insensitive saveframe name collision for CIF (v3.0.3, DAOTHER-7389, issue #4)
# 16-Nov-2021  M. Yokochi - map alphabet code of Entity_assembly_ID to valid integer (v3.0.4, DAOTHER-7475)
# 13-Dec-2021  M. Yokochi - fill list id (e.g. Assigned_chem_shift_list_ID) using a given saveframe counter (parent_pointer) just in case (v3.0.5, DAOTHER-7465, issue #2)
# 15-Dec-2021  M. Yokochi - fix TypeError: unsupported operand type(s) for -: 'NoneType' and 'set' (v3.0.6, DAOTHER-7545)
# 22-Dec-2021  M. Yokochi - extend validate_file() for uploading NMR restraint files in NMR-STAR format (v3.0.7, DAOTHER-7545, issue #2)
# 02-Mar-2022  M. Yokochi - revise logging and overall code revision (v3.1.0)
# 12-Apr-2022  M. Yokochi - add get_valid_star_atom_in_xplor(), which translates XPLOR atom name to IUPAC one (v3.1.1, NMR restraint remediation, DAOTHER-7407)
# 13-Apr-2022  M. Yokochi - use auth_*_id scheme preferentially in combined format translation (v3.1.2, NMR restraint remediation)
# 02-May-2022  M. Yokochi - remediate inconsistent _Atom_chem_shift.Chem_comp_ID tag values in reference to _Atom_chem_shift.Seq_ID (v3.1.3, NMR restraint remediation)
##
""" Bi-directional translator between NEF and NMR-STAR
    @author: Kumaran Baskaran, Masashi Yokochi
"""
import sys
import os
import ntpath
import logging
import re
import csv
import itertools
import copy
import pynmrstar

from packaging import version

try:
    from wwpdb.utils.nmr.AlignUtil import (emptyValue, trueValue, monDict3,
                                           letterToDigit, indexToLetter)
    from wwpdb.utils.nmr.ChemCompUtil import ChemCompUtil
    from wwpdb.utils.nmr.BMRBChemShiftStat import BMRBChemShiftStat
except ImportError:
    from nmr.AlignUtil import (emptyValue, trueValue, monDict3,
                               letterToDigit, indexToLetter)
    from nmr.ChemCompUtil import ChemCompUtil
    from nmr.BMRBChemShiftStat import BMRBChemShiftStat

__version__ = '3.1.3'

__pynmrstar_v3_2__ = version.parse(pynmrstar.__version__) >= version.parse("3.2.0")
__pynmrstar_v3_1__ = version.parse(pynmrstar.__version__) >= version.parse("3.1.0")
__pynmrstar_v3__ = version.parse(pynmrstar.__version__) >= version.parse("3.0.0")

logging.getLogger().setLevel(logging.ERROR)  # set level for pynmrstar

# supported version
NEF_VERSION = '1.1'


NMR_STAR_VERSION = '3.2.6.0'

# format name
NEF_FORMAT_NAME = 'nmr_exchange_format'


# NEF boolean values
NEF_BOOLEAN_VALUES = ('true', 'false')


# NMR-STAR boolean values
STAR_BOOLEAN_VALUES = ('yes', 'no')


# paramagnetic elements, except for Oxygen
PARAMAGNETIC_ELEMENTS = ('LI', 'NA', 'MG', 'AL', 'K', 'CA', 'SC', 'TI', 'V', 'MN', 'RB', 'SR',
                         'Y', 'ZR', 'NB', 'MO', 'TC', 'RU', 'RH', 'PD', 'SN', 'CS', 'BA', 'LA',
                         'CE', 'PR', 'ND', 'PM', 'SM', 'EU', 'GD', 'TB', 'DY', 'HO', 'ER', 'TM',
                         'YB', 'LU', 'HF', 'TA', 'W', 'RE', 'OS', 'IR', 'PT', 'FR', 'RA', 'AC')


# ferromagnetic elements
FERROMAGNETIC_ELEMENTS = ('CR', 'FE', 'CO', 'NI')


# non-metal elements
NON_METAL_ELEMENTS = ('H', 'C', 'N', 'O', 'P', 'S', 'SE')


# isotope numbers of NMR observable nucleus
ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS = {'H': [1, 2, 3],
                                   'C': [13],
                                   'N': [15, 14],
                                   'O': [17],
                                   'P': [31],
                                   'S': [33],
                                   'F': [19],
                                   'CD': [113, 111],
                                   'CA': [43]
                                   }


# nucleus with half spin
HALF_SPIN_NUCLEUS = ('H', 'C', 'N', 'P', 'F', 'CD')


# allowed BMRB ambiguity codes
ALLOWED_AMBIGUITY_CODES = (1, 2, 3, 4, 5, 6, 9)


ALLOWED_ISOTOPE_NUMBERS = []
for isotopeNums in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.values():
    ALLOWED_ISOTOPE_NUMBERS.extend(isotopeNums)


# limit number of dimensions
MAX_DIM_NUM_OF_SPECTRA = 16


# data items in _Entity_deleted_atom category of NMR-STAR
ENTITY_DELETED_ATOM_ITEMS = ['ID', 'Entity_assembly_ID', 'Comp_index_ID', 'Comp_ID', 'Atom_ID',
                             'Auth_entity_assembly_ID', 'Auth_seq_ID', 'Auth_comp_ID', 'Auth_atom_ID', 'Assembly_ID']

# integer pattern
intPattern = re.compile(r'^([+-]?[1-9]\d*|0)$')


# bad pattern
badPattern = re.compile(r'.*[\!\$\&\(\)\=\~\^\\\|\`\@\{\}\[\]\;\:\<\>\,\/].*')


# alternative dictionary of constraint type
altDistanceConstraintType = {'nef': {'NOE': 'noe',
                                     'NOE build-up': 'noe_build_up',
                                     'noe build-up': 'noe_build_up',
                                     'NOE buildup': 'noe_build_up',
                                     'noe buildup': 'noe_build_up',
                                     'NOE build up': 'noe_build_up',
                                     'noe build up': 'noe_build_up',
                                     'noe not seen': 'noe_not_seen',
                                     'ROE': 'roe',
                                     'roe build-up': 'roe_build_up',
                                     'ROE buildup': 'roe_build_up',
                                     'roe buildup': 'roe_build_up',
                                     'ROE build up': 'roe_build_up',
                                     'roe build up': 'roe_build_up',
                                     'hydrogen bond': 'hbond',
                                     'Hbond': 'hbond',
                                     'HBond': 'hbond',
                                     'H-bond': 'hbond',
                                     'h-bond': 'hbond',
                                     'H-Bond': 'hbond',
                                     'Hydrogen bond': 'hbond',
                                     'disulfide bond': 'disulfide_bond',
                                     'Disulfide bond': 'disulfide_bond',
                                     'S-S bond': 'disulfide_bond',
                                     'SS bond': 'disulfide_bond',
                                     'SS-bond': 'disulfide_bond',
                                     'disulfide bridge': 'disulfide_bond',
                                     'Disulfide bridge': 'disulfide_bond',
                                     'paramagnetic relaxation': 'pre',
                                     'PRE': 'pre',
                                     'Paramagnetic relaxation': 'pre',
                                     'paramagnetic relaxation enhancement': 'pre',
                                     'Paramagnetic relaxation enhancement': 'pre',
                                     'general distance': 'undefined',
                                     'distance': 'undefined',
                                     'Mutation': 'mutation',
                                     'chemical shift perturbation': 'shift_perturbation',
                                     'shift perturbation': 'shift_perturbation',
                                     'chem shift perturbation': 'shift_perturbation',
                                     'CS perturbation': 'shift_perturbation',
                                     'csp': 'shift_perturbation',
                                     'CSP': 'shift_perturbation'
                                     },
                             'nmr-star': {'noe': 'NOE',
                                          'noe_build_up': 'NOE build-up',
                                          'noe build-up': 'NOE build-up',
                                          'NOE buildup': 'NOE build-up',
                                          'noe buildup': 'NOE build-up',
                                          'NOE build up': 'NOE build-up',
                                          'noe build up': 'NOE build-up',
                                          'noe_not_seen': 'NOE not seen',
                                          'noe not seen': 'NOE not seen',
                                          'roe': 'ROE',
                                          'roe_build_up': 'ROE build-up',
                                          'roe build-up': 'ROE build-up',
                                          'ROE buildup': 'ROE build-up',
                                          'roe buildup': 'ROE build-up',
                                          'ROE build up': 'ROE build-up',
                                          'roe build up': 'ROE build-up',
                                          'hbond': 'hydrogen bond',
                                          'Hbond': 'hydrogen bond',
                                          'HBond': 'hydrogen bond',
                                          'H-bond': 'hydrogen bond',
                                          'h-bond': 'hydrogen bond',
                                          'H-Bond': 'hydrogen bond',
                                          'Hydrogen bond': 'hydrogen bond',
                                          'disulfide_bond': 'disulfide bond',
                                          'Disulfide bond': 'disulfide bond',
                                          'S-S bond': 'disulfide bond',
                                          'SS bond': 'disulfide bond',
                                          'SS-bond': 'disulfide bond',
                                          'disulfide bridge': 'disulfide bond',
                                          'Disulfide bridge': 'disulfide bond',
                                          'PRE': 'paramagnetic relaxation',
                                          'pre': 'paramagnetic relaxation',
                                          'Paramagnetic relaxation': 'paramagnetic relaxation',
                                          'paramagnetic relaxation enhancement': 'paramagnetic relaxation',
                                          'Paramagnetic relaxation enhancement': 'paramagnetic relaxation',
                                          'Mutation': 'mutation',
                                          'unknown': 'general distance',
                                          'undefined': 'general distance',
                                          'shift_perturbation': 'chemical shift perturbation',
                                          'shift perturbation': 'chemical shift perturbation',
                                          'chem shift perturbation': 'chemical shift perturbation',
                                          'CS perturbation': 'chemical shift perturbation',
                                          'csp': 'chemical shift perturbation',
                                          'CSP': 'chemical shift perturbation'
                                          }
                             }


altDihedralAngleConstraintType = {'nef': {'J-couplings': 'jcoupling',
                                          'j-couplings': 'jcoupling',
                                          'J couplings': 'jcoupling',
                                          'j couplings': 'jcoupling',
                                          'Jcouplings': 'jcoupling',
                                          'jcouplings': 'jcoupling',
                                          'J-coupling': 'jcoupling',
                                          'j-coupling': 'jcoupling',
                                          'J coupling': 'jcoupling',
                                          'j coupling': 'jcoupling',
                                          'Jcoupling': 'jcoupling',
                                          'chemical shift': 'chemical_shift',
                                          'Chemical shift': 'chemical_shift',
                                          'Chemical_shift': 'chemical_shift',
                                          'chemical shifts': 'chemical_shift',
                                          'Chemical shifts': 'chemical_shift',
                                          'Chemical_shifts': 'chemical_shift',
                                          'backbone chemical shifts': 'chemical_shift',
                                          'Backbone chemical shifts': 'chemical_shift',
                                          'Mainchain chemical shifts': 'chemical_shift',
                                          'mainchain chemical shifts': 'chemical_shift',
                                          'Main chain chemical shifts': 'chemical_shift',
                                          'main chain chemical shifts': 'chemical_shift',
                                          'bb chemical shifts': 'chemical_shift',
                                          'BB chemical shifts': 'chemical_shift',
                                          'backbone chemical shift': 'chemical_shift',
                                          'Backbone chemical shift': 'chemical_shift',
                                          'Mainchain chemical shift': 'chemical_shift',
                                          'mainchain chemical shift': 'chemical_shift',
                                          'Main chain chemical shift': 'chemical_shift',
                                          'main chain chemical shift': 'chemical_shift',
                                          'bb chemical shift': 'chemical_shift',
                                          'BB chemical shift': 'chemical_shift',
                                          'backbone chem shifts': 'chemical_shift',
                                          'Backbone chem shifts': 'chemical_shift',
                                          'Mainchain chem shifts': 'chemical_shift',
                                          'mainchain chem shifts': 'chemical_shift',
                                          'Main chain chem shifts': 'chemical_shift',
                                          'main chain chem shifts': 'chemical_shift',
                                          'bb chem shifts': 'chemical_shift',
                                          'BB chem shifts': 'chemical_shift',
                                          'backbone chem shift': 'chemical_shift',
                                          'Backbone chem shift': 'chemical_shift',
                                          'Mainchain chem shift': 'chemical_shift',
                                          'mainchain chem shift': 'chemical_shift',
                                          'Main chain chem shift': 'chemical_shift',
                                          'main chain chem shift': 'chemical_shift',
                                          'bb chem shift': 'chemical_shift',
                                          'BB chem shift': 'chemical_shift',
                                          'backbone cs': 'chemical_shift',
                                          'Backbone cs': 'chemical_shift',
                                          'Mainchain cs': 'chemical_shift',
                                          'mainchain cs': 'chemical_shift',
                                          'Main chain cs': 'chemical_shift',
                                          'main chain cs': 'chemical_shift',
                                          'bb cs': 'chemical_shift',
                                          'BB cs': 'chemical_shift',
                                          'backbone CS': 'chemical_shift',
                                          'Backbone CS': 'chemical_shift',
                                          'Mainchain CS': 'chemical_shift',
                                          'mainchain CS': 'chemical_shift',
                                          'Main chain CS': 'chemical_shift',
                                          'main chain CS': 'chemical_shift',
                                          'bb CS': 'chemical_shift',
                                          'BB CS': 'chemical_shift',
                                          'TALOS': 'chemical_shift',
                                          'talos': 'chemical_shift',
                                          'TALOS+': 'chemical_shift',
                                          'talos+': 'chemical_shift',
                                          'TALOS-N': 'chemical_shift',
                                          'talos-n': 'chemical_shift'
                                          },
                                  'nmr-star': {'jcoupling': 'J-couplings',
                                               'Jcoupling': 'J-couplings',
                                               'jcouplings': 'J-couplings',
                                               'Jcouplings': 'J-couplings',
                                               'j-couplings': 'J-couplings',
                                               'J couplings': 'J-couplings',
                                               'j couplings': 'J-couplings',
                                               'J-coupling': 'J-couplings',
                                               'j-coupling': 'J-couplings',
                                               'J coupling': 'J-couplings',
                                               'j coupling': 'J-couplings',
                                               'chemical_shift': 'backbone chemical shifts',
                                               'Chemical_shift': 'backbone chemical shifts',
                                               'chemical_shifts': 'backbone chemical shifts',
                                               'Chemical_shifts': 'backbone chemical shifts',
                                               'chemical shift': 'backbone chemical shifts',
                                               'Chemical shift': 'backbone chemical shifts',
                                               'chemical shifts': 'backbone chemical shifts',
                                               'Chemical shifts': 'backbone chemical shifts',
                                               'Backbone chemical shifts': 'backbone chemical shifts',
                                               'Mainchain chemical shifts': 'backbone chemical shifts',
                                               'mainchain chemical shifts': 'backbone chemical shifts',
                                               'Main chain chemical shifts': 'backbone chemical shifts',
                                               'main chain chemical shifts': 'backbone chemical shifts',
                                               'bb chemical shifts': 'backbone chemical shifts',
                                               'BB chemical shifts': 'backbone chemical shifts',
                                               'backbone chemical shift': 'backbone chemical shifts',
                                               'Backbone chemical shift': 'backbone chemical shifts',
                                               'Mainchain chemical shift': 'backbone chemical shifts',
                                               'mainchain chemical shift': 'backbone chemical shifts',
                                               'Main chain chemical shift': 'backbone chemical shifts',
                                               'main chain chemical shift': 'backbone chemical shifts',
                                               'bb chemical shift': 'backbone chemical shifts',
                                               'BB chemical shift': 'backbone chemical shifts',
                                               'backbone chem shifts': 'backbone chemical shifts',
                                               'Backbone chem shifts': 'backbone chemical shifts',
                                               'Mainchain chem shifts': 'backbone chemical shifts',
                                               'mainchain chem shifts': 'backbone chemical shifts',
                                               'Main chain chem shifts': 'backbone chemical shifts',
                                               'main chain chem shifts': 'backbone chemical shifts',
                                               'bb chem shifts': 'backbone chemical shifts',
                                               'BB chem shifts': 'backbone chemical shifts',
                                               'backbone chem shift': 'backbone chemical shifts',
                                               'Backbone chem shift': 'backbone chemical shifts',
                                               'Mainchain chem shift': 'backbone chemical shifts',
                                               'mainchain chem shift': 'backbone chemical shifts',
                                               'Main chain chem shift': 'backbone chemical shifts',
                                               'main chain chem shift': 'backbone chemical shifts',
                                               'bb chem shift': 'backbone chemical shifts',
                                               'BB chem shift': 'backbone chemical shifts',
                                               'backbone cs': 'backbone chemical shifts',
                                               'Backbone cs': 'backbone chemical shifts',
                                               'Mainchain cs': 'backbone chemical shifts',
                                               'mainchain cs': 'backbone chemical shifts',
                                               'Main chain cs': 'backbone chemical shifts',
                                               'main chain cs': 'backbone chemical shifts',
                                               'bb cs': 'backbone chemical shifts',
                                               'BB cs': 'backbone chemical shifts',
                                               'backbone CS': 'backbone chemical shifts',
                                               'Backbone CS': 'backbone chemical shifts',
                                               'Mainchain CS': 'backbone chemical shifts',
                                               'mainchain CS': 'backbone chemical shifts',
                                               'Main chain CS': 'backbone chemical shifts',
                                               'main chain CS': 'backbone chemical shifts',
                                               'bb CS': 'backbone chemical shifts',
                                               'BB CS': 'backbone chemical shifts',
                                               'TALOS': 'backbone chemical shifts',
                                               'talos': 'backbone chemical shifts',
                                               'TALOS+': 'backbone chemical shifts',
                                               'talos+': 'backbone chemical shifts',
                                               'TALOS-N': 'backbone chemical shifts',
                                               'talos-n': 'backbone chemical shifts'
                                               }
                                  }


altRdcConstraintType = {'nef': {'RDC': 'measured',
                                'rdc': 'measured'
                                },
                        'nmr-star': {'rdc': 'RDC',
                                     'measured': 'RDC'
                                     }
                        }


def get_lp_tag(lp_data, tags):
    """ Return the selected loop tags by row as a list of lists.
    """

    return lp_data.get_tag(tags) if __pynmrstar_v3__ else lp_data.get_data_by_tag(tags)


def get_first_sf_tag(sf_data=None, tag=None):
    """ Return the first value of a given saveframe tag.
        @return: The first tag value, empty string otherwise.
    """

    if sf_data is None or tag is None:
        return ''

    array = sf_data.get_tag(tag)

    if len(array) == 0:
        return ''

    return array[0]


def get_idx_msg(idx_tag_ids, tags, ent):
    """ Return description about current index.
        @author: Masashi Yokochi
        @return: description
    """

    try:

        idx_msg = ''

        if len(idx_tag_ids) > 0:
            for _j in idx_tag_ids:
                idx_msg += tags[_j] + " " + str(ent[tags[_j]]) + ", "

            idx_msg = "[Check row of " + idx_msg[:-2] + "] "

        return idx_msg

    except KeyError:
        return ''


def is_empty_loop(star_data, lp_category, data_type):
    """ Return whether one of specified loops is empty loop.
        @return: True for empty loop exists, False otherwise
    """

    if data_type == 'Entry':
        loops = star_data.get_loops_by_category(lp_category)

        return any(len(loop.data) == 0 for loop in loops)

    if data_type == 'Saveframe':
        if __pynmrstar_v3_2__:
            loop = star_data.get_loop(lp_category)
        else:
            loop = star_data.get_loop_by_category(lp_category)

        return len(loop.data) == 0

    return len(star_data.data) == 0


def count_non_empty_loops(star_data, lp_category, data_type):
    """ Return the number of non-empty loops.
        @return: the number of non-empty loops.
    """

    if data_type == 'Entry':
        loops = star_data.get_loops_by_category(lp_category)

        return sum(len(loop.data) > 0 for loop in loops)

    if data_type == 'Saveframe':
        if __pynmrstar_v3_2__:
            loop = star_data.get_loop(lp_category)
        else:
            loop = star_data.get_loop_by_category(lp_category)

        return 0 if len(loop.data) == 0 else 1

    return 0 if len(star_data.data) == 0 else 1


def get_sf_tag_values_with_empty_loop(star_data, lp_category, sf_category):
    """ Return list of saveframe tag values with empty loop.
        @return: list of saveframe tag values
    """

    sf_framecodes = []

    for sf_data in star_data.get_saveframes_by_category(sf_category):

        if __pynmrstar_v3_2__:
            loop = sf_data.get_loop(lp_category)
        else:
            loop = sf_data.get_loop_by_category(lp_category)

        if len(loop.data) == 0:
            sf_framecodes.append(get_first_sf_tag(sf_data, 'sf_framecode'))

    return sf_framecodes


def is_empty(array):
    """ Return whether the array contains empty data.
        @author: Masashi Yokochi
        @return: True for empty data in the array, False otherwise
    """

    return any(d in emptyValue for d in array)


def is_data(array):
    """ Return whether the array consists of no empty data.
        @author: Masashi Yokochi
        @return: True for no empty data in the array, False for empty data
    """

    return not any(d in emptyValue for d in array)


def is_good_data(array):
    """ Return whether the array consists of good pattern data (neither empty nor bad pattern).
        @author: Masashi Yokochi
        @return: True for good data in the array, False otherwise
    """

    return not any(d in emptyValue or badPattern.match(d) for d in array)


class NEFTranslator:
    """ Bi-directional translator between NEF and NMR-STAR
    """

    def __init__(self, verbose=False, log=sys.stderr, ccU=None, csStat=None):
        self.__verbose = verbose
        self.__lfh = log

        # whether to enable remediation routine
        self.__remediation_mode = False

        libDirPath = os.path.dirname(__file__) + '/lib/'

        self.tagMap = self.load_csv_data(libDirPath + 'NEF_NMRSTAR_equivalence.csv', transpose=True)
        self.nefMandatoryTag = self.load_csv_data(libDirPath + 'NEF_mandatory.csv')
        self.starMandatoryTag = self.load_csv_data(libDirPath + 'NMR-STAR_mandatory.csv')

        # whether to replace zero by empty if 'void-zero' is set
        self.replace_zero_by_null_in_case = False
        # whether to insert _Atom_chem_shift.Original_PDB_* items
        self.insert_original_pdb_cs_items = True

        # temporary dictionaries used in translation
        self.authChainId = None
        self.authSeqMap = None
        self.selfSeqMap = None
        self.atomIdMap = None

        self.star2NefChainMapping = None
        self.star2CifChainMapping = None

        # CCD accessing utility
        self.__ccU = ChemCompUtil(self.__verbose, self.__lfh) if ccU is None else ccU

        # BMRB chemical shift statistics
        self.__csStat = BMRBChemShiftStat(self.__verbose, self.__lfh) if csStat is None else csStat

        # readable item type
        self.readableItemType = {'str': 'a string',
                                 'bool': 'a boolean value',
                                 'int': 'an integer',
                                 'index-int': 'an unique positive integer',
                                 'positive-int': 'a positive integer',
                                 'positive-int-as-str': 'a positive integer',
                                 'pointer-index': 'an integer acting as a pointer to the parent item',
                                 'float': 'a floating point number',
                                 'positive-float': 'a positive floating point number',
                                 'range-float': 'a floating point number in a specific range',
                                 'enum': 'an enumeration value',
                                 'enum-int': 'an enumeration value restricted to integers'}

    def set_remediation(self, flag):
        """ Set remediation mode.
        """

        self.__remediation_mode = flag

    def load_csv_data(self, csv_file, transpose=False):
        """ Load CSV data to list.
            @param cvs_file: input CSV file path
            @param transpose: transpose CSV data
            @return: list object
        """

        data_map = []

        try:
            data = []

            with open(csv_file, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file, delimiter=',')

                for r in csv_reader:
                    if r[0][0] != '#':
                        data.append(r)

            data_map = list(map(list, zip(*data))) if transpose else data

        except Exception as e:
            self.__lfh.write(f"+NEFTranslator.load_csv_data() ++ Error  - {str(e)}\n")

        return data_map

    def read_input_file(self, in_file):  # pylint: disable=no-self-use
        """ Read input NEF/NMR-STAR file.
            @param in_file: input NEF/NMR-STAR file path
            @return: status, Entry/Saveframe/Loop data type or message, data object
        """

        is_ok = True
        star_data = None

        try:
            star_data = pynmrstar.Entry.from_file(in_file)
            msg = 'Entry'

        except Exception as e1:

            try:
                star_data = pynmrstar.Saveframe.from_file(in_file)
                msg = 'Saveframe'

            except Exception as e2:

                try:
                    star_data = pynmrstar.Loop.from_file(in_file)
                    msg = 'Loop'

                except Exception as e3:

                    is_ok = False

                    if __pynmrstar_v3_1__:
                        if 'The Sf_framecode tag cannot be different from the saveframe name.' in str(e2):
                            msg = str(e2)
                        elif "Invalid loop. Loops must start with the 'loop_' keyword." not in str(e3) and\
                             "Invalid token found in loop contents" not in str(e3) and\
                             "Illegal value: 'loop_'" not in str(e3):
                            msg = str(e3)
                        else:
                            msg = str(e1)

                    elif version.parse(pynmrstar.__version__) >= version.parse("2.6.5.1"):
                        if "Invalid loop. Loops must start with the 'loop_' keyword." not in str(e3):
                            msg = str(e3)
                        else:
                            msg = str(e1)

                    else:
                        if 'internaluseyoushouldntseethis_frame' not in str(e3):
                            msg = str(e3)
                        else:
                            msg = str(e1)

        return is_ok, msg, star_data

    def check_mandatory_tags(self, in_file=None, file_type=None):
        """ Returns list of missing mandatory saveframe/loop tags of the input file.
            @change: detect missing mandatory saveframe tags in Saveframe/Loop data as well as Entry data by Masashi Yokochi
            @param in_file: input NEF/NMR-STAR file path
            @param file_type: input file type either 'nef' or 'nmr-star'
            @return: list of missing mandatory saveframe tags, list of missing mandatory loop tags
        """

        mandatoryTag = self.nefMandatoryTag if file_type == 'nef' else self.starMandatoryTag

        missing_sf_tags = []
        missing_lp_tags = []

        try:
            star_data = pynmrstar.Entry.from_file(in_file)

            sf_list = [sf.category for sf in star_data.frame_list]

            for _tag in mandatoryTag:

                if _tag[0][0] == '_' and _tag[1] == 'yes':

                    try:
                        tags = star_data.get_tags([_tag[0]])
                        if len(tags[_tag[0]]) == 0 and _tag[0][1:].split('.')[0] in sf_list:
                            missing_sf_tags.append(_tag[0])
                    except:  # ValueError:  # noqa: E722 pylint: disable=bare-except
                        missing_lp_tags.append(_tag[0])

        except:  # ValueError:  # noqa: E722 pylint: disable=bare-except

            try:
                star_data = pynmrstar.Saveframe.from_file(in_file)

                for _tag in mandatoryTag:

                    if _tag[0][0] == '_' and _tag[1] == 'yes':

                        try:
                            tag = star_data.get_tag(_tag[0])
                            if len(tag) == 0 and _tag[0][1:].split('.')[0] == star_data.category:
                                missing_sf_tags.append(_tag[0])
                        except:  # ValueError:  # noqa: E722 pylint: disable=bare-except
                            missing_lp_tags.append(_tag[0])

            except:  # ValueError:  # noqa: E722 pylint: disable=bare-except

                try:
                    star_data = pynmrstar.Loop.from_file(in_file)

                    for _tag in mandatoryTag:

                        if _tag[0][0] == '_' and _tag[0][1:].split('.')[0] == star_data.category and _tag[1] == 'yes':

                            try:
                                get_lp_tag(star_data, _tag[0])
                            except:  # ValueError:  # noqa: E722 pylint: disable=bare-except
                                missing_lp_tags.append(_tag[0])

                except:  # ValueError:  # noqa: E722 pylint: disable=bare-except
                    pass

        return missing_sf_tags, missing_lp_tags

    def is_mandatory_tag(self, item, file_type):
        """ Return whether a given tag is mandatory.
            @author: Masashi Yokochi
            @param item: item name
            @param file_type: input file type either 'nef' or 'nmr-star'
            @return: True for mandatory tag, False otherwise
        """

        mandatoryTag = self.nefMandatoryTag if file_type == 'nef' else self.starMandatoryTag

        return any(t[0] == item and t[1] == 'yes' for t in mandatoryTag)

    def validate_file(self, in_file, file_subtype='A'):
        """ Validate input NEF/NMR-STAR file.
            @param infile: input NEF/NMR-STAR file path
            @param file_subtype: should be 'A', 'S', 'R', or 'O'
                , where A for All in one file, S for chemical Shifts file, R for Restraints file, O for Other conventional restraint file
            @return: status, message
        """

        is_valid = True
        info = []
        warning = []
        error = []

        file_type = 'unknown'

        err_template_for_missing_mandatory_loop = "The mandatory loop %r is missing. Deposition of %s is mandatory. Please re-upload the %s file."
        err_template_for_empty_mandatory_loop = "The mandatory loop %r is empty. Deposition of %s is mandatory. Please re-upload the %s file."
        err_template_for_empty_mandatory_loop_of_sf = "The mandatory loop %r in saveframe %r is empty. Deposition of %s is mandatory. Please re-upload the %s file."
        warn_template_for_empty_mandatory_loop = "The mandatory loop %r is empty. Please re-upload the %s file."
        warn_template_for_empty_mandatory_loop_of_sf = "The mandatory loop %r in saveframe %r is empty. Please re-upload the %s file."

        try:

            is_done, data_type, star_data = self.read_input_file(in_file)

            if is_done:

                minimal_lp_category_nef_a = ['_nef_chemical_shift', '_nef_distance_restraint']
                minimal_lp_category_nef_s = ['_nef_chemical_shift']
                minimal_lp_category_nef_r = ['_nef_distance_restraint']

                minimal_lp_category_star_a = ['_Atom_chem_shift', '_Gen_dist_constraint']
                minimal_lp_category_star_s = ['_Atom_chem_shift']
                minimal_lp_category_star_r = ['_Gen_dist_constraint']
                allowed_lp_category_star_o = ['_Gen_dist_constraint', '_Torsion_angle_constraint', '_RDC_constraint']

                minimal_sf_category_nef_a = ['nef_chemical_shift_list', 'nef_distance_restraint_list']
                minimal_sf_category_nef_s = ['nef_chemical_shift_list']
                minimal_sf_category_nef_r = ['nef_distance_restraint_list']

                minimal_sf_category_star_a = ['assigned_chemical_shifts', 'general_distance_constraints']
                minimal_sf_category_star_s = ['assigned_chemical_shifts']
                minimal_sf_category_star_r = ['general_distance_constraints']
                allowed_sf_category_star_o = ['general_distance_constraints', 'torsion_angle_constraints', 'RDC_constraints']

                sf_list, lp_list = self.get_inventory_list(star_data, data_type)

                info.append(f"{len(sf_list)} saveframes and {len(lp_list)} loops found")

                nef_sf_list = [i for i in sf_list if i is not None and 'nef' in i]
                nef_lp_list = [i for i in lp_list if i is not None and 'nef' in i]

                info.append(f"{len(nef_sf_list)} saveframes and {len(nef_lp_list)} loops found with NEF prefix")

                if len(nef_sf_list) > 0 or len(nef_lp_list) > 0:

                    is_nef_file = True
                    info.append(f"{in_file} is a NEF file")
                    file_type = 'nef'

                else:

                    is_nef_file = False
                    info.append(f"{in_file} is an NMR-STAR file")
                    file_type = 'nmr-star'

                _file_type = file_type.upper()

                if is_nef_file:
                    if file_subtype == 'A':

                        for lp_category, sf_category in zip(minimal_lp_category_nef_a, minimal_sf_category_nef_a):
                            content_subtype = 'assigned chemical shifts' if 'shift' in lp_category else 'distance restraints'
                            if lp_category not in lp_list:
                                is_valid = False
                                error.append(err_template_for_missing_mandatory_loop
                                             % (lp_category, content_subtype, _file_type))
                            else:
                                if is_empty_loop(star_data, lp_category, data_type):
                                    is_valid = False
                                    if data_type == 'Loop':
                                        if count_non_empty_loops(star_data, lp_category, data_type) == 0:
                                            error.append(err_template_for_empty_mandatory_loop
                                                         % (lp_category, content_subtype, _file_type))
                                        else:
                                            error.append(warn_template_for_empty_mandatory_loop
                                                         % (lp_category, _file_type))
                                    else:
                                        sf_framecodes = get_sf_tag_values_with_empty_loop(star_data, lp_category, sf_category)
                                        if count_non_empty_loops(star_data, lp_category, data_type) == 0:
                                            if len(sf_framecodes) == 1:
                                                error.append(err_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes[0], content_subtype, _file_type))
                                            else:
                                                error.append(err_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes, content_subtype, _file_type))
                                        else:
                                            if len(sf_framecodes) == 1:
                                                error.append(warn_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes[0], _file_type))
                                            else:
                                                error.append(warn_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes, _file_type))

                    elif file_subtype == 'S':
                        content_subtype = 'assigned chemical shifts'

                        for lp_category, sf_category in zip(minimal_lp_category_nef_s, minimal_sf_category_nef_s):
                            if lp_category not in lp_list:
                                is_valid = False
                                error.append(err_template_for_missing_mandatory_loop
                                             % (lp_category, content_subtype, _file_type))
                            else:
                                if is_empty_loop(star_data, lp_category, data_type):
                                    is_valid = False
                                    if data_type == 'Loop':
                                        if count_non_empty_loops(star_data, lp_category, data_type) == 0:
                                            error.append(err_template_for_empty_mandatory_loop
                                                         % (lp_category, content_subtype, _file_type))
                                        else:
                                            error.append(warn_template_for_empty_mandatory_loop
                                                         % (lp_category, _file_type))
                                    else:
                                        sf_framecodes = get_sf_tag_values_with_empty_loop(star_data, lp_category, sf_category)
                                        if count_non_empty_loops(star_data, lp_category, data_type) == 0:
                                            if len(sf_framecodes) == 1:
                                                error.append(err_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes[0], content_subtype, _file_type))
                                            else:
                                                error.append(err_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes, content_subtype, _file_type))
                                        else:
                                            if len(sf_framecodes) == 1:
                                                error.append(warn_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes[0], _file_type))
                                            else:
                                                error.append(warn_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes, _file_type))

                    elif file_subtype == 'R':
                        content_subtype = 'distance restraints'

                        for lp_category, sf_category in zip(minimal_lp_category_nef_r, minimal_sf_category_nef_r):
                            if lp_category not in lp_list:
                                is_valid = False
                                error.append(err_template_for_missing_mandatory_loop
                                             % (lp_category, content_subtype, _file_type))
                            else:
                                if is_empty_loop(star_data, lp_category, data_type):
                                    is_valid = False
                                    if data_type == 'Loop':
                                        if count_non_empty_loops(star_data, lp_category, data_type) == 0:
                                            error.append(err_template_for_empty_mandatory_loop
                                                         % (lp_category, content_subtype, _file_type))
                                        else:
                                            error.append(warn_template_for_empty_mandatory_loop
                                                         % (lp_category, _file_type))
                                    else:
                                        sf_framecodes = get_sf_tag_values_with_empty_loop(star_data, lp_category, sf_category)
                                        if count_non_empty_loops(star_data, lp_category, data_type) == 0:
                                            if len(sf_framecodes) == 1:
                                                error.append(err_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes[0], content_subtype, _file_type))
                                            else:
                                                error.append(err_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes, content_subtype, _file_type))
                                        else:
                                            if len(sf_framecodes) == 1:
                                                error.append(warn_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes[0], _file_type))
                                            else:
                                                error.append(warn_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes, _file_type))

                    else:
                        is_valid = False
                        error.append('file_subtype flag should be A/S/R')

                else:
                    if file_subtype == 'A':

                        for lp_category, sf_category in zip(minimal_lp_category_star_a, minimal_sf_category_star_a):
                            content_subtype = 'assigned chemical shifts' if 'shift' in lp_category else 'distance restraints'
                            if lp_category not in lp_list:
                                is_valid = False
                                error.append(err_template_for_missing_mandatory_loop
                                             % (lp_category, content_subtype, _file_type))
                            else:
                                if is_empty_loop(star_data, lp_category, data_type):
                                    is_valid = False
                                    if data_type == 'Loop':
                                        if count_non_empty_loops(star_data, lp_category, data_type) == 0:
                                            error.append(err_template_for_empty_mandatory_loop
                                                         % (lp_category, content_subtype, _file_type))
                                        else:
                                            error.append(warn_template_for_empty_mandatory_loop
                                                         % (lp_category, _file_type))
                                    else:
                                        sf_framecodes = get_sf_tag_values_with_empty_loop(star_data, lp_category, sf_category)
                                        if count_non_empty_loops(star_data, lp_category, data_type) == 0:
                                            if len(sf_framecodes) == 1:
                                                error.append(err_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes[0], content_subtype, _file_type))
                                            else:
                                                error.append(err_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes, content_subtype, _file_type))
                                        else:
                                            if len(sf_framecodes) == 1:
                                                error.append(warn_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes[0], _file_type))
                                            else:
                                                error.append(warn_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes, _file_type))

                    elif file_subtype == 'S':
                        content_subtype = 'assigned chemical shifts'

                        for lp_category, sf_category in zip(minimal_lp_category_star_s, minimal_sf_category_star_s):
                            if lp_category not in lp_list:
                                is_valid = False
                                error.append(err_template_for_missing_mandatory_loop
                                             % (lp_category, content_subtype, _file_type))
                            else:
                                if is_empty_loop(star_data, lp_category, data_type):
                                    is_valid = False
                                    if data_type == 'Loop':
                                        if count_non_empty_loops(star_data, lp_category, data_type) == 0:
                                            error.append(err_template_for_empty_mandatory_loop
                                                         % (lp_category, content_subtype, _file_type))
                                        else:
                                            error.append(warn_template_for_empty_mandatory_loop
                                                         % (lp_category, _file_type))
                                    else:
                                        sf_framecodes = get_sf_tag_values_with_empty_loop(star_data, lp_category, sf_category)
                                        if count_non_empty_loops(star_data, lp_category, data_type) == 0:
                                            if len(sf_framecodes) == 1:
                                                error.append(err_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes[0], content_subtype, _file_type))
                                            else:
                                                error.append(err_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes, content_subtype, _file_type))
                                        else:
                                            if len(sf_framecodes) == 1:
                                                error.append(warn_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes[0], _file_type))
                                            else:
                                                error.append(warn_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes, _file_type))

                    elif file_subtype == 'R':
                        content_subtype = 'distance restraints'

                        for lp_category, sf_category in zip(minimal_lp_category_star_r, minimal_sf_category_star_r):
                            if lp_category not in lp_list:
                                is_valid = False
                                error.append(err_template_for_missing_mandatory_loop
                                             % (lp_category, content_subtype, _file_type))
                            else:
                                if is_empty_loop(star_data, lp_category, data_type):
                                    is_valid = False
                                    if data_type == 'Loop':
                                        if count_non_empty_loops(star_data, lp_category, data_type) == 0:
                                            error.append(err_template_for_empty_mandatory_loop
                                                         % (lp_category, content_subtype, _file_type))
                                        else:
                                            error.append(warn_template_for_empty_mandatory_loop
                                                         % (lp_category, _file_type))
                                    else:
                                        sf_framecodes = get_sf_tag_values_with_empty_loop(star_data, lp_category, sf_category)
                                        if count_non_empty_loops(star_data, lp_category, data_type) == 0:
                                            if len(sf_framecodes) == 1:
                                                error.append(err_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes[0], content_subtype, _file_type))
                                            else:
                                                error.append(err_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes, content_subtype, _file_type))
                                        else:
                                            if len(sf_framecodes) == 1:
                                                error.append(warn_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes[0], _file_type))
                                            else:
                                                error.append(warn_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes, _file_type))

                    elif file_subtype == 'O':  # DAOTHER-7545, issue #2
                        is_valid = False
                        for lp_category in allowed_lp_category_star_o:
                            if lp_category in lp_list and not is_empty_loop(star_data, lp_category, data_type):
                                is_valid = True
                        if not is_valid:
                            error.append(f"One of the mandatory loops {allowed_lp_category_star_o} is missing. "
                                         f"Please re-upload the {_file_type} file.")
                        else:
                            for lp_category, sf_category in zip(allowed_lp_category_star_o, allowed_sf_category_star_o):
                                if lp_category in lp_list:
                                    if is_empty_loop(star_data, lp_category, data_type):
                                        is_valid = False
                                        if data_type == 'Loop':
                                            error.append(warn_template_for_empty_mandatory_loop
                                                         % (lp_category, _file_type))
                                        else:
                                            sf_framecodes = get_sf_tag_values_with_empty_loop(star_data, lp_category, sf_category)
                                            if len(sf_framecodes) == 1:
                                                error.append(warn_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes[0], _file_type))
                                            else:
                                                error.append(warn_template_for_empty_mandatory_loop_of_sf
                                                             % (lp_category, sf_framecodes, _file_type))

                    else:
                        is_valid = False
                        error.append('file_subtype flag should be A/S/R/O')

            else:
                is_valid = False
                error.append(data_type)

        except Exception as e:
            is_valid = False
            error.append(str(e))

        return is_valid, {'info': info, 'warning': warning, 'error': error, 'file_type': file_type}

    def resolve_sf_names_for_cif(self, star_data, data_type):  # pylint: disable=no-self-use # DAOTHER-7389, issue #4
        """ Resolve saveframe names to prevent case-insensitive name collisions occur in CIF format.
            @return: status, list of correction messages, dictionary of saveframe name corrections
        """

        if data_type != 'Entry':
            return True, [], {}

        original_names = [sf.name for sf in star_data.frame_list]

        while True:

            lower_names = [sf.name.lower() for sf in star_data.frame_list]
            dup_names = set(n for n in lower_names if lower_names.count(n) > 1)

            if len(dup_names) == 0:
                break

            for dup_name in dup_names:
                idx = 1
                for sf in star_data.frame_list:
                    if sf.name.lower() == dup_name:
                        sf.name = f"{sf.name}_{idx}"
                        idx += 1

        resolved_names = [sf.name for sf in star_data.frame_list]

        messages = []
        corrections = {}

        for original, resolved in zip(original_names, resolved_names):
            if original != resolved:
                messages.append(f"The saveframe name {original!r} has been renamed to {resolved!r} "
                                "in order to prevent case-insensitive name collisions occurring in CIF format.")
                corrections[original] = resolved

        return len(messages) == 0, messages, corrections

    def get_inventory_list(self, star_data, data_type):  # pylint: disable=no-self-use
        """ Return lists of saveframe category names and loop category names in an NEF/NMR-STAR file.
            @change: rename the original get_data_content() to get_inventory_list() by Masashi Yokochi
            @return: list of saveframe category names, list of loop category names
        """

        sf_list = []
        lp_list = []

        if data_type == 'Entry':

            for sf in star_data.frame_list:
                sf_list.append(sf.category)

                for lp in sf:
                    lp_list.append(lp.category)

        elif data_type == 'Saveframe':

            for lp in star_data:
                lp_list.append(lp.category)

        elif star_data is not None:
            lp_list.append(star_data.category)

        return sf_list, lp_list

    def get_seq_from_cs_loop(self, in_file):
        """ Extract sequence from chemical shift loop.
            @deprecated: used only for testing
            @param in_file: NEF/NMR-STAR file
            @return: status, message
        """

        is_valid, message = self.validate_file(in_file, 'S')

        info = message['info']
        warning = message['warning']
        error = message['error']
        file_type = message['file_type']

        is_ok = False
        seq = []

        if is_valid:

            info.append('File successfully read ')
            in_data = self.read_input_file(in_file)[-1]

            if file_type == 'nmr-star':

                info.append('NMR-STAR')
                seq = self.get_star_seq(in_data)

                if len(seq[0]) > 0:
                    is_ok = True

                else:
                    error.append("Can't extract sequence from chemical shift loop")

            elif file_type == 'nef':

                info.append('NEF')
                seq = self.get_nef_seq(in_data)

                if len(seq[0]) > 0:
                    is_ok = True

                else:
                    error.append("Can't extract sequence from chemical shift loop")

            else:
                error.append("Can't identify file type, it is neither NEF nor NMR-STAR")

        else:
            error.append('File validation failed (or) File contains no chemical shift information')

        return is_ok, {'info': info, 'warning': warning, 'error': error, 'file_type': file_type, 'data': seq}

    def get_nef_seq(self, star_data, lp_category='nef_chemical_shift', seq_id='sequence_code', comp_id='residue_name',  # pylint: disable=no-self-use
                    chain_id='chain_code', allow_empty=False, allow_gap=False):
        """ Extract sequence from any given loops in an NEF file.
            @change: re-written by Masashi Yokochi
            @return: list of sequence information for each loop
        """

        user_warn_msg = ''

        try:
            loops = star_data.get_loops_by_category(lp_category)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            try:
                if __pynmrstar_v3_2__:
                    loops = [star_data.get_loop(lp_category)]
                else:
                    loops = [star_data.get_loop_by_category(lp_category)]
            except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
                loops = [star_data]

        data = []  # data of all loops

        tags = [seq_id, comp_id, chain_id]

        for loop in loops:
            cmp_dict = {}
            seq_dict = {}

            seq_data = []

            len_loop_data = len(loop.data)

            if set(tags) & set(loop.tags) == set(tags):
                seq_data = get_lp_tag(loop, tags)
                for i in seq_data:
                    if i[2] in emptyValue:
                        i[2] = 1
            else:
                _tags_exist = False
                for i in range(1, MAX_DIM_NUM_OF_SPECTRA):
                    _tags = [seq_id + '_' + str(i), comp_id + '_' + str(i), chain_id + '_' + str(i)]
                    if set(_tags) & set(loop.tags) == set(_tags):
                        _tags_exist = True
                        seq_data += get_lp_tag(loop, _tags)

                if not _tags_exist:
                    missing_tags = list(set(tags) - set(loop.tags))
                    raise LookupError(f"Missing mandatory {missing_tags} loop tag(s).")

            if allow_empty:
                # seq_data = list(filter(is_data, seq_data))
                seq_data = list(filter(is_good_data, seq_data))  # DAOTHER-7389, issue #3
                if len(seq_data) == 0:
                    continue
            else:
                for l, i in enumerate(seq_data):  # noqa: E741
                    if is_empty(i) and l < len_loop_data:
                        r = {}
                        for j, t in enumerate(loop.tags):
                            r[t] = loop.data[l][j]
                        user_warn_msg += "[Invalid data] Sequence must not be empty. "\
                            f"#_of_row {l + 1}, data_of_row {r}.\n"

            for l, i in enumerate(seq_data):  # noqa: E741
                try:
                    int(i[0])
                except ValueError:
                    if l < len_loop_data:
                        r = {}
                        for j, t in enumerate(loop.tags):
                            r[t] = loop.data[l][j]
                        user_warn_msg += f"[Invalid data] {seq_id} must be an integer. "\
                            f"#_of_row {l + 1}, data_of_row {r}.\n"

            if len(user_warn_msg) > 0:
                raise UserWarning(user_warn_msg)

            try:

                chains = sorted(set(i[2] for i in seq_data))
                offset_seq_ids = {i[2]: 0 for i in seq_data}
                for c in chains:
                    min_seq_id = min([int(i[0]) for i in seq_data if i[2] == c])
                    if min_seq_id < 0:
                        offset_seq_ids[c] = min_seq_id * -1
                sorted_seq = sorted(set(f"{i[2]} {int(i[0]) + offset_seq_ids[i[2]]:04d} {i[1]}" for i in seq_data))

                chk_dict = {f"{i[2]} {int(i[0]):04d}": i[1] for i in seq_data}

                for i in seq_data:
                    chk_key = f"{i[2]} {int(i[0]):04d}"
                    if chk_dict[chk_key] != i[1]:
                        raise KeyError(f"{lp_category[1:]} loop contains different {comp_id} ({i[1]} and {chk_dict[chk_key]}) "
                                       f"with the same {chain_id} {i[2]}, {seq_id} {i[0]}.")

                if len(sorted_seq[0].split(' ')[-1]) > 1:
                    if len(chains) > 1:
                        for c in chains:
                            cmp_dict[c] = [i.split(' ')[-1].upper() for i in sorted_seq if i.split(' ')[0] == c]
                            seq_dict[c] = [int(i.split(' ')[1]) - offset_seq_ids[c] for i in sorted_seq if i.split(' ')[0] == c]
                    else:
                        c = list(chains)[0]
                        cmp_dict[c] = [i.split(' ')[-1].upper() for i in sorted_seq]
                        seq_dict[c] = [int(i.split(' ')[1]) - offset_seq_ids[c] for i in sorted_seq]
                else:
                    if len(chains) > 1:
                        for c in chains:
                            cmp_dict[c] = [i.split(' ')[-1].upper() for i in sorted_seq if i.split(' ')[0] == c]
                            seq_dict[c] = [int(i.split(' ')[1]) - offset_seq_ids[c] for i in sorted_seq if i.split(' ')[0] == c]
                    else:
                        c = list(chains)[0]
                        cmp_dict[c] = [i.split(' ')[-1].upper() for i in sorted_seq]
                        seq_dict[c] = [int(i.split(' ')[1]) - offset_seq_ids[c] for i in sorted_seq]

                asm = []  # assembly of a loop

                for c in chains:
                    ent = {}  # entity

                    ent['chain_id'] = str(c)

                    if allow_gap:
                        ent['seq_id'] = []
                        ent['comp_id'] = []

                        _seq_id_ = None

                        for _seq_id, _comp_id in zip(seq_dict[c], cmp_dict[c]):

                            if _seq_id_ is not None and _seq_id_ + 1 != _seq_id and _seq_id_ + 20 > _seq_id:
                                for s in range(_seq_id_ + 1, _seq_id):
                                    ent['seq_id'].append(s)
                                    ent['comp_id'].append('.')
                            ent['seq_id'].append(_seq_id)
                            ent['comp_id'].append(_comp_id)

                            _seq_id_ = _seq_id

                    else:
                        ent['seq_id'] = seq_dict[c]
                        ent['comp_id'] = cmp_dict[c]

                    if len(chains) > 1:
                        identity = []
                        for _c in chains:
                            if _c == c:
                                continue
                            if seq_dict[_c] == seq_dict[c]:
                                if cmp_dict[_c] == cmp_dict[c]:
                                    identity.append(_c)
                            else:
                                common_seq_id = set(seq_dict[_c]) & set(seq_dict[c])
                                if len(common_seq_id) == 0:
                                    continue
                                if any(s for s in common_seq_id
                                       if s in seq_dict[_c] and s in seq_dict[c]
                                       and cmp_dict[_c][seq_dict[_c].index(s)] != cmp_dict[c][seq_dict[c].index(s)]):
                                    continue
                                if not any(s for s in common_seq_id
                                           if s in seq_dict[_c] and s in seq_dict[c]
                                           and cmp_dict[_c][seq_dict[_c].index(s)] == cmp_dict[c][seq_dict[c].index(s)]):
                                    continue
                                identity.append(_c)
                        if len(identity) > 0:
                            ent['identical_chain_id'] = identity

                    asm.append(ent)

                data.append(asm)

            except ValueError:
                pass

        if len(data) == 0:
            data.append([])

        return data

    def get_star_seq(self, star_data, lp_category='Atom_chem_shift', seq_id='Comp_index_ID', comp_id='Comp_ID',  # pylint: disable=no-self-use
                     chain_id='Entity_assembly_ID', alt_seq_id='Seq_ID', alt_seq_id_offset=0, alt_chain_id='Auth_asym_ID',
                     allow_empty=False, allow_gap=False):
        """ Extract sequence from any given loops in an NMR-STAR file.
            @change: re-written by Masashi Yokochi
            @return: list of sequence information for each loop
        """

        user_warn_msg = ''

        try:
            loops = star_data.get_loops_by_category(lp_category)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            try:
                if __pynmrstar_v3_2__:
                    loops = [star_data.get_loop(lp_category)]
                else:
                    loops = [star_data.get_loop_by_category(lp_category)]
            except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
                loops = [star_data]

        def_chain_id = 'A' if self.__remediation_mode else '1'

        data = []  # data of all loops

        tags = [seq_id, comp_id, chain_id]
        tags_ = [seq_id, comp_id]
        tags__ = [seq_id, comp_id, alt_chain_id]  # DAOTHER-7421

        for loop in loops:
            cmp_dict = {}
            seq_dict = {}

            seq_data = []

            len_loop_data = len(loop.data)

            if set(tags) & set(loop.tags) == set(tags):
                seq_data = get_lp_tag(loop, tags)
                for i in seq_data:
                    if i[2] in emptyValue:
                        i[2] = def_chain_id
            elif set(tags__) & set(loop.tags) == set(tags__):  # DAOTHER-7421
                seq_data = get_lp_tag(loop, tags__)
                for i in seq_data:
                    i[2] = def_chain_id if i[2] in emptyValue else str(i[2] if self.__remediation_mode else letterToDigit(i[2], 1))
            elif set(tags_) & set(loop.tags) == set(tags_):  # No Entity_assembly_ID tag case
                seq_data = get_lp_tag(loop, tags_)
                for i in seq_data:
                    i.append(def_chain_id)
            else:
                _tags_exist = False
                for j in range(1, MAX_DIM_NUM_OF_SPECTRA):
                    _tags = [seq_id + '_' + str(j), comp_id + '_' + str(j), chain_id + '_' + str(j)]
                    _tags_ = [seq_id + '_' + str(j), comp_id + '_' + str(j)]
                    _tags__ = [seq_id + '_' + str(j), comp_id + '_' + str(j), alt_chain_id + '_' + str(j)]  # DAOTHER-7421
                    if set(_tags) & set(loop.tags) == set(_tags):
                        _tags_exist = True
                        seq_data_ = get_lp_tag(loop, _tags)
                        for i in seq_data_:
                            if alt_seq_id_offset != 0:
                                i[0] += alt_seq_id_offset
                            if i[2] in emptyValue:
                                i[2] = def_chain_id
                        seq_data += seq_data_
                    elif set(_tags__) & set(loop.tags) == set(_tags__):  # DAOTHER-7421
                        _tags_exist = True
                        seq_data_ = get_lp_tag(loop, _tags__)
                        for i in seq_data_:
                            i[2] = def_chain_id if i[2] in emptyValue else str(i[2] if self.__remediation_mode else letterToDigit(i[2], 1))
                        seq_data += seq_data_
                    elif set(_tags_) & set(loop.tags) == set(_tags_):
                        _tags_exist = True
                        seq_data_ = get_lp_tag(loop, _tags_)
                        for i in seq_data_:
                            i.append(def_chain_id)
                        seq_data += seq_data_

                if not _tags_exist:
                    missing_tags = list(set(tags) - set(loop.tags))
                    raise LookupError(f"Missing mandatory {missing_tags} loop tag(s).")

            if allow_empty:
                # seq_data = list(filter(is_data, seq_data))
                seq_data = list(filter(is_good_data, seq_data))  # DAOTHER-7389, issue #3
                if len(seq_data) == 0:
                    continue
            else:
                for l, i in enumerate(seq_data):  # noqa: E741
                    if is_empty(i) and l < len_loop_data:
                        r = {}
                        for j, t in enumerate(loop.tags):
                            r[t] = loop.data[l][j]
                        user_warn_msg += "[Invalid data] Sequence must not be empty. "\
                            f"#_of_row {l + 1}, data_of_row {r}.\n"

            for l, i in enumerate(seq_data):  # noqa: E741
                try:
                    int(i[0])
                except ValueError:
                    if l < len_loop_data:
                        r = {}
                        for j, t in enumerate(loop.tags):
                            r[t] = loop.data[l][j]
                        user_warn_msg += f"[Invalid data] {seq_id} must be an integer. "\
                            f"#_of_row {l + 1}, data_of_row {r}.\n"

            if len(user_warn_msg) > 0:
                raise UserWarning(user_warn_msg)

            try:

                chains = sorted(set(i[2] for i in seq_data))
                offset_seq_ids = {i[2]: 0 for i in seq_data}
                for c in chains:
                    min_seq_id = min([int(i[0]) for i in seq_data if i[2] == c])
                    if min_seq_id < 0:
                        offset_seq_ids[c] = min_seq_id * -1
                sorted_seq = sorted(set(f"{i[2]} {int(i[0]) + offset_seq_ids[i[2]]:04d} {i[1]}" for i in seq_data))

                chk_dict = {f"{i[2]} {int(i[0]):04d}": i[1] for i in seq_data}

                for i in seq_data:
                    chk_key = f"{i[2]} {int(i[0]):04d}"
                    if chk_dict[chk_key] != i[1]:

                        if seq_id != alt_seq_id and alt_seq_id in loop.tags:
                            to_idx = loop.tags.index(seq_id)
                            fr_idx = loop.tags.index(alt_seq_id)

                            seq_tags = [seq_id, alt_seq_id]
                            _seq_data = get_lp_tag(loop, seq_tags)

                            offset = None

                            for _i in _seq_data:
                                try:
                                    offset = int(_i[to_idx]) - int(_i[fr_idx])
                                    break
                                except ValueError:
                                    continue

                            if offset is not None:
                                return self.get_star_seq(star_data, lp_category, alt_seq_id, comp_id, chain_id,
                                                         alt_seq_id, offset, alt_chain_id, allow_empty, allow_gap)

                        raise KeyError(f"{lp_category[1:]} loop contains different {comp_id} ({i[1]} and {chk_dict[chk_key]}) "
                                       f"with the same {chain_id} {i[2]}, {seq_id} {i[0]}.")

                if len(sorted_seq[0].split(' ')[-1]) > 1:
                    if len(chains) > 1:
                        for c in chains:
                            cmp_dict[c] = [i.split(' ')[-1].upper() for i in sorted_seq if i.split(' ')[0] == c]
                            seq_dict[c] = [int(i.split(' ')[1]) - offset_seq_ids[c] for i in sorted_seq if i.split(' ')[0] == c]
                    else:
                        c = list(chains)[0]
                        cmp_dict[c] = [i.split(' ')[-1].upper() for i in sorted_seq]
                        seq_dict[c] = [int(i.split(' ')[1]) - offset_seq_ids[c] for i in sorted_seq]
                else:
                    if len(chains) > 1:
                        for c in chains:
                            cmp_dict[c] = [i.split(' ')[-1].upper() for i in sorted_seq if i.split(' ')[0] == c]
                            seq_dict[c] = [int(i.split(' ')[1]) - offset_seq_ids[c] for i in sorted_seq if i.split(' ')[0] == c]
                    else:
                        c = list(chains)[0]
                        cmp_dict[c] = [i.split(' ')[-1].upper() for i in sorted_seq]
                        seq_dict[c] = [int(i.split(' ')[1]) - offset_seq_ids[c] for i in sorted_seq]

                asm = []  # assembly of a loop

                for c in chains:
                    ent = {}  # entity

                    str_c = str(c)
                    ent['chain_id'] = str_c if str_c.isdigit() or self.__remediation_mode else str(letterToDigit(str_c, 1))

                    if allow_gap:
                        ent['seq_id'] = []
                        ent['comp_id'] = []

                        _seq_id_ = None

                        for _seq_id, _comp_id in zip(seq_dict[c], cmp_dict[c]):

                            if _seq_id_ is not None and _seq_id_ + 1 != _seq_id and _seq_id_ + 20 > _seq_id:
                                for s in range(_seq_id_ + 1, _seq_id):
                                    ent['seq_id'].append(s)
                                    ent['comp_id'].append('.')
                            ent['seq_id'].append(_seq_id)
                            ent['comp_id'].append(_comp_id)

                            _seq_id_ = _seq_id

                    else:
                        ent['seq_id'] = seq_dict[c]
                        ent['comp_id'] = cmp_dict[c]

                    if len(chains) > 1:
                        identity = []
                        for _c in chains:
                            if _c == c:
                                continue
                            if seq_dict[_c] == seq_dict[c]:
                                if cmp_dict[_c] == cmp_dict[c]:
                                    _str_c = str(_c)
                                    identity.append(_str_c if _str_c.isdigit() or self.__remediation_mode else str(letterToDigit(_str_c, 1)))
                            else:
                                common_seq_id = set(seq_dict[_c]) & set(seq_dict[c])
                                if len(common_seq_id) == 0:
                                    continue
                                if any(s for s in common_seq_id
                                       if s in seq_dict[_c] and s in seq_dict[c]
                                       and cmp_dict[_c][seq_dict[_c].index(s)] != cmp_dict[c][seq_dict[c].index(s)]):
                                    continue
                                if not any(s for s in common_seq_id
                                           if s in seq_dict[_c] and s in seq_dict[c]
                                           and cmp_dict[_c][seq_dict[_c].index(s)] == cmp_dict[c][seq_dict[c].index(s)]):
                                    continue
                                _str_c = str(_c)
                                identity.append(_str_c if _str_c.isdigit() or self.__remediation_mode else str(letterToDigit(_str_c, 1)))
                        if len(identity) > 0:
                            ent['identical_chain_id'] = identity

                    asm.append(ent)

                data.append(asm)

            except ValueError:
                pass

        if len(data) == 0:
            data.append([])

        return data

    def get_star_auth_seq(self, star_data, lp_category='Atom_chem_shift', aseq_id='Auth_seq_ID', acomp_id='Auth_comp_ID',  # pylint: disable=no-self-use
                          asym_id='Auth_asym_ID', seq_id='Comp_index_ID', chain_id='Entity_assembly_ID', allow_empty=True):
        """ Extract author sequence from any given loops in an NMR-STAR file.
            @author: Masashi Yokochi
            @return: list of author sequence information for each loop
        """

        user_warn_msg = ''

        try:
            loops = star_data.get_loops_by_category(lp_category)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            try:
                if __pynmrstar_v3_2__:
                    loops = [star_data.get_loop(lp_category)]
                else:
                    loops = [star_data.get_loop_by_category(lp_category)]
            except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
                loops = [star_data]

        data = []  # data of all loops

        tags = [aseq_id, acomp_id, asym_id, seq_id, chain_id]
        tags_ = [aseq_id, acomp_id, seq_id, asym_id]

        for loop in loops:
            seq_dict = {}
            acmp_dict = {}
            aseq_dict = {}
            asym_dict = {}

            seq_data = []

            len_loop_data = len(loop.data)

            if set(tags) & set(loop.tags) == set(tags):
                seq_data = get_lp_tag(loop, tags)
            elif set(tags_) & set(loop.tags) == set(tags_):  # No Entity_assembly_ID tag case
                seq_data = get_lp_tag(loop, tags_)
                for i in seq_data:
                    i.append('1')
            else:
                _tags_exist = False
                for j in range(1, MAX_DIM_NUM_OF_SPECTRA):
                    _tags = [aseq_id + '_' + str(j), acomp_id + '_' + str(j), asym_id + '_' + str(j),
                             seq_id + '_' + str(j), chain_id + '_' + str(j)]
                    _tags_ = [aseq_id + '_' + str(j), acomp_id + '_' + str(j), asym_id + '_' + str(j), seq_id + '_' + str(j)]
                    if set(_tags) & set(loop.tags) == set(_tags):
                        _tags_exist = True
                        seq_data += get_lp_tag(loop, _tags)
                    elif set(_tags_) & set(loop.tags) == set(_tags_):
                        _tags_exist = True
                        seq_data_ = get_lp_tag(loop, _tags_)
                        for i in seq_data_:
                            i.append('1')
                        seq_data += seq_data_

                if not _tags_exist:
                    missing_tags = list(set(tags) - set(loop.tags))
                    raise LookupError(f"Missing mandatory {missing_tags} loop tag(s).")

            if allow_empty:
                # seq_data = list(filter(is_data, seq_data))
                seq_data = list(filter(is_good_data, seq_data))  # DAOTHER-7389, issue #3
                if len(seq_data) == 0:
                    continue
            else:
                for l, i in enumerate(seq_data):  # noqa: E741
                    if is_empty(i) and l < len_loop_data:
                        r = {}
                        for j, t in enumerate(loop.tags):
                            r[t] = loop.data[l][j]
                        user_warn_msg += "[Invalid data] Author sequence must not be empty. "\
                            f"#_of_row {l + 1}, data_of_row {r}.\n"

            for l, i in enumerate(seq_data):  # noqa: E741
                try:
                    int(i[3])
                except ValueError:
                    if l < len_loop_data:
                        r = {}
                        for j, t in enumerate(loop.tags):
                            r[t] = loop.data[l][j]
                        user_warn_msg += f"[Invalid data] {seq_id} must be an integer. "\
                            f"#_of_row {l + 1}, data_of_row {r}.\n"

            if len(user_warn_msg) > 0:
                raise UserWarning(user_warn_msg)

            try:

                chains = sorted(set(i[4] for i in seq_data))
                offset_seq_ids = {i[4]: 0 for i in seq_data}
                for c in chains:
                    min_seq_id = min([int(i[3]) for i in seq_data if i[4] == c])
                    if min_seq_id < 0:
                        offset_seq_ids[c] = min_seq_id * -1
                sorted_seq = sorted(set(f"{i[4]}:{int(i[3]) + offset_seq_ids[i[4]]:04d}:{i[2]}:{i[0]: >4}:{i[1]}" for i in seq_data))

                chk_dict = {f"{i[4]}:{int(i[3]):04d}:{i[2]}:{i[0]: >4}": i[1] for i in seq_data}

                for i in seq_data:
                    chk_key = f"{i[4]}:{int(i[3]):04d}:{i[2]}:{i[0]: >4}"
                    if chk_dict[chk_key] != i[1]:
                        raise KeyError(f"Author sequence must be unique. {chain_id} {i[4]}, {seq_id} {i[3]}, "
                                       f"{asym_id} {i[2]}, {aseq_id} {i[0]}, "
                                       f"{acomp_id} {i[1]} vs {chk_dict[chk_key]}.")

                if len(sorted_seq[0].split(':')[-1]) > 1:
                    if len(chains) > 1:
                        for c in chains:
                            acmp_dict[c] = [i.split(':')[-1] for i in sorted_seq if i.split(':')[0] == c]
                            aseq_dict[c] = [i.split(':')[3].strip() for i in sorted_seq if i.split(':')[0] == c]
                            asym_dict[c] = [i.split(':')[2] for i in sorted_seq if i.split(':')[0] == c]
                            seq_dict[c] = [int(i.split(':')[1]) - offset_seq_ids[c] for i in sorted_seq if i.split(':')[0] == c]
                    else:
                        c = list(chains)[0]
                        acmp_dict[c] = [i.split(':')[-1] for i in sorted_seq]
                        aseq_dict[c] = [i.split(':')[3].strip() for i in sorted_seq]
                        asym_dict[c] = [i.split(':')[2] for i in sorted_seq]
                        seq_dict[c] = [int(i.split(':')[1]) - offset_seq_ids[c] for i in sorted_seq]
                else:
                    if len(chains) > 1:
                        for c in chains:
                            acmp_dict[c] = [i.split(':')[-1] for i in sorted_seq if i.split(':')[0] == c]
                            aseq_dict[c] = [i.split(':')[3].strip() for i in sorted_seq if i.split(':')[0] == c]
                            asym_dict[c] = [i.split(':')[2] for i in sorted_seq if i.split(':')[0] == c]
                            seq_dict[c] = [int(i.split(':')[1]) - offset_seq_ids[c] for i in sorted_seq if i.split(':')[0] == c]
                    else:
                        c = list(chains)[0]
                        acmp_dict[c] = [i.split(':')[-1] for i in sorted_seq]
                        aseq_dict[c] = [i.split(':')[3].strip() for i in sorted_seq]
                        asym_dict[c] = [i.split(':')[2] for i in sorted_seq]
                        seq_dict[c] = [int(i.split(':')[1]) - offset_seq_ids[c] for i in sorted_seq]

                asm = []  # assembly of a loop

                for c in chains:
                    ent = {}  # entity

                    ent['chain_id'] = str(c)
                    ent['seq_id'] = seq_dict[c]
                    ent['auth_asym_id'] = asym_dict[c]
                    ent['auth_seq_id'] = aseq_dict[c]
                    ent['auth_comp_id'] = acmp_dict[c]

                    asm.append(ent)

                data.append(asm)

            except ValueError:
                pass

        if len(data) == 0:
            data.append([])

        return data

    def get_nef_comp_atom_pair(self, star_data, lp_category='nef_chemical_shift', comp_id='residue_name', atom_id='atom_name',
                               allow_empty=False):
        """ Wrapper function of get_comp_atom_pair() for an NEF file.
            @author: Masashi Yokochi
        """

        return self.get_comp_atom_pair(star_data, lp_category, comp_id, atom_id, allow_empty)

    def get_star_comp_atom_pair(self, star_data, lp_category='Atom_chem_shift', comp_id='Comp_ID', atom_id='Atom_ID',
                                allow_empty=False):
        """ Wrapper function of get_comp_atom_pair() for an NMR-STAR file.
            @author: Masashi Yokochi
        """

        return self.get_comp_atom_pair(star_data, lp_category, comp_id, atom_id, allow_empty)

    def get_star_auth_comp_atom_pair(self, star_data, lp_category='Atom_chem_shift', comp_id='Auth_comp_ID', atom_id='Auth_atom_ID',
                                     allow_empty=True):
        """ Wrapper function of get_comp_atom_pair() for pairs of author comp_id and author atom_id in an NMR-STAR file.
            @author: Masashi Yokochi
        """

        return self.get_comp_atom_pair(star_data, lp_category, comp_id, atom_id, allow_empty)

    def get_comp_atom_pair(self, star_data, lp_category, comp_id, atom_id, allow_empty):  # pylint: disable=no-self-use
        """ Extract unique pairs of comp_id and atom_id from any given loops in an NEF/NMR-STAR file.
            @author: Masashi Yokochi
            @return: list of unique pairs of comp_id and atom_id for each loop
        """

        user_warn_msg = ''

        try:
            loops = star_data.get_loops_by_category(lp_category)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            try:
                if __pynmrstar_v3_2__:
                    loops = [star_data.get_loop(lp_category)]
                else:
                    loops = [star_data.get_loop_by_category(lp_category)]
            except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
                loops = [star_data]

        data = []  # data of all loops

        tags = [comp_id, atom_id]

        for loop in loops:
            atm_dict = {}

            pair_data = []

            len_loop_data = len(loop.data)

            if set(tags) & set(loop.tags) == set(tags):
                pair_data = get_lp_tag(loop, tags)
            else:
                _tags_exist = False
                for i in range(1, MAX_DIM_NUM_OF_SPECTRA):
                    _tags = [comp_id + '_' + str(i), atom_id + '_' + str(i)]
                    if set(_tags) & set(loop.tags) == set(_tags):
                        _tags_exist = True
                        pair_data += get_lp_tag(loop, _tags)

                if not _tags_exist:
                    missing_tags = list(set(tags) - set(loop.tags))
                    raise LookupError(f"Missing mandatory {missing_tags} loop tag(s).")

            if allow_empty:
                # pair_data = list(filter(is_data, pair_data))
                pair_data = list(filter(is_good_data, pair_data))  # DAOTHER-7389, issue #3
                if len(pair_data) == 0:
                    continue
            else:
                for l, i in enumerate(pair_data):  # noqa: E741
                    if is_empty(i) and l < len_loop_data:
                        r = {}
                        for j, t in enumerate(loop.tags):
                            r[t] = loop.data[l][j]
                        user_warn_msg += f"[Invalid data] {comp_id} and {atom_id} must not be empty. "\
                            f"#_of_row {l + 1}, data_of_row {r}.\n"

            if len(user_warn_msg) > 0:
                raise UserWarning(user_warn_msg)

            comps = sorted(set(i[0].upper() for i in pair_data if i[0] not in emptyValue))
            sorted_comp_atom = sorted(set(f"{i[0].upper()} {i[1]}" for i in pair_data))

            for c in comps:
                atm_dict[c] = [i.split(' ')[1] for i in sorted_comp_atom if i.split(' ')[0] == c]

            asm = []  # assembly of a loop

            for c in comps:
                ent = {}  # entity

                ent['comp_id'] = c
                ent['atom_id'] = atm_dict[c]

                asm.append(ent)

            data.append(asm)

        if len(data) == 0:
            data.append([])

        return data

    def get_nef_atom_type_from_cs_loop(self, star_data, lp_category='nef_chemical_shift',
                                       atom_type='element', isotope_number='isotope_number', atom_id='atom_name',
                                       allow_empty=False):
        """ Wrapper function of get_atom_type_from_cs_loop() for an NEF file.
            @author: Masashi Yokochi
        """

        return self.get_atom_type_from_cs_loop(star_data, lp_category, atom_type, isotope_number, atom_id, allow_empty)

    def get_star_atom_type_from_cs_loop(self, star_data, lp_category='Atom_chem_shift',
                                        atom_type='Atom_type', isotope_number='Atom_isotope_number', atom_id='Atom_ID',
                                        allow_empty=False):
        """ Wrapper function of get_atom_type_from_cs_loop() for an NMR-SAR file.
            @author: Masashi Yokochi
        """

        return self.get_atom_type_from_cs_loop(star_data, lp_category, atom_type, isotope_number, atom_id, allow_empty)

    def get_atom_type_from_cs_loop(self, star_data, lp_category, atom_type, isotope_number, atom_id, allow_empty):  # pylint: disable=no-self-use
        """ Extract unique pairs of atom_type, isotope number, and atom_id from assigned chemical shifts in n NEF/NMR-SAR file.
            @author: Masashi Yokochi
            @return: list of unique pairs of atom_type, isotope number, and atom_id for each CS loop
        """

        user_warn_msg = ''

        try:
            loops = star_data.get_loops_by_category(lp_category)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            try:
                if __pynmrstar_v3_2__:
                    loops = [star_data.get_loop(lp_category)]
                else:
                    loops = [star_data.get_loop_by_category(lp_category)]
            except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
                loops = [star_data]

        data = []  # data of all loops

        tags = [atom_type, isotope_number, atom_id]

        for loop in loops:
            ist_dict = {}
            atm_dict = {}

            a_type_data = []

            len_loop_data = len(loop.data)

            if set(tags) & set(loop.tags) != set(tags):
                missing_tags = list(set(tags) - set(loop.tags))
                raise LookupError(f"Missing mandatory {missing_tags} loop tag(s).")

            a_type_data = get_lp_tag(loop, tags)

            if allow_empty:
                # a_type_data = list(filter(is_data, a_type_data))
                a_type_data = list(filter(is_good_data, a_type_data))  # DAOTHER-7389, issue #3
                if len(a_type_data) == 0:
                    continue
            else:
                for l, i in enumerate(a_type_data):  # noqa: E741
                    if is_empty(i) and l < len_loop_data:
                        r = {}
                        for j, t in enumerate(loop.tags):
                            r[t] = loop.data[l][j]
                        user_warn_msg += f"[Invalid data] {atom_type}, {isotope_number}, and {atom_id} must not be empty. "\
                            f"#_of_row {l + 1}, data_of_row {r}.\n"

            for l, i in enumerate(a_type_data):  # noqa: E741
                try:
                    int(i[1])
                except ValueError:
                    if l < len_loop_data:
                        r = {}
                        for j, t in enumerate(loop.tags):
                            r[t] = loop.data[l][j]
                        user_warn_msg += f"[Invalid data] {isotope_number} must be an integer. "\
                            f"#_of_row {l + 1}, data_of_row {r}.\n"

            if len(user_warn_msg) > 0:
                raise UserWarning(user_warn_msg)

            try:

                a_types = sorted(set(i[0] for i in a_type_data))
                sorted_ist = sorted(set(f"{i[0]} {i[1]}" for i in a_type_data))
                sorted_atm = sorted(set(f"{i[0]} {i[2]}" for i in a_type_data
                                        if not (i[2] in emptyValue or badPattern.match(i[2]))))  # DAOTHER-7389, issue #3

                for t in a_types:
                    ist_dict[t] = [int(i.split(' ')[1]) for i in sorted_ist if i.split(' ')[0] == t]
                    atm_dict[t] = [i.split(' ')[1] for i in sorted_atm if i.split(' ')[0] == t]

                asm = []  # assembly of a loop

                for t in a_types:
                    ent = {}  # entity

                    ent['atom_type'] = t
                    ent['isotope_number'] = ist_dict[t]
                    ent['atom_id'] = atm_dict[t]

                    asm.append(ent)

                data.append(asm)

            except ValueError:
                pass

        if len(data) == 0:
            data.append([])

        return data

    def get_star_ambig_code_from_cs_loop(self, star_data, lp_category='Atom_chem_shift', comp_id='Comp_ID', atom_id='Atom_ID',  # pylint: disable=no-self-use
                                         ambig_code='Ambiguity_code', ambig_set_id='Ambiguity_set_ID'):
        """ Extract unique pairs of comp_id, atom_id, and ambiguity code from assigned chemical shifts in an NMR-SAR file.
            @author: Masashi Yokochi
            @return: list of unique pairs of comp_id, atom_id, and ambiguity code for each CS loop
        """

        user_warn_msg = ''

        try:
            loops = star_data.get_loops_by_category(lp_category)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            try:
                if __pynmrstar_v3_2__:
                    loops = [star_data.get_loop(lp_category)]
                else:
                    loops = [star_data.get_loop_by_category(lp_category)]
            except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
                loops = [star_data]

        data = []  # data of all loops

        tags = [comp_id, atom_id, ambig_code, ambig_set_id]

        for loop in loops:
            atm_dict = {}

            ambig_data = []

            len_loop_data = len(loop.data)

            if set(tags) & set(loop.tags) != set(tags):
                missing_tags = list(set(tags) - set(loop.tags))
                raise LookupError(f"Missing mandatory {missing_tags} loop tag(s).")

            ambig_data = get_lp_tag(loop, tags)

            if len(ambig_data) == 0:
                data.append(None)
                continue

            for l, i in enumerate(ambig_data):  # noqa: E741
                # already checked elsewhere
                # if i[0] in emptyValue:
                #   raise ValueError(f"{comp_id} must not be empty.")
                # if i[1] in emptyValue:
                #    raise ValueError(f"{comp_id} must not be empty.")
                if i[2] not in emptyValue:

                    try:
                        code = int(i[2])
                    except ValueError:
                        if l < len_loop_data:
                            r = {}
                            for j, t in enumerate(loop.tags):
                                r[t] = loop.data[l][j]
                            user_warn_msg += f"[Invalid data] {ambig_code} must be one of {ALLOWED_AMBIGUITY_CODES}. "\
                                f"#_of_row {l + 1}, data_of_row {r}.\n"

                    if code not in ALLOWED_AMBIGUITY_CODES:
                        if l < len_loop_data:
                            r = {}
                            for j, t in enumerate(loop.tags):
                                r[t] = loop.data[l][j]
                            user_warn_msg += f"[Invalid data] {ambig_code} must be one of {ALLOWED_AMBIGUITY_CODES}. "\
                                f"#_of_row {l + 1}, data_of_row {r}.\n"

                    if code >= 4:
                        if i[3] in emptyValue and l < len_loop_data:
                            r = {}
                            for j, t in enumerate(loop.tags):
                                r[t] = loop.data[l][j]
                            user_warn_msg += f"[Invalid data] {ambig_set_id} must not be empty for {ambig_code} {code}. "\
                                f"#_of_row {l + 1}, data_of_row {r}.\n"
                        else:
                            try:
                                int(i[3])
                            except ValueError:
                                if l < len_loop_data:
                                    r = {}
                                    for j, t in enumerate(loop.tags):
                                        r[t] = loop.data[l][j]
                                    user_warn_msg += f"[Invalid data] {ambig_set_id} must be an integer. "\
                                        f"#_of_row {l + 1}, data_of_row {r}.\n"

                if i[3] not in emptyValue:

                    if i[2] in emptyValue or i[2] not in ('4', '5', '6', '9'):
                        if l < len_loop_data:
                            r = {}
                            for j, t in enumerate(loop.tags):
                                r[t] = loop.data[l][j]
                            user_warn_msg += f"[Invalid data] {ambig_set_id} must be empty for {ambig_code} {i[2]}. "\
                                f"#_of_row {l + 1}, data_of_row {r}.\n"

            if len(user_warn_msg) > 0:
                raise UserWarning(user_warn_msg)

            _ambig_data = [i for i in ambig_data
                           if not (i[0] in emptyValue or badPattern.match(i[0]))
                           and not (i[1] in emptyValue or badPattern.match(i[1]))]  # DAOTHER-7389, issue #3

            if len(_ambig_data) == 0:
                continue

            ambigs = sorted(set(f"{i[0].upper()}:{i[2]}" for i in _ambig_data))
            sorted_atm = sorted(set(f"{i[0].upper()}:{i[2]} {i[1]}" for i in _ambig_data))

            for a in ambigs:
                atm_dict[a] = [i.split(' ')[1] for i in sorted_atm if i.split(' ')[0] == a]

            asm = []  # assembly of a loop

            for a in ambigs:
                ent = {}  # entity

                split_a = a.split(':')

                ent['comp_id'] = split_a[0]
                ent['ambig_code'] = None if split_a[1] in emptyValue else int(split_a[1])
                ent['atom_id'] = atm_dict[a]

                asm.append(ent)

            data.append(asm)

        if len(data) == 0:
            data.append([])

        return data

    def get_nef_index(self, star_data, lp_category='nef_sequence', index_id='index'):
        """ Wrapper function of get_index() for an NEF file.
            @deprecated: used only for testing
            @author: Masashi Yokochi
        """

        return self.get_index(star_data, lp_category, index_id)

    def get_star_index(self, star_data, lp_category='Chem_comp_assembly', index_id='NEF_index'):
        """ Wrapper function of get_index() for an NMR-STAR file.
            @deprecated: used only for testing
            @author: Masashi Yokochi
        """

        return self.get_index(star_data, lp_category, index_id)

    def get_index(self, star_data, lp_category, index_id):  # pylint: disable=no-self-use
        """ Extract index_id from any given loops in an NEF/NMR-STAR file.
            @author: Masashi Yokochi
            @return: list of index for each loop
        """

        user_warn_msg = ''

        try:
            loops = star_data.get_loops_by_category(lp_category)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            try:
                if __pynmrstar_v3_2__:
                    loops = [star_data.get_loop(lp_category)]
                else:
                    loops = [star_data.get_loop_by_category(lp_category)]
            except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
                loops = [star_data]

        data = []  # data of all loops

        tags = [index_id]

        for loop in loops:
            index_data = []

            len_loop_data = len(loop.data)

            if set(tags) & set(loop.tags) == set(tags):
                index_data = get_lp_tag(loop, tags)
            else:
                raise LookupError(f"Missing mandatory {index_id} loop tag.")

            for l, i in enumerate(index_data):  # noqa: E741
                if i in emptyValue and l < len_loop_data:
                    r = {}
                    for j, t in enumerate(loop.tags):
                        r[t] = loop.data[l][j]
                    user_warn_msg += f"[Invalid data] {index_id} must not be empty. "\
                        f"#_of_row {l + 1}, data_of_row {r}.\n"
                else:
                    try:
                        int(i)
                    except ValueError:
                        if l < len_loop_data:
                            r = {}
                            for j, t in enumerate(loop.tags):
                                r[t] = loop.data[l][j]
                            user_warn_msg += f"[Invalid data] {index_id} must be an integer. "\
                                f"#_of_row {l + 1}, data_of_row {r}.\n"

            if len(user_warn_msg) > 0:
                raise UserWarning(user_warn_msg)

            try:

                if __pynmrstar_v3__:
                    idxs = [int(i) for i in index_data]
                else:
                    idxs = [int(i) for i in index_data[0]]

                dup_idxs = [i for i in set(idxs) if idxs.count(i) > 1]

                if len(dup_idxs) > 0:
                    raise KeyError(f"{index_id} must be unique in loop. {dup_idxs} are duplicated.")

                data.append(idxs)

            except ValueError:
                pass

        if len(data) == 0:
            data.append([])

        return data

    def check_data(self, star_data, lp_category, key_items, data_items,
                   allowed_tags=None, disallowed_tags=None, parent_pointer=None,
                   test_on_index=False, enforce_non_zero=False, enforce_sign=False, enforce_range=False,
                   enforce_enum=False, enforce_allowed_tags=False, excl_missing_data=False):
        """ Extract data with sanity check from any given loops in an NEF/NMR-STAR file.
            @author: Masashi Yokochi
            @return: list of extracted data for each loop
        """

        try:
            loops = star_data.get_loops_by_category(lp_category)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            try:
                if __pynmrstar_v3_2__:
                    loops = [star_data.get_loop(lp_category)]
                else:
                    loops = [star_data.get_loop_by_category(lp_category)]
            except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
                loops = [star_data]

        user_warn_msg = ''

        data = []  # data of all loops

        item_types = ('str', 'bool', 'int', 'index-int', 'positive-int', 'positive-int-as-str', 'pointer-index',
                      'float', 'positive-float', 'range-float', 'enum', 'enum-int')

        key_names = [k['name'] for k in key_items]
        data_names = [d['name'] for d in data_items]
        mand_data_names = [d['name'] for d in data_items if d['mandatory']]
        _mand_data_names = [d['name'] for d in data_items if d['mandatory'] and 'default-from' in d]

        key_len = len(key_items)

        for k in key_items:
            if k['type'] not in item_types:
                raise TypeError(f"Type {k['type']} of data item {k['name']} must be one of {item_types}.")

        for d in data_items:
            if d['type'] not in item_types:
                raise TypeError(f"Type {d['type']} of data item {d['name']} must be one of {item_types}.")

        if allowed_tags is not None:

            if len(key_names) > 0 and (set(key_names) | set(allowed_tags)) != set(allowed_tags):
                raise LookupError(f"Key items {((set(key_names) | set(allowed_tags)) - set(allowed_tags))} must not exists.")

            if len(data_names) > 0 and (set(data_names) | set(allowed_tags)) != set(allowed_tags):
                raise LookupError(f"Data items {((set(data_names) | set(allowed_tags)) - set(allowed_tags))} must not exists.")

            for d in data_items:
                if 'group-mandatory' in d and d['group-mandatory']:
                    group = d['group']
                    if group['member-with'] is not None:
                        for mw in group['member-with']:
                            if mw not in allowed_tags:
                                raise ValueError(f"Member data item {mw} of {d['name']} must exists in allowed tags.")
                    if group['coexist-with'] is not None:
                        for cw in group['coexist-with']:
                            if cw not in allowed_tags:
                                raise ValueError(f"Coexisting data item {cw} of {d['name']} must exists in allowed tags.")

        for loop in loops:
            tag_data = []

            if len(key_names) > 0 and set(key_names) & set(loop.tags) != set(key_names):
                missing_tags = list(set(key_names) - set(loop.tags))
                for k in key_items:
                    if k['name'] in missing_tags:
                        if 'default-from' in k and k['default-from'] != 'self' and k['default-from'] in loop.tags:
                            from_col = loop.tags.index(k['default-from'])
                            for row in loop.data:
                                ref = row[from_col]
                                row.append(ref)
                            loop.add_tag(k['name'])
                        elif 'default' in k:
                            for row in loop.data:
                                row.append(k['default'])
                            loop.add_tag(k['name'])
                        else:
                            raise LookupError(f"Missing mandatory {missing_tags} loop tag(s).")

            if len(mand_data_names) > 0 and set(mand_data_names) & set(loop.tags) != set(mand_data_names):
                missing_tags = list(set(mand_data_names) - set(loop.tags))
                for k in key_items:
                    if k['name'] in missing_tags:
                        if 'default-from' in k and k['default-from'] != 'self' and k['default-from'] in loop.tags:
                            from_col = loop.tags.index(k['default-from'])
                            for row in loop.data:
                                ref = row[from_col]
                                row.append(ref)
                            loop.add_tag(k['name'])
                        elif 'default' in k:
                            for row in loop.data:
                                row.append(k['default'])
                            loop.add_tag(k['name'])
                        else:
                            raise LookupError(f"Missing mandatory {missing_tags} loop tag(s).")

            if len(_mand_data_names) > 0 and set(_mand_data_names) & set(loop.tags) != set(_mand_data_names):
                missing_tags = list(set(_mand_data_names) - set(loop.tags))
                for d in data_items:
                    if d['name'] in missing_tags:
                        if 'default-from' in d:
                            if d['type'] == 'index-int':
                                for lv, row in enumerate(loop.data, start=1):
                                    row.append(lv)
                                loop.add_tag(d['name'])
                            elif d['default-from'] != 'self' and d['default-from'] in loop.tags:
                                from_col = loop.tags.index(d['default-from'])
                                if d['name'] == 'element' or d['name'] == 'Atom_type':
                                    for row in loop.data:
                                        ref = row[from_col]
                                        if ref.startswith('H') or ref.startswith('Q') or ref.startswith('M'):
                                            row.append('H')
                                        else:
                                            row.append(ref[0])
                                    loop.add_tag(d['name'])
                                elif d['name'] == 'isotope_number' or d['name'] == 'Atom_isotope_number':
                                    for row in loop.data:
                                        ref = row[from_col]
                                        if ref.startswith('H') or ref.startswith('Q') or ref.startswith('M'):
                                            row.append(1)
                                        else:
                                            row.append(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[ref[0]][0])
                                    loop.add_tag(d['name'])
                                elif 'Entity_assembly_ID' in d['name']:
                                    for row in loop.data:
                                        ref = row[from_col]
                                        row.append(ref)
                                    loop.add_tag(d['name'])

            if disallowed_tags is not None:
                if len(set(loop.tags) & set(disallowed_tags)) > 0:
                    disallow_tags = list(set(loop.tags) & set(disallowed_tags))
                    raise LookupError(f"Disallowed {disallow_tags} loop tag(s) exists.")

            if enforce_allowed_tags and allowed_tags is not None:
                extra_tags = (set(loop.tags) | set(allowed_tags)) - set(allowed_tags)
                if len(extra_tags) > 0:
                    raise LookupError(f"Unauthorized {extra_tags} loop tag(s) must not exists.")  # DAOTHER-7545 only for NMR-STAR

            for d in data_items:
                if 'group-mandatory' in d and d['group-mandatory']:
                    name = d['name']
                    group = d['group']
                    if name in loop.tags:
                        if group['coexist-with'] is not None:
                            for cw in group['coexist-with']:
                                if cw not in loop.tags:
                                    set_cw = set(group['coexist-with'])
                                    set_cw.add(name)
                                    missing_tags = list(set_cw - set(loop.tags))
                                    raise LookupError(f"Missing mandatory {missing_tags} loop tag(s).")

                    elif group['member-with'] is not None:
                        has_member = False
                        for mw in group['member-with']:
                            if mw in loop.tags:
                                has_member = True
                                break
                        if not has_member:
                            set_mw = set(group['member-with'])
                            set_mw.add(name)
                            missing_tags = list(set_mw - set(loop.tags))
                            raise LookupError(f"Missing mandatory {missing_tags} loop tag(s).")

            tags = [k['name'] for k in key_items]
            for data_name in set(data_names) & set(loop.tags):
                tags.append(data_name)

            tag_len = len(tags)

            static_val = {}
            for name in tags:
                static_val[name] = None

            idx_tag_ids = set()
            for j in range(tag_len):
                name = tags[j]
                if name in key_names:
                    for k in key_items:
                        if k['name'] == name and k['type'] == 'index-int':
                            idx_tag_ids.add(j)
                else:
                    for d in data_items:
                        if d['name'] == name and d['type'] == 'index-int':
                            idx_tag_ids.add(j)

            relax_key_ids = set()
            for j in range(tag_len):
                name = tags[j]
                for d in data_items:
                    if d['name'] == name and 'relax-key-if-exist' in d and d['relax-key-if-exist']:
                        relax_key_ids.add(j)

            tag_data = get_lp_tag(loop, tags)

            if test_on_index and len(idx_tag_ids) > 0:

                for l, _j in enumerate(idx_tag_ids):  # noqa: E741

                    try:
                        idxs = [int(i[_j]) for i in tag_data]

                        dup_idxs = [i for i in set(idxs) if idxs.count(i) > 1]

                        if len(dup_idxs) > 0:
                            raise KeyError(f"{tags[_j]} must be unique in loop. {dup_idxs} are duplicated.")

                    except ValueError:
                        r = {}
                        for j, t in enumerate(loop.tags):
                            r[t] = loop.data[l][j]
                        raise ValueError(f"{tags[_j]} must be an integer. "
                                         f"#_of_row {l + 1}, data_of_row {r}.")

            if not excl_missing_data:
                for l, i in enumerate(tag_data):  # noqa: E741
                    for j in range(tag_len):
                        if i[j] in emptyValue:
                            name = tags[j]
                            if name in key_names:
                                k = key_items[key_names.index(name)]
                                if not ('remove-bad-pattern' in k and k['remove-bad-pattern']) and 'default' not in k:
                                    r = {}
                                    for _j, _t in enumerate(loop.tags):  # noqa: E741
                                        r[_t] = loop.data[l][_j]
                                    raise ValueError(f"{name} must not be empty. "
                                                     f"#_of_row {l + 1}, data_of_row {r}.")

                            for d in data_items:
                                if d['name'] == name and d['mandatory'] and 'default' not in d\
                                   and not ('remove-bad-pattern' in d and d['detele-bad-pattern']):
                                    r = {}
                                    for _j, _t in enumerate(loop.tags):
                                        r[_t] = loop.data[l][_j]
                                    raise ValueError(f"{name} must not be empty. "
                                                     f"#_of_row {l + 1}, data_of_row {r}.")

            if test_on_index and key_len > 0:
                keys = set()

                rechk = False

                for i in tag_data:

                    key = ''
                    for j in range(key_len):
                        key += ' ' + i[j]
                    key.rstrip()

                    if key in keys:

                        relax_key = False

                        if len(relax_key_ids) > 0:
                            for j in relax_key_ids:
                                if i[j] is not emptyValue:
                                    relax_key = True
                                    break

                        if relax_key:
                            rechk = True

                        else:
                            msg = ''
                            for j in range(key_len):
                                msg += key_names[j] + ' ' + i[j] + ', '

                            idx_msg = ''

                            if len(idx_tag_ids) > 0:
                                for _j in idx_tag_ids:
                                    idx_msg += tags[_j] + ' '

                                    for _i in tag_data:
                                        _key = ''
                                        for j in range(key_len):
                                            _key += " " + _i[j]
                                            _key.rstrip()

                                        if key == _key:
                                            idx_msg += _i[_j] + ' vs '

                                    idx_msg = idx_msg[:-4] + ', '

                                idx_msg = "[Check rows of " + idx_msg[:-2] + "] "

                            user_warn_msg += "[Multiple data] "\
                                f"{idx_msg}Duplicated rows having the following values {msg.rstrip().rstrip(',')} exist in a loop.\n"

                    else:
                        keys.add(key)

                if rechk:
                    keys = set()

                    for i in tag_data:

                        key = ''
                        for j in range(key_len):
                            key += ' ' + i[j]
                        for j in relax_key_ids:
                            key += ' ' + i[j]
                        key.rstrip()

                        if key in keys:

                            msg = ''
                            for j in range(key_len):
                                msg += key_names[j] + ' ' + i[j] + ', '
                            for j in relax_key_ids:
                                if i[j] not in emptyValue:
                                    msg += tags[j] + ' ' + i[j] + ', '

                            idx_msg = ''

                            if len(idx_tag_ids) > 0:
                                for _j in idx_tag_ids:
                                    idx_msg += tags[_j] + ' '

                                    for _i in tag_data:
                                        _key = ''
                                        for j in range(key_len):
                                            _key += " " + _i[j]
                                        for j in relax_key_ids:
                                            _key += " " + _i[j]
                                            _key.rstrip()

                                        if key == _key:
                                            idx_msg += _i[_j] + ' vs '

                                    idx_msg = idx_msg[:-4] + ', '

                                idx_msg = "[Check rows of " + idx_msg[:-2] + "] "

                            user_warn_msg += "[Multiple data] "\
                                f"{idx_msg}Duplicated rows having the following values {msg.rstrip().rstrip(',')} exist in a loop.\n"

                        else:
                            keys.add(key)

            if len(user_warn_msg) > 0:
                _user_warn_msg = ''

                for k in key_items:
                    if k['type'] == 'int' and 'default-from' in k and k['default-from'] in loop.tags:
                        to_idx = loop.tags.index(k['name'])
                        fr_idx = loop.tags.index(k['default-from'])

                        offset = None

                        for i in loop.data:
                            if i[to_idx] not in emptyValue and i[fr_idx] not in emptyValue:
                                try:
                                    offset = int(i[to_idx]) - int(i[fr_idx])
                                    break
                                except ValueError:
                                    continue

                        if offset is not None:

                            for l, i in enumerate(loop.data):  # noqa: E741
                                if i[to_idx] not in emptyValue and i[fr_idx] not in emptyValue:
                                    try:
                                        loop.data[l][to_idx] = str(int(i[fr_idx]) + offset)
                                    except ValueError:
                                        continue

                tag_data = get_lp_tag(loop, tags)

                if test_on_index and key_len > 0:
                    keys = set()

                    rechk = False

                    for i in tag_data:

                        key = ''
                        for j in range(key_len):
                            key += ' ' + i[j]
                        key.rstrip()

                        if key in keys:

                            relax_key = False

                            if len(relax_key_ids) > 0:
                                for j in relax_key_ids:
                                    if i[j] is not emptyValue:
                                        relax_key = True
                                        break

                            if relax_key:
                                rechk = True

                            else:
                                msg = ''
                                for j in range(key_len):
                                    msg += key_names[j] + ' ' + i[j] + ', '

                                idx_msg = ''

                                if len(idx_tag_ids) > 0:
                                    for _j in idx_tag_ids:
                                        idx_msg += tags[_j] + ' '

                                        for _i in tag_data:
                                            _key = ''
                                            for j in range(key_len):
                                                _key += " " + _i[j]
                                                _key.rstrip()

                                            if key == _key:
                                                idx_msg += _i[_j] + ' vs '

                                        idx_msg = idx_msg[:-4] + ', '

                                    idx_msg = "[Check rows of " + idx_msg[:-2] + "] "

                                _user_warn_msg += "[Multiple data] "\
                                    f"{idx_msg}Duplicated rows having the following values {msg.rstrip().rstrip(',')} exist in a loop.\n"

                        else:
                            keys.add(key)

                    if rechk:
                        keys = set()

                        for i in tag_data:

                            key = ''
                            for j in range(key_len):
                                key += ' ' + i[j]
                            for j in relax_key_ids:
                                key += ' ' + i[j]
                            key.rstrip()

                            if key in keys:

                                msg = ''
                                for j in range(key_len):
                                    msg += key_names[j] + ' ' + i[j] + ', '
                                for j in relax_key_ids:
                                    if i[j] not in emptyValue:
                                        msg += tags[j] + ' ' + i[j] + ', '

                                idx_msg = ''

                                if len(idx_tag_ids) > 0:
                                    for _j in idx_tag_ids:
                                        idx_msg += tags[_j] + ' '

                                        for _i in tag_data:
                                            _key = ''
                                            for j in range(key_len):
                                                _key += " " + _i[j]
                                            for j in relax_key_ids:
                                                _key += " " + _i[j]
                                                _key.rstrip()

                                            if key == _key:
                                                idx_msg += _i[_j] + ' vs '

                                        idx_msg = idx_msg[:-4] + ', '

                                    idx_msg = "[Check rows of " + idx_msg[:-2] + "] "

                                _user_warn_msg += "[Multiple data] "\
                                    f"{idx_msg}Duplicated rows having the following values {msg.rstrip().rstrip(',')} exist in a loop.\n"

                            else:
                                keys.add(key)

                if len(_user_warn_msg) == 0:
                    user_warn_msg = ''

            asm = []  # assembly of a loop

            for l, i in enumerate(tag_data):  # noqa: E741
                ent = {}  # entity

                missing_mandatory_data = False
                remove_bad_pattern = False
                clear_bad_pattern = False

                for j in range(tag_len):
                    name = tags[j]
                    val = i[j]
                    if j < key_len:
                        k = key_items[j]
                        type = k['type']  # pylint: disable=redefined-builtin
                        if val in emptyValue and 'default' in k and k['default'] in emptyValue:
                            ent[name] = k['default']
                        elif type == 'bool':
                            try:
                                ent[name] = val.lower() in trueValue
                            except ValueError:
                                if excl_missing_data:
                                    missing_mandatory_data = True
                                    continue
                                if 'remove-bad-pattern' in k and k['remove-bad-pattern']:
                                    remove_bad_pattern = True
                                    continue
                                if 'clear-bad-pattern' in k and k['clear-bad-pattern']:
                                    clear_bad_pattern = True
                                    continue
                                raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                 + f"{name} {val!r} must be {self.readableItemType[type]}.")
                        elif type == 'int':
                            try:
                                ent[name] = int(val)
                            except ValueError:
                                if 'default-from' in k and k['default-from'] == 'self':
                                    i[j] = ent[name] = letterToDigit(val)
                                elif 'default-from' in k and k['default-from'] in tags:
                                    i[j] = ent[name] = letterToDigit(i[tags.index(k['default-from'])])
                                elif 'default' in k:
                                    i[j] = ent[name] = int(k['default'])
                                elif excl_missing_data:
                                    missing_mandatory_data = True
                                    continue
                                elif 'remove-bad-pattern' in k and k['remove-bad-pattern']:
                                    remove_bad_pattern = True
                                    continue
                                elif 'clear-bad-pattern' in k and k['clear-bad-pattern']:
                                    clear_bad_pattern = True
                                    continue
                                else:
                                    raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                     + f"{name} {val!r} must be {self.readableItemType[type]}.")
                        elif type in ('index-int', 'positive-int', 'positive-int-as-str'):
                            try:
                                ent[name] = int(val)
                            except ValueError:
                                if 'default-from' in k and k['default-from'] == 'self':
                                    i[j] = ent[name] = letterToDigit(val, 1)
                                elif 'default-from' in k and k['default-from'] in tags and i[tags.index(k['default-from'])] not in emptyValue:
                                    i[j] = ent[name] = letterToDigit(i[tags.index(k['default-from'])], 1)
                                elif 'default-from' in k and k['default-from'].startswith('Auth_asym_ID'):
                                    i[j] = ent[name] = letterToDigit(val, 1)
                                elif 'default' in k:
                                    i[j] = ent[name] = int(k['default'])
                                elif excl_missing_data:
                                    missing_mandatory_data = True
                                    continue
                                elif 'remove-bad-pattern' in k and k['remove-bad-pattern']:
                                    remove_bad_pattern = True
                                    continue
                                elif 'clear-bad-pattern' in k and k['clear-bad-pattern']:
                                    clear_bad_pattern = True
                                    continue
                                else:
                                    raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                     + f"{name} {val!r} must be {self.readableItemType[type]}.")
                            if (type == 'index-int' and ent[name] <= 0)\
                               or (type == 'positive-int' and (ent[name] < 0 or (ent[name] == 0 and 'enforce-non-zero' in k and k['enforce-non-zero']))):
                                raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                 + f"{name} {val!r} must be {self.readableItemType[type]}.")
                            if ent[name] == 0 and enforce_non_zero:
                                if 'void-zero' in k:
                                    if self.replace_zero_by_null_in_case:
                                        loop.data[l][loop.tags.index(name)] = None
                                    ent[name] = None
                                else:
                                    user_warn_msg += f"[Zero value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                        f"{name} {val!r} should not be zero, "\
                                        f"as defined by {self.readableItemType[type]}.\n"
                            if type == 'positive-int-as-str':
                                i[j] = ent[name] = str(ent[name])
                        elif type == 'pointer-index':
                            try:
                                ent[name] = int(val)
                            except ValueError:
                                if 'default-from' in k and k['default-from'] == 'self':
                                    i[j] = ent[name] = letterToDigit(val, 1)
                                elif 'default-from' in k and k['default-from'] in tags:
                                    i[j] = ent[name] = letterToDigit(i[tags.index(k['default-from'])], 1)
                                elif 'default-from' in k and k['default-from'] == 'parent' and parent_pointer is not None:
                                    i[j] = ent[name] = parent_pointer
                                elif 'default' in k:
                                    i[j] = ent[name] = int(k['default'])
                                elif excl_missing_data:
                                    missing_mandatory_data = True
                                    continue
                                elif 'remove-bad-pattern' in k and k['remove-bad-pattern']:
                                    remove_bad_pattern = True
                                    continue
                                elif 'clear-bad-pattern' in k and k['clear-bad-pattern']:
                                    clear_bad_pattern = True
                                    continue
                                else:
                                    raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                     + f"{name} {val!r} must be {self.readableItemType[type]}.")
                            if ent[name] <= 0:
                                raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                 + f"{name} {val!r} must be {self.readableItemType[type]}.")
                            if static_val[name] is None:
                                static_val[name] = val
                            elif val != static_val[name] and test_on_index:
                                raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                 + f"{name} {val} vs {static_val[name]} must be {self.readableItemType[type]}.")
                        elif type == 'float':
                            try:
                                ent[name] = float(val)
                            except ValueError:
                                if excl_missing_data:
                                    missing_mandatory_data = True
                                    continue
                                if 'remove-bad-pattern' in k and k['remove-bad-pattern']:
                                    remove_bad_pattern = True
                                    continue
                                if 'clear-bad-pattern' in k and k['clear-bad-pattern']:
                                    clear_bad_pattern = True
                                    continue
                                raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                 + f"{name} {val!r} must be {self.readableItemType[type]}.")
                        elif type == 'positive-float':
                            try:
                                ent[name] = float(val)
                            except ValueError:
                                if excl_missing_data:
                                    missing_mandatory_data = True
                                    continue
                                if 'remove-bad-pattern' in k and k['remove-bad-pattern']:
                                    remove_bad_pattern = True
                                    continue
                                if 'clear-bad-pattern' in k and k['clear-bad-pattern']:
                                    clear_bad_pattern = True
                                    continue
                                raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                 + f"{name} {val!r} must be {self.readableItemType[type]}.")
                            if ent[name] < 0.0 or (ent[name] == 0.0 and 'enforce-non-zero' in k and k['enforce-non-zero']):
                                raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                 + f"{name} {val!r} must be {self.readableItemType[type]}.")
                            if ent[name] == 0.0 and enforce_non_zero:
                                if 'void-zero' in k:
                                    if self.replace_zero_by_null_in_case:
                                        loop.data[l][loop.tags.index(name)] = None
                                    ent[name] = None
                                else:
                                    user_warn_msg += f"[Zero value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                        f"{name} {val!r} should not be zero, "\
                                        f"as defined by {self.readableItemType[type]}.\n"
                        elif type == 'range-float':
                            try:
                                _range = k['range']
                                ent[name] = float(val)
                            except KeyError:
                                raise ValueError(f"Range of key item {name} is not defined")
                            except ValueError:
                                if excl_missing_data:
                                    missing_mandatory_data = True
                                    continue
                                if 'remove-bad-pattern' in k and k['remove-bad-pattern']:
                                    remove_bad_pattern = True
                                    continue
                                if 'clear-bad-pattern' in k and k['clear-bad-pattern']:
                                    clear_bad_pattern = True
                                    continue
                                if not enforce_range:
                                    ent[name] = None
                                    continue
                                user_warn_msg += f"[Range value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                    f"{name} {val!r} must be {self.readableItemType[type]}.\n"
                            if ('min_exclusive' in _range and _range['min_exclusive'] == 0.0 and ent[name] <= 0.0)\
                               or ('min_inclusive' in _range and _range['min_inclusive'] == 0.0 and ent[name] < 0):
                                if ent[name] < 0.0:
                                    if ('max_inclusive' in _range and abs(ent[name]) > _range['max_inclusive'])\
                                       or ('max_exclusive' in _range and abs(ent[name]) >= _range['max_exclusive'])\
                                       or ('enforce-sign' in k and k['enforce-sign']):
                                        if not enforce_range:
                                            ent[name] = None
                                        else:
                                            user_warn_msg += f"[Range value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                                f"{name} {val!r} must be within range {_range}.\n"
                                    elif enforce_sign:
                                        user_warn_msg += f"[Negative value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                            f"{name} {val!r} should not have "\
                                            f"negative value for {self.readableItemType[type]}, {_range}.\n"
                                elif ent[name] == 0.0 and 'enforce-non-zero' in k and k['enforce-non-zero']:
                                    if not enforce_range:
                                        ent[name] = None
                                    else:
                                        user_warn_msg += f"[Range value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                            f"{name} {val!r} must be within range {_range}.\n"
                                elif ent[name] == 0.0 and enforce_non_zero:
                                    if 'void-zero' in k:
                                        if self.replace_zero_by_null_in_case:
                                            loop.data[l][loop.tags.index(name)] = None
                                        ent[name] = None
                                    else:
                                        user_warn_msg += f"[Zero value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                            f"{name} {val!r} should not be zero, "\
                                            f"as defined by {self.readableItemType[type]}, {_range}.\n"
                            elif ('min_exclusive' in _range and ent[name] <= _range['min_exclusive']) or\
                                 ('min_inclusive' in _range and ent[name] < _range['min_inclusive']) or\
                                 ('max_inclusive' in _range and ent[name] > _range['max_inclusive']) or\
                                 ('max_exclusive' in _range and ent[name] >= _range['max_exclusive']):
                                if 'void-zero' in k and ent[name] == 0.0:
                                    if self.replace_zero_by_null_in_case:
                                        loop.data[l][loop.tags.index(name)] = None
                                    ent[name] = None
                                elif not enforce_range:
                                    ent[name] = None
                                else:
                                    user_warn_msg += f"[Range value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                        f"{name} {val!r} must be within range {_range}.\n"
                        elif type == 'enum':
                            try:
                                enum = k['enum']
                                if val not in enum:
                                    if 'default-from' in k and k['default-from'] in tags:
                                        if i[tags.index(k['default-from'])][0].upper() in enum:
                                            val = i[tags.index(k['default-from'])][0].upper()
                                    elif 'enum-alt' in k and val in k['enum-alt']:
                                        val = k['enum-alt'][val]
                                        i[j] = val
                                    elif 'enforce-enum' in k and k['enforce-enum']:
                                        if excl_missing_data:
                                            missing_mandatory_data = True
                                            continue
                                        if 'remove-bad-pattern' in k and k['remove-bad-pattern']:
                                            remove_bad_pattern = True
                                            continue
                                        if 'clear-bad-pattern' in k and k['clear-bad-pattern']:
                                            clear_bad_pattern = True
                                            continue
                                        raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                         + f"{name} {val!r} must be one of {enum}.")
                                    elif enforce_enum:
                                        user_warn_msg += f"[Enumeration error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                            f"{name} {val!r} should be one of {enum}.\n"
                                ent[name] = val
                            except KeyError:
                                raise ValueError(f"Enumeration of key item {name} is not defined")
                        elif type == 'enum-int':
                            try:
                                enum = k['enum']
                                if int(val) not in enum:
                                    if 'default-from' in k and k['default-from'] in tags:
                                        if i[tags.index(k['default-from'])][0].upper() in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS:
                                            val = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[i[tags.index(k['default-from'])][0].upper()][0]
                                    if 'enforce-enum' in k and k['enforce-enum']:
                                        raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                         + f"{name} {val!r} must be one of {enum}.")
                                    if enforce_enum:
                                        user_warn_msg += f"[Enumeration error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                            f"{name} {val!r} should be one of {enum}.\n"
                                ent[name] = int(val)
                            except KeyError:
                                raise ValueError(f"Enumeration of key item {name} is not defined")
                            except ValueError:
                                if excl_missing_data:
                                    missing_mandatory_data = True
                                    continue
                                if 'remove-bad-pattern' in k and k['remove-bad-pattern']:
                                    remove_bad_pattern = True
                                    continue
                                if 'clear-bad-pattern' in k and k['clear-bad-pattern']:
                                    clear_bad_pattern = True
                                    continue
                                raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                 + f"{name} {val!r} must be {self.readableItemType[type]}.")
                        else:
                            if val in emptyValue:
                                missing_mandatory_data = True
                                continue
                            if ('remove-bad-pattern' in k and k['remove-bad-pattern']) or ('clear-bad-pattern' in k and k['clear-bad-pattern']):
                                if badPattern.match(val):
                                    if 'remove-bad-pattern' in k and k['remove-bad-pattern']:
                                        remove_bad_pattern = True
                                        continue
                                    if 'clear-bad-pattern' in k and k['clear-bad-pattern']:
                                        clear_bad_pattern = True
                                        continue
                            if 'uppercase' in k and k['uppercase']:
                                ent[name] = val.upper()
                            else:
                                ent[name] = val

                    else:
                        for d in data_items:
                            if d['name'] == name:
                                type = d['type']
                                if val in emptyValue and ('enum' in type or ('default-from' not in d and 'default' not in d)):
                                    if d['mandatory'] and excl_missing_data:
                                        missing_mandatory_data = True
                                        continue
                                    ent[name] = None
                                elif type == 'bool':
                                    try:
                                        ent[name] = val.lower() in trueValue
                                    except ValueError:
                                        if excl_missing_data:
                                            ent[name] = None
                                            continue
                                        if 'remove-bad-pattern' in d and d['remove-bad-pattern']:
                                            remove_bad_pattern = True
                                            continue
                                        if 'clear-bad-pattern' in d and d['clear-bad-pattern']:
                                            clear_bad_pattern = True
                                            continue
                                        raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                         + f"{name} {val!r} must be {self.readableItemType[type]}.")
                                elif type == 'int':
                                    try:
                                        ent[name] = int(val)
                                    except ValueError:
                                        if 'default-from' in d and d['default-from'] == 'self':
                                            i[j] = ent[name] = letterToDigit(val)
                                        elif 'default-from' in d and d['default-from'] in tags:
                                            i[j] = ent[name] = letterToDigit(i[tags.index(d['default-from'])])
                                        elif 'default' in d:
                                            i[j] = ent[name] = int(d['default'])
                                        elif excl_missing_data:
                                            ent[name] = None
                                            continue
                                        elif 'remove-bad-pattern' in d and d['remove-bad-pattern']:
                                            remove_bad_pattern = True
                                            continue
                                        elif 'clear-bad-pattern' in d and d['clear-bad-pattern']:
                                            clear_bad_pattern = True
                                            continue
                                        else:
                                            raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                             + f"{name} {val!r} must be {self.readableItemType[type]}.")
                                elif type in ('index-int', 'positive-int', 'positive-int-as-str'):
                                    try:
                                        ent[name] = int(val)
                                    except ValueError:
                                        if 'default-from' in d and d['default-from'] == 'self':
                                            i[j] = ent[name] = letterToDigit(val, 1)
                                        elif 'default-from' in d and d['default-from'] in tags and i[tags.index(d['default-from'])] not in emptyValue:
                                            i[j] = ent[name] = letterToDigit(i[tags.index(d['default-from'])], 1)
                                        elif 'default-from' in d and d['default-from'].startswith('Auth_asym_ID'):
                                            i[j] = ent[name] = letterToDigit(val, 1)
                                        elif 'default' in d:
                                            i[j] = ent[name] = int(d['default'])
                                        elif excl_missing_data:
                                            ent[name] = None
                                            continue
                                        elif 'remove-bad-pattern' in d and d['remove-bad-pattern']:
                                            remove_bad_pattern = True
                                            continue
                                        elif 'clear-bad-pattern' in d and d['clear-bad-pattern']:
                                            clear_bad_pattern = True
                                            continue
                                        else:
                                            raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                             + f"{name} {val!r} must be {self.readableItemType[type]}.")
                                    if (type == 'index-int' and ent[name] <= 0)\
                                       or (type == 'positive-int' and (ent[name] < 0 or (ent[name] == 0 and 'enforce-non-zero' in d and d['enforce-non-zero']))):
                                        raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                         + f"{name} {val!r} must be {self.readableItemType[type]}.")
                                    if ent[name] == 0 and enforce_non_zero:
                                        if 'void-zero' in d:
                                            if self.replace_zero_by_null_in_case:
                                                loop.data[l][loop.tags.index(name)] = None
                                            ent[name] = None
                                        else:
                                            user_warn_msg += f"[Zero value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                                f"{name} {val!r} should not be zero, "\
                                                f"as defined by {self.readableItemType[type]}.\n"
                                    if type == 'positive-int-as-str':
                                        i[j] = ent[name] = str(ent[name])
                                elif type == 'pointer-index':
                                    try:
                                        ent[name] = int(val)
                                    except ValueError:
                                        if 'default-from' in d and d['default-from'] == 'self':
                                            i[j] = ent[name] = letterToDigit(val, 1)
                                        elif 'default-from' in d and d['default-from'] in tags:
                                            i[j] = ent[name] = letterToDigit(i[tags.index(d['default-from'])], 1)
                                        elif 'default-from' in d and d['default-from'] == 'parent' and parent_pointer is not None:
                                            i[j] = ent[name] = parent_pointer
                                        elif 'default' in d:
                                            i[j] = ent[name] = int(d['default'])
                                        elif excl_missing_data:
                                            ent[name] = None
                                            continue
                                        elif 'remove-bad-pattern' in d and d['remove-bad-pattern']:
                                            remove_bad_pattern = True
                                            continue
                                        elif 'clear-bad-pattern' in d and d['clear-bad-pattern']:
                                            clear_bad_pattern = True
                                            continue
                                        else:
                                            raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                             + f"{name} {val!r} must be {self.readableItemType[type]}.")
                                    if ent[name] <= 0:
                                        raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                         + f"{name} {val!r} must be {self.readableItemType[type]}.")
                                    if static_val[name] is None:
                                        static_val[name] = val
                                    elif val != static_val[name] and test_on_index:
                                        raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                         + f"{name} {val} vs {static_val[name]} must be {self.readableItemType[type]}.")
                                elif type == 'float':
                                    try:
                                        ent[name] = float(val)
                                    except ValueError:
                                        if excl_missing_data:
                                            ent[name] = None
                                            continue
                                        if 'remove-bad-pattern' in d and d['remove-bad-pattern']:
                                            remove_bad_pattern = True
                                            continue
                                        if 'clear-bad-pattern' in d and d['clear-bad-pattern']:
                                            clear_bad_pattern = True
                                            continue
                                        raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                         + f"{name} {val!r} must be {self.readableItemType[type]}.")
                                elif type == 'positive-float':
                                    try:
                                        ent[name] = float(val)
                                    except ValueError:
                                        if excl_missing_data:
                                            ent[name] = None
                                            continue
                                        if 'remove-bad-pattern' in d and d['remove-bad-pattern']:
                                            remove_bad_pattern = True
                                            continue
                                        if 'clear-bad-pattern' in d and d['clear-bad-pattern']:
                                            clear_bad_pattern = True
                                            continue
                                        raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                         + f"{name} {val!r} must be {self.readableItemType[type]}.")
                                    if ent[name] < 0.0 or (ent[name] == 0.0 and 'enforce-non-zero' in d and d['enforce-non-zero']):
                                        raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                         + f"{name} {val!r} must be {self.readableItemType[type]}.")
                                    if ent[name] == 0.0 and enforce_non_zero:
                                        if 'void-zero' in d:
                                            if self.replace_zero_by_null_in_case:
                                                loop.data[l][loop.tags.index(name)] = None
                                            ent[name] = None
                                        else:
                                            user_warn_msg += f"[Zero value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                                f"{name} {val!r} should not be zero, "\
                                                f"as defined by {self.readableItemType[type]}.\n"
                                elif type == 'range-float':
                                    try:
                                        _range = d['range']
                                        ent[name] = float(val)
                                    except KeyError:
                                        raise ValueError(f"Range of data item {name} is not defined")
                                    except ValueError:
                                        if excl_missing_data:
                                            ent[name] = None
                                            continue
                                        if not enforce_range:
                                            ent[name] = None
                                            continue
                                        if 'remove-bad-pattern' in d and d['remove-bad-pattern']:
                                            remove_bad_pattern = True
                                            continue
                                        if 'clear-bad-pattern' in d and d['clear-bad-pattern']:
                                            clear_bad_pattern = True
                                            continue
                                        user_warn_msg += f"[Range value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                            f"{name} {val!r} must be {self.readableItemType[type]}.\n"
                                    if ('min_exclusive' in _range and _range['min_exclusive'] == 0.0 and ent[name] <= 0.0)\
                                       or ('min_inclusive' in _range and _range['min_inclusive'] == 0.0 and ent[name] < 0):
                                        if ent[name] < 0.0:
                                            if ('max_inclusive' in _range and abs(ent[name]) > _range['max_inclusive'])\
                                               or ('max_exclusive' in _range and abs(ent[name]) >= _range['max_exclusive'])\
                                               or ('enforce-sign' in d and d['enforce-sign']):
                                                if not enforce_range:
                                                    ent[name] = None
                                                else:
                                                    user_warn_msg += f"[Range value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                                        f"{name} {val!r} must be within range {_range}.\n"
                                            elif enforce_sign:
                                                user_warn_msg += f"[Negative value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                                    f"{name} {val!r} should not have "\
                                                    f"negative value for {self.readableItemType[type]}, {_range}.\n"
                                        elif ent[name] == 0.0 and 'enforce-non-zero' in d and d['enforce-non-zero']:
                                            if not enforce_range:
                                                ent[name] = None
                                            else:
                                                user_warn_msg += f"[Range value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                                    f"{name} {val!r} must be within range {_range}.\n"
                                        elif ent[name] == 0.0 and enforce_non_zero:
                                            if 'void-zero' in d:
                                                if self.replace_zero_by_null_in_case:
                                                    loop.data[l][loop.tags.index(name)] = None
                                                ent[name] = None
                                            else:
                                                user_warn_msg += f"[Zero value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                                    f"{name} {val!r} should not be zero, "\
                                                    f"as defined by {self.readableItemType[type]}, {_range}.\n"
                                        elif 'remove-bad-pattern' in d and d['remove-bad-pattern']:
                                            remove_bad_pattern = True
                                            continue
                                        elif 'clear-bad-pattern' in d and d['clear-bad-pattern']:
                                            clear_bad_pattern = True
                                            continue
                                    elif ('min_exclusive' in _range and ent[name] <= _range['min_exclusive']) or\
                                         ('min_inclusive' in _range and ent[name] < _range['min_inclusive']) or\
                                         ('max_inclusive' in _range and ent[name] > _range['max_inclusive']) or\
                                         ('max_exclusive' in _range and ent[name] >= _range['max_exclusive']):
                                        if 'void-zero' in d and ent[name] == 0.0:
                                            if self.replace_zero_by_null_in_case:
                                                loop.data[l][loop.tags.index(name)] = None
                                            ent[name] = None
                                        elif not enforce_range:
                                            ent[name] = None
                                        elif 'remove-bad-pattern' in d and d['remove-bad-pattern']:
                                            remove_bad_pattern = True
                                            continue
                                        elif 'clear-bad-pattern' in d and d['clear-bad-pattern']:
                                            clear_bad_pattern = True
                                            continue
                                        else:
                                            user_warn_msg += f"[Range value error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                                f"{name} {val!r} must be within range {_range}.\n"
                                elif type == 'enum':
                                    try:
                                        enum = d['enum']
                                        if val not in enum:
                                            if 'default-from' in d and d['default-from'] in tags:
                                                if i[tags.index(d['default-from'])][0].upper() in enum:
                                                    val = i[tags.index(d['default-from'])][0].upper()
                                            elif 'enum-alt' in d and val in d['enum-alt']:
                                                val = d['enum-alt'][val]
                                                i[j] = val
                                            elif 'enforce-enum' in d and d['enforce-enum']:
                                                if excl_missing_data:
                                                    ent[name] = None
                                                    continue
                                                raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                                 + f"{name} {val!r} must be one of {enum}.")
                                            elif enforce_enum:
                                                user_warn_msg += f"[Enumeration error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                                    f"{name} {val!r} should be one of {enum}.\n"
                                            elif 'remove-bad-pattern' in d and d['remove-bad-pattern']:
                                                remove_bad_pattern = True
                                                continue
                                            elif 'clear-bad-pattern' in d and d['clear-bad-pattern']:
                                                clear_bad_pattern = True
                                                continue
                                        ent[name] = val
                                    except KeyError:
                                        raise ValueError(f"Enumeration of data item {name} is not defined")
                                elif type == 'enum-int':
                                    try:
                                        enum = d['enum']
                                        if int(val) not in enum:
                                            if 'default-from' in d and d['default-from'] in tags:
                                                if i[tags.index(d['default-from'])][0].upper() in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS:
                                                    val = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[i[tags.index(d['default-from'])][0].upper()][0]
                                            if 'enforce-enum' in d and d['enforce-enum']:
                                                raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                                 + f"{name} {val!r} must be one of {enum}.")
                                            if enforce_enum:
                                                user_warn_msg += f"[Enumeration error] {get_idx_msg(idx_tag_ids, tags, ent)}"\
                                                    f"{name} {val!r} should be one of {enum}.\n"
                                            elif 'remove-bad-pattern' in d and d['remove-bad-pattern']:
                                                remove_bad_pattern = True
                                                continue
                                            elif 'clear-bad-pattern' in d and d['clear-bad-pattern']:
                                                clear_bad_pattern = True
                                                continue
                                        ent[name] = int(val)
                                    except KeyError:
                                        raise ValueError(f"Enumeration of data item {name} is not defined")
                                    except ValueError:
                                        if excl_missing_data:
                                            ent[name] = None
                                            continue
                                        raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                         + f"{name} {val!r} must be {self.readableItemType[type]}.")
                                else:
                                    if ('remove-bad-pattern' in d and d['remove-bad-pattern']) or ('clear-bad-pattern' in d and d['clear-bad-pattern']):
                                        if badPattern.match(val):
                                            if 'remove-bad-pattern' in d and d['remove-bad-pattern']:
                                                remove_bad_pattern = True
                                                continue
                                            if 'clear-bad-pattern' in d and d['clear-bad-pattern']:
                                                clear_bad_pattern = True
                                                continue
                                    if 'uppercase' in d and d['uppercase']:
                                        ent[name] = val.upper()
                                    else:
                                        ent[name] = val

                for d in data_items:
                    if 'group-mandatory' in d and d['group-mandatory']:
                        name = d['name']
                        group = d['group']
                        if name in ent and ent[name] is not None:
                            if group['coexist-with'] is not None:
                                for cw in group['coexist-with']:
                                    if cw not in ent or ent[cw] is None:
                                        raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                         + f"One of data item {cw} must not be empty for a row having {name} {ent[name]!r}.")

                            if 'smaller-than' in group and group['smaller-than'] is not None:
                                for st in group['smaller-than']:
                                    if st in ent and ent[st] is not None:
                                        if ent[name] < ent[st]:
                                            if 'circular-shift' in group:
                                                ent[st] -= abs(group['circular-shift'])
                                            if ent[name] < ent[st]:
                                                raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                                 + f"Data item {name} {ent[name]!r} must be larger than {st} {ent[st]!r}.")

                            if 'larger-than' in group and group['larger-than'] is not None:
                                for lt in group['larger-than']:
                                    if lt in ent and ent[lt] is not None:
                                        if ent[name] > ent[lt]:
                                            if 'circular-shift' in group:
                                                ent[lt] += abs(group['circular-shift'])
                                            if ent[name] > ent[lt]:
                                                raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                                 + f"Data item {name} {ent[name]!r} must be smaller than {lt} {ent[lt]!r}.")

                            if 'not-equal-to' in group and group['not-equal-to'] is not None:
                                for ne in group['not-equal-to']:
                                    if ne in ent and ent[ne] is not None:
                                        if ent[name] == ent[ne]:
                                            raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                             + f"Data item {name} {ent[name]!r} must not be equal to {ne} {ent[ne]!r}.")

                        elif group['member-with'] is not None:
                            has_member = False
                            for mw in group['member-with']:
                                if mw in ent and ent[mw] is not None:
                                    has_member = True
                                    break
                            if not has_member:
                                member = set(group['member-with'])
                                member.add(name)
                                raise ValueError(get_idx_msg(idx_tag_ids, tags, ent)
                                                 + f"One of data items {member} must not be empty.")

                if missing_mandatory_data:
                    continue

                if remove_bad_pattern:
                    r = {}
                    for j, t in enumerate(loop.tags):
                        r[t] = loop.data[l][j]
                    user_warn_msg += f"[Remove bad pattern] Found bad pattern. "\
                        f"#_of_row {l + 1}, data_of_row {r}.\n"
                    continue  # should be removed from loop later

                if clear_bad_pattern:
                    r = {}
                    for j, t in enumerate(loop.tags):
                        r[t] = loop.data[l][j]
                    user_warn_msg += f"[Clear bad pattern] Found bad pattern. "\
                        f"#_of_row {l + 1}, data_of_row {r}.\n"
                    for k in key_items:
                        if k in loop.tags and 'clear-bad-pattern' in k and k['clear-bad-pattern']:
                            i[loop.tags.index(k)] = '?'
                            ent[k] = None
                    for d in data_items:
                        if d in loop.tags and 'clear-bad-pattern' in d and d['clear-bad-pattern']:
                            i[loop.tags.index(d)] = '?'
                            ent[d] = None

                asm.append(ent)

            data.append(asm)

        if len(user_warn_msg) > 0:
            raise UserWarning(user_warn_msg)

        if len(data) == 0:
            data.append([])

        return data

    def get_conflict_id(self, star_data, lp_category, key_items):  # pylint: disable=no-self-use
        """ Return list of conflicted row IDs except for rows of the first occurrence.
            @author: Masashi Yokochi
            @return: list of row IDs in reverse order for each loop
        """

        try:
            loops = star_data.get_loops_by_category(lp_category)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            try:
                if __pynmrstar_v3_2__:
                    loops = [star_data.get_loop(lp_category)]
                else:
                    loops = [star_data.get_loop_by_category(lp_category)]
            except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
                loops = [star_data]

        data = []  # data of all loops

        key_names = [k['name'] for k in key_items]
        uppercases = [('uppercase' in k and k['uppercase']) for k in key_items]

        key_len = len(key_items)

        for loop in loops:

            if len(key_names) > 0 and set(key_names) & set(loop.tags) != set(key_names):
                missing_tags = list(set(key_names) - set(loop.tags))
                for k in key_items:
                    if k['name'] in missing_tags:
                        if 'default' in k:
                            for row in loop.data:
                                row.append(k['default'])
                            loop.add_tag(k['name'])
                        else:
                            raise LookupError(f"Missing mandatory {missing_tags} loop tag(s).")

            keys = set()
            dup_ids = set()

            for l, i in enumerate(get_lp_tag(loop, key_names)):  # noqa: E741

                key = ''
                for j in range(key_len):
                    key += ' ' + (i[j].upper() if uppercases[j] else i[j])
                key.rstrip()

                if key in keys:
                    dup_ids.add(l)

                else:
                    keys.add(key)

            data.append(sorted(list(dup_ids), reverse=True))

        return data

    def get_conflict_id_set(self, star_data, lp_category, key_items):  # pylint: disable=no-self-use
        """ Return list of conflicted row ID sets.
            @author: Masashi Yokochi
            @return: list of row ID sets for each loop
        """

        try:
            loops = star_data.get_loops_by_category(lp_category)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            try:
                if __pynmrstar_v3_2__:
                    loops = [star_data.get_loop(lp_category)]
                else:
                    loops = [star_data.get_loop_by_category(lp_category)]
            except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
                loops = [star_data]

        data = []  # data of all loops

        key_names = [k['name'] for k in key_items]
        uppercases = [('uppercase' in k and k['uppercase']) for k in key_items]

        key_len = len(key_items)

        for loop in loops:

            if len(key_names) > 0 and set(key_names) & set(loop.tags) != set(key_names):
                missing_tags = list(set(key_names) - set(loop.tags))
                raise LookupError(f"Missing mandatory {missing_tags} loop tag(s).")

            tag_data = get_lp_tag(loop, key_names)

            keys = set()
            dup_ids = set()

            for l, i in enumerate(tag_data):  # noqa: E741

                key = ''
                for j in range(key_len):
                    key += ' ' + (i[j].upper() if uppercases[j] else i[j])
                key.rstrip()

                if key in keys:
                    dup_ids.add(l)

                else:
                    keys.add(key)

            conflict_id = sorted(list(dup_ids), reverse=True)

            if len(conflict_id) == 0:
                data.append(None)

            else:
                conflict_id_set = []

                for l in conflict_id:  # noqa: E741

                    key = ''
                    for j in range(key_len):
                        key += ' ' + tag_data[l][j]
                        key.rstrip()

                    id_set = [l]

                    for m in range(l):

                        _key = ''
                        for j in range(key_len):
                            _key += ' ' + tag_data[m][j]
                            _key.rstrip()

                        if key == _key:
                            id_set.append(m)

                            if m in conflict_id:
                                conflict_id.remove(m)

                    if len(id_set) > 1:
                        conflict_id_set.insert(0, sorted(id_set))

                data.append(conflict_id_set)

        return data

    def get_conflict_atom_id(self, star_data, file_type, lp_category, key_items):
        """ Return list of row IDs that include self atoms.
            @author: Masashi Yokochi
            @return: list of row IDs in reverse order for each loop
        """

        try:
            loops = star_data.get_loops_by_category(lp_category)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            try:
                if __pynmrstar_v3_2__:
                    loops = [star_data.get_loop(lp_category)]
                else:
                    loops = [star_data.get_loop_by_category(lp_category)]
            except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
                loops = [star_data]

        data = []  # data of all loops

        key_names = [k['name'] for k in key_items]

        for loop in loops:

            if len(key_names) > 0 and set(key_names) & set(loop.tags) != set(key_names):
                missing_tags = list(set(key_names) - set(loop.tags))
                for k in key_items:
                    if k['name'] in missing_tags:
                        if 'default' in k:
                            for row in loop.data:
                                row.append(k['default'])
                            loop.add_tag(k['name'])
                        else:
                            raise LookupError(f"Missing mandatory {missing_tags} loop tag(s).")

            atom_keys = self.get_atom_keys(loop.get_tag_names(), file_type)

            len_atom_keys = len(atom_keys)

            dup_ids = set()

            for tag, i in enumerate(get_lp_tag(loop, key_names)):

                for j in range(0, len_atom_keys - 2):
                    atom_key_j = atom_keys[j]
                    chain_id_j = i[key_names.index(atom_key_j['chain_tag'])]
                    seq_id_j = i[key_names.index(atom_key_j['seq_tag'])]
                    atom_id_j = i[key_names.index(atom_key_j['atom_tag'])]

                    for k in range(j + 1, len_atom_keys - 1):
                        atom_key_k = atom_keys[k]
                        chain_id_k = i[key_names.index(atom_key_k['chain_tag'])]
                        seq_id_k = i[key_names.index(atom_key_k['seq_tag'])]
                        atom_id_k = i[key_names.index(atom_key_k['atom_tag'])]

                        if chain_id_j == chain_id_k and seq_id_j == seq_id_k and atom_id_j == atom_id_k:
                            dup_ids.add(tag)
                            break

            data.append(sorted(list(dup_ids), reverse=True))

        return data

    def get_bad_pattern_id(self, star_data, lp_category, key_items, data_items):  # pylint: disable=no-self-use
        """ Return list of row IDs with bad patterns
            @author: Masashi Yokochi
            @return: list of row IDs in reverse order for each loop
        """

        try:
            loops = star_data.get_loops_by_category(lp_category)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            try:
                if __pynmrstar_v3_2__:
                    loops = [star_data.get_loop(lp_category)]
                else:
                    loops = [star_data.get_loop_by_category(lp_category)]
            except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
                loops = [star_data]

        data = []  # data of all loops

        key_names = [k['name'] for k in key_items if 'remove-bad-pattern' in k and k['remove-bad-pattern']]
        data_names = [d['name'] for d in data_items if 'remove-bad-pattern' in d and d['remove-bad-pattern']]

        key_names.extend(data_names)

        for loop in loops:

            bad_ids = set()

            for tag, i in enumerate(get_lp_tag(loop, key_names)):

                if any(badPattern.match(d) for d in i):
                    bad_ids.add(tag)

            data.append(sorted(list(bad_ids), reverse=True))

        return data

    def check_sf_tag(self, star_data, file_type, category, tag_items, allowed_tags=None,
                     enforce_non_zero=False, enforce_sign=False, enforce_range=False, enforce_enum=False):
        """ Extract saveframe tags with sanity check.
            @author: Masashi Yokochi
            @return: list of extracted saveframe tags
        """

        user_warn_msg = ''

        item_types = ('str', 'bool', 'int', 'positive-int', 'positive-int-as-str',
                      'float', 'positive-float', 'range-float', 'enum', 'enum-int')

        tag_names = [t['name'] for t in tag_items]
        mand_tag_names = [t['name'] for t in tag_items if t['mandatory']]

        for t in tag_items:
            if t['type'] not in item_types:
                raise TypeError(f"Type {t['type']} of tag item {t['name']} must be one of {item_types}.")

        if allowed_tags is not None:

            if (set(tag_names) | set(allowed_tags)) != set(allowed_tags):
                raise LookupError(f"Tag items {((set(tag_names) | set(allowed_tags)) - set(allowed_tags))} must not exists.")

            for t in tag_items:
                if 'group-mandatory' in t and t['group-mandatory']:
                    group = t['group']
                    if group['member-with'] is not None:
                        for mw in group['member-with']:
                            if mw not in allowed_tags:
                                raise ValueError(f"Member tag item {mw} of {t['name']} must exists in allowed tags.")
                    if group['coexist-with'] is not None:
                        for cw in group['coexist-with']:
                            if cw not in allowed_tags:
                                raise ValueError(f"Coexisting tag item {cw} of {t['name']} must exists in allowed tags.")

        sf_tags = {i[0]: i[1] for i in star_data.tags}

        if len(mand_tag_names) > 0 and set(mand_tag_names) & set(sf_tags.keys()) != set(mand_tag_names):
            missing_tags = list(set(mand_tag_names) - set(sf_tags.keys()))
            raise LookupError(f"Missing mandatory {missing_tags} saveframe tag(s).")

        for t in tag_items:
            if 'group-mandatory' in t and t['group-mandatory']:
                name = t['name']
                group = t['group']
                if name in sf_tags.keys():
                    if group['coexist-with'] is not None:
                        for cw in group['coexist-with']:
                            if cw not in sf_tags.keys():
                                set_cw = set(group['coexist-with'])
                                set_cw.add(name)
                                missing_tags = list(set_cw - set(sf_tags.keys()))
                                raise LookupError(f"Missing mandatory {missing_tags} saveframe tag(s).")

                elif group['member-with'] is not None:
                    has_member = False
                    for mw in group['member-with']:
                        if mw in sf_tags.keys():
                            has_member = True
                            break
                    if not has_member:
                        set_mw = set(group['member-with'])
                        set_mw.add(name)
                        missing_tags = list(set_mw - set(sf_tags.keys()))
                        raise LookupError(f"Missing mandatory {missing_tags} saveframe tag(s).")

        for name, val in sf_tags.items():
            if val in emptyValue:
                for t in tag_items:
                    if t['name'] == name and t['mandatory'] and 'default' not in t:
                        raise ValueError(f"{name} must not be empty.")

        ent = {}  # entity

        for name, val in sf_tags.items():
            for t in tag_items:
                if t['name'] == name:
                    type = t['type']  # pylint: disable=redefined-builtin
                    if val in emptyValue and 'enum' not in type and 'default-from' not in t and 'default' not in t:
                        ent[name] = None
                    elif type == 'bool':
                        try:
                            ent[name] = val.lower() in trueValue
                        except ValueError:
                            raise ValueError(f"{name} {val!r} must be {self.readableItemType[type]}.")
                    elif type == 'int':
                        try:
                            ent[name] = int(val)
                        except ValueError:
                            if 'default-from' in t and t['default-from'] == 'self':
                                ent[name] = letterToDigit(val)
                            elif 'default-from' in t and t['default-from'] in sf_tags.keys():
                                ent[name] = letterToDigit(sf_tags[t['default-from']])
                            elif 'default' in t:
                                ent[name] = int(t['default'])
                            else:
                                raise ValueError(f"{name} {val!r} must be {self.readableItemType[type]}.")
                    elif type in ('positive-int', 'positive-int-as-str'):
                        try:
                            ent[name] = int(val)
                        except ValueError:
                            if 'default-from' in t and t['default-from'] == 'self':
                                ent[name] = letterToDigit(val, 1)
                            elif 'default-from' in t and t['default-from'] in sf_tags.keys() and sf_tags[t['default-from']] not in emptyValue:
                                ent[name] = letterToDigit(sf_tags[t['default-from']], 1)
                            elif 'default-from' in t and t['default-from'].startswith('Auth_asym_ID'):
                                ent[name] = letterToDigit(val, 1)
                            elif 'default' in t:
                                ent[name] = int(t['default'])
                            else:
                                raise ValueError(f"{name} {val!r} must be {self.readableItemType[type]}.")
                        if ent[name] < 0 or (ent[name] == 0 and 'enforce-non-zero' in t and t['enforce-non-zero']):
                            raise ValueError(f"{name} {val!r} must be {self.readableItemType[type]}.")
                        if ent[name] == 0 and enforce_non_zero:
                            if 'void-zero' in t:
                                if self.replace_zero_by_null_in_case:
                                    star_data.tags[sf_tags.keys().index(name)][1] = None
                                ent[name] = None
                            else:
                                user_warn_msg += f"[Zero value error] {name} {val!r} should not be zero, "\
                                    f"as defined by {self.readableItemType[type]}.\n"
                        if type == 'positive-int-as-str':
                            ent[name] = str(ent[name])
                    elif type == 'float':
                        try:
                            ent[name] = float(val)
                        except ValueError:
                            raise ValueError(f"{name} {val!r} must be {self.readableItemType[type]}.")
                    elif type == 'positive-float':
                        try:
                            ent[name] = float(val)
                        except ValueError:
                            raise ValueError(f"{name} {val!r} must be {self.readableItemType[type]}.")
                        if ent[name] < 0.0 or (ent[name] == 0.0 and 'enforce-non-zero' in t and t['enforce-non-zero']):
                            raise ValueError(f"{name} {val!r} must be {self.readableItemType[type]}.")
                        if ent[name] == 0.0 and enforce_non_zero:
                            if 'void-zero' in t:
                                if self.replace_zero_by_null_in_case:
                                    star_data.tags[sf_tags.keys().index(name)][1] = None
                                ent[name] = None
                            else:
                                user_warn_msg += f"[Zero value error] {name} {val!r} should not be zero, "\
                                    f"as defined by {self.readableItemType[type]}.\n"
                    elif type == 'range-float':
                        try:
                            _range = t['range']
                            ent[name] = float(val)
                        except KeyError:
                            raise ValueError(f"Range of tag item {name} is not defined.")
                        except ValueError:
                            if not enforce_range:
                                ent[name] = None
                                continue
                            user_warn_msg += f"[Range value error] {name} {val!r} must be {self.readableItemType[type]}.\n"
                        if ('min_exclusive' in _range and _range['min_exclusive'] == 0.0 and ent[name] <= 0.0)\
                           or ('min_inclusive' in _range and _range['min_inclusive'] == 0.0 and ent[name] < 0):
                            if ent[name] < 0.0:
                                if ('max_inclusive' in _range and abs(ent[name]) > _range['max_inclusive'])\
                                   or ('max_exclusive' in _range and abs(ent[name]) >= _range['max_exclusive'])\
                                   or ('enforce-sign' in t and t['enforce-sign']):
                                    if not enforce_range:
                                        ent[name] = None
                                    else:
                                        user_warn_msg += f"[Range value error] {name} {val!r} must be within range {_range}.\n"
                                elif enforce_sign:
                                    user_warn_msg += f"[Negative value error] {name} {val!r} should not have "\
                                        f"negative value for {self.readableItemType[type]}, {_range}.\n"
                            elif ent[name] == 0.0 and 'enforce-non-zero' in t and t['enforce-non-zero']:
                                if not enforce_range:
                                    ent[name] = None
                                else:
                                    user_warn_msg += f"[Range value error] {name} {val!r} must be within range {_range}.\n"
                            elif ent[name] == 0.0 and enforce_non_zero:
                                if 'void-zero' in t:
                                    if self.replace_zero_by_null_in_case:
                                        star_data.tags[sf_tags.keys().index(name)][1] = None
                                    ent[name] = None
                                else:
                                    user_warn_msg += f"[Zero value error] {name} {val!r} should not be zero, "\
                                        f"as defined by {self.readableItemType[type]}, {_range}.\n"
                        elif ('min_exclusive' in _range and ent[name] <= _range['min_exclusive']) or\
                             ('min_inclusive' in _range and ent[name] < _range['min_inclusive']) or\
                             ('max_inclusive' in _range and ent[name] > _range['max_inclusive']) or\
                             ('max_exclusive' in _range and ent[name] >= _range['max_exclusive']):
                            if 'void-zero' in t and ent[name] == 0.0:
                                if self.replace_zero_by_null_in_case:
                                    star_data.tags[sf_tags.keys().index(name)][1] = None
                                ent[name] = None
                            elif not enforce_range:
                                ent[name] = None
                            else:
                                user_warn_msg += f"[Range value error] {name} {val} must be within range {_range}.\n"
                    elif type == 'enum':
                        if val in emptyValue:
                            val = '?'  # '.' raises internal error in NmrDpUtility
                        try:
                            enum = t['enum']
                            if val not in enum:
                                if 'enum-alt' in t and val in t['enum-alt']:
                                    tagNames = [_t[0] for _t in star_data.tags]
                                    itCol = tagNames.index(name)
                                    itName = '_' + category + '.' + t['name']
                                    if val == '?' and enforce_enum:
                                        if self.is_mandatory_tag(itName, file_type):
                                            user_warn_msg += f"[Enumeration error] The mandatory type {itName} {val!r} is missing "\
                                                f"and the type must be one of {enum}. {t['enum-alt'][val]} will be given "\
                                                f"unless you would like to fix the type and re-upload the {file_type.upper()} file.\n"
                                            val = t['enum-alt'][val]
                                            star_data.tags[itCol][1] = val
                                        else:
                                            user_warn_msg += f"[Enumeration error] {name} {val!r} should be one of {enum}. "\
                                                "The type may be filled with either 'undefined' or estimated value "\
                                                f"unless you would like to fix the type and re-upload the {file_type.upper()} file.\n"
                                    else:
                                        val = t['enum-alt'][val]
                                        star_data.tags[itCol][1] = val
                                elif 'enforce-enum' in t and t['enforce-enum']:
                                    raise ValueError(f"{name} {val!r} must be one of {enum}.")
                                elif enforce_enum:
                                    user_warn_msg += f"[Enumeration error] {name} {val!r} should be one of {enum}.\n"
                            ent[name] = None if val in emptyValue else val
                        except KeyError:
                            raise ValueError(f"Enumeration of tag item {name} is not defined.")
                    elif type == 'enum-int':
                        try:
                            enum = t['enum']
                            if int(val) not in enum:
                                if 'enforce-enum' in t and t['enforce-enum']:
                                    raise ValueError(f"{name} {val!r} must be one of {enum}.")
                                if enforce_enum:
                                    user_warn_msg += f"[Enumeration error] {name} {val!r} should be one of {enum}.\n"
                            ent[name] = int(val)
                        except KeyError:
                            raise ValueError(f"Enumeration of tag item {name} is not defined.")
                        except ValueError:
                            raise ValueError(f"{name} {val!r} must be {self.readableItemType[type]}.")
                    else:
                        ent[name] = val

            for t in tag_items:
                if 'group-mandatory' in t and t['group-mandatory']:
                    name = t['name']
                    group = t['group']
                    if name in ent and ent[name] is not None:
                        if group['coexist-with'] is not None:
                            for cw in group['coexist-with']:
                                if cw not in ent or ent[cw] is None:
                                    raise ValueError(f"One of tag item {cw} must not be empty due to {name} {ent[name]!r}.")

                        if 'smaller-than' in group and group['smaller-than'] is not None:
                            for st in group['smaller-than']:
                                if st in ent and ent[st] is not None:
                                    if ent[name] < ent[st]:
                                        if 'circular-shift' in group:
                                            ent[st] -= abs(group['circular-shift'])
                                        if ent[name] < ent[st]:
                                            raise ValueError(f"Tag item {name} {ent[name]!r} must be larger than {st} {ent[st]!r}.")

                        if 'larger-than' in group and group['larger-than'] is not None:
                            for lt in group['larger-than']:
                                if lt in ent and ent[lt] is not None:
                                    if ent[name] > ent[lt]:
                                        if 'circular-shift' in group:
                                            ent[lt] += abs(group['circular-shift'])
                                        if ent[name] > ent[lt]:
                                            raise ValueError(f"Tag item {name} {ent[name]!r} must be smaller than {lt} {ent[lt]!r}.")

                        if 'not-equal-to' in group and group['not-equal-to'] is not None:
                            for ne in group['not-equal-to']:
                                if ne in ent and ent[ne] is not None:
                                    if ent[name] == ent[ne]:
                                        raise ValueError(f"Tag item {name} {ent[name]!r} must not be equal to {ne} {ent[ne]!r}.")

                    elif group['member-with'] is not None:
                        has_member = False
                        for mw in group['member-with']:
                            if mw in ent and ent[mw] is not None:
                                has_member = True
                                break
                        if not has_member:
                            member = set(group['member-with'])
                            member.add(name)
                            raise ValueError(f"One of tag items {member} must not be empty.")

        if len(user_warn_msg) > 0:
            raise UserWarning(user_warn_msg)

        return ent

    def validate_comp_atom(self, comp_id, atom_id):
        """ Validate atom_id of comp_id.
            @change: support non-standard residue by Masashi Yokochi
            @return: True for valid atom_id of comp_id, False otherwise
        """

        if comp_id in emptyValue:
            return False

        comp_id = comp_id.upper()

        if self.__ccU.updateChemCompDict(comp_id):
            return atom_id in [a[self.__ccU.ccaAtomId] for a in self.__ccU.lastAtomList]

        return False

    def validate_atom(self, star_data, lp_category='Atom_chem_shift', comp_id='Comp_ID', atom_id='Atom_ID'):
        """ Validate atom_id in a given loop against CCD.
            @deprecated: used only for testing
            @change: support non-standard residue by Masashi Yokochi
            @return: list of valid row data
        """

        try:
            loops = star_data.get_loops_by_category(lp_category)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            try:
                if __pynmrstar_v3_2__:
                    loops = [star_data.get_loop(lp_category)]
                else:
                    loops = [star_data.get_loop_by_category(lp_category)]
            except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
                loops = [star_data]

        valid_row = []

        for loop in loops:

            try:

                data = get_lp_tag(loop, [comp_id, atom_id])

                for j in data:

                    _comp_id = j[0].upper()
                    _atom_id = j[1].upper()

                    if _comp_id in emptyValue:
                        valid_row.append(j)

                    else:
                        if self.__ccU.updateChemCompDict(_comp_id):
                            if _atom_id not in [a[self.__ccU.ccaAtomId] for a in self.__ccU.lastAtomList]:
                                valid_row.append(j)
                        else:
                            valid_row.append(j)

            except ValueError as e:
                self.__lfh.write(f"+NEFTranslator.validate_atom() ++ ValueError  - {str(e)}\n")

        return valid_row

    def get_star_tag(self, nef_tag):
        """ Return NMR-STAR saveframe/loop tag corresponding to NEF tag.
            @change: rename the original get_nmrstar_tag() to get_star_tag() by Masashi Yokochi
            @return: NMR-STAR's author tag and data tag corresponding to a given NEF tag
        """

        try:

            n = self.tagMap[0].index(nef_tag)

            return self.tagMap[1][n], self.tagMap[2][n], n  # author tag, data tag

        except ValueError:
            return None, None, None

    def get_nef_tag(self, star_tag):
        """ Return NEF saveframe/loop tag corresponding to NMR-STAR tag.
            @author: Masashi Yokochi
            @return: NEF data tag corresponding to a given NMR-STAR tag
        """

        try:

            n = self.tagMap[2].index(star_tag)  # NEF has no auth tags

            return self.tagMap[0][n], n

        except ValueError:  # None for NMR-STAR specific tag
            return None, None

    def get_star_auth_tag(self, star_tag):
        """ Return NMR-STAR saveframe/loop author tag corresponding to NMR-STAR data tag.
            @return: NMR-STAR's author tag corresponding to a given NMR-STAR data tag
        """

        try:

            n = self.tagMap[2].index(star_tag)

            return self.tagMap[1][n], n  # author tag

        except ValueError:
            return None, None

    def get_star_loop_tags(self, nef_loop_tags):
        """ Return list of NMR-STAR loop tags corresponding to NEF loop tags.
            @change: rename the original get_nmrstar_loop_tags() to get_star_loop_tags() by Masashi Yokochi
            @return: list of NMR-STAR loop tags corresponding to given NEF loop tags
        """

        out_tag_w_ordinal = {}
        out_tag = []

        for j in nef_loop_tags:

            auth_tag, data_tag, ordinal = self.get_star_tag(j)

            if auth_tag is None:
                continue

            out_tag_w_ordinal[data_tag] = ordinal

            if auth_tag != data_tag:
                out_tag_w_ordinal[auth_tag] = ordinal + 100

        out_tag = [t[0] for t in sorted(out_tag_w_ordinal.items(), key=lambda x:x[1])]

        lp_category = nef_loop_tags[0].split('.')[0]

        if lp_category == '_nef_sequence':
            out_tag.append('_Chem_comp_assembly.Assembly_ID')

        elif lp_category == '_nef_covalent_links':
            out_tag.insert(0, '_Bond.ID')
            out_tag.insert(1, '_Bond.Type')
            out_tag.insert(2, '_Bond.Value_order')
            out_tag.append('_Bond.Assembly_ID')

        elif lp_category == '_nef_chemical_shift':
            out_tag.insert(0, '_Atom_chem_shift.ID')
            out_tag.insert(9, '_Atom_chem_shift.Ambiguity_code')
            out_tag.insert(10, '_Atom_chem_shift.Ambiguity_set_ID')

            if self.insert_original_pdb_cs_items:
                out_tag.append('_Atom_chem_shift.Original_PDB_strand_ID')
                out_tag.append('_Atom_chem_shift.Original_PDB_residue_no')
                out_tag.append('_Atom_chem_shift.Original_PDB_residue_name')
                out_tag.append('_Atom_chem_shift.Original_PDB_atom_name')

            out_tag.append('_Atom_chem_shift.Details')
            out_tag.append('_Atom_chem_shift.Assigned_chem_shift_list_ID')

        elif lp_category == '_nef_distance_restraint':
            out_tag.append('_Gen_dist_constraint.Member_logic_code')
            out_tag.append('_Gen_dist_constraint.Gen_dist_constraint_list_ID')

        elif lp_category == '_nef_dihedral_restraint':
            out_tag.append('_Torsion_angle_constraint.Torsion_angle_constraint_list_ID')

        elif lp_category == '_nef_rdc_restraint':
            out_tag.append('_RDC_constraint.RDC_constraint_list_ID')

        elif lp_category == '_nef_peak':
            out_tag.append('_Peak_row_format.Details')
            out_tag.append('_Peak_row_format.Spectral_peak_list_ID')

        elif lp_category == '_nef_spectrum_dimension':
            out_tag.append('_Spectral_dim.Spectral_peak_list_ID')

        elif lp_category == '_nef_spectrum_dimension_transfer':
            out_tag.append('_Spectral_dim_transfer.Spectral_peak_list_ID')

        return out_tag

    def extend_star_loop_tags(self, star_loop_tags):
        """ Return list of NMR-STAR loop tags in addition to given NMR-STAR loop tags.
            @return: list of extended NMR-STAR loop tags
        """

        out_tag_w_ordinal = {}
        out_tag = []

        for data_tag in star_loop_tags:

            auth_tag, ordinal = self.get_star_auth_tag(data_tag)

            if auth_tag is None:
                continue

            out_tag_w_ordinal[data_tag] = ordinal

            if auth_tag != data_tag:
                out_tag_w_ordinal[auth_tag] = ordinal + 100

        out_tag = [t[0] for t in sorted(out_tag_w_ordinal.items(), key=lambda x:x[1])]

        lp_category = star_loop_tags[0].split('.')[0]

        if lp_category == '_Chem_comp_assembly':
            if '_Chem_comp_assembly.Assembly_ID' not in out_tag:
                out_tag.append('_Chem_comp_assembly.Assembly_ID')

        elif lp_category == '_Bond':
            if '_Bond.ID' not in out_tag:
                out_tag.insert(0, '_Bond.ID')
            if '_Bond.Type' not in out_tag:
                out_tag.insert(1, '_Bond.Type')
            if '_Bond.Value_order' not in out_tag:
                out_tag.insert(2, '_Bond.Value_order')
            if '_Bond.Assembly_ID' not in out_tag:
                out_tag.append('_Bond.Assembly_ID')

        elif lp_category == '_Atom_chem_shift':
            if '_Atom_chem_shift.ID' not in out_tag:
                out_tag.insert(0, '_Atom_chem_shift.ID')
            if '_Atom_chem_shift.Ambiguity_code' not in out_tag:
                out_tag.insert(9, '_Atom_chem_shift.Ambiguity_code')
            if '_Atom_chem_shift.Ambiguity_set_ID' not in out_tag:
                out_tag.insert(10, '_Atom_chem_shift.Ambiguity_set_ID')

            if self.insert_original_pdb_cs_items:
                if '_Atom_chem_shift.Original_PDB_strand_ID' not in out_tag:
                    out_tag.append('_Atom_chem_shift.Original_PDB_strand_ID')
                if '_Atom_chem_shift.Original_PDB_residue_no' not in out_tag:
                    out_tag.append('_Atom_chem_shift.Original_PDB_residue_no')
                if '_Atom_chem_shift.Original_PDB_residue_name' not in out_tag:
                    out_tag.append('_Atom_chem_shift.Original_PDB_residue_name')
                if '_Atom_chem_shift.Original_PDB_atom_name' not in out_tag:
                    out_tag.append('_Atom_chem_shift.Original_PDB_atom_name')

            if '_Atom_chem_shift.Details' not in out_tag:
                out_tag.append('_Atom_chem_shift.Details')
            if '_Atom_chem_shift.Assigned_chem_shift_list_ID' not in out_tag:
                out_tag.append('_Atom_chem_shift.Assigned_chem_shift_list_ID')

        elif lp_category == '_Gen_dist_constraint.Member':
            if '_Gen_dist_constraint.Member_logic_code' not in out_tag:
                out_tag.append('_Gen_dist_constraint.Member_logic_code')
            if '_Gen_dist_constraint.Gen_dist_constraint_list_ID' not in out_tag:
                out_tag.append('_Gen_dist_constraint.Gen_dist_constraint_list_ID')

        elif lp_category == '_Torsion_angle_constraint':
            if '_Torsion_angle_constraint.Torsion_angle_constraint_list_ID' not in out_tag:
                out_tag.append('_Torsion_angle_constraint.Torsion_angle_constraint_list_ID')

        elif lp_category == '_RDC_constraint':
            if '_RDC_constraint.RDC_constraint_list_ID' not in out_tag:
                out_tag.append('_RDC_constraint.RDC_constraint_list_ID')

        elif lp_category == '_Peak_row_format':
            if '_Peak_row_format.Details' not in out_tag:
                out_tag.append('_Peak_row_format.Details')
            if '_Peak_row_format.Spectral_peak_list_ID' not in out_tag:
                out_tag.append('_Peak_row_format.Spectral_peak_list_ID')

        elif lp_category == '_Spectral_dim':
            if '_Spectral_dim.Spectral_peak_list_ID' not in out_tag:
                out_tag.append('_Spectral_dim.Spectral_peak_list_ID')

        elif lp_category == '_Spectral_dim_transfer':
            if '_Spectral_dim_transfer.Spectral_peak_list_ID' not in out_tag:
                out_tag.append('_Spectral_dim_transfer.Spectral_peak_list_ID')

        return out_tag

    def get_nef_loop_tags(self, star_loop_tags):
        """ Return list of NEF loop tags corresponding to NMR-STAR loop tags.
            @author: Masashi Yokochi
            @return: list of NEF loop tags corresponding to given NMR-STAR loop tags
        """

        out_tag_w_ordinal = {}
        out_tag = []

        for j in star_loop_tags:

            data_tag, ordinal = self.get_nef_tag(j)

            if data_tag is not None:
                out_tag_w_ordinal[data_tag] = ordinal

        out_tag = [t[0] for t in sorted(out_tag_w_ordinal.items(), key=lambda x:x[1])]

        if len(out_tag) > 0 and out_tag[0].startswith('_nef_sequence.') and '_nef_sequence.index' not in out_tag:
            out_tag.insert(0, '_nef_sequence.index')

        return out_tag

    def get_valid_star_atom_in_xplor(self, comp_id, atom_id, details=None, leave_unmatched=True):
        """ Return lists of atom ID, ambiguity_code, details in IUPAC atom nomenclature for a given atom name in XPLOR atom nomenclature.
            @author: Masashi Yokochi
            @return: list of instanced atom_id, ambiguity_code, and description
        """

        if comp_id in emptyValue:
            return [], None, None

        if '#' in atom_id:
            atom_id = atom_id.replace('#', '%')

        if atom_id[0] in ('H', 'Q', 'M'):

            if atom_id.endswith('1') and not self.validate_comp_atom(comp_id, atom_id):
                _atom_id = atom_id[:-1] + '3'
                if self.validate_comp_atom(comp_id, _atom_id):
                    return self.get_valid_star_atom(comp_id, _atom_id, details, leave_unmatched)

            if atom_id.endswith('1*') or atom_id.endswith('1%'):
                _atom_id = atom_id[:-2] + '3' + atom_id[-1]
                _atom_list, _ambiguity_code, _details = self.get_valid_star_atom(comp_id, _atom_id, None, True)
                if _details is None:
                    if leave_unmatched:
                        return _atom_list, _ambiguity_code, _details
                    return self.get_valid_star_atom(comp_id, _atom_id, details, leave_unmatched)

                _atom_list, _ambiguity_code, _details = self.get_valid_star_atom(comp_id, _atom_id[:-1], None, True)
                if _details is None:
                    if leave_unmatched:
                        return _atom_list, _ambiguity_code, _details
                    return self.get_valid_star_atom(comp_id, _atom_id, details, leave_unmatched)

        return self.get_valid_star_atom(comp_id, atom_id, details, leave_unmatched)

    def get_valid_star_atom(self, comp_id, atom_id, details=None, leave_unmatched=True):
        """ Return lists of atom ID, ambiguity_code, details in IUPAC atom nomenclature for a given conventional NMR atom name.
            @author: Masashi Yokochi
            @return: list of instanced atom_id, ambiguity_code, and description
        """

        if comp_id in emptyValue:
            return [], None, None

        if '#' in atom_id:
            atom_id = atom_id.replace('#', '%')

        if atom_id == 'HN' or atom_id.endswith('%') or atom_id.endswith('*'):
            return self.get_star_atom(comp_id, atom_id, details, leave_unmatched)

        if atom_id.startswith('QQ'):
            return self.get_star_atom(comp_id, 'H' + atom_id[2:] + '%', details, leave_unmatched)

        if atom_id.startswith('QR'):
            qr_atoms = sorted(set(atom_id[:-1] + '%' for atom_id in self.__csStat.getAromaticAtoms(comp_id)
                                  if atom_id[0] == 'H' and self.__csStat.getMaxAmbigCodeWoSetId(comp_id, atom_id) == 3))
            if len(qr_atoms) == 0:
                return [], None, None
            atom_list = []
            for qr_atom in qr_atoms:
                _atom_list, ambiguity_code, details = self.get_star_atom(comp_id, qr_atom, details, leave_unmatched)
                atom_list.extend(_atom_list)
            return atom_list, ambiguity_code, details

        if atom_id.startswith('Q') or atom_id.startswith('M'):
            return self.get_star_atom(comp_id, 'H' + atom_id[1:] + '%', details, leave_unmatched)

        if (atom_id + '2' in self.__csStat.getAllAtoms(comp_id)) or (atom_id + '22' in self.__csStat.getAllAtoms(comp_id)):
            return self.get_star_atom(comp_id, atom_id + '%', details, leave_unmatched)

        return self.get_star_atom(comp_id, atom_id, details, leave_unmatched)

    def get_star_atom(self, comp_id, nef_atom, details=None, leave_unmatched=True):
        """ Return list of instanced atom_id of a given NEF atom (including wildcard codes) and its ambiguity code.
            @change: support non-standard residue by Masashi Yokochi
            @change: rename the original get_nmrstar_atom() to get_star_atom() by Masashi Yokochi
            @return: list of instanced atom_id of a given NEF atom, ambiguity_code, and description
        """

        if comp_id in emptyValue:
            return [], None, None

        comp_id = comp_id.upper()
        is_std_comp_id = comp_id in monDict3

        atom_list = []
        ambiguity_code = 1
        atoms = []

        if self.__ccU.updateChemCompDict(comp_id):
            atoms = [a[self.__ccU.ccaAtomId] for a in self.__ccU.lastAtomList]

        else:

            if leave_unmatched:
                details = f"Unknown non-standard residue {comp_id} found."
            elif self.__verbose:
                self.__lfh.write(f"+NEFTranslator.get_star_atom() ++ Error  - Unknown non-standard residue {comp_id} found.\n")

        try:

            ref_atom = re.findall(r'(\S+)([xyXY])([%*])$|(\S+)([%*])$|(\S+)([xyXY]$)', nef_atom)[0]

            atm_set = [ref_atom.index(i) for i in ref_atom if i != '']

            pattern = None

            if atm_set == [0, 1, 2]:  # endswith [xyXY][%*]

                atom_type = ref_atom[0]
                xy_code = ref_atom[1].lower()

                len_atom_type = len(atom_type)

                pattern = re.compile(fr'{atom_type}\S\d+')

                alist2 = [i for i in atoms
                          if re.search(pattern, i) and i[len_atom_type].isdigit()]  # bmrb_id: 15879, pdb_id: 2k6r, comp_id: DNS

                xid = sorted(set(int(i[len_atom_type]) for i in alist2))

                if xy_code == 'x':
                    atom_list = [i for i in alist2 if int(i[len_atom_type]) == xid[0]]
                    if len(atom_list) > 3:  # bmrb_id: 15879, pdb_id: 2k6r, comp_id: DNS
                        atom_list[3:] = []

                else:
                    atom_list = [i for i in alist2 if int(i[len_atom_type]) == xid[1]]
                    if len(atom_list) > 3:  # bmrb_id: 15879, pdb_id: 2k6r, comp_id: DNS
                        atom_list[3:] = []

                ambiguity_code = self.__csStat.getMaxAmbigCodeWoSetId(comp_id, atom_list[0])

            elif atm_set == [3, 4]:  # endswith [%*] but neither [xyXY][%*]

                atom_type = ref_atom[3]
                wc_code = ref_atom[4]

                if wc_code == '%':
                    pattern = re.compile(fr'{atom_type}\d+') if is_std_comp_id else re.compile(fr'{atom_type}\S?$')
                elif wc_code == '*':
                    pattern = re.compile(fr'{atom_type}\S+')
                elif self.__verbose:
                    self.__lfh.write(f"+NEFTranslator.get_star_atom() ++ Error  - Invalid NEF atom nomenclature {nef_atom} found.\n")

                atom_list = [i for i in atoms if re.search(pattern, i)]

                methyl_atoms = self.__csStat.getMethylAtoms(comp_id)

                ambiguity_code = 1 if atom_list[0] in methyl_atoms else self.__csStat.getMaxAmbigCodeWoSetId(comp_id, atom_list[0])

            elif atm_set == [5, 6]:  # endswith [xyXY]

                atom_type = ref_atom[5]
                xy_code = ref_atom[6].lower()

                pattern = re.compile(fr'{atom_type}[^\']+')

                atom_list = [i for i in atoms if re.search(pattern, i)]

                atom_list_len = len(atom_list)

                if atom_list_len != 2:
                    if atom_list_len > 2:
                        atom_list = []
                elif xy_code == 'y':
                    atom_list = atom_list[-1:]
                elif xy_code == 'x':
                    atom_list = atom_list[:1]
                elif self.__verbose:
                    self.__lfh.write(f"+NEFTranslator.get_star_atom() ++ Error  - Invalid NEF atom nomenclature {nef_atom} found.\n")

                ambiguity_code = self.__csStat.getMaxAmbigCodeWoSetId(comp_id, atom_list[0])

            elif self.__verbose:
                self.__lfh.write(f"+NEFTranslator.get_star_atom() ++ Error  - Invalid NEF atom nomenclature {nef_atom} found.\n")

        except IndexError:
            pass

        if len(atom_list) == 0:

            if nef_atom == 'HN' and self.__csStat.peptideLike(comp_id):
                return self.get_star_atom(comp_id, 'H', 'HN converted to H.' if leave_unmatched else None, leave_unmatched)

            if self.__csStat.hasCompId(comp_id):

                methyl_atoms = self.__csStat.getMethylAtoms(comp_id)

                if is_std_comp_id and not nef_atom.endswith('%') and not nef_atom.endswith('*') and nef_atom + '1' in methyl_atoms:
                    return self.get_star_atom(comp_id, nef_atom + '%',
                                              f"{nef_atom} converted to {nef_atom}%." if leave_unmatched else None, leave_unmatched)

                if nef_atom[-1].lower() == 'x' or nef_atom[-1].lower() == 'y' and nef_atom[:-1] + '1' in methyl_atoms:
                    return self.get_star_atom(comp_id, nef_atom[:-1] + '%',
                                              f"{nef_atom} converted to {nef_atom[:-1]}%." if leave_unmatched else None, leave_unmatched)

                if ((is_std_comp_id and nef_atom[-1] == '%') or nef_atom[-1] == '*') and (nef_atom[:-1] + '1' not in methyl_atoms) and\
                   len(nef_atom) > 2 and (nef_atom[-2].lower() == 'x' or nef_atom[-2].lower() == 'y'):
                    return self.get_star_atom(comp_id, nef_atom[:-2] + ('1' if nef_atom[-2].lower() == 'x' else '2') + '%',
                                              f"{nef_atom} converted to {nef_atom[:-2] + ('1' if nef_atom[-2].lower() == 'x' else '2')}%." if leave_unmatched else None,
                                              leave_unmatched)

            if nef_atom in atoms:
                atom_list.append(nef_atom)

            elif leave_unmatched:
                atom_list.append(nef_atom)
                ambiguity_code = None
                if details is None:
                    details = f"{nef_atom} is invalid atom_id in comp_id {comp_id}."

        return atom_list, ambiguity_code, details

    def get_nef_atom(self, comp_id, star_atom_list, details=None, leave_unmatched=True):
        """ Return list of all instanced atom_id of given NMR-STAR atoms with ambiguity code and CS value in a given comp_id.
            @author: Masashi Yokochi
            @return: list of instanced atom_id of given NMR-STAR atoms, descriptions, and atom conversion dictionary for conversion of other loops
        """

        if comp_id in emptyValue:
            return [], None, None

        comp_id = comp_id.upper()

        atom_list = []
        atom_id_map = {}
        atoms = []

        if self.__ccU.updateChemCompDict(comp_id):
            atoms = [a[self.__ccU.ccaAtomId] for a in self.__ccU.lastAtomList]

        methyl_atoms = self.__csStat.getMethylAtoms(comp_id)

        proc_atom_list = set()

        if details is None:
            details = {}

        try:

            for a in star_atom_list:

                atom_id = a['atom_id']
                _ambig_code = a['ambig_code']
                _value = a['value']

                if atom_id in proc_atom_list:
                    continue

                if atom_id not in atoms:

                    _atom_id = None

                    if atom_id == 'HN' and self.__csStat.peptideLike(comp_id):
                        _atom_id = 'H'
                    elif atom_id.startswith('QQ'):
                        _atom_id = 'H' + atom_id[2:] + '%'
                    elif atom_id.startswith('QR'):
                        qr_atoms = sorted(set(atom_id[:-1] + '%' for atom_id in self.__csStat.getAromaticAtoms(comp_id)
                                              if atom_id[0] == 'H' and self.__csStat.getMaxAmbigCodeWoSetId(comp_id, atom_id) == 3))
                        if len(qr_atoms) > 0:
                            for qr_atom in qr_atoms:
                                _a = copy.copy(a)
                                _a['atom_id'] = qr_atom
                                star_atom_list.append(_a)
                            star_atom_list.remove(a)
                            return self.get_nef_atom(comp_id, star_atom_list, details, leave_unmatched)
                    elif atom_id.startswith('Q') or atom_id.startswith('M'):
                        _atom_id = 'H' + atom_id[1:] + '%'
                    elif atom_id + '2' in self.__csStat.getAllAtoms(comp_id):
                        _atom_id = atom_id + '%'

                    if _atom_id is None:

                        if leave_unmatched:
                            atom_list.append(atom_id)
                            if not self.__ccU.lastStatus:
                                details[atom_id] = f"Unknown non-standard residue {comp_id} found."
                            else:
                                details[atom_id] = f"{atom_id} is invalid atom_id in comp_id {comp_id}."
                            atom_id_map[atom_id] = atom_id
                        elif self.__verbose:
                            if not self.__ccU.lastStatus:
                                self.__lfh.write(f"+NEFTranslator.get_nef_atom() ++ Error  - Unknown non-standard residue {comp_id} found.\n")
                            else:
                                self.__lfh.write(f"+NEFTranslator.get_nef_atom() ++ Error  - Invalid atom nomenclature {atom_id} found.\n")

                        continue

                    atom_id = _atom_id

                if _ambig_code in emptyValue:
                    ambig_code = self.__csStat.getMaxAmbigCodeWoSetId(comp_id, atom_id)
                    if atom_id.endswith("'"):
                        ambig_code = 1
                else:
                    ambig_code = int(_ambig_code)

                if ambig_code not in ALLOWED_AMBIGUITY_CODES:

                    if leave_unmatched:
                        atom_list.append(atom_id)
                        details[atom_id] = f"{atom_id} has invalid ambiguity code {ambig_code}."
                        atom_id_map[atom_id] = atom_id
                    elif self.__verbose:
                        self.__lfh.write(f"+NEFTranslator.get_nef_atom() ++ Error  - Invalid ambiguity code {ambig_code} for atom_id {atom_id} found.\n")

                    continue

                if ambig_code == 1:

                    if atom_id[0] == 'H' and atom_id in methyl_atoms:

                        methyl_c, methyl_h_list = self.get_group(comp_id, atom_id)

                        if methyl_h_list is None:

                            if leave_unmatched:
                                atom_list.append(atom_id)
                                details[atom_id] = f"{atom_id} is invalid atom_id in comp_id {comp_id}."
                                atom_id_map[atom_id] = atom_id
                            elif self.__verbose:
                                self.__lfh.write(f"+NEFTranslator.get_nef_atom() ++ Error  - Invalid atom nomenclature {atom_id} found.\n")

                        else:

                            has_methyl_proton = len([_a['atom_id'] for _a in star_atom_list
                                                     if _a['atom_id'] in methyl_h_list and (_a['value'] is None or _a['value'] == _value)]) == 3

                            if has_methyl_proton:

                                name_len = [len(n) for n in methyl_h_list]
                                max_len = max(name_len)
                                min_len = min(name_len)

                                if max_len == min_len or len(atom_id) == max_len:
                                    nef_atom = atom_id[:-1] + '%'
                                else:  # For example, HEM HM[A-D]
                                    nef_atom = atom_id + '%'

                                atom_list.append(nef_atom)
                                details[nef_atom] = None
                                for b in methyl_h_list:
                                    atom_id_map[b] = nef_atom
                                    proc_atom_list.add(b)

                            else:
                                atom_list.append(atom_id)
                                details[atom_id] = None
                                atom_id_map[atom_id] = atom_id

                    else:
                        atom_list.append(atom_id)
                        details[atom_id] = None
                        atom_id_map[atom_id] = atom_id

                elif ambig_code == 2:

                    if self.__csStat.getMaxAmbigCodeWoSetId(comp_id, atom_id) != 2:

                        if leave_unmatched:
                            atom_list.append(atom_id)
                            details[atom_id] = f"{atom_id} has invalid ambiguity code {ambig_code}."
                            atom_id_map[atom_id] = atom_id
                        elif self.__verbose:
                            self.__lfh.write(f"+NEFTranslator.get_nef_atom() ++ Error  - Invalid ambiguity code {ambig_code} for atom_id {atom_id} found.\n")

                    elif atom_id[0] == 'H':

                        if atom_id in methyl_atoms:

                            methyl_c, methyl_h_list = self.get_group(comp_id, atom_id)
                            _, methyl_h_list_2 = self.get_geminal_group(comp_id, methyl_c)

                            if methyl_h_list is None:

                                if leave_unmatched:
                                    atom_list.append(atom_id)
                                    details[atom_id] = f"{atom_id} is invalid atom_id in comp_id {comp_id}."
                                    atom_id_map[atom_id] = atom_id
                                elif self.__verbose:
                                    self.__lfh.write(f"+NEFTranslator.get_nef_atom() ++ Error  - Invalid atom nomenclature {atom_id} found.\n")

                            else:

                                has_methyl_proton = len([_a['atom_id'] for _a in star_atom_list
                                                         if _a['atom_id'] in methyl_h_list and (_a['value'] is None or _a['value'] == _value)]) == 3
                                has_methyl_proton_2 = methyl_h_list_2 is not None and len([_a['atom_id'] for _a in star_atom_list
                                                                                           if _a['atom_id'] in methyl_h_list_2
                                                                                           and (_a['value'] is None or _a['value'] == _value)]) == 3

                                nef_atom_prefix = 'x'
                                nef_atom_prefix_2 = 'y'

                                if has_methyl_proton and has_methyl_proton_2:

                                    methyl_proton_value = next((_a['value'] for _a in star_atom_list if _a['atom_id'] in methyl_h_list), None)
                                    methyl_proton_value_2 = next((_a['value'] for _a in star_atom_list if _a['atom_id'] in methyl_h_list_2), None)

                                    if methyl_proton_value is not None and methyl_proton_value_2 is not None\
                                       and float(methyl_proton_value_2) < float(methyl_proton_value):
                                        nef_atom_prefix = 'y'
                                        nef_atom_prefix_2 = 'x'

                                    nef_atom = methyl_h_list[0][:-2] + nef_atom_prefix + '%'

                                    atom_list.append(nef_atom)
                                    details[nef_atom] = None
                                    for b in methyl_h_list:
                                        atom_id_map[b] = nef_atom
                                        proc_atom_list.add(b)

                                    nef_atom_2 = methyl_h_list_2[0][:-2] + nef_atom_prefix_2 + '%'

                                    atom_list.append(nef_atom_2)
                                    details[nef_atom_2] = None
                                    for b in methyl_h_list_2:
                                        atom_id_map[b] = nef_atom_2
                                        proc_atom_list.add(b)

                                elif has_methyl_proton:

                                    nef_atom_prefix = 'x' if methyl_h_list[0] < methyl_h_list_2[0] else 'y'
                                    nef_atom = methyl_h_list[0][:-2] + nef_atom_prefix + '%'

                                    atom_list.append(nef_atom)
                                    details[nef_atom] = None
                                    for b in methyl_h_list:
                                        atom_id_map[b] = nef_atom
                                        proc_atom_list.add(b)

                                else:
                                    atom_list.append(atom_id)
                                    details[atom_id] = None
                                    atom_id_map[atom_id] = atom_id

                        else:

                            _, geminal_h_list = self.get_group(comp_id, atom_id)

                            if geminal_h_list is None:

                                if leave_unmatched:
                                    atom_list.append(atom_id)
                                    details[atom_id] = f"{atom_id} is invalid atom_id in comp_id {comp_id}."
                                    atom_id_map[atom_id] = atom_id
                                elif self.__verbose:
                                    self.__lfh.write(f"+NEFTranslator.get_nef_atom() ++ Error  - Invalid atom nomenclature {atom_id} found.\n")

                            else:

                                has_geminal_proton = len([_a['atom_id'] for _a in star_atom_list if _a['atom_id'] in geminal_h_list]) == 2

                                nef_atom_prefix = 'x'
                                nef_atom_prefix_2 = 'y'

                                if atom_id.endswith("'"):

                                    atom_list.append(atom_id)
                                    details[atom_id] = None
                                    atom_id_map[atom_id] = atom_id

                                elif has_geminal_proton:

                                    geminal_proton_value = next((_a['value'] for _a in star_atom_list if _a['atom_id'] == geminal_h_list[0]), None)
                                    geminal_proton_value_2 = next((_a['value'] for _a in star_atom_list if _a['atom_id'] == geminal_h_list[1]), None)

                                    if geminal_proton_value is not None and geminal_proton_value_2 is not None\
                                       and float(geminal_proton_value_2) < float(geminal_proton_value):
                                        nef_atom_prefix = 'y'
                                        nef_atom_prefix_2 = 'x'

                                    nef_atom = geminal_h_list[0][:-1] + nef_atom_prefix

                                    atom_list.append(nef_atom)
                                    details[nef_atom] = None
                                    atom_id_map[geminal_h_list[0]] = nef_atom

                                    nef_atom_2 = geminal_h_list[1][:-1] + nef_atom_prefix_2

                                    atom_list.append(nef_atom_2)
                                    details[nef_atom_2] = None
                                    atom_id_map[geminal_h_list[1]] = nef_atom_2

                                    for b in geminal_h_list:
                                        proc_atom_list.add(b)

                                else:

                                    nef_atom_prefix = 'x' if (atom_id == geminal_h_list[0] and geminal_h_list[0] < geminal_h_list[1]) or\
                                                             (atom_id == geminal_h_list[1] and geminal_h_list[1] < geminal_h_list[0]) else 'y'
                                    nef_atom = atom_id[:-1] + nef_atom_prefix

                                    atom_list.append(nef_atom)
                                    details[nef_atom] = None
                                    atom_id_map[atom_id] = nef_atom

                    else:

                        atom_id_2, _ = self.get_geminal_group(comp_id, atom_id)

                        if atom_id_2 is None:

                            if leave_unmatched:
                                atom_list.append(atom_id)
                                details[atom_id] = f"{atom_id} is invalid atom_id in comp_id {comp_id}."
                                atom_id_map[atom_id] = atom_id
                            elif self.__verbose:
                                self.__lfh.write(f"+NEFTranslator.get_nef_atom() ++ Error  - Invalid atom nomenclature {atom_id} found.\n")

                        else:

                            has_atom_id_2 = len([_a['atom_id'] for _a in star_atom_list if _a['atom_id'] == atom_id_2]) == 1

                            nef_atom_prefix = 'x'
                            nef_atom_prefix_2 = 'y'

                            if has_atom_id_2:

                                atom_id_value = next((_a['value'] for _a in star_atom_list if _a['atom_id'] == atom_id), None)
                                atom_id_value_2 = next((_a['value'] for _a in star_atom_list if _a['atom_id'] == atom_id_2), None)

                                if atom_id_value is not None and atom_id_value_2 is not None\
                                   and float(atom_id_value_2) < float(atom_id_value):
                                    nef_atom_prefix = 'y'
                                    nef_atom_prefix_2 = 'x'

                                nef_atom = atom_id[:-1] + nef_atom_prefix

                                atom_list.append(nef_atom)
                                details[nef_atom] = None
                                atom_id_map[atom_id] = nef_atom
                                proc_atom_list.add(atom_id)

                                nef_atom_2 = atom_id_2[:-1] + nef_atom_prefix_2

                                atom_list.append(nef_atom_2)
                                details[nef_atom_2] = None
                                atom_id_map[atom_id_2] = nef_atom_2
                                proc_atom_list.add(atom_id_2)

                            else:

                                nef_atom_prefix = 'x' if atom_id < atom_id_2 else 'y'
                                nef_atom = atom_id[:-1] + nef_atom_prefix

                                atom_list.append(nef_atom)
                                details[nef_atom] = None
                                atom_id_map[atom_id] = nef_atom

                elif ambig_code == 3:

                    if self.__csStat.getMaxAmbigCodeWoSetId(comp_id, atom_id) != 3:

                        if leave_unmatched:
                            atom_list.append(atom_id)
                            details[atom_id] = f"{atom_id} has invalid ambiguity code {ambig_code}."
                            atom_id_map[atom_id] = atom_id
                        elif self.__verbose:
                            self.__lfh.write(f"+NEFTranslator.get_nef_atom() ++ Error  - Invalid ambiguity code {ambig_code} for atom_id {atom_id} found.\n")

                    else:

                        atom_id_2 = self.__csStat.getGeminalAtom(comp_id, atom_id)

                        if atom_id_2 is None:

                            if leave_unmatched:
                                atom_list.append(atom_id)
                                details[atom_id] = f"{atom_id} is invalid atom_id in comp_id {comp_id}."
                                atom_id_map[atom_id] = atom_id
                            elif self.__verbose:
                                self.__lfh.write(f"+NEFTranslator.get_nef_atom() ++ Error  - Invalid atom nomenclature {atom_id} found.\n")

                        else:

                            has_atom_id_2 = len([_a['atom_id'] for _a in star_atom_list if _a['atom_id'] == atom_id_2]) == 1

                            nef_atom_prefix = 'x'
                            nef_atom_prefix_2 = 'y'

                            if has_atom_id_2:

                                atom_id_value = next((_a['value'] for _a in star_atom_list if _a['atom_id'] == atom_id), None)
                                atom_id_value_2 = next((_a['value'] for _a in star_atom_list if _a['atom_id'] == atom_id_2), None)

                                if atom_id_value is not None and atom_id_value_2 is not None\
                                   and float(atom_id_value_2) < float(atom_id_value):
                                    nef_atom_prefix = 'y'
                                    nef_atom_prefix_2 = 'x'

                                nef_atom = atom_id[:-1] + nef_atom_prefix

                                atom_list.append(nef_atom)
                                details[nef_atom] = None
                                atom_id_map[atom_id] = nef_atom
                                proc_atom_list.add(atom_id)

                                nef_atom_2 = atom_id_2[:-1] + nef_atom_prefix_2

                                atom_list.append(nef_atom_2)
                                details[nef_atom_2] = None
                                atom_id_map[atom_id_2] = nef_atom_2
                                proc_atom_list.add(atom_id_2)

                            else:

                                nef_atom_prefix = 'x' if atom_id < atom_id_2 else 'y'
                                nef_atom = atom_id[:-1] + nef_atom_prefix

                                atom_list.append(nef_atom)
                                details[nef_atom] = None
                                atom_id_map[atom_id] = nef_atom

                else:

                    atom_list.append(atom_id)
                    details[atom_id] = None
                    atom_id_map[atom_id] = atom_id

                proc_atom_list.add(atom_id)

        except KeyError:
            pass

        return atom_list, details, atom_id_map

    def get_group(self, comp_id, atom_id):
        """ Return heavy atom name and list of proton names bonded to the heavy atom.
            @author: Masashi Yokochi
            @return: heavy atom name and list of proton names
        """

        if comp_id in emptyValue:
            return None, None

        if atom_id is None or atom_id[0] not in ('H', 'C', 'N', 'O'):
            return None, None

        if not self.__ccU.updateChemCompDict(comp_id):
            return None, None

        try:

            ccb = next(b for b in self.__ccU.lastBonds
                       if (b[self.__ccU.ccbAtomId1] == atom_id and (atom_id[0] == 'H' or b[self.__ccU.ccbAtomId2][0] == 'H'))
                       or (b[self.__ccU.ccbAtomId2] == atom_id and (atom_id[0] == 'H' or b[self.__ccU.ccbAtomId1][0] == 'H')))

            hvy_col = self.__ccU.ccbAtomId1 if ccb[self.__ccU.ccbAtomId2 if atom_id[0] == 'H' else self.__ccU.ccbAtomId1] == atom_id else self.__ccU.ccbAtomId2
            pro_col = self.__ccU.ccbAtomId2 if self.__ccU.ccbAtomId1 == hvy_col else self.__ccU.ccbAtomId1

            hvy = ccb[hvy_col]

            return hvy, [b[pro_col] for b in self.__ccU.lastBonds if b[hvy_col] == hvy and b[pro_col][0] == 'H']

        except StopIteration:
            return None, None

    def get_geminal_group(self, comp_id, atom_id):
        """ Return geminal heavy atom and list of proton names bonded to the geminal heavy atom.
            @author: Masashi Yokochi
            @return: geminal heavy atom name and list of geminal proton names
        """

        if comp_id in emptyValue:
            return None, None

        if atom_id is None or atom_id[0] not in ('H', 'C', 'N', 'O'):
            return None, None

        if not self.__ccU.updateChemCompDict(comp_id):
            return None, None

        atom_id, h_list = self.get_group(comp_id, atom_id)

        if atom_id is None:
            return None, None

        h_list_len = len(h_list)

        try:

            ccb = next(b for b in self.__ccU.lastBonds
                       if (b[self.__ccU.ccbAtomId2] == atom_id and b[self.__ccU.ccbAtomId1][0] != 'H')
                       or (b[self.__ccU.ccbAtomId1] == atom_id and b[self.__ccU.ccbAtomId2][0] != 'H'))

            hvy_conn = ccb[self.__ccU.ccbAtomId1 if ccb[self.__ccU.ccbAtomId2] == atom_id else self.__ccU.ccbAtomId2]

            hvy_2 = next(c[self.__ccU.ccbAtomId1 if c[self.__ccU.ccbAtomId2] == hvy_conn else self.__ccU.ccbAtomId2]
                         for c in self.__ccU.lastBonds
                         if (c[self.__ccU.ccbAtomId2] == hvy_conn and c[self.__ccU.ccbAtomId1] != atom_id and c[self.__ccU.ccbAtomId1][0] != 'H'
                             and self.get_group(comp_id, c[self.__ccU.ccbAtomId1])[1] is not None
                             and len(self.get_group(comp_id, c[self.__ccU.ccbAtomId1])[1]) == h_list_len)
                         or (c[self.__ccU.ccbAtomId1] == hvy_conn and c[self.__ccU.ccbAtomId2] != atom_id and c[self.__ccU.ccbAtomId2][0] != 'H'
                             and self.get_group(comp_id, c[self.__ccU.ccbAtomId2])[1] is not None
                             and len(self.get_group(comp_id, c[self.__ccU.ccbAtomId2])[1]) == h_list_len))

            return self.get_group(comp_id, hvy_2)

        except StopIteration:
            return None, None

    def nef2star_seq_row(self, nef_tags, star_tags, loop_data, report=None):
        """ Translate rows in sequence loop from NEF into NMR-STAR.
            @change: rename the original translate_seq_row() to nef2star_seq_row() by Masashi Yokochi
            @param nef_tags: list of NEF tags
            @param star_tags: list of NMR-STAR tags
            @param loop_data: loop data of NEF
            @param report: NMR data processing report
            @return: rows of NMR-STAR, rows of _Entity_deleted_atom loop (residue variants), otherwise None
        """

        out_row = []
        aux_row = []

        chain_index = nef_tags.index('_nef_sequence.chain_code')
        seq_index = nef_tags.index('_nef_sequence.sequence_code')
        comp_index = nef_tags.index('_nef_sequence.residue_name')

        for _star_chain, nef_chain in enumerate(self.authChainId, start=1):

            seq_list = sorted(set(int(i[seq_index]) for i in loop_data if i[chain_index] == nef_chain))

            if len(seq_list) == 0:
                continue

            cif_chain = cif_ps = None
            if report is not None:
                seq_align = report.getSequenceAlignmentWithNmrChainId(nef_chain)
                if seq_align is not None:
                    cif_chain = seq_align['test_chain_id']  # label_asym_id
                    _star_chain = str(letterToDigit(cif_chain))
                    cif_ps = report.getModelPolymerSequenceOf(cif_chain, label_scheme=False)
                    if cif_ps is not None:
                        cif_chain = cif_ps['auth_chain_id']  # auth_asym_id
                    if self.__remediation_mode:
                        _star_chain = cif_chain

            offset = None

            for _nef_seq in seq_list:

                _cif_seq = None
                if cif_chain is not None:
                    try:
                        _cif_seq = seq_align['test_seq_id'][seq_align['ref_seq_id'].index(_nef_seq)]  # label_seq_id
                        if offset is None:
                            offset = _cif_seq - _nef_seq
                        if cif_ps is not None:
                            _cif_seq = cif_ps['auth_seq_id'][cif_ps['seq_id'].index(_cif_seq)]  # auth_seq_id
                    except:  # noqa: E722 pylint: disable=bare-except
                        pass

                nef_seq = str(_nef_seq)

                if offset is None:
                    offset = 1 - _nef_seq

                _star_seq = _nef_seq + offset

                i = next(i for i in loop_data if i[chain_index] == nef_chain and i[seq_index] == nef_seq)

                out = [None] * len(star_tags)

                variant = None

                for j in nef_tags:

                    auth_tag, data_tag, _ = self.get_star_tag(j)

                    if auth_tag is None:
                        continue

                    data = i[nef_tags.index(j)]

                    if j == '_nef_sequence.chain_code':
                        if cif_chain is None:
                            out[star_tags.index(auth_tag)] = data
                        else:
                            out[star_tags.index(auth_tag)] = cif_chain
                    elif j == '_nef_sequence.sequence_code':
                        if _cif_seq is None:
                            out[star_tags.index(auth_tag)] = data
                        else:
                            out[star_tags.index(auth_tag)] = str(_cif_seq)
                    else:
                        out[star_tags.index(auth_tag)] = data
                        if j == '_nef_sequence.residue_variant' and data not in emptyValue and '-' in data:
                            variant = data

                    if auth_tag != data_tag:

                        data_index = star_tags.index(data_tag)

                        if j == '_nef_sequence.chain_code':
                            out[data_index] = _star_chain
                        elif j == '_nef_sequence.sequence_code':
                            out[data_index] = _star_seq
                        elif data in NEF_BOOLEAN_VALUES:
                            out[data_index] = 'yes' if data in trueValue else 'no'
                        else:
                            out[data_index] = data

                out_row.append(out)

                self.authSeqMap[(nef_chain, _nef_seq)] = (_star_chain, _star_seq)
                self.selfSeqMap[(nef_chain, _nef_seq)] = (nef_chain if cif_chain is None else cif_chain,
                                                          _nef_seq if _cif_seq is None else _cif_seq)

                if variant is not None:
                    aux = [None] * len(ENTITY_DELETED_ATOM_ITEMS)
                    for l, aux_tag in enumerate(ENTITY_DELETED_ATOM_ITEMS):  # noqa: E741
                        if aux_tag == 'Entity_assembly_ID':
                            aux[l] = _star_chain
                        elif aux_tag == 'Comp_index_ID':
                            aux[l] = _star_seq
                        elif aux_tag == 'Auth_entity_assembly_ID':
                            aux[l] = nef_chain
                        elif aux_tag == 'Auth_seq_ID':
                            aux[l] = _nef_seq
                        elif aux_tag in ('Comp_ID', 'Auth_comp_ID'):
                            aux[l] = i[comp_index]

                    for _variant in variant.split(','):
                        _variant_ = _variant.strip(' ')
                        if _variant_.startswith('-'):
                            atom_list = self.get_star_atom(i[comp_index], _variant_[1:])[0]
                            if len(atom_list) > 0:
                                for atom in atom_list:
                                    _aux = copy.copy(aux)
                                    for l, aux_tag in enumerate(ENTITY_DELETED_ATOM_ITEMS):  # noqa: E741
                                        if aux_tag == 'ID':
                                            _aux[l] = len(aux_row) + 1
                                        elif aux_tag == 'Atom_ID':
                                            _aux[l] = atom
                                        elif aux_tag == 'Auth_variant_ID':
                                            _aux[l] = _variant_[1:]

                                    aux_row.append(_aux)

        return out_row, aux_row

    def star2nef_seq_row(self, star_tags, nef_tags, loop_data, report=None, entity_del_atom_loop=None):
        """ Translate rows in sequence loop from NMR-STAR into NEF.
            @author: Masashi Yokochi
            @param star_tags: list of NMR-STAR tags
            @param nef_tags: list of NEF tags
            @param loop_data: loop data of NMR-STAR
            @param report: NMR data processing report
            @return: rows of NEF
        """

        out_row = []

        has_nef_index = '_Chem_comp_assembly.NEF_index' in star_tags

        chain_index = star_tags.index('_Chem_comp_assembly.Entity_assembly_ID')
        seq_index = star_tags.index('_Chem_comp_assembly.Comp_index_ID')
        comp_index = star_tags.index('_Chem_comp_assembly.Comp_ID')

        if entity_del_atom_loop is not None:
            aux_tags = entity_del_atom_loop.get_tag_names()
            aux_chain_index = aux_tags.index('_Entity_deleted_atom.Entity_assembly_ID')
            aux_seq_index = aux_tags.index('_Entity_deleted_atom.Comp_index_ID')
            aux_atom_index = aux_tags.index('_Entity_deleted_atom.Atom_ID')

        self.star2NefChainMapping = {}
        self.star2CifChainMapping = {}

        auth_scheme = {}

        seq_list = {}

        for cid, star_chain in enumerate(self.authChainId):

            seq_list[star_chain] = sorted(set(int(i[seq_index]) for i in loop_data if i[chain_index] == star_chain))

            if len(seq_list[star_chain]) == 0:
                continue

            nef_chain = indexToLetter(cid)

            self.star2NefChainMapping[star_chain] = nef_chain

        if report is not None:

            for star_chain in self.authChainId:

                if len(seq_list[star_chain]) == 0:
                    continue

                cif_chain = cif_ps = None
                if report is not None:
                    seq_align = report.getSequenceAlignmentWithNmrChainId(star_chain)
                    if seq_align is not None:
                        cif_chain = seq_align['test_chain_id']  # label_asym_id
                        cif_ps = report.getModelPolymerSequenceOf(cif_chain, label_scheme=False)
                        if cif_ps is not None:
                            cif_chain = cif_ps['auth_chain_id']  # auth_asym_id

                self.star2CifChainMapping[star_chain] = cif_chain

                auth_scheme[star_chain] = cif_ps is not None

            for k, v in self.star2NefChainMapping.items():
                if self.star2CifChainMapping[k] is None:
                    for _k_ in [_k for _k, _v in self.star2NefChainMapping.items() if _v != v]:
                        if self.star2NefChainMapping[_k_] not in self.star2CifChainMapping.values():
                            self.star2CifChainMapping[k] = self.star2NefChainMapping[_k_]
                            break

            for k, v in self.star2NefChainMapping.items():
                if self.star2CifChainMapping[k] is None:
                    self.star2CifChainMapping[k] = v

        index = 1

        for star_chain in self.authChainId:

            _star_chain = int(star_chain)

            if len(seq_list[star_chain]) == 0:
                continue

            nef_chain = self.star2NefChainMapping[star_chain]

            cif_chain = cif_ps = None
            if report is not None:
                cif_chain = self.star2CifChainMapping[star_chain]
                seq_align = report.getSequenceAlignmentWithNmrChainId(star_chain)
                if star_chain in auth_scheme and auth_scheme[star_chain]:
                    cif_ps = report.getModelPolymerSequenceOf(cif_chain, label_scheme=False)

            offset = None

            for _star_seq in seq_list[star_chain]:

                _cif_seq = None
                if cif_chain is not None:
                    try:
                        _cif_seq = seq_align['test_seq_id'][seq_align['ref_seq_id'].index(_star_seq)]  # label_seq_id
                        if offset is None:
                            offset = _cif_seq - _star_seq
                        if cif_ps is not None:
                            _cif_seq = cif_ps['auth_seq_id'][cif_ps['seq_id'].index(_cif_seq)]  # auth_seq_id
                    except:  # noqa: E722 pylint: disable=bare-except
                        pass

                star_seq = str(_star_seq)

                if offset is None:
                    offset = 1 - _star_seq

                _nef_seq = (_star_seq + offset) if _cif_seq is None else _cif_seq

                i = next(i for i in loop_data if i[chain_index] == star_chain and i[seq_index] == star_seq)

                out = [None] * len(nef_tags)

                if not has_nef_index:
                    out[0] = index

                for j in star_tags:

                    nef_tag, _ = self.get_nef_tag(j)

                    if nef_tag is None:
                        continue

                    data = i[star_tags.index(j)]

                    data_index = nef_tags.index(nef_tag)

                    if nef_tag == '_nef_sequence.chain_code':
                        if cif_chain is None:
                            out[data_index] = nef_chain
                        else:
                            out[data_index] = cif_chain
                    elif nef_tag == '_nef_sequence.sequence_code':
                        if _cif_seq is None:
                            out[data_index] = _nef_seq
                        else:
                            out[data_index] = _cif_seq
                    elif data in STAR_BOOLEAN_VALUES:
                        out[data_index] = 'true' if data in trueValue else 'false'
                    elif nef_tag == '_nef_sequence.residue_variant':
                        if data not in emptyValue or entity_del_atom_loop is None:
                            out[data_index] = data
                        else:
                            star_atom_list = [{'atom_id': k[aux_atom_index], 'ambig_code': None, 'value': None} for k in entity_del_atom_loop
                                              if k[aux_chain_index] == star_chain and k[aux_seq_index] == star_seq]
                            if len(star_atom_list) == 0:
                                out[data_index] = data
                            else:
                                atom_list = self.get_nef_atom(i[comp_index], star_atom_list)[0]
                                if len(atom_list) == 0:
                                    out[data_index] = data
                                else:
                                    _atom_list = ['-' + a for a in atom_list]
                                    out[data_index] = ','.join(_atom_list)

                    else:
                        out[data_index] = data

                index += 1

                out_row.append(out)

                self.authSeqMap[(_star_chain, _star_seq)] = (nef_chain, _nef_seq)
                self.selfSeqMap[(_star_chain, _star_seq)] = (_star_chain if cif_chain is None else cif_chain,
                                                             _star_seq if _cif_seq is None else _cif_seq)

        return out_row

    def star2star_seq_row(self, in_star_tags, star_tags, loop_data, report=None):
        """ Translate rows in sequence loop from PyNMRSTAR data object into NMR-STAR.
            @author: Masashi Yokochi
            @param in_star_tags: list of input NMR-STAR tags
            @param star_tags: list of NMR-STAR tags
            @param loop_data: loop data of input NMR-STAR
            @param report: NMR data processing report
            @return: rows of NMR-STAR, rows of _Entity_deleted_atom loop (residue variants), otherwise None
        """

        out_row = []
        aux_row = []

        chain_index = in_star_tags.index('_Chem_comp_assembly.Entity_assembly_ID')
        seq_index = in_star_tags.index('_Chem_comp_assembly.Comp_index_ID')
        comp_index = in_star_tags.index('_Chem_comp_assembly.Comp_ID')

        for _star_chain, in_star_chain in enumerate(self.authChainId, start=1):

            seq_list = sorted(set(int(i[seq_index]) for i in loop_data if i[chain_index] == in_star_chain))

            if len(seq_list) == 0:
                continue

            cif_chain = cif_ps = None
            if report is not None:
                seq_align = report.getSequenceAlignmentWithNmrChainId(in_star_chain)
                if seq_align is not None:
                    cif_chain = seq_align['test_chain_id']  # label_asym_id
                    _star_chain = str(letterToDigit(cif_chain))
                    cif_ps = report.getModelPolymerSequenceOf(cif_chain, label_scheme=False)
                    if cif_ps is not None:
                        cif_chain = cif_ps['auth_chain_id']  # auth_asym_id
                    if self.__remediation_mode:
                        _star_chain = cif_chain

            offset = None

            for _in_star_seq in seq_list:

                _cif_seq = None
                if cif_chain is not None:
                    try:
                        _cif_seq = seq_align['test_seq_id'][seq_align['ref_seq_id'].index(_in_star_seq)]  # label_seq_id
                        if offset is None:
                            offset = _cif_seq - _in_star_seq
                        if cif_ps is not None:
                            _cif_seq = cif_ps['auth_seq_id'][cif_ps['seq_id'].index(_cif_seq)]  # auth_seq_id
                    except:  # noqa: E722 pylint: disable=bare-except
                        pass

                in_star_seq = str(_in_star_seq)

                if offset is None:
                    offset = 1 - _in_star_seq

                _star_seq = _in_star_seq + offset

                i = next(i for i in loop_data if i[chain_index] == in_star_chain and i[seq_index] == in_star_seq)

                out = [None] * len(star_tags)

                variant = None

                for data_tag in in_star_tags:

                    auth_tag, _ = self.get_star_auth_tag(data_tag)

                    if auth_tag is None:
                        continue

                    data = i[in_star_tags.index(data_tag)]

                    if data_tag == '_Chem_comp_assembly.Entity_assembly_ID':
                        if cif_chain is None:
                            out[star_tags.index(auth_tag)] = data
                        else:
                            out[star_tags.index(auth_tag)] = cif_chain
                    elif data_tag == '_Chem_comp_assembly.Comp_index_ID':
                        if _cif_seq is None:
                            out[star_tags.index(auth_tag)] = data
                        else:
                            out[star_tags.index(auth_tag)] = str(_cif_seq)
                    else:
                        out[star_tags.index(auth_tag)] = data
                        if data_tag == '_Chem_comp_assembly.Auth_variant_ID' and data not in emptyValue and '-' in data:
                            variant = data

                    if auth_tag != data_tag:

                        data_index = star_tags.index(data_tag)

                        if data_tag == '_Chem_comp_assembly.Entity_assembly_ID':
                            out[data_index] = _star_chain
                        elif data_tag == '_Chem_comp_assembly.Comp_index_ID':
                            out[data_index] = _star_seq
                        elif data_tag == '_Chem_comp_assembly.Comp_ID':
                            out[data_index] = data.upper()
                        else:
                            out[data_index] = data

                out_row.append(out)
                #
                # self.authSeqMap[(in_star_chain, _in_star_seq)] = (_star_chain, _star_seq)
                # self.selfSeqMap[(in_star_chain, _in_star_seq)] = (in_star_chain if cif_chain is None else cif_chain,
                #                                                   _in_star_seq if _cif_seq is None else _cif_seq)
                #
                if variant is not None:
                    aux = [None] * len(ENTITY_DELETED_ATOM_ITEMS)
                    for l, aux_tag in enumerate(ENTITY_DELETED_ATOM_ITEMS):  # noqa: E741
                        if aux_tag == 'Entity_assembly_ID':
                            aux[l] = _star_chain
                        elif aux_tag == 'Comp_index_ID':
                            aux[l] = _star_seq
                        elif aux_tag == 'Auth_entity_assembly_ID':
                            aux[l] = in_star_chain
                        elif aux_tag == 'Auth_seq_ID':
                            aux[l] = _in_star_seq
                        elif aux_tag == 'Comp_ID':
                            aux[l] = i[comp_index].upper()
                        elif aux_tag == 'Auth_comp_ID':
                            aux[l] = i[comp_index]

                    for _variant in variant.split(','):
                        _variant_ = _variant.strip(' ')
                        if _variant_.startswith('-'):
                            atom_list = self.get_valid_star_atom_in_xplor(i[comp_index].upper(), _variant_[1:])[0]
                            if len(atom_list) > 0:
                                for atom in atom_list:
                                    _aux = copy.copy(aux)
                                    for l, aux_tag in enumerate(ENTITY_DELETED_ATOM_ITEMS):  # noqa: E741
                                        if aux_tag == 'ID':
                                            _aux[l] = len(aux_row) + 1
                                        elif aux_tag == 'Atom_ID':
                                            _aux[l] = atom
                                        elif aux_tag == 'Auth_variant_ID':
                                            _aux[l] = _variant_[1:]

                                    aux_row.append(_aux)

        return out_row, aux_row

    def nef2star_bond_row(self, nef_tags, star_tags, loop_data):
        """ Translate rows in bond loop from NEF into NMR-STAR.
            @author: Masashi Yokochi
            @param nef_tags: list of NEF tags
            @param star_tags: list of NMR-STAR tags
            @param loop_data: loop data of NEF
            @return: rows of NMR-STAR
        """

        out_row = []

        nef_comp_index_1 = nef_tags.index('_nef_covalent_links.residue_name_1')
        nef_atom_index_1 = nef_tags.index('_nef_covalent_links.atom_name_1')
        nef_comp_index_2 = nef_tags.index('_nef_covalent_links.residue_name_2')
        nef_atom_index_2 = nef_tags.index('_nef_covalent_links.atom_name_2')

        if '_Bond.ID' in star_tags:
            star_id_index = star_tags.index('_Bond.ID')
        else:
            star_id_index = -1

        star_type_index = star_tags.index('_Bond.Type')
        star_value_order_index = star_tags.index('_Bond.Value_order')

        seq_ident_tags = self.get_seq_ident_tags(nef_tags, 'nef')

        for tag in seq_ident_tags:
            chain_tag = tag['chain_tag']
            seq_tag = tag['seq_tag']

            if chain_tag.endswith('_1'):
                chain_tag_1 = chain_tag
                seq_tag_1 = seq_tag
            else:
                chain_tag_2 = chain_tag
                seq_tag_2 = seq_tag

        key_indices = [star_tags.index(j) for j in ['_Bond.Entity_assembly_ID_1', '_Bond.Comp_index_ID_1', '_Bond.Atom_ID_1',
                                                    '_Bond.Entity_assembly_ID_2', '_Bond.Comp_index_ID_2', '_Bond.Atom_ID_2']]

        index = 1

        for i in loop_data:

            buf_row = []

            tag_map = {}
            self_tag_map = {}

            for tag in seq_ident_tags:
                chain_tag = tag['chain_tag']
                seq_tag = tag['seq_tag']

                nef_chain = i[nef_tags.index(chain_tag)]
                _nef_seq = i[nef_tags.index(seq_tag)]
                if isinstance(_nef_seq, str) and _nef_seq not in emptyValue:
                    _nef_seq = int(_nef_seq)

                seq_key = (nef_chain, _nef_seq)

                try:
                    tag_map[chain_tag], tag_map[seq_tag] = self.authSeqMap[seq_key]
                    self_tag_map[chain_tag], self_tag_map[seq_tag] = self.selfSeqMap[seq_key]
                except KeyError:
                    tag_map[chain_tag] = nef_chain
                    tag_map[seq_tag] = _nef_seq
                    self_tag_map[chain_tag] = nef_chain
                    self_tag_map[seq_tag] = _nef_seq

            intra_residue = i[nef_tags.index(chain_tag_1)] == i[nef_tags.index(chain_tag_2)]\
                and i[nef_tags.index(seq_tag_1)] == i[nef_tags.index(seq_tag_2)]

            atom_list_1 = self.get_star_atom(i[nef_comp_index_1], i[nef_atom_index_1])[0]
            atom_list_2 = self.get_star_atom(i[nef_comp_index_2], i[nef_atom_index_2])[0]

            for k in atom_list_1:

                for l in atom_list_2:  # noqa: E741

                    if intra_residue and l == k:  # noqa: E741
                        continue

                    buf = [None] * len(star_tags)

                    for j in nef_tags:

                        auth_tag, data_tag, _ = self.get_star_tag(j)

                        if auth_tag is None:
                            continue

                        data = i[nef_tags.index(j)]

                        if 'chain_code' in j or 'sequence_code' in j:
                            buf[star_tags.index(auth_tag)] = self_tag_map[j]
                        else:
                            buf[star_tags.index(auth_tag)] = data

                        if auth_tag != data_tag:

                            data_index = star_tags.index(data_tag)

                            if 'chain_code' in j or 'sequence_code' in j:
                                buf[data_index] = tag_map[j]
                            elif j == '_nef_covalent_links.atom_name_1':
                                buf[data_index] = k
                            elif j == '_nef_covalent_links.atom_name_2':
                                buf[data_index] = l
                            else:
                                buf[data_index] = data

                    # 'amide': (C=O)-N
                    # 'directed': N-O
                    # 'disulfide': S-S
                    # 'ester': (C=O)-O
                    # 'ether': -O-
                    # 'hydrogen': (O/N/F)-H-(O/N/F)
                    # 'metal coordination': (N/O/S)-Metal
                    # 'peptide': (C=O)-N
                    # 'thioether': -S-
                    # 'oxime': >C=N-OH
                    # 'thioester': -(C=O)-S-
                    # 'phosphoester': ?
                    # 'phosphodiester': -(PO4)-
                    # 'diselenide': Se-Se
                    buf[star_type_index] = 'covalent'
                    if k == 'SG' and l == 'SG':  # noqa: E741
                        buf[star_type_index] = 'disulfide'
                    elif k == 'SE' and l == 'SE':  # noqa: E741
                        buf[star_type_index] = 'diselenide'
                    elif (k in NON_METAL_ELEMENTS and (l in PARAMAGNETIC_ELEMENTS or l in FERROMAGNETIC_ELEMENTS)) or\
                         (l in NON_METAL_ELEMENTS and (k in PARAMAGNETIC_ELEMENTS or k in FERROMAGNETIC_ELEMENTS)):
                        buf[star_type_index] = 'metal coordination'
                    elif ((k == 'C' and l == 'N') or (l == 'C' and k == 'N'))\
                            and i[nef_tags.index(chain_tag_1)] == i[nef_tags.index(chain_tag_2)]\
                            and i[nef_tags.index(seq_tag_1)] != i[nef_tags.index(seq_tag_2)]:
                        buf[star_type_index] = 'peptide'
                    buf[star_value_order_index] = 'sing'

                    buf_row.append(buf)

            keys = set()

            for b in buf_row:

                key = ''
                for j in key_indices:
                    key += ' ' + str(b[j])
                key.rstrip()

                if key in keys:
                    continue

                keys.add(key)

                if star_id_index >= 0:
                    b[star_id_index] = index

                index += 1

                out_row.append(b)

        return out_row

    def star2star_bond_row(self, in_star_tags, star_tags, loop_data):
        """ Translate rows in bond loop from PyNMRSTAR data object into NMR-STAR.
            @author: Masashi Yokochi
            @param in_star_tags: list of input NMR-STAR tags
            @param star_tags: list of NMR-STAR tags
            @param loop_data: loop data of input NMR-STAR
            @return: rows of NMR-STAR
        """

        out_row = []

        in_star_comp_index_1 = in_star_tags.index('_Bond.Comp_ID_1')
        in_star_atom_index_1 = in_star_tags.index('_Bond.Atom_ID_1')
        in_star_comp_index_2 = in_star_tags.index('_Bond.Comp_ID_2')
        in_star_atom_index_2 = in_star_tags.index('_Bond.Atom_ID_2')

        if '_Bond.ID' in star_tags:
            star_id_index = star_tags.index('_Bond.ID')
        else:
            star_id_index = -1

        star_type_index = star_tags.index('_Bond.Type')
        star_value_order_index = star_tags.index('_Bond.Value_order')

        seq_ident_tags = self.get_seq_ident_tags(in_star_tags, 'nmr-star')

        for tag in seq_ident_tags:
            chain_tag = tag['chain_tag']
            seq_tag = tag['seq_tag']

            if chain_tag.endswith('_1'):
                chain_tag_1 = chain_tag
                seq_tag_1 = seq_tag
            else:
                chain_tag_2 = chain_tag
                seq_tag_2 = seq_tag

        key_indices = [star_tags.index(j) for j in ['_Bond.Entity_assembly_ID_1', '_Bond.Comp_index_ID_1', '_Bond.Atom_ID_1',
                                                    '_Bond.Entity_assembly_ID_2', '_Bond.Comp_index_ID_2', '_Bond.Atom_ID_2']]

        index = 1

        for i in loop_data:

            buf_row = []

            tag_map = {}
            self_tag_map = {}

            for tag in seq_ident_tags:
                chain_tag = tag['chain_tag']
                seq_tag = tag['seq_tag']

                in_star_chain = i[in_star_tags.index(chain_tag)]
                _in_star_seq = i[in_star_tags.index(seq_tag)]
                if isinstance(_in_star_seq, str) and _in_star_seq not in emptyValue:
                    _in_star_seq = int(_in_star_seq)

                seq_key = (in_star_chain, _in_star_seq)

                try:
                    tag_map[chain_tag], tag_map[seq_tag] = self.authSeqMap[seq_key]
                    self_tag_map[chain_tag], self_tag_map[seq_tag] = self.selfSeqMap[seq_key]
                except KeyError:
                    tag_map[chain_tag] = in_star_chain
                    tag_map[seq_tag] = _in_star_seq
                    self_tag_map[chain_tag] = in_star_chain
                    self_tag_map[seq_tag] = _in_star_seq

            intra_residue = i[in_star_tags.index(chain_tag_1)] == i[in_star_tags.index(chain_tag_2)]\
                and i[in_star_tags.index(seq_tag_1)] == i[in_star_tags.index(seq_tag_2)]

            atom_list_1 = self.get_valid_star_atom_in_xplor(i[in_star_comp_index_1], i[in_star_atom_index_1])[0]
            atom_list_2 = self.get_valid_star_atom_in_xplor(i[in_star_comp_index_2], i[in_star_atom_index_2])[0]

            for k in atom_list_1:

                for l in atom_list_2:  # noqa: E741

                    if intra_residue and l == k:  # noqa: E741
                        continue

                    buf = [None] * len(star_tags)

                    for data_tag in in_star_tags:

                        auth_tag, _ = self.get_star_auth_tag(data_tag)

                        if auth_tag is None:
                            continue

                        data = i[in_star_tags.index(data_tag)]

                        if 'Entity_assembly_ID' in data_tag or 'Comp_index_ID' in data_tag:
                            buf[star_tags.index(auth_tag)] = self_tag_map[data_tag]
                        else:
                            buf[star_tags.index(auth_tag)] = data

                        if auth_tag != data_tag:

                            data_index = star_tags.index(data_tag)

                            if 'Entity_assembly_ID' in data_tag or 'Comp_index_ID' in data_tag:
                                buf[data_index] = tag_map[data_tag]
                            elif 'Comp_ID' in data_tag:
                                buf[data_index] = data.upper()
                            elif data_tag == '_Bond.Atom_ID_1':
                                buf[data_index] = k
                            elif data_tag == '_Bond.Atom_ID_2':
                                buf[data_index] = l
                            else:
                                buf[data_index] = data

                    # 'amide': (C=O)-N
                    # 'directed': N-O
                    # 'disulfide': S-S
                    # 'ester': (C=O)-O
                    # 'ether': -O-
                    # 'hydrogen': (O/N/F)-H-(O/N/F)
                    # 'metal coordination': (N/O/S)-Metal
                    # 'peptide': (C=O)-N
                    # 'thioether': -S-
                    # 'oxime': >C=N-OH
                    # 'thioester': -(C=O)-S-
                    # 'phosphoester': ?
                    # 'phosphodiester': -(PO4)-
                    # 'diselenide': Se-Se
                    buf[star_type_index] = 'covalent'
                    if k == 'SG' and l == 'SG':  # noqa: E741
                        buf[star_type_index] = 'disulfide'
                    elif k == 'SE' and l == 'SE':  # noqa: E741
                        buf[star_type_index] = 'diselenide'
                    elif (k in NON_METAL_ELEMENTS and (l in PARAMAGNETIC_ELEMENTS or l in FERROMAGNETIC_ELEMENTS)) or\
                         (l in NON_METAL_ELEMENTS and (k in PARAMAGNETIC_ELEMENTS or k in FERROMAGNETIC_ELEMENTS)):
                        buf[star_type_index] = 'metal coordination'
                    elif ((k == 'C' and l == 'N') or (l == 'C' and k == 'N'))\
                            and i[in_star_tags.index(chain_tag_1)] == i[in_star_tags.index(chain_tag_2)]\
                            and i[in_star_tags.index(seq_tag_1)] != i[in_star_tags.index(seq_tag_2)]:
                        buf[star_type_index] = 'peptide'
                    buf[star_value_order_index] = 'sing'

                    buf_row.append(buf)

            keys = set()

            for b in buf_row:

                key = ''
                for j in key_indices:
                    key += ' ' + str(b[j])
                key.rstrip()

                if key in keys:
                    continue

                keys.add(key)

                if star_id_index >= 0:
                    b[star_id_index] = index

                index += 1

                out_row.append(b)

        return out_row

    def nef2star_cs_row(self, nef_tags, star_tags, loop_data, leave_unmatched=False):
        """ Translate rows in chemical shift loop from NEF into NMR-STAR.
            @change: rename from original translate_cs_row() to nef2star_cs_row() by Masashi Yokochi
            @param nef_tags: list of NEF tags
            @param star_tags: list of NMR-STAR tags
            @param loop_data: loop data of NEF
            @return: rows of NMR-STAR
        """

        out_row = []

        chain_index = nef_tags.index('_nef_chemical_shift.chain_code')
        seq_index = nef_tags.index('_nef_chemical_shift.sequence_code')
        comp_index = nef_tags.index('_nef_chemical_shift.residue_name')
        atom_index = nef_tags.index('_nef_chemical_shift.atom_name')
        value_index = nef_tags.index('_nef_chemical_shift.value')

        if '_Atom_chem_shift.ID' in star_tags:
            star_id_index = star_tags.index('_Atom_chem_shift.ID')
        else:
            star_id_index = -1

        star_ambig_code_index = star_tags.index('_Atom_chem_shift.Ambiguity_code')
        star_ambig_set_id_index = star_tags.index('_Atom_chem_shift.Ambiguity_set_ID')
        star_details_index = star_tags.index('_Atom_chem_shift.Details')

        if self.insert_original_pdb_cs_items:
            star_original_chani_id = star_tags.index('_Atom_chem_shift.Original_PDB_strand_ID')
            star_original_seq_id = star_tags.index('_Atom_chem_shift.Original_PDB_residue_no')
            star_original_comp_id = star_tags.index('_Atom_chem_shift.Original_PDB_residue_name')
            star_original_atom_id = star_tags.index('_Atom_chem_shift.Original_PDB_atom_name')

        index = 1

        for nef_chain in self.authChainId:

            mapped_seq_id = [s for c, s in self.authSeqMap if c == nef_chain]
            unmapped_seq_id = sorted(set(int(i[seq_index]) for i in loop_data
                                         if i[chain_index] == nef_chain
                                         and i[seq_index] not in emptyValue
                                         and intPattern.match(i[seq_index]) is not None
                                         and int(i[seq_index]) not in mapped_seq_id))

            if len(unmapped_seq_id) > 0:
                mapped_seq_id.extend(unmapped_seq_id)

            for _nef_seq in sorted(mapped_seq_id):

                nef_seq = str(_nef_seq)

                try:
                    star_chain, _star_seq = self.authSeqMap[(nef_chain, _nef_seq)]
                    cif_chain, _cif_seq = self.selfSeqMap[(nef_chain, _nef_seq)]
                except KeyError:
                    star_chain = nef_chain
                    _star_seq = _nef_seq
                    cif_chain = nef_chain
                    _cif_seq = _nef_seq

                in_row = [i for i in loop_data
                          if i[chain_index] == nef_chain and i[seq_index] == nef_seq and i[value_index] not in emptyValue]

                if len(in_row) == 0:
                    continue

                for i in in_row:

                    atom_list, ambiguity_code, details = self.get_star_atom(i[comp_index], i[atom_index], None, leave_unmatched)

                    for atom in atom_list:

                        out = [None] * len(star_tags)

                        for j in nef_tags:

                            auth_tag, data_tag, _ = self.get_star_tag(j)

                            if auth_tag is None:
                                continue

                            data = i[nef_tags.index(j)]

                            if j == '_nef_chemical_shift.chain_code':
                                out[star_tags.index(auth_tag)] = cif_chain
                            elif j == '_nef_chemical_shift.sequence_code':
                                out[star_tags.index(auth_tag)] = _cif_seq
                            else:
                                out[star_tags.index(auth_tag)] = data

                            if auth_tag != data_tag:

                                if j == '_nef_chemical_shift.atom_name':
                                    out[star_tags.index(data_tag)] = atom
                                    if self.insert_original_pdb_cs_items:
                                        out[star_original_atom_id] = atom
                                elif j == '_nef_chemical_shift.chain_code':
                                    out[star_tags.index(data_tag)] = star_chain
                                    if self.insert_original_pdb_cs_items:
                                        out[star_original_chani_id] = cif_chain
                                elif j == '_nef_chemical_shift.sequence_code':
                                    out[star_tags.index(data_tag)] = _star_seq
                                    if self.insert_original_pdb_cs_items:
                                        out[star_original_seq_id] = _cif_seq
                                elif j == '_nef_chemical_shift.residue_name':
                                    out[star_tags.index(data_tag)] = data
                                    if self.insert_original_pdb_cs_items:
                                        out[star_original_comp_id] = data
                                else:
                                    out[star_tags.index(data_tag)] = data

                        if star_id_index >= 0:
                            out[star_id_index] = index

                        out[star_ambig_code_index] = ambiguity_code
                        out[star_ambig_set_id_index] = None
                        out[star_details_index] = details

                        index += 1

                        out_row.append(out)

        return out_row

    def star2nef_cs_row(self, star_tags, nef_tags, loop_data):
        """ Translate rows in chemical shift loop from NMR-STAR into NEF.
            @author: Masashi Yokochi
            @param star_tags: list of NMR-STAR tags
            @param nef_tags: list of NEF tags
            @param loop_data: loop data of NMR-STAR
            @return: rows of NEF
        """

        out_row = []

        chain_index = star_tags.index('_Atom_chem_shift.Entity_assembly_ID')
        seq_index = star_tags.index('_Atom_chem_shift.Comp_index_ID')
        comp_index = star_tags.index('_Atom_chem_shift.Comp_ID')
        atom_index = star_tags.index('_Atom_chem_shift.Atom_ID')
        ambig_index = star_tags.index('_Atom_chem_shift.Ambiguity_code')
        value_index = star_tags.index('_Atom_chem_shift.Val')

        for star_chain in self.authChainId:

            _star_chain = int(star_chain)
            _cif_chain = None if star_chain not in self.star2CifChainMapping else self.star2CifChainMapping[star_chain]

            mapped_seq_id = [s for c, s in self.authSeqMap if c == _star_chain]
            unmapped_seq_id = set(int(i[seq_index]) for i in loop_data
                                  if i[chain_index] == star_chain
                                  and i[seq_index] not in emptyValue
                                  and intPattern.match(i[seq_index]) is not None
                                  and int(i[seq_index]) not in mapped_seq_id)

            if len(unmapped_seq_id) > 0:
                mapped_seq_id.extend(unmapped_seq_id)

            for _star_seq in sorted(mapped_seq_id):

                star_seq = str(_star_seq)

                in_row = [i for i in loop_data
                          if i[chain_index] == star_chain and i[seq_index] == star_seq and i[value_index] not in emptyValue]

                if len(in_row) == 0:
                    continue

                star_atom_list = [{'atom_id': i[atom_index], 'ambig_code': i[ambig_index], 'value': i[value_index]} for i in in_row]

                atom_list, _, atom_id_map = self.get_nef_atom(in_row[0][comp_index], star_atom_list)

                if len(atom_list) == 0:
                    continue

                seq_key = (_star_chain, _star_seq)

                try:
                    cif_chain, _cif_seq = self.authSeqMap[seq_key]
                except KeyError:
                    try:
                        cif_chain = self.selfSeqMap[(_star_chain, 1)][0]
                        _cif_seq = _star_seq
                    except KeyError:
                        if _star_chain in emptyValue or _star_chain not in self.authChainId:
                            nef_chain = _star_chain
                        else:
                            cid = self.authChainId.index(_star_chain)
                            nef_chain = indexToLetter(cid)
                        cif_chain = nef_chain
                        _cif_seq = _star_seq

                if _cif_chain is not None:
                    cif_chain = _cif_chain

                if seq_key not in self.atomIdMap:
                    self.atomIdMap[seq_key] = {}

                self.atomIdMap[seq_key].update(atom_id_map)

                for atom in atom_list:

                    out = [None] * len(nef_tags)

                    star_atom = next((k for k, v in atom_id_map.items() if v == atom), atom)
                    i = next((l for l in in_row if l[atom_index] == star_atom), None)  # noqa: E741

                    if i is None:

                        if star_atom.endswith('%'):
                            star_atom = star_atom.replace('%', '')
                            i = next((l for l in in_row if l[atom_index] == star_atom), None)  # noqa: E741

                        if i is None:
                            continue

                    for j in star_tags:

                        nef_tag, _ = self.get_nef_tag(j)

                        if nef_tag is None:
                            continue

                        data_index = nef_tags.index(nef_tag)

                        if nef_tag == '_nef_chemical_shift.atom_name':
                            out[data_index] = atom
                        elif nef_tag == '_nef_chemical_shift.chain_code':
                            out[data_index] = cif_chain
                        elif nef_tag == '_nef_chemical_shift.sequence_code':
                            out[data_index] = _cif_seq
                        else:
                            out[data_index] = i[star_tags.index(j)]

                    out_row.append(out)

        return out_row

    def star2star_cs_row(self, in_star_tags, star_tags, loop_data, leave_unmatched=False):
        """ Translate rows in chemical shift loop from PyNMRSTAR data object into NMR-STAR.
            @author: Masashi Yokochi
            @param in_star_tags: list of input NMR-STAR tags
            @param star_tags: list of NMR-STAR tags
            @param loop_data: loop data of input NMR-STAR
            @return: rows of NMR-STAR
        """

        out_row = []

        chain_index = in_star_tags.index('_Atom_chem_shift.Entity_assembly_ID')
        seq_index = in_star_tags.index('_Atom_chem_shift.Comp_index_ID')
        comp_index = in_star_tags.index('_Atom_chem_shift.Comp_ID')
        atom_index = in_star_tags.index('_Atom_chem_shift.Atom_ID')
        value_index = in_star_tags.index('_Atom_chem_shift.Val')

        if '_Atom_chem_shift.ID' in star_tags:
            star_id_index = star_tags.index('_Atom_chem_shift.ID')
        else:
            star_id_index = -1

        star_ambig_code_index = star_tags.index('_Atom_chem_shift.Ambiguity_code')
        star_ambig_set_id_index = star_tags.index('_Atom_chem_shift.Ambiguity_set_ID')
        star_details_index = star_tags.index('_Atom_chem_shift.Details')

        if self.insert_original_pdb_cs_items:
            star_original_chani_id = star_tags.index('_Atom_chem_shift.Original_PDB_strand_ID')
            star_original_seq_id = star_tags.index('_Atom_chem_shift.Original_PDB_residue_no')
            star_original_comp_id = star_tags.index('_Atom_chem_shift.Original_PDB_residue_name')
            star_original_atom_id = star_tags.index('_Atom_chem_shift.Original_PDB_atom_name')

        index = 1

        for in_star_chain in self.authChainId:

            mapped_seq_id = [s for c, s in self.authSeqMap if c == in_star_chain]
            unmapped_seq_id = sorted(set(int(i[seq_index]) for i in loop_data
                                         if i[chain_index] == in_star_chain
                                         and i[seq_index] not in emptyValue
                                         and intPattern.match(i[seq_index]) is not None
                                         and int(i[seq_index]) not in mapped_seq_id))

            if len(unmapped_seq_id) > 0:
                mapped_seq_id.extend(unmapped_seq_id)

            for _in_star_seq in sorted(mapped_seq_id):

                in_star_seq = str(_in_star_seq)

                try:
                    star_chain, _star_seq = self.authSeqMap[(in_star_chain, _in_star_seq)]
                    cif_chain, _cif_seq = self.selfSeqMap[(in_star_chain, _in_star_seq)]
                except KeyError:
                    star_chain = in_star_chain
                    _star_seq = _in_star_seq
                    cif_chain = in_star_chain
                    _cif_seq = _in_star_seq

                in_row = [i for i in loop_data
                          if (i[chain_index] == in_star_chain or i[chain_index] in emptyValue)
                          and i[seq_index] == in_star_seq
                          and i[value_index] not in emptyValue]

                if len(in_row) == 0:
                    continue

                for i in in_row:

                    atom_list, ambiguity_code, details = self.get_valid_star_atom_in_xplor(i[comp_index], i[atom_index], None, leave_unmatched)

                    for atom in atom_list:

                        out = [None] * len(star_tags)

                        for data_tag in in_star_tags:

                            auth_tag, _ = self.get_star_auth_tag(data_tag)

                            if auth_tag is None:
                                continue

                            data = i[in_star_tags.index(data_tag)]

                            if data_tag == '_Atom_chem_shift.Entity_assembly_ID':
                                out[star_tags.index(auth_tag)] = cif_chain
                            elif data_tag == '_Atom_chem_shift.Comp_index_ID':
                                out[star_tags.index(auth_tag)] = _cif_seq
                            else:
                                out[star_tags.index(auth_tag)] = data

                            if auth_tag != data_tag:

                                if data_tag == '_Atom_chem_shift.Atom_ID':
                                    out[star_tags.index(data_tag)] = atom
                                    if self.insert_original_pdb_cs_items:
                                        out[star_original_atom_id] = atom
                                elif data_tag == '_Atom_chem_shift.Entity_assembly_ID':
                                    out[star_tags.index(data_tag)] = star_chain
                                    if self.insert_original_pdb_cs_items:
                                        out[star_original_chani_id] = cif_chain
                                elif data_tag == '_Atom_chem_shift.Comp_index_ID':
                                    out[star_tags.index(data_tag)] = _star_seq
                                    if self.insert_original_pdb_cs_items:
                                        out[star_original_seq_id] = _cif_seq
                                elif data_tag == '_Atom_chem_shift.Comp_ID':
                                    out[star_tags.index(data_tag)] = data.upper()
                                    if self.insert_original_pdb_cs_items:
                                        out[star_original_comp_id] = data.upper()
                                else:
                                    out[star_tags.index(data_tag)] = data

                        if star_id_index >= 0:
                            out[star_id_index] = index

                        out[star_ambig_code_index] = ambiguity_code
                        out[star_ambig_set_id_index] = None
                        out[star_details_index] = details

                        index += 1

                        out_row.append(out)

        return out_row

    def get_seq_ident_tags(self, in_tags, file_type):  # pylint: disable=no-self-use
        """ Return list of tags utilized for sequence identification.
            @change: rename from original get_residue_identifier() to get_seq_ident_tags() by Masashi Yokochi
            @change: return list of dictionary
            @param in_tags: list of tags
            @param file_type: input file type either 'nef' or 'nmr-star'
            @return: list of tags utilized for sequence identification in given tags
        """

        out_tags = []

        for j in range(1, MAX_DIM_NUM_OF_SPECTRA):

            chain_tag_suffix = f".chain_code_{j}" if file_type == 'nef' else f".Entity_assembly_ID_{j}"

            try:
                chain_tag = next(i for i in in_tags if i.endswith(chain_tag_suffix))
            except StopIteration:
                break

            seq_tag_suffix = f".sequence_code_{j}" if file_type == 'nef' else f".Comp_index_ID_{j}"

            try:
                seq_tag = next(i for i in in_tags if i.endswith(seq_tag_suffix))
            except StopIteration:
                break

            out_tags.append({'chain_tag': chain_tag, 'seq_tag': seq_tag})

        return out_tags

    def get_atom_keys(self, in_tags, file_type):  # pylint: disable=no-self-use
        """ Return list of keys utilized for atom identification.
            @change: return list of dictionary
            @param in_tags: list of tags
            @param file_type: input file type either 'nef' or 'nmr-star'
            @return: list of keys utilized for atom identification in given tags
        """

        out_tags = []

        for j in range(1, MAX_DIM_NUM_OF_SPECTRA):

            chain_tag_suffix = f".chain_code_{j}" if file_type == 'nef' else f".Entity_assembly_ID_{j}"

            try:
                chain_tag = next(i for i in in_tags if i.endswith(chain_tag_suffix))
            except StopIteration:
                break

            seq_tag_suffix = f".sequence_code_{j}" if file_type == 'nef' else f".Comp_index_ID_{j}"

            try:
                seq_tag = next(i for i in in_tags if i.endswith(seq_tag_suffix))
            except StopIteration:
                break

            atom_tag_suffix = f".atom_name_{j}" if file_type == 'nef' else f".Atom_ID_{j}"

            try:
                atom_tag = next(i for i in in_tags if i.endswith(atom_tag_suffix))
            except StopIteration:
                break

            out_tags.append({'chain_tag': chain_tag.split('.')[1], 'seq_tag': seq_tag.split('.')[1], 'atom_tag': atom_tag.split('.')[1]})

        return out_tags

    def nef2star_dist_row(self, nef_tags, star_tags, loop_data):
        """ Translate rows in distance restraint loop from NEF into NMR-STAR.
            @change: rename the original translate_restraint_row() to nef2star_dist_row() by Masashi Yokochi
            @param nef_tags: list of NEF tags
            @param star_tags: list of NMR-STAR tags
            @param loop_data: loop data of NEF
            @return: rows of NMR-STAR
        """

        out_row = []

        nef_comp_index_1 = nef_tags.index('_nef_distance_restraint.residue_name_1')
        nef_atom_index_1 = nef_tags.index('_nef_distance_restraint.atom_name_1')
        nef_comp_index_2 = nef_tags.index('_nef_distance_restraint.residue_name_2')
        nef_atom_index_2 = nef_tags.index('_nef_distance_restraint.atom_name_2')

        seq_ident_tags = self.get_seq_ident_tags(nef_tags, 'nef')

        for tag in seq_ident_tags:
            chain_tag = tag['chain_tag']
            seq_tag = tag['seq_tag']

            if chain_tag.endswith('_1'):
                chain_tag_1 = chain_tag
                seq_tag_1 = seq_tag
            else:
                chain_tag_2 = chain_tag
                seq_tag_2 = seq_tag

        try:
            index_index = star_tags.index('_Gen_dist_constraint.Index_ID')
        except ValueError:
            index_index = -1

        key_indices = [star_tags.index(j) for j in ['_Gen_dist_constraint.Entity_assembly_ID_1',
                                                    '_Gen_dist_constraint.Comp_index_ID_1',
                                                    '_Gen_dist_constraint.Atom_ID_1',
                                                    '_Gen_dist_constraint.Entity_assembly_ID_2',
                                                    '_Gen_dist_constraint.Comp_index_ID_2',
                                                    '_Gen_dist_constraint.Atom_ID_2']]

        member_code_index = star_tags.index('_Gen_dist_constraint.Member_logic_code')

        id_index = nef_tags.index('_nef_distance_restraint.restraint_id')

        id_list = sorted(set(int(i[id_index]) for i in loop_data))

        index = 1

        for id in id_list:  # pylint: disable=redefined-builtin

            in_row = [i for i in loop_data if i[id_index] == str(id)]

            buf_row = []

            for i in in_row:

                tag_map = {}
                self_tag_map = {}

                for tag in seq_ident_tags:
                    chain_tag = tag['chain_tag']
                    seq_tag = tag['seq_tag']

                    nef_chain = i[nef_tags.index(chain_tag)]
                    _nef_seq = i[nef_tags.index(seq_tag)]
                    if isinstance(_nef_seq, str) and _nef_seq not in emptyValue:
                        _nef_seq = int(_nef_seq)

                    seq_key = (nef_chain, _nef_seq)

                    try:
                        tag_map[chain_tag], tag_map[seq_tag] = self.authSeqMap[seq_key]
                        self_tag_map[chain_tag], self_tag_map[seq_tag] = self.selfSeqMap[seq_key]
                    except KeyError:
                        tag_map[chain_tag] = nef_chain
                        tag_map[seq_tag] = _nef_seq
                        self_tag_map[chain_tag] = nef_chain
                        self_tag_map[seq_tag] = _nef_seq

                intra_residue = i[nef_tags.index(chain_tag_1)] == i[nef_tags.index(chain_tag_2)]\
                    and i[nef_tags.index(seq_tag_1)] == i[nef_tags.index(seq_tag_2)]

                atom_list_1 = self.get_star_atom(i[nef_comp_index_1], i[nef_atom_index_1])[0]
                atom_list_2 = self.get_star_atom(i[nef_comp_index_2], i[nef_atom_index_2])[0]

                or_code = len(atom_list_1) * len(atom_list_2) > 1

                for k in atom_list_1:

                    for l in atom_list_2:  # noqa: E741

                        if intra_residue and l == k:  # noqa: E741
                            continue

                        buf = [None] * len(star_tags)

                        for j in nef_tags:

                            auth_tag, data_tag, _ = self.get_star_tag(j)

                            if auth_tag is None:
                                continue

                            data = i[nef_tags.index(j)]

                            if 'chain_code' in j or 'sequence_code' in j:
                                buf[star_tags.index(auth_tag)] = self_tag_map[j]
                            else:
                                buf[star_tags.index(auth_tag)] = data

                            if auth_tag != data_tag:

                                data_index = star_tags.index(data_tag)

                                if 'chain_code' in j or 'sequence_code' in j:
                                    buf[data_index] = tag_map[j]
                                elif j == '_nef_distance_restraint.atom_name_1':
                                    buf[data_index] = k
                                elif j == '_nef_distance_restraint.atom_name_2':
                                    buf[data_index] = l
                                else:
                                    buf[data_index] = data
                            #
                            # if details_1 is None and details_2 is None:
                            #     pass

                            # else:

                            #     details_index = star_tags.index('_Gen_dist_constraint.Details')

                            #     buf[details_index] = ' '.join(filter(None, [details_1, detail_2]))
                            #
                        if or_code:
                            buf[member_code_index] = 'OR'

                        buf_row.append(buf)

            keys = set()

            for i in buf_row:

                key = ''
                for j in key_indices:
                    key += ' ' + str(i[j])
                key.rstrip()

                if key in keys:
                    continue

                keys.add(key)

                if index_index >= 0:
                    i[index_index] = index

                index += 1

                out_row.append(i)

        return out_row

    def star2nef_dist_row(self, star_tags, nef_tags, loop_data):
        """ Translate rows in distance restraint loop from NMR-STAR into NEF.
            @author: Masashi Yokochi
            @param star_tags: list of NMR-STAR tags
            @param nef_tags: list of NEF tags
            @param loop_data: loop data of NMR-STAR
            @return: rows of NEF
        """

        out_row = []

        comp_1_index = star_tags.index('_Gen_dist_constraint.Comp_ID_1')
        comp_2_index = star_tags.index('_Gen_dist_constraint.Comp_ID_2')

        seq_ident_tags = self.get_seq_ident_tags(star_tags, 'nmr-star')

        for tag in seq_ident_tags:
            chain_tag = tag['chain_tag']
            seq_tag = tag['seq_tag']

            if chain_tag.endswith('_1'):
                chain_tag_1 = chain_tag
                # seq_tag_1 = seq_tag
            else:
                pass
                # chain_tag_2 = chain_tag
                # seq_tag_2 = seq_tag

        try:
            index_index = nef_tags.index('_nef_distance_restraint.index')
        except ValueError:
            index_index = -1

        key_indices = [nef_tags.index(j) for j in ['_nef_distance_restraint.chain_code_1',
                                                   '_nef_distance_restraint.sequence_code_1',
                                                   '_nef_distance_restraint.atom_name_1',
                                                   '_nef_distance_restraint.chain_code_2',
                                                   '_nef_distance_restraint.sequence_code_2',
                                                   '_nef_distance_restraint.atom_name_2']]

        id_index = star_tags.index('_Gen_dist_constraint.ID')

        id_list = sorted(set(int(i[id_index]) for i in loop_data))

        index = 1

        for id in id_list:  # pylint: disable=redefined-builtin

            in_row = [i for i in loop_data if i[id_index] == str(id)]

            buf_row = []

            for i in in_row:

                tag_map = {}

                for tag in seq_ident_tags:
                    chain_tag = tag['chain_tag']
                    seq_tag = tag['seq_tag']

                    star_chain = i[star_tags.index(chain_tag)]
                    _star_chain = star_chain
                    if isinstance(star_chain, str) and star_chain not in emptyValue:
                        _star_chain = int(star_chain)

                    _star_seq = i[star_tags.index(seq_tag)]
                    if isinstance(_star_seq, str) and _star_seq not in emptyValue:
                        _star_seq = int(_star_seq)

                    seq_key = (_star_chain, _star_seq)

                    try:
                        tag_map[chain_tag], tag_map[seq_tag] = self.authSeqMap[seq_key]
                    except KeyError:
                        try:
                            nef_chain = self.selfSeqMap[(_star_chain, 1)][0]
                        except KeyError:
                            if _star_chain in emptyValue or _star_chain not in self.authChainId:
                                nef_chain = _star_chain
                            else:
                                cid = self.authChainId.index(_star_chain)
                                nef_chain = indexToLetter(cid)
                        tag_map[chain_tag] = nef_chain
                        tag_map[seq_tag] = _star_seq

                    if star_chain in self.star2CifChainMapping:
                        tag_map[chain_tag] = self.star2CifChainMapping[star_chain]

                    if chain_tag == chain_tag_1:
                        seq_key_1 = seq_key
                    else:
                        seq_key_2 = seq_key

                buf = [None] * len(nef_tags)

                for j in star_tags:

                    nef_tag, _ = self.get_nef_tag(j)

                    if nef_tag is None:
                        continue

                    data = i[star_tags.index(j)]

                    data_index = nef_tags.index(nef_tag)

                    if 'chain_code' in nef_tag or 'sequence_code' in nef_tag:
                        buf[data_index] = tag_map[j]
                    elif nef_tag == '_nef_distance_restraint.atom_name_1':
                        try:
                            if self.atomIdMap is not None:
                                buf[data_index] = self.atomIdMap[seq_key_1][data]
                        except KeyError:
                            atom_list = self.get_nef_atom(i[comp_1_index], [{'atom_id': data, 'ambig_code': None, 'value': None}])[0]
                            if len(atom_list) > 0:
                                buf[data_index] = atom_list[0]
                            else:
                                buf[data_index] = data
                    elif nef_tag == '_nef_distance_restraint.atom_name_2':
                        try:
                            if self.atomIdMap is not None:
                                buf[data_index] = self.atomIdMap[seq_key_2][data]
                        except KeyError:
                            atom_list = self.get_nef_atom(i[comp_2_index], [{'atom_id': data, 'ambig_code': None, 'value': None}])[0]
                            if len(atom_list) > 0:
                                buf[data_index] = atom_list[0]
                            else:
                                buf[data_index] = data
                    else:
                        buf[data_index] = data

                buf_row.append(buf)

            keys = set()

            for i in buf_row:

                key = ''
                for j in key_indices:
                    key += ' ' + str(i[j])
                key.rstrip()

                if key in keys:
                    continue

                keys.add(key)

                if index_index >= 0:
                    i[index_index] = index

                index += 1

                out_row.append(i)

        return out_row

    def star2star_dist_row(self, in_star_tags, star_tags, loop_data):
        """ Translate rows in distance restraint loop from PyNMRSTAR data object into NMR-STAR.
            @author: Masashi Yokochi
            @param in_star_tags: list of input NMR-STAR tags
            @param star_tags: list of NMR-STAR tags
            @param loop_data: loop data of input NMR-STAR
            @return: rows of NMR-STAR
        """

        out_row = []

        in_star_comp_index_1 = in_star_tags.index('_Gen_dist_constraint.Comp_ID_1')
        in_star_atom_index_1 = in_star_tags.index('_Gen_dist_constraint.Atom_ID_1')
        in_star_comp_index_2 = in_star_tags.index('_Gen_dist_constraint.Comp_ID_2')
        in_star_atom_index_2 = in_star_tags.index('_Gen_dist_constraint.Atom_ID_2')

        seq_ident_tags = self.get_seq_ident_tags(in_star_tags, 'nmr-star')

        for tag in seq_ident_tags:
            chain_tag = tag['chain_tag']
            seq_tag = tag['seq_tag']

            if chain_tag.endswith('_1'):
                chain_tag_1 = chain_tag
                seq_tag_1 = seq_tag
            else:
                chain_tag_2 = chain_tag
                seq_tag_2 = seq_tag

        try:
            index_index = star_tags.index('_Gen_dist_constraint.Index_ID')
        except ValueError:
            index_index = -1

        key_indices = [star_tags.index(j) for j in ['_Gen_dist_constraint.Entity_assembly_ID_1',
                                                    '_Gen_dist_constraint.Comp_index_ID_1',
                                                    '_Gen_dist_constraint.Atom_ID_1',
                                                    '_Gen_dist_constraint.Entity_assembly_ID_2',
                                                    '_Gen_dist_constraint.Comp_index_ID_2',
                                                    '_Gen_dist_constraint.Atom_ID_2']]

        member_code_index = star_tags.index('_Gen_dist_constraint.Member_logic_code')

        id_index = in_star_tags.index('_Gen_dist_constraint.ID')

        id_list = sorted(set(int(i[id_index]) for i in loop_data))

        index = 1

        for id in id_list:  # pylint: disable=redefined-builtin

            in_row = [i for i in loop_data if i[id_index] == str(id)]

            buf_row = []

            for i in in_row:

                tag_map = {}
                self_tag_map = {}

                for tag in seq_ident_tags:
                    chain_tag = tag['chain_tag']
                    seq_tag = tag['seq_tag']

                    in_star_chain = i[in_star_tags.index(chain_tag)]
                    _in_star_seq = i[in_star_tags.index(seq_tag)]
                    if isinstance(_in_star_seq, str) and _in_star_seq not in emptyValue:
                        _in_star_seq = int(_in_star_seq)

                    seq_key = (in_star_chain, _in_star_seq)

                    try:
                        tag_map[chain_tag], tag_map[seq_tag] = self.authSeqMap[seq_key]
                        self_tag_map[chain_tag], self_tag_map[seq_tag] = self.selfSeqMap[seq_key]
                    except KeyError:
                        tag_map[chain_tag] = in_star_chain
                        tag_map[seq_tag] = _in_star_seq
                        self_tag_map[chain_tag] = in_star_chain
                        self_tag_map[seq_tag] = _in_star_seq

                intra_residue = i[in_star_tags.index(chain_tag_1)] == i[in_star_tags.index(chain_tag_2)]\
                    and i[in_star_tags.index(seq_tag_1)] == i[in_star_tags.index(seq_tag_2)]

                atom_list_1 = self.get_valid_star_atom_in_xplor(i[in_star_comp_index_1], i[in_star_atom_index_1])[0]
                atom_list_2 = self.get_valid_star_atom_in_xplor(i[in_star_comp_index_2], i[in_star_atom_index_2])[0]

                or_code = len(atom_list_1) * len(atom_list_2) > 1

                for k in atom_list_1:

                    for l in atom_list_2:  # noqa: E741

                        if intra_residue and l == k:  # noqa: E741
                            continue

                        buf = [None] * len(star_tags)

                        for data_tag in in_star_tags:

                            auth_tag, _ = self.get_star_auth_tag(data_tag)

                            if auth_tag is None:
                                continue

                            data = i[in_star_tags.index(data_tag)]

                            if 'Entity_assembly_ID' in data_tag or 'Comp_index_ID' in data_tag:
                                buf[star_tags.index(auth_tag)] = self_tag_map[data_tag]
                            else:
                                buf[star_tags.index(auth_tag)] = data

                            if auth_tag != data_tag:

                                data_index = star_tags.index(data_tag)

                                if 'Entity_assembly_ID' in data_tag or 'Comp_index_ID' in data_tag:
                                    buf[data_index] = tag_map[data_tag]
                                elif 'Comp_ID' in data_tag:
                                    buf[data_index] = data.upper()
                                elif data_tag == '_Gen_dist_constraint.Atom_ID_1':
                                    buf[data_index] = k
                                elif data_tag == '_Gen_dist_constraint.Atom_ID_2':
                                    buf[data_index] = l
                                else:
                                    buf[data_index] = data

                        if or_code:
                            buf[member_code_index] = 'OR'

                        buf_row.append(buf)

            keys = set()

            for i in buf_row:

                key = ''
                for j in key_indices:
                    key += ' ' + str(i[j])
                key.rstrip()

                if key in keys:
                    continue

                keys.add(key)

                if index_index >= 0:
                    i[index_index] = index

                index += 1

                out_row.append(i)

        return out_row

    def nef2star_dihed_row(self, nef_tags, star_tags, loop_data):
        """ Translate rows in dihedral angle restraint loop from NEF into NMR-STAR.
            @author: Masashi Yokochi
            @param nef_tags: list of NEF tags
            @param star_tags: list of NMR-STAR tags
            @param loop_data: loop data of NEF
            @return: rows of NMR-STAR
        """

        out_row = []

        nef_comp_index_1 = nef_tags.index('_nef_dihedral_restraint.residue_name_1')
        nef_atom_index_1 = nef_tags.index('_nef_dihedral_restraint.atom_name_1')
        nef_comp_index_2 = nef_tags.index('_nef_dihedral_restraint.residue_name_2')
        nef_atom_index_2 = nef_tags.index('_nef_dihedral_restraint.atom_name_2')
        nef_comp_index_3 = nef_tags.index('_nef_dihedral_restraint.residue_name_3')
        nef_atom_index_3 = nef_tags.index('_nef_dihedral_restraint.atom_name_3')
        nef_comp_index_4 = nef_tags.index('_nef_dihedral_restraint.residue_name_4')
        nef_atom_index_4 = nef_tags.index('_nef_dihedral_restraint.atom_name_4')

        seq_ident_tags = self.get_seq_ident_tags(nef_tags, 'nef')

        for tag in seq_ident_tags:
            chain_tag = tag['chain_tag']
            seq_tag = tag['seq_tag']

            if chain_tag.endswith('_1'):
                chain_tag_1 = chain_tag
                seq_tag_1 = seq_tag
            elif chain_tag.endswith('_2'):
                chain_tag_2 = chain_tag
                seq_tag_2 = seq_tag
            elif chain_tag.endswith('_3'):
                chain_tag_3 = chain_tag
                seq_tag_3 = seq_tag
            else:
                chain_tag_4 = chain_tag
                seq_tag_4 = seq_tag

        try:
            index_index = star_tags.index('_Torsion_angle_constraint.Index_ID')
        except ValueError:
            index_index = -1

        key_indices = [star_tags.index(j) for j in ['_Torsion_angle_constraint.Entity_assembly_ID_1',
                                                    '_Torsion_angle_constraint.Comp_index_ID_1',
                                                    '_Torsion_angle_constraint.Atom_ID_1',
                                                    '_Torsion_angle_constraint.Entity_assembly_ID_2',
                                                    '_Torsion_angle_constraint.Comp_index_ID_2',
                                                    '_Torsion_angle_constraint.Atom_ID_2',
                                                    '_Torsion_angle_constraint.Entity_assembly_ID_3',
                                                    '_Torsion_angle_constraint.Comp_index_ID_3',
                                                    '_Torsion_angle_constraint.Atom_ID_3',
                                                    '_Torsion_angle_constraint.Entity_assembly_ID_4',
                                                    '_Torsion_angle_constraint.Comp_index_ID_4',
                                                    '_Torsion_angle_constraint.Atom_ID_4']]

        id_index = nef_tags.index('_nef_dihedral_restraint.restraint_id')

        id_list = sorted(set(int(i[id_index]) for i in loop_data))

        index = 1

        for id in id_list:  # pylint: disable=redefined-builtin

            in_row = [i for i in loop_data if i[id_index] == str(id)]

            buf_row = []

            for i in in_row:

                tag_map = {}
                self_tag_map = {}

                for tag in seq_ident_tags:
                    chain_tag = tag['chain_tag']
                    seq_tag = tag['seq_tag']

                    nef_chain = i[nef_tags.index(chain_tag)]
                    _nef_seq = i[nef_tags.index(seq_tag)]
                    if isinstance(_nef_seq, str) and _nef_seq not in emptyValue:
                        _nef_seq = int(_nef_seq)

                    seq_key = (nef_chain, _nef_seq)

                    try:
                        tag_map[chain_tag], tag_map[seq_tag] = self.authSeqMap[seq_key]
                        self_tag_map[chain_tag], self_tag_map[seq_tag] = self.selfSeqMap[seq_key]
                    except KeyError:
                        tag_map[chain_tag] = nef_chain
                        tag_map[seq_tag] = _nef_seq
                        self_tag_map[chain_tag] = nef_chain
                        self_tag_map[seq_tag] = _nef_seq

                intra_residue_12 = i[nef_tags.index(chain_tag_1)] == i[nef_tags.index(chain_tag_2)]\
                    and i[nef_tags.index(seq_tag_1)] == i[nef_tags.index(seq_tag_2)]
                intra_residue_13 = i[nef_tags.index(chain_tag_1)] == i[nef_tags.index(chain_tag_3)]\
                    and i[nef_tags.index(seq_tag_1)] == i[nef_tags.index(seq_tag_3)]
                intra_residue_14 = i[nef_tags.index(chain_tag_1)] == i[nef_tags.index(chain_tag_4)]\
                    and i[nef_tags.index(seq_tag_1)] == i[nef_tags.index(seq_tag_4)]
                intra_residue_23 = i[nef_tags.index(chain_tag_2)] == i[nef_tags.index(chain_tag_3)]\
                    and i[nef_tags.index(seq_tag_2)] == i[nef_tags.index(seq_tag_3)]
                intra_residue_24 = i[nef_tags.index(chain_tag_2)] == i[nef_tags.index(chain_tag_4)]\
                    and i[nef_tags.index(seq_tag_2)] == i[nef_tags.index(seq_tag_4)]
                intra_residue_34 = i[nef_tags.index(chain_tag_3)] == i[nef_tags.index(chain_tag_4)]\
                    and i[nef_tags.index(seq_tag_3)] == i[nef_tags.index(seq_tag_4)]

                atom_list_1 = self.get_star_atom(i[nef_comp_index_1], i[nef_atom_index_1])[0]
                atom_list_2 = self.get_star_atom(i[nef_comp_index_2], i[nef_atom_index_2])[0]
                atom_list_3 = self.get_star_atom(i[nef_comp_index_3], i[nef_atom_index_3])[0]
                atom_list_4 = self.get_star_atom(i[nef_comp_index_4], i[nef_atom_index_4])[0]

                for k in atom_list_1:

                    for l in atom_list_2:  # noqa: E741

                        if intra_residue_12 and l == k:  # noqa: E741
                            continue

                        for m in atom_list_3:

                            if (intra_residue_13 and m == k) or (intra_residue_23 and m == l):
                                continue

                            for n in atom_list_4:

                                if (intra_residue_14 and n == k) or (intra_residue_24 and n == l) or (intra_residue_34 and n == m):
                                    continue

                                buf = [None] * len(star_tags)

                                for j in nef_tags:

                                    auth_tag, data_tag, _ = self.get_star_tag(j)

                                    if auth_tag is None:
                                        continue

                                    data = i[nef_tags.index(j)]

                                    if 'chain_code' in j or 'sequence_code' in j:
                                        buf[star_tags.index(auth_tag)] = self_tag_map[j]
                                    else:
                                        buf[star_tags.index(auth_tag)] = data

                                    if auth_tag != data_tag:

                                        data_index = star_tags.index(data_tag)

                                        if 'chain_code' in j or 'sequence_code' in j:
                                            buf[data_index] = tag_map[j]
                                        elif j == '_nef_dihedral_restraint.atom_name_1':
                                            buf[data_index] = k
                                        elif j == '_nef_dihedral_restraint.atom_name_2':
                                            buf[data_index] = l
                                        elif j == '_nef_dihedral_restraint.atom_name_3':
                                            buf[data_index] = m
                                        elif j == '_nef_dihedral_restraint.atom_name_4':
                                            buf[data_index] = n
                                        else:
                                            buf[data_index] = data

                                buf_row.append(buf)

            keys = set()

            for i in buf_row:

                key = ''
                for j in key_indices:
                    key += ' ' + str(i[j])
                key.rstrip()

                if key in keys:
                    continue

                keys.add(key)

                if index_index >= 0:
                    i[index_index] = index

                index += 1

                out_row.append(i)

        return out_row

    def star2star_dihed_row(self, in_star_tags, star_tags, loop_data):
        """ Translate rows in dihedral angle restraint loop from PyNMRSTAR data object into NMR-STAR.
            @author: Masashi Yokochi
            @param in_star_tags: list of input NMR-STAR tags
            @param star_tags: list of NMR-STAR tags
            @param loop_data: loop data of input NMR-STAR
            @return: rows of NMR-STAR
        """

        out_row = []

        in_star_comp_index_1 = in_star_tags.index('_Torsion_angle_constraint.Comp_ID_1')
        in_star_atom_index_1 = in_star_tags.index('_Torsion_angle_constraint.Atom_ID_1')
        in_star_comp_index_2 = in_star_tags.index('_Torsion_angle_constraint.Comp_ID_2')
        in_star_atom_index_2 = in_star_tags.index('_Torsion_angle_constraint.Atom_ID_2')
        in_star_comp_index_3 = in_star_tags.index('_Torsion_angle_constraint.Comp_ID_3')
        in_star_atom_index_3 = in_star_tags.index('_Torsion_angle_constraint.Atom_ID_3')
        in_star_comp_index_4 = in_star_tags.index('_Torsion_angle_constraint.Comp_ID_4')
        in_star_atom_index_4 = in_star_tags.index('_Torsion_angle_constraint.Atom_ID_4')

        seq_ident_tags = self.get_seq_ident_tags(in_star_tags, 'nmr-star')

        for tag in seq_ident_tags:
            chain_tag = tag['chain_tag']
            seq_tag = tag['seq_tag']

            if chain_tag.endswith('_1'):
                chain_tag_1 = chain_tag
                seq_tag_1 = seq_tag
            elif chain_tag.endswith('_2'):
                chain_tag_2 = chain_tag
                seq_tag_2 = seq_tag
            elif chain_tag.endswith('_3'):
                chain_tag_3 = chain_tag
                seq_tag_3 = seq_tag
            else:
                chain_tag_4 = chain_tag
                seq_tag_4 = seq_tag

        try:
            index_index = star_tags.index('_Torsion_angle_constraint.Index_ID')
        except ValueError:
            index_index = -1

        key_indices = [star_tags.index(j) for j in ['_Torsion_angle_constraint.Entity_assembly_ID_1',
                                                    '_Torsion_angle_constraint.Comp_index_ID_1',
                                                    '_Torsion_angle_constraint.Atom_ID_1',
                                                    '_Torsion_angle_constraint.Entity_assembly_ID_2',
                                                    '_Torsion_angle_constraint.Comp_index_ID_2',
                                                    '_Torsion_angle_constraint.Atom_ID_2',
                                                    '_Torsion_angle_constraint.Entity_assembly_ID_3',
                                                    '_Torsion_angle_constraint.Comp_index_ID_3',
                                                    '_Torsion_angle_constraint.Atom_ID_3',
                                                    '_Torsion_angle_constraint.Entity_assembly_ID_4',
                                                    '_Torsion_angle_constraint.Comp_index_ID_4',
                                                    '_Torsion_angle_constraint.Atom_ID_4']]

        id_index = in_star_tags.index('_Torsion_angle_constraint.ID')

        id_list = sorted(set(int(i[id_index]) for i in loop_data))

        index = 1

        for id in id_list:  # pylint: disable=redefined-builtin

            in_row = [i for i in loop_data if i[id_index] == str(id)]

            buf_row = []

            for i in in_row:

                tag_map = {}
                self_tag_map = {}

                for tag in seq_ident_tags:
                    chain_tag = tag['chain_tag']
                    seq_tag = tag['seq_tag']

                    in_star_chain = i[in_star_tags.index(chain_tag)]
                    _in_star_seq = i[in_star_tags.index(seq_tag)]
                    if isinstance(_in_star_seq, str) and _in_star_seq not in emptyValue:
                        _in_star_seq = int(_in_star_seq)

                    seq_key = (in_star_chain, _in_star_seq)

                    try:
                        tag_map[chain_tag], tag_map[seq_tag] = self.authSeqMap[seq_key]
                        self_tag_map[chain_tag], self_tag_map[seq_tag] = self.selfSeqMap[seq_key]
                    except KeyError:
                        tag_map[chain_tag] = in_star_chain
                        tag_map[seq_tag] = _in_star_seq
                        self_tag_map[chain_tag] = in_star_chain
                        self_tag_map[seq_tag] = _in_star_seq

                intra_residue_12 = i[in_star_tags.index(chain_tag_1)] == i[in_star_tags.index(chain_tag_2)]\
                    and i[in_star_tags.index(seq_tag_1)] == i[in_star_tags.index(seq_tag_2)]
                intra_residue_13 = i[in_star_tags.index(chain_tag_1)] == i[in_star_tags.index(chain_tag_3)]\
                    and i[in_star_tags.index(seq_tag_1)] == i[in_star_tags.index(seq_tag_3)]
                intra_residue_14 = i[in_star_tags.index(chain_tag_1)] == i[in_star_tags.index(chain_tag_4)]\
                    and i[in_star_tags.index(seq_tag_1)] == i[in_star_tags.index(seq_tag_4)]
                intra_residue_23 = i[in_star_tags.index(chain_tag_2)] == i[in_star_tags.index(chain_tag_3)]\
                    and i[in_star_tags.index(seq_tag_2)] == i[in_star_tags.index(seq_tag_3)]
                intra_residue_24 = i[in_star_tags.index(chain_tag_2)] == i[in_star_tags.index(chain_tag_4)]\
                    and i[in_star_tags.index(seq_tag_2)] == i[in_star_tags.index(seq_tag_4)]
                intra_residue_34 = i[in_star_tags.index(chain_tag_3)] == i[in_star_tags.index(chain_tag_4)]\
                    and i[in_star_tags.index(seq_tag_3)] == i[in_star_tags.index(seq_tag_4)]

                atom_list_1 = self.get_valid_star_atom_in_xplor(i[in_star_comp_index_1], i[in_star_atom_index_1])[0]
                atom_list_2 = self.get_valid_star_atom_in_xplor(i[in_star_comp_index_2], i[in_star_atom_index_2])[0]
                atom_list_3 = self.get_valid_star_atom_in_xplor(i[in_star_comp_index_3], i[in_star_atom_index_3])[0]
                atom_list_4 = self.get_valid_star_atom_in_xplor(i[in_star_comp_index_4], i[in_star_atom_index_4])[0]

                for k in atom_list_1:

                    for l in atom_list_2:  # noqa: E741

                        if intra_residue_12 and l == k:  # noqa: E741
                            continue

                        for m in atom_list_3:

                            if (intra_residue_13 and m == k) or (intra_residue_23 and m == l):
                                continue

                            for n in atom_list_4:

                                if (intra_residue_14 and n == k) or (intra_residue_24 and n == l) or (intra_residue_34 and n == m):
                                    continue

                                buf = [None] * len(star_tags)

                                for data_tag in in_star_tags:

                                    auth_tag, _ = self.get_star_auth_tag(data_tag)

                                    if auth_tag is None:
                                        continue

                                    data = i[in_star_tags.index(data_tag)]

                                    if 'Entity_assembly_ID' in data_tag or 'Comp_index_ID' in data_tag:
                                        buf[star_tags.index(auth_tag)] = self_tag_map[data_tag]
                                    else:
                                        buf[star_tags.index(auth_tag)] = data

                                    if auth_tag != data_tag:

                                        data_index = star_tags.index(data_tag)

                                        if 'Entity_assembly_ID' in data_tag or 'Comp_index_ID' in data_tag:
                                            buf[data_index] = tag_map[data_tag]
                                        elif 'Comp_ID' in data_tag:
                                            buf[data_index] = data.upper()
                                        elif data_tag == '_Torsion_angle_constraint.Atom_ID_1':
                                            buf[data_index] = k
                                        elif data_tag == '_Torsion_angle_constraint.Atom_ID_2':
                                            buf[data_index] = l
                                        elif data_tag == '_Torsion_angle_constraint.Atom_ID_3':
                                            buf[data_index] = m
                                        elif data_tag == '_Torsion_angle_constraint.Atom_ID_4':
                                            buf[data_index] = n
                                        else:
                                            buf[data_index] = data

                                buf_row.append(buf)

            keys = set()

            for i in buf_row:

                key = ''
                for j in key_indices:
                    key += ' ' + str(i[j])
                key.rstrip()

                if key in keys:
                    continue

                keys.add(key)

                if index_index >= 0:
                    i[index_index] = index

                index += 1

                out_row.append(i)

        return out_row

    def nef2star_rdc_row(self, nef_tags, star_tags, loop_data):
        """ Translate rows in RDC restraint loop from NEF into NMR-STAR.
            @author: Masashi Yokochi
            @param nef_tags: list of NEF tags
            @param star_tags: list of NMR-STAR tags
            @param loop_data: loop data of NEF
            @return: rows of NMR-STAR
        """

        out_row = []

        nef_comp_index_1 = nef_tags.index('_nef_rdc_restraint.residue_name_1')
        nef_atom_index_1 = nef_tags.index('_nef_rdc_restraint.atom_name_1')
        nef_comp_index_2 = nef_tags.index('_nef_rdc_restraint.residue_name_2')
        nef_atom_index_2 = nef_tags.index('_nef_rdc_restraint.atom_name_2')

        seq_ident_tags = self.get_seq_ident_tags(nef_tags, 'nef')

        for tag in seq_ident_tags:
            chain_tag = tag['chain_tag']
            seq_tag = tag['seq_tag']

            if chain_tag.endswith('_1'):
                chain_tag_1 = chain_tag
                seq_tag_1 = seq_tag
            else:
                chain_tag_2 = chain_tag
                seq_tag_2 = seq_tag

        try:
            index_index = star_tags.index('_RDC_constraint.Index_ID')
        except ValueError:
            index_index = -1

        key_indices = [star_tags.index(j) for j in ['_RDC_constraint.Entity_assembly_ID_1',
                                                    '_RDC_constraint.Comp_index_ID_1',
                                                    '_RDC_constraint.Atom_ID_1',
                                                    '_RDC_constraint.Entity_assembly_ID_2',
                                                    '_RDC_constraint.Comp_index_ID_2',
                                                    '_RDC_constraint.Atom_ID_2']]

        id_index = nef_tags.index('_nef_rdc_restraint.restraint_id')

        id_list = sorted(set(int(i[id_index]) for i in loop_data))

        index = 1

        for id in id_list:  # pylint: disable=redefined-builtin

            in_row = [i for i in loop_data if i[id_index] == str(id)]

            buf_row = []

            for i in in_row:

                tag_map = {}
                self_tag_map = {}

                for tag in seq_ident_tags:
                    chain_tag = tag['chain_tag']
                    seq_tag = tag['seq_tag']

                    nef_chain = i[nef_tags.index(chain_tag)]
                    _nef_seq = i[nef_tags.index(seq_tag)]
                    if isinstance(_nef_seq, str) and _nef_seq not in emptyValue:
                        _nef_seq = int(_nef_seq)

                    seq_key = (nef_chain, _nef_seq)

                    try:
                        tag_map[chain_tag], tag_map[seq_tag] = self.authSeqMap[seq_key]
                        self_tag_map[chain_tag], self_tag_map[seq_tag] = self.selfSeqMap[seq_key]
                    except KeyError:
                        tag_map[chain_tag] = nef_chain
                        tag_map[seq_tag] = _nef_seq
                        self_tag_map[chain_tag] = nef_chain
                        self_tag_map[seq_tag] = _nef_seq

                intra_residue = i[nef_tags.index(chain_tag_1)] == i[nef_tags.index(chain_tag_2)]\
                    and i[nef_tags.index(seq_tag_1)] == i[nef_tags.index(seq_tag_2)]

                atom_list_1 = self.get_star_atom(i[nef_comp_index_1], i[nef_atom_index_1])[0]
                atom_list_2 = self.get_star_atom(i[nef_comp_index_2], i[nef_atom_index_2])[0]

                for k in atom_list_1:

                    for l in atom_list_2:  # noqa: E741

                        if intra_residue and l == k:  # noqa: E741
                            continue

                        buf = [None] * len(star_tags)

                        for j in nef_tags:

                            auth_tag, data_tag, _ = self.get_star_tag(j)

                            if auth_tag is None:
                                continue

                            data = i[nef_tags.index(j)]

                            if 'chain_code' in j or 'sequence_code' in j:
                                buf[star_tags.index(auth_tag)] = self_tag_map[j]
                            else:
                                buf[star_tags.index(auth_tag)] = data

                            if auth_tag != data_tag:

                                data_index = star_tags.index(data_tag)

                                if 'chain_code' in j or 'sequence_code' in j:
                                    buf[data_index] = tag_map[j]
                                elif j == '_nef_rdc_restraint.atom_name_1':
                                    buf[data_index] = k
                                elif j == '_nef_rdc_restraint.atom_name_2':
                                    buf[data_index] = l
                                else:
                                    buf[data_index] = data

                        buf_row.append(buf)

            keys = set()

            for i in buf_row:

                key = ''
                for j in key_indices:
                    key += ' ' + str(i[j])
                key.rstrip()

                if key in keys:
                    continue

                keys.add(key)

                if index_index >= 0:
                    i[index_index] = index

                index += 1

                out_row.append(i)

        return out_row

    def star2star_rdc_row(self, in_star_tags, star_tags, loop_data):
        """ Translate rows in RDC restraint loop from PyNMRSTAR data object into NMR-STAR.
            @author: Masashi Yokochi
            @param in_star_tags: list of input NMR-STAR tags
            @param star_tags: list of NMR-STAR tags
            @param loop_data: loop data of input NMR-STAR
            @return: rows of NMR-STAR
        """

        out_row = []

        in_star_comp_index_1 = in_star_tags.index('_RDC_constraint.Comp_ID_1')
        in_star_atom_index_1 = in_star_tags.index('_RDC_constraint.Atom_ID_1')
        in_star_comp_index_2 = in_star_tags.index('_RDC_constraint.Comp_ID_2')
        in_star_atom_index_2 = in_star_tags.index('_RDC_constraint.Atom_ID_2')

        seq_ident_tags = self.get_seq_ident_tags(in_star_tags, 'nmr-star')

        for tag in seq_ident_tags:
            chain_tag = tag['chain_tag']
            seq_tag = tag['seq_tag']

            if chain_tag.endswith('_1'):
                chain_tag_1 = chain_tag
                seq_tag_1 = seq_tag
            else:
                chain_tag_2 = chain_tag
                seq_tag_2 = seq_tag

        try:
            index_index = star_tags.index('_RDC_constraint.Index_ID')
        except ValueError:
            index_index = -1

        key_indices = [star_tags.index(j) for j in ['_RDC_constraint.Entity_assembly_ID_1',
                                                    '_RDC_constraint.Comp_index_ID_1',
                                                    '_RDC_constraint.Atom_ID_1',
                                                    '_RDC_constraint.Entity_assembly_ID_2',
                                                    '_RDC_constraint.Comp_index_ID_2',
                                                    '_RDC_constraint.Atom_ID_2']]

        id_index = in_star_tags.index('_RDC_constraint.ID')

        id_list = sorted(set(int(i[id_index]) for i in loop_data))

        index = 1

        for id in id_list:  # pylint: disable=redefined-builtin

            in_row = [i for i in loop_data if i[id_index] == str(id)]

            buf_row = []

            for i in in_row:

                tag_map = {}
                self_tag_map = {}

                for tag in seq_ident_tags:
                    chain_tag = tag['chain_tag']
                    seq_tag = tag['seq_tag']

                    in_star_chain = i[in_star_tags.index(chain_tag)]
                    _in_star_seq = i[in_star_tags.index(seq_tag)]
                    if isinstance(_in_star_seq, str) and _in_star_seq not in emptyValue:
                        _in_star_seq = int(_in_star_seq)

                    seq_key = (in_star_chain, _in_star_seq)

                    try:
                        tag_map[chain_tag], tag_map[seq_tag] = self.authSeqMap[seq_key]
                        self_tag_map[chain_tag], self_tag_map[seq_tag] = self.selfSeqMap[seq_key]
                    except KeyError:
                        tag_map[chain_tag] = in_star_chain
                        tag_map[seq_tag] = _in_star_seq
                        self_tag_map[chain_tag] = in_star_chain
                        self_tag_map[seq_tag] = _in_star_seq

                intra_residue = i[in_star_tags.index(chain_tag_1)] == i[in_star_tags.index(chain_tag_2)]\
                    and i[in_star_tags.index(seq_tag_1)] == i[in_star_tags.index(seq_tag_2)]

                atom_list_1 = self.get_valid_star_atom_in_xplor(i[in_star_comp_index_1], i[in_star_atom_index_1])[0]
                atom_list_2 = self.get_valid_star_atom_in_xplor(i[in_star_comp_index_2], i[in_star_atom_index_2])[0]

                for k in atom_list_1:

                    for l in atom_list_2:  # noqa: E741

                        if intra_residue and l == k:  # noqa: E741
                            continue

                        buf = [None] * len(star_tags)

                        for data_tag in in_star_tags:

                            auth_tag, _ = self.get_star_auth_tag(data_tag)

                            if auth_tag is None:
                                continue

                            data = i[in_star_tags.index(data_tag)]

                            if 'Entity_assembly_ID' in data_tag or 'Comp_index_ID' in data_tag:
                                buf[star_tags.index(auth_tag)] = self_tag_map[data_tag]
                            else:
                                buf[star_tags.index(auth_tag)] = data

                            if auth_tag != data_tag:

                                data_index = star_tags.index(data_tag)

                                if 'Entity_assembly_ID' in data_tag or 'Comp_index_ID' in data_tag:
                                    buf[data_index] = tag_map[data_tag]
                                elif 'Comp_ID' in data_tag:
                                    buf[data_index] = data.upper()
                                elif data_tag == '_RDC_constraint.Atom_ID_1':
                                    buf[data_index] = k
                                elif data_tag == '_RDC_constraint.Atom_ID_2':
                                    buf[data_index] = l
                                else:
                                    buf[data_index] = data

                        buf_row.append(buf)

            keys = set()

            for i in buf_row:

                key = ''
                for j in key_indices:
                    key += ' ' + str(i[j])
                key.rstrip()

                if key in keys:
                    continue

                keys.add(key)

                if index_index >= 0:
                    i[index_index] = index

                index += 1

                out_row.append(i)

        return out_row

    def nef2star_peak_row(self, nef_tags, star_tags, loop_data, leave_unmatched=False):
        """ Translate rows in spectral peak loop from NEF into NMR-STAR.
            @author: Masashi Yokochi
            @param nef_tags: list of NEF tags
            @param star_tags: list of NMR-STAR tags
            @param loop_data: loop data of NEF
            @return: rows of NMR-STAR
        """

        out_row = []

        nef_comp_indices = []
        nef_atom_indices = []

        seq_ident_tags = self.get_seq_ident_tags(nef_tags, 'nef')

        num_dim = len(seq_ident_tags)

        for d in range(1, num_dim + 1):
            nef_comp_indices.append(nef_tags.index(f"_nef_peak.residue_name_{d}"))
            nef_atom_indices.append(nef_tags.index(f"_nef_peak.atom_name_{d}"))

        try:
            index_index = star_tags.index('_Peak_row_format.Index_ID')
        except ValueError:
            index_index = -1

        key_indices = [star_tags.index(j) for j in [k for k in star_tags
                                                    if k.startswith('_Peak_row_format.Entity_assembly_ID')
                                                    or k.startswith('_Peak_row_format.Comp_index_ID')
                                                    or k.startswith('_Peak_row_format.Atom_ID')]]

        id_index = nef_tags.index('_nef_peak.peak_id')

        id_list = sorted(set(int(i[id_index]) for i in loop_data))

        index = 1

        for id in id_list:  # pylint: disable=redefined-builtin

            in_row = [i for i in loop_data if i[id_index] == str(id)]

            buf_row = []

            for i in in_row:

                tag_map = {}
                self_tag_map = {}

                for tag in seq_ident_tags:
                    chain_tag = tag['chain_tag']
                    seq_tag = tag['seq_tag']

                    nef_chain = i[nef_tags.index(chain_tag)]
                    _nef_seq = i[nef_tags.index(seq_tag)]
                    if isinstance(_nef_seq, str) and _nef_seq not in emptyValue:
                        _nef_seq = int(_nef_seq)

                    seq_key = (nef_chain, _nef_seq)

                    try:
                        tag_map[chain_tag], tag_map[seq_tag] = self.authSeqMap[seq_key]
                        self_tag_map[chain_tag], self_tag_map[seq_tag] = self.selfSeqMap[seq_key]
                    except KeyError:
                        tag_map[chain_tag] = nef_chain
                        tag_map[seq_tag] = _nef_seq
                        self_tag_map[chain_tag] = nef_chain
                        self_tag_map[seq_tag] = _nef_seq

                details = ''
                a = []

                for nef_comp_index, nef_atom_index in zip(nef_comp_indices, nef_atom_indices):
                    atom_list = self.get_star_atom(i[nef_comp_index], i[nef_atom_index])[0]
                    len_atom_list = len(atom_list)
                    if len_atom_list == 0:
                        atom_list.append('.')
                    elif len_atom_list > 1 and leave_unmatched:
                        details += f"{i[nef_atom_index]} -> {atom_list}, "

                    a.append(atom_list)

                if num_dim == 1:

                    for comb in itertools.product(a[0]):
                        buf_row.append(self.__nef2star_peak_row(nef_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 2:

                    for comb in itertools.product(a[0], a[1]):
                        buf_row.append(self.__nef2star_peak_row(nef_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 3:

                    for comb in itertools.product(a[0], a[1], a[2]):
                        buf_row.append(self.__nef2star_peak_row(nef_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 4:

                    for comb in itertools.product(a[0], a[1], a[2], a[3]):
                        buf_row.append(self.__nef2star_peak_row(nef_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 5:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4]):
                        buf_row.append(self.__nef2star_peak_row(nef_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 6:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5]):
                        buf_row.append(self.__nef2star_peak_row(nef_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 7:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6]):
                        buf_row.append(self.__nef2star_peak_row(nef_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 8:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7]):
                        buf_row.append(self.__nef2star_peak_row(nef_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 9:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8]):
                        buf_row.append(self.__nef2star_peak_row(nef_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 10:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9]):
                        buf_row.append(self.__nef2star_peak_row(nef_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 11:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10]):
                        buf_row.append(self.__nef2star_peak_row(nef_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 12:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11]):
                        buf_row.append(self.__nef2star_peak_row(nef_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 13:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12]):
                        buf_row.append(self.__nef2star_peak_row(nef_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 14:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12], a[13]):
                        buf_row.append(self.__nef2star_peak_row(nef_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 15:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12], a[13], a[14]):
                        buf_row.append(self.__nef2star_peak_row(nef_tags, star_tags, tag_map, self_tag_map, i, details, comb))

            keys = set()

            for i in buf_row:

                key = ''
                for j in key_indices:
                    key += ' ' + str(i[j])
                key.rstrip()

                if key in keys:
                    continue

                keys.add(key)

                if index_index >= 0:
                    i[index_index] = index

                index += 1

                out_row.append(i)

        return out_row

    def __nef2star_peak_row(self, nef_tags, star_tags, tag_map, self_tag_map, row, details, comb):
        """ Translate rows in spectral peak loop from NEF into NMR-STAR.
            @author: Masashi Yokochi
        """

        buf = [None] * len(star_tags)

        for j in nef_tags:

            auth_tag, data_tag, _ = self.get_star_tag(j)

            if auth_tag is None:
                continue

            data = row[nef_tags.index(j)]

            if 'chain_code' in j or 'sequence_code' in j:
                buf[star_tags.index(auth_tag)] = self_tag_map[j]
            else:
                buf[star_tags.index(auth_tag)] = data

            if auth_tag != data_tag:

                data_index = star_tags.index(data_tag)

                if 'chain_code' in j or 'sequence_code' in j:
                    buf[data_index] = tag_map[j]
                elif j.startswith('_nef_peak.atom_name'):
                    buf[data_index] = comb[int(j[20:]) - 1]
                else:
                    buf[data_index] = data

            if len(details) > 0:
                details_index = star_tags.index('_Peak_row_format.Details')

                buf[details_index] = details[:-2]

        return buf

    def star2nef_peak_row(self, star_tags, nef_tags, loop_data):
        """ Translate rows in spectral peak loop from NMR-STAR into NEF.
            @author: Masashi Yokochi
            @param star_tags: list of NMR-STAR tags
            @param nef_tags: list of NEF tags
            @param loop_data: loop data of NMR-STAR
            @return: rows of NEF
        """

        out_row = []

        comp_indices = []

        seq_ident_tags = self.get_seq_ident_tags(star_tags, 'nmr-star')

        num_dim = len(seq_ident_tags)

        for d in range(1, num_dim + 1):
            comp_indices.append(star_tags.index(f"_Peak_row_format.Comp_ID_{d}"))

        try:
            index_index = nef_tags.index('_nef_peak.index')
        except ValueError:
            index_index = -1

        key_indices = [nef_tags.index(j) for j in [k for k in nef_tags
                                                   if k.startswith('_nef_peak.chain_code')
                                                   or k.startswith('_nef_peak.sequence_code')
                                                   or k.startswith('_nef_peak.atom_name')]]

        id_index = star_tags.index('_Peak_row_format.ID')

        id_list = sorted(set(int(i[id_index]) for i in loop_data))

        index = 1

        for id in id_list:  # pylint: disable=redefined-builtin

            in_row = [i for i in loop_data if i[id_index] == str(id)]

            buf_row = []

            for i in in_row:

                tag_map = {}

                s = []

                for tag in seq_ident_tags:
                    chain_tag = tag['chain_tag']
                    seq_tag = tag['seq_tag']

                    star_chain = i[star_tags.index(chain_tag)]
                    _star_chain = star_chain
                    if isinstance(star_chain, str) and star_chain not in emptyValue:
                        _star_chain = int(star_chain)

                    _star_seq = i[star_tags.index(seq_tag)]
                    if isinstance(_star_seq, str) and _star_seq not in emptyValue:
                        _star_seq = int(_star_seq)

                    seq_key = (_star_chain, _star_seq)

                    try:
                        tag_map[chain_tag], tag_map[seq_tag] = self.authSeqMap[seq_key]
                    except KeyError:
                        try:
                            nef_chain = self.selfSeqMap[(_star_chain, 1)][0]
                        except KeyError:
                            if _star_chain in emptyValue or _star_chain not in self.authChainId:
                                nef_chain = _star_chain
                            else:
                                cid = self.authChainId.index(_star_chain)
                                nef_chain = indexToLetter(cid)
                        tag_map[chain_tag] = nef_chain
                        tag_map[seq_tag] = _star_seq

                    if star_chain in self.star2CifChainMapping:
                        tag_map[chain_tag] = self.star2CifChainMapping[star_chain]

                    s.append(seq_key)

                buf = [None] * len(nef_tags)

                for j in star_tags:

                    nef_tag, _ = self.get_nef_tag(j)

                    if nef_tag is None:
                        continue

                    data = i[star_tags.index(j)]

                    data_index = nef_tags.index(nef_tag)

                    if 'chain_code' in nef_tag or 'sequence_code' in nef_tag:
                        buf[data_index] = tag_map[j]
                    elif nef_tag.startswith('_nef_peak.atom_name'):
                        try:
                            if self.atomIdMap is not None:
                                buf[data_index] = self.atomIdMap[s[int(nef_tag[20:]) - 1]][data]
                        except KeyError:
                            atom_list = self.get_nef_atom(i[comp_indices[int(nef_tag[20:]) - 1]],
                                                          [{'atom_id': data, 'ambig_code': None, 'value': None}])[0]
                            if len(atom_list) > 0:
                                buf[data_index] = atom_list[0]
                            else:
                                buf[data_index] = data
                    else:
                        buf[data_index] = data

                buf_row.append(buf)

            keys = set()

            for i in buf_row:

                key = ''
                for j in key_indices:
                    key += ' ' + str(i[j])
                key.rstrip()

                if key in keys:
                    continue

                keys.add(key)

                if index_index >= 0:
                    i[index_index] = index

                index += 1

                out_row.append(i)

        return out_row

    def star2star_peak_row(self, in_star_tags, star_tags, loop_data, leave_unmatched=False):
        """ Translate rows in spectral peak loop from PyNMRSTAR data object into NMR-STAR.
            @author: Masashi Yokochi
            @param in_star_tags: list of input NMR-STAR tags
            @param star_tags: list of NMR-STAR tags
            @param loop_data: loop data of input NMR-STAR
            @return: rows of NMR-STAR
        """

        out_row = []

        in_star_comp_indices = []
        in_star_atom_indices = []

        seq_ident_tags = self.get_seq_ident_tags(in_star_tags, 'nmr-star')

        num_dim = len(seq_ident_tags)

        for d in range(1, num_dim + 1):
            in_star_comp_indices.append(in_star_tags.index(f"_Peak_row_format.Comp_ID_{d}"))
            in_star_atom_indices.append(in_star_tags.index(f"_Peak_row_format.Atom_ID_{d}"))

        try:
            index_index = star_tags.index('_Peak_row_format.Index_ID')
        except ValueError:
            index_index = -1

        key_indices = [star_tags.index(j) for j in [k for k in star_tags
                                                    if k.startswith('_Peak_row_format.Entity_assembly_ID')
                                                    or k.startswith('_Peak_row_format.Comp_index_ID')
                                                    or k.startswith('_Peak_row_format.Atom_ID')]]

        id_index = in_star_tags.index('_Peak_row_format.ID')

        id_list = sorted(set(int(i[id_index]) for i in loop_data))

        index = 1

        for id in id_list:  # pylint: disable=redefined-builtin

            in_row = [i for i in loop_data if i[id_index] == str(id)]

            buf_row = []

            for i in in_row:

                tag_map = {}
                self_tag_map = {}

                for tag in seq_ident_tags:
                    chain_tag = tag['chain_tag']
                    seq_tag = tag['seq_tag']

                    in_star_chain = i[in_star_tags.index(chain_tag)]
                    _in_star_seq = i[in_star_tags.index(seq_tag)]
                    if isinstance(_in_star_seq, str) and _in_star_seq not in emptyValue:
                        _in_star_seq = int(_in_star_seq)

                    seq_key = (in_star_chain, _in_star_seq)

                    try:
                        tag_map[chain_tag], tag_map[seq_tag] = self.authSeqMap[seq_key]
                        self_tag_map[chain_tag], self_tag_map[seq_tag] = self.selfSeqMap[seq_key]
                    except KeyError:
                        tag_map[chain_tag] = in_star_chain
                        tag_map[seq_tag] = _in_star_seq
                        self_tag_map[chain_tag] = in_star_chain
                        self_tag_map[seq_tag] = _in_star_seq

                details = ''
                a = []

                for in_star_comp_index, in_star_atom_index in zip(in_star_comp_indices, in_star_atom_indices):
                    atom_list = self.get_valid_star_atom_in_xplor(i[in_star_comp_index], i[in_star_atom_index])[0]
                    len_atom_list = len(atom_list)
                    if len_atom_list == 0:
                        atom_list.append('.')
                    elif len_atom_list > 1 and leave_unmatched:
                        details += f"{i[in_star_atom_index]} -> {atom_list}, "

                    a.append(atom_list)

                if num_dim == 1:

                    for comb in itertools.product(a[0]):
                        buf_row.append(self.__star2star_peak_row(in_star_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 2:

                    for comb in itertools.product(a[0], a[1]):
                        buf_row.append(self.__star2star_peak_row(in_star_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 3:

                    for comb in itertools.product(a[0], a[1], a[2]):
                        buf_row.append(self.__star2star_peak_row(in_star_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 4:

                    for comb in itertools.product(a[0], a[1], a[2], a[3]):
                        buf_row.append(self.__star2star_peak_row(in_star_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 5:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4]):
                        buf_row.append(self.__star2star_peak_row(in_star_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 6:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5]):
                        buf_row.append(self.__star2star_peak_row(in_star_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 7:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6]):
                        buf_row.append(self.__star2star_peak_row(in_star_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 8:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7]):
                        buf_row.append(self.__star2star_peak_row(in_star_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 9:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8]):
                        buf_row.append(self.__star2star_peak_row(in_star_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 10:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9]):
                        buf_row.append(self.__star2star_peak_row(in_star_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 11:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10]):
                        buf_row.append(self.__star2star_peak_row(in_star_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 12:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11]):
                        buf_row.append(self.__star2star_peak_row(in_star_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 13:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12]):
                        buf_row.append(self.__star2star_peak_row(in_star_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 14:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12], a[13]):
                        buf_row.append(self.__star2star_peak_row(in_star_tags, star_tags, tag_map, self_tag_map, i, details, comb))

                elif num_dim == 15:

                    for comb in itertools.product(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12], a[13], a[14]):
                        buf_row.append(self.__star2star_peak_row(in_star_tags, star_tags, tag_map, self_tag_map, i, details, comb))

            keys = set()

            for i in buf_row:

                key = ''
                for j in key_indices:
                    key += ' ' + str(i[j])
                key.rstrip()

                if key in keys:
                    continue

                keys.add(key)

                if index_index >= 0:
                    i[index_index] = index

                index += 1

                out_row.append(i)

        return out_row

    def __star2star_peak_row(self, in_star_tags, star_tags, tag_map, self_tag_map, row, details, comb):
        """ Translate rows in spectral peak loop from PyNMRSTAR data object into NMR-STAR.
            @author: Masashi Yokochi
        """

        buf = [None] * len(star_tags)

        for data_tag in in_star_tags:

            auth_tag, _ = self.get_star_auth_tag(data_tag)

            if auth_tag is None:
                continue

            data = row[in_star_tags.index(data_tag)]

            if 'Entity_assembly_ID' in data_tag or 'Comp_index_ID' in data_tag:
                buf[star_tags.index(auth_tag)] = self_tag_map[data_tag]
            else:
                buf[star_tags.index(auth_tag)] = data

            if auth_tag != data_tag:

                data_index = star_tags.index(data_tag)

                if 'Entity_assembly_ID' in data_tag or 'Comp_index_ID' in data_tag:
                    buf[data_index] = tag_map[data_tag]
                elif 'Comp_ID' in data_tag:
                    buf[data_index] = data.upper()
                elif data_tag.startswith('_Peak_row_format.Atom_ID'):
                    buf[data_index] = comb[int(data_tag[25:]) - 1]
                else:
                    buf[data_index] = data

            if len(details) > 0:
                details_index = star_tags.index('_Peak_row_format.Details')

                buf[details_index] = details[:-2]

        return buf

    def nef2star_row(self, nef_tags, star_tags, in_row):
        """ Translate rows in a loop from NEF into NMR-STAR.
            @change: rename from original translate_row() to nef2star_row() by Masashi Yokochi
            @param nef_tags: list of NEF tags
            @param star_tags: list of NMR-STAR tags
            @param in_row: rows of NEF
            @return: rows of NMR-STAR
        """

        out_row = []

        tag_map = {}
        self_tag_map = {}

        for tag in self.get_seq_ident_tags(nef_tags, 'nef'):
            chain_tag = tag['chain_tag']
            seq_tag = tag['seq_tag']

            nef_chain = in_row[nef_tags.index(chain_tag)]
            _nef_seq = in_row[nef_tags.index(seq_tag)]
            if isinstance(_nef_seq, str) and _nef_seq not in emptyValue:
                _nef_seq = int(_nef_seq)

            seq_key = (nef_chain, _nef_seq)

            try:
                tag_map[chain_tag], tag_map[seq_tag] = self.authSeqMap[seq_key]
                self_tag_map[chain_tag], self_tag_map[seq_tag] = self.selfSeqMap[seq_key]
            except KeyError:
                tag_map[chain_tag] = nef_chain
                tag_map[seq_tag] = _nef_seq
                self_tag_map[chain_tag] = nef_chain
                self_tag_map[seq_tag] = _nef_seq

        if len(nef_tags) != len(star_tags):

            out = [None] * len(star_tags)

            for j in nef_tags:

                auth_tag, data_tag, _ = self.get_star_tag(j)

                if auth_tag is None:
                    continue

                data = in_row[nef_tags.index(j)]

                if 'chain_code' in j or 'sequence_code' in j:
                    out[star_tags.index(auth_tag)] = self_tag_map[j]
                else:
                    out[star_tags.index(auth_tag)] = data

                if auth_tag != data_tag:

                    data_index = star_tags.index(data_tag)

                    if 'chain_code' in j or 'sequence_code' in j:
                        out[data_index] = tag_map[j]
                    elif data in NEF_BOOLEAN_VALUES:
                        out[data_index] = 'yes' if data in trueValue else 'no'
                    else:
                        out[data_index] = data

            out_row.append(out)

        else:
            out_row.append(in_row)

        return out_row

    def star2nef_row(self, star_tags, nef_tags, in_row):
        """ Translate rows in a loop from NMR-STAR into NEF.
            @author: Masashi Yokochi
            @param star_tags: list of NMR-STAR tags
            @param nef_tags: list of NEF tags
            @param in_row: rows of NMR-STAR
            @return: rows of NEF
        """

        out_row = []

        tag_map = {}

        for tag in self.get_seq_ident_tags(star_tags, 'nmr-star'):
            chain_tag = tag['chain_tag']
            seq_tag = tag['seq_tag']

            star_chain = in_row[star_tags.index(chain_tag)]
            _star_chain = star_chain
            if isinstance(star_chain, str) and star_chain not in emptyValue:
                _star_chain = int(star_chain)

            _star_seq = in_row[star_tags.index(seq_tag)]
            if isinstance(_star_seq, str) and _star_seq not in emptyValue:
                _star_seq = int(_star_seq)

            try:
                tag_map[chain_tag], tag_map[seq_tag] = self.authSeqMap[(_star_chain, _star_seq)]
            except KeyError:
                try:
                    nef_chain = self.selfSeqMap[(_star_chain, 1)][0]
                except KeyError:
                    if _star_chain in emptyValue or _star_chain not in self.authChainId:
                        nef_chain = _star_chain
                    else:
                        cid = self.authChainId.index(_star_chain)
                        nef_chain = indexToLetter(cid)
                tag_map[chain_tag] = nef_chain
                tag_map[seq_tag] = _star_seq

            if star_chain in self.star2CifChainMapping:
                tag_map[chain_tag] = self.star2CifChainMapping[star_chain]

        out = [None] * len(nef_tags)

        for j in star_tags:

            nef_tag, _ = self.get_nef_tag(j)

            if nef_tag is None:
                continue

            data = in_row[star_tags.index(j)]

            data_index = nef_tags.index(nef_tag)

            if 'chain_code' in nef_tag or 'sequence_code' in nef_tag:
                out[data_index] = tag_map[j]
            elif data in STAR_BOOLEAN_VALUES:
                out[data_index] = 'true' if data in trueValue else 'false'
            else:
                out[data_index] = data

        out_row.append(out)

        return out_row

    def star2star_row(self, in_star_tags, star_tags, in_row):
        """ Translate rows in a loop from PyNMRSTAR data object into NMR-STAR.
            @author: Masashi Yokochi
            @param in_star_tags: list of input NMR-STAR tags
            @param star_tags: list of NMR-STAR tags
            @param in_row: rows of input NMR-STAR
            @return: rows of NMR-STAR
        """

        out_row = []

        tag_map = {}
        self_tag_map = {}

        for tag in self.get_seq_ident_tags(in_star_tags, 'nmr-star'):
            chain_tag = tag['chain_tag']
            seq_tag = tag['seq_tag']

            in_star_chain = in_row[in_star_tags.index(chain_tag)]
            _in_star_seq = in_row[in_star_tags.index(seq_tag)]
            if isinstance(_in_star_seq, str) and _in_star_seq not in emptyValue:
                _in_star_seq = int(_in_star_seq)

            seq_key = (in_star_chain, _in_star_seq)

            try:
                tag_map[chain_tag], tag_map[seq_tag] = self.authSeqMap[seq_key]
                self_tag_map[chain_tag], self_tag_map[seq_tag] = self.selfSeqMap[seq_key]
            except KeyError:
                tag_map[chain_tag] = in_star_chain
                tag_map[seq_tag] = _in_star_seq
                self_tag_map[chain_tag] = in_star_chain
                self_tag_map[seq_tag] = _in_star_seq

        if len(in_star_tags) != len(star_tags):

            out = [None] * len(star_tags)

            for data_tag in in_star_tags:

                auth_tag, _ = self.get_star_auth_tag(data_tag)

                if auth_tag is None:
                    continue

                data = in_row[in_star_tags.index(data_tag)]

                if 'Entity_assembly_ID' in data_tag or 'Comp_index_ID' in data_tag:
                    out[star_tags.index(auth_tag)] = self_tag_map[data_tag]
                else:
                    out[star_tags.index(auth_tag)] = data

                if auth_tag != data_tag:

                    data_index = star_tags.index(data_tag)

                    if 'Entity_assembly_ID' in data_tag or 'Comp_index_ID' in data_tag:
                        out[data_index] = tag_map[data_tag]
                    elif 'Comp_ID' in data_tag:
                        out[data_index] = data.upper()
                    else:
                        out[data_index] = data

            out_row.append(out)

        else:
            out_row.append(in_row)

        return out_row

    def star2nef_peak_can(self, in_sf, out_sf):
        """ Translate NMR-STAR canonical spectral peak loops (_Peak, _Peak_general_char, _Peak.char, _Assigned_peak_chem_shift) into NEF.
            @author: Masashi Yokochi
            @param in_sf: input saveframe
            @param out_sf: output saveframe
            @return: assigned chemical shift list id
        """

        try:
            num_dim = int(in_sf.get_tag('Number_of_spectral_dimensions')[0])
        except ValueError:
            return None

        try:
            if __pynmrstar_v3_2__:
                pk_loop = in_sf.get_loop('_Peak')
            else:
                pk_loop = in_sf.get_loop_by_category('_Peak')
        except KeyError:
            return None

        try:
            if __pynmrstar_v3_2__:
                pk_gen_char_loop = in_sf.get_loop('_Peak_general_char')
            else:
                pk_gen_char_loop = in_sf.get_loop_by_category('_Peak_general_char')
        except KeyError:
            pk_gen_char_loop = None

        try:
            if __pynmrstar_v3_2__:
                pk_char_loop = in_sf.get_loop('_Peak_char')
            else:
                pk_char_loop = in_sf.get_loop_by_category('_Peak_char')
        except KeyError:
            return None

        try:
            if __pynmrstar_v3_2__:
                pk_assign_loop = in_sf.get_loop('_Assigned_peak_chem_shift')
            else:
                pk_assign_loop = in_sf.get_loop_by_category('_Assigned_peak_chem_shift')
        except KeyError:
            pk_assign_loop = None

        out_lp = pynmrstar.Loop.from_scratch()
        out_tags = ['_nef_peak.index', '_nef_peak.peak_id',
                    '_nef_peak.volume', '_nef_peak.volume_uncertainty',
                    '_nef_peak.height', '_nef_peak.height_uncertainty']
        for d in range(1, num_dim + 1):
            out_tags.append(f"_nef_peak.position_{d}")
            out_tags.append(f"_nef_peak.position_uncertainty_{d}")
        for d in range(1, num_dim + 1):
            out_tags.append(f"_nef_peak.chain_code_{d}")
            out_tags.append(f"_nef_peak.sequence_code_{d}")
            out_tags.append(f"_nef_peak.residue_name_{d}")
            out_tags.append(f"_nef_peak.atom_name_{d}")

        for tag in out_tags:
            out_lp.add_tag(tag)

        pk_tags = pk_loop.get_tag_names()

        pk_id_col = pk_tags.index('_Peak.ID')

        if pk_gen_char_loop is not None:
            pk_gen_char_tags = pk_gen_char_loop.get_tag_names()
            pk_gen_char_id_col = pk_gen_char_tags.index('_Peak_general_char.Peak_ID')
            pk_gen_char_val_col = pk_gen_char_tags.index('_Peak_general_char.Intensity_val')
            pk_gen_char_val_err_col = pk_gen_char_tags.index('_Peak_general_char.Intensity_val_err')
            pk_gen_char_type_col = pk_gen_char_tags.index('_Peak_general_char.Measurement_method')

        pk_char_tags = pk_char_loop.get_tag_names()

        pk_char_id_col = pk_char_tags.index('_Peak_char.Peak_ID')
        pk_char_dim_id_col = pk_char_tags.index('_Peak_char.Spectral_dim_ID')
        pk_char_pos_col = pk_char_tags.index('_Peak_char.Chem_shift_val')
        pk_char_pos_err_col = pk_char_tags.index('_Peak_char.Chem_shift_val_err')

        if pk_assign_loop is not None:
            pk_assign_tags = pk_assign_loop.get_tag_names()
            pk_assign_id_col = pk_assign_tags.index('_Assigned_peak_chem_shift.Peak_ID')
            pk_assign_dim_id_col = pk_assign_tags.index('_Assigned_peak_chem_shift.Spectral_dim_ID')
            pk_assign_chain_id_col = pk_assign_tags.index('_Assigned_peak_chem_shift.Entity_assembly_ID')
            pk_assign_seq_id_col = pk_assign_tags.index('_Assigned_peak_chem_shift.Comp_index_ID')
            pk_assign_comp_id_col = pk_assign_tags.index('_Assigned_peak_chem_shift.Comp_ID')
            pk_assign_atom_id_col = pk_assign_tags.index('_Assigned_peak_chem_shift.Atom_ID')
            pk_assign_cs_list_id_col = pk_assign_tags.index('_Assigned_peak_chem_shift.Assigned_chem_shift_list_ID')

        cs_list_id_set = set()

        index = 1

        for pk in pk_loop.data:

            out = [None] * len(out_tags)

            pk_id = pk[pk_id_col]

            out[0] = index
            out[1] = pk_id

            if pk_gen_char_loop is not None:
                out[2], out[3] = next(((pk_gen_char[pk_gen_char_val_col], pk_gen_char[pk_gen_char_val_err_col])
                                       for pk_gen_char in pk_gen_char_loop.data
                                       if pk_gen_char[pk_gen_char_id_col] == pk_id
                                       and pk_gen_char[pk_gen_char_type_col] == 'volume'), (None, None))

                out[4], out[5] = next(((pk_gen_char[pk_gen_char_val_col], pk_gen_char[pk_gen_char_val_err_col])
                                       for pk_gen_char in pk_gen_char_loop.data
                                       if pk_gen_char[pk_gen_char_id_col] == pk_id
                                       and pk_gen_char[pk_gen_char_type_col] == 'height'), (None, None))

            l = 6  # noqa: E741

            for d in range(1, num_dim + 1):
                out[l], out[l + 1] = next(((pk_char[pk_char_pos_col], pk_char[pk_char_pos_err_col]) for pk_char in pk_char_loop.data
                                           if pk_char[pk_char_id_col] == pk_id and int(pk_char[pk_char_dim_id_col]) == d), (None, None))
                l += 2  # noqa: E741

            if pk_assign_loop is not None:
                for d in range(1, num_dim + 1):
                    pk_assign = next((pk_assign for pk_assign in pk_assign_loop.data
                                      if pk_assign[pk_assign_id_col] == pk_id and int(pk_assign[pk_assign_dim_id_col]) == d), None)

                    if pk_assign is not None:

                        _star_chain = pk_assign[pk_assign_chain_id_col]
                        if isinstance(_star_chain, str) and _star_chain not in emptyValue:
                            _star_chain = int(_star_chain)

                        _star_seq = pk_assign[pk_assign_seq_id_col]
                        if isinstance(_star_seq, str) and _star_seq not in emptyValue:
                            _star_seq = int(_star_seq)

                        seq_key = (_star_chain, _star_seq)

                        try:
                            nef_chain, nef_seq = self.authSeqMap[seq_key]
                        except KeyError:
                            try:
                                nef_chain = self.selfSeqMap[(_star_chain, 1)][0]
                            except KeyError:
                                if _star_chain in emptyValue or _star_chain not in self.authChainId:
                                    nef_chain = _star_chain
                                else:
                                    cid = self.authChainId.index(_star_chain)
                                    nef_chain = indexToLetter(cid)
                            nef_seq = _star_seq

                        if _star_chain in self.star2CifChainMapping:
                            nef_chain = self.star2CifChainMapping[_star_chain]

                        out[l] = nef_chain
                        out[l + 1] = nef_seq

                        comp_id = pk_assign[pk_assign_comp_id_col]
                        atom_id = pk_assign[pk_assign_atom_id_col]

                        try:
                            if self.atomIdMap is not None:
                                _atom_id = self.atomIdMap[seq_key][atom_id]
                        except KeyError:
                            atom_list = self.get_nef_atom(comp_id,
                                                          [{'atom_id': atom_id, 'ambig_code': None, 'value': None}])[0]
                            if len(atom_list) > 0:
                                _atom_id = atom_list[0]
                            else:
                                _atom_id = atom_id

                        out[l + 2] = comp_id
                        out[l + 3] = _atom_id

                        cs_list_id = pk_assign[pk_assign_cs_list_id_col]

                        if cs_list_id not in emptyValue:
                            cs_list_id_set.add(cs_list_id)

                    l = l + 4  # noqa: E741

            out_lp.add_data(out)

            index += 1

        out_sf.add_loop(out_lp)

        return None if len(cs_list_id_set) == 0 else list(cs_list_id_set)[0]

    def nef_to_nmrstar(self, nef_file, star_file=None, report=None, leave_unmatched=False):
        """ Convert NEF file to NMR-STAR file.
            @param nef_file: input NEF file path
            @param star_file: output NMR-STAR file path
            @param report: NMR data processing report object (optional)
        """

        (file_path, file_name) = ntpath.split(os.path.realpath(nef_file))

        info = []
        warning = []
        error = []

        if star_file is None:
            star_file = file_path + '/' + file_name.split('.')[0] + '.str'

        is_readable, data_type, nef_data = self.read_input_file(nef_file)

        self.resolve_sf_names_for_cif(nef_data, data_type)  # DAOTHER-7389, issue #4

        try:
            star_data = pynmrstar.Entry.from_scratch(nef_data.entry_id)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            star_data = pynmrstar.Entry.from_scratch(file_name.split('.')[0])
            warning.append('Not a complete Entry')

        if not is_readable:
            error.append('Input file not readable.')
            return False, {'info': info, 'warning': warning, 'error': error}

        if data_type not in ('Entry', 'Saveframe', 'Loop'):
            error.append('File content unknown.')
            return False, {'info': info, 'warning': warning, 'error': error}

        if data_type == 'Entry':
            if len(nef_data.get_loops_by_category('nef_sequence')) == 0:  # DAOTHER-6694
                error.append("Missing mandatory '_nef_sequence' category.")
                return False, {'info': info, 'warning': warning, 'error': error}
            self.authChainId = sorted(list(set(nef_data.get_loops_by_category('nef_sequence')[0].get_tag('chain_code'))))
        elif data_type == 'Saveframe':
            self.authChainId = sorted(list(set(nef_data[0].get_tag('chain_code'))))
        else:
            self.authChainId = sorted(list(set(nef_data.get_tag('chain_code'))))

        self.authSeqMap = None
        self.selfSeqMap = None

        asm_id = 0
        cs_list_id = 0
        dist_list_id = 0
        dihed_list_id = 0
        rdc_list_id = 0
        peak_list_id = 0

        if data_type == 'Entry':

            for saveframe in nef_data:
                sf = pynmrstar.Saveframe.from_scratch(saveframe.name)

                if saveframe.category == 'nef_nmr_meta_data':
                    sf.set_tag_prefix('Entry')

                elif saveframe.category == 'nef_molecular_system':
                    asm_id += 1
                    sf.set_tag_prefix('Assembly')

                elif saveframe.category == 'nef_chemical_shift_list':
                    cs_list_id += 1
                    sf.set_tag_prefix('Assigned_chem_shift_list')

                elif saveframe.category == 'nef_distance_restraint_list':
                    dist_list_id += 1
                    sf.set_tag_prefix('Gen_dist_constraint_list')

                elif saveframe.category == 'nef_dihedral_restraint_list':
                    dihed_list_id += 1
                    sf.set_tag_prefix('Torsion_angle_constraint_list')

                elif saveframe.category == 'nef_rdc_restraint_list':
                    rdc_list_id += 1
                    sf.set_tag_prefix('RDC_constraint_list')

                elif saveframe.category == 'nef_nmr_spectrum':
                    peak_list_id += 1
                    sf.set_tag_prefix('Spectral_peak_list')

                else:
                    continue

                for tag in saveframe.tags:

                    if tag[0].lower() == 'sf_category':
                        auth_tag = self.get_star_tag(saveframe.category)[0]
                        if auth_tag is not None:
                            sf.add_tag('Sf_category', auth_tag)
                    elif saveframe.category == 'nef_distance_restraint_list' and tag[0] == 'restraint_origin':
                        nef_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_tag(nef_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1] if tag[1] not in altDistanceConstraintType['nmr-star'] else altDistanceConstraintType['nmr-star'][tag[1]])
                    elif saveframe.category == 'nef_dihedral_restraint_list' and tag[0] == 'restraint_origin':
                        nef_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_tag(nef_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1] if tag[1] not in altDihedralAngleConstraintType['nmr-star'] else altDihedralAngleConstraintType['nmr-star'][tag[1]])
                    elif saveframe.category == 'nef_rdc_restraint_list' and tag[0] == 'restraint_origin':
                        nef_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_tag(nef_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1] if tag[1] not in altRdcConstraintType['nmr-star'] else altRdcConstraintType['nmr-star'][tag[1]])
                    else:
                        nef_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_tag(nef_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1])

                has_covalent_links = any(loop for loop in saveframe if loop.category == '_nef_covalent_links')
                aux_rows = []

                for loop in saveframe:

                    lp = pynmrstar.Loop.from_scratch()
                    tags = self.get_star_loop_tags(loop.get_tag_names())

                    if len(tags) == 0:
                        continue

                    for tag in tags:
                        lp.add_tag(tag)

                    if loop.category == '_nef_sequence':
                        if self.authSeqMap is None:
                            self.authSeqMap = {}
                            self.selfSeqMap = {}
                        rows, aux_rows = self.nef2star_seq_row(loop.get_tag_names(), lp.get_tag_names(), loop.data, report)
                        for d in rows:
                            d[lp.get_tag_names().index('_Chem_comp_assembly.Assembly_ID')] = asm_id
                            lp.add_data(d)

                    elif loop.category == '_nef_covalent_links':
                        rows = self.nef2star_bond_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                        for d in rows:
                            d[lp.get_tag_names().index('_Bond.Assembly_ID')] = asm_id
                            lp.add_data(d)

                    elif loop.category == '_nef_chemical_shift':
                        rows = self.nef2star_cs_row(loop.get_tag_names(), lp.get_tag_names(), loop.data, leave_unmatched)
                        for d in rows:
                            d[lp.get_tag_names().index('_Atom_chem_shift.Assigned_chem_shift_list_ID')] = cs_list_id
                            lp.add_data(d)

                    elif loop.category == '_nef_distance_restraint':
                        rows = self.nef2star_dist_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                        for d in rows:
                            d[lp.get_tag_names().index('_Gen_dist_constraint.Gen_dist_constraint_list_ID')] = dist_list_id
                            lp.add_data(d)

                    elif loop.category == '_nef_dihedral_restraint':
                        rows = self.nef2star_dihed_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                        for d in rows:
                            d[lp.get_tag_names().index('_Torsion_angle_constraint.Torsion_angle_constraint_list_ID')] = dihed_list_id
                            lp.add_data(d)

                    elif loop.category == '_nef_rdc_restraint':
                        rows = self.nef2star_rdc_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                        for d in rows:
                            d[lp.get_tag_names().index('_RDC_constraint.RDC_constraint_list_ID')] = rdc_list_id
                            lp.add_data(d)

                    elif loop.category == '_nef_peak':
                        rows = self.nef2star_peak_row(loop.get_tag_names(), lp.get_tag_names(), loop.data, leave_unmatched)
                        for d in rows:
                            d[lp.get_tag_names().index('_Peak_row_format.Spectral_peak_list_ID')] = peak_list_id
                            lp.add_data(d)

                    else:

                        for data in loop.data:

                            if loop.category == '_nef_spectrum_dimension':
                                rows = self.nef2star_row(loop.get_tag_names(), lp.get_tag_names(), data)
                                for d in rows:
                                    d[lp.get_tag_names().index('_Spectral_dim.Spectral_peak_list_ID')] = peak_list_id
                                    lp.add_data(d)

                            elif loop.category == '_nef_spectrum_dimension_transfer':
                                rows = self.nef2star_row(loop.get_tag_names(), lp.get_tag_names(), data)
                                for d in rows:
                                    d[lp.get_tag_names().index('_Spectral_dim_transfer.Spectral_peak_list_ID', )] = peak_list_id
                                    lp.add_data(d)

                            else:
                                rows = self.nef2star_row(loop.get_tag_names(), lp.get_tag_names(), data)
                                for d in rows:
                                    lp.add_data(d)

                    sf.add_loop(lp)

                    if len(aux_rows) > 0 and ((loop.category == '_nef_sequence' and not has_covalent_links)
                                              or (loop.category == '_nef_covalent_links' and has_covalent_links)):
                        lp = pynmrstar.Loop.from_scratch()
                        for _tag in ENTITY_DELETED_ATOM_ITEMS:
                            lp.add_tag('_Entity_deleted_atom.' + _tag)
                        for d in aux_rows:
                            d[lp.get_tag_names().index('_Entity_deleted_atom.Assembly_ID')] = asm_id
                            lp.add_data(d)
                        sf.add_loop(lp)

                if saveframe.category == 'nef_nmr_meta_data':
                    sf.add_tag('NMR_STAR_version', NMR_STAR_VERSION)

                    try:
                        if __pynmrstar_v3_2__:
                            loop = sf.get_loop('_Software_applied_methods')
                        else:
                            loop = sf.get_loop_by_category('_Software_applied_methods')
                        row = []
                        for t in loop.tags:
                            if t == 'Software_name':
                                row.append(self.__class__.__name__)
                            elif t == 'Script_name':
                                row.append(self.nef_to_nmrstar.__name__)
                            else:
                                row.append('.')
                        loop.add_data(row)
                    except KeyError:
                        pass

                elif saveframe.category == 'nef_molecular_system':
                    sf.add_tag('ID', asm_id)

                elif saveframe.category == 'nef_chemical_shift_list':
                    sf.add_tag('ID', cs_list_id)

                elif saveframe.category == 'nef_distance_restraint_list':
                    sf.add_tag('ID', dist_list_id)

                elif saveframe.category == 'nef_dihedral_restraint_list':
                    sf.add_tag('ID', dihed_list_id)

                elif saveframe.category == 'nef_rdc_restraint_list':
                    sf.add_tag('ID', rdc_list_id)

                elif saveframe.category == 'nef_nmr_spectrum':
                    sf.add_tag('ID', peak_list_id)

                else:
                    continue

                star_data.add_saveframe(sf)

        elif data_type in ('Saveframe', 'Loop'):

            if data_type == 'Saveframe':
                saveframe = nef_data
                sf = pynmrstar.Saveframe.from_scratch(saveframe.name)

                if saveframe.category == 'nef_nmr_meta_data':
                    sf.set_tag_prefix('Entry')

                elif saveframe.category == 'nef_molecular_system':
                    asm_id += 1
                    sf.set_tag_prefix('Assembly')

                elif saveframe.category == 'nef_chemical_shift_list':
                    cs_list_id += 1
                    sf.set_tag_prefix('Assigned_chem_shift_list')

                elif saveframe.category == 'nef_distance_restraint_list':
                    dist_list_id += 1
                    sf.set_tag_prefix('Gen_dist_constraint_list')

                elif saveframe.category == 'nef_dihedral_restraint_list':
                    dihed_list_id += 1
                    sf.set_tag_prefix('Torsion_angle_constraint_list')

                elif saveframe.category == 'nef_rdc_restraint_list':
                    rdc_list_id += 1
                    sf.set_tag_prefix('RDC_constraint_list')

                elif saveframe.category == 'nef_nmr_spectrum':
                    peak_list_id += 1
                    sf.set_tag_prefix('Spectral_peak_list')

                for tag in saveframe.tags:

                    if tag[0].lower() == 'sf_category':
                        auth_tag = self.get_star_tag(saveframe.category)[0]
                        if auth_tag is not None:
                            sf.add_tag('Sf_category', auth_tag)
                    elif saveframe.category == 'nef_distance_restraint_list' and tag[0] == 'restraint_origin':
                        nef_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_tag(nef_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1] if tag[1] not in altDistanceConstraintType['nmr-star'] else altDistanceConstraintType['nmr-star'][tag[1]])
                    elif saveframe.category == 'nef_dihedral_restraint_list' and tag[0] == 'restraint_origin':
                        nef_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_tag(nef_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1] if tag[1] not in altDihedralAngleConstraintType['nmr-star'] else altDihedralAngleConstraintType['nmr-star'][tag[1]])
                    elif saveframe.category == 'nef_rdc_restraint_list' and tag[0] == 'restraint_origin':
                        nef_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_tag(nef_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1] if tag[1] not in altRdcConstraintType['nmr-star'] else altRdcConstraintType['nmr-star'][tag[1]])
                    else:
                        nef_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_tag(nef_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1])

            else:

                if nef_data.category == '_nef_program_script':
                    sf = pynmrstar.Saveframe.from_scratch('entry')
                    sf.set_tag_prefix('Entry')
                    sf.add_tag('Sf_category', 'entry_information')

                elif nef_data.category == '_audit':  # DAOTHER-6327
                    sf = pynmrstar.Saveframe.from_scratch('entry')
                    sf.set_tag_prefix('Entry')
                    sf.add_tag('Sf_category', 'entry_information')

                elif nef_data.category == '_nef_sequence':
                    asm_id += 1
                    sf = pynmrstar.Saveframe.from_scratch('assembly')
                    sf.set_tag_prefix('Assembly')
                    sf.add_tag('Sf_category', 'assembly')

                elif nef_data.category == '_nef_chemical_shift':
                    cs_list_id += 1
                    sf = pynmrstar.Saveframe.from_scratch(f"assigned_chem_shift_list_{cs_list_id}")
                    sf.set_tag_prefix('Assigned_chem_shift_list')
                    sf.add_tag('Sf_category', 'assigned_chemical_shifts')

                elif nef_data.category == '_nef_distance_restraint':
                    dist_list_id += 1
                    sf = pynmrstar.Saveframe.from_scratch(f"gen_dist_constraint_list_{dist_list_id}")
                    sf.set_tag_prefix('Gen_dist_constraint_list')
                    sf.add_tag('Sf_category', 'general_distance_constraints')

                elif nef_data.category == '_nef_dihedral_restraint':
                    dihed_list_id += 1
                    sf = pynmrstar.Saveframe.from_scratch(f"torsion_angle_constraint_list_{dihed_list_id}")
                    sf.set_tag_prefix('Torsion_angle_constraint_list')
                    sf.add_tag('Sf_category', 'torsion_angle_constraints')

                elif nef_data.category == '_nef_rdc_restraint':
                    rdc_list_id += 1
                    sf = pynmrstar.Saveframe.from_scratch(f"rdc_constraint_list_{rdc_list_id}")
                    sf.set_tag_prefix('RDC_constraint_list')
                    sf.add_tag('Sf_category', 'RDC_constraints')

                elif nef_data.category == '_nef_peak':
                    peak_list_id += 1
                    sf = pynmrstar.Saveframe.from_scratch(f"spectral_peak_list_{peak_list_id}")
                    sf.set_tag_prefix('Spectral_peak_list')
                    sf.add_tag('Sf_category', 'spectral_peak_list')

                else:
                    error.append(f"Loop category {nef_data.category} is not supported.")
                    return False, {'info': info, 'warning': warning, 'error': error}

                sf.add_tag('Sf_framecode', sf.name)

                saveframe = [nef_data]

            has_covalent_links = any(loop for loop in saveframe if loop.category == '_nef_covalent_links')
            aux_rows = []

            for loop in saveframe:

                lp = pynmrstar.Loop.from_scratch()
                tags = self.get_star_loop_tags(loop.get_tag_names())

                if len(tags) == 0:
                    continue

                for tag in tags:
                    lp.add_tag(tag)

                if loop.category == '_nef_sequence':
                    if self.authSeqMap is None:
                        self.authSeqMap = {}
                        self.selfSeqMap = {}
                    rows, aux_rows = self.nef2star_seq_row(loop.get_tag_names(), lp.get_tag_names(), loop.data, report)
                    for d in rows:
                        d[lp.get_tag_names().index('_Chem_comp_assembly.Assembly_ID')] = asm_id
                        lp.add_data(d)

                elif loop.category == '_nef_covalent_links':
                    rows = self.nef2star_bond_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                    for d in rows:
                        d[lp.get_tag_names().index('_Bond.Assembly_ID')] = asm_id
                        lp.add_data(d)

                elif loop.category == '_nef_chemical_shift':
                    rows = self.nef2star_cs_row(loop.get_tag_names(), lp.get_tag_names(), loop.data, leave_unmatched)
                    for d in rows:
                        d[lp.get_tag_names().index('_Atom_chem_shift.Assigned_chem_shift_list_ID')] = cs_list_id
                        lp.add_data(d)

                elif loop.category == '_nef_distance_restraint':
                    rows = self.nef2star_dist_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                    for d in rows:
                        d[lp.get_tag_names().index('_Gen_dist_constraint.Gen_dist_constraint_list_ID')] = dist_list_id
                        lp.add_data(d)

                elif loop.category == '_nef_dihedral_restraint':
                    rows = self.nef2star_dihed_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                    for d in rows:
                        d[lp.get_tag_names().index('_Torsion_angle_constraint.Torsion_angle_constraint_list_ID')] = dihed_list_id
                        lp.add_data(d)

                elif loop.category == '_nef_rdc_restraint':
                    rows = self.nef2star_rdc_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                    for d in rows:
                        d[lp.get_tag_names().index('_RDC_constraint.RDC_constraint_list_ID')] = rdc_list_id
                        lp.add_data(d)

                elif loop.category == '_nef_peak':
                    rows = self.nef2star_peak_row(loop.get_tag_names(), lp.get_tag_names(), loop.data, leave_unmatched)
                    for d in rows:
                        d[lp.get_tag_names().index('_Peak_row_format.Spectral_peak_list_ID')] = peak_list_id
                        lp.add_data(d)

                else:

                    for data in loop.data:

                        if loop.category == '_nef_spectrum_dimension':
                            rows = self.nef2star_row(loop.get_tag_names(), lp.get_tag_names(), data)
                            for d in rows:
                                d[lp.get_tag_names().index('_Spectral_dim.Spectral_peak_list_ID')] = peak_list_id
                                lp.add_data(d)

                        elif loop.category == '_nef_spectrum_dimension_transfer':
                            rows = self.nef2star_row(loop.get_tag_names(), lp.get_tag_names(), data)
                            for d in rows:
                                d[lp.get_tag_names().index('_Spectral_dim_transfer.Spectral_peak_list_ID', )] = peak_list_id
                                lp.add_data(d)

                        else:
                            rows = self.nef2star_row(loop.get_tag_names(), lp.get_tag_names(), data)
                            for d in rows:
                                lp.add_data(d)

                sf.add_loop(lp)

                if len(aux_rows) > 0 and ((loop.category == '_nef_sequence' and not has_covalent_links)
                                          or (loop.category == '_nef_covalent_links' and has_covalent_links)):
                    lp = pynmrstar.Loop.from_scratch()
                    for _tag in ENTITY_DELETED_ATOM_ITEMS:
                        lp.add_tag('_Entity_deleted_atom.' + _tag)
                    for d in aux_rows:
                        d[lp.get_tag_names().index('_Entity_deleted_atom.Assembly_ID')] = asm_id
                        lp.add_data(d)
                    sf.add_loop(lp)

            if sf.category == 'nef_nmr_meta_data':
                sf.add_tag('NMR_STAR_version', NMR_STAR_VERSION)

                try:
                    if __pynmrstar_v3_2__:
                        loop = sf.get_loop('_Software_applied_methods')
                    else:
                        loop = sf.get_loop_by_category('_Software_applied_methods')
                    row = []
                    for t in loop.tags:
                        if t == 'Software_name':
                            row.append(self.__class__.__name__)
                        elif t == 'Script_name':
                            row.append(self.nef_to_nmrstar.__name__)
                        else:
                            row.append('.')
                    loop.add_data(row)
                except KeyError:
                    pass

            elif sf.category == 'nef_molecular_system':
                sf.add_tag('ID', asm_id)

            elif sf.category == 'nef_chemical_shift_list':
                sf.add_tag('ID', cs_list_id)

            elif sf.category == 'nef_distance_restraint_list':
                sf.add_tag('ID', dist_list_id)

            elif sf.category == 'nef_dihedral_restraint_list':
                sf.add_tag('ID', dihed_list_id)

            elif sf.category == 'nef_rdc_restraint_list':
                sf.add_tag('ID', rdc_list_id)

            elif sf.category == 'nef_nmr_spectrum':
                sf.add_tag('ID', peak_list_id)

            star_data.add_saveframe(sf)

        # star_data.normalize() # do not invoke normalize() to preserve author provided Peak_row_format.ID using pynmrstar v3 library

        if __pynmrstar_v3__:
            star_data.write_to_file(star_file, skip_empty_loops=True, skip_empty_tags=False)
        else:
            star_data.write_to_file(star_file)

        info.append(f"File {star_file} successfully written.")

        return True, {'info': info, 'warning': warning, 'error': error}

    def nmrstar_to_nef(self, star_file, nef_file=None, report=None):
        """ Convert NMR-STAR file to NEF file.
            @author: Masashi Yokochi
            @param star_file: input NMR-STAR file path
            @param nef_file: output NEF file path
            @param report: NMR data processing report object (optional)
        """

        (file_path, file_name) = ntpath.split(os.path.realpath(star_file))

        info = []
        warning = []
        error = []

        if nef_file is None:
            nef_file = file_path + '/' + file_name.split('.')[0] + '.nef'

        is_readable, data_type, star_data = self.read_input_file(star_file)

        self.resolve_sf_names_for_cif(star_data, data_type)  # DAOTHER-7389, issue #4

        try:
            nef_data = pynmrstar.Entry.from_scratch(star_data.entry_id)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            nef_data = pynmrstar.Entry.from_scratch(file_name.split('.')[0])
            warning.append('Not a complete Entry.')

        if not is_readable:
            error.append('Input file not readable.')
            return False, {'info': info, 'warning': warning, 'error': error}

        if data_type not in ('Entry', 'Saveframe', 'Loop'):
            error.append('File content unknown.')
            return False, {'info': info, 'warning': warning, 'error': error}

        asm_id = 0
        cs_list_id = 0
        dist_list_id = 0
        dihed_list_id = 0
        rdc_list_id = 0
        peak_list_id = 0

        if data_type == 'Entry':
            if len(star_data.get_loops_by_category('Chem_comp_assembly')) == 0:  # DAOTHER-6694
                error.append("Missing mandatory '_Chem_comp_assembly' category.")
                return False, {'info': info, 'warning': warning, 'error': error}
            self.authChainId = sorted(list(set(star_data.get_loops_by_category('Chem_comp_assembly')[0].get_tag('Entity_assembly_ID'))),
                                      key=lambda x: float(re.sub(r'[^\d]+', '', x)))
        elif data_type == 'Saveframe':
            self.authChainId = sorted(list(set(star_data[0].get_tag('Entity_assembly_ID'))),
                                      key=lambda x: float(re.sub(r'[^\d]+', '', x)))
        else:
            self.authChainId = sorted(list(set(star_data.get_tag('Entity_assembly_ID'))),
                                      key=lambda x: float(re.sub(r'[^\d]+', '', x)))

        self.authSeqMap = None
        self.selfSeqMap = None
        self.atomIdMap = None

        if data_type == 'Entry':

            for saveframe in star_data:
                sf = pynmrstar.Saveframe.from_scratch(saveframe.name)

                nef_tag, _ = self.get_nef_tag(saveframe.category)

                if nef_tag is None:
                    continue

                sf.set_tag_prefix(nef_tag)

                sf.add_tag('sf_category', nef_tag)
                sf.add_tag('sf_framecode', saveframe.name)

                for tag in saveframe.tags:
                    tag_name = tag[0].lower()
                    if tag_name in ('sf_category', 'sf_framecode'):
                        continue
                    if saveframe.category == 'entry_information':
                        if tag_name == 'source_data_format':
                            sf.add_tag('format_name', NEF_FORMAT_NAME)
                        elif tag_name == 'source_data_format_version':
                            sf.add_tag('format_version', NEF_VERSION)
                        else:
                            nef_tag, _ = self.get_nef_tag(saveframe.tag_prefix + '.' + tag[0])
                            if nef_tag is not None:
                                sf.add_tag(nef_tag, tag[1])
                    elif saveframe.category == 'general_distance_constraints' and tag_name == 'constraint_type':
                        nef_tag, _ = self.get_nef_tag(saveframe.tag_prefix + '.' + tag[0])
                        if nef_tag is not None:
                            sf.add_tag(nef_tag, tag[1] if tag[1] not in altDistanceConstraintType['nef'] else altDistanceConstraintType['nef'][tag[1]])
                    elif saveframe.category == 'torsion_angle_constraints' and tag_name == 'constraint_type':
                        nef_tag, _ = self.get_nef_tag(saveframe.tag_prefix + '.' + tag[0])
                        if nef_tag is not None:
                            sf.add_tag(nef_tag, tag[1] if tag[1] not in altDihedralAngleConstraintType['nef'] else altDihedralAngleConstraintType['nef'][tag[1]])
                    elif saveframe.category == 'RDC_constraints' and tag_name == 'constraint_type':
                        nef_tag, _ = self.get_nef_tag(saveframe.tag_prefix + '.' + tag[0])
                        if nef_tag is not None:
                            sf.add_tag(nef_tag, tag[1] if tag[1] not in altRdcConstraintType['nef'] else altRdcConstraintType['nef'][tag[1]])
                    else:
                        nef_tag, _ = self.get_nef_tag(saveframe.tag_prefix + '.' + tag[0])
                        if nef_tag is not None:
                            sf.add_tag(nef_tag, tag[1])

                entity_del_atom_loop = next((loop for loop in saveframe if loop.category == '_Entity_deleted_atom'), None)

                has_pk_can_format = False
                has_pk_row_format = False

                for loop in saveframe:

                    try:

                        lp = pynmrstar.Loop.from_scratch()
                        tags = self.get_nef_loop_tags(loop.get_tag_names())
                        tag_set = set(tags)
                        if len(tags) > len(tag_set):
                            tags = list(tag_set)

                        if len(tags) == 0:
                            continue

                        for tag in tags:
                            lp.add_tag(tag)

                        if loop.category == '_Chem_comp_assembly':
                            if self.authSeqMap is None:
                                self.authSeqMap = {}
                                self.selfSeqMap = {}
                            rows = self.star2nef_seq_row(loop.get_tag_names(), lp.get_tag_names(), loop.data, report,
                                                         None if entity_del_atom_loop is None else entity_del_atom_loop)
                            for d in rows:
                                lp.add_data(d)

                        elif loop.category == '_Atom_chem_shift':
                            if self.atomIdMap is None:
                                self.atomIdMap = {}

                            rows = self.star2nef_cs_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                            for d in rows:
                                lp.add_data(d)

                        elif loop.category == '_Gen_dist_constraint':
                            rows = self.star2nef_dist_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                            for d in rows:
                                lp.add_data(d)

                        elif loop.category == '_Peak_row_format':
                            rows = self.star2nef_peak_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                            for d in rows:
                                lp.add_data(d)
                            has_pk_row_format = True

                        elif len(tags) > 0:
                            for data in loop.data:
                                rows = self.star2nef_row(loop.get_tag_names(), lp.get_tag_names(), data)
                                for d in rows:
                                    lp.add_data(d)

                        elif loop.category == '_Peak':
                            has_pk_can_format = True

                        sf.add_loop(lp)

                    except ValueError:
                        pass

                if saveframe.category == 'entry_information':
                    has_format_name = False
                    has_format_ver = False
                    for tags in sf.tags:
                        if tags[0] == 'format_name':
                            has_format_name = True
                        elif tags[0] == 'format_version':
                            has_format_ver = True

                    if not has_format_name:
                        sf.add_tag('format_name', NEF_FORMAT_NAME)
                    if not has_format_ver:
                        sf.add_tag('format_version', NEF_VERSION)

                    try:
                        if __pynmrstar_v3_2__:
                            loop = sf.get_loop('_nef_program_script')
                        else:
                            loop = sf.get_loop_by_category('_nef_program_script')
                        row = []
                        for t in loop.tags:
                            if t == 'program_name':
                                row.append(self.__class__.__name__)
                            elif t == 'script_name':
                                row.append(self.nmrstar_to_nef.__name__)
                            else:
                                row.append('.')
                        loop.add_data(row)
                    except KeyError:
                        pass

                if saveframe.category == 'spectral_peak_list' and has_pk_can_format and not has_pk_row_format:
                    cs_list_id = self.star2nef_peak_can(saveframe, sf)
                    if cs_list_id is not None and (len(sf.get_tag('chemical_shift_list')) == 0 or sf.get_tag('chemical_shift_list') in emptyValue):
                        for cs_sf in star_data:
                            if cs_sf.get_tag('Sf_category')[0] == 'assigned_chemical_shifts' and cs_sf.get_tag('ID')[0] == cs_list_id and cs_sf.name not in emptyValue:
                                if len(sf.get_tag('chemical_shift_list')) == 0:
                                    sf.add_tag('chemical_shift_list', cs_sf.name)
                                else:
                                    sf.tags[sf.tags.index('chemical_shift_list')][1] = cs_sf.name
                                break

                nef_data.add_saveframe(sf)

        elif data_type in ('Saveframe', 'Loop'):

            if data_type == 'Saveframe':
                saveframe = star_data
                sf = pynmrstar.Saveframe.from_scratch(saveframe.name)

                nef_tag, _ = self.get_nef_tag(saveframe.category)

                if nef_tag is not None:

                    sf.set_tag_prefix(nef_tag)

                    sf.add_tag('sf_category', nef_tag)
                    sf.add_tag('sf_framecode', saveframe.name)

                    for tag in saveframe.tags:
                        tag_name = tag[0].lower()
                        if tag_name in ('sf_category', 'sf_framecode'):
                            continue
                        if saveframe.category == 'entry_information':
                            if tag_name == 'source_data_format':
                                sf.add_tag('format_name', NEF_FORMAT_NAME)
                            elif tag_name == 'source_data_format_version':
                                sf.add_tag('format_version', NEF_VERSION)
                            else:
                                nef_tag, _ = self.get_nef_tag(saveframe.tag_prefix + '.' + tag[0])
                                if nef_tag is not None:
                                    sf.add_tag(nef_tag, tag[1])
                        elif saveframe.category == 'general_distance_constraints' and tag_name == 'constraint_type':
                            nef_tag, _ = self.get_nef_tag(saveframe.tag_prefix + '.' + tag[0])
                            if nef_tag is not None:
                                sf.add_tag(nef_tag, tag[1] if tag[1] not in altDistanceConstraintType['nef'] else altDistanceConstraintType['nef'][tag[1]])
                        elif saveframe.category == 'torsion_angle_constraints' and tag_name == 'constraint_type':
                            nef_tag, _ = self.get_nef_tag(saveframe.tag_prefix + '.' + tag[0])
                            if nef_tag is not None:
                                sf.add_tag(nef_tag, tag[1] if tag[1] not in altDihedralAngleConstraintType['nef'] else altDihedralAngleConstraintType['nef'][tag[1]])
                        elif saveframe.category == 'RDC_constraints' and tag_name == 'constraint_type':
                            nef_tag, _ = self.get_nef_tag(saveframe.tag_prefix + '.' + tag[0])
                            if nef_tag is not None:
                                sf.add_tag(nef_tag, tag[1] if tag[1] not in altRdcConstraintType['nef'] else altRdcConstraintType['nef'][tag[1]])
                        else:
                            nef_tag, _ = self.get_nef_tag(saveframe.tag_prefix + '.' + tag[0])
                            if nef_tag is not None:
                                sf.add_tag(nef_tag, tag[1])

            else:

                if star_data.category == '_Software_applied_methods':
                    sf = pynmrstar.Saveframe.from_scratch('nef_nmr_meta_data')
                    sf.set_tag_prefix('nef_nmr_meta_data')
                    sf.add_tag('sf_category', 'nef_molecular_system')

                elif star_data.category == '_Assembly':
                    asm_id += 1
                    sf = pynmrstar.Saveframe.from_scratch('nef_molecular_system')
                    sf.set_tag_prefix('nef_molecular_system')
                    sf.add_tag('sf_category', 'nef_molecular_system')

                elif star_data.category == '_Atom_chem_shift':
                    cs_list_id += 1
                    sf = pynmrstar.Saveframe.from_scratch(f"nef_chemical_shift_list_{cs_list_id}")
                    sf.set_tag_prefix('nef_chemical_shift_list')
                    sf.add_tag('sf_category', 'nef_chemical_shift_list')

                elif star_data.category == '_Gen_dist_constraint':
                    dist_list_id += 1
                    sf = pynmrstar.Saveframe.from_scratch(f"nef_distance_restraint_list_{dist_list_id}")
                    sf.set_tag_prefix('nef_distance_restraint_list')
                    sf.add_tag('sf_category', 'nef_distance_restraint_list')

                elif star_data.category == '_Torsion_angle_constraint':
                    dihed_list_id += 1
                    sf = pynmrstar.Saveframe.from_scratch(f"nef_dihedral_restraint_list_{dihed_list_id}")
                    sf.set_tag_prefix('nef_dihedral_restraint_list')
                    sf.add_tag('sf_category', 'nef_dihedral_restraint_list')

                elif star_data.category == '_RDC_constraint':
                    rdc_list_id += 1
                    sf = pynmrstar.Saveframe.from_scratch(f"nef_rdc_restraint_list_{rdc_list_id}")
                    sf.set_tag_prefix('nef_rdc_restraint_list')
                    sf.add_tag('sf_category', 'nef_rdc_restraint_list')

                elif star_data.category == '_Peak_row_format':
                    peak_list_id += 1
                    sf = pynmrstar.Saveframe.from_scratch(f"nef_nmr_spectrum_{peak_list_id}")
                    sf.set_tag_prefix('nef_nmr_spectrum')
                    sf.add_tag('sf_category', 'nef_nmr_spectrum')

                else:
                    error.append(f"Loop category {star_data.category} is not supported.")
                    return False, {'info': info, 'warning': warning, 'error': error}

                sf.add_tag('sf_framecode', sf.name)

                saveframe = [star_data]

            entity_del_atom_loop = next((loop for loop in saveframe if loop.category == '_Entity_deleted_atom'), None)

            has_pk_can_format = False
            has_pk_row_format = False

            for loop in saveframe:

                try:

                    lp = pynmrstar.Loop.from_scratch()
                    tags = self.get_nef_loop_tags(loop.get_tag_names())
                    tag_set = set(tags)
                    if len(tags) > len(tag_set):
                        tags = list(tag_set)

                    if len(tags) == 0:
                        continue

                    for tag in tags:
                        lp.add_tag(tag)

                    if loop.category == '_Chem_comp_assembly':
                        if self.authSeqMap is None:
                            self.authSeqMap = {}
                            self.selfSeqMap = {}
                        rows = self.star2nef_seq_row(loop.get_tag_names(), lp.get_tag_names(), loop.data, report,
                                                     None if entity_del_atom_loop is None else entity_del_atom_loop)
                        for d in rows:
                            lp.add_data(d)

                    elif loop.category == '_Atom_chem_shift':
                        if self.atomIdMap is None:
                            self.atomIdMap = {}

                        rows = self.star2nef_cs_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                        for d in rows:
                            lp.add_data(d)

                    elif loop.category == '_Gen_dist_constraint':
                        rows = self.star2nef_dist_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                        for d in rows:
                            lp.add_data(d)

                    elif loop.category == '_Peak_row_format':
                        rows = self.star2nef_peak_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                        for d in rows:
                            lp.add_data(d)
                        has_pk_row_format = True

                    elif len(tags) > 0:
                        for data in loop.data:
                            rows = self.star2nef_row(loop.get_tag_names(), lp.get_tag_names(), data)
                            for d in rows:
                                lp.add_data(d)

                    elif loop.category == '_Peak':
                        has_pk_can_format = True

                    sf.add_loop(lp)

                except ValueError:
                    pass

            if sf.category == 'entry_information':
                has_format_name = False
                has_format_ver = False
                for tags in sf.tags:
                    if tags[0] == 'format_name':
                        has_format_name = True
                    elif tags[0] == 'format_version':
                        has_format_ver = True

                if not has_format_name:
                    sf.add_tag('format_name', NEF_FORMAT_NAME)
                if not has_format_ver:
                    sf.add_tag('format_version', NEF_VERSION)

                try:
                    if __pynmrstar_v3_2__:
                        loop = sf.get_loop('_nef_program_script')
                    else:
                        loop = sf.get_loop_by_category('_nef_program_script')
                    row = []
                    for t in loop.tags:
                        if t == 'program_name':
                            row.append(self.__class__.__name__)
                        elif t == 'script_name':
                            row.append(self.nmrstar_to_nef.__name__)
                        else:
                            row.append('.')
                    loop.add_data(row)
                except KeyError:
                    pass

            if sf.category == 'spectral_peak_list' and has_pk_can_format and not has_pk_row_format:
                cs_list_id = self.star2nef_peak_can(saveframe, sf)
                if cs_list_id is not None and (len(sf.get_tag('chemical_shift_list')) == 0
                                               or sf.get_tag('chemical_shift_list') in emptyValue):
                    for cs_sf in star_data:
                        if cs_sf.get_tag('Sf_category')[0] == 'assigned_chemical_shifts' and cs_sf.get_tag('ID')[0] == cs_list_id and cs_sf.name not in emptyValue:
                            if len(sf.get_tag('chemical_shift_list')) == 0:
                                sf.add_tag('chemical_shift_list', cs_sf.name)
                            else:
                                sf.tags[sf.tags.index('chemical_shift_list')][1] = cs_sf.name
                            break

            nef_data.add_saveframe(sf)

        if __pynmrstar_v3__:
            nef_data.write_to_file(nef_file, skip_empty_loops=True, skip_empty_tags=False)
        else:
            nef_data.write_to_file(nef_file)

        info.append(f"File {nef_file} successfully written.")

        return True, {'info': info, 'warning': warning, 'error': error}

    def star_data_to_nmrstar(self, data_type, star_data, output_file_path=None, input_source_id=None, report=None, leave_unmatched=False):
        """ Convert PyNMRSTAR data object (Entry/Saveframe/Loop) to complete NMR-STAR (Entry) file.
            @author: Masashi Yokochi
            @param data_type: input PyNMRSTAR data object type, one of Entry/Saveframe/Loop
            @param star_data: input PyNMRSTAR data object
            @param output_file_path: output NMR-STAR file path
            @param input_source_id: input source id of NMR data processing report
            @param report: NMR data processing report object
        """

        _, file_name = ntpath.split(os.path.realpath(output_file_path))

        info = []
        warning = []
        error = []

        try:
            out_data = pynmrstar.Entry.from_scratch(star_data.entry_id)
        except:  # AttributeError:  # noqa: E722 pylint: disable=bare-except
            out_data = pynmrstar.Entry.from_scratch(file_name.split('.')[0])
            warning.append('Not a complete Entry.')

        if star_data is None or report is None:
            error.append('Input file not readable.')
            return False, {'info': info, 'warning': warning, 'error': error}

        if data_type not in ('Entry', 'Saveframe', 'Loop'):
            error.append('Data type unknown.')
            return False, {'info': info, 'warning': warning, 'error': error}

        polymer_sequence = report.getPolymerSequenceByInputSrcId(input_source_id)

        if polymer_sequence is None:
            error.append('Common polymer sequence does not exist.')
            return False, {'info': info, 'warning': warning, 'error': error}

        self.authChainId = sorted([ps['chain_id'] for ps in polymer_sequence])
        self.authSeqMap = {}
        self.selfSeqMap = {}

        for star_chain in self.authChainId:

            ps = next(ps for ps in polymer_sequence if ps['chain_id'] == star_chain)

            if len(ps['seq_id']) == 0:
                continue

            cif_chain = cif_ps = None
            if report is not None:
                seq_align = report.getSequenceAlignmentWithNmrChainId(star_chain)
                if seq_align is not None:
                    cif_chain = seq_align['test_chain_id']  # label_asym_id
                    cif_ps = report.getModelPolymerSequenceOf(cif_chain, label_scheme=False)
                    if cif_ps is not None:
                        cif_chain = cif_ps['auth_chain_id']  # auth_asym_id

            # self.star2CifChainMapping[star_chain] = cif_chain

            for star_seq in ps['seq_id']:

                _cif_seq = None
                if cif_chain is not None:
                    try:
                        _cif_seq = seq_align['test_seq_id'][seq_align['ref_seq_id'].index(star_seq)]  # label_seq_id
                        if cif_ps is not None:
                            _cif_seq = cif_ps['auth_seq_id'][cif_ps['seq_id'].index(_cif_seq)]  # auth_seq_id
                    except:  # noqa: E722 pylint: disable=bare-except
                        pass

                self.authSeqMap[(star_chain, star_seq)] = (star_chain, star_seq)
                self.selfSeqMap[(star_chain, star_seq)] = (star_chain if cif_chain is None else cif_chain,
                                                           star_seq if _cif_seq is None else _cif_seq)

        asm_id = 0
        cs_list_id = 0
        dist_list_id = 0
        dihed_list_id = 0
        rdc_list_id = 0
        peak_list_id = 0

        if data_type == 'Entry':

            for saveframe in star_data:
                sf = pynmrstar.Saveframe.from_scratch(saveframe.name)

                if saveframe.tag_prefix == '_Assembly':
                    asm_id += 1

                elif saveframe.tag_prefix == '_Assigned_chem_shift_list':
                    cs_list_id += 1

                elif saveframe.tag_prefix == '_Gen_dist_constraint_list':
                    dist_list_id += 1

                elif saveframe.tag_prefix == '_Torsion_angle_constraint_list':
                    dihed_list_id += 1

                elif saveframe.tag_prefix == '_RDC_constraint_list':
                    rdc_list_id += 1

                elif saveframe.tag_prefix == '_Spectral_peak_list':
                    peak_list_id += 1

                sf.set_tag_prefix(saveframe.tag_prefix)

                for tag in saveframe.tags:

                    if tag[0].lower() == 'sf_category':
                        auth_tag = self.get_star_auth_tag(saveframe.category)[0]
                        if auth_tag is not None:
                            sf.add_tag('Sf_category', auth_tag)
                    elif saveframe.tag_prefix == '_Gen_dist_constraint_list' and tag[0] == 'Constraint_type':
                        star_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_auth_tag(star_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1] if tag[1] not in altDistanceConstraintType['nmr-star'] else altDistanceConstraintType['nmr-star'][tag[1]])
                    elif saveframe.tag_prefix == '_Torsion_angle_constraint_list' and tag[0] == 'Constraint_type':
                        star_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_auth_tag(star_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1] if tag[1] not in altDihedralAngleConstraintType['nmr-star'] else altDihedralAngleConstraintType['nmr-star'][tag[1]])
                    elif saveframe.tag_prefix == '_RDC_constraint_list' and tag[0] == 'Constraint_type':
                        star_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_auth_tag(star_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1] if tag[1] not in altRdcConstraintType['nmr-star'] else altRdcConstraintType['nmr-star'][tag[1]])
                    else:
                        star_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_auth_tag(star_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1])

                for loop in saveframe:

                    lp = pynmrstar.Loop.from_scratch()
                    tags = self.extend_star_loop_tags(loop.get_tag_names())

                    if len(tags) == 0:
                        continue

                    for tag in tags:
                        lp.add_tag(tag)

                    if loop.category == '_Chem_comp_assembly':
                        rows, aux_rows = self.star2star_seq_row(loop.get_tag_names(), lp.get_tag_names(), loop.data, report)
                        for d in rows:
                            d[lp.get_tag_names().index('_Chem_comp_assembly.Assembly_ID')] = asm_id
                            lp.add_data(d)

                    elif loop.category == '_Bond':
                        rows = self.star2star_bond_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                        for d in rows:
                            d[lp.get_tag_names().index('_Bond.Assembly_ID')] = asm_id
                            lp.add_data(d)

                    elif loop.category == '_Atom_chem_shift':
                        rows = self.star2star_cs_row(loop.get_tag_names(), lp.get_tag_names(), loop.data, leave_unmatched)
                        for d in rows:
                            d[lp.get_tag_names().index('_Atom_chem_shift.Assigned_chem_shift_list_ID')] = cs_list_id
                            lp.add_data(d)

                    elif loop.category == '_Gen_dist_constraint':
                        rows = self.star2star_dist_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                        for d in rows:
                            d[lp.get_tag_names().index('_Gen_dist_constraint.Gen_dist_constraint_list_ID')] = dist_list_id
                            lp.add_data(d)

                    elif loop.category == '_Torsion_angle_constraint':
                        rows = self.star2star_dihed_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                        for d in rows:
                            d[lp.get_tag_names().index('_Torsion_angle_constraint.Torsion_angle_constraint_list_ID')] = dihed_list_id
                            lp.add_data(d)

                    elif loop.category == '_RDC_constraint':
                        rows = self.star2star_rdc_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                        for d in rows:
                            d[lp.get_tag_names().index('_RDC_constraint.RDC_constraint_list_ID')] = rdc_list_id
                            lp.add_data(d)

                    elif loop.category == '_Peak_row_format':
                        rows = self.star2star_peak_row(loop.get_tag_names(), lp.get_tag_names(), loop.data, leave_unmatched)
                        for d in rows:
                            d[lp.get_tag_names().index('_Peak_row_format.Spectral_peak_list_ID')] = peak_list_id
                            lp.add_data(d)

                    else:

                        for data in loop.data:

                            if loop.category == '_Spectral_dim':
                                rows = self.star2star_row(loop.get_tag_names(), lp.get_tag_names(), data)
                                for d in rows:
                                    d[lp.get_tag_names().index('_Spectral_dim.Spectral_peak_list_ID')] = peak_list_id
                                    lp.add_data(d)

                            elif loop.category == '_Spectral_dim_transfer':
                                rows = self.star2star_row(loop.get_tag_names(), lp.get_tag_names(), data)
                                for d in rows:
                                    d[lp.get_tag_names().index('_Spectral_dim_transfer.Spectral_peak_list_ID', )] = peak_list_id
                                    lp.add_data(d)

                            else:
                                rows = self.star2star_row(loop.get_tag_names(), lp.get_tag_names(), data)
                                for d in rows:
                                    lp.add_data(d)

                    sf.add_loop(lp)

                if saveframe.tag_prefix == '_Entry':
                    sf.add_tag('NMR_STAR_version', NMR_STAR_VERSION)

                    try:
                        if __pynmrstar_v3_2__:
                            loop = sf.get_loop('_Software_applied_methods')
                        else:
                            loop = sf.get_loop_by_category('_Software_applied_methods')
                        row = []
                        for t in loop.tags:
                            if t == 'Software_name':
                                row.append(self.__class__.__name__)
                            elif t == 'Script_name':
                                row.append(self.star_data_to_nmrstar.__name__)
                            else:
                                row.append('.')
                        loop.add_data(row)
                    except KeyError:
                        pass

                elif saveframe.tag_prefix == '_Assembly':
                    sf.add_tag('ID', asm_id)

                elif saveframe.tag_prefix == '_Assigned_chem_shift_list':
                    sf.add_tag('ID', cs_list_id)

                elif saveframe.tag_prefix == '_Gen_dist_constraint_list':
                    sf.add_tag('ID', dist_list_id)

                elif saveframe.tag_prefix == '_Torsion_angle_constraint_list':
                    sf.add_tag('ID', dihed_list_id)

                elif saveframe.tag_prefix == '_RDC_constraint_list':
                    sf.add_tag('ID', rdc_list_id)

                elif saveframe.tag_prefix == '_Spectral_peak_list':
                    sf.add_tag('ID', peak_list_id)

                else:
                    continue

                out_data.add_saveframe(sf)

        elif data_type in ('Saveframe', 'Loop'):

            if data_type == 'Saveframe':
                saveframe = star_data
                sf = pynmrstar.Saveframe.from_scratch(saveframe.name)

                if saveframe.category == 'entry_information':
                    sf.set_tag_prefix('Entry')

                elif saveframe.category == 'assembly':
                    asm_id += 1
                    sf.set_tag_prefix('Assembly')

                elif saveframe.category == 'assigned_chemical_shifts':
                    cs_list_id += 1
                    sf.set_tag_prefix('Assigned_chem_shift_list')

                elif saveframe.category == 'general_distance_constraints':
                    dist_list_id += 1
                    sf.set_tag_prefix('Gen_dist_constraint_list')

                elif saveframe.category == 'torsion_angle_constraints':
                    dihed_list_id += 1
                    sf.set_tag_prefix('Torsion_angle_constraint_list')

                elif saveframe.category == 'RDC_constraints':
                    rdc_list_id += 1
                    sf.set_tag_prefix('RDC_constraint_list')

                elif saveframe.category == 'spectral_peak_list':
                    peak_list_id += 1
                    sf.set_tag_prefix('Spectral_peak_list')

                for tag in saveframe.tags:

                    if tag[0].lower() == 'sf_category':
                        auth_tag = self.get_star_auth_tag(saveframe.category)[0]
                        if auth_tag is not None:
                            sf.add_tag('Sf_category', auth_tag)
                    elif saveframe.tag_prefix == '_Gen_dist_constraint_list' and tag[0] == 'Constraint_type':
                        star_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_auth_tag(star_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1] if tag[1] not in altDistanceConstraintType['nmr-star'] else altDistanceConstraintType['nmr-star'][tag[1]])
                    elif saveframe.tag_prefix == '_Torsion_angle_constraint_list' and tag[0] == 'Constraint_type':
                        star_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_auth_tag(star_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1] if tag[1] not in altDihedralAngleConstraintType['nmr-star'] else altDihedralAngleConstraintType['nmr-star'][tag[1]])
                    elif saveframe.tag_prefix == '_RDC_constraint_list' and tag[0] == 'Constraint_type':
                        star_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_auth_tag(star_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1] if tag[1] not in altRdcConstraintType['nmr-star'] else altRdcConstraintType['nmr-star'][tag[1]])
                    else:
                        star_tag = f"{saveframe.tag_prefix}.{tag[0]}"
                        auth_tag = self.get_star_auth_tag(star_tag)[0]
                        if auth_tag is not None:
                            sf.add_tag(auth_tag, tag[1])

            else:

                if star_data.category == '_Software_applied_methods':
                    sf = pynmrstar.Saveframe.from_scratch('entry')
                    sf.set_tag_prefix('Entry')
                    sf.add_tag('Sf_category', 'entry_information')

                elif star_data.category == '_Audit':  # DAOTHER-6327
                    sf = pynmrstar.Saveframe.from_scratch('entry')
                    sf.set_tag_prefix('Entry')
                    sf.add_tag('Sf_category', 'entry_information')

                elif star_data.category == '_Chem_comp_assembly':
                    sf = pynmrstar.Saveframe.from_scratch('assembly')
                    asm_id += 1
                    sf.set_tag_prefix('Assembly')
                    sf.add_tag('Sf_category', 'assembly')

                elif star_data.category == '_Atom_chem_shift':
                    cs_list_id += 1
                    sf = pynmrstar.Saveframe.from_scratch(f"assigned_chem_shift_list_{cs_list_id}")
                    sf.set_tag_prefix('Assigned_chem_shift_list')
                    sf.add_tag('Sf_category', 'assigned_chemical_shifts')

                elif star_data.category == '_Gen_dist_constraint':
                    dist_list_id += 1
                    sf = pynmrstar.Saveframe.from_scratch(f"gen_dist_constraint_list_{dist_list_id}")
                    sf.set_tag_prefix('Gen_dist_constraint_list')
                    sf.add_tag('Sf_category', 'general_distance_constraints')

                elif star_data.category == '_Torsion_angle_constraint':
                    dihed_list_id += 1
                    sf = pynmrstar.Saveframe.from_scratch(f"torsion_angle_constraint_list_{dihed_list_id}")
                    sf.set_tag_prefix('Torsion_angle_constraint_list')
                    sf.add_tag('Sf_category', 'torsion_angle_constraints')

                elif star_data.category == '_RDC_constraint':
                    rdc_list_id += 1
                    sf = pynmrstar.Saveframe.from_scratch(f"rdc_constraint_list_{rdc_list_id}")
                    sf.set_tag_prefix('RDC_constraint_list')
                    sf.add_tag('Sf_category', 'RDC_constraints')

                elif star_data.category == '_Peak_row_format':
                    peak_list_id += 1
                    sf = pynmrstar.Saveframe.from_scratch(f"spectral_peak_list_{peak_list_id}")
                    sf.set_tag_prefix('Spectral_peak_list')
                    sf.add_tag('Sf_category', 'spectral_peak_list')

                else:
                    error.append(f"Loop category {star_data.category} is not supported.")
                    return False, {'info': info, 'warning': warning, 'error': error}

                sf.add_tag('Sf_framecode', sf.name)

                saveframe = [star_data]

            has_covalent_links = any(loop for loop in saveframe if loop.category == '_Bond')
            aux_rows = []

            for loop in saveframe:

                lp = pynmrstar.Loop.from_scratch()
                tags = self.extend_star_loop_tags(loop.get_tag_names())

                if len(tags) == 0:
                    continue

                for tag in tags:
                    lp.add_tag(tag)

                if loop.category == '_Chem_comp_assembly':
                    rows, aux_rows = self.star2star_seq_row(loop.get_tag_names(), lp.get_tag_names(), loop.data, report)
                    for d in rows:
                        d[lp.get_tag_names().index('_Chem_comp_assembly.Assembly_ID')] = asm_id
                        lp.add_data(d)

                elif loop.category == '_Bond':
                    rows = self.star2star_bond_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                    for d in rows:
                        d[lp.get_tag_names().index('_Bond.Assembly_ID')] = asm_id
                        lp.add_data(d)

                elif loop.category == '_Atom_chem_shift':
                    rows = self.star2star_cs_row(loop.get_tag_names(), lp.get_tag_names(), loop.data, leave_unmatched)
                    for d in rows:
                        d[lp.get_tag_names().index('_Atom_chem_shift.Assigned_chem_shift_list_ID')] = cs_list_id
                        lp.add_data(d)

                elif loop.category == '_Gen_dist_constraint':
                    rows = self.star2star_dist_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                    for d in rows:
                        d[lp.get_tag_names().index('_Gen_dist_constraint.Gen_dist_constraint_list_ID')] = dist_list_id
                        lp.add_data(d)

                elif loop.category == '_Torsion_angle_constraint':
                    rows = self.star2star_dihed_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                    for d in rows:
                        d[lp.get_tag_names().index('_Torsion_angle_constraint.Torsion_angle_constraint_list_ID')] = dihed_list_id
                        lp.add_data(d)

                elif loop.category == '_RDC_constraint':
                    rows = self.star2star_rdc_row(loop.get_tag_names(), lp.get_tag_names(), loop.data)
                    for d in rows:
                        d[lp.get_tag_names().index('_RDC_constraint.RDC_constraint_list_ID')] = rdc_list_id
                        lp.add_data(d)

                elif loop.category == '_Peak_row_format':
                    rows = self.star2star_peak_row(loop.get_tag_names(), lp.get_tag_names(), loop.data, leave_unmatched)
                    for d in rows:
                        d[lp.get_tag_names().index('_Peak_row_format.Spectral_peak_list_ID')] = peak_list_id
                        lp.add_data(d)

                else:

                    for data in loop.data:

                        if loop.category == '_Spectral_dim':
                            rows = self.star2star_row(loop.get_tag_names(), lp.get_tag_names(), data)
                            for d in rows:
                                d[lp.get_tag_names().index('_Spectral_dim.Spectral_peak_list_ID')] = peak_list_id
                                lp.add_data(d)

                        elif loop.category == '_Spectral_dim_transfer':
                            rows = self.star2star_row(loop.get_tag_names(), lp.get_tag_names(), data)
                            for d in rows:
                                d[lp.get_tag_names().index('_Spectral_dim_transfer.Spectral_peak_list_ID', )] = peak_list_id
                                lp.add_data(d)

                        else:
                            rows = self.star2star_row(loop.get_tag_names(), lp.get_tag_names(), data)
                            for d in rows:
                                lp.add_data(d)

                sf.add_loop(lp)

                if len(aux_rows) > 0 and ((loop.category == '_Chem_comp_assembly' and not has_covalent_links)
                                          or (loop.category == '_Bond' and has_covalent_links)):
                    lp = pynmrstar.Loop.from_scratch()
                    for _tag in ENTITY_DELETED_ATOM_ITEMS:
                        lp.add_tag('_Entity_deleted_atom.' + _tag)
                    for d in aux_rows:
                        d[lp.get_tag_names().index('_Entity_deleted_atom.Assembly_ID')] = asm_id
                        lp.add_data(d)
                    sf.add_loop(lp)

            if sf.tag_prefix == '_Entry':
                sf.add_tag('NMR_STAR_version', NMR_STAR_VERSION)

                try:
                    if __pynmrstar_v3_2__:
                        loop = sf.get_loop('_Software_applied_methods')
                    else:
                        loop = sf.get_loop_by_category('_Software_applied_methods')
                    row = []
                    for t in loop.tags:
                        if t == 'Software_name':
                            row.append(self.__class__.__name__)
                        elif t == 'Script_name':
                            row.append(self.star_data_to_nmrstar.__name__)
                        else:
                            row.append('.')
                    loop.add_data(row)
                except KeyError:
                    pass

            elif sf.tag_prefix == '_Assembly':
                sf.add_tag('ID', asm_id)

            elif sf.tag_prefix == '_Assigned_chem_shift_list':
                sf.add_tag('ID', cs_list_id)

            elif sf.tag_prefix == '_Gen_dist_constraint':
                sf.add_tag('ID', dist_list_id)

            elif sf.tag_prefix == '_Torsion_angle_constraint':
                sf.add_tag('ID', dihed_list_id)

            elif sf.tag_prefix == '_RDC_constraint':
                sf.add_tag('ID', rdc_list_id)

            elif sf.tag_prefix == '_Peak_row_format':
                sf.add_tag('ID', peak_list_id)

            out_data.add_saveframe(sf)

        if __pynmrstar_v3__:
            out_data.write_to_file(output_file_path, skip_empty_loops=True, skip_empty_tags=False)
        else:
            out_data.write_to_file(output_file_path)

        info.append(f"File {output_file_path} successfully written.")

        return True, {'info': info, 'warning': warning, 'error': error}


if __name__ == "__main__":
    _nefT = NEFTranslator()
    _nefT.nef_to_nmrstar('data/2l9r.nef')
    print(_nefT.validate_file('data/2l9r.str', 'A'))

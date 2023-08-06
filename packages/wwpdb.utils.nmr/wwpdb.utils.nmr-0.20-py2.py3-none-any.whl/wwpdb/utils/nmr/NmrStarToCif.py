##
# File: NmrStarToCif.py
# Date: 03-Apr-2020
#
# Updates:
# 06-Apr-2020  M. Yokochi - add support for Original_pdb_* items in restraints/peak lists
# 07-Apr-2020  M. Yokochi - add clean() for NMR legacy deposition (DAOTHER-2874)
# 18-Oct-2021  M. Yokochi - code revision according to PEP8 using Pylint (DAOTHER-7389, issue #5)
##
""" Wrapper class for NMR-STAR to CIF converter.
    @author: Masashi Yokochi
"""
import sys

from mmcif.io.IoAdapterPy import IoAdapterPy

try:
    from wwpdb.utils.nmr.io.mmCIFUtil import mmCIFUtil
    from wwpdb.utils.nmr.AlignUtil import emptyValue
except ImportError:
    from nmr.io.mmCIFUtil import mmCIFUtil
    from nmr.AlignUtil import emptyValue


class NmrStarToCif:
    """ NMR-STAR to CIF converter.
    """

    def __init__(self, verbose=False, log=sys.stderr):
        self.__verbose = verbose
        self.__lfh = log

        # whether to remove _pdbx_nmr_assigned_chem_shift_list (DAOTHER-2874)
        self.__remove_cs_list_cif = True
        # whether to add Original_pdb_* items in chemical shifts
        self.__add_original_pdb_in_chem_shift = True
        # whether to add Original_pdb_* items in distance restraints
        self.__add_original_pdb_in_dist_restraint = True
        # whether to add Origianl_pdb_* items in other restraints
        self.__add_original_pdb_in_others = False

    def clean(self, cifPath=None, originalCsFileNameList=None, originalMrFileNameList=None):
        """ Clean up CIF formatted NMR data for NMR legacy deposition
        """

        if cifPath is None:
            return False

        try:

            # post modification for converted CIF file

            cifObj = mmCIFUtil(filePath=cifPath)

            categories = cifObj.GetCategories()

            cs_loop_str = 'Atom_chem_shift'
            cs_list_cif = 'pdbx_nmr_assigned_chem_shift_list'

            # remove _pdbx_nmr_assigned_chem_shift_list

            cs_list_cif_info = []

            for k, v in categories.items():

                if cs_list_cif in v:

                    if cs_loop_str in v:
                        dList, _ = cifObj.GetValueAndItemByBlock(k, cs_list_cif)

                        if len(dList) == 0:
                            continue

                        for d in dList:
                            info = {'sf_framecode': k}
                            if 'entry_id' in d:
                                info['entry_id'] = d['entry_id']
                            if 'id' in d:
                                info['id'] = d['id']
                            if 'data_file_name' in d:
                                info['data_file_name'] = d['data_file_name']
                            cs_list_cif_info.append(info)

                    if self.__remove_cs_list_cif or cs_loop_str not in v:
                        cifObj.RemoveCategory(k, cs_list_cif)

            # add the following saveframe tag
            if self.__remove_cs_list_cif:

                content_subtypes = ('chem_shift', 'dist_restraint', 'dihed_restraint', 'rdc_restraint', 'spectral_peak')

                sf_tags = {'chem_shift': 'Assigned_chem_shift_list',
                           'dist_restraint': 'Gen_dist_constraint_list',
                           'dihed_restraint': 'Torsion_angle_constraint_list',
                           'rdc_restraint': 'RDC_constraint_list',
                           'spectral_peak': 'Spectral_peak_list'}
                lp_tags = {'chem_shift': 'Atom_chem_shift',
                           'dist_restraint': 'Gen_dist_constraint',
                           'dihed_restraint': 'Torsion_angle_constraint',
                           'rdc_restraint': 'RDC_constraint',
                           'spectral_peak': 'Peak_row_format'}
                sf_catgories = {'chem_shift': 'assigned_chemical_shifts',
                                'dist_restraint': 'general_distance_constraints',
                                'dihed_restraint': 'torsion_angle_constraints',
                                'rdc_restraint': 'RDC_constraints',
                                'spectral_peak': 'spectral_peak_list'}
                list_id_tags = {'chem_shift': 'Assigned_chem_shift_list_ID',
                                'dist_restraint': 'Gen_dist_constraint_list_ID',
                                'dihed_restraint': 'Torsion_angle_constraint_list_ID',
                                'rdc_restraint': 'RDC_constraint_list_ID',
                                'spectral_peak': 'Spectral_peak_list_ID'}

                sf_category_tag = 'Sf_category'
                sf_framecode_tag = 'Sf_framecode'
                entry_id_tag = 'Entry_ID'
                id_tag = 'ID'
                data_file_name_tag = 'Data_file_name'

                cs_list_id = 0
                mr_list_id = 0

                for content_subtype in content_subtypes:

                    for k, v in categories.items():

                        if lp_tags[content_subtype] in v:

                            dList, _ = cifObj.GetValueAndItemByBlock(k, lp_tags[content_subtype])

                            try:
                                entry_id = next(row[entry_id_tag] for row in dList if row[entry_id_tag] not in emptyValue)
                            except:  # noqa: E722 pylint: disable=bare-except
                                entry_id = '?'

                            try:
                                list_id = next(row[list_id_tags[content_subtype]] for row in dList if row[list_id_tags[content_subtype]] not in emptyValue)
                            except:  # noqa: E722 pylint: disable=bare-except
                                list_id = '?'

                            if content_subtype == 'chem_shift':
                                originalFileName = '?' if originalCsFileNameList is None or cs_list_id >= len(originalCsFileNameList) else originalCsFileNameList[cs_list_id]
                                cs_list_id += 1
                            else:
                                originalFileName = '?' if originalMrFileNameList is None or mr_list_id >= len(originalMrFileNameList) else originalMrFileNameList[mr_list_id]
                                mr_list_id += 1

                            try:
                                info = next(info for info in cs_list_cif_info if info['sf_framecode'] == k)
                                if 'entry_id' in info and info['entry_id'] not in emptyValue:
                                    entry_id = info['entry_id']
                                if 'id' in info and info['id'] not in emptyValue:
                                    list_id = info['id']
                                if 'data_file_name' in info and info['data_file_name'] not in emptyValue:
                                    originalFileName = info['data_file_name']
                            except StopIteration:
                                pass

                            sf_item_names = [sf_category_tag, sf_framecode_tag, entry_id_tag, id_tag, data_file_name_tag]
                            sf_item_values = [sf_catgories[content_subtype], k, entry_id, list_id, originalFileName]

                            if sf_tags[content_subtype] in v:
                                attrs = cifObj.GetAttributes(k, sf_tags[content_subtype])
                                for i, sf_item_name in enumerate(sf_item_names):
                                    if sf_item_name in attrs:
                                        cifObj.UpdateSingleRowValue(k, sf_tags[content_subtype], sf_item_name, 0, sf_item_values[i])
                                    else:
                                        cifObj.ExtendCategory(k, sf_tags[content_subtype], [sf_item_name], [[sf_item_values[i]]])

                            else:
                                cifObj.AddCategory(k, sf_tags[content_subtype], sf_item_names)
                                cifObj.InsertData(k, sf_tags[content_subtype], [sf_item_values])

                            cifObj.MoveCategoryToTop(k, sf_tags[content_subtype])

            cifObj.WriteCif(outputFilePath=cifPath)

            return True

        except Exception as e:
            self.__lfh.write(f"+ERROR- NmrStarToCif.clean() {str(e)}\n")

        return False

    def convert(self, strPath=None, cifPath=None, originalFileName=None, fileType='nm-uni-nef'):
        """ Convert NMR-STAR to CIF for NMR unified deposition
        """

        if strPath is None or cifPath is None:
            return False

        # whether to overwrite Auth_atom_ID by Atom_ID
        overwrite_auth_atom_id = 'nef' in fileType

        try:

            myIo = IoAdapterPy(False, sys.stderr)
            containerList = myIo.readFile(strPath)

            if containerList is not None and len(containerList) > 1:

                if self.__verbose:
                    self.__lfh.write(f"Input container list is {[(c.getName(), c.getType()) for c in containerList]!r}\n")

                for c in containerList:
                    c.setType('data')

                myIo.writeFile(cifPath, containerList=containerList[1:])

                # post modification for converted CIF file

                cifObj = mmCIFUtil(filePath=cifPath)

                categories = cifObj.GetCategories()

                # add Data_file_name item in the following saveframe tag

                sf_tags = ['Assigned_chem_shift_list', 'Gen_dist_constraint_list', 'Torsion_angle_constraint_list', 'RDC_constraint_list', 'Spectral_peak_list']
                data_file_name_tag = 'Data_file_name'

                for sf_tag in sf_tags:

                    for k, v in categories.items():

                        if sf_tag in v:
                            attrs = cifObj.GetAttributes(k, sf_tag)

                            if data_file_name_tag in attrs:
                                cifObj.UpdateSingleRowValue(k, sf_tag, data_file_name_tag, 0, originalFileName)
                            else:
                                cifObj.ExtendCategory(k, sf_tag, [data_file_name_tag], [[originalFileName]])

                cs_loop_str = 'Atom_chem_shift'
                cs_list_cif = 'pdbx_nmr_assigned_chem_shift_list'

                # add _pdbx_nmr_assigned_chem_shift_list for each _Assigned_chem_shift_list for backward compatibility
                if not self.__remove_cs_list_cif:

                    for k, v in categories.items():

                        if cs_loop_str in v:

                            entry_id_tag = 'Entry_ID'
                            list_id_tag = 'Assigned_chem_shift_list_ID'

                            dList, _ = cifObj.GetValueAndItemByBlock(k, cs_loop_str)

                            try:
                                entry_id = next(row[entry_id_tag] for row in dList if row[entry_id_tag] not in emptyValue)
                            except:  # noqa: E722 pylint: disable=bare-except
                                entry_id = '?'

                            try:
                                list_id = next(row[list_id_tag] for row in dList if row[list_id_tag] not in emptyValue)
                            except:  # noqa: E722 pylint: disable=bare-except
                                list_id = '?'

                            cifObj.AddCategory(k, cs_list_cif, ['entry_id', 'id', 'data_file_name'])
                            cifObj.InsertData(k, cs_list_cif, [[entry_id, list_id, originalFileName]])

                # add _Atom_chem_shift.Original_PDB_* items

                lp_category = 'Atom_chem_shift'
                original_items = ['Original_PDB_strand_ID', 'Original_PDB_residue_no', 'Original_PDB_residue_name', 'Original_PDB_atom_name']
                original_auth_map = {'Original_PDB_strand_ID': 'Auth_asym_ID',
                                     'Original_PDB_residue_no': 'Auth_seq_ID',
                                     'Original_PDB_residue_name': 'Auth_comp_ID',
                                     'Original_PDB_atom_name': 'Auth_atom_ID'}
                atom_id_tags = ['Atom_ID']
                auth_atom_id_tags = ['Auth_atom_ID']

                for k, v in categories.items():

                    if lp_category in v:
                        items = cifObj.GetAttributes(k, lp_category)

                        extended_items = [original_item for original_item in original_items if original_item not in items]

                        if len(extended_items) > 0:
                            dList, _ = cifObj.GetValueAndItemByBlock(k, lp_category)

                            auth_items = [original_auth_map[original_item] for original_item in extended_items]

                            extended_data_list = []

                            for src in dList:
                                dst = []
                                for auth_item in auth_items:
                                    dst.append(src[auth_item])
                                extended_data_list.append(dst)

                            if self.__add_original_pdb_in_chem_shift:
                                cifObj.ExtendCategory(k, lp_category, extended_items, extended_data_list, items.index('Auth_atom_ID') + 1)

                        if overwrite_auth_atom_id:
                            cifObj.CopyValueInRow(k, lp_category, atom_id_tags, auth_atom_id_tags)

                # add _Gen_dist_constraint.Original_PDB_* items

                lp_category = 'Gen_dist_constraint'
                _original_items = []
                _original_auth_map = {}
                _atom_id_tags = []
                _auth_atom_id_tags = []
                for i in range(1, 3):
                    for original_item in original_items:
                        _original_items.append(original_item + '_' + str(i))
                    for k, v in original_auth_map.items():
                        _original_auth_map[k + '_' + str(i)] = v + '_' + str(i)
                    for atom_id_tag in atom_id_tags:
                        _atom_id_tags.append(atom_id_tag + '_' + str(i))
                    for auth_atom_id_tag in auth_atom_id_tags:
                        _auth_atom_id_tags.append(auth_atom_id_tag + '_' + str(i))

                for k, v in categories.items():

                    if lp_category in v:
                        items = cifObj.GetAttributes(k, lp_category)

                        extended_items = [original_item for original_item in _original_items if original_item not in items]

                        if len(extended_items) > 0:
                            dList, _ = cifObj.GetValueAndItemByBlock(k, lp_category)

                            auth_items = [_original_auth_map[original_item] for original_item in extended_items]

                            extended_data_list = []

                            for src in dList:
                                dst = []
                                for auth_item in auth_items:
                                    dst.append(src[auth_item])
                                extended_data_list.append(dst)

                            if self.__add_original_pdb_in_dist_restraint:
                                cifObj.ExtendCategory(k, lp_category, extended_items, extended_data_list, items.index('Auth_atom_ID_2') + 1)

                        if overwrite_auth_atom_id:
                            cifObj.CopyValueInRow(k, lp_category, _atom_id_tags, _auth_atom_id_tags)

                if self.__add_original_pdb_in_others:

                    # add _Torsion_angle_constraint.Original_PDB_* items

                    lp_category = 'Torsion_angle_constraint'
                    _original_items = []
                    _original_auth_map = {}
                    _atom_id_tags = []
                    _auth_atom_id_tags = []
                    for i in range(1, 5):
                        for original_item in original_items:
                            _original_items.append(original_item + '_' + str(i))
                        for k, v in original_auth_map.items():
                            _original_auth_map[k + '_' + str(i)] = v + '_' + str(i)
                        for atom_id_tag in atom_id_tags:
                            _atom_id_tags.append(atom_id_tag + '_' + str(i))
                        for auth_atom_id_tag in auth_atom_id_tags:
                            _auth_atom_id_tags.append(auth_atom_id_tag + '_' + str(i))

                    for k, v in categories.items():

                        if lp_category in v:
                            items = cifObj.GetAttributes(k, lp_category)

                            extended_items = [original_item for original_item in _original_items if original_item not in items]

                            if len(extended_items) > 0:
                                dList, _ = cifObj.GetValueAndItemByBlock(k, lp_category)

                                auth_items = [_original_auth_map[original_item] for original_item in extended_items]

                                extended_data_list = []

                                for src in dList:
                                    dst = []
                                    for auth_item in auth_items:
                                        dst.append(src[auth_item])
                                    extended_data_list.append(dst)

                                cifObj.ExtendCategory(k, lp_category, extended_items, extended_data_list, items.index('Auth_atom_ID_4') + 1)

                            if overwrite_auth_atom_id:
                                cifObj.CopyValueInRow(k, lp_category, _atom_id_tags, _auth_atom_id_tags)

                    # add _RDC_constraint.Origianl_PDB_* items

                    lp_category = 'RDC_constraint'
                    _original_items = []
                    _original_auth_map = {}
                    _atom_id_tags = []
                    _auth_atom_id_tags = []
                    for i in range(1, 3):
                        for original_item in original_items:
                            _original_items.append(original_item + '_' + str(i))
                        for k, v in original_auth_map.items():
                            _original_auth_map[k + '_' + str(i)] = v + '_' + str(i)
                        for atom_id_tag in atom_id_tags:
                            _atom_id_tags.append(atom_id_tag + '_' + str(i))
                        for auth_atom_id_tag in auth_atom_id_tags:
                            _auth_atom_id_tags.append(auth_atom_id_tag + '_' + str(i))

                    for k, v in categories.items():

                        if lp_category in v:
                            items = cifObj.GetAttributes(k, lp_category)

                            extended_items = [original_item for original_item in _original_items if original_item not in items]

                            if len(extended_items) > 0:
                                dList, _ = cifObj.GetValueAndItemByBlock(k, lp_category)

                                auth_items = [_original_auth_map[original_item] for original_item in extended_items]

                                extended_data_list = []

                                for src in dList:
                                    dst = []
                                    for auth_item in auth_items:
                                        dst.append(src[auth_item])
                                    extended_data_list.append(dst)

                                cifObj.ExtendCategory(k, lp_category, extended_items, extended_data_list, items.index('Auth_atom_ID_2') + 1)

                            if overwrite_auth_atom_id:
                                cifObj.CopyValueInRow(k, lp_category, _atom_id_tags, _auth_atom_id_tags)

                    lp_category = 'Peak_row_format'

                    for k, v in categories.items():

                        if lp_category in v:
                            items = cifObj.GetAttributes(k, lp_category)
                            max_dim = 0
                            for i in range(1, 16):
                                if 'Atom_ID_' + str(i) not in items:
                                    break
                                max_dim = i

                            if 1 < max_dim <= 16:
                                _original_items = []
                                _original_auth_map = {}
                                _atom_id_tags = []
                                _auth_atom_id_tags = []
                                for i in range(1, max_dim):
                                    for original_item in original_items:
                                        _original_items.append(original_item + '_' + str(i))
                                    for _k, _v in original_auth_map.items():
                                        _original_auth_map[_k + '_' + str(i)] = _v + '_' + str(i)
                                    for atom_id_tag in atom_id_tags:
                                        _atom_id_tags.append(atom_id_tag + '_' + str(i))
                                    for auth_atom_id_tag in auth_atom_id_tags:
                                        _auth_atom_id_tags.append(auth_atom_id_tag + '_' + str(i))

                                extended_items = [original_item for original_item in _original_items if original_item not in items]

                                has_auth_value = False

                                if len(extended_items) > 0:
                                    dList, _ = cifObj.GetValueAndItemByBlock(k, lp_category)

                                    auth_items = [_original_auth_map[original_item] for original_item in extended_items]

                                    extended_data_list = []

                                    for src in dList:
                                        dst = []
                                        for auth_item in auth_items:
                                            dst.append(src[auth_item])
                                            if src[auth_item] not in emptyValue:
                                                has_auth_value = True
                                        extended_data_list.append(dst)

                                    if has_auth_value:
                                        cifObj.ExtendCategory(k, lp_category, extended_items, extended_data_list, items.index(f"Auth_atom_ID_{max_dim - 1}") + 1)

                                if overwrite_auth_atom_id and has_auth_value:
                                    cifObj.CopyValueInRow(k, lp_category, _atom_id_tags, _auth_atom_id_tags)

                cifObj.WriteCif(outputFilePath=cifPath)

                return True

        except Exception as e:
            self.__lfh.write(f"+ERROR- NmrStarToCif.convert() {str(e)}\n")

        return False

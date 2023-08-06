##
# File: NmrDpReport.py
# Date: 29-Jul-2019
#
# Updates:
# 09-Oct-2019  M. Yokochi - add setCorrectedError() to catch missing mandatory saveframe tag
# 10-Oct-2019  M. Yokochi - add 'enum_failure_ignorable' warning type
# 15-Oct-2019  M. Yokochi - add 'encouragement' waring type
# 27-Jan-2020  M. Yokochi - change warning type 'enum_failure' to 'enum_mismatch'
# 05-Feb-2020  M. Yokochi - move conflicted_data error to warning
# 10-Feb-2020  M. Yokochi - add methods to retrieve polymer sequence for sample sequence alignment
# 13-Feb-2020  M. Yokochi - add methods to retrieve content_subtype for apilayer.postModifyNMR
# 14-Feb-2020  M. Yokochi - add methods to pre-populate pdbx_nmr_spectral_peak_list, apilayer.postModifyNMRPeaks
# 21-Feb-2020  M. Yokochi - update content-type definitions
# 28-Feb-2020  M. Yokochi - add support for 'nmr-chemical-shifts' content type (DAOTHER-4515)
# 02-Mar-2020  M. Yokochi - add support for 'nmr-restraints' content type (DAOTHER-4515)
# 13-Mar-2020  M. Yokochi - change warning type from suspicious_data to anomalous_data
# 17-Mar-2020  M. Yokochi - remove irrelevant warning types in corrected_warning
# 18-Mar-2020  M. Yokochi - rename warning type from skipped_sf/lp_category to skipped_saveframe/loop_category
# 23-Mar-2020  M. Yokochi - add 'anomalous_chemical_shift' and 'unusual_chemical_shift' warning types
# 24-Mar-2020  M. Yokochi - add method to retrieve chemical shift reference (DAOTHER-1682)
# 03-Apr-2020  M. Yokochi - add methods to retrieve sequence alignment between coordinate and NMR data
# 15-Apr-2020  M. Yokochi - add getAverageRMSDWithinRange() (DAOTHER-4060)
# 18-Apr-2020  M. Yokochi - fix error of apilayer - getNmrSeqAlignment in NMR legacy deposition (DAOTHER-5594)
# 19-Apr-2020  M. Yokochi - support concatenated CS data in NMR legacy deposition (DAOTHER-5594)
# 19 Apr-2020  M. Yokochi - add 'not_superimposed_model' warning type (DAOTHER-4060)
# 20 Apr-2020  M. Yokochi - add 'concatenated_sequence' warning type (DAOTHER-5594)
# 22-Apr-2020  M. Yokochi - add 'ambiguity_code_mismatch' warning type (DAOTHER-5601)
# 25-Apr-2020  M. Yokochi - add 'entity' content subtype (DAOTHER-5611)
# 25-Apr-2020  M. Yokochi - add 'corrected_format_issue' warning type (DAOTHER-5611)
# 27-Apr-2020  M. Yokochi - add 'auth_atom_nomenclature_mismatch' warning type (DAOTHER-5611)
# 28-Apr-2020  M. Yokochi - prevent system clash due to 'number_of_assignments' (DAOTHER-5611)
# 28-Apr-2020  M. Yokochi - fix 'NOE? (To be decided)' to be 'NOE' (DAOTHER-5626)
# 29-Apr-2020  M. Yokochi - sort 'conflicted_data' and 'inconsistent_data' items (DAOTHER-5622)
# 13-May-2020  M. Yokochi - avoid system crash when format issue occurs (DAOTHER-5673)
# 15-May-2020  M. Yokochi - ignore 'disordered_index' warning (DAOTHER-5485)
# 15-May-2020  M. Yokochi - add 'content_mismatch' error for NMR legacy deposition (DAOTHER-5687)
# 12-Jun-2020  M. Yokochi - performance improvement by reusing cached data
# 25-Jun-2020  M. Yokochi - add 'anomalous_bond_length' warning
# 01-Jul-2020  M. Yokochi - suppress null error/warning in JSON report
# 09-Jul-2020  M. Yokochi - support spectral_peak_alt content subtype (DAOTHER-5926)
# 20-Nov-2020  M. Yokochi - rename 'remarkable_data' warning category to 'unusual/rare_data' (DAOTHER-6372)
# 27-Nov-2020  M. Yokochi - support grouped error/warning message (DAOTHER-6373)
# 17-Dec-2020  M. Yokochi - add 'atom_not_found' error (DAOTHER-6345)
# 21-Jan-2021  M. Yokochi - symptomatic treatment for DAOTHER-6509
# 03-Feb-2021  M. Yokochi - add support for 'identical_chain_id' attribute, which contains mapping of chain id(s), which shares the same entity.
# 30-Mar-2021  M. Yokochi - getNmrSeq1LetterCodeOf() and getModelSeq1LetterCodeOf() do not return any 3-letter code (DAOTHER-6744)
# 24-Jun-2021  M. Yokochi - resolve duplication in grouped error/warning message (DAOTHER-6345, 6830)
# 29-Jun-2021  M. Yokochi - enable to access NMR polymer sequence from auth_asym_id (DAOTHER-7108)
# 02-Jul-2021  M. Yokochi - add content types of NMR restraint file (DAOTHER-6830)
# 24-Aug-2021  M. Yokochi - add content subtype for XPLOR-NIH planarity restraints (DAOTHER-7265)
# 13-Oct-2021  M. Yokochi - code revision according to PEP8 using Pylint (DAOTHER-7389, issue #5)
# 14-Oct-2021  M. Yokochi - add 'incompletely_ssigned_chemical_shift' and 'incompletely_assigned_spectral_peak' (DAOTHER-7389, issue #3)
# 28-Oct-2021  M. Yokochi - add 'corrected_saveframe_name' warning (DAOTHER-7389, issue #4)
# 16-Nov-2021  M. Yokochi - revised error message for malformed XPLOR-NIH RDC restraints (DAOTHER-7478)
# 18-Nov-2021  M. Yokochi - detect content type of XPLOR-NIH hydrogen bond geometry restraints (DAOTHER-7478)
# 21 Dec-2021  M. Yokochi - add 'exactly_overlaid_model' warning type (DAOTHER-7544)
# 27-Jan-2022  M. Yokochi - add restraint types described by XPLOR-NIH, CNS, CYANA, and AMBER systems (NMR restraint remediation)
# 22 Feb-2022  M. Yokochi - add 'complemented_chemical_shift' warning type (DAOTHER-7681, issue #1)
# 04-Mar-2022  M. Yokochi - add coordinate geometry restraints (DAOTHER-7690, NMR restraint remediation)
# 22-Mar-2022  M. Yokochi - add 'nm-res-ros' file type for ROSETTA restraint format (DAOTHER-7690)
# 23-Mar-2022  M. Yokochi - add 'conflicted_mr_data', 'inconsistent_mr_data', 'redundant_mr_data', 'unsupported_mr_data' warning types (DAOTHER-7690)
# 13-Apr-2022  M. Yokochi - add 'label_scheme' option to select label_*_id or auth_*_id scheme of the coordinate file (NMR restraint remediation)
# 14 Apr-2022  M. Yokochi - add 'nm-res-mr' file type for NMR restraint remediation and V5.13
# 17-May-2022  M. Yokochi - add 'nm-res-bio' file type for BIOSYM restraint format (DAOTHER-7825, NMR restraint remediation)
##
""" Wrapper class for NMR data processing report.
    @author: Masashi Yokochi
"""
import logging
import json
import copy
import re

try:
    from wwpdb.utils.nmr.AlignUtil import emptyValue, monDict3
except ImportError:
    from nmr.AlignUtil import emptyValue, monDict3


def get_value_safe(d=None, key=None):
    """ Return value of a given dictionary for a key.
        @return: value for a key, None otherwise
    """

    if d is None or key is None:
        return None

    if key not in d:
        return None

    return d[key]


class NmrDpReport:
    """ Wrapper class for data processing report of NMR data.
    """

    def __init__(self):
        self.__immutable = False

        self.__report = {'information': {'input_sources': [],
                                         'sequence_alignments': None,
                                         'chain_assignments': None,
                                         'diamagnetic': True,
                                         'disulfide_bond': False,
                                         'other_bond': False,
                                         'cyclic_polymer': False,
                                         'status': 'OK'
                                         },
                         'error': None,
                         'warning': None,
                         'corrected_warning': None
                         }

        self.status_codes = ('OK', 'Error', 'Warning')

        self.input_sources = [NmrDpReportInputSource()]
        self.sequence_alignment = NmrDpReportSequenceAlignment()
        self.chain_assignment = NmrDpReportChainAssignment()
        self.error = NmrDpReportError()
        self.warning = NmrDpReportWarning()
        self.corrected_warning = None

    def appendInputSource(self):
        """ Append empty input source.
        """

        self.input_sources.append(NmrDpReportInputSource())

    def isOk(self):
        """ Return whether processing status is OK.
        """

        return self.__report['information']['status'] == 'OK'

    def isError(self):
        """ Return whether processing status is Error.
        """

        return self.__report['information']['status'] == 'Error'

    def isDiamagnetic(self):
        """ Return whether molecular assembly is diamagnetic.
        """

        return self.__report['information']['diamagnetic']

    def hasDisulfideBond(self):
        """ Return whether molecular assembly has disulfide bond.
        """

        return self.__report['information']['disulfide_bond']

    def hasOtherBond(self):
        """ Return whether molecular assembly has other bond.
        """

        return self.__report['information']['other_bond']

    def hasCyclicPolymer(self):
        """ Return whether molecular assembly contains cyclic polymer.
        """

        return self.__report['information']['cyclic_polymer']

    def getInputSourceDict(self, id):  # pylint: disable=redefined-builtin
        """ Return input source dictionary of a given index.
            @return: input source of a given index, None otherwise
        """

        if id < 0 or id >= len(self.input_sources):
            return None

        return self.input_sources[id].get()

    def getInputSourceIdOfNmrData(self):
        """ Return input_source_id of NMR data file.
            @return: index of input source of NMR data file, -1 otherwise
        """

        for i in self.input_sources:
            if i.get()['content_type'] in ('nmr-data-nef', 'nmr-data-str'):
                return self.input_sources.index(i)

        return -1

    def getInputSourceIdsOfNmrLegacyData(self):
        """ Return array of input_source_id of NMR legacy data file.
            @return: array of index of input source of NMR legacy data file, [] otherwise
        """

        return [self.input_sources.index(i) for i in self.input_sources if i.get()['content_type'] in ('nmr-chemical-shifts', 'nmr-restraints')]

    def getInputSourceIdOfCoord(self):
        """ Return input_source_id of coordinate file.
            @return: index of input source of coordinate file, -1 otherwise
        """

        for i in self.input_sources:
            if i.get()['content_type'] == 'model':
                return self.input_sources.index(i)

        return -1

    def getNmrContentSubTypes(self):
        """ Return effective NMR content subtypes.
        """

        content_subtype = get_value_safe(self.getInputSourceDict(self.getInputSourceIdOfNmrData()), 'content_subtype')

        if content_subtype is None:
            return None

        return {k: v for k, v in content_subtype.items() if v > 0}

    def getNmrLegacyContentSubTypes(self, id):  # pylint: disable=redefined-builtin
        """ Return effective NMR content subtypes.
        """

        content_subtype = get_value_safe(self.getInputSourceDict(id), 'content_subtype')

        if content_subtype is None:
            return None

        return {k: v for k, v in content_subtype.items() if v > 0}

    def getNmrStatsOfExptlData(self, content_subtype):
        """ Return stats of experimental data of a given content subtype.
        """

        return get_value_safe(get_value_safe(self.getInputSourceDict(self.getInputSourceIdOfNmrData()), 'stats_of_exptl_data'), content_subtype)

    def getNmrLegacyStatsOfExptlData(self, id, content_subtype):  # pylint: disable=redefined-builtin
        """ Return stats of experimental data of a given content subtype.
        """

        return get_value_safe(get_value_safe(self.getInputSourceDict(id), 'stats_of_exptl_data'), content_subtype)

    def getNmrRestraints(self):
        """ Return stats of NMR restraints.
        """

        content_subtypes = self.getNmrContentSubTypes()

        if content_subtypes is None:
            return self.__getNmrRestraints()

        restraints = []

        sid = self.getInputSourceIdOfNmrData()

        nmr_input_source_dic = self.getInputSourceDict(sid)

        if nmr_input_source_dic is None:
            return None

        file_name = nmr_input_source_dic['file_name']
        file_type = 'NEF' if nmr_input_source_dic['file_type'] == 'nef' else 'NMR-STAR'

        content_subtype = 'dist_restraint'

        if content_subtype in content_subtypes:
            hydrogen_bonds = 0
            disulfide_bonds = 0
            diselenide_bonds = 0
            other_bonds = 0
            symmetric = 0
            noe_like = 0
            noe_exp_type = None
            for stat in self.getNmrStatsOfExptlData(content_subtype):

                if 'number_of_constraints' not in stat:
                    continue

                for k, v in stat['number_of_constraints'].items():
                    if 'hydrogen_bonds' in k:
                        hydrogen_bonds += v
                    elif 'disulfide_bonds' in k:
                        disulfide_bonds += v
                    elif 'diselenide_bonds' in k:
                        diselenide_bonds += v
                    elif 'other_bonds' in k:
                        other_bonds += v
                    elif k == 'symmetric_constraints':
                        symmetric += v
                    else:
                        if noe_exp_type is None:
                            noe_exp_type = stat['exp_type']
                        noe_like += v
            if noe_like > 0:
                if noe_exp_type.lower() == 'unknown':
                    noe_exp_type = 'NOE'  # ? (To be decided)'
                else:
                    _noe_exp_type = noe_exp_type.lower()
                    if _noe_exp_type in ('csp', 'chemical shift perturbation', 'shift_perturbation'):
                        noe_exp_type = 'CSP'
                    elif _noe_exp_type == 'noe':
                        noe_exp_type = 'NOE'
                    elif _noe_exp_type in ('noe buildup', 'noe build-up', 'noe_build_up'):
                        noe_exp_type = 'NOE buildup'
                    elif _noe_exp_type in ('noe not seen', 'noe_not_seen'):
                        noe_exp_type = 'NOE not seen'
                    elif _noe_exp_type in ('pre', 'paramagnetic relaxation'):
                        noe_exp_type = 'PRE'
                    elif _noe_exp_type == 'pre solvent':
                        noe_exp_type = 'PRE solvent'
                    elif _noe_exp_type == 'roe':
                        noe_exp_type = 'ROE'

                restraint = {'constraint_filename': file_name,
                             'software_name': file_type,
                             'constraint_type': 'distance',
                             'constraint_subtype': noe_exp_type,
                             'constraint_number': noe_like}
                restraints.append(restraint)
            if hydrogen_bonds > 0:
                restraint = {'constraint_filename': file_name,
                             'software_name': file_type,
                             'constraint_type': 'distance',
                             'constraint_subtype': 'hydrogen bond',
                             'constraint_number': hydrogen_bonds}
                restraints.append(restraint)
            if disulfide_bonds > 0:
                restraint = {'constraint_filename': file_name,
                             'software_name': file_type,
                             'constraint_type': 'distance',
                             'constraint_subtype': 'disulfide bond',
                             'constraint_number': disulfide_bonds}
                restraints.append(restraint)
            if diselenide_bonds > 0:
                restraint = {'constraint_filename': file_name,
                             'software_name': file_type,
                             'constraint_type': 'distance',
                             'constraint_subtype': 'diselenide bond',
                             'constraint_number': diselenide_bonds}
                restraints.append(restraint)
            if other_bonds > 0:
                restraint = {'constraint_filename': file_name,
                             'software_name': file_type,
                             'constraint_type': 'distance',
                             'constraint_subtype': 'other bond',
                             'constraint_number': other_bonds}
                restraints.append(restraint)
            if symmetric > 0:
                restraint = {'constraint_filename': file_name,
                             'software_name': file_type,
                             'constraint_type': 'distance',
                             'constraint_subtype': 'symmetry',
                             'constraint_number': symmetric}
                restraints.append(restraint)

        content_subtype = 'dihed_restraint'

        if content_subtype in content_subtypes:
            proteins = 0
            nucleic_acids = 0
            carbohydrates = 0
            others = 0
            for stat in self.getNmrStatsOfExptlData(content_subtype):

                if 'constraints_per_polymer_type' in stat:  # DAOTHER-6509
                    for k, v in stat['constraints_per_polymer_type'].items():
                        if k == 'protein':
                            proteins += v
                        elif k == 'nucleic_acid':
                            nucleic_acids += v
                        elif k == 'carbohydrate':
                            carbohydrates += v
                        elif k == 'other':
                            others += v
                elif 'number_of_constraints_per_polymer_type' in stat:  # DAOTHER-6509
                    for k, v in stat['number_of_constraints_per_polymer_type'].items():
                        if k == 'protein':
                            proteins += v
                        elif k == 'nucleic_acid':
                            nucleic_acids += v
                        elif k == 'carbohydrate':
                            carbohydrates += v
                        elif k == 'other':
                            others += v

            if proteins > 0:
                restraint = {'constraint_filename': file_name,
                             'software_name': file_type,
                             'constraint_type': 'protein dihedral angle',
                             'constraint_subtype': 'Not applicable',
                             'constraint_number': proteins}
                restraints.append(restraint)
            if nucleic_acids > 0:
                restraint = {'constraint_filename': file_name,
                             'software_name': file_type,
                             'constraint_type': 'nucleic acid dihedral angle',
                             'constraint_subtype': 'Not applicable',
                             'constraint_number': nucleic_acids}
                restraints.append(restraint)
            if carbohydrates > 0:
                restraint = {'constraint_filename': file_name,
                             'software_name': file_type,
                             'constraint_type': 'carbohydrate dihedral angle',
                             'constraint_subtype': 'Not applicable',
                             'constraint_number': carbohydrates}
                restraints.append(restraint)
            if others > 0:
                restraint = {'constraint_filename': file_name,
                             'software_name': file_type,
                             'constraint_type': 'other angle',
                             'constraint_subtype': 'Not applicable',
                             'constraint_number': others}
                restraints.append(restraint)

        content_subtype = 'rdc_restraint'

        if content_subtype in content_subtypes:
            rdc_total = 0
            for stat in self.getNmrStatsOfExptlData(content_subtype):

                if 'number_of_constraints' not in stat:
                    continue

                for k, v in stat['number_of_constraints'].items():
                    rdc_total += v

            restraint = {'constraint_filename': file_name,
                         'software_name': file_type,
                         'constraint_type': 'intervector projection angle',
                         'constraint_subtype': 'RDC',
                         'constraint_number': rdc_total}

            restraints.append(restraint)
        # """
        # content_subtype = 'plane_restraint'

        # if content_subtype in content_subtypes:
        #     proteins = 0
        #     nucleic_acids = 0
        #     for stat in self.getNmrStatsOfExptlData(content_subtype):

        #         if 'constraints_per_polymer_type' in stat:
        #             for k, v in stat['constraints_per_polymer_type'].items():
        #                 if k == 'protein':
        #                     proteins += v
        #                 elif k == 'nucleic_acid':
        #                     nucleic_acids += v
        #         elif 'number_of_constraints_per_polymer_type' in stat:  # DAOTHER-6509
        #             for k, v in stat['number_of_constraints_per_polymer_type'].items():
        #                 if k == 'protein':
        #                     proteins += v
        #                 elif k == 'nucleic_acid':
        #                     nucleic_acids += v

        #     if proteins > 0:
        #         restraint = {'constraint_filename': file_name,
        #                      'software_name': file_type,
        #                      'constraint_type': 'protein peptide planarity',
        #                      'constraint_subtype': 'peptide',
        #                      'constraint_number': proteins}
        #         restraints.append(restraint)
        #     if nucleic_acids > 0:
        #         restraint = {'constraint_filename': file_name,
        #                      'software_name': file_type,
        #                      'constraint_type': 'nucleic acid base planarity',
        #                      'constraint_subtype': 'ring',
        #                      'constraint_number': nucleic_acids}
        #         restraints.append(restraint)
        # """
        return restraints if len(restraints) > 0 else None

    def __getNmrRestraints(self):
        """ Return stats of NMR restraints. (legacy)
        """

        list_id = self.getInputSourceIdsOfNmrLegacyData()

        if len(list_id) == 0:
            return None

        restraints = []

        for lid in list_id:

            content_subtypes = self.getNmrLegacyContentSubTypes(lid)

            if content_subtypes is None:
                continue

            nmr_input_source_dic = self.getInputSourceDict(lid)

            if nmr_input_source_dic is None:
                continue

            file_name = nmr_input_source_dic['file_name']
            file_type = 'NEF' if nmr_input_source_dic['file_type'] == 'nef' else 'NMR-STAR'

            content_subtype = 'dist_restraint'

            if content_subtype in content_subtypes:

                stats = self.getNmrLegacyStatsOfExptlData(lid, content_subtype)

                if stats is None:
                    continue

                hydrogen_bonds = 0
                disulfide_bonds = 0
                diselenide_bonds = 0
                other_bonds = 0
                symmetric = 0
                noe_like = 0
                noe_exp_type = None

                for stat in stats:

                    if 'number_of_constraints' not in stat:
                        continue

                    for k, v in stat['number_of_constraints'].items():
                        if 'hydrogen_bonds' in k:
                            hydrogen_bonds += v
                        elif 'disulfide_bonds' in k:
                            disulfide_bonds += v
                        elif 'diselenide_bonds' in k:
                            diselenide_bonds += v
                        elif 'other_bonds' in k:
                            other_bonds += v
                        elif k == 'symmetric_constraints':
                            symmetric += v
                        else:
                            if noe_exp_type is None:
                                noe_exp_type = stat['exp_type']
                            noe_like += v
                if noe_like > 0:
                    if noe_exp_type.lower() == 'unknown':
                        noe_exp_type = 'NOE'  # ? (To be decided)'
                    else:
                        _noe_exp_type = noe_exp_type.lower()
                        if _noe_exp_type in ('csp', 'chemical shift perturbation', 'shift_perturbation'):
                            noe_exp_type = 'CSP'
                        elif _noe_exp_type == 'noe':
                            noe_exp_type = 'NOE'
                        elif _noe_exp_type in ('noe buildup', 'noe build-up', 'noe_build_up'):
                            noe_exp_type = 'NOE buildup'
                        elif _noe_exp_type in ('noe not seen', 'noe_not_seen'):
                            noe_exp_type = 'NOE not seen'
                        elif _noe_exp_type in ('pre', 'paramagnetic relaxation'):
                            noe_exp_type = 'PRE'
                        elif _noe_exp_type == 'pre solvent':
                            noe_exp_type = 'PRE solvent'
                        elif _noe_exp_type == 'roe':
                            noe_exp_type = 'ROE'

                    restraint = {'constraint_filename': file_name,
                                 'software_name': file_type,
                                 'constraint_type': 'distance',
                                 'constraint_subtype': noe_exp_type,
                                 'constraint_number': noe_like}
                    restraints.append(restraint)
                if hydrogen_bonds > 0:
                    restraint = {'constraint_filename': file_name,
                                 'software_name': file_type,
                                 'constraint_type': 'distance',
                                 'constraint_subtype': 'hydrogen bond',
                                 'constraint_number': hydrogen_bonds}
                    restraints.append(restraint)
                if disulfide_bonds > 0:
                    restraint = {'constraint_filename': file_name,
                                 'software_name': file_type,
                                 'constraint_type': 'distance',
                                 'constraint_subtype': 'disulfide bond',
                                 'constraint_number': disulfide_bonds}
                    restraints.append(restraint)
                if diselenide_bonds > 0:
                    restraint = {'constraint_filename': file_name,
                                 'software_name': file_type,
                                 'constraint_type': 'distance',
                                 'constraint_subtype': 'diselenide bond',
                                 'constraint_number': diselenide_bonds}
                    restraints.append(restraint)
                if other_bonds > 0:
                    restraint = {'constraint_filename': file_name,
                                 'software_name': file_type,
                                 'constraint_type': 'distance',
                                 'constraint_subtype': 'other bond',
                                 'constraint_number': other_bonds}
                    restraints.append(restraint)
                if symmetric > 0:
                    restraint = {'constraint_filename': file_name,
                                 'software_name': file_type,
                                 'constraint_type': 'distance',
                                 'constraint_subtype': 'symmetry',
                                 'constraint_number': symmetric}
                    restraints.append(restraint)

            content_subtype = 'dihed_restraint'

            if content_subtype in content_subtypes:

                stats = self.getNmrLegacyStatsOfExptlData(lid, content_subtype)

                if stats is None:
                    continue

                proteins = 0
                nucleic_acids = 0
                carbohydrates = 0
                others = 0

                for stat in stats:

                    if 'constraints_per_polymer_type' in stat:  # DAOTHER-6509
                        for k, v in stat['constraints_per_polymer_type'].items():
                            if k == 'protein':
                                proteins += v
                            elif k == 'nucleic_acid':
                                nucleic_acids += v
                            elif k == 'carbohydrate':
                                carbohydrates += v
                            elif k == 'other':
                                others += v
                    elif 'number_of_constraints_per_polymer_type' in stat:  # DAOTHER-6509
                        for k, v in stat['number_of_constraints_per_polymer_type'].items():
                            if k == 'protein':
                                proteins += v
                            elif k == 'nucleic_acid':
                                nucleic_acids += v
                            elif k == 'carbohydrate':
                                carbohydrates += v
                            elif k == 'other':
                                others += v

                if proteins > 0:
                    restraint = {'constraint_filename': file_name,
                                 'software_name': file_type,
                                 'constraint_type': 'protein dihedral angle',
                                 'constraint_subtype': 'Not applicable',
                                 'constraint_number': proteins}
                    restraints.append(restraint)
                if nucleic_acids > 0:
                    restraint = {'constraint_filename': file_name,
                                 'software_name': file_type,
                                 'constraint_type': 'nucleic acid dihedral angle',
                                 'constraint_subtype': 'Not applicable',
                                 'constraint_number': nucleic_acids}
                    restraints.append(restraint)
                if carbohydrates > 0:
                    restraint = {'constraint_filename': file_name,
                                 'software_name': file_type,
                                 'constraint_type': 'carbohydrate dihedral angle',
                                 'constraint_subtype': 'Not applicable',
                                 'constraint_number': carbohydrates}
                    restraints.append(restraint)
                if others > 0:
                    restraint = {'constraint_filename': file_name,
                                 'software_name': file_type,
                                 'constraint_type': 'other angle',
                                 'constraint_subtype': 'Not applicable',
                                 'constraint_number': others}
                    restraints.append(restraint)

            content_subtype = 'rdc_restraint'

            if content_subtype in content_subtypes:

                stats = self.getNmrLegacyStatsOfExptlData(lid, content_subtype)

                if stats is None:
                    continue

                rdc_total = 0

                for stat in stats:

                    if 'number_of_constraints' not in stat:
                        continue

                    for k, v in stat['number_of_constraints'].items():
                        rdc_total += v

                restraint = {'constraint_filename': file_name,
                             'software_name': file_type,
                             'constraint_type': 'intervector projection angle',
                             'constraint_subtype': 'RDC',
                             'constraint_number': rdc_total}

                restraints.append(restraint)

        return restraints if len(restraints) > 0 else None

    def getNmrPeaks(self):
        """ Return stats of NMR spectral peaks.
        """

        content_subtypes = self.getNmrContentSubTypes()

        if content_subtypes is None:
            return self.__getNmrPeaks()

        spectral_peaks = []

        content_subtype = 'spectral_peak'

        if content_subtype in content_subtypes:
            for stat in self.getNmrStatsOfExptlData(content_subtype):
                spectral_peaks.append({'list_id': stat['list_id'],
                                       'sf_framecode': stat['sf_framecode'],
                                       'number_of_spectral_dimensions': stat['number_of_spectral_dimensions'],
                                       'spectral_dim': stat['spectral_dim']})

        content_subtype = 'spectral_peak_alt'

        if content_subtype in content_subtypes:
            for stat in self.getNmrStatsOfExptlData(content_subtype):
                spectral_peaks.append({'list_id': stat['list_id'],
                                       'sf_framecode': stat['sf_framecode'],
                                       'number_of_spectral_dimensions': stat['number_of_spectral_dimensions'],
                                       'spectral_dim': stat['spectral_dim']})

        return spectral_peaks

    def __getNmrPeaks(self):
        """ Return stats of NMR spectral peaks. (legacy)
        """

        list_id = self.getInputSourceIdsOfNmrLegacyData()

        if len(list_id) == 0:
            return []

        spectral_peaks = []

        content_subtype = 'spectral_peak'

        for lid in list_id:

            content_subtypes = self.getNmrLegacyContentSubTypes(lid)

            if content_subtypes is None:
                continue

            stats = self.getNmrLegacyStatsOfExptlData(lid, content_subtype)

            if stats is None:
                continue

            for stat in stats:
                spectral_peaks.append({'list_id': stat['list_id'],
                                       'sf_framecode': stat['sf_framecode'],
                                       'number_of_spectral_dimensions': stat['number_of_spectral_dimensions'],
                                       'spectral_dim': stat['spectral_dim']})

        content_subtype = 'spectral_peak_alt'

        for lid in list_id:

            content_subtypes = self.getNmrLegacyContentSubTypes(lid)

            if content_subtypes is None:
                continue

            stats = self.getNmrLegacyStatsOfExptlData(lid, content_subtype)

            if stats is None:
                continue

            for stat in stats:
                spectral_peaks.append({'list_id': stat['list_id'],
                                       'sf_framecode': stat['sf_framecode'],
                                       'number_of_spectral_dimensions': stat['number_of_spectral_dimensions'],
                                       'spectral_dim': stat['spectral_dim']})

        return spectral_peaks

    def getNmrIsotopes(self):
        """ Return set of isotopes in assigned chemical shifts.
        """

        content_subtypes = self.getNmrContentSubTypes()

        if content_subtypes is None:
            return self.__getNmrIsotopes()

        content_subtype = 'chem_shift'

        if content_subtype not in content_subtypes:
            return None

        isotopes = {}

        pat = re.compile(r'^(\d+)(\D)$')

        for stat in self.getNmrStatsOfExptlData(content_subtype):
            if 'number_of_assignments' in stat:
                for k in stat['number_of_assignments'].keys():
                    try:
                        g = pat.search(k.split('_')[0].upper()).groups()
                        isotopes[g[0]] = g[1]
                    except AttributeError:
                        pass

        return None if len(isotopes) == 0 else isotopes

    def __getNmrIsotopes(self):
        """ Return set of isotopes in assigned chemical shifts. (legacy)
        """

        list_id = self.getInputSourceIdsOfNmrLegacyData()

        if len(list_id) == 0:
            return None

        content_subtype = 'chem_shift'

        isotopes = {}

        pat = re.compile(r'^(\d+)(\D)$')

        for lid in list_id:

            content_subtypes = self.getNmrLegacyContentSubTypes(lid)

            if content_subtypes is None:
                continue

            stats = self.getNmrLegacyStatsOfExptlData(lid, content_subtype)

            if stats is None:
                continue

            for stat in stats:
                if 'number_of_assignments' in stat:
                    for k in stat['number_of_assignments'].keys():
                        try:
                            g = pat.search(k.split('_')[0].upper()).groups()
                            isotopes[g[0]] = g[1]
                        except AttributeError:
                            pass

        return None if len(isotopes) == 0 else isotopes

    def getNmrChemShiftRefs(self):
        """ Return stats of NMR chemical shift references.
        """

        content_subtypes = self.getNmrContentSubTypes()

        if content_subtypes is None:
            return self.__getNmrChemShiftRefs()

        content_subtype = 'chem_shift_ref'

        if content_subtype not in content_subtypes:
            return None

        chem_shift_refs = []

        for stat in self.getNmrStatsOfExptlData(content_subtype):
            loop = []

            if stat['loop'] is not None:
                for el in stat['loop']:
                    _l = {}
                    for k, v in el.items():
                        if v is None or k == 'Entry_ID':
                            continue
                        _l[k.lower()] = v
                    loop.append(_l)

            saveframe_tag = {}

            if stat['saveframe_tag'] is not None:
                for k, v in stat['saveframe_tag'].items():
                    if v is None or k == 'Entry_ID' or k.startswith('Sf_'):
                        continue
                    saveframe_tag[k.lower()] = v

            chem_shift_refs.append({'list_id': stat['list_id'], 'sf_framecode': stat['sf_framecode'], 'loop': loop, 'saveframe_tag': saveframe_tag})

        return chem_shift_refs

    def __getNmrChemShiftRefs(self):
        """ Return stats of NMR chemical shift references. (legacy)
        """

        list_id = self.getInputSourceIdsOfNmrLegacyData()

        if len(list_id) == 0:
            return None

        content_subtype = 'chem_shift_ref'

        chem_shift_refs = []

        for lid in list_id:

            content_subtypes = self.getNmrLegacyContentSubTypes(lid)

            if content_subtypes is None:
                continue

            stats = self.getNmrLegacyStatsOfExptlData(lid, content_subtype)

            if stats is None:
                continue

            for stat in stats:
                loop = []

                if stat['loop'] is not None:
                    for el in stat['loop']:
                        _l = {}
                        for k, v in el.items():
                            if v is None or k == 'Entry_ID':
                                continue
                            _l[k.lower()] = v
                        loop.append(_l)

                saveframe_tag = {}

                if stat['saveframe_tag'] is not None:
                    for k, v in stat['saveframe_tag'].items():
                        if v is None or k == 'Entry_ID' or k.startswith('Sf_'):
                            continue
                        saveframe_tag[k.lower()] = v

                chem_shift_refs.append({'list_id': stat['list_id'], 'sf_framecode': stat['sf_framecode'], 'loop': loop, 'saveframe_tag': saveframe_tag})

        return None if len(chem_shift_refs) == 0 else chem_shift_refs

    def getPolymerSequenceByInputSrcId(self, input_source_id):
        """ Retrieve polymer sequence of a given input_source_id.
        """

        return get_value_safe(self.getInputSourceDict(input_source_id), 'polymer_sequence')

    def getNmrPolymerSequenceOf(self, nmr_chain_id):
        """ Retrieve NMR polymer sequence having a given chain_id.
        """

        sid = self.getInputSourceIdOfNmrData()

        if sid < 0:
            ids = self.getInputSourceIdsOfNmrLegacyData()
            if len(ids) == 0:
                return None
            sid = ids[0]

        nmr_polymer_sequence = self.getPolymerSequenceByInputSrcId(sid)

        if nmr_polymer_sequence is None:
            return None

        return next((ps for ps in nmr_polymer_sequence if ps['chain_id'] == nmr_chain_id), None)

    def getModelPolymerSequenceOf(self, cif_chain_id, label_scheme=True):
        """ Retrieve model polymer sequence having a given chain_id.
        """

        cif_polymer_sequence = self.getPolymerSequenceByInputSrcId(self.getInputSourceIdOfCoord())

        if cif_polymer_sequence is None:
            return None

        return next((ps for ps in cif_polymer_sequence
                     if (ps['chain_id'] == cif_chain_id and label_scheme)
                     or ('auth_chain_id' in ps and ps['auth_chain_id'] == cif_chain_id and not label_scheme)), None)

    def getChainIdsForSameEntity(self):
        """ Return mapping of chain_id in the NMR data, which share the same entity.
        """

        sid = self.getInputSourceIdOfNmrData()

        if sid < 0:
            ids = self.getInputSourceIdsOfNmrLegacyData()
            if len(ids) == 0:
                return None
            sid = ids[0]

        nmr_polymer_sequence = self.getPolymerSequenceByInputSrcId(sid)

        if nmr_polymer_sequence is None:
            return None

        ret = {}

        for ps in nmr_polymer_sequence:
            if 'identical_chain_id' in ps:
                ret[ps['chain_id']] = ps['identical_chain_id']

        if len(ret) == 0:
            return None

        return ret

    def getAsymIdsForSameEntity(self):
        """ Return mapping of asym_id in the coordinates, which share the same entity.
        """

        cif_polymer_sequence = self.getPolymerSequenceByInputSrcId(self.getInputSourceIdOfCoord())

        if cif_polymer_sequence is None:
            return None

        ret = {}

        for ps in cif_polymer_sequence:
            if 'identical_chain_id' in ps:
                ret[ps['chain_id']] = ps['identical_chain_id']

        if len(ret) == 0:
            return None

        return ret

    def getNmrSeq1LetterCodeOf(self, nmr_chain_id, fullSequence=True, unmappedSeqId=None):
        """ Retrieve NMR polymer sequence (1-letter code) having a given chain_id.
        """

        sid = self.getInputSourceIdOfNmrData()

        if sid < 0:
            ids = self.getInputSourceIdsOfNmrLegacyData()
            if len(ids) == 0:
                return None
            sid = ids[0]

        nmr_polymer_sequence = self.getPolymerSequenceByInputSrcId(sid)

        if nmr_polymer_sequence is None:
            return None

        ps = next((ps for ps in nmr_polymer_sequence if ps['chain_id'] == nmr_chain_id), None)

        if ps is None:
            return None

        code = ''

        for seq_id, comp_id in zip(ps['seq_id'], ps['comp_id']):

            if not fullSequence and unmappedSeqId is not None and seq_id in unmappedSeqId:
                continue

            if comp_id in monDict3:
                code += monDict3[comp_id]
            elif comp_id in emptyValue:
                code += ' '
            else:
                code += '(' + comp_id + ')'

        return code

    def getModelSeq1LetterCodeOf(self, cif_chain_id, label_scheme=True):
        """ Retrieve model polymer sequence (1-letter code) having a given chain_id.
        """

        cif_polymer_sequence = self.getPolymerSequenceByInputSrcId(self.getInputSourceIdOfCoord())

        if cif_polymer_sequence is None:
            return None

        ps = next((ps for ps in cif_polymer_sequence
                   if (ps['chain_id'] == cif_chain_id and label_scheme)
                   or ('auth_chain_id' in ps and ps['auth_chain_id'] == cif_chain_id and not label_scheme)), None)

        if ps is None:
            return None

        code = ''
        for comp_id in ps['comp_id']:
            if comp_id in monDict3:
                code += monDict3[comp_id]
            elif comp_id in emptyValue:
                code += ' '
            else:
                code += '(' + comp_id + ')'

        return code

    def getNmrPolymerSequenceWithModelChainId(self, cif_chain_id, label_scheme=True):
        """ Retrieve NMR polymer sequence corresponding to a given coordinate chain_id.
        """

        chain_assigns = get_value_safe(self.chain_assignment.get(), 'model_poly_seq_vs_nmr_poly_seq')

        if chain_assigns is None:
            return None

        for chain_assign in chain_assigns:

            if (chain_assign['ref_chain_id'] == cif_chain_id and label_scheme) or\
               ('ref_auth_chain_id' in chain_assign and chain_assign['ref_auth_chain_id'] == cif_chain_id and not label_scheme):
                return self.getNmrPolymerSequenceOf(chain_assign['test_chain_id'])

        return None

    def getSequenceAlignmentWithNmrChainId(self, nmr_chain_id):
        """ Retrieve sequence alignment (nmr vs model) of a given NMR chain_id.
        """

        key = 'nmr_poly_seq_vs_model_poly_seq'

        chain_assigns = get_value_safe(self.chain_assignment.get(), key)

        if chain_assigns is None:
            return None

        for chain_assign in chain_assigns:

            if chain_assign['ref_chain_id'] == nmr_chain_id:

                if chain_assign['conflict'] > 0:
                    return None

                cif_chain_id = chain_assign['test_chain_id']

                sequence_aligns = get_value_safe(self.sequence_alignment.get(), key)

                if sequence_aligns is None:
                    return None

                for sequence_align in sequence_aligns:

                    if sequence_align['ref_chain_id'] == nmr_chain_id and sequence_align['test_chain_id'] == cif_chain_id:

                        if sequence_align['conflict'] > 0:
                            return None

                        return sequence_align

        return None

    def getSequenceAlignmentWithModelChainId(self, cif_chain_id, label_scheme=True):
        """ Retrieve sequence alignment (model vs nmr) of a given coordinate chain_id.
        """

        key = 'model_poly_seq_vs_nmr_poly_seq'

        chain_assigns = get_value_safe(self.chain_assignment.get(), key)

        if chain_assigns is None:
            return None

        for chain_assign in chain_assigns:

            if (chain_assign['ref_chain_id'] == cif_chain_id and label_scheme) or\
               ('ref_auth_chain_id' in chain_assign and chain_assign['ref_auth_chain_id'] == cif_chain_id and not label_scheme):

                if chain_assign['conflict'] > 0:
                    return None

                _cif_chain_id = chain_assign['ref_chain_id']

                nmr_chain_id = chain_assign['test_chain_id']

                sequence_aligns = get_value_safe(self.sequence_alignment.get(), key)

                if sequence_aligns is None:
                    return None

                for sequence_align in sequence_aligns:

                    if sequence_align['ref_chain_id'] == _cif_chain_id and sequence_align['test_chain_id'] == nmr_chain_id:

                        if sequence_align['conflict'] > 0:
                            return None

                        return sequence_align

        return None

    def getModelPolymerSequenceWithNmrChainId(self, nmr_chain_id):
        """ Retrieve coordinate polymer sequence corresponding to a given NMR chain_id.
        """

        chain_assigns = get_value_safe(self.chain_assignment.get(), 'nmr_poly_seq_vs_model_poly_seq')

        if chain_assigns is None:
            return None

        for chain_assign in chain_assigns:

            if chain_assign['ref_chain_id'] == nmr_chain_id:
                return self.getModelPolymerSequenceOf(chain_assign['test_chain_id'])

        return None

    def getNmrSeq1LetterCodeWithModelChainId(self, cif_chain_id, label_scheme=True):
        """ Retrieve NMR polymer sequence (1-letter code) corresponding to a given coordinate chain_id.
        """

        fullSeqeucne = self.getInputSourceIdOfNmrData() != -1
        unmappedSeqId = []

        chain_assign_dic = self.chain_assignment.get()

        chain_assigns = get_value_safe(chain_assign_dic, 'model_poly_seq_vs_nmr_poly_seq')

        if chain_assigns is None:
            return None

        if not fullSeqeucne:

            _chain_assigns = get_value_safe(chain_assign_dic, 'nmr_poly_seq_vs_model_poly_seq')

            if _chain_assigns is not None:

                for _chain_assign in _chain_assigns:

                    if (_chain_assign['test_chain_id'] == cif_chain_id and label_scheme) or\
                       ('test_auth_chain_id' in _chain_assign and _chain_assign['test_auth_chain_id'] == cif_chain_id and not label_scheme):

                        if 'unmapped_sequence' in _chain_assign:

                            for unmapped_sequence in _chain_assign['unmapped_sequence']:
                                unmappedSeqId.append(unmapped_sequence['ref_seq_id'])

                        break

        for chain_assign in chain_assigns:

            if (chain_assign['ref_chain_id'] == cif_chain_id and label_scheme) or\
               ('ref_auth_chain_id' in chain_assign and chain_assign['ref_auth_chain_id'] == cif_chain_id and not label_scheme):
                return self.getNmrSeq1LetterCodeOf(chain_assign['test_chain_id'], fullSequence=fullSeqeucne, unmappedSeqId=unmappedSeqId)

        return None

    def getModelSeq1LetterCodeWithNmrChainId(self, nmr_chain_id):
        """ Retrieve coordinate polymer sequence (1-letter code) corresponding to a given NMR chain_id.
        """

        chain_assigns = get_value_safe(self.chain_assignment.get(), 'nmr_poly_seq_vs_model_poly_seq')

        if chain_assigns is None:
            return None

        for chain_assign in chain_assigns:

            if chain_assign['ref_chain_id'] == nmr_chain_id:
                return self.getModelSeq1LetterCodeOf(chain_assign['test_chain_id'])

        return None

    def getAverageRMSDWithinRange(self, cif_chain_id, cif_beg_seq_id, cif_end_seq_id, label_scheme=True):
        """ Calculate average RMSD of alpha carbons/phosphates within a given range in the ensemble.
        """

        poly_seq = self.getModelPolymerSequenceOf(cif_chain_id, label_scheme)

        if poly_seq is None or 'type' not in poly_seq:
            return None

        stype = poly_seq['type']

        if 'polypeptide' in stype:
            rmsd_label = 'ca_rmsd'
        elif 'ribonucleotide' in stype:
            rmsd_label = 'p_rmsd'
        else:
            return None

        if rmsd_label not in poly_seq:
            return None

        if not (cif_beg_seq_id in poly_seq['seq_id'] and cif_end_seq_id in poly_seq['seq_id'] and label_scheme)\
           and not('auth_seq_id' in poly_seq and cif_beg_seq_id in poly_seq['auth_seq_id'] and cif_end_seq_id in poly_seq['auth_seq_id'] and not label_scheme):
            return None

        if label_scheme:
            rmsd = [s[rmsd_label] for s in poly_seq if s['seq_id'] >= cif_beg_seq_id and s['seq_id'] <= cif_end_seq_id and s[rmsd_label] is not None]
        else:
            rmsd = [s[rmsd_label] for s in poly_seq if s['auth_seq_id'] >= cif_beg_seq_id and s['auth_seq_id'] <= cif_end_seq_id and s[rmsd_label] is not None]

        if len(rmsd) == 0:
            return None

        return sum(rmsd) / len(rmsd)

    def getTotalErrors(self):
        """ Return total number of errors.
        """

        return self.error.getTotal()

    def getTotalWarnings(self):
        """ Return total number of warnings.
        """

        return self.warning.getTotal()

    def __setStatus(self, status):
        """ Set processing status.
        """

        if status in self.status_codes:
            self.__report['information']['status'] = status
        else:
            logging.error('+NmrDpReport.__setStatus() ++ Error  - Unknown status %s', status)
            raise KeyError(f"+NmrDpReport.__setStatus() ++ Error  - Unknown status {status}")

    def setError(self):
        """ Set processing status Error.
        """

        if not self.__immutable:
            self.__report['error'] = self.error.get()

            self.__setStatus('Error')

        else:
            logging.warning('+NmrDpReport.setError() ++ Warning  - No effects on NMR data processing report because the report is immutable')
            raise UserWarning('+NmrDpReport.setError() ++ Warning  - No effects on NMR data processing report because the report is immutable')

    def setWarning(self):
        """ Set processing status Warning.
        """

        if not self.__immutable:
            self.__report['warning'] = self.warning.get()

            if not self.isError():
                self.__setStatus('Warning')

        else:
            logging.warning('+NmrDpReport.setWarning() ++ Warning  - No effects on NMR data processing report because the report is immutable')
            raise UserWarning('+NmrDpReport.setWarning() ++ Warning  - No effects on NMR data processing report because the report is immutable')

    def clean(self):
        """ Clear errors and warnings.
        """

        if not self.__immutable:

            self.error.clean()
            self.warning.clean()

            self.__report['error'] = None if self.error.getTotal() == 0 else self.error.get()
            self.__report['warning'] = None if self.warning.getTotal() == 0 else self.warning.get()

        else:
            logging.warning('+NmrDpReport.clean() ++ Warning  - No effects on NMR data processing report because the report is immutable')
            raise UserWarning('+NmrDpReport.clean() ++ Warning  - No effects on NMR data processing report because the report is immutable')

    def setDiamagnetic(self, diamagnetic):
        """ Set diamagetism of molecular assembly.
        """

        if isinstance(diamagnetic, bool):
            self.__report['information']['diamagnetic'] = diamagnetic

        else:
            logging.warning('+NmrDpReport.setDiamagnetic() ++ Warning  - No effects on NMR data processing report because input variable is not boolean type')
            raise UserWarning('+NmrDpReport.setDiamagnetic() ++ Warning  - No effects on NMR data processing report because input variable is not boolean type')

    def setDisulfideBond(self, disulfide_bond):
        """ Set whether molecular assembly has a disulfide bond at least or not.
        """

        if isinstance(disulfide_bond, bool):
            self.__report['information']['disulfide_bond'] = disulfide_bond

        else:
            logging.warning('+NmrDpReport.setDisulfideBond() ++ Warning  - No effects on NMR data processing report because input variable is not boolean type')
            raise UserWarning('+NmrDpReport.setDisulfideBond() ++ Warning  - No effects on NMR data processing report because input variable is not boolean type')

    def setOtherBond(self, other_bond):
        """ Set whether molecular assemble has an other bond at least or not.
        """

        if isinstance(other_bond, bool):
            self.__report['information']['other_bond'] = other_bond

        else:
            logging.warning('+NmrDpReport.setOtherBond() ++ Warning  - No effects on NMR data processing report because input variable is not boolean type')
            raise UserWarning('+NmrDpReport.setOtherBond() ++ Warning  - No effects on NMR data processing report because input variable is not boolean type')

    def setCyclicPolymer(self, cyclic_polymer):
        """ Set whether molecular assemble contains a cyclic polymer or not.
        """

        if isinstance(cyclic_polymer, bool):
            self.__report['information']['cyclic_polymer'] = cyclic_polymer

        else:
            logging.warning('+NmrDpReport.setCyclicPolymer() ++ Warning  - No effects on NMR data processing report because input variable is not boolean type')
            raise UserWarning('+NmrDpReport.setCyclicPolymer() ++ Warning  - No effects on NMR data processing report because input variable is not boolean type')

    def setMutable(self):
        """ Enable to mute the report.
        """

        self.__immutable = False

    def get(self):
        """ Return NMR data processing report.
        """

        if not self.__immutable:
            self.__report['information']['input_sources'] = [input_source.get() for input_source in self.input_sources]
            self.__report['information']['sequence_alignments'] = self.sequence_alignment.get()
            self.__report['information']['chain_assignments'] = self.chain_assignment.get()

            self.__immutable = True

        return self.__report

    def load(self, report):
        """ Retrieve NMR data processing report from JSON content.
            @return: True for success or False otherwise
        """

        if report is None:
            return False

        self.__report = copy.copy(report)

        self.input_sources = []

        for contents in self.__report['information']['input_sources']:

            input_source = NmrDpReportInputSource()
            input_source.put(contents)

            self.input_sources.append(input_source)

        self.sequence_alignment.put(self.__report['information']['sequence_alignments'])
        self.chain_assignment.put(self.__report['information']['chain_assignments'])

        if self.__report['error'] is None:
            self.error = NmrDpReportError()
        else:
            self.error.put(self.__report['error'])

        if self.__report['warning'] is None:
            self.warning = NmrDpReportWarning()
        else:
            self.warning.put(self.__report['warning'])

        self.setMutable()

        return True

    def writeFile(self, out_path):
        """ Write NMR data processing report as JSON file.
            @return: True for success or False otherwise
        """

        if self.get() is None:
            return False

        with open(out_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.get(), indent=2))

        return True

    def loadFile(self, in_path):
        """ Retrieve NMR data processing report from JSON file.
            @return: True for success or False otherwise
        """

        with open(in_path, 'r', encoding='utf-8') as file:

            report = json.loads(file.read())

            if report is None:
                return False

            self.load(report)

        return True

    def inheritFormatIssueErrors(self, prev_report):
        """ Inherit format issue errors from the previous report (e.g. nmr-*-consistency-check workflow operation).
        """

        item = 'format_issue'

        if not self.__immutable:

            file_name = self.input_sources[self.getInputSourceIdOfNmrData()].get()['file_name']
            _file_name = prev_report.input_sources[prev_report.getInputSourceIdOfNmrData()].get()['file_name']

            value_list = prev_report.error.getValueList(item, _file_name)

            if value_list is None:
                return

            for c in value_list:

                if 'file_name' in c:
                    c['file_name'] = file_name

                self.error.appendDescription(item, c)

        else:
            logging.warning('+NmrDpReport.inheritFormatIssueErrors() ++ Warning  - No effects on NMR data processing report because the report is immutable')
            raise UserWarning('+NmrDpReport.inheritFormatIssueErrors() ++ Warning  - No effects on NMR data processing report because the report is immutable')

    def inheritCorrectedFormatIssueWarnings(self, prev_report):
        """ Inherit corrected format issue warnings from the previous report (e.g. nmr-*-consistency-check workflow operation).
        """

        item = 'corrected_format_issue'

        if not self.__immutable:

            file_name = self.input_sources[self.getInputSourceIdOfNmrData()].get()['file_name']
            _file_name = prev_report.input_sources[prev_report.getInputSourceIdOfNmrData()].get()['file_name']

            value_list = prev_report.warning.getValueList(item, _file_name)

            if value_list is None:
                return

            for c in value_list:

                if 'file_name' in c:
                    c['file_name'] = file_name

                self.warning.appendDescription(item, c)

        else:
            logging.warning('+NmrDpReport.inheritCorrectedFormatIssueWarnings() ++ Warning  - No effects on NMR data processing report because the report is immutable')
            raise UserWarning('+NmrDpReport.inheritCorrectedFormatIssueWarnings() ++ Warning  - No effects on NMR data processing report because the report is immutable')

    def inheritCorrectedSaveframeNameWarnings(self, prev_report):
        """ Inherit corrected saveframe name warnings from the previous report (e.g. nmr-*-consistency-check workflow operation).
        """

        item = 'corrected_saveframe_name'

        if not self.__immutable:

            file_name = self.input_sources[self.getInputSourceIdOfNmrData()].get()['file_name']
            _file_name = prev_report.input_sources[prev_report.getInputSourceIdOfNmrData()].get()['file_name']

            value_list = prev_report.warning.getValueList(item, _file_name)

            if value_list is None:
                return

            for c in value_list:

                if 'file_name' in c:
                    c['file_name'] = file_name

                self.warning.appendDescription(item, c)

        else:
            logging.warning('+NmrDpReport.inheritCorrectedSaveframeNameWarnings() ++ Warning  - No effects on NMR data processing report because the report is immutable')
            raise UserWarning('+NmrDpReport.inheritCorrectedSaveframeNameWarnings() ++ Warning  - No effects on NMR data processing report because the report is immutable')

    def setCorrectedError(self, prev_report):
        """ Initialize history of corrected errors in the previous report.
        """

        if not self.__immutable:

            file_name = self.input_sources[self.getInputSourceIdOfNmrData()].get()['file_name']
            _file_name = prev_report.input_sources[prev_report.getInputSourceIdOfNmrData()].get()['file_name']

            for item in prev_report.error.get().keys():

                if item == 'total':
                    continue

                value_list = self.error.getValueList(item, file_name)
                _value_list = prev_report.error.getUniqueValueList(item, _file_name)

                if _value_list is None:
                    continue

                tlist = []

                for _c in _value_list:

                    if value_list is None or\
                       not any(c for c in value_list
                               if 'sf_framecode' in c and 'sf_framecode' in _c and c['sf_framecode'] == _c['sf_framecode'] and c['description'] == _c['description']):
                        tlist.append(_c)

                for c in tlist:
                    self.error.appendDescription(item, c)

                if len(tlist) > 0:
                    self.setError()

        else:
            logging.warning('+NmrDpReport.setCorrectedError() ++ Warning  - No effects on NMR data processing report because the report is immutable')
            raise UserWarning('+NmrDpReport.setCorrectedError() ++ Warning  - No effects on NMR data processing report because the report is immutable')

    def setCorrectedWarning(self, prev_report):
        """ Initialize history of corrected warnings in the previous report.
        """

        if not self.__immutable:

            ignorable_warning_types = ['auth_atom_nomenclature_mismatch', 'ccd_mismatch', 'disordered_index', 'enum_mismatch_ignorable',
                                       'skipped_saveframe_category', 'skipped_loop_category',
                                       'anomalous_chemical_shift', 'unusual_chemical_shift',
                                       'complemented_chemical_shift', 'incompletely_assigned_chemical_shift', 'incompletely_assigned_spectral_peak',
                                       'anomalous_data', 'unusual_data', 'unusual/rare_data', 'insufficient_data', 'conflicted_data', 'inconsistent_data',
                                       'total']

            self.corrected_warning = NmrDpReportWarning()

            file_name = self.input_sources[self.getInputSourceIdOfNmrData()].get()['file_name']
            _file_name = prev_report.input_sources[prev_report.getInputSourceIdOfNmrData()].get()['file_name']

            for item in prev_report.warning.get().keys():

                if item in ignorable_warning_types:
                    continue

                value_list = self.warning.getValueList(item, file_name)
                _value_list = prev_report.warning.getUniqueValueList(item, _file_name)

                if _value_list is None:
                    continue

                tlist = []

                for _c in _value_list:

                    if value_list is None or not any(c for c in value_list
                                                     if 'sf_framecode' in c and 'sf_framecode' in _c
                                                     and c['sf_framecode'] == _c['sf_framecode']
                                                     and c['description'] == _c['description']):
                        tlist.append(_c)

                for c in tlist:
                    self.corrected_warning.appendDescription(item, c)

            if self.corrected_warning.getTotal() > 0:
                self.__report['corrected_warning'] = self.corrected_warning.get()

            else:
                self.corrected_warning = None

        else:
            logging.warning('+NmrDpReport.setCorrectedWarning() ++ Warning  - No effects on NMR data processing report because the report is immutable')
            raise UserWarning('+NmrDpReport.setCorrectedWarning() ++ Warning  - No effects on NMR data processing report because the report is immutable')


class NmrDpReportInputSource:
    """ Wrapper class for data processing report of NMR data (input source).
    """

    def __init__(self):
        self.items = ('file_name', 'file_type', 'original_file_name', 'content_type', 'content_subtype',
                      'polymer_sequence', 'polymer_sequence_in_loop',
                      'non_standard_residue', 'disulfide_bond', 'other_bond',
                      'stats_of_exptl_data')
        self.file_types = ('pdbx',
                           'nef', 'nmr-star',
                           'nm-res-amb', 'nm-res-cns', 'nm-res-cya', 'nm-res-xpl', 'nm-res-oth',
                           'nm-aux-amb', 'nm-res-ros', 'nm-res-bio', 'nm-res-mr')
        self.content_types = ('model',
                              'nmr-data-nef', 'nmr-data-str',
                              'nmr-chemical-shifts', 'nmr-restraints')
        self.content_subtypes = ('coordinate', 'non_poly', 'entry_info', 'poly_seq', 'entity', 'chem_shift',
                                 'chem_shift_ref', 'dist_restraint', 'dihed_restraint', 'rdc_restraint',
                                 'plane_restraint', 'adist_restraint', 'jcoup_restraint', 'hvycs_restraint',
                                 'procs_restraint', 'rama_restraint', 'radi_restraint', 'diff_restraint',
                                 'nbase_restraint', 'csa_restraint', 'ang_restraint', 'pre_restraint',
                                 'pcs_restraint', 'prdc_restraint', 'pang_restraint', 'pccr_restraint',
                                 'hbond_restraint', 'geo_restraint', 'noepk_restraint',
                                 'spectral_peak', 'spectral_peak_alt', 'topology')

        self.__contents = {item: None for item in self.items}

    def setItemValue(self, item, value):
        """ Set an item with a given value.
        """

        if item in self.items:

            if item == 'file_type' and value not in self.file_types:
                logging.error('+NmrDpReportInputSource.setItemValue() ++ Error  - Unknown file type %s', value)
                raise ValueError(f"+NmrDpReportInputSource.setItemValue() ++ Error  - Unknown file type {value}")

            if item == 'content_type' and value not in self.content_types:
                logging.error('+NmrDpReportInputSource.setItemValue() ++ Error  - Unknown content type %s', value)
                raise ValueError(f"+NmrDpReportInputSource.setItemValue() ++ Error  - Unknown content type {value}")

            if item == 'content_subtype':

                for key in value:

                    if key not in self.content_subtypes:
                        logging.error('+NmrDpReportInputSource.setItemValue() ++ Error  - Unknown content subtype in %s', value.keys())
                        raise ValueError(f"+NmrDpReportInputSource.setItemValue() ++ Error  - Unknown content subtype in {value.keys()}")

                non_positive_keys = [key for key in value if int(value[key]) <= 0]

                for key in non_positive_keys:
                    value.pop(key)

                if len(value) > 0:
                    self.__contents[item] = value

            else:
                self.__contents[item] = value

        else:
            logging.error('+NmrDpReportInputSource.setItemValue() ++ Error  - Unknown item type %s', item)
            raise KeyError(f"+NmrDpReportInputSource.setItemValue() ++ Error  - Unknown item type {item}")

    def get(self):
        """ Retrieve contents.
        """

        return self.__contents

    def put(self, contents):
        """ Set contents.
        """

        self.__contents = contents

    def updateNonStandardResidueByExptlData(self, chain_id, seq_id, content_subtype):
        """ Update specified non_starndard_residue by experimental data.
        """

        if self.__contents['non_standard_residue'] is None:
            return

        try:

            c = next(c for c in self.__contents['non_standard_residue'] if c['chain_id'] == chain_id)

            if seq_id in c['seq_id']:
                c['exptl_data'][c['seq_id'].index(seq_id)][content_subtype] = True
            # # should pass because reallocation of chain_id may happen
            # else:
            #     logging.error('+NmrDpReportInputSource.updateNonStandardResidueByExptlData() ++ Error  - Unknown seq_id %s', seq_id)
            #     raise KeyError(f"+NmrDpReportInputSource.updateNonStandardResidueByExptlData() ++ Error  - Unknown seq_id {seq_id}")
            #
        except StopIteration:
            logging.error('+NmrDpReportInputSource.updateNonStandardResidueByExptlData() ++ Error  - Unknown chain_id %s', chain_id)
            raise KeyError(f"+NmrDpReportInputSource.updateNonStandardResidueByExptlData() ++ Error  - Unknown chain_id {chain_id}")  # pylint: disable=raise-missing-from


class NmrDpReportSequenceAlignment:
    """ Wrapper class for data processing report of NMR data (sequence alignment).
    """

    def __init__(self):
        self.items = ('model_poly_seq_vs_coordinate', 'model_poly_seq_vs_nmr_poly_seq', 'nmr_poly_seq_vs_model_poly_seq',
                      'model_poly_seq_vs_dist_restraint', 'model_poly_seq_vs_dihed_restraint', 'model_poly_seq_vs_rdc_restraint',
                      'model_poly_seq_vs_plane_restraint', 'model_poly_seq_vs_adist_restraint', 'model_poly_seq_vs_jcoup_restraint',
                      'model_poly_seq_vs_hvycs_restraint', 'model_poly_seq_vs_procs_restraint', 'model_poly_seq_vs_rama_restraint',
                      'model_poly_seq_vs_radi_restraint', 'model_poly_seq_vs_diff_restraint', 'model_poly_seq_vs_nbase_restraint',
                      'model_poly_seq_vs_csa_restraint', 'model_poly_seq_vs_ang_restraint', 'model_poly_seq_vs_pre_restraint',
                      'model_poly_seq_vs_pcs_restraint', 'model_poly_seq_vs_prdc_restraint', 'model_poly_seq_vs_pang_restraint',
                      'model_poly_seq_vs_pccr_restraint', 'model_poly_seq_vs_hbond_restraint', 'model_poly_seq_vs_geo_restraint',
                      'model_poly_seq_vs_noepk_restraint',
                      'nmr_poly_seq_vs_chem_shift', 'nmr_poly_seq_vs_dist_restraint', 'nmr_poly_seq_vs_dihed_restraint',
                      'nmr_poly_seq_vs_rdc_restraint', 'nmr_poly_seq_vs_spectral_peak', 'nmr_poly_seq_vs_spectral_peak_alt')

        self.__contents = {item: None for item in self.items}

    def setItemValue(self, item, value):
        """ Set an item with a given value.
        """

        if item in self.items:
            self.__contents[item] = value

        else:
            logging.error('+NmrDpReportSequenceAlignment.setItemValue() ++ Error  - Unknown item type %s', item)
            raise KeyError(f"+NmrDpReportSequenceAlignment.setItemValue() ++ Error  - Unknown item type {item}")

    def get(self):
        """ Retrieve contents.
        """

        return self.__contents

    def put(self, contents):
        """ Set contents.
        """

        self.__contents = contents


class NmrDpReportChainAssignment:
    """ Wrapper class for data processing report of NMR data (chain assignment).
    """

    def __init__(self):
        self.items = ('model_poly_seq_vs_nmr_poly_seq', 'nmr_poly_seq_vs_model_poly_seq')

        self.__contents = {item: None for item in self.items}

    def setItemValue(self, item, value):
        """ Set an item with a given value.
        """

        if item in self.items:
            self.__contents[item] = value

        else:
            logging.error('+NmrDpReportChainAssignment.setItemValue() ++ Error  - Unknown item type %s', item)
            raise KeyError(f"+NmrDpReportChainAssignment.setItemValue() ++ Error  - Unknown item type {item}")

    def get(self):
        """ Retrieve contents.
        """

        return self.__contents

    def put(self, contents):
        """ Set contents.
        """

        self.__contents = contents


class NmrDpReportError:
    """ Wrapper class for data processing report of NMR data (error).
    """

    def __init__(self):
        self.items = ('internal_error', 'format_issue', 'missing_mandatory_content', 'missing_mandatory_item',
                      'content_mismatch', 'sequence_mismatch',
                      'invalid_data', 'invalid_atom_nomenclature', 'invalid_atom_type', 'invalid_isotope_number', 'invalid_ambiguity_code',
                      'atom_not_found', 'multiple_data', 'missing_data', 'duplicated_index', 'anomalous_data')

        self.group_items = ('sequence_mismatch',
                            'invalid_data', 'invalid_atom_nomenclature', 'invalid_atom_type', 'invalid_isotope_number', 'invalid_ambiguity_code',
                            'atom_not_found', 'multiple_data', 'missing_data', 'anomalous_data')

        self.__contents = {item: None for item in self.items}

        self.__contents['total'] = 0

        self.chk_row_pat = re.compile(r'^\[Check row of (.*)\] (.*)$')
        self.chk_rows_pat = re.compile(r'\[Check rows of (.*)\] (.*)$')

    def appendDescription(self, item, value):
        """ Append an error with a give description.
        """

        if item in self.items:

            if item not in self.__contents or self.__contents[item] is None:
                self.__contents[item] = []

            if item != 'internal_error' and 'category' in value:
                value['category'] = value['category'].lstrip('_')

            if item != 'internal_error' and 'description' in value:
                d = value['description']

                if d.startswith("[Check row of"):
                    g = self.chk_row_pat.search(d).groups()

                    loc = {}
                    for i in g[0].split(','):
                        p = i.lstrip()
                        s = p.index(' ')
                        loc[p[0: s]] = p[s:].lstrip()

                    value['row_location'] = loc
                    value['description'] = g[1]

                elif d.startswith("[Check rows of"):
                    g = self.chk_rows_pat.search(d).groups()

                    locs = {}
                    for i in g[0].split(','):
                        p = i.lstrip()
                        q = p.split(' ', 1)
                        locs[q[0]] = re.sub(' vs ', ',', q[1]).split(',')

                    value['row_locations'] = locs
                    value['description'] = g[1]

            if not any(v for v in self.__contents[item] if v == value):

                if item in self.group_items and 'file_name' in value and 'row_location' not in value and 'row_locations' not in value:

                    if 'sf_framecode' in value:
                        v = next((v for v in self.__contents[item]
                                  if 'file_name' in v and v['file_name'] == value['file_name']
                                  and 'sf_framecode' in v and v['sf_framecode'] == value['sf_framecode']
                                  and 'row_location' not in v and 'row_locations' not in v), None)
                    else:
                        v = next((v for v in self.__contents[item]
                                  if 'file_name' in v and v['file_name'] == value['file_name']
                                  and 'sf_framecode' not in v
                                  and 'row_location' not in v and 'row_locations' not in v), None)

                        if v is not None and value['description'] in v['description'].split('\n'):
                            return

                    if v is not None:
                        v['description'] += f"\n{value['description']}"

                        v['subtotal'] += 1

                        return

                    value['subtotal'] = 1

                self.__contents[item].append(value)

                self.__contents['total'] += 1

        else:
            logging.error('+NmrDpReportError.appendDescription() ++ Error  - Unknown item type %s', item)
            raise KeyError(f"+NmrDpReportError.appendDescription() ++ Error  - Unknown item type {item}")

    def get(self):
        """ Retrieve errors.
        """

        return {k: v for k, v in self.__contents.items() if v is not None}

    def put(self, contents):
        """ Set errors.
        """

        self.__contents = contents

    def getTotal(self):
        """ Return total number of errors.
            @return: total number of errors
        """

        return self.__contents['total']

    def exists(self, file_name, sf_framecode):
        """ Return whether an error specified by file name and saveframe exists.
            @return: True for an error exists or False otherwise
        """

        for item in self.__contents.keys():

            if item in ('total', 'internal_error') or self.__contents[item] is None:
                continue

            if any(c for c in self.__contents[item] if c['file_name'] == file_name and 'sf_framecode' in c and c['sf_framecode'] == sf_framecode):
                return True

        return False

    def getValueList(self, item, file_name, key=None):
        """ Return list of error values specified by item name and file name.
        """

        if item in ('total', 'internal_error') or self.__contents is None or (item not in self.__contents.keys()) or self.__contents[item] is None:
            return None

        return [c for c in self.__contents[item] if c['file_name'] == file_name or (key is None or key in c['description'])]

    def getValueListWithSf(self, item, file_name, sf_framecode, key=None):
        """ Return list of error values specified by item name, file name, and saveframe.
        """

        if item in ('total', 'internal_error') or self.__contents is None or (item not in self.__contents.keys()) or self.__contents[item] is None:
            return None

        return [c for c in self.__contents[item]
                if c['file_name'] == file_name and 'sf_framecode' in c and c['sf_framecode'] == sf_framecode and (key is None or key in c['description'])]

    def getUniqueValueList(self, item, file_name):
        """ Return list of error values having unique sf_framecode and description.
        """

        if item in ('total', 'internal_error') or self.__contents is None or (item not in self.__contents.keys()) or self.__contents[item] is None:
            return None

        rlist = []

        keys = set()

        for c in self.getValueList(item, file_name):

            if 'sf_framecode' not in c:
                continue

            key = c['sf_framecode'] + c['description']

            if key in keys:
                continue

            if 'row_location' in c:
                del c['row_location']

            elif 'row_locations' in c:
                del c['row_locations']

            rlist.append(c)

            keys.add(key)

        return rlist

    def getDescription(self, item, file_name, sf_framecode):
        """ Return error description specified by item name, file name, and saveframe.
        """

        if item in ('total', 'internal_error') or self.__contents is None or (item not in self.__contents.keys()) or self.__contents[item] is None:
            return None

        try:
            c = next(c for c in self.__contents[item] if c['file_name'] == file_name and 'sf_framecode' in c and c['sf_framecode'] == sf_framecode)
            return c['description']
        except StopIteration:
            return None

    def getCombinedDescriptions(self, file_name, sf_framecode):
        """ Return combined error descriptions specified by file name and saveframe.
        """

        if self.__contents is None:
            return None

        d = []

        for item in self.items:

            if item == 'internal_error' or self.__contents[item] is None:
                continue

            for c in self.__contents[item]:

                if c['file_name'] == file_name and 'sf_framecode' in c and c['sf_framecode'] == sf_framecode:
                    d.append(item + ': ' + c['description'])

        if len(d) == 0:
            return None

        return d

    def clean(self):
        """ Clean-up empty items and update stats.
        """

        if self.__contents is None:
            return

        items = [item for item in self.__contents.keys() if item != 'total' and (self.__contents[item] is None or len(self.__contents[item]) == 0)]

        for item in items:
            del self.__contents[item]

        total = 0
        for item in self.__contents.keys():
            if item != 'total':
                total += len(self.__contents[item])

        self.__contents['total'] = total


class NmrDpReportWarning:
    """ Wrapper class for data processing report of NMR unified data (warning).
    """

    def __init__(self):
        self.items = ('encouragement', 'missing_content', 'missing_saveframe', 'missing_data', 'enum_mismatch',
                      'enum_mismatch_ignorable', 'corrected_format_issue', 'corrected_saveframe_name',
                      'disordered_index', 'sequence_mismatch',
                      'atom_nomenclature_mismatch', 'auth_atom_nomenclature_mismatch', 'ccd_mismatch', 'ambiguity_code_mismatch',
                      'skipped_saveframe_category', 'skipped_loop_category',
                      'anomalous_bond_length',
                      'anomalous_chemical_shift', 'unusual_chemical_shift',
                      'complemented_chemical_shift', 'incompletely_assigned_chemical_shift', 'incompletely_assigned_spectral_peak',
                      'anomalous_data', 'unusual_data', 'unusual/rare_data', 'insufficient_data',
                      'conflicted_data', 'inconsistent_data', 'redundant_data',
                      'conflicted_mr_data', 'inconsistent_mr_data', 'redundant_mr_data', 'unsupported_mr_data',
                      'concatenated_sequence', 'not_superimposed_model', 'exactly_overlaid_model')

        self.group_items = ('sequence_mismatch',
                            'atom_nomenclature_mismatch', 'auth_atom_nomenclature_mismatch', 'ccd_mismatch', 'ambiguity_code_mismatch',
                            'anomalous_bond_length',
                            'complemented_chemical_shift', 'incompletely_assigned_chemical_shift', 'incompletely_assigned_spectral_peak',
                            'unusual/rare_data', 'insufficient_data',
                            'conflicted_data', 'inconsistent_data', 'redundant_data',
                            'conflicted_mr_data', 'inconsistent_mr_data', 'redundant_mr_data')

        self.__contents = {item: None for item in self.items}

        self.__contents['total'] = 0

        self.chk_row_pat = re.compile(r'^\[Check row of (.*)\] (.*)$')
        self.chk_rows_pat = re.compile(r'\[Check rows of (.*)\] (.*)$')

    def appendDescription(self, item, value):
        """ Append a warning with a give description.
        """

        if item in self.items:

            if item not in self.__contents or self.__contents[item] is None:
                self.__contents[item] = []

            if 'category' in value:
                value['category'] = value['category'].lstrip('_')

            if 'description' in value:
                d = value['description']

                if d.startswith("[Check row of"):
                    g = self.chk_row_pat.search(d).groups()

                    loc = {}
                    for i in g[0].split(','):
                        p = i.lstrip()
                        s = p.index(' ')
                        loc[p[0: s]] = p[s:].lstrip()

                    value['row_location'] = loc
                    value['description'] = g[1]

                elif d.startswith("[Check rows of"):
                    g = self.chk_rows_pat.search(d).groups()

                    locs = {}
                    for i in g[0].split(','):
                        p = i.lstrip()
                        q = p.split(' ', 1)
                        locs[q[0]] = re.sub(' vs ', ',', q[1]).split(',')

                    value['row_locations'] = locs
                    value['description'] = g[1]

            if not any(v for v in self.__contents[item] if v == value):

                if item in self.group_items and 'file_name' in value and 'row_location' not in value and 'row_locations' not in value:

                    if 'sf_framecode' in value:
                        v = next((v for v in self.__contents[item]
                                  if 'file_name' in v and v['file_name'] == value['file_name']
                                  and 'sf_framecode' in v and v['sf_framecode'] == value['sf_framecode']
                                  and 'row_location' not in v and 'row_locations' not in v), None)
                    else:
                        v = next((v for v in self.__contents[item]
                                  if 'file_name' in v and v['file_name'] == value['file_name']
                                  and 'sf_framecode' not in v
                                  and 'row_location' not in v and 'row_locations' not in v), None)

                        if v is not None and value['description'] in v['description'].split('\n'):
                            return

                    if v is not None:
                        v['description'] += f"\n{value['description']}"

                        v['subtotal'] += 1

                        return

                    value['subtotal'] = 1

                self.__contents[item].append(value)

                self.__contents['total'] += 1

        else:
            logging.error('+NmrDpReportWarning.appendDescription() ++ Error  - Unknown item type %s', item)
            raise KeyError(f"+NmrDpReportWarning.appendDescription() ++ Error  - Unknown item type {item}")

    def get(self):
        """ Retrieve warnings.
        """

        return {k: v for k, v in self.__contents.items() if v is not None}

    def put(self, contents):
        """ Set warnings.
        """

        self.__contents = contents

    def getTotal(self):
        """ Return total number of warnings.
            @return: total number of warnings
        """

        return self.__contents['total']

    def exists(self, file_name, sf_framecode):
        """ Return whether a warning specified by file name and saveframe exists.
            @return: True for a warning exists or False otherwise
        """

        for item in self.__contents.keys():

            if item in ('total', 'enum_mismatch_ignorable') or self.__contents[item] is None:
                continue

            if any(c for c in self.__contents[item] if c['file_name'] == file_name and 'sf_framecode' in c and c['sf_framecode'] == sf_framecode):
                return True

        return False

    def getValueList(self, item, file_name, key=None):
        """ Return list of warning values specified by item name and file name.
        """

        if item == 'total' or self.__contents is None or (item not in self.__contents.keys()) or self.__contents[item] is None:
            return None

        return [c for c in self.__contents[item] if c['file_name'] == file_name and (key is None or key in c['description'])]

    def getValueListWithSf(self, item, file_name, sf_framecode, key=None):
        """ Return list of warning values specified by item name, file name, and saveframe.
        """

        if item == 'total' or self.__contents is None or (item not in self.__contents.keys()) or self.__contents[item] is None:
            return None

        return [c for c in self.__contents[item]
                if c['file_name'] == file_name and 'sf_framecode' in c and c['sf_framecode'] == sf_framecode and (key is None or key in c['description'])]

    def getUniqueValueList(self, item, file_name):
        """ Return list of warning values having unique sf_framecode and description.
        """

        if item == 'total' or self.__contents is None or (item not in self.__contents.keys()) or self.__contents[item] is None:
            return None

        rlist = []

        keys = set()

        for c in self.getValueList(item, file_name):

            if 'sf_framecode' not in c:
                continue

            key = c['sf_framecode'] + c['description']

            if key in keys:
                continue

            if 'row_location' in c:
                del c['row_location']

            elif 'row_locations' in c:
                del c['row_locations']

            rlist.append(c)

            keys.add(key)

        return rlist

    def getDescription(self, item, file_name, sf_framecode):
        """ Return warning description specified by item name, file name, and saveframe.
        """

        if item == 'total' or self.__contents is None or (item not in self.__contents.keys()) or self.__contents[item] is None:
            return None

        try:
            c = next(c for c in self.__contents[item] if c['file_name'] == file_name and 'sf_framecode' in c and c['sf_framecode'] == sf_framecode)
            return c['description']
        except StopIteration:
            return None

    def getCombinedDescriptions(self, file_name, sf_framecode):
        """ Return combined warning descriptions specified by file name and saveframe.
        """

        if self.__contents is None:
            return None

        d = []

        for item in self.items:

            if item == 'enum_mismatch_ignorable' or self.__contents[item] is None:
                continue

            for c in self.__contents[item]:

                if c['file_name'] == file_name and 'sf_framecode' in c and c['sf_framecode'] == sf_framecode:
                    d.append(item + ': ' + c['description'])

        if len(d) == 0:
            return None

        return d

    def sortChemicalShiftValidation(self):
        """ Sort warning about anomalous/unusual chemical shift.
        """

        if self.__contents is None:
            return

        d = []

        anomalous_cs = False
        mixed_status = False

        for item in ['anomalous_data', 'anomalous_chemical_shift', 'unusual_data', 'unusual_chemical_shift']:

            if item not in self.__contents.keys() or self.__contents[item] is None:
                continue

            _d = [c for c in self.__contents[item] if 'sigma' in c] if 'data' in item else self.__contents[item]
            _d_ = copy.copy(_d)

            if len(_d) > 0:

                if 'anomalous' in item:
                    anomalous_cs = True
                    for c in _d:
                        c['status'] = 'A'

                elif anomalous_cs:
                    mixed_status = True

                d.extend(_d)

                for c in _d_:
                    self.__contents[item].remove(c)

                if len(self.__contents[item]) == 0:
                    self.__contents[item] = None

        if len(d) == 0:
            return

        item = 'anomalous_chemical_shift' if anomalous_cs else 'unusual_chemical_shift'

        self.__contents[item] = []

        if mixed_status:
            for c in d:
                if 'status' not in c:
                    c['status'] = 'S'
                if 'sigma' not in c:
                    c['sigma'] = 0.0

            for c in sorted(sorted(d, key=lambda i: i['sigma'], reverse=True), key=lambda j: j['status']):
                if 'description_alt' in c:
                    c['description'] = c['description_alt']
                    del c['description_alt']
                del c['sigma']
                self.__contents[item].append(c)

        else:
            for c in d:
                if 'status' in c and not anomalous_cs:
                    del c['status']
                if 'sigma' not in c:
                    c['sigma'] = 0.0

            for c in sorted(d, key=lambda i: i['sigma'], reverse=True):
                if 'description_alt' in c:
                    c['description'] = c['description_alt']
                    del c['description_alt']
                del c['sigma']
                self.__contents[item].append(c)

    def sortBySigma(self, item):
        """ Sort warning about sigma.
        """

        if self.__contents is None:
            return

        if item not in self.__contents or self.__contents[item] is None or len(self.__contents[item]) < 2:
            return

        d = copy.copy(self.__contents[item])

        self.__contents[item] = []

        for c in sorted(d, key=lambda i: i['sigma'], reverse=True):
            self.__contents[item].append(c)

    def clean(self):
        """ Clean-up empty items and update stats.
        """

        if self.__contents is None:
            return

        items = [item for item in self.__contents.keys() if item != 'total' and (self.__contents[item] is None or len(self.__contents[item]) == 0)]

        for item in items:
            del self.__contents[item]

        total = 0
        for item in self.__contents.keys():
            if item != 'total':
                total += len(self.__contents[item])

        self.__contents['total'] = total

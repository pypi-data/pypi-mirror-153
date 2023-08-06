##
# File: CifToNmrStar.py
# Date: 19-Jul-2021
#
# Updates:
# 13-Oct-2021  M. Yokochi - code revision according to PEP8 using Pylint (DAOTHER-7389, issue #5)
# 20-Apr-2022  M. Yokochi - enable to fix broken data block order of CIF formatted NMR-STAR using NMR-STAR schema (DAOTHER-7407, NMR restraint remediation)
##
""" Wrapper class for CIF to NMR-STAR converter.
    @author: Masashi Yokochi
"""
import sys
import os
import pynmrstar
import pickle

try:
    from wwpdb.utils.nmr.io.mmCIFUtil import mmCIFUtil
    from wwpdb.utils.nmr.AlignUtil import (emptyValue, trueValue)
except ImportError:
    from nmr.io.mmCIFUtil import mmCIFUtil
    from nmr.AlignUtil import (emptyValue, trueValue)


def load_schema_from_pickle(file_name):
    """ Load NMR-STAR schema from pickle file.
    """

    if os.path.exists(file_name):

        with open(file_name, 'rb') as ifp:
            return pickle.load(ifp)

    return None


def write_schema_as_pickle(obj, file_name):
    """ Write NMR-STAR schema as pickle file.
    """

    with open(file_name, 'wb') as ofp:
        pickle.dump(obj, ofp)


class CifToNmrStar:
    """ Simple CIF to NMR-STAR converter.
    """

    def __init__(self, log=sys.stderr):
        self.__lfh = log

        # directory
        self.schema_dir = os.path.dirname(__file__) + '/nmr-star_schema/'

        # NMR-STAR schema
        self.schema = load_schema_from_pickle(self.schema_dir + 'schema.pkl')

        # NMR-STAR schema order
        # self.schema_order = load_schema_from_pickle(self.schema_dir + 'schema_order.pkl')

        # NMR-STAR category order
        self.category_order = load_schema_from_pickle(self.schema_dir + 'category_order.pkl')

        if self.schema is None:
            schema = pynmrstar.Schema()  # network latency occurs if pickle resource files are not available
            self.schema = schema.schema
            self.category_order = schema.category_order

    def write_schema_as_pickles(self):
        """ Retrieve NMR-STAR schema from pynmrstar.Schema, then write schema objects as each pickle file.
        """

        schema = pynmrstar.Schema()  # retrieve the latest schema via interet access

        # print(schema.headers)
        with open(self.schema_dir + 'headers.txt', 'w') as ofp:
            for header in schema.headers:
                ofp.write(header + '\n')
        print('headers.txt: Done.')

        # print(schema.schema)
        write_schema_as_pickle(schema.schema, self.schema_dir + 'schema.pkl')
        print('schema.pkl: Done.')

        # print(schema.schema_order)
        write_schema_as_pickle(schema.schema_order, self.schema_dir + 'schema_order.pkl')
        print('schema_order.pkl: Done.')

        # print(schema.category_order)
        write_schema_as_pickle(schema.category_order, self.schema_dir + 'category_order.pkl')
        print('category_order.pkl: Done.')

        # print(schema.data_types)
        write_schema_as_pickle(schema.data_types, self.schema_dir + 'data_types.pkl')
        print('data_types.pkl: Done.')

        with open(self.schema_dir + 'version.txt', 'w') as ofp:
            ofp.write(schema.version)
        print(f"version: {schema.version}")

    def convert(self, cifPath=None, strPath=None):
        """ Convert CIF to NMR-STAR for re-upload without CS data
        """

        if cifPath is None or strPath is None:
            return False

        try:

            cifObj = mmCIFUtil(filePath=cifPath)

            block_name_list = cifObj.GetBlockIDList()

            if len(block_name_list) == 0:  # single loop
                return False

            entry_id = None

            strObj = pynmrstar.Entry.from_scratch(os.path.basename(cifPath))

            # check category order in CIF
            category_order = []
            previous_order = -1

            for block_name in block_name_list:

                dict_list = cifObj.GetDataBlock(block_name)

                ordered_block = True
                sf_category = ''

                for category, itVals in dict_list.items():
                    try:
                        current_order = self.category_order.index('_' + category)
                    except ValueError:
                        continue
                    # print(f"{block_name} {category} {current_order}")
                    item = {'block_name': block_name, 'category': category,
                            'category_order': current_order}
                    if current_order < previous_order:
                        ordered_block = False
                        for item2 in category_order:
                            if item2['block_name'] == block_name:
                                item2['ordered'] = False
                    item['ordered'] = ordered_block

                    item['sf_category_flag'] = False
                    for _item, _value in zip(itVals['Items'], itVals['Values'][0]):
                        tag = '_' + category + '.' + _item
                        tag = tag.lower()
                        if tag in self.schema:
                            sdict = {k: v for k, v in self.schema[tag].items() if v not in emptyValue}
                            if 'sf_category' not in item:
                                item['sf_category'] = sdict['SFCategory']
                            if 'super_category' not in item:
                                item['super_category'] = sdict['ADIT super category']
                            if 'Sf category flag' in sdict and sdict['Sf category flag'].lower() in trueValue:
                                item['sf_category_flag'] = True
                            if _item == 'Entry_ID' and entry_id in emptyValue:
                                entry_id = _value

                    if 'Sf_category' not in itVals['Items']:
                        _tag = '_' + category.lower() + '.sf_category'
                        if _tag in self.schema:
                            sdict = {k: v for k, v in self.schema[_tag].items() if v not in emptyValue}
                            if 'sf_category' not in item:
                                item['sf_category'] = sdict['SFCategory']
                            if 'super_category' not in item:
                                item['super_category'] = sdict['ADIT super category']
                            if 'Sf category flag' in sdict and sdict['Sf category flag'].lower() in trueValue:
                                item['sf_category_flag'] = True

                    if len(sf_category) == 0:
                        sf_category = item['sf_category']
                    elif sf_category != item['sf_category']:
                        for item2 in category_order:
                            if item2['block_name'] == block_name:
                                item2['ordered'] = False
                        item['ordered'] = False

                    if item not in category_order:
                        category_order.append(item)

                    if item['sf_category_flag']:
                        previous_order = current_order

            if entry_id in emptyValue:
                entry_id = block_name_list[0]

            # reorder
            category_order.sort(key=lambda k: k['category_order'])

            # correct block name in case
            reserved_block_names = []
            prev_sf_category = ''
            prev_sf_block_name = ''
            for item in category_order:
                if item['ordered']:
                    continue
                block_name = item['block_name']
                if item['sf_category_flag']:
                    if item['sf_category'] == item['super_category']:
                        block_name = item['sf_category']
                    else:
                        list_id = 1
                        while True:
                            block_name = item['sf_category'] + '_' + str(list_id)
                            if block_name not in reserved_block_names:
                                break
                            list_id += 1
                    prev_sf_category = item['sf_category']
                    prev_sf_block_name = block_name
                else:
                    if item['sf_category'] == prev_sf_category:
                        block_name = prev_sf_block_name
                    else:
                        item['missing_sf_category'] = True
                        if item['sf_category'] == item['super_category']:
                            block_name = item['sf_category']
                        else:
                            list_id = 1
                            while True:
                                block_name = item['sf_category'] + '_' + str(list_id)
                                if block_name not in reserved_block_names:
                                    break
                                list_id += 1
                        prev_sf_category = item['sf_category']
                        prev_sf_block_name = block_name
                item['new_block_name'] = block_name

            ordered_block_names = []
            for item in category_order:
                block_name = item['new_block_name'] if 'new_block_name' in item else item['block_name']
                if block_name not in ordered_block_names:
                    ordered_block_names.append(block_name)

            _category_order = []
            for _block_name in ordered_block_names:
                count = 0
                for item in category_order:
                    block_name = item['new_block_name'] if 'new_block_name' in item else item['block_name']
                    if block_name == _block_name:
                        _category_order.append(item)
                        count += 1
                if count == 1:
                    last_item = _category_order[-1]
                    if not last_item['sf_category_flag'] and last_item['ordered']:
                        last_item['missing_sf_category'] = True
                        last_item['new_block_name'] = last_item['block_name']

            category_order = _category_order

            reserved_block_names = []
            sf = None
            for item in category_order:
                block_name = item['block_name']
                category = item['category']

                if 'missing_sf_category' in item and item['missing_sf_category']:
                    new_block_name = item['new_block_name']

                    if new_block_name in reserved_block_names:
                        continue

                    if sf is not None:
                        strObj.add_saveframe(sf)

                    sf = pynmrstar.Saveframe.from_scratch(new_block_name)
                    reserved_block_names.append(new_block_name)
                    sf_tag_prefix = next(v['Tag category'] for k, v in self.schema.items()
                                         if v['SFCategory'] == item['sf_category'] and v['Tag field'] == 'Sf_category')
                    sf.set_tag_prefix(sf_tag_prefix)
                    sf.add_tag('Sf_category', item['sf_category'])
                    sf.add_tag('Sf_framecode', new_block_name)
                    sf.add_tag('Entry_ID', entry_id.upper())
                    if item['sf_category'] != item['super_category']:
                        sf.add_tag('ID', '1')

                elif item['sf_category_flag']:
                    new_block_name = item['new_block_name'] if 'new_block_name' in item else block_name

                    if new_block_name in reserved_block_names:
                        continue

                    if sf is not None:
                        strObj.add_saveframe(sf)

                    sf = pynmrstar.Saveframe.from_scratch(new_block_name)
                    reserved_block_names.append(new_block_name)
                    sf.set_tag_prefix(category)

                    dict_list = cifObj.GetDataBlock(block_name)
                    itVals = next(v for k, v in dict_list.items() if k == category)

                    for _item, value in zip(itVals['Items'], itVals['Values'][0]):
                        sf.add_tag(_item, new_block_name if _item == 'Sf_framecode' else value)

                if not item['sf_category_flag']:
                    lp = pynmrstar.Loop.from_scratch(category)

                    dict_list = cifObj.GetDataBlock(block_name)
                    itVals = next(v for k, v in dict_list.items() if k == category)

                    for _item in itVals['Items']:
                        lp.add_tag(_item)

                    for _value in itVals['Values']:
                        lp.add_data(_value)

                    sf.add_loop(lp)

            if sf is not None:
                strObj.add_saveframe(sf)

            strObj.write_to_file(strPath, skip_empty_tags=False)

        except Exception as e:
            self.__lfh.write(f"+ERROR- CifToNmrStar.convert() {str(e)}\n")

            return False

        return True

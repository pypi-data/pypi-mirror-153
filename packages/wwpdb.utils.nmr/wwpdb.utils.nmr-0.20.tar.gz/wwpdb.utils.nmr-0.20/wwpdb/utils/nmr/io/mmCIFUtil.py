"""
File:    mmCIFUtil.py
Author:  Zukang Feng
Update:  21-August-2012
Version: 001  Initial version
# Update:
# 07-Apr-2020  M. Yokochi - Re-write Zukang's version to being aware of multiple data blocks
##
"""

__author__ = "Zukang Feng"
__email__ = "zfeng@rcsb.rutgers.edu"
__version__ = "V0.001"

import sys
import copy

from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import DataContainer
from mmcif.io.PdbxReader import PdbxReader
from mmcif.io.PdbxWriter import PdbxWriter


class mmCIFUtil:
    """ Using pdbx mmCIF utility to parse mmCIF file
    """

    def __init__(self, verbose=False, log=sys.stderr, filePath=None):  # pylint: disable=unused-argument
        # self.__verbose = verbose
        self.__lfh = log
        self.__filePath = filePath
        self.__dataList = []
        self.__dataMap = {}
        self.__blockNameList = []
        self.__read()

    def __read(self):
        if not self.__filePath:
            return
        #
        try:
            with open(self.__filePath, 'r', encoding='utf-8') as ifh:
                pRd = PdbxReader(ifh)
                pRd.read(self.__dataList)

            if self.__dataList:
                idx = 0
                for container in self.__dataList:
                    blockName = container.getName()
                    self.__blockNameList.append(blockName)
                    self.__dataMap[blockName] = idx
                    idx += 1
                #
            #
        except Exception as e:
            self.__lfh.write(f"Read {self.__filePath} failed {str(e)}.\n")

    def GetBlockIDList(self):
        """ Return list of block ID
        """
        return self.__blockNameList

    def GetValueAndItemByBlock(self, blockName, catName):
        """ Get category values and item names
        """
        dList = []
        iList = []
        if blockName not in self.__dataMap:
            return dList, iList
        #
        catObj = self.__dataList[self.__dataMap[blockName]].getObj(catName)
        if not catObj:
            return dList, iList
        #
        iList = catObj.getAttributeList()
        rowList = catObj.getRowList()
        for row in rowList:
            tD = {}
            for idxIt, itName in enumerate(iList):
                if row[idxIt] != "?" and row[idxIt] != ".":
                    tD[itName] = row[idxIt]
            #
            if tD:
                dList.append(tD)
            #
        #
        return dList, iList

    def GetValue(self, blockName, catName):
        """ Get category values in a given Data Block and Category
            The results are stored in a list of dictionaries with item name as key
        """
        return self.GetValueAndItemByBlock(blockName, catName)[0]

    def GetSingleValue(self, blockName, catName, itemName):
        """ Get the first value of a given Data Block, Category, Item
        """
        text = ""
        dlist = self.GetValue(blockName, catName)
        if dlist:
            if itemName in dlist[0]:
                text = dlist[0][itemName]
        return text

    def UpdateSingleRowValue(self, blockName, catName, itemName, rowIndex, value):
        """ Update value in single row
        """
        if blockName not in self.__dataMap:
            return

        catObj = self.__dataList[self.__dataMap[blockName]].getObj(catName)

        if not catObj:
            return
        #
        catObj.setValue(value, itemName, rowIndex)

    def UpdateMultipleRowsValue(self, blockName, catName, itemName, value):
        """ Update value in multiple rows
        """
        if blockName not in self.__dataMap:
            return

        catObj = self.__dataList[self.__dataMap[blockName]].getObj(catName)

        if not catObj:
            return
        #
        rowNo = catObj.getRowCount()
        for rowIndex in range(0, rowNo):
            catObj.setValue(value, itemName, rowIndex)

    def AddBlock(self, blockName):
        """ Add Data Block
        """
        container = DataContainer(blockName)
        self.__dataMap[blockName] = len(self.__dataList)
        self.__dataList.append(container)

    def AddCategory(self, blockName, catName, items):
        """ Add Category in a given Data Block
        """
        if blockName not in self.__dataMap:
            return

        category = DataCategory(catName)
        for item in items:
            category.appendAttribute(item)
        #
        self.__dataList[self.__dataMap[blockName]].append(category)

    def RemoveCategory(self, blockName, catName):
        """ Remove Category in a given Data Block
        """
        if blockName not in self.__dataMap:
            return

        catObj = self.__dataList[self.__dataMap[blockName]].getObj(catName)

        if catObj is None:
            return

        self.__dataList[self.__dataMap[blockName]].remove(catName)

    def MoveCategoryToTop(self, blockName, catName):
        """ Move Category to top in a given Data Block
        """
        if blockName not in self.__dataMap:
            return

        catObj = self.__dataList[self.__dataMap[blockName]].getObj(catName)

        if catObj is None:
            return

        _catNameList = copy.copy(self.__dataList[self.__dataMap[blockName]].getObjNameList())
        _catNameList.remove(catName)

        _catObjList = [copy.copy(catObj)]
        _catObjList.extend([copy.copy(self.__dataList[self.__dataMap[blockName]].getObj(_catName)) for _catName in _catNameList])

        for _catName in _catNameList:
            self.__dataList[self.__dataMap[blockName]].remove(_catName)

        for _catObj in _catObjList:
            self.__dataList[self.__dataMap[blockName]].append(_catObj)

    def InsertData(self, blockName, catName, dataList):
        """ Insert data in a given Data Block and Category
        """
        if blockName not in self.__dataMap:
            return

        catObj = self.__dataList[self.__dataMap[blockName]].getObj(catName)

        if catObj is None:
            return
        #
        for data in dataList:
            catObj.append(data)

    def ExtendCategory(self, blockName, catName, items, dataList, col=-1):
        """ Extend existing Category in a given Data Block
        """
        if blockName not in self.__dataMap:
            return

        catObj = self.__dataList[self.__dataMap[blockName]].getObj(catName)

        if catObj is None:
            return

        append_items = col < 0 or col >= catObj.getAttributeCount()

        data_len = len(dataList)
        empty_row = ['.'] * len(items)

        if append_items:

            for item in items:
                catObj.appendAttribute(item)

            rowList = catObj.getRowList()

            for idx, row in enumerate(rowList):

                if idx < data_len:
                    row.extend(dataList[idx])
                else:
                    row.extend(empty_row)

        else:

            attrNameList = catObj.getAttributeList()

            _attrNameList = attrNameList[0:col] + items + attrNameList[col:]

            rowList = catObj.getRowList()

            _rowList = []

            for idx, row in enumerate(rowList):
                _row = row[0:col]

                if idx < data_len:
                    _row.extend(dataList[idx])
                else:
                    _row.extend(empty_row)

                _row.extend(row[col:])

                _rowList.append(_row)

            catObj.setAttributeNameList(_attrNameList)
            catObj.setRowList(_rowList)

    def CopyValueInRow(self, blockName, catName, srcItems, dstItems):
        """ Copy value from source items to destination items
        """
        if srcItems is None or dstItems is None or len(srcItems) != len(dstItems):
            return

        if blockName not in self.__dataMap:
            return

        catObj = self.__dataList[self.__dataMap[blockName]].getObj(catName)

        if catObj is None:
            return

        attrs = catObj.getAttributeList()

        for item in srcItems:
            if item not in attrs:
                return

        for item in dstItems:
            if item not in attrs:
                return

        src_cols = [attrs.index(item) for item in srcItems]
        dst_cols = [attrs.index(item) for item in dstItems]

        for row in catObj.getRowList():
            for j, src_col in enumerate(src_cols):
                row[dst_cols[j]] = row[src_col]

    def WriteCif(self, outputFilePath=None):
        """ Write out cif file
        """
        if not outputFilePath:
            return
        #
        with open(outputFilePath, 'w', encoding='utf-8') as ofh:
            pdbxW = PdbxWriter(ofh)
            pdbxW.write(self.__dataList)

    def GetCategories(self):
        """ Get all Categories in all Data Blocks
        """
        data = {}
        for container in self.__dataList:
            blockName = container.getName()
            data[blockName] = container.getObjNameList()
        #
        return data

    def GetAttributes(self, blockName, catName):
        """ Get item name in Data Block and Category
        """
        if blockName not in self.__dataMap:
            return []

        catObj = self.__dataList[self.__dataMap[blockName]].getObj(catName)

        if not catObj:
            return []
        #
        return catObj.getAttributeList()

    def GetDictList(self, blockName, catName):
        """ Get a list of dictionaries of a given Data Block and Category
        """
        dList, iList = self.GetValueAndItemByBlock(blockName, catName)
        data = [[x[y] if y in x else None for y in iList] for x in dList]
        #
        return {catName: {"Items": iList, "Values": data}}

    def GetDataBlock(self, blockName):
        """ Get a list of dictionaries of a given Data Block
        """
        data = {}
        categories = self.GetCategories()
        if blockName not in categories:
            return data
        #
        for catName in categories[blockName]:
            data.update(self.GetDictList(blockName, catName))
        #
        return data

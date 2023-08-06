##
# CyanaMRReader.py
#
# Update:
##
""" A collection of classes for parsing CYANA MR files.
"""
import sys
import os

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

try:
    from wwpdb.utils.nmr.mr.LexerErrorListener import LexerErrorListener
    from wwpdb.utils.nmr.mr.ParserErrorListener import ParserErrorListener
    from wwpdb.utils.nmr.mr.CyanaMRLexer import CyanaMRLexer
    from wwpdb.utils.nmr.mr.CyanaMRParser import CyanaMRParser
    from wwpdb.utils.nmr.mr.CyanaMRParserListener import CyanaMRParserListener
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (checkCoordinates,
                                                       MAX_ERROR_REPORT,
                                                       REPRESENTATIVE_MODEL_ID)
    from wwpdb.utils.nmr.io.CifReader import CifReader
    from wwpdb.utils.nmr.ChemCompUtil import ChemCompUtil
    from wwpdb.utils.nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from wwpdb.utils.nmr.NEFTranslator.NEFTranslator import NEFTranslator
except ImportError:
    from nmr.mr.LexerErrorListener import LexerErrorListener
    from nmr.mr.ParserErrorListener import ParserErrorListener
    from nmr.mr.CyanaMRLexer import CyanaMRLexer
    from nmr.mr.CyanaMRParser import CyanaMRParser
    from nmr.mr.CyanaMRParserListener import CyanaMRParserListener
    from nmr.mr.ParserListenerUtil import (checkCoordinates,
                                           MAX_ERROR_REPORT,
                                           REPRESENTATIVE_MODEL_ID)
    from nmr.io.CifReader import CifReader
    from nmr.ChemCompUtil import ChemCompUtil
    from nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from nmr.NEFTranslator.NEFTranslator import NEFTranslator


class CyanaMRReader:
    """ Accessor methods for parsing CYANA MR files.
    """

    def __init__(self, verbose=True, log=sys.stdout,
                 representativeModelId=REPRESENTATIVE_MODEL_ID,
                 cR=None, cC=None, ccU=None, csStat=None, nefT=None,
                 reasons=None, upl_or_lol=None, file_ext=None):
        self.__verbose = verbose
        self.__lfh = log
        self.__debug = False
        self.__remediate = False

        self.__maxLexerErrorReport = MAX_ERROR_REPORT
        self.__maxParserErrorReport = MAX_ERROR_REPORT

        self.__representativeModelId = representativeModelId

        if cR is not None and cC is None:
            cC = checkCoordinates(verbose, log, representativeModelId, cR, None, testTag=False)

        self.__cR = cR
        self.__cC = cC

        # CCD accessing utility
        self.__ccU = ChemCompUtil(verbose, log) if ccU is None else ccU

        # BMRB chemical shift statistics
        self.__csStat = BMRBChemShiftStat(verbose, log, self.__ccU) if csStat is None else csStat

        # NEFTranslator
        self.__nefT = NEFTranslator(verbose, log, self.__ccU, self.__csStat) if nefT is None else nefT

        # reasons for re-parsing request from the previous trial
        self.__reasons = reasons

        self.__upl_or_lol = upl_or_lol

        self.__file_ext = file_ext

    def setDebugMode(self, debug):
        self.__debug = debug

    def setRemediateMode(self, remediate):
        self.__remediate = remediate

    def setLexerMaxErrorReport(self, maxErrReport):
        self.__maxLexerErrorReport = maxErrReport

    def setParserMaxErrorReport(self, maxErrReport):
        self.__maxParserErrorReport = maxErrReport

    def parse(self, mrFilePath, cifFilePath=None, isFilePath=True):
        """ Parse CYANA MR file.
            @return: CyanaMRParserListener for success or None otherwise, ParserErrorListener, LexerErrorListener.
        """

        ifp = None

        try:

            if isFilePath:
                mrString = None

                if not os.access(mrFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"CyanaMRReader.parse() {mrFilePath} is not accessible.\n")
                    return None, None, None

                ifp = open(mrFilePath, 'r')  # pylint: disable=consider-using-with
                input = InputStream(ifp.read())

            else:
                mrFilePath, mrString = None, mrFilePath

                if mrString is None or len(mrString) == 0:
                    if self.__verbose:
                        self.__lfh.write("CyanaMRReader.parse() Empty string.\n")
                    return None, None, None

                input = InputStream(mrString)

            if cifFilePath is not None:
                if not os.access(cifFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"CyanaMRReader.parse() {cifFilePath} is not accessible.\n")
                    return None, None, None

                if self.__cR is None:
                    self.__cR = CifReader(self.__verbose, self.__lfh)
                    if not self.__cR.parse(cifFilePath):
                        return None, None, None

            lexer = CyanaMRLexer(input)
            lexer.removeErrorListeners()

            lexer_error_listener = LexerErrorListener(mrFilePath, maxErrorReport=self.__maxLexerErrorReport)
            lexer.addErrorListener(lexer_error_listener)

            messageList = lexer_error_listener.getMessageList()

            if messageList is not None and self.__verbose:
                for description in messageList:
                    self.__lfh.write(f"[Syntax error] line {description['line_number']}:{description['column_position']} {description['message']}\n")
                    if 'input' in description:
                        self.__lfh.write(f"{description['input']}\n")
                        self.__lfh.write(f"{description['marker']}\n")

            stream = CommonTokenStream(lexer)
            parser = CyanaMRParser(stream)
            parser.removeErrorListeners()
            parser_error_listener = ParserErrorListener(mrFilePath, maxErrorReport=self.__maxParserErrorReport)
            parser.addErrorListener(parser_error_listener)
            tree = parser.cyana_mr()

            walker = ParseTreeWalker()
            listener = CyanaMRParserListener(self.__verbose, self.__lfh,
                                             self.__representativeModelId,
                                             self.__cR, self.__cC,
                                             self.__ccU, self.__csStat, self.__nefT,
                                             self.__reasons, self.__upl_or_lol, self.__file_ext)
            listener.setDebugMode(self.__debug)
            listener.setRemediateMode(self.__remediate)
            walker.walk(listener, tree)

            messageList = parser_error_listener.getMessageList()

            if messageList is not None and self.__verbose:
                for description in messageList:
                    self.__lfh.write(f"[Syntax error] line {description['line_number']}:{description['column_position']} {description['message']}\n")
                    if 'input' in description:
                        self.__lfh.write(f"{description['input']}\n")
                        self.__lfh.write(f"{description['marker']}\n")

            if self.__verbose:
                if listener.warningMessage is not None:
                    print(listener.warningMessage)
                if isFilePath:
                    print(listener.getContentSubtype())

            return listener, parser_error_listener, lexer_error_listener

        except IOError as e:
            if self.__verbose:
                self.__lfh.write(f"+CyanaMRReader.parse() ++ Error - {str(e)}\n")
            return None, None, None

        finally:
            if isFilePath and ifp is not None:
                ifp.close()


if __name__ == "__main__":
    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/7acb/7acb-trimmed.mr',
                 '../../tests-nmr/mock-data-remediation/7acb/7acb.cif')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/D_1300028390_mr-upload_P1.cyana.V1',
                 '../../tests-nmr/mock-data-daother-7690/D_1300028390_model-annotate_P1.cif.V2')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/D_1300022821_mr-upload_P2.cyana.V1',
                 '../../tests-nmr/mock-data-daother-7690/D_1300022821_model-annotate_P1.cif.V1')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/D_1300024364_mr-upload_P1.cyana.V2',
                 '../../tests-nmr/mock-data-daother-7690/D_1300024364_model-release_P1.cif.V1')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-6830/2nd_test/cyana_rdc_restraints_exmaple',
                 '../../tests-nmr/mock-data-daother-6830/2nd_test/D_800411_model_P1.cif.V1')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-6830/2nd_test/cyana_dihed_restraints_exmaple',
                 '../../tests-nmr/mock-data-daother-6830/2nd_test/D_800411_model_P1.cif.V1')

    reader = CyanaMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-5829/D_1000249951_mr-upload_P1.cyana.V1',
                 '../../tests-nmr/mock-data-daother-5829/D_800467_model_P1.cif.V3')

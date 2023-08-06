##
# AmberMRReader.py
#
# Update:
##
""" A collection of classes for parsing AMBER MR files.
"""
import sys
import os

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

try:
    from wwpdb.utils.nmr.mr.LexerErrorListener import LexerErrorListener
    from wwpdb.utils.nmr.mr.ParserErrorListener import ParserErrorListener
    from wwpdb.utils.nmr.mr.AmberMRLexer import AmberMRLexer
    from wwpdb.utils.nmr.mr.AmberMRParser import AmberMRParser
    from wwpdb.utils.nmr.mr.AmberMRParserListener import AmberMRParserListener
    from wwpdb.utils.nmr.mr.AmberPTReader import AmberPTReader
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
    from nmr.mr.AmberMRLexer import AmberMRLexer
    from nmr.mr.AmberMRParser import AmberMRParser
    from nmr.mr.AmberMRParserListener import AmberMRParserListener
    from nmr.mr.AmberPTReader import AmberPTReader
    from nmr.mr.ParserListenerUtil import (checkCoordinates,
                                           MAX_ERROR_REPORT,
                                           REPRESENTATIVE_MODEL_ID)
    from nmr.io.CifReader import CifReader
    from nmr.ChemCompUtil import ChemCompUtil
    from nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from nmr.NEFTranslator.NEFTranslator import NEFTranslator


class AmberMRReader:
    """ Accessor methods for parsing AMBER MR files.
    """

    def __init__(self, verbose=True, log=sys.stdout,
                 representativeModelId=REPRESENTATIVE_MODEL_ID,
                 cR=None, cC=None, ccU=None, csStat=None, nefT=None,
                 atomNumberDict=None):
        self.__verbose = verbose
        self.__lfh = log
        self.__debug = False

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

        # AmberPTParserListener.getAtomNumberDict()
        self.__atomNumberDict = atomNumberDict

    def setDebugMode(self, debug):
        self.__debug = debug

    def setLexerMaxErrorReport(self, maxErrReport):
        self.__maxLexerErrorReport = maxErrReport

    def setParserMaxErrorReport(self, maxErrReport):
        self.__maxParserErrorReport = maxErrReport

    def parse(self, mrFilePath, cifFilePath=None, ptFilePath=None, isFilePath=True):
        """ Parse AMBER MR file.
            @return: AmberMRParserListener for success or None otherwise, ParserErrorListener, LexerErrorListener.
        """

        ifp = None

        try:

            if isFilePath:
                mrString = None

                if not os.access(mrFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"AmberMRReader.parse() {mrFilePath} is not accessible.\n")
                    return None, None, None

            else:
                mrFilePath, mrString = None, mrFilePath

                if mrString is None or len(mrString) == 0:
                    if self.__verbose:
                        self.__lfh.write("AmberMRReader.parse() Empty string.\n")
                    return None, None, None

            if cifFilePath is not None:
                if not os.access(cifFilePath, os.R_OK):
                    if self.__verbose:
                        self.__lfh.write(f"AmberMRReader.parse() {cifFilePath} is not accessible.\n")
                    return None, None, None

                if self.__cR is None:
                    self.__cR = CifReader(self.__verbose, self.__lfh)
                    if not self.__cR.parse(cifFilePath):
                        return None, None, None

            if ptFilePath is not None and self.__atomNumberDict is None:
                ptR = AmberPTReader(self.__verbose, self.__lfh,
                                    self.__representativeModelId,
                                    self.__cR, self.__cC,
                                    self.__ccU, self.__csStat)
                ptPL, _, _ = ptR.parse(ptFilePath, cifFilePath)
                if ptPL is not None:
                    self.__atomNumberDict = ptPL.getAtomNumberDict()

            while True:

                if isFilePath:
                    ifp = open(mrFilePath, 'r')  # pylint: disable=consider-using-with
                    input = InputStream(ifp.read())
                else:
                    input = InputStream(mrString)

                lexer = AmberMRLexer(input)
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
                parser = AmberMRParser(stream)
                parser.removeErrorListeners()
                parser_error_listener = ParserErrorListener(mrFilePath, maxErrorReport=self.__maxParserErrorReport)
                parser.addErrorListener(parser_error_listener)
                tree = parser.amber_mr()

                walker = ParseTreeWalker()
                listener = AmberMRParserListener(self.__verbose, self.__lfh,
                                                 self.__representativeModelId,
                                                 self.__cR, self.__cC,
                                                 self.__ccU, self.__csStat, self.__nefT,
                                                 self.__atomNumberDict)
                listener.setDebugMode(self.__debug)
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

                if self.__atomNumberDict is not None:
                    if self.__verbose:
                        if isFilePath:
                            print(listener.getContentSubtype())
                    break

                sanderAtomNumberDict = listener.getSanderAtomNumberDict()
                if len(sanderAtomNumberDict) > 0:
                    self.__atomNumberDict = sanderAtomNumberDict
                else:
                    break

                if isFilePath and ifp is not None:
                    ifp.close()

            return listener, parser_error_listener, lexer_error_listener

        except IOError as e:
            if self.__verbose:
                self.__lfh.write(f"+AmberMRReader.parse() ++ Error - {str(e)}\n")
            return None, None, None

        finally:
            if isFilePath and ifp is not None:
                ifp.close()


if __name__ == "__main__":
    reader = AmberMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/5n8m/RST-2-tensors.dip',
                 '../../tests-nmr/mock-data-remediation/5n8m/5n8m.cif',
                 None)

    reader = AmberMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-remediation/2lar/2lar-trimmed.mr',
                 '../../tests-nmr/mock-data-remediation/2lar/2lar.cif',
                 None)

    reader = AmberMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/D_1300018283_mr-upload_P1.dat.V1',
                 '../../tests-nmr/mock-data-daother-7690/D_1300018283_model-release_P1.cif.V3',
                 None)

    reader = AmberMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/D_1300020743_mr-upload_P1.amber.V1',
                 '../../tests-nmr/mock-data-daother-7690/D_1300020743_model-release_P1.cif.V2',
                 None)

    reader = AmberMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/D_1300028390_mr-upload_P1.amber.V1',
                 '../../tests-nmr/mock-data-daother-7690/D_1300028390_model-annotate_P1.cif.V2',
                 '../../tests-nmr/mock-data-daother-7690/D_1300028390_mr-upload_P1.dat.V1')

    reader = AmberMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7690/D_1300028390_mr-upload_P1.amber.V1',
                 '../../tests-nmr/mock-data-daother-7690/D_1300028390_model-annotate_P1.cif.V2',
                 None)

    reader = AmberMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7421/amber_rdc.test',
                 '../../tests-nmr/mock-data-daother-7421/D_800450_model_P1.cif.V1',
                 '../../tests-nmr/mock-data-daother-7421/D_1292118884_mr-upload_P1.dat.V1')

    reader = AmberMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7421/D_1292118884_mr-upload_P1.amber.V1',
                 '../../tests-nmr/mock-data-daother-7421/D_800450_model_P1.cif.V1',
                 None)

    reader = AmberMRReader(True)
    reader.setDebugMode(True)
    reader.parse('../../tests-nmr/mock-data-daother-7421/D_1292118884_mr-upload_P1.amber.V1',
                 '../../tests-nmr/mock-data-daother-7421/D_800450_model_P1.cif.V1',
                 '../../tests-nmr/mock-data-daother-7421/D_1292118884_mr-upload_P1.dat.V1')

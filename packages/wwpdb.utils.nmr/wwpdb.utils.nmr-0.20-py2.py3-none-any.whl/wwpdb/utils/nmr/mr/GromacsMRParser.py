# Generated from GromacsMRParser.g4 by ANTLR 4.10.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,17,127,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,1,0,1,0,1,0,1,0,1,
        0,5,0,30,8,0,10,0,12,0,33,9,0,1,0,1,0,1,1,1,1,1,1,1,1,4,1,41,8,1,
        11,1,12,1,42,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,3,
        1,3,4,3,59,8,3,11,3,12,3,60,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,
        1,5,1,5,1,5,1,5,4,5,76,8,5,11,5,12,5,77,1,6,1,6,1,6,1,6,1,6,1,6,
        1,6,1,6,1,6,1,6,1,7,1,7,1,7,1,7,4,7,94,8,7,11,7,12,7,95,1,8,1,8,
        1,8,3,8,101,8,8,1,8,3,8,104,8,8,1,8,1,8,1,8,1,8,1,8,1,9,1,9,1,9,
        1,9,4,9,115,8,9,11,9,12,9,116,1,10,1,10,1,10,1,10,1,10,1,10,1,11,
        1,11,1,11,0,0,12,0,2,4,6,8,10,12,14,16,18,20,22,0,1,1,0,8,9,126,
        0,31,1,0,0,0,2,36,1,0,0,0,4,44,1,0,0,0,6,54,1,0,0,0,8,62,1,0,0,0,
        10,71,1,0,0,0,12,79,1,0,0,0,14,89,1,0,0,0,16,97,1,0,0,0,18,110,1,
        0,0,0,20,118,1,0,0,0,22,124,1,0,0,0,24,30,3,2,1,0,25,30,3,6,3,0,
        26,30,3,10,5,0,27,30,3,14,7,0,28,30,3,18,9,0,29,24,1,0,0,0,29,25,
        1,0,0,0,29,26,1,0,0,0,29,27,1,0,0,0,29,28,1,0,0,0,30,33,1,0,0,0,
        31,29,1,0,0,0,31,32,1,0,0,0,32,34,1,0,0,0,33,31,1,0,0,0,34,35,5,
        0,0,1,35,1,1,0,0,0,36,37,5,1,0,0,37,38,5,3,0,0,38,40,5,2,0,0,39,
        41,3,4,2,0,40,39,1,0,0,0,41,42,1,0,0,0,42,40,1,0,0,0,42,43,1,0,0,
        0,43,3,1,0,0,0,44,45,5,8,0,0,45,46,5,8,0,0,46,47,5,8,0,0,47,48,5,
        8,0,0,48,49,5,8,0,0,49,50,3,22,11,0,50,51,3,22,11,0,51,52,3,22,11,
        0,52,53,3,22,11,0,53,5,1,0,0,0,54,55,5,1,0,0,55,56,5,4,0,0,56,58,
        5,2,0,0,57,59,3,8,4,0,58,57,1,0,0,0,59,60,1,0,0,0,60,58,1,0,0,0,
        60,61,1,0,0,0,61,7,1,0,0,0,62,63,5,8,0,0,63,64,5,8,0,0,64,65,5,8,
        0,0,65,66,5,8,0,0,66,67,5,8,0,0,67,68,3,22,11,0,68,69,3,22,11,0,
        69,70,3,22,11,0,70,9,1,0,0,0,71,72,5,1,0,0,72,73,5,5,0,0,73,75,5,
        2,0,0,74,76,3,12,6,0,75,74,1,0,0,0,76,77,1,0,0,0,77,75,1,0,0,0,77,
        78,1,0,0,0,78,11,1,0,0,0,79,80,5,8,0,0,80,81,5,8,0,0,81,82,5,8,0,
        0,82,83,5,8,0,0,83,84,5,8,0,0,84,85,3,22,11,0,85,86,3,22,11,0,86,
        87,3,22,11,0,87,88,3,22,11,0,88,13,1,0,0,0,89,90,5,1,0,0,90,91,5,
        6,0,0,91,93,5,2,0,0,92,94,3,16,8,0,93,92,1,0,0,0,94,95,1,0,0,0,95,
        93,1,0,0,0,95,96,1,0,0,0,96,15,1,0,0,0,97,98,5,8,0,0,98,100,5,8,
        0,0,99,101,5,8,0,0,100,99,1,0,0,0,100,101,1,0,0,0,101,103,1,0,0,
        0,102,104,5,8,0,0,103,102,1,0,0,0,103,104,1,0,0,0,104,105,1,0,0,
        0,105,106,5,8,0,0,106,107,3,22,11,0,107,108,3,22,11,0,108,109,5,
        8,0,0,109,17,1,0,0,0,110,111,5,1,0,0,111,112,5,7,0,0,112,114,5,2,
        0,0,113,115,3,20,10,0,114,113,1,0,0,0,115,116,1,0,0,0,116,114,1,
        0,0,0,116,117,1,0,0,0,117,19,1,0,0,0,118,119,5,8,0,0,119,120,5,8,
        0,0,120,121,3,22,11,0,121,122,3,22,11,0,122,123,3,22,11,0,123,21,
        1,0,0,0,124,125,7,0,0,0,125,23,1,0,0,0,9,29,31,42,60,77,95,100,103,
        116
    ]

class GromacsMRParser ( Parser ):

    grammarFileName = "GromacsMRParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'['", "']'", "'distance_restraints'", 
                     "'dihedral_restraints'", "'orientation_restraints'", 
                     "'angle_restraints'", "'position_restraints'" ]

    symbolicNames = [ "<INVALID>", "L_brkt", "R_brkt", "Distance_restraints", 
                      "Dihedral_restraints", "Orientation_restraints", "Angle_restraints", 
                      "Position_restraints", "Integer", "Float", "SHARP_COMMENT", 
                      "EXCLM_COMMENT", "SMCLN_COMMENT", "Simple_name", "SPACE", 
                      "COMMENT", "SECTION_COMMENT", "LINE_COMMENT" ]

    RULE_gromacs_mr = 0
    RULE_distance_restraints = 1
    RULE_distance_restraint = 2
    RULE_dihedral_restraints = 3
    RULE_dihedral_restraint = 4
    RULE_orientation_restraints = 5
    RULE_orientation_restraint = 6
    RULE_angle_restraints = 7
    RULE_angle_restraint = 8
    RULE_position_restraints = 9
    RULE_position_restraint = 10
    RULE_number = 11

    ruleNames =  [ "gromacs_mr", "distance_restraints", "distance_restraint", 
                   "dihedral_restraints", "dihedral_restraint", "orientation_restraints", 
                   "orientation_restraint", "angle_restraints", "angle_restraint", 
                   "position_restraints", "position_restraint", "number" ]

    EOF = Token.EOF
    L_brkt=1
    R_brkt=2
    Distance_restraints=3
    Dihedral_restraints=4
    Orientation_restraints=5
    Angle_restraints=6
    Position_restraints=7
    Integer=8
    Float=9
    SHARP_COMMENT=10
    EXCLM_COMMENT=11
    SMCLN_COMMENT=12
    Simple_name=13
    SPACE=14
    COMMENT=15
    SECTION_COMMENT=16
    LINE_COMMENT=17

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.10.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Gromacs_mrContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(GromacsMRParser.EOF, 0)

        def distance_restraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GromacsMRParser.Distance_restraintsContext)
            else:
                return self.getTypedRuleContext(GromacsMRParser.Distance_restraintsContext,i)


        def dihedral_restraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GromacsMRParser.Dihedral_restraintsContext)
            else:
                return self.getTypedRuleContext(GromacsMRParser.Dihedral_restraintsContext,i)


        def orientation_restraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GromacsMRParser.Orientation_restraintsContext)
            else:
                return self.getTypedRuleContext(GromacsMRParser.Orientation_restraintsContext,i)


        def angle_restraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GromacsMRParser.Angle_restraintsContext)
            else:
                return self.getTypedRuleContext(GromacsMRParser.Angle_restraintsContext,i)


        def position_restraints(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GromacsMRParser.Position_restraintsContext)
            else:
                return self.getTypedRuleContext(GromacsMRParser.Position_restraintsContext,i)


        def getRuleIndex(self):
            return GromacsMRParser.RULE_gromacs_mr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGromacs_mr" ):
                listener.enterGromacs_mr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGromacs_mr" ):
                listener.exitGromacs_mr(self)




    def gromacs_mr(self):

        localctx = GromacsMRParser.Gromacs_mrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_gromacs_mr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==GromacsMRParser.L_brkt:
                self.state = 29
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 24
                    self.distance_restraints()
                    pass

                elif la_ == 2:
                    self.state = 25
                    self.dihedral_restraints()
                    pass

                elif la_ == 3:
                    self.state = 26
                    self.orientation_restraints()
                    pass

                elif la_ == 4:
                    self.state = 27
                    self.angle_restraints()
                    pass

                elif la_ == 5:
                    self.state = 28
                    self.position_restraints()
                    pass


                self.state = 33
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 34
            self.match(GromacsMRParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Distance_restraintsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_brkt(self):
            return self.getToken(GromacsMRParser.L_brkt, 0)

        def Distance_restraints(self):
            return self.getToken(GromacsMRParser.Distance_restraints, 0)

        def R_brkt(self):
            return self.getToken(GromacsMRParser.R_brkt, 0)

        def distance_restraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GromacsMRParser.Distance_restraintContext)
            else:
                return self.getTypedRuleContext(GromacsMRParser.Distance_restraintContext,i)


        def getRuleIndex(self):
            return GromacsMRParser.RULE_distance_restraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDistance_restraints" ):
                listener.enterDistance_restraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDistance_restraints" ):
                listener.exitDistance_restraints(self)




    def distance_restraints(self):

        localctx = GromacsMRParser.Distance_restraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_distance_restraints)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.match(GromacsMRParser.L_brkt)
            self.state = 37
            self.match(GromacsMRParser.Distance_restraints)
            self.state = 38
            self.match(GromacsMRParser.R_brkt)
            self.state = 40 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 39
                self.distance_restraint()
                self.state = 42 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==GromacsMRParser.Integer):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Distance_restraintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(GromacsMRParser.Integer)
            else:
                return self.getToken(GromacsMRParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GromacsMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(GromacsMRParser.NumberContext,i)


        def getRuleIndex(self):
            return GromacsMRParser.RULE_distance_restraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDistance_restraint" ):
                listener.enterDistance_restraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDistance_restraint" ):
                listener.exitDistance_restraint(self)




    def distance_restraint(self):

        localctx = GromacsMRParser.Distance_restraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_distance_restraint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.match(GromacsMRParser.Integer)
            self.state = 45
            self.match(GromacsMRParser.Integer)
            self.state = 46
            self.match(GromacsMRParser.Integer)
            self.state = 47
            self.match(GromacsMRParser.Integer)
            self.state = 48
            self.match(GromacsMRParser.Integer)
            self.state = 49
            self.number()
            self.state = 50
            self.number()
            self.state = 51
            self.number()
            self.state = 52
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Dihedral_restraintsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_brkt(self):
            return self.getToken(GromacsMRParser.L_brkt, 0)

        def Dihedral_restraints(self):
            return self.getToken(GromacsMRParser.Dihedral_restraints, 0)

        def R_brkt(self):
            return self.getToken(GromacsMRParser.R_brkt, 0)

        def dihedral_restraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GromacsMRParser.Dihedral_restraintContext)
            else:
                return self.getTypedRuleContext(GromacsMRParser.Dihedral_restraintContext,i)


        def getRuleIndex(self):
            return GromacsMRParser.RULE_dihedral_restraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDihedral_restraints" ):
                listener.enterDihedral_restraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDihedral_restraints" ):
                listener.exitDihedral_restraints(self)




    def dihedral_restraints(self):

        localctx = GromacsMRParser.Dihedral_restraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_dihedral_restraints)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54
            self.match(GromacsMRParser.L_brkt)
            self.state = 55
            self.match(GromacsMRParser.Dihedral_restraints)
            self.state = 56
            self.match(GromacsMRParser.R_brkt)
            self.state = 58 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 57
                self.dihedral_restraint()
                self.state = 60 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==GromacsMRParser.Integer):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Dihedral_restraintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(GromacsMRParser.Integer)
            else:
                return self.getToken(GromacsMRParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GromacsMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(GromacsMRParser.NumberContext,i)


        def getRuleIndex(self):
            return GromacsMRParser.RULE_dihedral_restraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDihedral_restraint" ):
                listener.enterDihedral_restraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDihedral_restraint" ):
                listener.exitDihedral_restraint(self)




    def dihedral_restraint(self):

        localctx = GromacsMRParser.Dihedral_restraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_dihedral_restraint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self.match(GromacsMRParser.Integer)
            self.state = 63
            self.match(GromacsMRParser.Integer)
            self.state = 64
            self.match(GromacsMRParser.Integer)
            self.state = 65
            self.match(GromacsMRParser.Integer)
            self.state = 66
            self.match(GromacsMRParser.Integer)
            self.state = 67
            self.number()
            self.state = 68
            self.number()
            self.state = 69
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Orientation_restraintsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_brkt(self):
            return self.getToken(GromacsMRParser.L_brkt, 0)

        def Orientation_restraints(self):
            return self.getToken(GromacsMRParser.Orientation_restraints, 0)

        def R_brkt(self):
            return self.getToken(GromacsMRParser.R_brkt, 0)

        def orientation_restraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GromacsMRParser.Orientation_restraintContext)
            else:
                return self.getTypedRuleContext(GromacsMRParser.Orientation_restraintContext,i)


        def getRuleIndex(self):
            return GromacsMRParser.RULE_orientation_restraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrientation_restraints" ):
                listener.enterOrientation_restraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrientation_restraints" ):
                listener.exitOrientation_restraints(self)




    def orientation_restraints(self):

        localctx = GromacsMRParser.Orientation_restraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_orientation_restraints)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            self.match(GromacsMRParser.L_brkt)
            self.state = 72
            self.match(GromacsMRParser.Orientation_restraints)
            self.state = 73
            self.match(GromacsMRParser.R_brkt)
            self.state = 75 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 74
                self.orientation_restraint()
                self.state = 77 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==GromacsMRParser.Integer):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Orientation_restraintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(GromacsMRParser.Integer)
            else:
                return self.getToken(GromacsMRParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GromacsMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(GromacsMRParser.NumberContext,i)


        def getRuleIndex(self):
            return GromacsMRParser.RULE_orientation_restraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrientation_restraint" ):
                listener.enterOrientation_restraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrientation_restraint" ):
                listener.exitOrientation_restraint(self)




    def orientation_restraint(self):

        localctx = GromacsMRParser.Orientation_restraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_orientation_restraint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 79
            self.match(GromacsMRParser.Integer)
            self.state = 80
            self.match(GromacsMRParser.Integer)
            self.state = 81
            self.match(GromacsMRParser.Integer)
            self.state = 82
            self.match(GromacsMRParser.Integer)
            self.state = 83
            self.match(GromacsMRParser.Integer)
            self.state = 84
            self.number()
            self.state = 85
            self.number()
            self.state = 86
            self.number()
            self.state = 87
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Angle_restraintsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_brkt(self):
            return self.getToken(GromacsMRParser.L_brkt, 0)

        def Angle_restraints(self):
            return self.getToken(GromacsMRParser.Angle_restraints, 0)

        def R_brkt(self):
            return self.getToken(GromacsMRParser.R_brkt, 0)

        def angle_restraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GromacsMRParser.Angle_restraintContext)
            else:
                return self.getTypedRuleContext(GromacsMRParser.Angle_restraintContext,i)


        def getRuleIndex(self):
            return GromacsMRParser.RULE_angle_restraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAngle_restraints" ):
                listener.enterAngle_restraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAngle_restraints" ):
                listener.exitAngle_restraints(self)




    def angle_restraints(self):

        localctx = GromacsMRParser.Angle_restraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_angle_restraints)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 89
            self.match(GromacsMRParser.L_brkt)
            self.state = 90
            self.match(GromacsMRParser.Angle_restraints)
            self.state = 91
            self.match(GromacsMRParser.R_brkt)
            self.state = 93 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 92
                self.angle_restraint()
                self.state = 95 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==GromacsMRParser.Integer):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Angle_restraintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(GromacsMRParser.Integer)
            else:
                return self.getToken(GromacsMRParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GromacsMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(GromacsMRParser.NumberContext,i)


        def getRuleIndex(self):
            return GromacsMRParser.RULE_angle_restraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAngle_restraint" ):
                listener.enterAngle_restraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAngle_restraint" ):
                listener.exitAngle_restraint(self)




    def angle_restraint(self):

        localctx = GromacsMRParser.Angle_restraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_angle_restraint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 97
            self.match(GromacsMRParser.Integer)
            self.state = 98
            self.match(GromacsMRParser.Integer)
            self.state = 100
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.state = 99
                self.match(GromacsMRParser.Integer)


            self.state = 103
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.state = 102
                self.match(GromacsMRParser.Integer)


            self.state = 105
            self.match(GromacsMRParser.Integer)
            self.state = 106
            self.number()
            self.state = 107
            self.number()
            self.state = 108
            self.match(GromacsMRParser.Integer)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Position_restraintsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_brkt(self):
            return self.getToken(GromacsMRParser.L_brkt, 0)

        def Position_restraints(self):
            return self.getToken(GromacsMRParser.Position_restraints, 0)

        def R_brkt(self):
            return self.getToken(GromacsMRParser.R_brkt, 0)

        def position_restraint(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GromacsMRParser.Position_restraintContext)
            else:
                return self.getTypedRuleContext(GromacsMRParser.Position_restraintContext,i)


        def getRuleIndex(self):
            return GromacsMRParser.RULE_position_restraints

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPosition_restraints" ):
                listener.enterPosition_restraints(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPosition_restraints" ):
                listener.exitPosition_restraints(self)




    def position_restraints(self):

        localctx = GromacsMRParser.Position_restraintsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_position_restraints)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 110
            self.match(GromacsMRParser.L_brkt)
            self.state = 111
            self.match(GromacsMRParser.Position_restraints)
            self.state = 112
            self.match(GromacsMRParser.R_brkt)
            self.state = 114 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 113
                self.position_restraint()
                self.state = 116 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==GromacsMRParser.Integer):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Position_restraintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Integer(self, i:int=None):
            if i is None:
                return self.getTokens(GromacsMRParser.Integer)
            else:
                return self.getToken(GromacsMRParser.Integer, i)

        def number(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GromacsMRParser.NumberContext)
            else:
                return self.getTypedRuleContext(GromacsMRParser.NumberContext,i)


        def getRuleIndex(self):
            return GromacsMRParser.RULE_position_restraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPosition_restraint" ):
                listener.enterPosition_restraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPosition_restraint" ):
                listener.exitPosition_restraint(self)




    def position_restraint(self):

        localctx = GromacsMRParser.Position_restraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_position_restraint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            self.match(GromacsMRParser.Integer)
            self.state = 119
            self.match(GromacsMRParser.Integer)
            self.state = 120
            self.number()
            self.state = 121
            self.number()
            self.state = 122
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Float(self):
            return self.getToken(GromacsMRParser.Float, 0)

        def Integer(self):
            return self.getToken(GromacsMRParser.Integer, 0)

        def getRuleIndex(self):
            return GromacsMRParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)




    def number(self):

        localctx = GromacsMRParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            _la = self._input.LA(1)
            if not(_la==GromacsMRParser.Integer or _la==GromacsMRParser.Float):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx






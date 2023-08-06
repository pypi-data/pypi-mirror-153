##
# File: AlignUtil.py
# Date: 18-Feb-2022
#
# Updates:
""" Utilities for pairwise alignment.
    @author: Masashi Yokochi
"""


# empty value
emptyValue = (None, '', '.', '?', 'null')


# true value
trueValue = ('true', 't', 'yes', 'y', '1')


# taken from wwpdb.utils.align.SequenceReferenceData.py
monDict3 = {'ALA': 'A',
            'ARG': 'R',
            'ASN': 'N',
            'ASP': 'D',
            'ASX': 'B',
            'CYS': 'C',
            'GLN': 'Q',
            'GLU': 'E',
            'GLX': 'Z',
            'GLY': 'G',
            'HIS': 'H',
            'ILE': 'I',
            'LEU': 'L',
            'LYS': 'K',
            'MET': 'M',
            'PHE': 'F',
            'PRO': 'P',
            'SER': 'S',
            'THR': 'T',
            'TRP': 'W',
            'TYR': 'Y',
            'VAL': 'V',
            'DA': 'A',
            'DC': 'C',
            'DG': 'G',
            'DT': 'T',
            'DU': 'U',
            'DI': 'I',
            'A': 'A',
            'C': 'C',
            'G': 'G',
            'I': 'I',
            'T': 'T',
            'U': 'U'
            }


def hasLargeSeqGap(polySeq1, polySeq2):
    """ Return whether large gap in combined sequence of polySeq1 and polySeq2.
    """

    _s = sorted(set(polySeq1['seq_id']) | set(polySeq2['seq_id']))

    for idx, seqId in enumerate(_s):
        if idx > 0 and seqId - _s[idx - 1] > 20:
            return True

    return False


def fillBlankCompId(polySeq1, polySeq2):
    """ Fill blanked comp ID in polySeq2 against polySeq1.
    """

    _s = sorted(set(polySeq1['seq_id']) | set(polySeq2['seq_id']))
    _c = []

    for seqId in _s:
        if seqId in polySeq2['seq_id']:
            idx = polySeq2['seq_id'].index(seqId)
            if idx < len(polySeq2['comp_id']):
                _c.append(polySeq2['comp_id'][idx])
            else:
                _c.append('.')
        else:
            _c.append('.')

    return {'chain_id': polySeq2['chain_id'], 'seq_id': _s, 'comp_id': _c}


def fillBlankCompIdWithOffset(ps, offset):
    """ Fill blanked comp ID with offset.
    """

    _s = list(range(ps['seq_id'][0] - offset, ps['seq_id'][-1] + 1))
    _c = []

    for seqId in _s:
        if seqId in ps['seq_id']:
            idx = ps['seq_id'].index(seqId)
            if idx < len(ps['comp_id']):
                _c.append(ps['comp_id'][idx])
            else:
                _c.append('.')
        else:
            _c.append('.')

    return {'chain_id': ps['chain_id'], 'seq_id': _s, 'comp_id': _c}


def beautifyPolySeq(polySeq1, polySeq2):
    """ Truncate negative seq IDs and insert spacing between the large gap.
    """

    _polySeq1 = fillBlankCompId(polySeq2, polySeq1)  # pylint: disable=arguments-out-of-order
    _polySeq2 = fillBlankCompId(polySeq1, polySeq2)  # pylint: disable=arguments-out-of-order

    if _polySeq1['seq_id'] != _polySeq2['seq_id']:
        return _polySeq1, _polySeq2

    _s = [seqId for seqId in _polySeq1['seq_id'] if seqId > 0]
    _c1 = [compId for seqId, compId
           in zip(_polySeq1['seq_id'], _polySeq1['comp_id']) if seqId > 0]
    _c2 = [compId for seqId, compId
           in zip(_polySeq1['seq_id'], _polySeq2['comp_id']) if seqId > 0]

    gapS = []
    gapP = []

    lenSpacer = 5  # DAOTHER-7465, issue #2

    for idx, seqId in enumerate(_s):
        if idx > 0 and seqId - _s[idx - 1] > 20:
            prevSeqId = _s[idx - 1]
            for sp in range(1, lenSpacer + 1):
                gapS.append(prevSeqId + sp)
                gapS.append(seqId - sp)
            gapP.append(idx)

    if len(gapS) == 0:
        return {'chain_id': _polySeq1['chain_id'], 'seq_id': _s, 'comp_id': _c1},\
               {'chain_id': _polySeq2['chain_id'], 'seq_id': _s, 'comp_id': _c2}

    _s.extend(gapS)
    _s.sort()

    for p in reversed(gapP):
        for sp in range(1, lenSpacer + 1):
            _c1.insert(p, '.')
            _c2.insert(p, '.')

    return {'chain_id': _polySeq1['chain_id'], 'seq_id': _s, 'comp_id': _c1},\
           {'chain_id': _polySeq2['chain_id'], 'seq_id': _s, 'comp_id': _c2}


def getMiddleCode(seqIdList1, seqIdList2):
    """ Return array of middle code of sequence alignment.
    """

    middleCode = ''

    for idx, seqId in enumerate(seqIdList1):
        if idx < len(seqIdList2):
            middleCode += '|' if seqId == seqIdList2[idx] and seqId != '.' else ' '
        else:
            middleCode += ' '

    return middleCode


def getGaugeCode(seqIdList, offset=0):
    """ Return gauge code for a give sequence.
    """

    if offset > 0:
        _seqIdList = list(range(1, offset + 1))
        for idx, seqId in enumerate(seqIdList):
            if idx < offset:
                continue
            _seqIdList.append(seqId)
        seqIdList = _seqIdList

    lenSeqId = len([seqId for seqId in seqIdList if seqId is not None])
    lenCode = 0

    chars = []

    for seqId in seqIdList:

        if seqId is None:
            chars.append('-')
            continue

        if seqId >= 0 and seqId % 10 == 0 and lenCode == 0:

            code = str(seqId)
            lenCode = len(code)

            for p in range(lenCode):
                chars.append(code[p])

        if lenCode > 0:
            lenCode -= 1
        else:
            chars.append('-')

    lenChars = len(chars)

    for idx, seqId in enumerate(seqIdList):

        if seqId is None or seqId % 10 != 0:
            continue

        code = str(seqId)
        lenCode = len(code)

        if idx - lenCode > 0:
            for p in range(lenCode):
                if idx + p - lenCode + 1 >= 0 and idx + p < lenChars:
                    chars[idx + p - lenCode + 1] = chars[idx + p]
                    chars[idx + p] = '-'

    if offset > 0:
        for p in range(offset):
            chars[p] = '-'

    gaugeCode = ''.join(chars)

    if lenSeqId == len(seqIdList):
        return gaugeCode[:lenSeqId]

    _lenSeqId = len(seqIdList)

    offset = 0
    for idx, seqId in enumerate(seqIdList):

        if seqId is None:
            p = idx + offset
            gaugeCode = gaugeCode[0:p] + ' ' + gaugeCode[p:]
            offset += 1

    return gaugeCode[:_lenSeqId]


def getScoreOfSeqAlign(myAlign):
    """ Return score of sequence alignment.
    """

    length = len(myAlign)

    aligned = [True] * length

    for p in range(length):
        myPr = myAlign[p]
        myPr0 = str(myPr[0])
        myPr1 = str(myPr[1])
        if myPr0 == '.' or myPr1 == '.':
            aligned[p] = False
        elif myPr0 != myPr1:
            pass
        else:
            break

    notAligned = True
    offset1 = 0
    offset2 = 0

    unmapped = 0
    conflict = 0
    matched = 0
    for p in range(length):
        myPr = myAlign[p]
        myPr0 = str(myPr[0])
        myPr1 = str(myPr[1])
        if myPr0 == '.' or myPr1 == '.':
            if notAligned and not aligned[p]:
                if myPr0 == '.' and myPr1 != '.'\
                   and offset2 == 0:  # DAOTHER-7421
                    offset1 += 1
                if myPr0 != '.' and myPr1 == '.'\
                   and offset1 == 0:  # DAOTHER-7421
                    offset2 += 1
                if myPr0 == '.' and myPr1 == '.':  # DAOTHER-7465
                    if offset2 == 0:
                        offset1 += 1
                    if offset1 == 0:
                        offset2 += 1
            unmapped += 1
        elif myPr0 != myPr1:
            conflict += 1
        else:
            notAligned = False
            matched += 1

    return matched, unmapped, conflict, offset1, offset2


def getOneLetterCode(compId):
    """ Convert comp ID to 1-letter code.
    """

    compId = compId.upper()

    if compId in monDict3:
        return monDict3[compId]

    if compId in emptyValue:
        return '.'

    return 'X'


def getOneLetterCodeSequence(compIdList):
    """ Convert array of comp IDs to 1-letter code sequence.
    """

    compCode = ''

    for compId in compIdList:
        compCode += getOneLetterCode(compId)

    return compCode


def letterToDigit(code, minDigit=0):
    """ Return digit from a given chain code.
    """

    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    unit = 1
    digit = 0

    for char in ''.join(reversed(code.lower())):

        if char.isdigit():
            digit += unit * int(char)
        elif char.isalpha():
            digit += unit * (alphabet.index(char) + 1)
        else:
            continue

        unit *= 27

    return digit if digit > minDigit else minDigit


def indexToLetter(index):
    """ Return chain code from a given index (0 based).
    """

    if index < 0:
        return '.'

    if index > 19683:
        index = index % 19683

    if index < 27:
        return str(chr(65 + index))

    if index < 729:
        return str(chr(64 + (index // 27)))\
            + str(chr(65 + (index % 27)))

    return str(chr(64 + (index // 729)))\
        + str(chr(64 + ((index % 729) // 27)))\
        + str(chr(65 + (index % 27)))

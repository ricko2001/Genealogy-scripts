from enum import Enum

# ===================================================DIV60==


def main():
    # RD = "DR+19210113..+19220125.."
    RD = "D-+19210113.S+00010000.."
    # SD = 6710968738434343951
    SD = 6710968736419938325

    print(from_RMDate(RD, Format.SHORT))
    print(to_RMsort_date(RD))
    print(from_RMsort_date(SD))


# ===================================================DIV60==
def to_RMDate(DateStr, form):
    # form is Format.LONG, Format.SHORT
    # may want to first implement with strict canonical format and
    # later implement logic found in RM to interpret strings.

    raise Exception("ToRMDate not yet implemented")

    return ""

# ===================================================DIV60==


def from_RMDate(RMDate, form):
    # form is Format.LONG, Format.SHORT

    date_type = RMDate[0:1]
    if date_type == 'T':
        return RMDate[1:]
    elif date_type == 'Q':
        raise Exception("RM Quaker dates not yet supported")
    elif date_type == 'R':
        raise Exception("RM Quarter dates not yet supported")
    elif date_type == '.':
        return ""
    elif date_type == 'D':
        pass  # continue and process D type below
    else:
        raise Exception("Malformed RM Date: unsuported start character")

    # Handle D type Dates
    if len(RMDate) != 24:
        raise Exception("Malformed RM Date: wrong length")

    Char_1_2 = RMDate[1:2]
    data_s = RMdate_structure()
    StructCodeE = data_s.get_enum_from_symbol(Char_1_2)

    Char_2_3 = RMDate[2:3]
    if Char_2_3 == '-':
        AdBc_1 = ' BC'
    elif Char_2_3 == '+':
        AdBc_1 = ''
    else:
        raise Exception("Malformed RM Date: AD-BC_1 indicator")

    try:
        year_1 = (RMDate[3:7]).lstrip("0")
        month_1_i = int(RMDate[7:9])
        day_1 = RMDate[9:11].lstrip("0")
    except ValueError as ve:
        raise Exception("Malformed RM Date: Invalid characters in date 1")

    Char_11_12 = RMDate[11:12]
    DoubDate_1 = False
    if Char_11_12 == '/':
        DoubDate_1 = True
    elif Char_11_12 != '.':
        raise Exception("Malformed RM Date: Double Date 1 indicator")

    Char_12_13 = RMDate[12:13]
    data_c = RMdate_confidence()
    ConfidenceE_1 = data_c.get_enum_from_symbol(Char_12_13)

    Char_13_14 = RMDate[13:14]
    if Char_13_14 == '-':
        AdBc_2 = ' BC'
    elif Char_13_14 == '+':
        AdBc_2 = ''
    else:
        raise Exception("Malformed RM Date: AD-BC_2 indicator")

    # must be all 0 if not date range Confidence
    try:
        year_2 = RMDate[14:18].lstrip("0")
        month_2_i = int(RMDate[18:20])
        day_2 = RMDate[20:22].lstrip("0")
    except ValueError as ve:
        raise Exception("Malformed RM Date: Invalid characters in date 1")

        # complicated TODO
    Char_22_23 = RMDate[22:23]
    DoubDate_2 = False
    if Char_22_23 == '/':
        DoubDate_2 = True
    elif Char_22_23 != '.':
        raise Exception("Malformed RM Date: Double Date 2 indicator")

    # only if 2nd date
    Char_23_24 = RMDate[23:24]
    ConfidenceE_2 = data_c.get_enum_from_symbol(Char_23_24)

    SingleDate = False
    if year_2 == '' and month_2_i == 0 and day_2 == '' and AdBc_2 == '':
        SingleDate = True

    if SingleDate and RMdate_structure[StructCodeE][2] == 2:
        raise Exception(
            "Malformed date: conflict between struct code & second date empty")

    if year_1 != '' and day_1 != '' and month_1_i == 0:
        month_1_i = 13
    if day_1 != '':
        day_1 = day_1 + ' '
    if year_1 == '' or (year_1 != '' and month_1_i == 0):
        month_trsp_1 = ''
    else:
        month_trsp_1 = ' '

        fDate_1 = (data_s.get_str_1(StructCodeE, form) + data_c.get_str(ConfidenceE_1, form)
                   + day_1 + NumToMonthStr(month_1_i, 0) + month_trsp_1 + year_1 + AdBc_1)

    fDate = ''
    if SingleDate:
        fDate = fDate_1
    else:
        if year_2 != '' and day_2 != '' and month_2_i == 0:
            month_2_i = 13
        if day_2 != '':
            day_2 = day_2 + ' '
        if year_2 == '' or (year_2 != '' and month_2_i == 0):
            month_trsp_2 = ''
        else:
            month_trsp_2 = ' '

        fDate_2 = (data_s.get_str_2(StructCodeE, form) + data_c.get_str(ConfidenceE_2, form)
                   + day_2 + NumToMonthStr(month_2_i, 0) + month_trsp_2 + year_2 + AdBc_2)

        fDate = fDate_1 + fDate_2

    return fDate


# ===================================================DIV60==
def to_RMsort_date(RM_date):
    # RM_date is an RM internal date string

    date_type = RM_date[0:1]
    # Julian date / slash date
    date_type_slash = RM_date[11:12]

    try:
        year_1 = int(RM_date[3:7])
        month_1 = int(RM_date[7:9])
        day_1 = int(RM_date[9:11])
    except ValueError as ve:
        raise Exception("Malformed RM Date: Invalid characters in date part 1")

    try:
        year_2 = int(RM_date[14:18])
        month_2 = int(RM_date[18:20])
        day_2 = int(RM_date[20:22])
    except ValueError as ve:
        raise Exception("Malformed RM Date: Invalid characters in date part 2")

    if date_type in ('.', 'T'):
        # x'7F FF FF FF FF FF FF FF' (2^63-1)
        RM_sort_date = 9223372036854775807

    Char_1_2 = RM_date[1:2]
    struct_data = RMdate_structure()
    offset = struct_data.get_offset_from_symbol(Char_1_2)

    if year_1 == 0 and ((month_1 != 0) or (day_1 != 0)):
        y1 = 16383 << 49  # a date with no year
    else:
        # Slash date is in Julian and increments year by 1
        y1 = ((year_1 + 10000 + (1 if date_type_slash else 0)) << 49)

    if year_2 == 0:
        y2 = 17178820608     # x'03 FF F0 00 00' or (2^34 - 2^20)
    else:
        y2 = (year_2 + 10000) << 20

    return (y1 + (month_1 << 45) + (day_1 << 39)
              + y2 + (month_2 << 16) + (day_2 << 10) + offset)


# ===================================================DIV60==
def from_RMsort_date(RM_sort_date):

    # cannot produce
    # BC dates
    # confidence indicators
    # slash dates

    Y1 = (RM_sort_date >> 49) - 10000
    M1 = (RM_sort_date >> 45) & 0xf
    D1 = (RM_sort_date >> 39) & 0x3f
    Y2 = ((RM_sort_date >> 20) & 0x3fff) - 10000
    M2 = (RM_sort_date >> 16) & 0xf
    D2 = (RM_sort_date >> 10) & 0x3f
    F = RM_sort_date & 0x3ff

    data_s = RMdate_structure()
    FF = data_s.get_symbol_from_offset(F)

    #  raise Exception("FromRMSortDate not yet implemented")
 # "DR+19210113..+19220125.."

    RM_date = ( "D" + FF + "+{:=04}{:=02}{:=02}".format(Y1, M1, D1)
               + ".." + "{:=04}{:=02}{:=02}".format(Y2, M2, D2) + ".." )

    return RM_date


# ===================================================DIV60==
class StructCode(Enum):
    NORM = 1
    AFT = 2
    BEF = 3
    FROM = 4
    SINC = 5
    TO = 6
    UNTL = 7
    BY = 8
    OR = 9
    BTWN = 10
    FRTO = 11
    DASH = 12

# ===================================================DIV60==
class RMdate_structure:

    _data = (
        #  fmt: off
        #          0          1      2          3    4         5          6        7
        #          enum       sym    offset     num  1stShort  1stLong    2ndShort 2ndLong
        ( StructCode.NORM,    '.',   12,        1,   '',       '',        '',      ''     ),
        ( StructCode.AFT,     'A',   1047583,   1,   'aft ',   'after ',  '',      ''     ),
        ( StructCode.BEF,     'B',   0,         1,   'bef ',   'before ', '',      ''     ),
        ( StructCode.FROM,    'F',   1047579,   1,   'from ',  'from ',   '',      ''     ),
        ( StructCode.SINC,    'I',   1047582,   1,   'since ', 'since ',  '',      ''     ),
        ( StructCode.TO,      'T',   6,         1,   'to ',    'to ',     '',      ''     ),
        ( StructCode.UNTL,    'U',   9,         1,   'until ', 'until ',  '',      ''     ),
        ( StructCode.BY,      'Y',   3,         1,   'by ',    'by ',     '',      ''     ),
        ( StructCode.OR,      'O',   24,        2,   '',       '',        ' or ',  ' or ' ),
        ( StructCode.BTWN,    'R',   15,        2,   'bet ',   'between ' ' and ', ' and '),
        ( StructCode.FRTO,    'S',   18,        2,   'from ',  'from ',   ' to ',  ' to ' ),
        ( StructCode.DASH,    '-',   21,        2,   '',       '',        '–',     '–'    )
        # fmt: on
    )

# Sort order  TODO
# F FROM  = 1047579 = (27 + xFFC00)
# I SINCE = 1047582 = (30 + xFFC00)
# A AFTER = 1047583 = (31 + xFFC00)

    def get_enum_from_symbol(self, symbol):
        for date_type in RMdate_structure._data:
            if symbol == date_type[1]:
                return date_type[0]
        raise Exception(
            "Malformed RM Date: StructCode character, no enum available")

    def get_offset_from_symbol(self, symbol):
        for date_type in RMdate_structure._data:
            if symbol == date_type[1]:
                return date_type[2]
        raise Exception(
            "Malformed RM Date: StructCode character, no offset available")

    def get_symbol_from_offset(self, offset):
        for date_type in RMdate_structure._data:
            if offset == date_type[2]:
                return date_type[1]
        raise Exception(
            "Malformed RM Date: unsuported offset")

    def get_str_1(self, type, format):
        for date_type in RMdate_structure._data:
            if type == date_type[0]:
                if format == Format.SHORT:
                    return date_type[4]
                elif format == Format.LONG:
                    return date_type[5]
                else:
                    raise Exception("Format not supported")
        raise Exception(
            "Malformed RM Date: StructCode character, no offset available")

    def get_str_2(self, type, format):
        for date_type in RMdate_structure._data:
            if type == date_type[0]:
                if format == Format.SHORT:
                    return date_type[6]
                elif format == Format.LONG:
                    return date_type[7]
                else:
                    raise Exception("Format not supported")
        raise Exception(
            "Malformed RM Date: StructCode character, no offset available")

 # ===================================================DIV60==
class ConfidenceCode(Enum):
    NONE = 1
    ABT = 2
    SAY = 3
    CIR = 4
    EST = 5
    CAL = 6
    MAY = 7
    PER = 8
    APAR = 9
    LKLY = 10
    POSS = 11
    PROB = 12
    CERT = 13


# ===================================================DIV60==
class RMdate_confidence:

    _data = (
        # fmt: off 
        #                0        1       2              3
        #                enum     sym     short          long
        ( ConfidenceCode.NONE,    '.',    "",            ""           ),
        ( ConfidenceCode.ABT,     'A',    "abt ",        "about "     ),
        ( ConfidenceCode.SAY,     'S',    "say ",        "say "       ),
        ( ConfidenceCode.CIR,     'C',    "ca ",         "circa "     ),
        ( ConfidenceCode.EST,     'E',    "est ",        "estimated " ),
        ( ConfidenceCode.CAL,     'L',    "calc ",       "calculated "),
        ( ConfidenceCode.MAY,     '?'   , "maybe ",      "maybe "     ),
        ( ConfidenceCode.PER,     '1',    "perhaps ",    "perhaps "   ),
        ( ConfidenceCode.APAR,    '2',    "apparently ", "apparently "),
        ( ConfidenceCode.LKLY,    '3',    "likely ",     "likely "    ),
        ( ConfidenceCode.POSS,    '4',    "poss ",       "possibly "  ),
        ( ConfidenceCode.PROB,    '5',    "prob ",       "probably "  ),
        ( ConfidenceCode.CERT,    '6',    "cert ",       "certainly " )
        # fmt: on
    )

    def get_enum_from_symbol(self, symbol):
        for date_type in RMdate_confidence._data:
            if symbol == date_type[1]:
                return date_type[0]
        raise Exception("Malformed RM Date: Confidence character")

    def get_str(self, type, format):
        for date_type in RMdate_confidence._data:
            if type == date_type[0]:
                if format == Format.SHORT:
                    return date_type[2]
                elif format == Format.LONG:
                    return date_type[3]
                else:
                    raise Exception("Format not supported")
        raise Exception("Confidence enum not supported")


# ===================================================DIV60==
class Direction(Enum):
    FROM_RM = 1
    TO_RM = 2


# ===================================================DIV60==
class Format(Enum):
    SHORT = 1
    LONG = 2


# ===================================================DIV60==
def NumToMonthStr(MonthNum, style):
    if style != 0 and style != 1:
        raise Exception("style not supported")
    if MonthNum < 0 or MonthNum > 13:
        raise Exception("Month number out of range")

   # Items must appear in this order
    Months = (
        ('',   ''),
        ('Jan',  "January"),
        ('Feb',  "February"),
        ('Mar',  "March"),
        ('Apr',  "April"),
        ('May',  "May"),
        ('Jun',  "June"),
        ('Jul',  "July"),
        ('Aug',  "August"),
        ('Sep',  "September"),
        ('Oct',  "October"),
        ('Nov',  "November"),
        ('Dec',  "December"),
        ('???',  "??????")
    )
    return Months[MonthNum][style]


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==

from enum import Enum

## RM Internal Date structure

#   0123456789A123456789B1234
#   0               1   type
#   1               1   structure

#   2      13       1   BC-AD  -/+ year
#   3-10   14-21    8   YYYYMMDD
#   11     22       1   slash date
#   12     23       1   confidence


# all RN External human readable formats (from RM v9 prefereces)
#  10 Jan 1959
#  Jan 10, 1959
#  10 January 1950
#  January 10, 1959
#  10 JAN 1959
#  JAN 10, 1950
#  10 JANUARY 1950
#  JANUARY 10, 1950

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

    char_0_1 = RMDate[0:1]
    if char_0_1 == 'T':
        return RMDate[1:]
    elif char_0_1 == 'Q':
        raise Exception("RM Quaker dates not yet supported")
    elif char_0_1 == 'R':
        raise Exception("RM Quarter dates not yet supported")
    elif char_0_1 == '.':
        return ""
    elif char_0_1 == 'D':
        pass  # continue and process D type below
    else:
        raise Exception("Malformed RM Date: unsuported start character")

    # Process D type dates

    if len(RMDate) != 24:
        raise Exception("Malformed RM Date: wrong length")

    if RMDate[11:12] == '/' or  RMDate[22:23] == '/':
        raise Exception("Slash dates not yet supported")

    char_1_2 = RMDate[1:2]
    data_s = RMdate_structure()
    StructCodeE = data_s.get_enum_from_symbol(char_1_2)

    char_2_3 = RMDate[2:3]
    if char_2_3 == '-':
        bc_ad_1 = ' BC'
    elif char_2_3 == '+':
        bc_ad_1 = ''
    else:
        raise Exception("Malformed RM Date: bc_ad_1 indicator")
    
    try:
        year_1 = (RMDate[3:7]).lstrip("0")
        month_1_i = int(RMDate[7:9])
        day_1 = RMDate[9:11].lstrip("0")
    except ValueError as ve:
        raise Exception("Malformed RM Date: Invalid characters in date 1")
    
    char_11_12 = RMDate[11:12]
    DoubleDate_1 = False
    if char_11_12 == '/':
        DoubleDate_1 = True
    elif char_11_12 != '.':
        raise Exception("Malformed RM Date: Double Date 1 indicator")

    char_12_13 = RMDate[12:13]
    data_c = RMdate_confidence()
    ConfidenceE_1 = data_c.get_enum_from_symbol(char_12_13)

    char_13_14 = RMDate[13:14]
    if char_13_14 == '-':
        bc_ad_2 = ' BC'
    elif char_13_14 == '+':
        bc_ad_2 = ''
    else:
        raise Exception("Malformed RM Date: bc_ad_2 indicator")

    # must be all 0 if not date range Confidence
    try:
        year_2 = RMDate[14:18].lstrip("0")
        month_2_i = int(RMDate[18:20])
        day_2 = RMDate[20:22].lstrip("0")
    except ValueError as ve:
        raise Exception("Malformed RM Date: Invalid characters in date 1")

    # complicated TODO
    char_22_23 = RMDate[22:23]
    DoubleDate_2 = False
    if char_22_23 == '/':
        DoubleDate_2 = True
    elif char_22_23 != '.':
        raise Exception("Malformed RM Date: Double Date 2 indicator")

    # only if 2nd date
    char_23_24 = RMDate[23:24]
    ConfidenceE_2 = data_c.get_enum_from_symbol(char_23_24)

    single_date = False
    if year_2 == '' and month_2_i == 0 and day_2 == '' and bc_ad_2 == '':
        single_date = True

    if single_date and data_s.get_num_from_enum(StructCodeE) != 1:
        raise Exception(
            "Malformed date: conflict between struct code & second date empty")

    month_trsp_1 = ''  # month's trailing space
    if year_1 != '' and day_1 != '' and month_1_i == 0:
        month_1_i = 13
    if day_1 != '':
        day_1 = day_1 + ' '
    if year_1 == '' or (year_1 != '' and month_1_i == 0):
        month_trsp_1 = ''
    else:
        month_trsp_1 = ' '

    fDate_1 = (data_s.get_str_1(StructCodeE, form) + data_c.get_str(ConfidenceE_1, form)
                + day_1 + NumToMonthStr(month_1_i, form) + month_trsp_1 + year_1 + bc_ad_1)
    
    month_trsp_2 = ''
    fDate = ''
    if single_date:
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
             + day_2 + NumToMonthStr(month_2_i, form) + month_trsp_2 + year_2 + bc_ad_2)
        fDate = fDate_1 + fDate_2

    return fDate


# ===================================================DIV60==
def to_RMsort_date(RM_date):
    # RM_date is an RM internal date string

    date_type = RM_date[0:1]
    if date_type == 'T':
        #  9223372036854775807    ( 2^63,  sign bit is 0, largest possible signed 64 bit int)
        return 0x7F_FF_FF_FF_FF_FF_FF_FF 
    elif date_type == 'Q':
        raise Exception("RM Quaker dates not yet supported")
    elif date_type == 'R':
        raise Exception("RM Quarter dates not yet supported")
    elif date_type == '.':
        #  9223372036854775807    ( 2^63,  sign bit is 0, largest possible signed 64 bit int)
        return 0x7F_FF_FF_FF_FF_FF_FF_FF 
    elif date_type == 'D':
        pass  # continue and process D type below
    else:
        raise Exception("Malformed RM Date: unsuported Type character")

    # Process D type dates

    # Julian date / slash date
    date_type_slash_1 = False
    date_type_slash_2 = False
    if  RM_date[11:12]== '/':
        date_type_slash_1 == True
        raise Exception("Slash dates not yet supported")
    if  RM_date[22:23]== '/':
        date_type_slash_1 == True
        raise Exception("Slash dates not yet supported")
    
    try:
        # include +/- sign in year
        year_1 = int(RM_date[2:7])
        month_1 = int(RM_date[7:9])
        day_1 = int(RM_date[9:11])
    except ValueError as ve:
        raise Exception("Malformed RM Date: Invalid characters in date part 1")

    try:
        # include +/- sign in year
        year_2 = int(RM_date[13:18])
        month_2 = int(RM_date[18:20])
        day_2 = int(RM_date[20:22])
    except ValueError as ve:
        raise Exception("Malformed RM Date: Invalid characters in date part 2")

    Char_1_2 = RM_date[1:2]
    struct_data = RMdate_structure()
    offset = struct_data.get_offset_from_symbol(Char_1_2)

    if year_1 == 0 and ((month_1 != 0) or (day_1 != 0)):
        # year 1 is 0 but month or day or both present
        y1 =  0x3F_FF << 49  # a date with no year  16383<<49 = 9,222,809,086,901,354,496
    else:
        # Slash date is in Julian and increments year by 1
        y1 = ((year_1 + 10000 + (1 if date_type_slash_1 else 0)) << 49)

    # np correction for slash date in part 2 of date ?  TODO test case
    if year_2 == 0 and month_2 == 0 and day_2 == 0:
        y2 = 0x03_FF_F0_00_00        # (2^34 - 2^20)  17178820608
    else:
        y2 = (year_2 + 10000) << 20

    return (y1 + (month_1 << 45) + (day_1 << 39)
              + y2 + (month_2 << 16) + (day_2 << 10) + offset)


# ===================================================DIV60==
def from_RMsort_date(sort_date):

    # cannot produce
    # BC dates
    # confidence indicators
    # slash dates

    RM_sort_date = int(sort_date)

    Y1 = (RM_sort_date >> 49) - 10000
    M1 = (RM_sort_date >> 45) & 0xF
    D1 = (RM_sort_date >> 39) & 0x3F
    Y2 = ((RM_sort_date >> 20) & 0x3F_FF)  - 10000   #-6383
    M2 = (RM_sort_date >> 16) & 0xF
    D2 = (RM_sort_date >> 10) & 0x3F
    F = RM_sort_date & 0x3F_FF

    if Y1 > 0:
        ADBC1 = '+'
    else:
        ADBC1 = '-'
        Y1 = -Y1

    if Y2 > 0:
        ADBC2 = '+'
    else:
        ADBC2 = '-'
        Y2 = -Y2

    data_s = RMdate_structure()
    FF = data_s.get_symbol_from_offset(F)

    RM_date = ( "D" + FF + ADBC1 + "{:=04}{:=02}{:=02}".format(Y1, M1, D1) + ".."
                         + ADBC2 + "{:=04}{:=02}{:=02}".format(Y2, M2, D2) + ".." )

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
        #          0          1      2          3    4         5           6        7
        #          enum       sym    offset     num  1stShort  1stLong     2ndShort 2ndLong
        ( StructCode.NORM,    '.',   12,        1,   '',       '',         '',      ''     ),
#        ( StructCode.AFT,     'A',   31,        1,   'aft ',   'after ',   '',      ''     ),
        ( StructCode.AFT,     'A',   1047583,   1,   'aft ',   'after ',   '',      ''     ),
        ( StructCode.BEF,     'B',   0,         1,   'bef ',   'before ',  '',      ''     ),
#        ( StructCode.FROM,    'F',   27,        1,   'from ',  'from ',    '',      ''     ),
        ( StructCode.FROM,    'F',   1047579,   1,   'from ',  'from ',    '',      ''     ),
#        ( StructCode.SINC,    'I',   30,        1,   'since ', 'since ',   '',      ''     ),
        ( StructCode.SINC,    'I',   1047582,   1,   'since ', 'since ',   '',      ''     ),
        ( StructCode.TO,      'T',   6,         1,   'to ',    'to ',      '',      ''     ),
        ( StructCode.UNTL,    'U',   9,         1,   'until ', 'until ',   '',      ''     ),
        ( StructCode.BY,      'Y',   3,         1,   'by ',    'by ',      '',      ''     ),
        ( StructCode.OR,      'O',   24,        2,   '',       '',         ' or ',  ' or ' ),
        ( StructCode.BTWN,    'R',   15,        2,   'bet ',   'between ', ' and ', ' and '),
        ( StructCode.FRTO,    'S',   18,        2,   'from ',  'from ',    ' to ',  ' to ' ),
        ( StructCode.DASH,    '-',   21,        2,   '',       '',         '–',     '–'    )
        # fmt: on
    )

# Sort order  TODO
# F FROM  = 1047579 = (27 + xFFC00)
# I SINCE = 1047582 = (30 + xFFC00)
# A AFTER = 1047583 = (31 + xFFC00)


    def get_num_from_enum(self, enum):
        for date_type in RMdate_structure._data:
            if enum == date_type[0]:
                return date_type[3]
        raise Exception(
            "Malformed RM Date: unsuported StructCode: " + str(enum))

    def get_enum_from_symbol(self, symbol):
        for date_type in RMdate_structure._data:
            if symbol == date_type[1]:
                return date_type[0]
        raise Exception(
            "Malformed RM Date: unsuported symbol: " + symbol)

    def get_offset_from_symbol(self, symbol):
        for date_type in RMdate_structure._data:
            if symbol == date_type[1]:
                return date_type[2]
        raise Exception(
            "Malformed RM Date: unsuported character: " + symbol)

    def get_symbol_from_offset(self, offset):
        for date_type in RMdate_structure._data:
            if offset == date_type[2]:
                return date_type[1]
        raise Exception(
            "Malformed RM Date: unsuported offset: " + offset)

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
    if MonthNum < 0 or MonthNum > 13:
        raise Exception("Month number out of range")
    if style == Format.LONG:
        index=1
    elif style == Format.SHORT:
        index=0
    else:
        raise Exception("style not supported")

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
        ('???',  "???")
    )
    return Months[MonthNum][index]

# ===================================================DIV60==

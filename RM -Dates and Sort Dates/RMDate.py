from enum import Enum


# ===================================================DIV60==
def ToRMDate(DateStr, form):
  #form is Format.LONG, Format.SHORT

  raise Exception( "ToRMDate not yet implemented")

  return ""

# ===================================================DIV60==
def FromRMDate(RMDate, form):
  #form is Format.LONG, Format.SHORT

  if RMDate[0:1] == 'T':
    return RMDate[1:]
  elif RMDate[0:1] == 'Q':
    raise Exception( "RM Quaker dates not yet supported")
  elif RMDate[0:1] == '.':
    return ""
  elif RMDate[0:1] == 'D':
    pass
  else:
    raise Exception( "Malformed RM Date: wrong start character")

  # Handle D type Dates
  if len(RMDate)  != 24:
    raise Exception( "Malformed RM Date: wrong length")

  Char_1_2 = RMDate[1:2]
  StructCodeE = None
  if   Char_1_2 == '.': StructCodeE = StructCode.NORM
  elif Char_1_2 == 'A': StructCodeE = StructCode.AFT
  elif Char_1_2 == 'B': StructCodeE = StructCode.BEF
  elif Char_1_2 == 'F': StructCodeE = StructCode.FROM
  elif Char_1_2 == 'I': StructCodeE = StructCode.SINC
  elif Char_1_2 == 'T': StructCodeE = StructCode.TO
  elif Char_1_2 == 'U': StructCodeE = StructCode.UNTL
  elif Char_1_2 == 'Y': StructCodeE = StructCode.BY
  elif Char_1_2 == 'O': StructCodeE = StructCode.OR
  elif Char_1_2 == 'R': StructCodeE = StructCode.BTWN
  elif Char_1_2 == 'S': StructCodeE = StructCode.FRTO
  elif Char_1_2 == '-': StructCodeE = StructCode.DASH
  else: raise Exception( "Malformed RM Date: StructCode character")

  Char_2_3 = RMDate[2:3]
  if   Char_2_3 == '-': AdBc_1 = ' BC'
  elif Char_2_3 == '+': AdBc_1 = ''
  else: raise Exception( "Malformed RM Date: AD-BC_1 indicator")

  try:
    year_1    = (RMDate[3:7]).lstrip("0")
    month_1_i = int(RMDate[7:9])
    day_1     = RMDate[9:11].lstrip("0")
  except ValueError as ve:
   raise Exception( "Malformed RM Date: Invalid characters in date 1")

  Char_11_12 = RMDate[11:12]
  DoubDate_1 = False
  if   Char_11_12 == '/': DoubDate_1 = True
  elif Char_11_12 != '.': raise Exception( "Malformed RM Date: Double Date 1 indicator")
  
  Char_12_13 = RMDate[12:13]
  ConfidenceE_1 = None
  if   Char_12_13 == '.': ConfidenceE_1 = ConfidenceCode.NONE
  elif Char_12_13 == 'A': ConfidenceE_1 = ConfidenceCode.ABT
  elif Char_12_13 == 'S': ConfidenceE_1 = ConfidenceCode.SAY
  elif Char_12_13 == 'C': ConfidenceE_1 = ConfidenceCode.CIR
  elif Char_12_13 == 'E': ConfidenceE_1 = ConfidenceCode.EST
  elif Char_12_13 == 'L': ConfidenceE_1 = ConfidenceCode.CAL
  elif Char_12_13 == '?': ConfidenceE_1 = ConfidenceCode.MAY
  elif Char_12_13 == '1': ConfidenceE_1 = ConfidenceCode.PER
  elif Char_12_13 == '2': ConfidenceE_1 = ConfidenceCode.APAR
  elif Char_12_13 == '3': ConfidenceE_1 = ConfidenceCode.LKLY
  elif Char_12_13 == '4': ConfidenceE_1 = ConfidenceCode.POSS
  elif Char_12_13 == '5': ConfidenceE_1 = ConfidenceCode.PROB
  elif Char_12_13 == '6': ConfidenceE_1 = ConfidenceCode.CERT
  else: raise Exception( "Malformed RM Date: Confidence 1")
  
  Char_13_14 = RMDate[13:14]
  if   Char_13_14 == '-': AdBc_2 = ' BC'
  elif Char_13_14 == '+': AdBc_2 = ''
  else: raise Exception( "Malformed RM Date: AD-BC_2 indicator")
  
  # must be all 0 if not date range Confidence
  try:
    year_2    = RMDate[14:18].lstrip("0")
    month_2_i = int(RMDate[18:20])
    day_2     = RMDate[20:22].lstrip("0")
  except ValueError as ve:
   raise Exception( "Malformed RM Date: Invalid characters in date 1")
  
   # complicated TODO
  Char_22_23 = RMDate[22:23]
  DoubDate_2 = False
  if   Char_22_23 == '/': DoubDate_2 = True
  elif Char_22_23 != '.': raise Exception( "Malformed RM Date: Double Date 2 indicator")

  # only if 2nd date
  Char_23_24 = RMDate[23:24]
  ConfidenceE_2 = None
  if   Char_23_24 == '.': ConfidenceE_2 = ConfidenceCode.NONE
  elif Char_23_24 == 'A': ConfidenceE_2 = ConfidenceCode.ABT
  elif Char_23_24 == 'S': ConfidenceE_2 = ConfidenceCode.SAY
  elif Char_23_24 == 'C': ConfidenceE_2 = ConfidenceCode.CIR
  elif Char_23_24 == 'E': ConfidenceE_2 = ConfidenceCode.EST
  elif Char_23_24 == 'L': ConfidenceE_2 = ConfidenceCode.CAL
  elif Char_23_24 == '?': ConfidenceE_2 = ConfidenceCode.MAY
  elif Char_23_24 == '1': ConfidenceE_2 = ConfidenceCode.PER
  elif Char_23_24 == '2': ConfidenceE_2 = ConfidenceCode.APAR
  elif Char_23_24 == '3': ConfidenceE_2 = ConfidenceCode.LKLY
  elif Char_23_24 == '4': ConfidenceE_2 = ConfidenceCode.POSS
  elif Char_23_24 == '5': ConfidenceE_2 = ConfidenceCode.PROB
  elif Char_23_24 == '6': ConfidenceE_2 = ConfidenceCode.CERT
  else: raise Exception( "Malformed RM Date: Confidence 1")

  # Format the date
  ConfidenceData = {}
  #                                       short          long
  ConfidenceData[ConfidenceCode.NONE] = ( "",            "")
  ConfidenceData[ConfidenceCode.ABT ] = ( "abt ",        "about ")
  ConfidenceData[ConfidenceCode.SAY ] = ( "say ",        "say ")
  ConfidenceData[ConfidenceCode.CIR ] = ( "ca ",         "circa ")
  ConfidenceData[ConfidenceCode.EST ] = ( "est ",        "estimated ")
  ConfidenceData[ConfidenceCode.CAL ] = ( "calc ",       "calculated ")
  ConfidenceData[ConfidenceCode.MAY ] = ( "maybe ",      "maybe ")
  ConfidenceData[ConfidenceCode.PER ] = ( "perhaps ",    "perhaps ")
  ConfidenceData[ConfidenceCode.APAR] = ( "apparently ", "apparently ")
  ConfidenceData[ConfidenceCode.LKLY] = ( "likely ",     "likely ")
  ConfidenceData[ConfidenceCode.POSS] = ( "poss ",       "possibly ")
  ConfidenceData[ConfidenceCode.PROB] = ( "prob ",       "probably ")
  ConfidenceData[ConfidenceCode.CERT] = ( "cert ",       "certainly ")

  FormatData = { }
  #                                    num     1stShort      1stLong       2ndShort      2ndLong 
  FormatData[StructCode.NORM] =   (   1,      '',           '',            '',          ''     )
  FormatData[StructCode.AFT]  =   (   1,      'aft ',       'after ',      '',          ''     )
  FormatData[StructCode.BEF]  =   (   1,      'bef ',       'before ',     '',          ''     )
  FormatData[StructCode.FROM] =   (   1,      'from ',      'from ',       '',          ''     )
  FormatData[StructCode.SINC] =   (   1,      'since ',     'since ',      '',          ''     )
  FormatData[StructCode.TO]   =   (   1,      'to ',        'to ',         '',          ''     )
  FormatData[StructCode.UNTL] =   (   1,      'until ',     'until ',      '',          ''     )
  FormatData[StructCode.BY]   =   (   1,      'by ',        'by ',         '',          ''     )
  FormatData[StructCode.OR]   =   (   2,      '',           '',            ' or ',      ' or ' )
  FormatData[StructCode.BTWN] =   (   2,      'bet ',       'between ',    ' and ',     ' and ')
  FormatData[StructCode.FRTO] =   (   2,      'from ',      'from ',       ' to ',      ' to ' )
  FormatData[StructCode.DASH] =   (   2,      '',           '',            '–',         '–'   )

  SingleDate = False
  if year_2 == '' and month_2_i == 0 and day_2 == '' and AdBc_2 == '': SingleDate = True

  if SingleDate and FormatData[StructCodeE][0] == 2 :
    raise Exception("Malformed date: conflict between struct code & second date empty")

  if year_1 != '' and day_1 != '' and month_1_i == 0: month_1_i = 13
  if day_1 != '':
    day_1 = day_1 + ' '
  if year_1 == '' or (year_1 != '' and month_1_i == 0):
    month_trsp_1 = ''
  else: month_trsp_1 = ' '


  if form ==Format.SHORT :
    fDate_1 = (FormatData[StructCodeE][1] + ConfidenceData[ConfidenceE_1][0] 
             + day_1 + NumToMonthStr(month_1_i, 0) + month_trsp_1 + year_1 + AdBc_1)

  elif form ==Format.LONG :
    fDate_1 = (FormatData[StructCodeE][2] + ConfidenceData[ConfidenceE_1][1] 
             + day_1 + NumToMonthStr(month_1_i, 1) + month_trsp_1 + year_1 + AdBc_1)

  else: raise Exception( "Format not supported")


  fDate = ''
  if SingleDate:
    fDate = fDate_1
  else:
    if year_2 != '' and day_2 != '' and month_2_i == 0: month_2_i = 13
    if day_2 != '': 
      day_2 = day_2 + ' '
    if year_2 == '' or (year_2 != '' and month_2_i == 0):
      month_trsp_2 = ''
    else: month_trsp_2 = ' '

    if form ==Format.SHORT :
      fDate_2= (FormatData[StructCodeE][3] + ConfidenceData[ConfidenceE_2][0] 
               + day_2 + NumToMonthStr(month_2_i, 0) + month_trsp_2 + year_2 + AdBc_2)
  
    elif form ==Format.LONG :
      fDate_2 = (FormatData[StructCodeE][4] + ConfidenceData[ConfidenceE_2][1] 
               + day_2 + NumToMonthStr(month_2_i, 1) + month_trsp_2 + year_2 + AdBc_2)
  
    else: raise Exception( "Format not supported")

    fDate = fDate_1 + fDate_2

  return fDate


# ===================================================DIV60==
class Direction(Enum):
  FROM_RM = 1
  TO_RM = 2


# ===================================================DIV60==
class Format(Enum):
  SHORT = 1
  LONG  = 2


# ===================================================DIV60==
class StructCode(Enum):
  NORM = 1
  AFT  = 2
  BEF  = 3
  FROM = 4
  SINC = 5
  TO   = 6
  UNTL = 7
  BY   = 8
  OR   = 9
  BTWN = 10
  FRTO = 11
  DASH = 12


# ===================================================DIV60==
class ConfidenceCode(Enum):
  NONE = 1
  ABT  = 2 
  SAY  = 3
  CIR  = 4
  EST  = 5
  CAL  = 6
  MAY  = 7
  PER  = 8
  APAR = 9
  LKLY = 10
  POSS = 11
  PROB = 12
  CERT = 13


# ===================================================DIV60==
def NumToMonthStr(MonthNum, style):
  if style != 0 and style != 1: raise Exception ("style not supported")
  if MonthNum < 0 or MonthNum > 13: raise Exception ("Month number out of range")

 # Items must appear in this order
  Months = (
  (    '',   ''),
  ( 'Jan',  "January" ),
  ( 'Feb',  "February" ),
  ( 'Mar',  "March" ),
  ( 'Apr',  "April" ),
  ( 'May',  "May" ),
  ( 'Jun',  "June" ),
  ( 'Jul',  "July" ),
  ( 'Aug',  "August" ),
  ( 'Sep',  "September" ),
  ( 'Oct',  "October" ),
  ( 'Nov',  "November" ),
  ( 'Dec',  "December" ),
  ( '???',  "??????" )
  )
  return Months[ MonthNum ] [ style ]


# ===================================================DIV60==

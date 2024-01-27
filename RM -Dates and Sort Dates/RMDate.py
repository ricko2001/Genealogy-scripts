
from enum import Enum

# ===================================================DIV60==
def main():

    print ("===========================================DIV50==\n")

    Test("D-+19210113..+99990000..", "13 Jan 1921-9999", Direction.FROM_RM )
    Test("D.-10000000..+00000000..", "1000 BC   [BC dates, for my Neanderthal cousins]", Direction.FROM_RM )
    Test("D.+00050000..+00000000..", "5  [date & sort date=5]", Direction.FROM_RM )
    Test(".", "date is blank [sort date=10]", Direction.FROM_RM )
    Test(".", "date is blank [sort date=11]", Direction.FROM_RM )
    Test("D.+00300000..+00000000..", "30   [ date & sort date=30]", Direction.FROM_RM )
    Test("D.+03000000..+00000000..", "300     [date & sort date=300] number, too big for day of month", Direction.FROM_RM )
    Test("D.+15830101/.+00000000..", "1 Jan 1583/84 [double date]", Direction.FROM_RM )
    Test("Q.+15880212..+00000000..", "12da 2mo 1588   [quaker date format, neeeds further investigation]", Direction.FROM_RM )
    Test("QR+15881112..+15881201..", "Bet 12da 11mo 1588 and 1da 12mo 1588 [quaker date format, not investigated] ", Direction.FROM_RM )
    Test("Q.+15881112..+00000000..", "12da 11mo 1588  [quaker date]", Direction.FROM_RM )
    Test("Q.+15880102/.+00000000..", "2da 1mo 1588/9   [quaker double-date]", Direction.FROM_RM )
    Test("Q.+15881102/.+00000000..", "2da 11mo 1588/9  [quaker double-date]", Direction.FROM_RM )
    Test("Q.+17511031..+00000000..", "31da 10mo 1751 [quaker date pre-1752]", Direction.FROM_RM )
    Test("Q.+17520101..+00000000..", "1da 1mo 1752  [quaker date post-1751]", Direction.FROM_RM )
    Test("D-+19210000..+00010000..", "1921-1   [ sort date=1921-1 ]", Direction.FROM_RM )
    Test("D-+19210000..+00020000..", "1921-2  [ sort date=1921-2 ]", Direction.FROM_RM )
    Test("D-+19210000..+00030000..", "1921-3   [ sort date=1921-3 ]", Direction.FROM_RM )
    Test("D-+19210000..+00100000..", "1921-10  [sort date=1921-10 ]", Direction.FROM_RM )
    Test("D.+19210000..+00000000..", "1921   [std date- year only]", Direction.FROM_RM )
    Test("D-+19210000..+99990000..", "1921–9999  [sort date=1921–9999]", Direction.FROM_RM )
    Test("D.+19210013..+00000000..", "13 ??? 1921", Direction.FROM_RM )
    Test("D.+19210100..+00000000..", "Jan 1921", Direction.FROM_RM )
    Test("D.+19210113..+00000000..", "13 Jan 1921  ( sort date 13 Jan 1921-1 )", Direction.FROM_RM )
    Test("D-+19210113.E+00010000..", "Est 13 Jan 1921-1    [prefix ignored in sort date]", Direction.FROM_RM )
    Test("D-+19210113.A+00010000..", "Abt 13 Jan 1921-1    [prefix ignored in sort date]", Direction.FROM_RM )
    Test("D-+19210113.S+00010000..", "Say 13 Jan 1921-1  [prefix ignored in sort date]", Direction.FROM_RM )
    Test("D-+19210113.L+00010000..", "Calc 13 Jan 1921–1 [prefix ignored in sort date]", Direction.FROM_RM )
    Test("D-+19210113.C+00010000..", "Ca 13 Jan 1921–1 [prefix ignored in sort date]", Direction.FROM_RM )
    Test("D-+19210113..+00010000..", "13 Jan 1921–10000  [N=10000 changed to 1 in both dates]", Direction.FROM_RM )
    Test("D.+19210113..+00000000..", "13 Jan 1921  ( sort date 13 Jan 1921-2 )", Direction.FROM_RM )
    Test("D.+19210113..+00000000..", "13 Jan 1921  ( sort date 13 Jan 1921-10 )", Direction.FROM_RM )
    Test("D-+19210113..+10000000..", "13 Jan 1921–1000", Direction.FROM_RM )
    Test("DR+19210113..+19220125..", "Bet 13 Jan 1921 and 25 Jan 1922", Direction.FROM_RM )
    Test("DS+19210113..+19220125..", "From 13 Jan 1921 to 25 Jan 1922", Direction.FROM_RM )
    Test("D-+19210113..+19220125..", "13 Jan 1921-25 Jan 1922", Direction.FROM_RM )
    Test("DO+19210113..+19220125..", "13 Jan 1921 or 25 Jan 1922", Direction.FROM_RM )
    Test("DO+19210113..+19250125..", "13 Jan 1921 or 25 Jan 1925", Direction.FROM_RM )
    Test("D-+19210113..+49990000..", "13 Jan 1921–4999   [largest N]", Direction.FROM_RM )
    Test("D-+19210113..+50000000..", "13 Jan 1921–5000   [N too big, ignored in sort date]", Direction.FROM_RM )
    Test("DB+19210113..+00000000..", "Bef 13 Jan 1921", Direction.FROM_RM )
    Test("DY+19210113..+00000000..", "By 13 Jan 1921", Direction.FROM_RM )
    Test("DT+19210113..+00000000..", "To 13 Jan 1921", Direction.FROM_RM )
    Test("DU+19210113..+00000000..", "Until 13 Jan 1921", Direction.FROM_RM )
    Test("DU+19210113..+00000000..", "Until 13 Jan 1921-1", Direction.FROM_RM )
    Test("D.+19210113..+00000000..", "13 Jan 1921", Direction.FROM_RM )
    Test("D.+19210113.A+00000000..", "Abt 13 Jan ", Direction.FROM_RM )
    Test("D.+19210113.E+00000000..", "Est 13 Jan 1921   [prefix ignored in sort date]", Direction.FROM_RM )
    Test("D.+19210113.L+00000000..", "Calc 13 Jan 1921   [prefix ignored in sort date]", Direction.FROM_RM )
    Test("D.+19210113.C+00000000..", "Ca 13 Jan 1921     [prefix ignored in sort date]", Direction.FROM_RM )
    Test("D.+19210113.S+00000000..", "Say 13 Jan 1921   [prefix ignored in sort date]", Direction.FROM_RM )
    Test("DF+19210113..+00000000..", "From 13 Jan 1921", Direction.FROM_RM )
    Test("DI+19210113..+00000000..", "Since 13 Jan 1921", Direction.FROM_RM )
    Test("DA+19210113..+00000000..", "Aft 13 Jan 1921", Direction.FROM_RM )
    Test("D-+19210113..+90000000..", "13 Jan 1921–9000", Direction.FROM_RM )
    Test("D.+19210114..+00000000..", "14 Jan 1921", Direction.FROM_RM )
    Test("D-+19230000..+19240000..", "1923-1924", Direction.FROM_RM )
    Test("D.+20000000.A+00000000..", "about 2000", Direction.FROM_RM )
    Test("D.+20000000.S+00000000..", "say 2000", Direction.FROM_RM )
    Test("D.+20000000.C+00000000..", "circa 2000", Direction.FROM_RM )
    Test("D.+20000000.E+00000000..", "estimated 2000", Direction.FROM_RM )
    Test("D.+20000000.L+00000000..", "calculated 2000", Direction.FROM_RM )
    Test("D.+20000000.?+00000000..", "maybe 2000", Direction.FROM_RM )
    Test("D.+20000000.1+00000000..", "perhaps 2000", Direction.FROM_RM )
    Test("D.+20000000.2+00000000..", "apparently 2000", Direction.FROM_RM )
    Test("D.+20000000.3+00000000..", "likely 2000", Direction.FROM_RM )
    Test("D.+20000000.4+00000000..", "possibly 2000", Direction.FROM_RM )
    Test("D.+20000000.5+00000000..", "probably 2000", Direction.FROM_RM )
    Test("D.+20000000.6+00000000..", "certainly 2000", Direction.FROM_RM )
    Test("DB+21000000..+00000000..", "before 2100", Direction.FROM_RM )
    Test("DY+21000000..+00000000..", "by 2100", Direction.FROM_RM )
    Test("DT+21000000..+00000000..", "to 2100", Direction.FROM_RM )
    Test("DU+21000000..+00000000..", "until 2100", Direction.FROM_RM )
    Test("DF+21000000..+00000000..", "from 2100", Direction.FROM_RM )
    Test("DI+21000000..+00000000..", "since 2100", Direction.FROM_RM )
    Test("DA+21000000..+00000000..", "after 2100", Direction.FROM_RM )
    Test("DR+22000000..+23000000..", "between 2200 and 2300", Direction.FROM_RM )
    Test("DS+22000000..+23000000..", "from 2200 to 2300", Direction.FROM_RM )
    Test("D-+22000000..+23000000..", "2200–2300", Direction.FROM_RM )
    Test("DO+22000000..+23000000..", "2200–2300", Direction.FROM_RM )
    Test("D.+00000100..+00000000..", "Jan   [std date - month only]", Direction.FROM_RM )
    Test("D-+00000100..+00000300..", "Jan-Mar   [month range, no year]", Direction.FROM_RM )
    Test("D.+00000113..+00000000..", "13 Jan   [no year]", Direction.FROM_RM )
    Test("D.+00000300..+00000000..", "Mar  [month only]", Direction.FROM_RM )
    Test(".", "blank date", Direction.FROM_RM )
    Test("TText date", "Text date", Direction.FROM_RM )
    Test("T1 January 1583/1 apr 4", "TEXT DATE because double date does lots of validation", Direction.FROM_RM )

    Test("TThis is a text date", "Normal text date", Direction.FROM_RM )
    Test("TLast Monday", "Normal text date", Direction.FROM_RM )
    Test(".", "Empty date", Direction.FROM_RM )

    Test("P.+19690000.A+00000000..", "malformed: initial char", Direction.FROM_RM )
    Test("Q.+19690000.A+00000000..", "Quaker dates not supported", Direction.FROM_RM )


  #  Test("Say 1960",   Direction.TO_RM )
  #  Test("About 1970", Direction.TO_RM )
  #  Test("5 Jan 1945", Direction.TO_RM )


    PauseWithMessage()
    return

# ===================================================DIV60==
def ToRMDate(DateStr):

  raise Exception( "ToRMDate not yet implemented")

  return RMDate

# ===================================================DIV60==
def FromRMDate(RMDate):

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

  # Handle D Dates
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
    Year_1  = (RMDate[3:7]).lstrip("0")
    Year_1  = Year_1.lstrip("0")
    Month_1 = RMDate[7:9]
    Month_1_i = int(Month_1)
    if Month_1_i == 0: Month_1 = ''
    if Month_1_i < 0 or Month_1_i >12 :raise Exception( "Invalid month 1 number")
    Day_1   = RMDate[9:11] + ' '
    Day_1_i = int(Day_1)
    if Day_1_i == 0: Day_1 = ''
    if Day_1_i < 0 or Day_1_i >31 : raise Exception( "Invalid day 1 number")
  except ValueError as ve:
   raise Exception( "Invalid characters in YYYY MM DD of date 1")


  Char_11_12 = RMDate[11:12]
  DoubDate_1 = False
  if   Char_11_12 == '/': DoubDate_1 = True
  elif Char_11_12 != '.': raise Exception( "Malformed RM Date: Double Date 1 indicator")
  
  Char_12_13 = RMDate[12:13]
  Confidence_1 = None
  if   Char_12_13 == '.': Confidence_1 = ConfidenceCode.NONE
  elif Char_12_13 == 'A': Confidence_1 = ConfidenceCode.ABT
  elif Char_12_13 == 'S': Confidence_1 = ConfidenceCode.SAY
  elif Char_12_13 == 'C': Confidence_1 = ConfidenceCode.CIR
  elif Char_12_13 == 'E': Confidence_1 = ConfidenceCode.EST
  elif Char_12_13 == 'L': Confidence_1 = ConfidenceCode.CAL
  elif Char_12_13 == '?': Confidence_1 = ConfidenceCode.MAY
  elif Char_12_13 == '1': Confidence_1 = ConfidenceCode.PER
  elif Char_12_13 == '2': Confidence_1 = ConfidenceCode.APAR
  elif Char_12_13 == '3': Confidence_1 = ConfidenceCode.LKLY
  elif Char_12_13 == '4': Confidence_1 = ConfidenceCode.POSS
  elif Char_12_13 == '5': Confidence_1 = ConfidenceCode.PROB
  elif Char_12_13 == '6': Confidence_1 = ConfidenceCode.CERT
  else: raise Exception( "Malformed RM Date: Confidence 1")
  
  Char_13_14 = RMDate[13:14]
  if   Char_13_14 == '-': AdBc_2 = ' BC'
  elif Char_13_14 == '+': AdBc_2 = ''
  else: raise Exception( "Malformed RM Date: AD-BC_2 indicator")
  
  # must be all 0 if not date range Confidence
  try:
    Year_2  = RMDate[14:18].lstrip("0")
    Year_2  = Year_2.lstrip("0")
    Month_2 = RMDate[18:20]
    Month_2_i = int(Month_2)
    if Month_2_i == 0: Month_2 = ''
    if Month_2_i < 0 or Month_2_i >12 :raise Exception( "Invalid month 2 number")
    Day_2   = RMDate[20:22] + ' '
    Day_2_i = int(Day_2)
    if Day_2_i == 0: Day_2 = ''
    if Day_2_i < 0 or Day_2_i >31 : raise Exception( "Invalid day 2 number")
  
  except ValueError as ve:
   raise Exception( "Invalid characters in YYYY MM DD of date 2")
  
   # complicated
  Char_22_23 = RMDate[22:23]
  DoubDate_2 = False
  if   Char_22_23 == '/': DoubDate_2 = True
  elif Char_22_23 != '.': raise Exception( "Malformed RM Date: Double Date 2 indicator")

  # only if 2nd date
  Char_23_24 = RMDate[23:24]
  Confidence_2 = None
  if   Char_23_24 == '.': Confidence_2 = ConfidenceCode.NONE
  elif Char_23_24 == 'A': Confidence_2 = ConfidenceCode.ABT
  elif Char_23_24 == 'S': Confidence_2 = ConfidenceCode.SAY
  elif Char_23_24 == 'C': Confidence_2 = ConfidenceCode.CIR
  elif Char_23_24 == 'E': Confidence_2 = ConfidenceCode.EST
  elif Char_23_24 == 'L': Confidence_2 = ConfidenceCode.CAL
  elif Char_23_24 == '?': Confidence_2 = ConfidenceCode.MAY
  elif Char_23_24 == '1': Confidence_2 = ConfidenceCode.PER
  elif Char_23_24 == '2': Confidence_2 = ConfidenceCode.APAR
  elif Char_23_24 == '3': Confidence_2 = ConfidenceCode.LKLY
  elif Char_23_24 == '4': Confidence_2 = ConfidenceCode.POSS
  elif Char_23_24 == '5': Confidence_2 = ConfidenceCode.PROB
  elif Char_23_24 == '6': Confidence_2 = ConfidenceCode.CERT
  else: raise Exception( "Malformed RM Date: Confidence 1")


#  debug print
#  print (  "StructCode: " + StructCodeE.name
#         + "\nAdBc_1: " + AdBc_1
#         + "\nYear_1: " + Year_1 
#         + "\nMonth_1: " + Month_1 
#         + "\nMonth_1_i: " + str(Month_1_i)
#         + "\nDay_1: " + Day_1
#         + "\nstr(DoubDate_1): " + str(DoubDate_1)
#         + "\nConfidence_1: " + Confidence_1.name
#         + "\nAdBc_2: " + AdBc_2
#         + "\nYear_2: " + Year_2
#         + "\nMonth_2: " + Month_2
#         + "\nMonth_2_i: " + str(Month_2_i)
#         + "\nDay_2: " + Day_2
#         + "\nstr(DoubDate_2): " + str(DoubDate_2)
#         + "\nConfidence_2: " + Confidence_2.name
#         + "\n" )

  # Format the date

  ConfidenceData = {}
  #                                      short    long
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
  FormatData[StructCode.DASH] =   (   2,      '',           '',           ' – ',       ' – '   )

  SingleDate = False
  if (Year_2 == '') and (Month_2_i == 0) and (Day_2_i == 0): SingleDate = True

  StructCodeNum=1
  if (StructCodeE == StructCode.OR or StructCodeE == StructCode.BTWN
                    or StructCodeE == StructCode.FRTO or StructCodeE == StructCode.DASH ): StructCodeNum=2

  if SingleDate and StructCodeNum == 2 :
    raise Exception("Malformed date: conflict between struct code & # dates")

#  if Year_1 != '' and Month_1_i == 0: 
#    Month_1_i = 13

  fDate_1 = (FormatData[StructCodeE][1] + ConfidenceData[Confidence_1][0] 
             + Day_1 + NumToMonthStr(Month_1_i, 1)  + Year_1 + AdBc_1)



  fDate = ''
  if SingleDate:
    fDate = fDate_1
  else:
    #if Year_2 != '   ' and Month_2_i == 0: Month_2_i = 13
    fDate_2 =  (FormatData[StructCodeE][3] + ConfidenceData[Confidence_2][0] 
                + Day_2 + NumToMonthStr(Month_2_i, 1) + Year_2 + AdBc_2)
    fDate = fDate_1 + fDate_2


  return fDate


# if date has no month, need a place holder for month if day is 1-12   =  use ??? 

# ===================================================DIV60==
def Test(In, Expected, whichWay):
  try:
    print( In , "     : " + Expected )

    if whichWay == Direction.TO_RM:
      print ( ToRMDate(In) )
  
    elif whichWay == Direction.FROM_RM:
      print ( FromRMDate(In) )

  except Exception as e:
    print (e)

  print("\n")

# ===================================================DIV60==
#def Test(In, Expected, whichWay):
#    print( In , "     : " + Expected )
#
#    if whichWay == Direction.TO_RM:
#      print ( ToRMDate(In) )
#  
#    elif whichWay == Direction.FROM_RM:
#      print ( FromRMDate(In) )
#
#
#    print("\n")

# ===================================================DIV60==
def PauseWithMessage(message = None):
  if (message != None):
    print(message)
  input("\nPress the <Enter> key to exit...")
  return


# ===================================================DIV60==
class Direction(Enum):
  FROM_RM = 1
  TO_RM = 2


# ===================================================DIV60==
class Weekday(Enum):
  MONDAY = 1
  TUESDAY = 2
  WEDNESDAY = 3
  THURSDAY = 4
  FRIDAY = 5
  SATURDAY = 6
  SUNDAY = 7


# ===================================================DIV60==
class Month(Enum):
  JAN = 1
  FEB = 2
  MAR = 3
  APR = 4
  MAY = 5
  JUN = 6
  JUL = 7
  AUG = 8
  SEP = 9
  OCT = 10
  NOV = 11
  DEC = 12


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
  if style != 1 and style != 2: raise Exception ("style not supported")

  Months = (
  (         0,    '',   ''),
  ( Month.JAN, 'Jan ',  "January " ),
  ( Month.FEB, 'Feb ',  "February " ),
  ( Month.MAR, 'Mar ',  "March " ),
  ( Month.APR, 'Apr ',  "April " ),
  ( Month.MAY, 'May ',  "May " ),
  ( Month.JUN, 'Jun ',  "June " ),
  ( Month.JUL, 'Jul ',  "July " ),
  ( Month.AUG, 'Aug ',  "August " ),
  ( Month.SEP, 'Sep ',  "September " ),
  ( Month.OCT, 'Oct ',  "October " ),
  ( Month.NOV, 'Nov ',  "November " ),
  ( Month.DEC, 'Dec ',  "December " )
#  ( Month.PH, '??? ',  "??? " )
  )

  return Months[ MonthNum ] [ style ]


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==

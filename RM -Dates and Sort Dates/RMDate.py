#  D.+19550925..+00000000..
#  D.+19690000.A+00000000..
#  DS+19850301..+19861123..
#  DS+19861120..+19901200..
#  DS+19770700..+19820700..
#  DS+19820725..+19830700..
#  DS+20030000..+20200000..
#  DS+19970721..+20030000..
#  DS+19911100..+19970700..

from enum import Enum

# ===================================================DIV60==
def main():
  try:
  
    Test("D.+19550925..+00000000..", "not sure", Direction.FROM_RM )
    Test("DS+19850301..+19861123..", "not sure", Direction.FROM_RM )
    Test("D.+19690000.A+00000000..", "not sure", Direction.FROM_RM )

    Test("TThis is a text date", "Normal text date", Direction.FROM_RM )
    Test("TLast Monday", "Normal text date", Direction.FROM_RM )
    Test(".", "Empty date", Direction.FROM_RM )


    Test("P.+19690000.A+00000000..", "malformed: inital char", Direction.FROM_RM )
    Test("Q.+19690000.A+00000000..", "Quaker dtes not supported", Direction.FROM_RM )


  #  Test("Say 1960",   Direction.TO_RM )
  #  Test("About 1970", Direction.TO_RM )
  #  Test("5 Jan 1945", Direction.TO_RM )

  except Exception as e:
    print (e)

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
  if   Char_1_2 == '.': Prefix_1 = ''
  elif Char_1_2 == 'A': Prefix_1 = 'After'
  elif Char_1_2 == 'B': Prefix_1 = 'Bef'
  elif Char_1_2 == 'F': Prefix_1 = 'From'
  elif Char_1_2 == 'I': Prefix_1 = 'Since'
  elif Char_1_2 == 'O': Prefix_1 = 'Or'
  elif Char_1_2 == 'R': Prefix_1 = 'Bet/And'
  elif Char_1_2 == 'S': Prefix_1 = 'From/To'
  elif Char_1_2 == 'T': Prefix_1 = 'To'
  elif Char_1_2 == 'U': Prefix_1 = 'Until'
  elif Char_1_2 == 'Y': Prefix_1 = 'By'
  elif Char_1_2 == '-': Prefix_1 = '–'
  else: raise Exception( "Malformed RM Date: prefix_1 character")

  Char_2_3 = RMDate[2:3]
  if   Char_2_3 == '-': AdBc_1 = 'BC'
  elif Char_2_3 == '+': AdBc_1 = ''
  else: raise Exception( "Malformed RM Date: AD-BC_1 indicator")

  try:
    Year_1  = RMDate[3:7]
    Year_1_i  = int(Year_1)
    if Year_1_i == 0: Year_1 = ''
    Month_1 = RMDate[7:9]
    Month_1_i = int(Month_1)
    if Month_1_i == 0: Month_1 = ''
    if Month_1_i < 0 or Month_1_i >12 :raise Exception( "Invalid month 1 number")
    Day_1   = RMDate[9:11]
    Day_1_i = int(Day_1)
    if Day_1_i == 0: Day_1 = ''
    if Day_1_i < 0 or Day_1_i >31 : raise Exception( "Invalid day 1 number")

  except ValueError as ve:
   raise Exception( "Invalid characters in YYYY MM DD of date 2")


  DoubDate_1 = False
  Char_11_12 = RMDate[11:12]
  if   Char_11_12 == '/': DoubDate_1 = True
  elif Char_11_12 != '.': raise Exception( "Malformed RM Date: Double Date 1 indicator")

  Char_12_13 = RMDate[12:13]
  if   Char_12_13 == '.': Modifier_1 = ''
  elif Char_12_13 == 'A': Modifier_1 = 'Abt'
  elif Char_12_13 == 'S': Modifier_1 = 'Say'
  elif Char_12_13 == 'C': Modifier_1 = 'Ca'
  elif Char_12_13 == 'E': Modifier_1 = 'Est'
  elif Char_12_13 == 'L': Modifier_1 = 'Calc'
  elif Char_12_13 == '?': Modifier_1 = 'Maybe'
  elif Char_12_13 == '1': Modifier_1 = 'Prhps'
  elif Char_12_13 == '2': Modifier_1 = 'Appar'
  elif Char_12_13 == '3': Modifier_1 = 'Lkly'
  elif Char_12_13 == '4': Modifier_1 = 'Poss'
  elif Char_12_13 == '5': Modifier_1 = 'Prob'
  elif Char_12_13 == '6': Modifier_1 = 'Cert'
  elif Char_11_12 != '.': raise Exception( "Malformed RM Date: Modifier 1")

  Char_13_14 = RMDate[13:14]
  if   Char_13_14 == '-': AdBc_2 = 'BC'
  elif Char_13_14 == '+': AdBc_2 = ''
  else: raise Exception( "Malformed RM Date: AD-BC_2 indicator")

  # must be all 0 if not date range modifier
  try:
    Year_2  = RMDate[14:18]
    Year_2_i  = int(Year_2)
    if Year_2_i == 0: Year_2 = ''
    Month_2 = RMDate[18:20]
    Month_2_i = int(Month_2)
    if Month_2_i == 0: Month_2 = ''
    if Month_2_i < 0 or Month_2_i >12 :raise Exception( "Invalid month 2 number")
    Day_2   = RMDate[20:22]
    Day_2_i = int(Day_2)
    if Day_2_i == 0: Day_2 = ''
    if Day_2_i < 0 or Day_2_i >31 : raise Exception( "Invalid day 2 number")

  except ValueError as ve:
   raise Exception( "Invalid haracters in YYYY MM DD of date 2")

   # complicated
  DoubDate_2 = False
  Char_22_23 = RMDate[22:23]
  if   Char_22_23 == '/': DoubDate_2 = True
  elif Char_22_23 != '.': raise Exception( "Malformed RM Date: Double Date 2 indicator")


  # only if 2nd date
  Char_23_24 = RMDate[23:24]
  if   Char_23_24 == '.': Modifier_2 = ''
  elif Char_23_24 == 'A': Modifier_2 = 'Abt'
  elif Char_23_24 == 'S': Modifier_2 = 'Say'
  elif Char_23_24 == 'C': Modifier_2 = 'Ca'
  elif Char_23_24 == 'E': Modifier_2 = 'Est'
  elif Char_23_24 == 'L': Modifier_2 = 'Calc'
  elif Char_23_24 == '?': Modifier_2 = 'Maybe'
  elif Char_23_24 == '1': Modifier_2 = 'Prhps'
  elif Char_23_24 == '2': Modifier_2 = 'Appar'
  elif Char_23_24 == '3': Modifier_2 = 'Lkly'
  elif Char_23_24 == '4': Modifier_2 = 'Poss'
  elif Char_23_24 == '5': Modifier_2 = 'Prob'
  elif Char_23_24 == '6': Modifier_2 = 'Cert'
  elif Char_23_24 != '.': raise Exception( "Malformed RM Date: Modifier 1")

# Format the date


  Concat_date = (Prefix_1 + " " + Day_1 + " " + Month_1 + " " + Year_1 + " " + AdBc_1 + " " 
         + str(DoubDate_1) + " " + Modifier_1 + " "
         + Day_2 + " " + Month_2 + " " + Year_2 + " " + AdBc_2 + " " 
         + str(DoubDate_2) + " " + Modifier_2)
  print ("Concat_date: " + Concat_date)



  Date_1 = Day_1 + " " + NumToMonthAbbrev(Month_1_i) + " " + Year_1 + " " + AdBc_1 

  return Date_1




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
  Jan = 1
  Feb = 2
  Mar = 3
  Apr = 4
  May = 5
  Jun = 6
  Jul = 7
  Aug = 8
  Sep = 9
  Oct = 10
  Nov = 11
  Dec = 12

# ===================================================DIV60==
def NumToMonthAbbrev(MonthNum):

  if   MonthNum == 1:  name = 'Jan'
  elif MonthNum == 2:  name = 'Feb' 
  elif MonthNum == 3:  name = 'Mar' 
  elif MonthNum == 4:  name = 'Apr' 
  elif MonthNum == 5:  name = 'May' 
  elif MonthNum == 6:  name = 'Jun' 
  elif MonthNum == 7:  name = 'Jul' 
  elif MonthNum == 8:  name = 'Aug' 
  elif MonthNum == 9:  name = 'Sep' 
  elif MonthNum == 10: name = 'Oct' 
  elif MonthNum == 11: name = 'Nov' 
  elif MonthNum == 12: name = 'Dec' 
  elif MonthNum == 0: name = '' 
  else: raise Exception( "ERROR: Invalid month number")

  return name

# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==

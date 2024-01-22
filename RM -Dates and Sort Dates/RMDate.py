#  D.+19550925..+00000000..
#  D.+19690000.A+00000000..
#  DS+19850301..+19861123..
#  DS+19861120..+19901200..
#  DS+19770700..+19820700..
#  DS+19820725..+19830700..
#  DS+20030000..+20200000..
#  DS+19970721..+20030000..
#  DS+19911100..+19970700..


# ===================================================DIV60==
def main():
  try:
    Test("TThis is a text date", Direction.FROM_RM )
    Test("TLast Monday", Direction.FROM_RM )
  
    Test("D.+19550925..+00000000..", Direction.FROM_RM )
    Test("DS+19850301..+19861123..", Direction.FROM_RM )
    Test("D.+19690000.A+00000000..", Direction.FROM_RM )

    #Test("P.+19690000.A+00000000..", Direction.FROM_RM )
    #Test("Q.+19690000.A+00000000..", Direction.FROM_RM )

    #Test("Say 1960",   Direction.TO_RM )
    #Test("About 1970", Direction.TO_RM )
    #Test("5 Jan 1945", Direction.TO_RM )

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
    raise Exception( "Malformed RM Date")

  return ""

# ===================================================DIV60==
def Test(In, which):

  if which == Direction.TO_RM:
    print( In , "  to RM")
    print ( ToRMDate(In) )

  elif which == Direction.FROM_RM:
    print( In , "  from RM")
    print ( FromRMDate(In) )

  print("\n")

# ===================================================DIV60==
def PauseWithMessage(message = None):
  if (message != None):
    print(message)
  input("\nPress the <Enter> key to exit...")
  return


# ===================================================DIV60==
from enum import Enum

class Direction(Enum):
  FROM_RM = 1
  TO_RM = 2


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==

import RMDate

# ===================================================DIV60==
def main():

    print ("===========================================DIV50==\n")
    
    Test("D.+19210011..+00000000..", "11 ??? 1921", RMDate.Direction.FROM_RM )
    Test("D-+19210008..+19210011..", "11 ??? 1921", RMDate.Direction.FROM_RM )
    Test("D-+19210113..+99990000..", "13 Jan 1921-9999", RMDate.Direction.FROM_RM )
    Test("D.-10000000..+00000000..", "1000 BC   [BC dates, for my Neanderthal cousins]", RMDate.Direction.FROM_RM )
    Test("D.+00050000..+00000000..", "5  [date & sort date=5]", RMDate.Direction.FROM_RM )
    Test(".", "date is blank [sort date=10]", RMDate.Direction.FROM_RM )
    Test(".", "date is blank [sort date=11]", RMDate.Direction.FROM_RM )
    Test("D.+00300000..+00000000..", "30   [ date & sort date=30]", RMDate.Direction.FROM_RM )
    Test("D.+03000000..+00000000..", "300     [date & sort date=300] number, too big for day of month", RMDate.Direction.FROM_RM )
    Test("D.+15830101/.+00000000..", "1 Jan 1583/84 [double date]", RMDate.Direction.FROM_RM )
    Test("Q.+15880212..+00000000..", "12da 2mo 1588   [quaker date format, neeeds further investigation]", RMDate.Direction.FROM_RM )
#    Test("QR+15881112..+15881201..", "Bet 12da 11mo 1588 and 1da 12mo 1588 [quaker date format, not investigated] ", RMDate.Direction.FROM_RM )
#    Test("Q.+15881112..+00000000..", "12da 11mo 1588  [quaker date]", RMDate.Direction.FROM_RM )
#    Test("Q.+15880102/.+00000000..", "2da 1mo 1588/9   [quaker double-date]", RMDate.Direction.FROM_RM )
#    Test("Q.+15881102/.+00000000..", "2da 11mo 1588/9  [quaker double-date]", RMDate.Direction.FROM_RM )
#    Test("Q.+17511031..+00000000..", "31da 10mo 1751 [quaker date pre-1752]", RMDate.Direction.FROM_RM )
#    Test("Q.+17520101..+00000000..", "1da 1mo 1752  [quaker date post-1751]", RMDate.Direction.FROM_RM )
    Test("D-+19210000..+00010000..", "1921-1   [ sort date=1921-1 ]", RMDate.Direction.FROM_RM )
    Test("D-+19210000..+00020000..", "1921-2  [ sort date=1921-2 ]", RMDate.Direction.FROM_RM )
    Test("D-+19210000..+00030000..", "1921-3   [ sort date=1921-3 ]", RMDate.Direction.FROM_RM )
    Test("D-+19210000..+00100000..", "1921-10  [sort date=1921-10 ]", RMDate.Direction.FROM_RM )
    Test("D.+19210000..+00000000..", "1921   [std date- year only]", RMDate.Direction.FROM_RM )
    Test("D-+19210000..+99990000..", "1921–9999  [sort date=1921–9999]", RMDate.Direction.FROM_RM )
    Test("D.+19210013..+00000000..", "13 ??? 1921", RMDate.Direction.FROM_RM )
    Test("D.+19210100..+00000000..", "Jan 1921", RMDate.Direction.FROM_RM )
    Test("D.+19210113..+00000000..", "13 Jan 1921  ( sort date 13 Jan 1921-1 )", RMDate.Direction.FROM_RM )
    Test("D-+19210113.E+00010000..", "Est 13 Jan 1921-1    [prefix ignored in sort date]", RMDate.Direction.FROM_RM )
    Test("D-+19210113.A+00010000..", "Abt 13 Jan 1921-1    [prefix ignored in sort date]", RMDate.Direction.FROM_RM )
    Test("D-+19210113.S+00010000..", "Say 13 Jan 1921-1  [prefix ignored in sort date]", RMDate.Direction.FROM_RM )
    Test("D-+19210113.L+00010000..", "Calc 13 Jan 1921–1 [prefix ignored in sort date]", RMDate.Direction.FROM_RM )
    Test("D-+19210113.C+00010000..", "Ca 13 Jan 1921–1 [prefix ignored in sort date]", RMDate.Direction.FROM_RM )
    Test("D-+19210113..+00010000..", "13 Jan 1921–10000  [N=10000 changed to 1 in both dates]", RMDate.Direction.FROM_RM )
    Test("D.+19210113..+00000000..", "13 Jan 1921  ( sort date 13 Jan 1921-2 )", RMDate.Direction.FROM_RM )
    Test("D.+19210113..+00000000..", "13 Jan 1921  ( sort date 13 Jan 1921-10 )", RMDate.Direction.FROM_RM )
    Test("D-+19210113..+10000000..", "13 Jan 1921–1000", RMDate.Direction.FROM_RM )
    Test("DR+19210113..+19220125..", "Bet 13 Jan 1921 and 25 Jan 1922", RMDate.Direction.FROM_RM )
    Test("DS+19210113..+19220125..", "From 13 Jan 1921 to 25 Jan 1922", RMDate.Direction.FROM_RM )
    Test("D-+19210113..+19220125..", "13 Jan 1921-25 Jan 1922", RMDate.Direction.FROM_RM )
    Test("DO+19210113..+19220125..", "13 Jan 1921 or 25 Jan 1922", RMDate.Direction.FROM_RM )
    Test("DO+19210113..+19250125..", "13 Jan 1921 or 25 Jan 1925", RMDate.Direction.FROM_RM )
    Test("D-+19210113..+49990000..", "13 Jan 1921–4999   [largest N]", RMDate.Direction.FROM_RM )
    Test("D-+19210113..+50000000..", "13 Jan 1921–5000   [N too big, ignored in sort date]", RMDate.Direction.FROM_RM )
    Test("DB+19210113..+00000000..", "Bef 13 Jan 1921", RMDate.Direction.FROM_RM )
    Test("DY+19210113..+00000000..", "By 13 Jan 1921", RMDate.Direction.FROM_RM )
    Test("DT+19210113..+00000000..", "To 13 Jan 1921", RMDate.Direction.FROM_RM )
    Test("DU+19210113..+00000000..", "Until 13 Jan 1921", RMDate.Direction.FROM_RM )
    Test("DU+19210113..+00000000..", "Until 13 Jan 1921-1", RMDate.Direction.FROM_RM )
    Test("D.+19210113..+00000000..", "13 Jan 1921", RMDate.Direction.FROM_RM )
    Test("D.+19210113.A+00000000..", "Abt 13 Jan ", RMDate.Direction.FROM_RM )
    Test("D.+19210113.E+00000000..", "Est 13 Jan 1921   [prefix ignored in sort date]", RMDate.Direction.FROM_RM )
    Test("D.+19210113.L+00000000..", "Calc 13 Jan 1921   [prefix ignored in sort date]", RMDate.Direction.FROM_RM )
    Test("D.+19210113.C+00000000..", "Ca 13 Jan 1921     [prefix ignored in sort date]", RMDate.Direction.FROM_RM )
    Test("D.+19210113.S+00000000..", "Say 13 Jan 1921   [prefix ignored in sort date]", RMDate.Direction.FROM_RM )
    Test("DF+19210113..+00000000..", "From 13 Jan 1921", RMDate.Direction.FROM_RM )
    Test("DI+19210113..+00000000..", "Since 13 Jan 1921", RMDate.Direction.FROM_RM )
    Test("DA+19210113..+00000000..", "Aft 13 Jan 1921", RMDate.Direction.FROM_RM )
    Test("D-+19210113..+90000000..", "13 Jan 1921–9000", RMDate.Direction.FROM_RM )
    Test("D.+19210114..+00000000..", "14 Jan 1921", RMDate.Direction.FROM_RM )
    Test("D-+19230000..+19240000..", "1923-1924", RMDate.Direction.FROM_RM )
    Test("D.+20000000.A+00000000..", "about 2000", RMDate.Direction.FROM_RM )
    Test("D.+20000000.S+00000000..", "say 2000", RMDate.Direction.FROM_RM )
    Test("D.+20000000.C+00000000..", "circa 2000", RMDate.Direction.FROM_RM )
    Test("D.+20000000.E+00000000..", "estimated 2000", RMDate.Direction.FROM_RM )
    Test("D.+20000000.L+00000000..", "calculated 2000", RMDate.Direction.FROM_RM )
    Test("D.+20000000.?+00000000..", "maybe 2000", RMDate.Direction.FROM_RM )
    Test("D.+20000000.1+00000000..", "perhaps 2000", RMDate.Direction.FROM_RM )
    Test("D.+20000000.2+00000000..", "apparently 2000", RMDate.Direction.FROM_RM )
    Test("D.+20000000.3+00000000..", "likely 2000", RMDate.Direction.FROM_RM )
    Test("D.+20000000.4+00000000..", "possibly 2000", RMDate.Direction.FROM_RM )
    Test("D.+20000000.5+00000000..", "probably 2000", RMDate.Direction.FROM_RM )
    Test("D.+20000000.6+00000000..", "certainly 2000", RMDate.Direction.FROM_RM )
    Test("DB+21000000..+00000000..", "before 2100", RMDate.Direction.FROM_RM )
    Test("DY+21000000..+00000000..", "by 2100", RMDate.Direction.FROM_RM )
    Test("DT+21000000..+00000000..", "to 2100", RMDate.Direction.FROM_RM )
    Test("DU+21000000..+00000000..", "until 2100", RMDate.Direction.FROM_RM )
    Test("DF+21000000..+00000000..", "from 2100", RMDate.Direction.FROM_RM )
    Test("DI+21000000..+00000000..", "since 2100", RMDate.Direction.FROM_RM )
    Test("DA+21000000..+00000000..", "after 2100", RMDate.Direction.FROM_RM )
    Test("DR+22000000..+23000000..", "between 2200 and 2300", RMDate.Direction.FROM_RM )
    Test("DS+22000000..+23000000..", "from 2200 to 2300", RMDate.Direction.FROM_RM )
    Test("D-+22000000..+23000000..", "2200–2300", RMDate.Direction.FROM_RM )
    Test("DO+22000000..+23000000..", "2200–2300", RMDate.Direction.FROM_RM )
    Test("D.+00000100..+00000000..", "Jan   [std date - month only]", RMDate.Direction.FROM_RM )
    Test("D-+00000100..+00000300..", "Jan-Mar   [month range, no year]", RMDate.Direction.FROM_RM )
    Test("D.+00000113..+00000000..", "13 Jan   [no year]", RMDate.Direction.FROM_RM )
    Test("D.+00000300..+00000000..", "Mar  [month only]", RMDate.Direction.FROM_RM )
    Test(".", "blank date", RMDate.Direction.FROM_RM )
    Test("TText date", "Text date", RMDate.Direction.FROM_RM )
    Test("T1 January 1583/1 apr 4", "TEXT DATE because double date does lots of validation", RMDate.Direction.FROM_RM )

    Test("TThis is a text date", "Normal text date", RMDate.Direction.FROM_RM )
    Test("TLast Monday", "Normal text date", RMDate.Direction.FROM_RM )
    Test(".", "Empty date", RMDate.Direction.FROM_RM )

    Test("P.+19690000.A+00000000..", "malformed: initial char", RMDate.Direction.FROM_RM )
    Test("Q.+19690000.A+00000000..", "Quaker dates not supported", RMDate.Direction.FROM_RM )


  #  Test("Say 1960",   RMDate.Direction.TO_RM )
  #  Test("About 1970", RMDate.Direction.TO_RM )
  #  Test("5 Jan 1945", RMDate.Direction.TO_RM )


    PauseWithMessage()
    return


# ===================================================DIV60==
def Test(In, Expected, whichWay):
  try:
    print( In , "     : " + Expected )

    if whichWay == RMDate.Direction.TO_RM:
      print ( RMDate.ToRMDate(In, RMDate.Format.SHORT) )
  
    elif whichWay == RMDate.Direction.FROM_RM:
#      print ( "==" + RMDate.FromRMDate(In, RMDate.Format.SHORT) + "==" )
      print ( "==" + RMDate.FromRMDate(In, RMDate.Format.LONG) + "==" )

  except Exception as e:
    print (e)

  print("\n")


# ===================================================DIV60==
def PauseWithMessage(message = None):
  if (message != None):
    print(message)
  input("\nPress the <Enter> key to continue...")
  return


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==

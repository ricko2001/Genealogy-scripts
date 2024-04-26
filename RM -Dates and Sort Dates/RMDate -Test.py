import RMDate

# ===================================================DIV60==
def main():
    print("===========================================DIV50==\n")

#   SELECT '    ('|| rowid ||', ' , char(34)|| Date|| char(34)||', ', char(34)|| SortDate|| char(34)||', ', char(34)|| Details|| char(34)||'),' 
#   FROM EventTable ORDER BY SortDate
#
#   in the eventTable in RM database, Fact description=   full Date || Sort Date  || comments


    TestData = (
    (51, 	"D.-99990101..+00000000..", 	"598701260144652", 	"1 January 9999 BC || 1 January 9999 BC  || "),
    (49, 	"D.-00100101..+00000000..", 	"5623905785985630220", 	"1 January 10 BC || 1 January 10 BC || "),
    (50, 	"D.-00010101..+00000000..", 	"5628972335566422028", 	"1 January 1 BC || 1 January 1 BC  ||   year 0 not allowed"),
    (41, 	".", 	"5635129050926153740", 	"|| 10 || date is blank, sort date=10"),
    (42, 	".", 	"5635692000879575052", 	" || 11 || date is blank, sort date=11"),
    (19, 	"D.+15830101/.+00000000..", 	"6521248011739201548", 	"1 January 1583/4 || 1 January 1584 || double date"),
    (22, 	"Q.+15880212..+00000000..", 	"6523611411983106060", 	"12th da 2nd mo 1588 || 12 April 1588 ||  entered =12da 2mo 1588"),
    (21, 	"QR+15881112..+15881201..", 	"6524068803793519631", 	"between 12th da 11th mo 1588 and 1st da 12th mo 1588 || between 12 January 1589 and 1 February 1589 || Bet 12da 11mo 1588 and 1da 12mo 1588 Quaker"),
    (20, 	"Q.+15881112..+00000000..", 	"6524068808820260876", 	"12th da 11th mo 1588 || 12 January 1589 || 12da 11mo 1588 Quaker Date"),
    (31, 	"Q.+15880102/.+00000000..", 	"6524133680006299660", 	"2nd da 1st mo 1588/9 || 2 March 1589 || 2da 1mo 1588/9 Quaker double-date"),
    (33, 	"Q.+15881102/.+00000000..", 	"6524626261215543308", 	"2nd da 11th mo 1588/9 || 2 January 1590 || 2da 11mo 1588/9"),
    (25, 	"Q.+17511031..+00000000..", 	"6615664174727954444", 	"31st da 10th mo 1751 || 31 December 1751 || 31da 10mo 1751 Quaker date pre-1752"),
    (23, 	"Q.+17520101..+00000000..", 	"6615823603913981964", 	"1st da 1st mo 1752 || 1 January 1752 || 1da 1mo 1752 Quaker date post-1751"),
    (45, 	"R.+19200100..+00000000..", 	"6710398646332948492", 	"March Quarter 1920 || January 1920 || "),
    (46, 	"R.+19200200..+00000000..", 	"6710504199449214988", 	"June Quarter 1920 || April 1920 || "),
    (47, 	"R.+19200300..+00000000..", 	"6710609752565481484", 	"September Quarter 1920 ||  July 1920  || "),
    (48, 	"R.+19200400..+00000000..", 	"6710715305681747980", 	"December Quarter 1920 || October 1920 ||  "),
    (35, 	"D.+19210000..+00000000..", 	"6710926405222268949", 	"1921 || 1921-1  ||"),
    (36, 	"D.+19210000..+00000000..", 	"6710926405223317525", 	"1921 || 1921-2 || "),
    (37, 	"D.+19210000..+00000000..", 	"6710926405231706133", 	"1921 || 1921-10  || "),
    (28, 	"D.+19210000..+00000000..", 	"6710926411914280972", 	"1921 || 1921 || "),
    (26, 	"D.+19210013..+00000000..", 	"6710933558739861516", 	"13 ??? 1921 || 13 ??? 1921 || "),
    (27, 	"D.+19210100..+00000000..", 	"6710961596286369804", 	"January 1921 || January 1921 ||"),
    (38, 	"D.+19210113..+00000000..", 	"6710968736419938325", 	"13 January 1921 || 13 January 1921–1 || "),
    (39, 	"D.+19210113..+00000000..", 	"6710968736420986901", 	"13 January 1921 || 13 January 1921–2 || "),
    (40, 	"D.+19210113..+00000000..", 	"6710968736429375509", 	"13 January 1921 ||  13 January 1921–10  || "),
    (14, 	"DR+19210113..+19220125..", 	"6710968738434343951", 	"between 13 January 1921 and 25 January 1922 || between 13 January 1921 and 25 January 1922  || "),
    (15, 	"DS+19210113..+19220125..", 	"6710968738434343954", 	"from 13 January 1921 to 25 January 1922  || from 13 January 1921 to 25 January 1922  || "),
    (16, 	"D-+19210113..+19220125..", 	"6710968738434343957", 	"13 January 1921–25 January 1922 || 13 January 1921–25 January 1922  ||  "),
    (17, 	"DO+19210113..+19220125..", 	"6710968738434343960", 	"13 January 1921 or 25 January 1922 || 13 January 1921 or 25 January 1922 || "),
    (43, 	"DO+19210113..+19250125..", 	"6710968738437489688", 	"13 January 1921 or 25 January 1925 ||  13 January 1921 or 25 January 1925 || "),
    (2, 	"DB+19210113..+00000000..", 	"6710968743111950336", 	"before 13 January 1921 || before 13 January 1921 ||"),
    (3, 	"DY+19210113..+00000000..", 	"6710968743111950339", 	"by 13 January 1921 || by 13 January 1921  || "),
    (4, 	"DT+19210113..+00000000..", 	"6710968743111950342", 	"to 13 January 1921 || to 13 January 1921  |} "),
    (5, 	"DU+19210113..+00000000..", 	"6710968743111950345", 	"until 13 January 1921 || until 13 January 1921 || "),
    (1, 	"D.+19210113..+00000000..", 	"6710968743111950348", 	"13 January 1921 || 13 January 1921 || "),
    (9, 	"D.+19210113.A+00000000..", 	"6710968743111950348", 	"about 13 January 1921 || 13 January 1921 || "),
    (10, 	"D.+19210113.E+00000000..", 	"6710968743111950348", 	"estimated 13 January 1921 || 13 January 1921 || "),
    (11, 	"D.+19210113.L+00000000..", 	"6710968743111950348", 	"calculated 13 January 1921 || 13 January 1921 || "),
    (12, 	"D.+19210113.C+00000000..", 	"6710968743111950348", 	"circa 13 January 1921 || 13 January 1921 || "),
    (13, 	"D.+19210113.S+00000000..", 	"6710968743111950348", 	"say 13 January 1921 || 13 January 1921 ||  "),
    (6, 	"DF+19210113..+00000000..", 	"6710968743112997915", 	"from 13 January 1921 || from 13 January 1921 || "),
    (7, 	"DI+19210113..+00000000..", 	"6710968743112997918", 	"since 13 January 1921 || since 13 January 1921 || "),
    (8, 	"DA+19210113..+00000000..", 	"6710968743112997919", 	"after 13 January 1921 || after 13 January 1921 || "),
    (52, 	"D.+20240324/.+00000000/.", 	"6769591954325897228", 	"24 March 2024/5 || 24 March 2025 ||   VALID 1 Jan to 24 Mar only.   1583/4 to present"),
    (30, 	"D.+00000100..+00000000..", 	"9222844288452263948", 	"January || January || "),
    (32, 	"D-+00000100..+00000300..", 	"9222844288452460565", 	"January–March || January–March ||   no-year range"),
    (29, 	"D.+00000113..+00000000..", 	"9222851435277844492", 	"13 January || 13 January  || "),
    (44, 	"D.+00000300..+00000000..", 	"9222914657196441612", 	"March || March ||  "),
    (18, 	".", 	"9223372036854775807", 	" || || blank date"),
    (34, 	"TText date", 	"9223372036854775807", 	"Text date ||  ||  "),

  )


    for item in TestData:
        Test(item )

   # PauseWithMessage()
    return


# ===================================================DIV60==
def Test(test_item):
    try:
        out= RMDate.from_RMDate(test_item[1], RMDate.Format.LONG)
        expect_full_date = parse_description(test_item[3], 0 )
        expect_sort_date = parse_description(test_item[3], 1 )
        if out != expect_full_date:
            print("   {} ======= '{}'  !=  '{}'  full date".format(test_item[0], out, expect_full_date))
        else:
            print("   {}     '{}'  ==  '{}'  full date".format(test_item[0], out, expect_full_date))

        if out != expect_sort_date:
            print("   {} ======= '{}'  !=  '{}'  sort date".format(test_item[0], out, expect_full_date))
        else:
            print("   {}     '{}'  ==  '{}'  sort date".format(test_item[0], out, expect_full_date))


        #   print(RMDate.FromRMDate(In, RMDate.Format.LONG) + "==")

    except Exception as e:
        print(e)




# ===================================================DIV60==
def parse_description(In, which):
    parsed=  (In.split("||", 2) [which])
    return parsed.strip()


# ===================================================DIV60==
def Test_OLD(In, Expected, whichWay):
    try:
        print(In, "     : " + Expected)

        if whichWay == RMDate.Direction.TO_RM:
            print(RMDate.ToRMDate(In, RMDate.Format.SHORT))

        elif whichWay == RMDate.Direction.FROM_RM:
            #      print ( "==" + RMDate.FromRMDate(In, RMDate.Format.SHORT) + "==" )
            print("==" + RMDate.FromRMDate(In, RMDate.Format.LONG) + "==")

    except Exception as e:
        print(e)

    print("\n")


# ===================================================DIV60==
def PauseWithMessage(message=None):
    if (message != None):
        print(message)
    input("\nPress the <Enter> key to continue...")
    return


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':

    main()

# ===================================================DIV60==

import RMDate

# ===================================================DIV60==
def main():
    print("===========================================DIV50==\n")

#   SELECT '    ('|| EventID|| ', ',
#                 char(34) || Name     || char(34) || ', ',
#                 char(34) || Date     || char(34) || ', ',
#                             SortDate || ', ',
#                 char(34) || Details  || char(34) || '),' 
#   FROM EventTable AS et
#   INNER JOIN FactTypeTable AS ftt ON et.EventType = ftt.FactTypeID
#   ORDER BY SortDate
#   
#   
#   char(34) = double quote char
#   || concatenation operator
#   use a , to add a tab between column output
#   
#
#   in the eventTable in RM database, Fact description=   full Date || Sort Date  || comments


    TestData = (
#    0       1           2                              3                       4
    (66, 	"_Std_1", 	"D.+99991231..+00000000..", 	-7187868683162615796, 	"31 December 9999 || 31 December 9999 || largest date, wrong sort generated $NG"),
    (51, 	"_Std_1", 	"D.-99990101..+00000000..", 	598701260144652, 	"1 January 9999 BC || 1 January 9999 BC  || largetst abs year 9999"),
    (49, 	"_Std_1", 	"D.-00100101..+00000000..", 	5623905785985630220, 	"1 January 10 BC || 1 January 10 BC || "),
    (50, 	"_Std_1", 	"D.-00010101..+00000000..", 	5628972335566422028, 	"1 January 1 BC || 1 January 1 BC  ||   year 0 not allowed"),
    (72, 	"_Std_1", 	"D.+00010000..+00000000..", 	5630062501345361932, 	"1 || 1 || year 1"),
    (41, 	"_Std_1", 	"D.+00100000..+00000000..", 	5635129050926153740, 	" 10 || 10 || year 10"),
    (42, 	"_Std_1", 	"D.+00110000..+00000000..", 	5635692000879575052, 	" 11 || 11 ||  year 11"),
    (19, 	"_JulGeor", 	"D.+15880101/.+00000000/.", 	6524062761506308108, 	"1 January 1588/9 || 1 January 1589 ||  DD"),
    (68, 	"_JulGeor", 	"DS+15880201/.+16000302..", 	6524097940863256594, 	"from 1 February 1588/9 to 2 March 1600 || from 1 February 1591 to 2 March 1600 ||  DD range w/ norm"),
    (62, 	"_JulGeor", 	"DS+15880201/.+16000302/.", 	6524097940864305170, 	"from 1 February 1588/9 to 2 March 1600/1 || from 1 February 1589 to 2 March 1601|| DD range"),
    (31, 	"_Quaker", 	"Q.+15880102/.+00000000..", 	6524133680006299660, 	"2nd da 1st mo 1588/9 || 2 March 1589 || 2da 1mo 1588/9 Quaker double-date"),
    (33, 	"_Quaker", 	"Q.+15881102/.+00000000..", 	6524626261215543308, 	"2nd da 11th mo 1588/9 || 2 January 1590 || 2da 11mo 1588/9"),
    (22, 	"_Quaker", 	"Q.+15930212..+00000000..", 	6526426161750212620, 	"12th da 2nd mo 1593 || 12 April 1588 ||  entered =12da 2mo 1593"),
    (21, 	"_Quaker", 	"QR+15981112..+15991201..", 	6529698303339267087, 	"between 12th da 11th mo 1598 and 1st da 12th mo 1599 || between 12 January 1599 and 1 February 1600 ||  range Q & Q"),
    (20, 	"_Quaker", 	"Q.+15981112..+00000000..", 	6529698308354473996, 	"12th da 11th mo 1598 || 12 January 1599 || Quaker "),
    (73, 	"_Quaker", 	"Q.+16010300..+00000000..", 	6530958348679905292, 	"3rd mo 1601 || May 1601 || Quaker- no day"),
    (25, 	"_Quaker", 	"Q.+17511031..+00000000..", 	6615664174727954444, 	"31st da 10th mo 1751 || 31 December 1751 || 31da 10mo 1751 Quaker date pre-1752"),
    (23, 	"_Quaker", 	"Q.+17520101..+00000000..", 	6615823603913981964, 	"1st da 1st mo 1752 || 1 January 1752 || 1da 1mo 1752 Quaker date post-1751"),
    (45, 	"_Quarter", 	"R.+19200100..+00000000..", 	6710398646332948492, 	"March Quarter 1920 || January 1920 || QT"),
    (63, 	"_Quarter", 	"RS+19200200..+19900000..", 	6710504194842820626, 	"from June Quarter 1920 to 1990 || from April 1920 to 1990 || Quarter- range QT & STD"),
    (46, 	"_Quarter", 	"R.+19200200..+00000000..", 	6710504199449214988, 	"June Quarter 1920 || April 1920 ||  QT"),
    (47, 	"_Quarter", 	"R.+19200300..+00000000..", 	6710609752565481484, 	"September Quarter 1920 ||  July 1920  ||  QT"),
    (48, 	"_Quarter", 	"R.+19200400..+00000000..", 	6710715305681747980, 	"December Quarter 1920 || October 1920 ||  QT"),
    (35, 	"_Std_2", 	"D-+19210000..+00010000..", 	6710926405222268949, 	"1921–1 || 1921–1 ||  STD dash range"),
    (36, 	"_Std_2", 	"D-+19210000..+00020000..", 	6710926405223317525, 	"1921–2 || 1921–2 || STD dash range"),
    (37, 	"_Std_2", 	"D-+19210000..+00100000..", 	6710926405231706133, 	"1921–10 || 1921–10  || STD dash range"),
    (28, 	"_Std_1", 	"D.+19210000..+00000000..", 	6710926411914280972, 	"1921 || 1921 || STD no day or month"),
    (69, 	"_Std_2", 	"DR+19210013..+19230015..", 	6710933554063227919, 	"between 13 ??? 1921 and 15 ??? 1923 || between 13 ??? 1921 and 15 ??? 1923 || "),
    (26, 	"_Std_1", 	"D.+19210013..+00000000..", 	6710933558739861516, 	"13 ??? 1921 || 13 ??? 1921 ||  STD no month"),
    (27, 	"_Std_1", 	"D.+19210100..+00000000..", 	6710961596286369804, 	"January 1921 || January 1921 || STD"),
    (38, 	"_Std_1", 	"D.+19210113..+00000000..", 	6710968736419938325, 	"13 January 1921 || 13 January 1921–1 ||  D & SD differ"),
    (39, 	"_Std_1", 	"D.+19210113..+00000000..", 	6710968736420986901, 	"13 January 1921 || 13 January 1921–2 ||  D & SD differ"),
    (40, 	"_Std_1", 	"D.+19210113..+00000000..", 	6710968736429375509, 	"13 January 1921 ||  13 January 1921–10  ||  D & SD differ"),
    (12, 	"_Std_2", 	"DS+19210113.C+19210217.S", 	6710968738433352722, 	"from circa 13 January 1921 to say 17 February 1921 || from 13 January 1921 to 17 February 1921 ||"),
    (14, 	"_Std_2", 	"DR+19210113..+19220125..", 	6710968738434343951, 	"between 13 January 1921 and 25 January 1922 || between 13 January 1921 and 25 January 1922  || "),
    (15, 	"_Std_2", 	"DS+19210113..+19220125..", 	6710968738434343954, 	"from 13 January 1921 to 25 January 1922  || from 13 January 1921 to 25 January 1922  || "),
    (16, 	"_Std_2", 	"D-+19210113..+19220125..", 	6710968738434343957, 	"13 January 1921–25 January 1922 || 13 January 1921–25 January 1922  ||  STD dash range"),
    (17, 	"_Std_2", 	"DO+19210113..+19220125..", 	6710968738434343960, 	"13 January 1921 or 25 January 1922 || 13 January 1921 or 25 January 1922 || "),
    (43, 	"_JulGeor", 	"DO+19210113..+19220223/.", 	6710968738435456024, 	"13 January 1921 or 23 February 1922/3 || 13 January 1921 or 23 February 1923 || DD range & STD"),
    (2, 	"_Std_2", 	"DB+19210113..+00000000..", 	6710968743111950336, 	"before 13 January 1921 || before 13 January 1921 ||"),
    (3, 	"_Std_1", 	"DY+19210113..+00000000..", 	6710968743111950339, 	"by 13 January 1921 || by 13 January 1921  || "),
    (4, 	"_Std_1", 	"DT+19210113..+00000000..", 	6710968743111950342, 	"to 13 January 1921 || to 13 January 1921  |} "),
    (5, 	"_Std_1", 	"DU+19210113..+00000000..", 	6710968743111950345, 	"until 13 January 1921 || until 13 January 1921 || "),
    (9, 	"_Std_1", 	"D.+19210113.A+00000000..", 	6710968743111950348, 	"about 13 January 1921 || 13 January 1921 || confidence not in SD"),
    (10, 	"_Std_1", 	"D.+19210113.E+00000000..", 	6710968743111950348, 	"estimated 13 January 1921 || 13 January 1921 || confidence not in SD"),
    (11, 	"_Std_1", 	"D.+19210113.L+00000000..", 	6710968743111950348, 	"calculated 13 January 1921 || 13 January 1921 || confidence not in SD"),
    (13, 	"_Std_1", 	"D.+19210113.S+00000000..", 	6710968743111950348, 	"say 13 January 1921 || 13 January 1921 ||  confidence not in SD"),
    (71, 	"_Std_1", 	"D.+19210113..+00000000..", 	6710968743111950348, 	"13 January 1921 || 13 January 1921||  STD"),
    (6, 	"_Std_1", 	"DF+19210113..+00000000..", 	6710968743112997915, 	"from 13 January 1921 || from 13 January 1921 ||  from  STD"),
    (64, 	"_Std_1", 	"DF+19210113.C+00000000..", 	6710968743112997915, 	"from circa 13 January 1921  || from 13 January 1921  ||  confidence not in SD"),
    (7, 	"_Std_1", 	"DI+19210113..+00000000..", 	6710968743112997918, 	"since 13 January 1921 || since 13 January 1921 ||  since STD"),
    (8, 	"_Std_1", 	"DA+19210113..+00000000..", 	6710968743112997919, 	"after 13 January 1921 || after 13 January 1921 ||  after STD"),
    (59, 	"_Std_1", 	"DF+19210100..+00000000..", 	6710996230903692315, 	"from January 1921 || from January 1921 || from- no day"),
    (60, 	"_Std_1", 	"DF+19210000..+00000000..", 	6711488812112935963, 	"from 1921 || from 1921 || from- no day, no month"),
    (58, 	"_Std_2", 	"D-+19300600..+00010000..", 	6716204061035593749, 	"June 1930–1 || June 1930–1 || STD dash range"),
    (57, 	"_Std_2", 	"D-+19300600..+19300000..", 	6716204063058296853, 	"June 1930–1930 || June 1930–1930 || STD dash range"),
    (56, 	"_Std_2", 	"D-+19300600..+19300700..", 	6716204063058755605, 	"June 1930–July 1930 || June 1930–July 1930 || STD dash range"),
    (52, 	"_JulGeor", 	"D.+20240324/.+00000000/.", 	6769591954325897228, 	"24 March 2024/5 || 24 March 2025 ||   DD   VALID 1 Jan to 24 Mar only.   1583/4 to present"),
    (67, 	"_Std_1", 	"D.+49991231..+00000000..", 	8444125623440375820, 	"31 December 4999 || 31 December 4999 || largest date with correct generated sort  date"),
    (30, 	"_Std_1", 	"D.+00000100..+00000000..", 	9222844288452263948, 	"January || January || "),
    (32, 	"_Std_2", 	"D-+00000100..+00000300..", 	9222844288452460565, 	"January–March || January–March ||   no years"),
    (54, 	"_Std_2", 	"D-+00000104..+00000200..", 	9222846487475650581, 	"4 January–February || 4 January–February || no years"),
    (29, 	"_Std_1", 	"D.+00000113..+00000000..", 	9222851435277844492, 	"13 January || 13 January  ||  no years"),
    (55, 	"_Std_2", 	"D-+00000300..+00010000..", 	9222914650504429589, 	"March–1 || March–1 || no year dash a year"),
    (44, 	"_Std_1", 	"D.+00000300..+00000000..", 	9222914657196441612, 	"March || March ||  "),
    (53, 	"_Std_2", 	"D-+00000304..+00000406..", 	9222916856219965461, 	"4 March–6 April  || 4 March–6 April || "),
    (18, 	"_Std_1", 	".", 	9223372036854775807, 	" || || blank date"),
    (34, 	"_Std_1", 	"TText date", 	9223372036854775807, 	"Text date ||  ||  "),
  )
    

    Subset = False

    for item in TestData:
        if Subset:
            if item[0] not in (60, ):    # to run a specific test 
                continue
        else:
            # SKIP THESE TESTS
            # Quaker dates
            # Quarter dates
            # Split dates
            # Sort date changed from default
            if item[0] in (31, 33, 22, 21, 20, 73, 25, 23 ):  
                continue # QUAKER
            if item[0] in (45, 63, 46, 47, 48 ): 
                continue # QUARTER
            if item[0] in (19, 68, 62, 43, 52): 
                continue # Julian double date
            if item[0] in (38, 39, 40): 
                continue # SORT date set differently than main date
            if item[0] in (66,): 
                continue # out of range date, sort date generated by RM is wrong
        Test(item)

   # PauseWithMessage()
    return


# ===================================================DIV60==
def Test(test_item):
    try:
        #   types of date
        #   human readable with 8 formats and internal storage date
        #   internal dates can be displayed as human readable in 8 formats
        #   human readable canonical form can be converted to internal storage dates
        #   human readable non-canonical form can be parsed to a canonical form and then converted

        #   internal Date   (RMDate)
        #   internal Sort Date 
        #   human readable Date
        #   human readable Sort Date

        TD_EvemtID = test_item[0]
        TD_internal_RMdate = test_item[2]
        TD_internal_Sortdate = int(test_item[3])
        GUI_full_date = parse_description(test_item[4], 0 )
        GUI_sort_date = parse_description(test_item[4], 1 )

        out_human_readable_from_internal_RMDate= RMDate.from_RMDate(TD_internal_RMdate, RMDate.Format.LONG)
        out_internal_Sortdate = RMDate.to_RMsort_date(TD_internal_RMdate)
    #    out_internal_RMDate= RMDate.from_RMsort_date(TD_internal_Sortdate)
    #    out_human_readable_from_internal_sort_Date= RMDate.from_RMDate(out_internal_RMDate, RMDate.Format.LONG)


        # DB internal date to human readable vs GUI date
        if out_human_readable_from_internal_RMDate != GUI_full_date:
            print("   {} ======= '{}'  !=  '{}'  ".format(TD_EvemtID, out_human_readable_from_internal_RMDate, GUI_full_date))
        else:
            print("   {}     '{}'  ==  '{}'  ".format(    TD_EvemtID, out_human_readable_from_internal_RMDate, GUI_full_date))

        # out_internal_Sortdate vs TD_internal_Sortdate
        if out_internal_Sortdate != TD_internal_Sortdate:
            print("   {} ======= '{}'  !=  '{}'  ".format(TD_EvemtID, out_internal_Sortdate, TD_internal_Sortdate))
        else:
            print("   {}     '{}'  ==  '{}'  ".format(    TD_EvemtID, out_internal_Sortdate, TD_internal_Sortdate))

#        # DB internal SORT date to human readable vs GUI sort date
#        if out_human_readable_from_internal_sort_Date != GUI_sort_date:
#            print("   {} ======= '{}'  !=  '{}'  ".format(TD_EvemtID, out_human_readable_from_internal_sort_Date, GUI_sort_date))
#        else:
#            print("   {}     '{}'  ==  '{}'  ".format(TD_EvemtID, out_human_readable_from_internal_sort_Date, GUI_sort_date))


        #   print(RMDate.FromRMDate(In, RMDate.Format.LONG) + "==")

    except Exception as e:
        print(e)


# ===================================================DIV60==
def parse_description(In, which):
    # Fact description=   full Date || Sort Date  || comments
    # 0 human readable date, format= 10 January 1959
    # 1 human readable sort date, format= 10 January 1959

    # all formats (from RM v9 prefereces)
    #  10 Jan 1959
    #  Jan 10, 1959
    #  10 January 1950
    #  January 10, 1959
    #  10 JAN 1959
    #  JAN 10, 1950
    #  10 JANUARY 1950
    #  JANUARY 10, 1950

    parsed=  (In.split("||") [which])
    return parsed.strip()


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

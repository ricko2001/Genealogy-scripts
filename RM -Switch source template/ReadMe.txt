Change the source template used by a source

The RootsMagic (RM) application does not provide a way for the user to modify a Source by changing which SourceTemplate it uses. This utility does that.

A common use is when one wants to change the fields of a SourceTemplate that's already in use. Instead of editing the template, one copies the in-use SourceTemplate in RM, renames the copy, edits the copy and then uses this utility to switch the source or set of sources to use the new SourceTemplate copy that now has the desired fields.

This application is what is called a command line utility. To use it, one first edits
the supplied text file named "RM-Python-config.ini". This can be done using the Windows app "NotePad."
The file contains options and required configuration settings. One then double clicks 
the SwitchSourceTemplate file. This momentarily displays the black command console window 
and at the same time, generates the Report text file which contains the results of the requested actions.


Overview
The use this this utility involves several steps-
* download the necessary files to your computer.
* determine witch source or set of sources should have their SourceTemplates switched.
  (If more than one source is to be changed, they all need to be based on the same SourceTemplate.)
* determine the exact names of the SourceTemplate already in use and the SourceTemplate to be used instead.
* determine how data described by the existing SourceTemplate will be mapped to the new SourceTemplate.
* edit the RM-Config.ini file to include the information determined above.
* test the RM-Config.ini file values by running the options in order they appear.
* run the utility with the MAKE_CHANGES option
* confirm that the desired changes have been made and no others.





Step 1
Specify which sources should have their SourceTemplate switched.
We need to create a list of these. A SQL select will create the list using search criteria: 
 * SourceTemplate name (exact match)
 * Source name allowing SQL LIKE wild card characters "%" and "_".

The RM_Config.ini file has a field named "old" which is assigned the name of the existing SourceTemplate
and the ini file has a field named "SourceNamesLike" which is assigned the search expression.

An example:
Say there are a bunch of sources in the RM file that have SourceTemplate names and SourceNames
SourceTemplate		SourceName
TemplBIRTH			BIRTH Ancestry John Smith
TemplBIRTH			BIRTH MyHeritage JOE
TemplBIRTH			BIRTH Helen Sauer
TemplBIRTH			BIRTH Frank Sauer
oldBIRTH			BIRTH MyHeritage Mike

Say we wanted to change the SourceTemplate for the first 4 of these.
TEMPLATE_OLD = TemplBIRTH
SOURCE_NAME_LIKE = BIRTH %

The list would include the first 4.

If the search criteria were-
TEMPLATE_OLD = oldBIRTH
SOURCE_NAME_LIKE = BIRTH %

the list would only include the 5th source.

One could work with just one source at a time by giving the full source name and not including a wild card, say
TEMPLATE_OLD = TemplBIRTH
SOURCE_NAME_LIKE = BIRTH Helen Sauer

the list would include only the 3rd source. (Note that the search is not case sensitive)

If all of the desired Sources can't be found with one value of SOURCE_NAME_LIKE, you can run the utility multiple times with different values of SOURCE_NAME_LIKE.

Note that we have already determined the existing SourceTemplate name and have specified it in th RM-Config.ini file as the value of "TEMPLATE_OLD". Look in the Source template list in RM to get the name of the SourceTemplate to be used.


======================================================================
Getting Started

To install and use the script file version:
*  Download and install Python for Windows x64  -see below
*  Download unifuzz64.dll   -see below
*  Download these files from GitHub
      Switch-source-template.py
      RM-Python-config.ini
*  Create a folder on disk and copy these files to it-
      TestExternalFiles.py
      RM-Python-config.ini
      unifuzz64.dll
*  Edit the RM-Python-config.ini to specify the required parameters.
   (To edit, Open NotePad and drag the ini file onto the notepad window.)
   location of the RM file and 
   the unifuzz64.dll file . 
   Some script functions may be turned on or off. The required edits should be obvious.
*  Double click the Switch-source-template.py file to run the 
   script and generate the report file. 
*  Examine the report output file.




The template currently in use and the one that will be used will presumably have differiert fields, type sentences etc.
If one only changes a source's template in the database, the source will have the fields and data corresponding to the template it was created with.

We assume that we want to rename fields to those used in the new template.
We may want to add new empty fields if they exist in the new template
We may want to delete old fields if there is no point to rename them to a field used in new template.

Fields may be in either source or citation. In RM UI, citation fields have a y in column.
All fields are saved as plain text. Their type info is used for display and input.

Script use:
Edit the RM-Python-config.ini file-
Set DB path and RMNOCASE path
Add section-

[Source_Templates]
List_Sources	= yes
old	=	10034
SourceNamesLike = MR %

old is the existing SourceTemplateID specified by the source
SourceNamesLike is the search criteria fed to the SQL LIKE function.
Looks like leading or trailing spaces won't work in search.

The selection by SourceTemplateID is easy, the name Like selection may be an issue.
The script prints out the selected sources (ID and name) to the console.
Confirm that the list is what is desired.

Now double check that a new source template exists and has the properties desired.
run the script with

[Source_Templates]
old	=	10034
new	=	10045
List_Fields		= yes

to list fields of old and new template.
Copy from window and paste into the RM-Python-config.ini.

Organize into a table with whitespace separating columns (tabs, or blanks)
Important- "mapping" is at left margin, subsequent lines are indented all the same amount.

mapping = 
	n		SrcInfo			SrcInfo
	n		SrcCitation		SrcCitation
	n		Person			CoupleNames
	n		AccessDate		AccessDate
	n		NULL			EventDate
	n		NULL			EventType
	y		CD				CD
	y		NULL			NewField


first column specified whether the mapping is for source (no) or citation (y)
second col specifies the field name as it currently exists.
third is the name to use in renaming the first column. 
NULL is a special name. 
in first column, it means add a field with the name specified in the third column.
in the third column, it means delete the field specified in the second column.

This mapping should correspond to the templates being used.
Don't add fields that aren't specified in the new template,
add a fields for all templates specified in the new template.

all three tables have XML data-
SourceTemplateTable		FieldDefs
SourceTable				Fields
CitationTable			Fields


SourceTemplateTable fields
<Root>
<Fields>
<Field>
<FieldName></FieldName>
<DisplayName></DisplayName>
<Type></Type>
<Hint></Hint>
<LongHint></LongHint>
<CitationField>False</CitationField>
</Field>
</Fields>
</Root>



First test case
split Marriage records entered under template-
_Ancestry SrcInfo, SrcCitation, Person, Access Date -S		ID=10034

fields:
n	SrcInfo
n	SrcCitation
n	Person
n	AccessDate
y	CD

list them-   WHERE SourceTable.Name LIKE 'MR%' AND SurceTable.TemplateID = 10034
the selected sources-
Name
1007       MR Motsinger & Choe m1979 -ANC
1008       MR Motsinger & Wong m1976  -ANC
1195       MR Cho & Tsuji m1948  -ANC
1292       MR Schwab & Reuss m1935  -ANC
1642       MR Och & Kilgus m1887 -ANC
2074       MR Lumsden & Horn m1972 -ANC
2098       MR Kurisu & Nakawaki -ANC
2802       MR Bell & Bernal m1992 -ANC
2803       MR Bell & Barker m1972 -ANC
2922       MR Urcia & Cheung m1990  -ANC
3056       MR Herko & Betner m1905  -ANC
3069       MR Lake & Haberkern m1938 -ANC
4097       MR Bungay & Lake m1950  -ANC
4127       MR Ripberger & Gerding m1963  -ANC
4249       MR Gardner & Hess m1963  -ANC
4302       MR Grant & Green m1900  -ANC
4325       MR Plooster,Roger Dean b1927  -ANC
4549       MR Imai & Takano m1925  -ANC
4654       MR Morris & Lumsden m1936  -ANC
4657       MR Hirely & Ikemoto m1928  -ANC
4819       MR Takagawa & Kinoshita ml 1926  -license -ANC
4831       MR Koike & Yoshima m1918 -ANC






This template was designed without marriage in mind and is missing some fields.
Design a new one

_MR ANC -S			ID=10045
CoupleNames
EventDate
EventType	default is Marriage, or Marriage license
SrcInfo
SrcCitation
AccessDate
CD

	mapping-
oldST		newST

SrcInfo		SrcInfo
SrcCitation	SrcCitation
Person		CoupleNames
AccessDate	AccessDate
NULL		EventDate
NULL		EventType
CD			CD



Sample RM XML
NOTE- when copying from SQLite expert BLOB editor, the leading 3 BOM bytes and line feed 0A byes are copied as periods.

Old style XML
...<?xml version="1.0" encoding="UTF-8"?>.
and an 0A at end of BLOB

==============================================
sample SourceTemplateTable XML
...<?xml version="1.0" encoding="UTF-8"?>.<Root><Fields><Field><FieldName>Compiler</FieldName><DisplayName>Compiler</DisplayName><Type>Name</Type><Hint>name of the original compiler/author (put slashes around multi-part surnames, like /van Durren/.)</Hint><LongHint/><CitationField>True</CitationField></Field><Field><FieldName>FamilyGroup</FieldName><DisplayName>Family Group</DisplayName><Type>Text</Type><Hint>e.g. John Doe-May Smith family group sheet</Hint><LongHint/><CitationField>True</CitationField></Field><Field><FieldName>Type</FieldName><DisplayName>Type</DisplayName><Type>Text</Type><Hint>e.g. undocumented, partially documented, or fully documented</Hint><LongHint/><CitationField>True</CitationField></Field><Field><FieldName>AFNumbers</FieldName><DisplayName>AF numbers</DisplayName><Type>Text</Type><Hint>Ancestral File number(s)</Hint><LongHint>e.g. A5DX-3R and A5DX-S6</LongHint><CitationField>True</CitationField></Field><Field><FieldName>AFVersion</FieldName><DisplayName>AF version</DisplayName><Type>Text</Type><Hint>Ancestral File version, e.g. 4.13</Hint><LongHint/><CitationField>False</CitationField></Field><Field><FieldName>Year</FieldName><DisplayName>Year</DisplayName><Type>Date</Type><Hint>the year of the AF Version, e.g. 1994</Hint><LongHint/><CitationField>False</CitationField></Field></Fields></Root>.

==============================================
sample SourceTable XML
...<?xml version="1.0" encoding="UTF-8"?>.<Root><Fields><Field><Name>Informant</Name><Value>Alban Josef Otter</Value></Field><Field><Name>InterviewDate</Name><Value>1996-10-20</Value></Field><Field><Name>Interviewer</Name><Value>Richard Otter</Value></Field></Fields></Root>.

==============================================
sample CitationTable XML
<Root><Fields><Field><Name>CD</Name><Value>Listed on p2 as &apos;Longin heiratet die Agnes Ludwig aus Waldzell (Maria ihr Eltern!)&apos;</Value></Field></Fields></Root>

==============================================




==================
Odd cases found:
==================

Fix done-
Found an odd Fields value in citationTable.
citationID 101294 had just <root />
<Root> <Fields> </Fields> </Root>

for citations, found one that had no Fields tag.
So when finding them, got None.
If changed <Root /> to one with fields, works.
Do this happen in other places?
maybe do a search for just <Root > in citations.

Fixed by adding a Fields empty element within Root, then continuing.

==================
Fix done:
Caused by same fields value of <Root />
When looking to remove processing instruction element found in old data, was looking for strt or XML by searinging for <Root>, but it wasn't found in this case. So look for "<Root"
==================






=======================================
=======================================



=====================================================
=====================================================
=====================================================

=====================================================




Sample output from test case
Using TEST database

Script output

=====================================================
1007       MR Motsinger & Choe m1979 -ANC
30118     Record states that Donald W Motsinger, age 32, and Inja Choe, age 22 w
30119     Record states that Donald W Motsinger, age 32, and Inja Choe, age 22 w
30120     Record states that Donald W Motsinger, age 32, and Inja Choe, age 22 w
=====================================================
1008       MR Motsinger & Wong m1976  -ANC
30127     Index does not mention the bride.
=====================================================
1195       MR Cho & Tsuji m1948  -ANC
32414     Name: Clara Hiroko Tsuji
Age: 24
Birth Year: abt 1924
Birth Plac
=====================================================
1292       MR Schwab & Reuss m1935  -ANC
33090     Listed as Margert Reuss, age 21, b in Germany, daughter of Friedrich R
33096     Listed as second marriage for Leo. His first wife is deceased.
33097     Lists Leonard Schwab as son of Nicholas Schwab and Mary A. Siekhartner
33101     Lists Leonard Schwabs as son of Nicholas Schwab and Mary A. Siekhartne
33106     Lists Margret Reuss as daughter of Friedrich Reuss and Kunigunde Lips.
=====================================================
1642       MR Och & Kilgus m1887 -ANC
51830     Lists Henry Och and Kilgus married in 1887 in Philadelphia. License #
=====================================================
2074       MR Lumsden & Horn m1972 -ANC
84626
=====================================================
2098       MR Kurisu & Nakawaki -ANC
84779
84782     Listed as 22 yr old in 1958 => b 1935-36
=====================================================
2802       MR Bell & Bernal m1992 -ANC
94220
=====================================================
2803       MR Bell & Barker m1972 -ANC
94240
=====================================================
2922       MR Urcia & Cheung m1990  -ANC
96973
=====================================================
3056       MR Herko & Betner m1905  -ANC
100024
=====================================================
3069       MR Lake & Haberkern m1938 -ANC
100132     Lists Theresa's parents establishing the correct Theresa.
=====================================================
4097       MR Bungay & Lake m1950  -ANC
101294
=====================================================
4127       MR Ripberger & Gerding m1963  -ANC
103484
=====================================================
4249       MR Gardner & Hess m1963  -ANC
104219
=====================================================
4302       MR Grant & Green m1900  -ANC
104533
=====================================================
4325       MR Plooster,Roger Dean b1927  -ANC
104719
=====================================================
4549       MR Imai & Takano m1925  -ANC
105970
105971     Lists parents.
=====================================================
4654       MR Morris & Lumsden m1936  -ANC
106595
106598     Lists parents.
=====================================================
4657       MR Hirely & Ikemoto m1928  -ANC
106615
106617     Lists parents.
=====================================================
4819       MR Takagawa & Kinoshita ml 1926  -license -ANC
107694
107695     Lists parents.
=====================================================
4831       MR Koike & Yoshima m1918 -ANC
107783
107786     Lists parents.
Press any key to continue . . .
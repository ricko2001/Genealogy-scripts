Change the source template used by a source script

Also used when one wants to change the fields of a source template. Instead of editing the template, may be best to copy it, rename it, edit it and then switch the sources using it.


Start with a source or set of sources, all created with he same source template, whose template we want to change.
We need to create a list of these. The select will use the sourceTemplateID as the search criteria. Code also allows a Like test on source name.

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
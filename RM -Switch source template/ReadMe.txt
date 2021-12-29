Change the source template used by a source script

Start with a source that should have its source template changed from oldST to newST
Presume that not all sources with the oldST should be chagned, so first need
to select the group of sources based on source name. Confirm that all selected sources have the same oldST.


all three have XML data-
SourceTemplateTable		FieldDefs
SourceTable				Fields
CitationTable			Fields


OLD DATA =========================
old source template		oldST
old source				oldSRC
old citations			oldCITn

OLD DATA =========================


NEW DATA =========================
new source template		newST
new source				newSRC
new citations.			newCITn

NEW DATA =========================

Have list of fields in oldST and list of fields in newST
need to compare the 2.
create an option to list the fields in old and new and print out so 
they can be copied and placed in a config file to do the mapping.

once mapping is determined-
for each source
  change the field names in the source to match the field names in the newST.
  for each citation to the source
     change the field name in the citation to match the newST and newSRC


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

How to do mapping of fields

First test case
split MR records entered under template-
_Ancestry SrcInfo, SrcCitation, Person, Access Date -S		ID=10034
SrcInfo
SrcCitation
Person
AccessDate
CD

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


citationID 101294 had just <root />
<Root> <Fields> </Fields> </Root>
Adding and removing is wrking- more testing-
for citations, found one that had no Fields tag.
Go when finding them, got None.
If changed <Root /> to one with fields, works.
Do this happen in other places?
maye do a search for just roort in citations.
Can it be fixed by going to the citation in RM app and adding a value?




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


CONVERSION PLAN

This plan assumes that no information in existing citations need to be preserved- except the link to the uses of the citation.

Media items and Web Links attached to an old source will be moved to 
the citation (that points to the new master source)

The fields in the 2 new master sources are filled in manually.
It's the fields in the citations that will be filled in by script.

=citation=
new citation field          old source field

CitationName                SourceTable.Name
Name                        parse data
BirthDate                   parse data
SSN                         parse data
SSDate                      parse data
AccessDate                  AccessDate
AccessType                  NULL
ParentsInfo                 yes for SSACI when Father is found. NULL for SSDI

ResearchNote                SourceText
DetailComment               SourceComment

UTCmodDate                  UTCModDate

=======================================
=======================================


==============================================
CONVERSION Process
Assume that future uses may deal more with moving data from custom fields to new custom fields.
The SS data is so easy to parse, use it instead.

have an old srcID and new srcID what next

check how many citations linked to oldSrcID.
skip if 0 
(its not used. figure out what to do with it later)

get info from oldSrc	XML and Std fields

Move each citation to under the old source to the  newSrcID
fill it in with old info	XML and Std fields
Also move the UTCModDate field from old source to citation.

This will change when other sources are lumped but makes sense for the SSDI specific conversion

After an old src is processed, delete it.(it should have 0 citations 
and web links, because they should have been moved already.)


=====================================================

In this case,
multiple citations to old source will create multiple identical citations to new source.
Run Merge Identical Citations command in RM.

When web tags from src to moved citation to first citation but not second and following citations. They don't "get copies" until the merge is done in RM.

check number of citation uses to check for proper use missing and duplicates for improvements

=====================================================
=====================================================
=====================================================
new, empty database created with 8.1.3 does not have the old style XML BOM or XML processing line.

=====================================================

List source templates by the number of uses

SELECT stt.Name, st.TemplateID, COUNT(st.TemplateID)
FROM SourceTemplateTable stt
JOIN SourceTable st ON  stt.TemplateID = st.TemplateID
GROUP BY stt.TemplateID
order by COUNT(st.TemplateID) desc

Name	TemplateID	COUNT(st.TemplateID)
_Title and Date	10023	1120
_Census: US Federal Population Schedules -1850-1940 -S	10026	259
_Passenger Lists, Ancestry	10043	139
_TMG_Interview-family	10001	122
_Obituary: Newspapers.com -S	10037	110
_Ancestry Database-Single -L	10036	107
_Ancestry SrcInfo, SrcCitation, Person, Access Date -S	10034	93
_Obituary - OnLine -S	10038	49
_Ancestry Database-Double (marriage) -L	10041	40
_TMG_Photograph (Private Possession) (Annotated with Provenance)	10025	37
_Census: US State -L	10030	22
_Marriage Announcement: Newspapers.com -S	10039	17
_TMG_Book (Authored)	10014	13
_SSDI: Ancestry.com	10008	11
_TMG_Letter (Annotated Citation)	10009	10
_SSACI-Ancestry	10033	9
_Obituary: GenealogyBank.com -S	10040	7
_TMG_Death Registration (State Level)	10011	6
_TMG_Birth Registration (Local Level)	10006	6
_TMG_Personal Knowledge	10000	6
_TMG_E-Mail Message	10022	4
_TMG_Family Group Sheet (with Annotation)	10007	4
_TMG_Research Report	10005	3
_Social Security Data -L	10044	2
_TMG_Periodical (Issued in Multiple Series)	10024	2
_TMG_Interview	10015	2
_Obituary/Newspaper item (Copy)	10035	1
_TMG_Town Record	10032	1
_TMG_Article (Serialized; Annotated Citation)	10031	1
_TMG_Electronic Web Site	10028	1
_TMG_Cemetery Marker	10027	1
_TMG_Guess-Person	10021	1
_TMG_Guess-Place	10020	1
_TMG_Guess-Calc date	10019	1
_TMG_Research Report-short	10017	1
_TMG_Book (Multi-Volume)	10016	1
_TMG_Book (Edited)	10013	1
_Social Security Account Application	10012	1
_TMG_Birth Registration (State Level)	10004	1
Website "as book"	197	1

=====================================================






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
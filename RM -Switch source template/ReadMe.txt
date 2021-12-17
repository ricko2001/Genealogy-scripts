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
<Field>
<FieldName>name</FieldName>
<DisplayName>Compiler</DisplayName>
<Type>Name</Type>
<Hint>name of the original compiler/author (put slashen/.)</Hint>
<LongHint/>
<CitationField>True</CitationField>
</Field>


How to do mapping of fields



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
=====================================================
=====================================================







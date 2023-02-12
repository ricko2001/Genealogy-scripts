Un-split source script

Start with a specific group of sources. Might generalize it later, if desired.

Currently handles 1 set of sources in my database-
Find a Grave  "GSFG" sources.  Have lots of them.

The existing multitude of GSFG sources were created with the "free form" template 
described immediately below as OLD DATA.

OLD DATA =========================
old source template		_SSDI:Ancestry.com				TemplateID=10008
old source				many, each source name in the form:  SSDI Lname,Fname bYYYY
Each source had multiple citations. 
has 4 custom fields

=master source=
FileNumber
Subject
AccessDate

=citation=
CD


OLD DATA =========================
old source template		_SSACI-Ancestry					TemplateID=10033
old source				many, each source name in the form:  SSACI Lname,Fname bYYYY
has 4 custom fields

=master source=
FileNumber
Subject
AccessDate

=citation=
CD


NEW DATA =========================
new source template     _Social Security Data
has 13 custom fields

=master source=
Owner
WebsiteTitle
URL
DatabaseName
DataType
DbInfoDate

=citation=
Name
BirthDate
SSN
SSDate
AccessDate
Acesstype
ParentsInfo

==============================================
It was decided to create one source template that would be the basis of all and onlt FaG data.
A new template was created- " _Find-a-Grave"



New Data will consist of citations to a new Master Source.
One Master Source will be for GSFG records.

new sources
FindaGrave_db		ID 6276			


==============================================
CONVERSION PLAN

This plan assumes that
the Footnote in existing citations will be preserved
media links will be moved
source citation web link will be a citation web link
all uses of the source will get moved to the new citation

Need to check data to confirm that all existing sources have just one citation.




The fields in the 2 new master sources are filled in manually.
It's the fields in the citations that will be filled in by script.

=citation=
new citation field          old source field

Name                       parse data
DateBirth                  parse data
PlaceBurial                parse data
PlaceCemetery              parse data
EntryNumber                parse data
CD                          ????
Transcription              NULL
DateCitation               parse data
SrcCitation                footnote
UTCmodDate                  UTCModDate



ResearchNote                SourceText
DetailComment               SourceComment



=======================================
=======================================

in original source Fields  eg SourceID 6272


rowid	SourceID	Name	RefNumber	ActualText	Comments	IsPrivate	TemplateID	Fields	UTCModDate
6272	6272	GSFG Boland, Terry P -b1957		[INVALID_DATA]		1	0	[BLOB_DATA]	44967.2476061806

RowTable
	rowid
	SourceID
	Name
	RefNumber
	ActualText
	Comments
	IsPrivate
	TemplateID
	Fields
	UTCModDate


CitationTable
	rowid
	CitationID
	SourceID
	Comments
	ActualText
	RefNumber
	Footnote
	ShortFootnote
	Bibliography
	Fields
	UTCModDate
	CitationName



<Root><Fields>
<Field><Name>Footnote</Name>
<Value>
Find a Grave, database and images (https://www.findagrave.com/memorial/30357596/terry-p-boland: accessed 9 February 2023), memorial page for Terry P Boland (5 Jan 1957...26 Jun 2005), Find a Grave Memorial ID 30357596, citing Calvary Cemetery, Terre Haute, Vigo County, Indiana, USA; Maintained by Wabash Valley Genealogy Society Cemetery Committee (contributor 46834757).
</Value></Field>

<Field><Name>ShortFootnote</Name>
<Value>
Find a Grave, database and images (https://www.findagrave.com/memorial/30357596/terry-p-boland: accessed 9 February 2023), memorial page for Terry P Boland (5 Jan 1957...26 Jun 2005), Find a Grave Memorial ID 30357596, citing Calvary Cemetery, Terre Haute, Vigo County, Indiana, USA; Maintained by Wabash Valley Genealogy Society Cemetery Committee (contributor 46834757).
</Value></Field>

<Field><Name>Bibliography</Name>
<Value>
</Value></Field>
</Fields></Root>


Find a Grave, database and images (https://www.findagrave.com/memorial/30357596/terry-p-boland: accessed 9 February 2023), memorial page for Terry P Boland (5 Jan 1957...26 Jun 2005), Find a Grave Memorial ID 30357596, citing Calvary Cemetery, Terre Haute, Vigo County, Indiana, USA; Maintained by Wabash Valley Genealogy Society Cemetery Committee (contributor 46834757).

Find a Grave, database and images (https://www.findagrave.com/memorial/30357596/terry-p-boland: accessed 9 February 2023), memorial page for Terry P Boland (5 Jan 1957...26 Jun 2005), Find a Grave Memorial ID 30357596, citing Calvary Cemetery, Terre Haute, Vigo County, Indiana, USA; Maintained by Wabash Valley Genealogy Society Cemetery Committee (contributor 46834757).

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
typical record-  SSACI

Name:	Hilda Sauer
[Hilda Stamm]
Gender:	Female
Race:	White
Birth Date:	6 Oct 1900
Birth Place:	Hausen, Federal Republic of Germany
Death Date:	13 Apr 1998
Father:	John Stamm
Mother:	Josepha Stamm
SSN:	061525080
Notes:	28 Aug 1972: Name listed as HILDA SAUER

=====================================================
typical record-  SSDI

Name: Charles Auzout
Social Security Number: 433-05-9371
Birth Date: 21 Nov 1896
Issue Year: Before 1951
Issue State: Louisiana
Last Residence: 70117, New Orleans, Orleans, Louisiana, USA
Death Date: Jul 1971

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







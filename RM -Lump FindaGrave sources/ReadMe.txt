Un-split source script

Start with a specific group of sources. Might generalize it later, if desired.

Currently handles 1 set of sources in my database-
Find a Grave  "GSFG" sources.  Have lots of them.

The existing multitude of GSFG sources were created with the "free form" template 
described immediately below as OLD DATA.

OLD DATA =========================
old source template		FreeForm			TemplateID=0
old source				many, each source name in the form:  GSFG LN, FN <bdate>

Each source had multiple citations. Most have one, some 0.



NEW DATA =========================
new source template     _Find-a-Grave
It was decided to create one source template that would be the basis of only FaG data.

New Data will consist of citations to a new Master Source.
One Master Source will be for GSFG records.

new source
FindaGrave_db		ID 6276


==============================================
CONVERSION PLAN

This plan assumes that
the Footnote in existing citations will be preserved
media links will be moved
source citation web link will be a citation web link
all uses of the source will get moved to the new citation



The fields in the 2 new master sources are filled in manually.
It's the fields in the citations that will be filled in by script.

=citation=
new citation field          old source field

Name                       parse data
DateBirth                  parse data
PlaceBurial                parse data
PlaceCemetery              parse data
EntryNumber                parse data
CD                         Page data from citation XML
Transcription              NULL   manual update
DateCitation               parse data
SrcCitation                footnote from old citation
UTCmodDate                 UTCModDate from old citation


ResearchNote                SourceText
DetailComment               SourceComment
Media links                 from source (existing on citation preserved)
Web links                   from source (existing on citation preserved)


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

have an old srcID and new srcID what next

check how many citations linked to oldSrcID.
skip if 0 

(its not used. figure out what to do with it later)

get info from oldSrc	XML and SourceTable fields

Move each citation under the old source to the  newSrcID
fill it in with old info	XML and Std fields
Also move the UTCModDate field from old source to citation.


After an old src is processed, delete it.(it should have 0 citations 
and web links and media links, because they should have been moved already.)


=====================================================

In this case,
multiple citations to old source will create multiple identical citations to new source.
They will usually have different CD data.

***
When web tags from src to moved citation to first citation but not second and following citations. They don't "get copies" until the merge is done in RM.
***

check number of citation uses to check for proper use missing and duplicates for improvements

=====================================================
=====================================================
=====================================================
=====================================================
=====================================================







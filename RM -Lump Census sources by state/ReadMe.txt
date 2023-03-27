Un-split source script

Start with a specific group of sources. Might generalize it later, if desired.

Currently handles 1 set of sources in my database-
C_1950 SS
where SS is the state abbreviation

The existing multitude of GSFG sources were created with the "_Census:  RETIRED   do not use -S" template 
described immediately below as OLD DATA.

TODO Check this
Each source had multiple citations. Most have one, some 0.
if 0 citations, thenthe code would need to create one, becasue it currently moves existing citations only.


OLD DATA =========================
_Census:  RETIRED   do not use -S
ID=10026

	[Household]				Household				Text
	[BirthDateHead]			Head's birth date		Date
	[Place]					Place					Place
	[Location]				Location				Text
	[County]				County					Text
	[State]					State					Text
	[HouseNumber]			HouseNumber				Text
	[Street]				Street					Text
	[FilmNumber]			Film Number				Text
	[Page]					Page					Text
	[EnumerationDistrict]	Enumeration District	Text
	[Dwelling]				Dwelling				Text
	[Family]				Family					Text
	[FS]					ANC Citation			Text
	[CD]					Citation Detail			Text
	[CitationDateUpdated]	CitationDateUpdated		Date
	[ANC_RID]				Ancestry Rec ID			Text





NEW DATA ========================= ID=
_Census: New census template -L (by year-state)
ID=10054
	[PlaceState]			US State						Text		State or Territory	
	[DateSource]			Date Source updated				Date			
	[Household]				Household Head					Text	X		X
	[DateHeadBirth]			Head's birth date				Date	X	for identification	X
	[DateSheet]				Date on Sheet					Date	X	Date census was taken for this household	
	[PlaceFull]				Place -full						Place	X	databasef format	X
	[PlaceLocality]			Locality						Text	X		
	[PlaceCounty]			County							Text	X		
	[PlaceStreet]			Street name						Text	X		
	[PlaceHouseNumber]		House Number					Text	X		
	[EnumerationDistrict]	Enumeration Dist				Text	X		
	[SheetLineNumber]		Sheet Line						Text	X	Sheet, line range	X
	[DwellingSN]			Dwelling SN						Text	X	Dwelling Serial Number	X
	[FilmRollNumber]		Film Roll Number				Text	X	NARA Product # _ Roll #	X
	[ANC_SRC_ID]			Ancestry source ID				Text	X		X
	[FS_SRC_ID]				FamilySearch Src ID				Text	X		X
	[DateCitation]			Date Citation					Date	X	Date Citation Updated or created	
	[CD]					Citation Detail					Text	X		

New data will be citations attached to a previously created source

old template= ID=10026   retired
new template ID=10054     new census 1950

new source ID=6290    CenFEDdb 1950 Hawaii


maybe add place details   House number Street

It was decided to create one source template that would be the basis 
census sources that are lumped by state

Not yet clear is one source will be for either or both ancestry ad FS.
Ancestry- citation, index info, web link, image
FS- citation, index info, web link, image
YES- one source will handle both. 
make the source have info just about the census in abstract
citation will have a field for ANC id and FS ID
can have 2 media files attached,
Research note can have multiple index info along with RJO Transcription.

Film number- NAR or FS ?
for 1950, use T1234_1234

Source Text
Source Comment
Research Note
Detail Comment

So specific ANC of FS details in the template. That info goes into Research Note.
Like before.

Record Type is almost always Population schedule

don't bother with repositories. That can be done late as there won't be that many sources/
move from source to citation- media and web tag and citations

==============================================
CONVERSION PLAN

This plan assumes that
the Source info  will be preserved and moved to citation research 
media links will be moved
source citation web link will be a citation web link
all uses of the source will get moved to the new citation



The fields in the new master sources are filled in manually when the source is created.
It's the fields in the citations that will be filled in by script.

=citation=
new citation field          old source field




ResearchNote                SourceText
DetailComment               SourceComment
Media links                 from source (existing on citation preserved)
Web links                   from source (existing on citation preserved)


=======================================
=======================================

in original source Fields  eg SourceID 6272


SourceTable
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



==============================================
CONVERSION Process
Assume that future uses may deal more with moving data from custom fields to new custom fields.

have an old srcID and new srcID what next

check how many citations linked to oldSrcID.
skip if 0 (is this necessary?)
(its not used. figure out what to do with it later)

get info from oldSrc	XML and SourceTable fields

Move each citation under the old source to the  newSrcID
fill it in with old info	XML and Std fields
Also move the UTCModDate field from old source to citation.


After an old src is processed, delete it.(it should have 0 citations 
and web links and media links, because they should have been moved already.)


=====================================================

In this case,
multiple citations to old source will create multiple citations to new source.
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







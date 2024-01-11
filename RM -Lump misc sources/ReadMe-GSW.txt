

Un-split source script

Start with a specific group of sources. Might generalize it later, if desired.

Analyze what the sources have, what the citations have and what needs to preserved.


Currently handles 1 set of sources in my database-
Marriage Record - Lohr   "GS Waldzell" sources.  
Have about 80 of them.
several have 2 citations
	GS Waldzell, plot 2022-1-2-01, -Schubert
about 15 have 0 citations
	GS Waldzell, plot 2022-1-3-04 -Geier; Kreser -unlinked
	GS Waldzell, plot 2022-1-2-05 -Röder -unlinked
	GS Waldzell, plot 2022-1-W-02 -Loschert -unlinked

The multiple citations are important


most have 1 citation which has the previous CD's all in the citation comment should that go in source comment ??



OLD DATA =========================
old source template		ID=10051	_Friedhof_BurialPlot
old source				many, each source name in the form:  GS Waldzell%

Each source had multiple citations. Most have one, some 0.
the ones with multiple citations had CD items. These CD items were all put into the - citation Detail comment.



NEW DATA =========================
new source template		ID=		name
Will create a source template that will be the basis of all Cemetery gravestone sources.



==============================================

OLD Template
	Source Name
	[FriedhofName]	FriedhofName	Text
	[FriedhofPlace]	FriedhofPlace	Place
	[PlotID]		PlotID			Text
	[DateSource]	DateSource		Date
	Source Text
	Source Comment
	Media
	WebTags
=============
	Citation Name
	[DateMarker]	DateMarker		Date	X
	[FamilyNames]	FamilyNames		Text	X
	[DateCitation]	DateCitation	Date	X
	Research Note
	Detail Comment
	media
	WebTags



OLD Template	what data do sources have
	Source Name		plot name & family name  - both in fields
	[FriedhofName]	FriedhofName	Text	goes to source
	[FriedhofPlace]	FriedhofPlace	Place	goes to source
	[PlotID]		PlotID			Text	goes to cit
	[DateSource]	DateSource		Date	goes to source
	Source Text								empty
	Source Comment							misc comments text ??
	Media									plot photos and grave file
	WebTags									NONE
=============
	Citation Name									auto
	[DateMarker]	DateMarker		Date	X		to cit
	[FamilyNames]	FamilyNames		Text	X		to cit
	[DateCitation]	DateCitation	Date	X		to cit
	Research Note									empty
	Detail Comment									empty
	media											NONE
	WebTags											NONE



NEW Template
	[FriedhofName]	FriedhofName	Text
	[FriedhofPlace]	FriedhofPlace	Place
	[DateSource]	DateSource		Date
=============
	[PlotID]		PlotID			Text	X
	[DateMarker]	DateMarker		Date	X
	[FamilyNames]	FamilyNames		Text	X
	[DateCitation]	DateCitation	Date	X



source is for entire cemetery
has almost no info, just name & location descriotion.
Citation will be to grave plot and person name

the grave plot file & images would be the same for all the different citations that had diff names but same plot.
Since citations would be copied (not reused) would want updateable info- plot history- to be in sep file, not in the citation, otherwise, would have to keep multiple citations in sync when plot info changed.





Should the cemetery be the repository ?



note-
web links and media attached to old source citations are lost. (there are none)
Actually- is this true? Not checked. If there were any, they should be carried over after the citation is moved.
Text in Citation Note fields- Research note and Research comment (?) are not preserved.


==============================================
CONVERSION PLAN

This plan assumes that no information in existing citations need to be preserved- except the link to the uses of the citation.

Media items and Web Links attached to an old source will be moved to 
the citation (that points to the new master source)

The fields in the new master source are filled in manually.
It's the fields in the citations that will be filled in by script.

=======================================
=======================================


==============================================
CONVERSION Process
Assume that future uses may deal more with moving data from custom fields to new custom fields.


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



Confirmed all old sources have 1 cit each
(if they had 0, added a sample citation.)
confirmed all old source have one - that has no research note or comment or media or web link
only has name = -
and citations used

backup after all done 21:5X



Un-split source script

Start with a specific group of sources. Might generalize it later, if desired.

Currently handles 1 set of sources in my database-
Marriage Record - Lohr   "MR-L" sources.  
Have 31 of them.
none have more than 1 citation 
4 have 0 citations

most have 1 citation which has the previous CD's all in the citation comment should that go in source comment ??



OLD DATA =========================
old source template		_Title, Date; Name [etc]			TemplateID=10023
old source				many, each source name in the form:  MR-L

Each source had multiple citations. Most have one, some 0.
the ones with multiple citations had CD items. These CD items were all put into the - citation Detail comment.



NEW DATA =========================
new source template			__MR-Lohr		ID=10059
It was decided to create one source template that would be the basis of only MR-L data.

New Data will consist of citations to a new Master Source.
One Master Source will be for all MR-L records.

new source
MRdb-Lohr, Bayern		ID=6643



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

New Data will consist of citations to a new Master Source.
Only the fields need to be finalized now. Source sentence can follow later.

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

Old Template
	[Title]	Title	Text
	[Date]	Date Source last updated	Date
========
	[Person]	Person	Name	X
	[BDate]	Birth Date	Date	X
	[CD]	Citation Detail	Text	X
	[CitationDate]	Date Citation last updated	Date	X


New Template
	[Title]	Title	Text
	[Authors]	Authors	Text
	[Publication]	Publication	Text
	[Date]	Last DB info update	Date
========
	[Name]	Couple surnames	Text	X
	[EventDate]	Event date	Date	X
	[EnrtyNumber]	EnrtyNumber  SAW	Text	X
	[CallNumber]	CallNumber	Text	X
	[ImageNumbers]	ImageNumbers	Text	X
	[CD]	Citation Detail	Text	X
	[DateCitation]	Date citation updated	Date	X







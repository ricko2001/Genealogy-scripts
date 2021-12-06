Un-split source script

Start with a specific group of sources. Might generalize it later, if desired.

Currently handles 2 sets of sources in my database-
SSDI and SSACI sources.  Have lots of them.

The existing multitude of SSDI and SSACI sources were created with the templates 
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
It was decided to create one source template that would be the basis of SSDI and SSACI data
from possibly multiple on-line sources.
A new template was created- " _Social Security Data"

Note that the new template does not have a CitationDetail field in the citation section.
My old style used the CitationDetail field to explain what data in the source is being cited 
and why the source was attached.

Instead, explain why its attached in a narrative research summary for each fact, not in 
the source or citation. No need to cite the data since the the transcription of the data is so small.


New Data will consist of citations to a new Master Source.
One Master Source will be for SSDI records in Ancestry, the other SSACI records in Ancestry.
These are both created with the new Source Template "_Social Security Data" described above.
Only the fields need to be finalized now. Source sentence can follow later.

new sources
SSACIdb ANC US		ID 5502			has "sample citation"
SSDIdb ANC US		ID 5503			has "sample citation"

note-
web links and media attached to old source citations are lost. (there are none)
Actually- is this true? Not checked. If there were any, they should be carried over after the citation is moved.
Text in Citation Note fields- Research note and Research comment (?) are not preserved.


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







Un-split source scripts

Start with a specific group of sources. Can generalize it later, if desired.

Start with SSDI sources.
Have lots of them.

Go thru them looking for srcs that have more than one citation.
Usually they can be merged into a blank citation. There was never much value in repeating info
from the source in the source detail field and have it print.
This was not necessary. Now move them all and then merge.
It was useful to cofirm that citations to old source has no info to be saved.


OLD DATA =========================
old source template     _SSDI:Ancestry.com      TemplateID=10008
old source              mnay

has 4 custom fields=
FileNumber
Subject
AccessDate

=citation=
CD


STANDARD FIELDS=

Source Name

Source Text
Source Comment

Media
Repositories
Web Tags
Used
UTCmodDate		

=citation=
Research Note
Detail Comment

Media
WebTags
cit Used

Quality
  Source
  Information
  Evidence



NEW DATA =========================
new source template     _Docial Security Data
new source              ID 5503             has "sample citation"

has 13 custom fields=
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

 =========================
 CONVERSION PLAN

 The fields in the new source are filled in manually
 It's the fields in the citations that will be filled in by script.

=ALL SRC FIELDS=
Source Name	    SSDIdb ANC US
Owner
WebsiteTitle	
URL				
DatabaseName	Ancestry database name for SSDI
DataType		SSDI or SSACI
DbInfoDate		when source was updated

Source Text		full info about database		CitationTable.ActualText	=	SourceTable.ActualText
SourceComment	

Media			NULL
Repositories	Ancestry repo
Web Tags		URL of ancestry database
Used			<output>

=ALL CITATION FIELDS=
new citation field          old source field
CitationName                SourceTable.Name
Name                        parse data
BirthDate                   parse data
SSN                         parse data
SSDate                      parse data
AccessDate                  AccessDate
AccessType                  NULL
ParentsInfo                 NULL

ResearchNote                SourceText
DetailComment               SourceComment
UTCmodDate                  UTCModDate



=======================================

Create a source form the template
SSDIdb ANC US
Create a citation (empty, no uses) name it ""sample citation""

=======================================

Conversion process

Figure out which group of sources will be lumped.
do a select based on name and templateID 

Get the SourceID of the source to get citations
Let's assume all CD fields are blank and there is no citation in old source. This is true for this first implementation.

Fill in its 
Citation Name = SourceName
Name		Name
BirthDate	get it from SSDI
SSN 		get it from SSDI
SSDate		get it from SSDI
CitationDate	copy from old Src
AccessType		"downloaded"

need to deal with XML fields

have an old srcID and new srcID what next

check how many citations linked to oldSrcID. stop if >1, skip if 0

get info from oldSrc	XML

Move the citation to newSrcID
fill it in with old info	XML



if old source has more than one citation stop
or has 0 citations, skip it
This will change when other sources are lumped but makes sense for the SSDI specific conversion

After an old src is processed, delete it.(it should have 0 citations 
and web links, becasue they should have been changed already.)

All citation records are trimmed.
All source records that have been modofed in RM8 and have a UTCModDate, are trimmed.




Parsing of SS data is a bit complicated
2 forms of data, old has SSN, new has Social Scurity Number.
New is predominant.
Change all to new format and make sure all have a web tag

ancestry pasting-
each line has a 0d 0a, as expected.


check number of citations for improvements



SSACI lumping-
deal with most have 2 citation- blank and Lists parents, lists father etc
remove limitations and handle each citation

=====================================================
typical recod-

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
=====================================================
old source template     _SSACI-Ancestry     TemplateID=10033
old source              mnany

has 4 custom fields
FileNumber
Subject
AccessDate

=citation=
CD

=====================================================
new source template     _Social Security Data
new source              ID 5503     has "sample citation"


has 13 custom fields=
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
=====================================================
=====================================================

decission- do not include a CD firld in new source template
for ssaci, the CD was used to indicate "lists parets" etc so that when a child's SSACI source
was attached to a parent "person", one could see in the source list why.
Instead, use the Evience "tag" in the Note for a fact to summarize evidence.
Leave the existing data as is, when lumped, it won't have a CD to distinguis the citations. They can then be merged by RM.

=====================================================


  SSDI      searchStrings = ['Name:\t', 'Social Security Number:\t', 'Birth Date:\t', 'Issue Year:\t' ]
  SSACI     searchStrings = ['Name:\t', 'Birth Date:\t', 'Father:\t', 'SSN:\t' ]
=====================================================

Fill in new citation fields
=custom fields=
Name			parse data
BirthDate		parse data
SSN			    parse data
SSDate			NULL
AccessDate	=	AccessDate
AccessType		NULL
ParentsInfo     set to yes if Father is found

=standard fields=
CitationName	    SourceTable.Name
ResearchNote		SourceText
DetailComment		SourceComment
UTCmodDate			UTCModDate	

media           done & tested
citation use    done & tested
web links       done & tested

=====================================================


note web links and media cattached to old source  citations are lost.


Figure out text parsing of actualText field.

Nice to have- add dashes to SSN in SSN field

=====================================================
=====================================================



move web tags from src to moved citation- but what about second and following citations. They don'e get copies.
But they will after merge of dup citations at end.


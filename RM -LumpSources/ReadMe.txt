Un-split source scripts

Start with a specific group of sources. Can generalize it later, if desired.

Start with SSDI sources.
Have lots of them.

Go thru them looking for srcs that have more than one citation.
Usually they can be merged into a blank citation. There was never much value in repeating info
from the source in the source detail field and have it print.

OLD DATA =========================
Source template is _SSDI: Ancestry.com

has 4 custom fields=
FileNumber
Subject
AccessDate

=citation=
CD

ALL FIELDS=

Source Name
File Number
Subject
AccessDate

Source Text
Source Comment

Media
Repositories
Web Tags
Used
UTCmodDate		

In citation
Research Note
Detail Comment

Media
WebTags
cit Used

Quality
Source
Information
Evidence


=========================


start with a SSDIdb source

New source Template
Make it specific for SSDI or SSACI

So use it to create 2 sources- SSDI Ancestry and SSACI Ancestry


NEW DATA =========================
Source template is _SSDI: Ancestry.com

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


ALL FIELDS=

Source Name	    
Owner
WebsiteTitle	
URL				
DatabaseName	Ancestry database name for SSDI
DataType		SSDI or SSACI
DbInfoDate		when source was updated

Source Text		full info about database		CitationTable.ActualText	=	SourceTable.ActualText
SourceComment									SourceTable.Comments			SourceTable.Comments

Media			NULL
Repositories	Ancestry repo
Web Tags		URL of ancestry database
Used			<output>

In citation
CitationName	SourceTable.Name
Name			parse data
BirthDate		parse data
SSN			parse data
SSDate			parse data
AccessDate	=	AccessDate
AccessType		NULL
ParentsInfo     NULL

ResearchNote	=	SourceText
DetailComment	=	SourceComment
UTCmodDate		=	UTCModDate	

Research Note	full listing of record
Detail Comment	any notes relating to src

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
sometimes there is a DC4 (char 20) char before value in table instead of tab.
(when pasting to notepad, it is converted to a space.
In older formats, there is a 20 char before and after value.

each line has a 0d 0a, as expected.


check number of citations for improvements



SSACI lumping-
deal with most have 2 citation- blank and Lists parents, lists father etc


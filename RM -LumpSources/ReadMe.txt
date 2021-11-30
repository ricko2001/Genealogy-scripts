Un-split source scripts

Start with a specific group of sources. Can generalize it later, if desired.

Start with SSDI sources.
Have lots of them.

Can go thru them looking for srcs that have more than one citation.
Usually they can be merged into a blank citation. There was never much value in repeating info
from the source in the source detail field and have it print.

Source template is _SSDI: Ancestry.com
has fields-
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

start with a SSDIdb source
One exists, but should be updated to include more fields.
New source Template
Make it specific for SSDI and SSACI
So use it to create 2 sources- SSDI and SSACI
assume that the data will come from ancestry

Source Name		SSDIdb ANC US
DataType		SSDI or SSACI
Owner
WebsiteTitle
URL
DatabaseName	Ancestyr database name for SSDI
Access Date		when source was updated

Source Text		full info about database
Source Comment

Media			NULL
Repositories	Ancestry repo
Web Tags		URL of ancestry database
Used			<output>

In citation
Name
BirthDate
Number
SSDate		
CitationDate
AccessType


Research Note	full listing of record
Detail Comment	any notes relating to src


=======================================
Conversion process

Figure out which group of sources will be lumped.
do a select based on name and templateID 

Get the SourceID of the source to get citations
Let's assume all CD fields are blank and there is no citation in old source.

Fill in its 
Citation Name = SourceName
Name		Name
BirthDate	get it from SSDI
Number		get it from SSDI
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
and web links, becasue they should have been chnaged already.)

Deal with Issue state- can be railroad worker-  e.g. SSDI Centron, Michael b1918

How does the source I created handle different web site sources??
each website would need a diff source, but with same template.

WOULD BE NICE TO HAVE A FIELD FOR SSACI THAT INDICATE LSTING OF PARENTS.

Citation table 
<Root><Fields><Field><Name>CD</Name><Value></Value></Field></Fields></Root>

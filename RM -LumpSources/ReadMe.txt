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

Source Name	=	SSDIdb ANC US
Owner
WebsiteTitle	
URL				
DatabaseName	Ancestyr database name for SSDI
DataType		SSDI or SSACI
DbInfoDate		when source was updated

Source Text		full info about database		CitationTable.ActualText	=	SourceTable.ActualText
SourceComment									SourceTable.Comments			SourceTable.Comments

Media			NULL
Repositories	Ancestry repo
Web Tags		URL of ancestry database
Used			<output>

In citation
CitationName	=	SourceTable.Name		done
Name			parse data
BirthDate		parse data
Number			parse data
SSDate			parse data
AccessDate	=	AccessDate
AccessType		NULL

ResearchNote	=	SourceText
DetailComment	=	SourceComment
UTCmodDate		=	UTCModDate			done

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

All citation records are trimmed.
All source records that have been modofed in RM8 and have a UTCModDate, are trimmed.


Citation table 
<Root><Fields><Field><Name>CD</Name><Value></Value></Field></Fields></Root>


Src table Fields
..<?xml version="1.0" encoding="UTF-8"?>.
<Root>
<Fields>
<Field><Name>Title</Name><Value>Dharma Treasures- Spiritual Insights from Hawaii&apos;s Shin Buddhist Pioneers.</Value></Field>
<Field><Name>ShortTitle</Name><Value>Dharma Treasures</Value></Field>
<Field><Name>Author</Name><Value>Tatsuo Muneto</Value></Field>
<Field><Name>PublishDate</Name><Value>1997</Value></Field>
<Field><Name>Publisher</Name><Value>Bhuddist Study Center Press</Value></Field>
<Field><Name>PublisherAddress</Name><Value>Honpa Hongwanji Mission, 1727 Pali Highway, Honolulu, HI 96813</Value></Field>
<Field><Name>CD</Name><Value/></Field>
</Fields>
</Root>.



Citation Table Fields
<Root>
<Fields>
    <Field><Name>Name</Name><Value>Martin Schwarz</Value></Field>
    <Field><Name>BirthDate</Name><Value>1878</Value></Field>
    <Field><Name>EventDate</Name><Value>25 January 1957</Value></Field>
    <Field><Name>CD</Name><Value></Value></Field>
    <Field><Name>DateCitation</Name><Value>27 November 2021</Value></Field>
    <Field><Name>SrcCitation </Name><Value>The Miami Herald; Publication Date: 25 Jan 1957; Publication Place: Miami, Florida, USA; URL: https://www.newspapers.com/image/618738175/?article=b76ae0bb-94df-496e-b292-46dfa83381e9&amp;focus=0.14746958,0.2750365,0.26154417,0.4597442&amp;xid=3355</Value></Field>
</Fields>
</Root>


    root = ET.fromstring(srcFieldsStr)
    root.find("Field")


    new citation

<Root>
<Fields>
 <Field><Name>BirthDate</Name><Value></Value></Field>
 <Field><Name>Number</Name><Value></Value></Field>
 <Field><Name>SSDate</Name><Value></Value></Field>
 <Field><Name>CitationDate</Name><Value></Value></Field>
 <Field><Name>AccessType</Name><Value></Value></Field>
</Fields>
</Root>


Name		Name
BirthDate	get it from SSDI
Number		get it from SSDI
SSDate		get it from SSDI
CitationDate	copy from old Src
AccessType		"downloaded"
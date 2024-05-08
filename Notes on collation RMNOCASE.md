# Note on the Collation RMNOCASE

SQLite needs the ability to sort data. It does so by comparing two items and determining if they are equal, less than or greater than by using a collation function.\
A summary can be found at:
[sqlite-collating-function-or-sequence](https://www.w3resource.com/sqlite/sqlite-collating-function-or-sequence.php)

RMNOCASE is the name of a collation used by the RM schema for columns that represent names. If you look at the listings at the end of this doc, you'll see that the name columns in the NameTable and SourceTable are ordered by RMNOCASE. Many other names also use the same collation. 

Collations specified in the table declaration are the default collations for any index created using that column.

RMNOCASE is designed to sort upper and lower case names together (not tested by me) like SQLite's builtin NOCASE collation.
NOCASE does this for the 26 letters of the latin alphabet, but not for accented characters found, for example, in European languages. RMNOCASE also sorts upper and lower case accented characters together.

RMNOCASE is not part of SQLite. It's a piece of SW created by RM Inc. as a SQLite extension. That software is proprietary and its specification has not be made public.

A shared library (dll in Windows) that approximates the function of the RMNOCASE collation extension is on Tom's site, SQLiteToolsForRootsMagic.com. We'll call it the fake RMNOCASE.

A key point is the available dll and the proprietary code found inside RootsMagic do not function identically.

## Workarounds

When doing read-only queries externally, one can often include a specific collation sequence in the query that will override the defalut specified in the table declaration. This may mean that exisring indexes won't be used which could impact speed.

The safest procedure to run data modifing SQL on a RM database is-
-close the database in RM\
-open it in an external app and load the “fake” RMNOCASE collation extension\
-do a “reindex RMNOCASE” SQL command\
-do whatever SQL operations desired, including inserts\
-close the database\
-open the database in RM and immediately use the RM tool to rebuild indexes.\

Another idea-
Modify the RM database tables so that the they do not use RMNOCASE. Once would have to move all of the data to the new desired tables, delete the old table, and then rename the table. Rebuild the indexes.\
It is not clear whether the RM app will notice the removal of the RMNOCASE dependency.\
If NOCASE were substituted for RMNOCASE, at least ASCII name would sort as expected.

Of course, one would want to create the corresponding SQL to return the schema back to "the factory default".

Another idea-\
Reverse engineer the real RMNOCASE collatiion and write an extension that implements it exactly.

## The Fake RMNOCASE: unifuzz64.dll

direct download:\
https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2018/05/unifuzz64.dll

the link above is found in this context:\
https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/

The SQLiteToolsforRootsMagic website has been around for many years and is run by a trusted RM user. Many posts to public RootsMagic user forums mention use of unifuzz64.dll from the SQLiteToolsforRootsMagic website.

 MD5 hash values are used to confirm the identity of files.

 ```
 MD5 hash							File size		File name
 06a1f485b0fae62caa80850a8c7fd7c2	256,406 bytes	unifuzz64.dll
```

## An interesting issue

The RMNOCASE collation function used within the RM app for Windows and MacOS seems to use a OS native call, because the collations on Win and MacOS are not identical. This can be seen when moving a DB file between platforms; integrity check shows errors until a reindex is done.

Note that an empty database created on MacOS will fail integrity check when done on a Windows OS machine due to missing entries in the idxSourceTemplateName index.
Not clear what characters sort differently on Win and MacOS.

## What to worry about

While operating on a database with RootsMagic alone, there is no problem. The authentic RMNOCASE collation is always used.

When working on a RootsMagic database externally, there can be issues if precautions are not take,

If names contain only the 26 latin characters, it would seem that there should not be a problem because the fake and authentic RMNOCASE should produce the same results. NOT TESTED

Indexes contain data that can be easily reconstructed by the SQLite command "reindex". However, if a database is opened and it already has an index created with, say the authentic RMNOCASE and one operates on the date using the fake RMNOCASE and an index using RMNOCASE collation is used, bad things may happen.

### Two situations to consider

Operating on a database opened only in an external tool
Operating on a database opened in RootsMagic and an external tool simultaneously.

Every time you plan to add, remove, or modify data in a column sorted by RMNOCASE, you must run the command to reindex first.

reindex RMNOCASE

Then all of your modification will work fine. But then, when you open your file in RM, the very first thing to do is the RM Rebuild indexes tool. After that, you'll be ok
I always confirm by running check file integrity after the build index.


When opening RootsMagic after having had the database reindexed using a fake RMNOCASE-
One can open the file, switch to the File tab, select Tools and then Rebuild Indexes.

Is the database completely inert before running the Rebuild Indexes tool?
Perhaps meta data is saved to ConfigTable ?
Perhaps Web Hints will be searched for ?

Are those problems- or ignorable with regard to the RMNOCASE issue?


## References

Some links to discussions about custom collations and extensions/

SQLite documentation states that while a database is operational, a collation may not change. If it does, it may lead to indeterminate results. BAD.BAD.BAD.

[How to handle collation version changes](https://sqlite.org/forum/info/5317344555f7a5f2)

Other collations-\
https://learn.microsoft.com/en-us/dotnet/standard/data/sqlite/collation

https://github.com/nalgeon/sqlean/blob/main/docs/unicode.md

SQLite extensions listings-

https://sqlpkg.org/all/

issues with custom collations-

https://stackoverflow.com/questions/75494491/how-to-use-sqlite-database-created-with-custom-collation-in-an-environment-wher

https://stackoverflow.com/questions/47095400/exporting-a-sqlite3-table-from-a-db-with-error-no-such-collation-sequence-iun

[Define New Collating Sequences](https://sqlite.org/c3ref/create_collation.html)


https://shallowdepth.online/posts/2022/01/5-ways-to-implement-case-insensitive-search-in-sqlite-with-full-unicode-support/

https://www.sqlite.org/src/artifact?ci=trunk&filename=ext/icu/README.txt

https://stackoverflow.com/questions/15051018/
localized-collate-on-a-sqlite-string-comparison

https://stackoverflow.com/questions/181037/
case-insensitive-utf-8-string-collation-for-sqlite-c-c

https://sourceforge.net/projects/icu/files/ICU4C/58.2/

https://icu.unicode.org/

https://www.npcglib.org/~stathis/blog/precompiled-icu/

https://www.sqlite.org/src/artifact?ci=trunk&filename=ext/icu/README.txt

https://github.com/nalgeon/sqlean


## Where is RMNOCASE used in v9 schema
```
SELECT
  tbl_name,
  sql
FROM sqlite_master
WHERE SQL like  '%RMNOCASE%'


AddressTable
CREATE TABLE AddressTable (AddressID INTEGER PRIMARY KEY, AddressType INTEGER, Name TEXT COLLATE RMNOCASE, Street1 TEXT, Street2 TEXT, City TEXT, State TEXT, Zip TEXT, Country TEXT, Phone1 TEXT, Phone2 TEXT, Fax TEXT, Email TEXT, URL TEXT, Latitude INTEGER, Longitude INTEGER, Note TEXT, UTCModDate FLOAT )

FactTypeTable
CREATE TABLE FactTypeTable (FactTypeID INTEGER PRIMARY KEY, OwnerType INTEGER, Name TEXT COLLATE RMNOCASE, Abbrev TEXT, GedcomTag TEXT, UseValue INTEGER, UseDate INTEGER, UsePlace INTEGER, Sentence TEXT, Flags INTEGER, UTCModDate FLOAT )

MultimediaTable
CREATE TABLE MultimediaTable (MediaID INTEGER PRIMARY KEY, MediaType INTEGER, MediaPath TEXT, MediaFile TEXT COLLATE RMNOCASE, URL TEXT, Thumbnail BLOB, Caption TEXT COLLATE RMNOCASE, RefNumber TEXT COLLATE RMNOCASE, Date TEXT, SortDate BIGINT, Description TEXT, UTCModDate FLOAT )

NameTable
CREATE TABLE NameTable (NameID INTEGER PRIMARY KEY, OwnerID INTEGER, Surname TEXT COLLATE RMNOCASE, Given TEXT COLLATE RMNOCASE, Prefix TEXT COLLATE RMNOCASE, Suffix TEXT COLLATE RMNOCASE, Nickname TEXT COLLATE RMNOCASE, NameType INTEGER, Date TEXT, SortDate BIGINT, IsPrimary INTEGER, IsPrivate INTEGER, Proof INTEGER, Sentence TEXT, Note TEXT, BirthYear INTEGER, DeathYear INTEGER, Display INTEGER, Language TEXT, UTCModDate FLOAT, SurnameMP TEXT, GivenMP TEXT, NicknameMP TEXT )

PlaceTable
CREATE TABLE PlaceTable (PlaceID INTEGER PRIMARY KEY, PlaceType INTEGER, Name TEXT COLLATE RMNOCASE, Abbrev TEXT, Normalized TEXT, Latitude INTEGER, Longitude INTEGER, LatLongExact INTEGER, MasterID INTEGER, Note TEXT, Reverse TEXT COLLATE RMNOCASE, fsID INTEGER, anID INTEGER, UTCModDate FLOAT )

RoleTable
CREATE TABLE RoleTable (RoleID INTEGER PRIMARY KEY, RoleName TEXT COLLATE RMNOCASE, EventType INTEGER, RoleType INTEGER, Sentence TEXT, UTCModDate FLOAT )

SourceTable
CREATE TABLE SourceTable (SourceID INTEGER PRIMARY KEY, Name TEXT COLLATE RMNOCASE, RefNumber TEXT, ActualText TEXT, Comments TEXT, IsPrivate INTEGER, TemplateID INTEGER, Fields BLOB, UTCModDate FLOAT )

SourceTemplateTable
CREATE TABLE SourceTemplateTable (TemplateID INTEGER PRIMARY KEY, Name TEXT COLLATE RMNOCASE, Description TEXT, Favorite INTEGER, Category TEXT, Footnote TEXT, ShortFootnote TEXT, Bibliography TEXT, FieldDefs BLOB, UTCModDate FLOAT )

TagTable
CREATE TABLE TagTable (TagID INTEGER PRIMARY KEY, TagType INTEGER, TagValue INTEGER, TagName TEXT COLLATE RMNOCASE, Description TEXT, UTCModDate FLOAT )

TaskTable
CREATE TABLE TaskTable (TaskID INTEGER PRIMARY KEY, TaskType INTEGER, RefNumber TEXT, Name TEXT COLLATE RMNOCASE, Status INTEGER, Priority INTEGER, Date1 TEXT, Date2 TEXT, Date3 TEXT, SortDate1 BIGINT, SortDate2 BIGINT, SortDate3 BITINT, Filename TEXT, Details TEXT, Results TEXT, UTCModDate FLOAT, Exclude INTEGER )

WitnessTable
CREATE TABLE WitnessTable (WitnessID INTEGER PRIMARY KEY, EventID INTEGER, PersonID INTEGER, WitnessOrder INTEGER, Role INTEGER, Sentence TEXT, Note TEXT, Given TEXT COLLATE RMNOCASE, Surname TEXT COLLATE RMNOCASE, Prefix TEXT COLLATE RMNOCASE, Suffix TEXT COLLATE RMNOCASE, UTCModDate FLOAT )

FANTypeTable
CREATE TABLE FANTypeTable (FANTypeID INTEGER PRIMARY KEY, Name TEXT COLLATE RMNOCASE, Role1 TEXT, Role2 TEXT, Sentence1 TEXT, Sentence2 TEXT, UTCModDate FLOAT )

CitationTable
CREATE TABLE CitationTable (CitationID INTEGER PRIMARY KEY, SourceID INTEGER, Comments TEXT, ActualText TEXT, RefNumber TEXT, Footnote TEXT, ShortFootnote TEXT, Bibliography TEXT, Fields BLOB, UTCModDate FLOAT, CitationName TEXT COLLATE RMNOCASE )



idxSourceName
CREATE INDEX idxSourceName ON SourceTable (Name COLLATE RMNOCASE)
```

### Listing by table in simplified format

```
AddressTable
Name TEXT COLLATE RMNOCASE

FactTypeTable
Name TEXT COLLATE RMNOCASE

MultimediaTable
MediaFile TEXT COLLATE RMNOCASE
Caption TEXT COLLATE RMNOCASE
RefNumber TEXT COLLATE RMNOCASE

NameTable
Surname TEXT COLLATE RMNOCASE
Given TEXT COLLATE RMNOCASE
Prefix TEXT COLLATE RMNOCASE
Suffix TEXT COLLATE RMNOCASE
Nickname TEXT COLLATE RMNOCASE

PlaceTable
Name TEXT COLLATE RMNOCASE
Reverse TEXT COLLATE RMNOCASE

RoleTable
RoleName TEXT COLLATE RMNOCASE

SourceTable
Name TEXT COLLATE RMNOCASE

SourceTemplateTable
Name TEXT COLLATE RMNOCASE

TagTable
TagName TEXT COLLATE RMNOCASE

TaskTable
Name TEXT COLLATE RMNOCASE

WitnessTable
Given TEXT COLLATE RMNOCASE
Surname TEXT COLLATE RMNOCASE
Prefix TEXT COLLATE RMNOCASE
Suffix TEXT COLLATE RMNOCASE

FANTypeTable
Name TEXT COLLATE RMNOCASE

CitationTable
CitationName TEXT COLLATE RMNOCASE

idxSourceName
SourceTable
Name COLLATE RMNOCASE
```

13 tables and 1 index on name in SourceTable

The index use of RMNOCASE can be ignored since the table already specifies RMNOCASE as the default collation for SourceTable.Name. Why was it specified for this one index? Why were the tables set up with default collations instead of the collation being specified in the Index declaration statements?
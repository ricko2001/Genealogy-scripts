-- Change RM7 BLOB columns to text, remove extraneous XML processing stmst and trailing /n.

-- RM Table: CREATE TABLE CitationTable (
-- CitationID INTEGER PRIMARY KEY, 
-- OwnerType INTEGER, SourceID INTEGER, OwnerID INTEGER, 
-- Quality TEXT, IsPrivate INTEGER, Comments BLOB, ActualText BLOB, RefNumber TEXT, Flags INTEGER, Fields BLOB );

DROP TABLE if exists  CitationTableMod;

CREATE TABLE CitationTableMod 
(CitationID INTEGER PRIMARY KEY, 
OwnerType INTEGER,
SourceID INTEGER, 
OwnerID INTEGER, 
Quality TEXT, 
IsPrivate INTEGER, 
Comments TEXT, 
ActualText TEXT, 
RefNumber TEXT, 
Flags INTEGER, 
Fields TEXT );

INSERT INTO CitationTableMod (CitationID, OwnerType, SourceID, OwnerID, Quality, 
IsPrivate, Comments, ActualText, RefNumber, Flags, Fields)
SELECT 
CitationID, OwnerType, SourceID, OwnerID, Quality, 
IsPrivate, 
cast(Comments as text), 
cast(ActualText as text), 
RefNumber, Flags, 
trim(substr(cast(Fields as text),41),char(10, 13))
FROM CitationTable
WHERE true;

-- RM Table: CREATE TABLE SourceTable (
-- SourceID INTEGER PRIMARY KEY, Name TEXT COLLATE RMNOCASE, RefNumber TEXT, 
-- ActualText TEXT, Comments TEXT, IsPrivate INTEGER, TemplateID INTEGER,
-- Fields BLOB );

DROP TABLE if exists  SourceTableMod;

CREATE TABLE SourceTableMod (
SourceID INTEGER PRIMARY KEY, 
Name TEXT, 
RefNumber TEXT, 
ActualText TEXT, 
Comments TEXT, 
IsPrivate INTEGER, 
TemplateID INTEGER, 
Fields TEXT );

INSERT INTO SourceTableMod (SourceID, Name, RefNumber, 
ActualText, Comments, IsPrivate, TemplateID, Fields )
SELECT 
SourceID, Name, RefNumber, 
ActualText, Comments, IsPrivate, TemplateID, 
trim(substr(cast(Fields as text),41),char(10, 13))
FROM SourceTable
WHERE true;







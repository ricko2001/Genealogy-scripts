
REINDEX RMNOCASE;

--===========================================DIV50==
-- REF from Trim space.txt

--===========================================DIV50==
-- Trim Surname, Give, Suffix, Prefix in NameTable

UPDATE NameTable
  SET
    Surname = TRIM(Surname),
    Given   = TRIM(Given),
    Suffix  = TRIM(Suffix),
    Prefix  = TRIM(Prefix)
  WHERE 
        Surname <> TRIM(Surname)
    OR  Given   <> TRIM(Given)
    OR  Suffix  <> TRIM(Suffix)
    OR  Prefix  <> TRIM(Prefix);


--===========================================DIV50==
-- Trim Details in EventTable

UPDATE EventTable
  SET   Details =  TRIM(Details)
  WHERE Details <> TRIM(Details);


--===========================================DIV50==
-- Trim Name, Abbrev, Normalized in PlaceTable

UPDATE PlaceTable
  SET
    Name       = TRIM(Name),
    Abbrev     = TRIM(Abbrev),
    Normalized = TRIM(Normalized)
  WHERE
        Name       <> TRIM(Name)
    OR  Abbrev     <> TRIM(Abbrev)
    OR  Normalized <> TRIM(Normalized);


--===========================================DIV50==
-- Trim Name in SourceTemplateTable

UPDATE SourceTemplateTable
  SET   Name = TRIM(Name)
  WHERE Name <> TRIM(Name);


--===========================================DIV50==
-- Trim Name in SourceTable 

UPDATE SourceTable
  SET   Name =  TRIM(Name)
  WHERE Name <> TRIM(Name);


--===========================================DIV50==
-- Trim CitationName in CitationTable

UPDATE CitationTable
  SET   CitationName =  TRIM(CitationName)
  WHERE CitationName <> TRIM(CitationName);


--===========================================DIV50==
--REF from Fix WebTag names.txt

--===========================================DIV50==
--Ancestry links WebTag names that should have tree name

UPDATE URLTable
  SET Name='otter-saito'
  WHERE OwnerType =0 
    AND URL LIKE 'https://www.ancestry.com/family-tree/person/tree/14741034/person%'
    AND Name <> 'otter-saito';


UPDATE URLTable
  SET Name='lumsden-horn'
  WHERE OwnerType =0 
    AND URL LIKE 'https://www.ancestry.com/family-tree/person/tree/111641456/person%'
    AND Name <> 'lumsden-horn';


UPDATE URLTable
  SET Name='felton-tsujimoto'
  WHERE OwnerType =0 
    AND URL LIKE 'https://www.ancestry.com/family-tree/person/tree/111652204/person%'
    AND Name <> 'felton-tsujimoto';


UPDATE URLTable
  SET Name='smith-burke'
  WHERE OwnerType =0 
    AND URL LIKE 'https://www.ancestry.com/family-tree/person/tree/111800644/person%'
    AND Name <> 'smith-burke';


UPDATE URLTable
  SET Name='Find a Grave'
  WHERE OwnerType =4
    AND URL LIKE 'https://www.findagrave.com/memorial%'
    AND Name <> 'Find a Grave';


--===========================================DIV50==
--REF from Fix placeholders.txt

--===========================================DIV50==
-- Fix placeholder in Details or Date in EventTable

UPDATE EventTable
  SET Details = ''
  WHERE Details = '=' 
   OR Details = '-';

UPDATE EventTable
  SET Date = '.',
      SortDate ='9223372036854775807'
  WHERE Date = 'T=' 
   OR Date = 'T-';


--===========================================DIV50==
--REF from Add Sort date to undated events.txt

--===========================================DIV50==
-- Add Sort date to undated events

-- No sort date = 9223372036854775807
-- Family data and Names  4000

-- ChildParent  1065  4000 = 7881299365077188620
UPDATE EventTable
SET SortDate = 7881299365077188620
WHERE EventType = 1065
AND SortDate <> 7881299365077188620;

-- PrimaryName  4001 = 7881862315030609932
UPDATE NameTable
SET SortDate = 7881862315030609932
WHERE SortDate = 9223372036854775807
AND IsPrimary = 1;

-- Alternate-Name  4010 = 7886928864611401740
UPDATE NameTable
SET SortDate = 7886928864611401740
WHERE SortDate = 9223372036854775807
AND IsPrimary <> 1;

-- Person Attributes  4100

-- NeverMarried  1090  4100 = 7937594360419319820
UPDATE EventTable
SET SortDate = 7937594360419319820
WHERE EventType = 1090
AND SortDate <> 7937594360419319820;

-- Medical   1054  4100 = 7937594360419319820
UPDATE EventTable
SET SortDate = 7937594360419319820
WHERE EventType = 1054
AND SortDate <> 7937594360419319820;

-- Anecdote  1090  4100 = 7937594360419319820
UPDATE EventTable
SET SortDate = 7937594360419319820
WHERE SortDate = 9223372036854775807
AND EventType = 1090;

-- Religion  29  4100 = 7937594360419319820
UPDATE EventTable
SET SortDate = 9223372036854775807
WHERE SortDate = 7937594360419319820
AND EventType = 28;

-- Research Data

-- ResearchNote       1096  4400 = 8106479346445713420
UPDATE EventTable
SET SortDate = 8106479346445713420
WHERE EventType = 1096
AND SortDate <> 8106479346445713420;

-- Evidence-Summary   1100  4500 = 8162774341787844620
UPDATE EventTable
SET SortDate = 8162774341787844620
WHERE EventType = 1100
AND SortDate <> 8106479346445713420;

-- Misc facts

-- MetWithRJO   1099  4600 = 8219069337129975820
UPDATE EventTable
SET SortDate = 8219069337129975820
WHERE EventType = 1099
AND SortDate <> 8219069337129975820;

-- Links to other systems  4900

-- ID_TMG  1064  4901 = 8388517273109790732
UPDATE EventTable
SET SortDate = 8388517273109790732
WHERE EventType = 1064
AND SortDate <> 8388517273109790732;

-- ID_ANC  1098  4911 = 8394146772644003852
UPDATE EventTable
SET SortDate = 8394146772644003852
WHERE EventType = 1098
AND SortDate <> 8394146772644003852;

-- ID_FG  1094  4912 = 8394709722597425164 
UPDATE EventTable
SET SortDate = 8394709722597425164
WHERE EventType = 1094
AND SortDate <> 8394709722597425164;

-- ID_FSFT  1063  4913 = 8395272672550846476
UPDATE EventTable
SET SortDate = 8395272672550846476
WHERE EventType = 1063
AND SortDate <> 8395272672550846476;

 -- ID_WIKTR  1050  4914 = 8395835622504267788
UPDATE EventTable
SET SortDate = 8395835622504267788
WHERE EventType = 1050
AND SortDate <> 8395835622504267788;

--===========================================DIV50==
--REF from Citation sort order.sql

--===========================================DIV50==
-- Update all SortOrder values in CitationLinkTable

UPDATE CitationLinkTable AS clt1
SET SortOrder= ( SELECT SUBSTR(st.Name, 1,25) || SUBSTR(ct.CitationName, 1,10) 
    FROM CitationLinkTable AS clt2
    JOIN CitationTable AS ct USING (CitationID)
    JOIN SourceTable AS st USING (SourceID)
    WHERE clt1.LinkID = clt2.LinkID
    );


--===========================================DIV50==


--===========================================DIV50==
-- REBUILD INDEXES in RM first thing after opening


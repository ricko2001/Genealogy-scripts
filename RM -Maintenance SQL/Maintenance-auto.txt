
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
-- REBUILD INDEXES in RM first thing after opening


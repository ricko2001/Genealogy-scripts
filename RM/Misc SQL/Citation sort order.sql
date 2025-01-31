-- from https://sqlitetoolsforrootsmagic.com/forum/topic/sorting-the-order-of-rm9-citations/

-- CitationSortOrders.sql
/* 2024-01-21 Tom Holden ve3meo
rev 2024-01-22 code made more compact
 and SortOrder values prepended with SortKey code

Sorts the order of Citations as viewed in the "Sources" pane of the Edit Person 
form by exploiting the undocumented SortOrder column in the CitationLinkTable. 
N.B.: The slide-in Citations form and the tool tip listing that arises from 
hovering over the Sources option on the Edit Person form do not respect the 
SortOrder column. Only the Sources pane of the Edit Person form does.

Requires a SQLite Manager that supports run-time variables and the REGEXP 
function. Developed and tested with SQLite Expert Personal 5.5.8.619 (x64)
on a database under RootsMagic 9.1.3.0 on a Windows 10 pc.

A sort order can be chosen from several by entering one of the following codes
when prompted for SortKeys (case-insensitive):
SortKeys	Description/Effect
C		  Citation Name ascending in alphabetical order
CID		CitationID ascending, earliest created citation at top of list
CID-	CitationID descending, most recently created citation at top of list
CM 		Citation Modified Date asc, most recently edited last
CM-		Citation Modified Date desc, most recently edited last
Q 		Citation Quality descending, best Evidence at top of list
QS 		Citation Quality descending, Source Name secondary, ascending
QSC 	Citation Quality desc, Source Name asc, Citation Name ascending
S		  Source Name ascending in alphabetical order
SC		Source Name, Citation Name ascending
SID		SourceID ascending, earliest created source at top of list
SID-	SourceID descending, most recently created source at top of list
SM 		Source Modified Date asc, most recently edited last
SM-		Source Modified Date desc, most recently edited last
TID		CitationLinkID asc, earliest created link|tag|use at top of list
TID-	CitationLinkID desc, most recently created link|tag|use at top of list
TM 		Citation Tag (Link) Modified Date asc, most recently edited last
TM- 	Citation Tag (Link) Modified Date desc, most recently edited first

The second prompt, OverwriteSortOrderIntegersYN, asks whether you want to 
overwrite Integer values in the SortOrder column. Only Y or y will do so.
The reason for this constraint is the expectation (hope) that RM Inc will
develop further functionality including manual sorting of the sources for
a fact. Other implementations of such sorting in the RM app use integers.
Therefore, this script by default exempts integer driven sortorders from
its global changes. 
 
Note on Sort by Citation Quality 
Relies on the characters associated with each of the categories and should result
in an order having Primary Information+Direct Evidence+OriginalSource first 
and Unknown+Unknown+Unknown last. See 
https://sqlitetoolsforrootsmagic.com/understanding-the-rootsmagic-8-database-type-decodes/#Citations


*/

--Gather the potential Sort Keys into a temporary View
DROP VIEW IF EXISTS CitationLinkView
;
CREATE TEMP VIEW CitationLinkView AS
SELECT
   CL.LinkID, CL.SortOrder, CL.Quality, CL.UTCModDate AS clUTCModDate
 , C.CitationID, C.CitationName, C.UTCModDate AS cUTCModDate 
 , S.SourceID, S.Name, S.UTCModDate AS sUTCModDate
FROM CitationLinkTable CL
JOIN CitationTable C USING (CitationID)
JOIN SourceTable S USING (SourceID)
;

--SELECT * FROM CitationLinkView
;

UPDATE CitationLinkTable
SET SortOrder=
 UPPER($SortKeys)|| -- get user inputted keycode and concat with field(s)
 (SELECT
   (CASE UPPER($SortKeys) -- concat field(s) according to SortKey code
     WHEN 'C'  -- Citation Name Ascending
      THEN CitationName
     WHEN 'CID' -- CitationID Ascending
      THEN FORMAT('%010i', CitationID)
     WHEN 'CID-' -- CitationID Descending
      THEN FORMAT('%010i', 10000000000-CitationID)
     WHEN 'CM' -- Citation Modified Date ascending
      THEN cUTCModDate
     WHEN 'CM-'  -- Citation Modified Date descending
      THEN 100000-cUTCModDate 
     WHEN 'Q'  -- Citation Quality descending
      THEN Quality
     WHEN 'QS' -- Citation Quality descending, Source name ascending
      THEN Quality||Name
     WHEN 'QSC' -- Citation Quality descending, Source name, Citation name ascending
      THEN Quality||Name||CitationName
     WHEN 'S'  -- Source Name Ascending
      THEN Name 
     WHEN 'SC'  -- Source Name, Citation Name ascending
      THEN Name||CitationName 
     WHEN 'SID' -- SourceID Ascending
      THEN FORMAT('%010i', SourceID) 
     WHEN 'SID-' -- SourceID Descending
      THEN FORMAT('%010i', 10000000000-SourceID) 
     WHEN 'SM'  -- Source Modified Date ascending
      THEN sUTCModDate 
     WHEN 'SM-'  -- Source Modified Date descending
      THEN 100000-sUTCModDate
     WHEN 'TID' -- LinkID Ascending
      THEN FORMAT('%010i', LinkID)
     WHEN 'TID-' -- LinkID Descending
      THEN FORMAT('%010i', 10000000000-LinkID)
     WHEN 'TM'  -- Citation Tag (Link) Modified Date ascending
      THEN clUTCModDate
     WHEN 'TM-' -- Citation Tag (Link) Modified Date descending
      THEN 100000-clUTCModDate
    END
    )
  FROM CitationLinkView CLV
  WHERE CitationLinkTable.LinkID = CLV.LinkID
  )
WHERE 
UPPER($SortKeys)IN  -- update only if SortKey code is valid 
 (
  'C','CID','CID-','CM','CM-'
 ,'Q','QS','QSC'
 ,'S','SC','SID','SID-','SM','SM-'
 ,'TID','TID-','TM','TM-'
 )
AND
CASE UPPER($OverwriteSortOrderIntegersYN)
 WHEN 'Y' THEN 1
 ELSE
  CitationLinkTable.SortOrder NOT REGEXP '^[0-9]+$' -- Don't change integer values
END
;
------------END OF SCRIPT---------------



--Streamlined- hard code the sort values

UPDATE CitationLinkTable AS clt1
SET SortOrder= ( SELECT SUBSTR(st.Name, 1,25) || SUBSTR(ct.CitationName, 1,10) 
    FROM CitationLinkTable AS clt2
    JOIN CitationTable AS ct USING (CitationID)
    JOIN SourceTable AS st USING (SourceID)
    WHERE clt1.LinkID = clt2.LinkID
    )


--NOT WORKING-  WHERE clt1.LinkID = clt2.LinkID

-- WITH SortValue(s_value) AS (
-- SELECT S.Name
-- FROM CitationLinkTable AS clt1
-- JOIN CitationTable AS ct USING (CitationID)
-- JOIN SourceTable AS st USING (SourceID)
-- )
-- UPDATE CitationLinkTable AS clt2
-- SET SortOrder= (
-- SELECT s_value 
-- FROM SortValue
-- WHERE clt1.LinkID = clt2.LinkID);
-- 

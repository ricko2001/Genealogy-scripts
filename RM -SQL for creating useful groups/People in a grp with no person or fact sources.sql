--[SRC: People in grp with no Person or Fact src-citations]
--SQL_QUERY =
  -- people in a specified group with no Person or fact source-citations
  -- people may still have family, family fact, association,or name citations
  -- specify the group name in line 9
  WITH
    constants(C_GroupName) AS (
      SELECT    'GROUP_NAME_GOES_HERE'    AS C_GroupName
      ),
    group_members(PersonID) AS (
      SELECT pt.PersonID
        FROM PersonTable AS pt
        INNER JOIN GroupTable AS gt ON pt.PersonID BETWEEN gt.StartID AND gt.EndID
        INNER JOIN TagTable AS tt ON tt.TagValue = gt.GroupID
        WHERE gt.GroupID = tt.TagValue
          AND tt.TagType = 0
          AND tt.TagName = (SELECT C_GroupName FROM constants) COLLATE NOCASE
      )
  -- No person citations
  SELECT gm.PersonID
    FROM group_members AS gm
    LEFT JOIN CitationLinkTable AS clt ON clt.OwnerID = gm.PersonID AND clt.OwnerType=0
    WHERE clt.LinkID is NULL
  --
  INTERSECT
  -- No fact citations
  SELECT gm.PersonID
    FROM group_members AS gm
    INNER JOIN EventTable AS et ON et.OwnerID = gm.PersonID AND et.OwnerType=0
    LEFT JOIN CitationLinkTable AS clt ON clt.OwnerID = et.EventID AND clt.OwnerType=2
  GROUP BY gm.PersonID
  HAVING COUNT(LinkID)=0
  --
  ORDER BY gm.PersonID;
  --




-- preliminary work
--  person citations, 
  WITH 
  constants(C_GroupName) AS (
    SELECT  
   'REL: Friends' AS C_GroupName
    ),
  group_members(PersonID) AS (
    SELECT pt.PersonID
     FROM PersonTable AS pt
     INNER JOIN GroupTable AS gt ON pt.PersonID BETWEEN gt.StartID AND gt.EndID
     INNER JOIN TagTable AS tt ON tt.TagValue = gt.GroupID
     WHERE gt.GroupID = tt.TagValue
     AND tt.TagType = 0
     AND tt.TagName = (SELECT C_GroupName FROM CONSTANTS) COLLATE NOCASE
     )
    SELECT gm.PersonID, nt.Surname, nt.Given , clt.LinkID, clt.OwnerType
    --SELECT gm.PersonID
     FROM group_members AS gm
    INNER JOIN nameTable AS nt ON gm.PersonID = nt.OwnerID
    LEFT JOIN CitationLinkTable AS clt ON clt.OwnerID = gm.PersonID AND clt.OwnerType=0
    WHERE clt.LinkID is NULL
    ORDER BY gm.PersonID    



  WITH 
  constants(C_GroupName) AS (
    SELECT  
   'REL: Friends' AS C_GroupName
    ),
  group_members(PersonID) AS (
    SELECT pt.PersonID
     FROM PersonTable AS pt
     INNER JOIN GroupTable AS gt ON pt.PersonID BETWEEN gt.StartID AND gt.EndID
     INNER JOIN TagTable AS tt ON tt.TagValue = gt.GroupID
     WHERE gt.GroupID = tt.TagValue
     AND tt.TagType = 0
     AND tt.TagName = (SELECT C_GroupName FROM CONSTANTS) COLLATE NOCASE
     )
     -- these have at least one fact with no citation
  SELECT DISTINCT gm.PersonID
    --SELECT gm.PersonID, nt.Surname, nt.Given , clt.LinkID, clt.OwnerType
    FROM group_members AS gm
    INNER JOIN nameTable AS nt ON gm.PersonID = nt.OwnerID
    INNER JOIN EventTable AS et ON et.OwnerID = gm.PersonID AND et.OwnerType=0
    LEFT JOIN CitationLinkTable AS clt ON clt.OwnerID = et.EventID AND clt.OwnerType=2
    WHERE clt.LinkID is NULL
    ORDER BY gm.PersonID


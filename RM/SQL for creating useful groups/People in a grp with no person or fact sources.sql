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

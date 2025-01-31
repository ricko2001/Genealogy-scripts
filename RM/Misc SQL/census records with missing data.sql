  -- select people with various census records with bad/missing data
  -- 
  -- description is empty
  SELECT  OwnerID AS PersonID
  FROM EventTable AS et
  INNER JOIN FactTypeTable AS ftt ON et.EventType = ftt.FactTypeID
  WHERE et.OwnerType=0
  AND ftt.Name='Census' COLLATE NOCASE
  AND et.Details = ''
  -- 
  UNION
  -- 
  -- date does not match description date
  SELECT  OwnerID AS PersonID
  FROM EventTable AS et
  INNER JOIN FactTypeTable AS ftt ON et.EventType = ftt.FactTypeID
  WHERE et.OwnerType=0
  AND ftt.Name='Census' COLLATE NOCASE
  AND substr(et.DATE,4,4) <> substr(et.Details,1,4)
  -- 
  UNION
  -- 
  -- description does not fit pattern
  SELECT  OwnerID AS PersonID
  FROM EventTable AS et
  INNER JOIN FactTypeTable AS ftt ON et.EventType = ftt.FactTypeID
  WHERE et.OwnerType=0
  AND ftt.Name='Census' COLLATE NOCASE
  AND NOT (
       et.Details LIKE '____ US Federal Census'
    OR et.Details LIKE '____ US Federal Census - Veterans Schedule'
    OR et.Details LIKE '____ US Federal Census TODO'
    OR et.Details LIKE '____ US Federal Census TODO use cit'
    OR et.Details LIKE '____ US Federal Census summary'
    OR et.Details LIKE '____ US Federal Census summary-img'
    OR et.Details LIKE '____ %State%'   -- US State census
    OR et.Details LIKE '____ %Nation%'  -- American Indian nations
    OR et.Details LIKE '____ NOT FOUND'
    )
  -- 
  UNION
  --
  -- note is empty for 1940 or 1950 summary
  SELECT  OwnerID AS PersonID
  FROM EventTable AS et
  INNER JOIN FactTypeTable AS ftt ON et.EventType = ftt.FactTypeID
  WHERE et.OwnerType=0
  AND ftt.Name='Census' COLLATE NOCASE
  AND ( substr(et.DATE,4,4) = '1940' OR substr(et.DATE,4,4) = '1950' )
  AND et.Note = ''
  AND et.Details LIKE '%summary%'

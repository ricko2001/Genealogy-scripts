--[FACT-FG: bad data]
--SQL_QUERY =
  SELECT et.OwnerID as PersonID
  FROM EventTable AS et
  INNER JOIN FactTypeTable AS ftt ON ftt.FactTypeID = et.EventType
  WHERE 
    ftt.Name COLLATE NOCASE = 'Evidence-Summary' 
    AND et.OwnerType = 0
    AND Details <> ''
  --
  UNION
  --
  SELECT et.OwnerID AS PersonID
  FROM EventTable AS et
  INNER JOIN FactTypeTable AS ftt ON ftt.FactTypeID = et.EventType
  WHERE ftt.Name COLLATE NOCASE = 'Evidence-Summary'
  GROUP BY et.OwnerID, ftt.FactTypeID
  HAVING COUNT(*) >1;

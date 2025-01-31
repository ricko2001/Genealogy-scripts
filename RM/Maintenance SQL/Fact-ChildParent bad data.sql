--[FACT-ChildParent: bad data]
--SQL_QUERY =
  SELECT et.OwnerID as PersonID
  FROM EventTable AS et
  INNER JOIN FactTypeTable AS ftt ON ftt.FactTypeID = et.EventType
  WHERE 
    ftt.Name COLLATE NOCASE = 'ChildParent' 
    AND et.OwnerType = 0
    AND NOT (
      Details = ''
      OR Details = '_STOP'
      OR Details = '_CENSUS'
      OR Details = '_OBIT'
      OR Details = '_START-OF-LINE'
      OR Details LIKE '%TODO%'
    )
  --
  UNION
  --
  SELECT et.OwnerID AS PersonID
  FROM EventTable AS et
  INNER JOIN FactTypeTable AS ftt ON ftt.FactTypeID = et.EventType
  WHERE ftt.Name COLLATE NOCASE = 'ChildParent'
  GROUP BY et.OwnerID, ftt.FactTypeID
  HAVING COUNT(*) <> 1;

--[FACT-Bir-Dea:  >1]
--SQL_QUERY =
  SELECT et.OwnerID as PersonID
  FROM EventTable et
  INNER JOIN FactTypeTable AS ftt ON ftt.FactTypeID = et.EventType
  WHERE et.OwnerType = 0 
       AND ftt.Name = 'Birth' COLLATE NOCASE
  GROUP BY et.OwnerID
  HAVING COUNT(EventID) > 1
  --
  UNION
  --
  SELECT et.OwnerID as PersonID
  FROM EventTable et
  INNER JOIN FactTypeTable AS ftt ON ftt.FactTypeID = et.EventType
  WHERE et.OwnerType = 0 
       AND ftt.Name = 'Death' COLLATE NOCASE
  GROUP BY et.OwnerID
  HAVING COUNT(EventID) > 1
  
--===========================================DIV50==
--Check for missing or misplaced event data

  SELECT OwnerID as PersonID
--  SELECT OwnerID, Date, ftt.Name, Details
  FROM EventTable AS et
  INNER JOIN FactTypeTable AS ftt ON ftt.FactTypeID = et.EventType
  WHERE 
     (
      ftt.Name COLLATE NOCASE = 'Occupation' 
      OR ftt.Name COLLATE NOCASE = 'ID_FG' 
      OR ftt.Name COLLATE NOCASE = 'ID_FSFT' 
      OR ftt.Name COLLATE NOCASE = 'ID_TMG'
      ) 
    AND Details = ''
    AND et.OwnerType = 0
  ORDER BY OwnerID, Date; 

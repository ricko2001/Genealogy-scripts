SELECT stm.Name , ctm.CitationID, ctm.Fields, ctm.actualtext, ctm.comments
FROM CitationTablemod AS ctm
INNER JOIN SourceTablemod AS stm ON ctm.SourceID = stm.SourceID
WHERE 
 (
    stm.name not like 'A%' 
and stm.name not like 'B%'
and stm.name not like 'C%'
and stm.name not like 'D%' 
and stm.name not like 'E%' 
and stm.name not like 'F%'
and stm.name not like 'G%' 
and stm.name not like 'I%'
and stm.name not like 'M%'
and stm.name not like 'N%'
and stm.name not like 'O%'
and stm.name not like 'RR%'
and stm.name not like 'S%'
and stm.name not like 'WEB%' 
and stm.name not like '_ANC %' 
and stm.name not like '_TEMP%' 
  )
 and
  ctm.Fields LIKE '%'|| CHAR(10) || CHAR(13)|| '%' 
  ORDER BY stm.name



-- prod database

SELECT st.Name COLLATE NOCASE, 'SRC ' || cast(st.Fields as text) AS textData
FROM SourceTable AS st
WHERE cast(st.Fields as text)LIKE '%'|| CHAR(10) || '%'
    
UNION

SELECT st.Name COLLATE NOCASE, "CIT " || cast(ct.Fields as text) AS textData
FROM CitationTable AS ct
INNER JOIN SourceTable AS st ON ct.SourceID = st.SourceID
WHERE cast(ct.Fields as text)LIKE '%'|| CHAR(10) || '%'

ORDER BY st.Name COLLATE NOCASE

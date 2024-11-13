--===========================================DIV50==
--Some people have facts of blank type
--They have 0 as fact type

SELECT personID, 'has Fact type 0 event'
  FROM PersonTable
  JOIN EventTable ON PersonID = OwnerID
  WHERE OwnerType =0 AND EventType=0;


--===========================================DIV50==
--Check for Person # 0
SELECT PersonID
FROM PersonTable
WHERE PersonID = 0


--===========================================DIV50==
--Check for FamilyID # 0
SELECT FamilyID
FROM FamilyTable
WHERE FamilyID = 0

--===========================================DIV50==
--Check for PlaceD # 0
SELECT PlaceID
FROM PlaceTable
WHERE PlaceID = 0


-- from https://sqlitetoolsforrootsmagic.com/forum/topic/detecting-corruption-from-rm10-dragndrop/
-- https://sqlitetoolsforrootsmagic.com/wp-content/uploads/asgarosforum/1418/SuspectChildParent.sql
-- By Tom Holden



--SuspectChildParent.sql
/* 2025-01-26 Tom Holdenve3meo
Identifies probable corruption of parentage arising
from RM10 drag'n'drop of "descendants and their spouses" and,
possibly, from other causes. It cannot detect all forms of
parentage corruption.

The _PID columns indicate whether the ID to their left is found
in the PersonTable. If one or more is N, there is a problem to
be investigated using the valid RINs to find the situation in RM.
 
This script depends on the drag'n'drop failing to transfer a parent's
profile but creates a FamilyTable record pointing to their
original PersonID. If no person exists in the target database
with that RIN, this script can detect it. 

If a person with that ID already exists, they receive 
family-type events and children belonging to the source parent.
Unfortunately, this script does not detect such corruption.  
*/

SELECT DISTINCT
 Ch.ChildID
 , IIF((SELECT PersonID FROM PersonTable WHERE PersonID=Ch.ChildID),'Y','N') AS CPID 
 , FatherID
 , IIF((SELECT PersonID FROM PersonTable WHERE PersonID=FatherID),'Y','N') AS FPID 
 , MotherID
 , IIF((SELECT PersonID FROM PersonTable WHERE PersonID=MotherID),'Y','N') AS MPID 
 , FamilyID 
FROM ChildTable Ch
LEFT JOIN FamilyTable USING(FamilyID)
WHERE 
Ch.ChildID NOT IN (SELECT PersonID FROM PersonTable) --Child is a non-person (no matching PersonID)
OR
(FatherID NOT IN (SELECT PersonID FROM PersonTable) AND FatherID) -- non-zero and non-person
OR 
(MotherID NOT IN (SELECT PersonID FROM PersonTable) AND MotherID) -- non-zero and non-person
;

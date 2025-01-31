
--to get a list of a person's parent sets (FamilyID), 
SELECT ct.FamilyID
FROM NameTable AS nt
INNER JOIN ChildTable AS ct ON ct.ChildID = nt.OwnerID
WHERE
     nt.IsPrimary = 1
AND  nt.SurName = 'Otter'
AND  nt.Given = 'Richard'


--to get a list of a person's parents (both names) (all sets)
SELECT  nt1.OwnerID, ct.FamilyID, nt2.Given, nt2.Surname, nt3.Given, nt3.Surname
FROM NameTable AS nt1
INNER JOIN ChildTable AS ct ON ct.ChildID = nt1.OwnerID
INNER JOIN FamilyTable AS ft ON ft.FamilyID = ct.FamilyID
INNER JOIN NameTable AS nt2 ON nt2.OwnerID = ft.FatherID
INNER JOIN NameTable AS nt3 ON nt3.OwnerID = ft.MotherID
WHERE
     nt1.IsPrimary = 1 AND nt2.IsPrimary = 1 AND nt3.IsPrimary = 1
AND  nt1.Surname = 'Otter'
AND  nt1.Given = 'Richard'






--to get a list of children (names) of a father's name (all families)
SELECT  ft.FamilyID, ct.ChildID, nt2.Given, nt2.Surname
FROM NameTable AS nt1 
INNER JOIN FamilyTable AS ft ON nt1.OwnerID = ft.FatherID
INNER JOIN ChildTable AS ct ON ct.FamilyID = ft.FamilyID
INNER JOIN NameTable AS nt2 ON ct.ChildID = nt2.OwnerID
WHERE
     nt1.IsPrimary = 1 AND nt2.IsPrimary = 1
AND  nt1.Given = 'Daniel Kung-Hua'
AND  nt1.Surname = 'Chao'







--to get a list of children (names) of a mother (all families)
SELECT  ft.FamilyID, ct.ChildID, nt2.Given, nt2.Surname
--ft.FatherID, ft.MotherID
FROM NameTable AS nt1 
INNER JOIN FamilyTable AS ft ON nt1.OwnerID = ft.MotherID
INNER JOIN ChildTable AS ct ON ct.FamilyID = ft.FamilyID
INNER JOIN NameTable AS nt2 ON ct.ChildID = nt2.OwnerID
WHERE
     nt1.IsPrimary = 1 AND nt2.IsPrimary = 1
AND  nt1.Given = 'Gloria Chieko'
AND  nt1.Surname = 'Saito'



-- list all children of a particular familyID

SELECT  ft.FamilyID, ct.ChildID, nt2.Given, nt2.Surname
FROM NameTable AS nt1 
INNER JOIN FamilyTable AS ft ON nt1.OwnerID = ft.MotherID
INNER JOIN ChildTable AS ct ON ct.FamilyID = ft.FamilyID
INNER JOIN NameTable AS nt2 ON ct.ChildID = nt2.OwnerID
WHERE
     nt1.IsPrimary = 1 AND nt2.IsPrimary = 1
AND  ft.FamilyID=125

===========================================DIV50==
===========================================DIV50==
Family interpretation

ChildTable
ChildID		ChildTable.ChildID ==> PersonTable.PersonID
FamilyID	ChildTable.FamilyID ==> FamilyTable.FamilyID


FamilyTable

FatherID		FamilyTable.FatherID ==> PersonTable.PersonID
MotherID		FamilyTable.MotherID ==> PersonTable.PersonID

ChildID			FamilyTable.ChildID ==> ChildTable.ChildID



Some examples from DB

eg, me
I am PersonID	1
Maryann PersonID	2

Alban		3
Rose		4

Ferdinand	7
Agnes		8

Leonhard	9
Dorothea	10

FamilyTable
Alban & Rose
FamilyID = 125
FatherId = 3		PersonID
MotherID = 4		PersonID
ChildID = 1			

FamilyTable
Ferdinand & Agnes
FamilyID = 129
FatherId = 7
MotherID = 8
ChildID = 3

FamilyTable
Richard & Gloria
FamilyID = 127
FatherId = 1
MotherID = 6
ChildID = 2360

ChildTable
RecID = 797
ChildID = 1
FamilyID = 125

ChildTable
RecID = 748
ChildID = 3
FamilyID = 129

PersonTable
PersonID = 1
ParentID = 125
SpouseID =127

SpouseID points to 
FamilyID =127 
Richard & Gloria 
perople 1-6 
childID 2360  


ChildTable
RecID = 25
ChildID = 2360
FamilyID = 127

PersonTable
PersonID = 1
ParentID = 125
SpouseID = 127

Person can link to multiple families/parent sets

Family/parent set can link to multiple people/children

there are links inPerson Table for primary parent family and primary spouse
but these are for limited use and loow for only "primary" results.



person    child    family(parents)

family    child     person(kids)



FamilyTable               ChildTable            NameTable
FamilyID     <==           FamilyID
ChildID      ==>           ChildID     <==       OwnerID
MotherID
FatherID


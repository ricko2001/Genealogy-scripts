--[REL: ancestors]
--SQL_QUERY =
  -- Hard coded for starting with PersonID/RIN = 2361  CAO
  -- See line 3         SELECT   2361   AS C_StartPerson
  -- C_BirthParentOnly = 0 or 1.   1=only birth parents included
  WITH RECURSIVE
  constants(C_StartPerson, C_BirthParentOnly) AS (
    SELECT   2361   AS C_StartPerson,
                1   AS C_BirthParentOnly
    ),
  cousin_of(CousinID) AS (
    SELECT AncestorID FROM ancestor_of
      UNION 
      SELECT ChildID FROM child_of
        INNER JOIN cousin_of ON ParentID = CousinID
    ),
  ancestor_of(AncestorID) AS (
    SELECT ParentID FROM parent_of
      WHERE ChildID=(SELECT C_StartPerson FROM constants)
    UNION
    SELECT ParentID FROM parent_of
      INNER JOIN ancestor_of ON ChildID = AncestorID
    ),
  parent_of(ChildID, ParentID) AS (
    SELECT ct.ChildID, FatherID AS ParentID
      FROM ChildTable AS ct
      LEFT JOIN FamilyTable USING(FamilyID)
      WHERE ParentID <> 0
        AND CASE (SELECT C_BirthParentOnly FROM constants)
            WHEN 1 THEN RelFather=0 ELSE 1
            END
    UNION
    SELECT ct.ChildID, MotherID AS ParentID
      FROM ChildTable AS ct
      LEFT JOIN FamilyTable USING(FamilyID)
      WHERE ParentID <> 0
        AND CASE (SELECT C_BirthParentOnly FROM constants)
            WHEN 1 THEN RelMother=0 ELSE 1
            END
    )
  SELECT AncestorID AS PersonID FROM ancestor_of
  --


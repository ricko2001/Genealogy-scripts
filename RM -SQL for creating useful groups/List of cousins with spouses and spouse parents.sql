--[REL: cousin+spouses+parents]
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
    ),
  child_of(ParentID, ChildID) AS (
    SELECT FatherID, ct.ChildID FROM FamilyTable
      LEFT JOIN ChildTable as ct USING(FamilyID)
      WHERE FatherID <> 0
        AND CASE (SELECT C_BirthParentOnly FROM constants)
            WHEN 1 THEN RelFather=0 ELSE 1
            END
    UNION
    SELECT MotherID, ct.ChildID FROM FamilyTable
      LEFT JOIN ChildTable as ct USING(FamilyID)
      WHERE MotherID <> 0
        AND CASE (SELECT C_BirthParentOnly FROM constants)
            WHEN 1 THEN RelFather=0 ELSE 1
            END
    ),
  spouse_of(PersonID, SpouseID) AS (
    SELECT ft.FatherID AS PersonID, ft.MotherID AS SpouseID
      FROM FamilyTable AS ft
      WHERE PersonID <> 0 AND SpouseID <> 0
    UNION
    SELECT ft.MotherID AS PersonID, ft.FatherID AS SpouseID
      FROM FamilyTable AS ft
      WHERE PersonID <> 0 AND SpouseID <> 0
    ),
  cousin_spouse_of(SpouseID) AS (
    SELECT SpouseID AS PersonID
      FROM spouse_of AS so
      INNER JOIN cousin_of AS co ON co.CousinID = so.PersonID
    ),
  cousin_spouse_parent_of(ParentID) AS (
    SELECT ParentID
      FROM parent_of AS po
      INNER JOIN cousin_spouse_of AS cso ON cso.SpouseID = po.ChildID
    )
  SELECT CousinID AS PersonID FROM cousin_of
  UNION
  SELECT SpouseID AS PersonID FROM cousin_spouse_of
  UNION
  SELECT ParentID AS PersonID FROM cousin_spouse_parent_of
  --

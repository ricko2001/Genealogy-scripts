-- [FACT-any: role]
-- SQL_QUERY =
  -- Query on Role Name and optionally, FactType Name
  WITH
  constants(C_FactName, C_RoleName) AS (
     SELECT   '%'             AS C_FactName,
              'spouse'        AS C_RoleName
    )
  SELECT pt.PersonID
    FROM PersonTable       AS pt
  INNER JOIN WitnessTable  AS wt  ON wt.PersonID = pt.PersonId
  INNER JOIN RoleTable     AS rt  ON rt.RoleID = wt.Role
  INNER JOIN FactTypeTable AS ftt ON ftt.FactTypeID = rt.EventType
  WHERE ftt.Name     LIKE (SELECT C_FactName FROM constants)
    AND  rt.RoleName LIKE (SELECT C_RoleName FROM constants)


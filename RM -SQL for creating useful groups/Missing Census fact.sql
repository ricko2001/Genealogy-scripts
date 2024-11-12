  -- Search for missing Census on people with constraints:
  -- people who might be in census but have no FACT or SHARED FACT
  -- Requires Birth place in "United States"
  -- Requires Birth birth date in specified range (between YearBirth and YearCensus)
  -- Death date after YearCensus or no DeathFact
  -- Person does not have a Census fact or shared census fact (Description starts with YearCensus)
  -- Does not find people not born in US but residing in USA in 1950
  -- Does not support Census Family type event.
  -- TO USE: EDIT LINES 14 TO 16
  -- (make place '' for no selection of birth place e.g. if places do not include country)
  --
  WITH
  constants(C_YearCensus, C_YearBirth, C_PlaceBirth) AS (
    SELECT   1930            AS C_YearCensus,
             1830            AS C_YearBirth,
             'United States' AS C_PlaceBirth
  ),
  existing_events AS  -- All census events whose Description starts with YearCensus
  (
  SELECT EventID
  FROM EventTable AS et
  INNER JOIN FactTypeTable AS ftt ON et.EventType = ftt.FactTypeID
  WHERE
      et.OwnerType = 0
  AND et.Details LIKE ( (SELECT C_YearCensus FROM constants) || '%') COLLATE NOCASE
  AND ftt.Name = 'Census' COLLATE NOCASE
  )
  --
  SELECT personID
  FROM PersonTable as pt
    INNER JOIN PlaceTable AS plt ON et_birth.PlaceID = plt.PlaceID
    INNER JOIN EventTable AS et_birth ON et_birth.OwnerID = pt.PersonID
                                      AND et_birth.EventType = 1
    LEFT JOIN EventTable AS et_death  ON et_death.OwnerID = pt.PersonID
                                      AND et_death.EventType = 2
  WHERE
    plt.Name LIKE '%' || (SELECT C_PlaceBirth FROM constants) || '%'
    AND  CAST(SUBSTR(et_birth.DATE, 4,4) as Integer) < CAST((SELECT C_YearCensus FROM constants) as Integer)
    AND  CAST(SUBSTR(et_birth.DATE, 4,4) as Integer) > CAST((SELECT C_YearBirth FROM constants) as Integer)
    AND ( CAST(SUBSTR(et_death.DATE, 4,4) as Integer) > CAST((SELECT C_YearCensus FROM constants) as Integer)
          OR et_death.OwnerID IS NULL)
  --
  EXCEPT
  -- people who have a census fact of YearCensus type
  SELECT et.OwnerID
  FROM EventTable AS et
  INNER JOIN existing_events ON existing_events.EventID = et.EventID
  --
  EXCEPT
  -- people who are witness to a census fact of YearCensus type
  SELECT wt.PersonID
  FROM WitnessTable AS wt
  INNER JOIN existing_events ON existing_events.EventID = wt.EventID
  --
  ORDER BY 1 ASC;
  --

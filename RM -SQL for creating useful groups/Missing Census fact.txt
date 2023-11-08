  -- Search for missing 1950 Census on appropriate people
  -- people who might be in 1950 census but have no FACT or SHARED FACT
  -- Requires Birth place in United States
  -- Requires Birth birth date in specified range
  -- Death Fact not required
  -- Does not find people with Census fact or shared fact Detail 1950%
  -- Does not find people not born in US but residing in USA in 1950
  --
  WITH existing_events AS
  (
  SELECT EventID
  FROM EventTable AS et
  INNER JOIN FactTypeTable AS ftt ON et.EventType = ftt.FactTypeID
  WHERE
      et.OwnerType = 0
  AND et.Details LIKE ('1950%')
  AND ftt.Name = 'Census'
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
    plt.Name LIKE '%United States%'
    AND SUBSTR(et_birth.DATE, 4,4) < '1950'
    AND SUBSTR(et_birth.DATE, 4,4) > '1850'
    AND (SUBSTR(et_death.DATE, 4,4) > '1950' OR et_death.OwnerID IS NULL)
  --
  EXCEPT
  -- people who have a census fact of specified type
  SELECT et.OwnerID
  FROM EventTable AS et
  INNER JOIN existing_events ON existing_events.EventID = et.EventID
  --
  EXCEPT
  -- people who are witness to a census fact of specified type
  SELECT wt.PersonID
  FROM WitnessTable AS wt
  INNER JOIN existing_events ON existing_events.EventID = wt.EventID
  --
  ORDER BY 1 ASC;
  --

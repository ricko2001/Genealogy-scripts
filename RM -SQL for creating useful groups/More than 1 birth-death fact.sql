
SELECT et.OwnerID as PersonID
FROM EventTable et
WHERE et.OwnerType = 0 and EventType = 1 -- Birth 
GROUP BY et.OwnerID
HAVING COUNT(EventID) > 1


SELECT et.OwnerID as PersonID
FROM EventTable et
WHERE et.OwnerType = 0 and EventType = 2 -- Death 
GROUP BY et.OwnerID
HAVING COUNT(EventID) > 1
select  pt.PersonID
from PersonTable as pt 
join EventTable as et1 on et1.OwnerID = pt.PersonID
join CitationLinkTable as clt on clt.OwnerID = et1.EventID
join CitationTable as ct on ct.CitationID = clt.CitationID
where et1.EventType = 4 -- Burial
and   clt.OwnerType = 2
and   ct.SourceID = 6276  -- Find_a_Grave_db

intersect

select  pt.PersonID
from PersonTable as pt 
where pt.PersonID not in 
( select  EventTable.OwnerID from EventTable 
  where EventTable.EventType = 1094 -- ID_Fag
)
order by pt.PersonID desc


-- Or
-- select a.* from a
-- left outer join b on a.id = b.a_id
-- where b.a_id is null
-- 
-- https://stackoverflow.com/questions/38549/what-is-the-difference-between-inner-join-and-outer-join
-- 
-- add test for fag citation
-- 
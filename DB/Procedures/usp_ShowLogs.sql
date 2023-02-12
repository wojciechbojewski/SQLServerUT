create procedure usp_ShowLogs
(
	@event_type tinyint
)
as
select
	l.id as LogID,
	u.name as UserName,
	e.name as EventName,
	l.created
from
	Logs l
	left join Events e
		on l.event_id = e.id
	left join Users u
		on l.user_id = u.id
where
	e.id = @event_type
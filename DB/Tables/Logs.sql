create table Logs
(
	id int identity(1,1) primary key,
	user_id int,
	event_id int,
	created datetime default GETDATE()
)
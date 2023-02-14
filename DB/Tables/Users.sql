create table Users
(
	id int identity(1,1) primary key,
	name varchar(50),
	created datetime default GETDATE()
)
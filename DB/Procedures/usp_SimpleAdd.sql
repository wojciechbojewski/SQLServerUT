create procedure usp_SimpleAdd
(
	@a int,
	@b int
)
as
begin
	return @a+@b
end
create function usf_SimplyAdd
(
	@a int,
	@b int
)
returns int
as
begin
	return @a+@b
end
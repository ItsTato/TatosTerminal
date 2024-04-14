return function()
	if Session:isRunning() then -- just in case.
		Session:Exit();
	end;
end;
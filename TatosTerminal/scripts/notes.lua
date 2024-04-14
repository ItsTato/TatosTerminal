--Python:Import("sleep","time")(1);
	
--local time = Python:Import("time")
--time.sleep(1);

--local parts = Python:Require({ "sleep", "time" }, "time");
--print(parts.time());

--local modules = Python:Require({ "time", "os" });
--print(modules.time.time());

--[[
alertnative syntax:

	local function run(ctx)
		...
	end;

	return run;

--]]
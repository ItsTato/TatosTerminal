return function()
	local os = Python:Require({ "path", "listdir" }, "os");
	local raw_scripts = list.curate(os.listdir(os.path.join(TTMeta.directory,"scripts")));
	local scripts = {};

	for _, directory in ipairs(raw_scripts) do
		if os.path.isdir(os.path.join(os.path.join(TTMeta.directory,"scripts"),directory)) then
			table.insert(scripts,directory);
		end;
	end;

	print("SUSM | Installed Packages @ "..TTMeta.directory.."/scripts");
	local final = "";
	for index, directory in ipairs(scripts) do
		if index == 1 then
			final = directory
		else
			final = final..", "..directory;
		end;
	end;

	print(final);

end;

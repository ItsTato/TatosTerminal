return function()
	local os = Python:Require({ "path", "listdir" },"os");
	local scripts = list.curate(os.listdir(os.path.join(TTMeta.directory,"scripts")));
	for index, directory in ipairs(scripts) do
		if not os.path.isdir(os.path.join(os.path.join(TTMeta.directory,"scripts"),directory)) then
			list.remove(scripts,index);
		elseif string.find(directory,".") then
			list.remove(scripts,index);
		else
			print(index.." "..directory);
		end;
	end;
	print(scripts);
end;

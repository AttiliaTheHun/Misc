from os import listdir
import re

targetDir="/home/johnw/GitStuff/Misc/underhand_website/eve/events/"
outputDir="/home/johnw/GitStuff/Misc/underhand_website/_source/events/"

exp = "<title.*?>(.+?)</title>"
pattern = re.compile(exp)

f = listdir(targetDir)

print(f)

for filename in f:
	if filename.endswith(".php"):
		with open(targetDir + filename) as file:
			content = file.read()
			title = re.findall(pattern,content)[0]
			start = content.index("<div class=\"content\">");
			end = content.index("<?php include '../server-files/footer.php' ?>");
			with open(outputDir + filename.replace(".php", ".html"), "a") as target:
				target.write(f"---\ntitle: {title}\ndescription: Underhand gods.\nlayout: base.html\n---\n\n")
				target.write(content[start:end])
			print(f"Done {targetDir + filename} -> {outputDir + filename.replace(".php", ".html")}");

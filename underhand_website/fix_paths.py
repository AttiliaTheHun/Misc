from os import listdir
import re

targetDir="/home/johnw/GitStuff/Misc/underhand_website/_source/events/"

f = listdir(targetDir)

for filename in f:
	if filename.endswith(".html"):
		content = ""
		with open(targetDir + filename, "r") as file:
			content = file.read()
			content = content.replace("/res/Card", "/assets/images/cards/Card");
			content = content.replace("/res/", "/assets/images/");
		with open(targetDir + filename, "w") as file:
			file.write(content);
			print(f"Done {targetDir + filename}");

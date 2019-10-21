import os
import re

# Path of unparsed papers
path_unparsed = "./papers_to_index/"

# Path of parsed papers
path_parsed = "./parsed_paper/"

# Content of all papers
papers = []

# Get files in the unparsed papers folder
files = os.listdir(path_unparsed)

for file in files:
    # If file is not a folder
    if not os.path.isdir(file):
        with open(path_unparsed + file, encoding="utf8") as f:
            text = f.read()
            res = re.findall('<title>(.*)</title>',text)[0]
            res += " "
            res += re.findall('<abstract>(.*)</abstract>',text)[0]
            # If file is not empty
            if res.strip():
                papers.append(res) 

# Convert papers to MeTA format
papers = [' '.join(line.split('\n')) for line in s]
papers = '\n'.join(s)

with open(path_parsed + 'parsed_paper.dat', 'w', encoding="utf8") as f:
    f.write(s)

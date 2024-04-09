import os, argparse
from pathlib import Path
parser = argparse.ArgumentParser()
parser.add_argument(
		'--inScriptName', type=Path,
		help='Input Script to Combine'
)

parser.add_argument(
		'--outfolder', type=Path,
		help='Output path'
)

args = parser.parse_args()

IN_SCRIPTNAME = args.inScriptName
 
# Creating a list of filenames
filenames = ['head.txt', IN_SCRIPTNAME, 'tail.txt']
out = ""

# Iterate through list
for names in filenames:
    data = ""
    # Open each file in read mode
    with open(names) as infile:

        # read the data from file1 and
        # file2 and write it in file3
        data = infile.read()
    out += data
    out += '\n'
    # Add '\n' to enter data of file2
    # from next line

out += f'jump {IN_SCRIPTNAME}'

outfile = os.path.join(args.outfolder, IN_SCRIPTNAME)
with open(outfile, 'w') as outfile:
    outfile.write(out)
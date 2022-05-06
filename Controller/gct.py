from time import clock_getres
import tabula
import os
import sys
import json

# uncomment if you want to pass pdf file from command line arguments
# import sys
 
# read PDF file
# uncomment if you want to pass pdf file from command line arguments
# tables = tabula.read_pdf(sys.argv[1], pages="all")
# new_path=os.path.dirname(__file__)

url = sys.argv[1]
tables = tabula.read_pdf(url, pages="all", output_format="json", encoding="utf-8", stream=False, lattice=True)


# json_object = json.dumps(tables, indent = 4, skipkeys=True)
json_string = json.dumps(tables)
print(str(json_string))


# with open("output.json", "w") as jsonFile:
#     json.dump(tables, jsonFile, indent=4)
# with open(os.path.join(new_path, "output.json"), "w", encoding='utf-8') as outfile:
#     outfile.write(json_object)

# convert all tables of a PDF file into a single CSV file
# supported output_formats are "csv", "json" or "tsv"
# tabula.convert_into(url, os.path.join(new_path, "output"),'json',pages="all", stream=True)
# pd.read_csv
# output  = open(os.path.join(new_path, "output"))
# data = json.load(output)
# convert all PDFs in a folder into json format
# `pdfs` folder should exist in the current directory
# tabula.convert_into_by_batch("pdfs", output_format="json", pages="all")
import tabula
import os
import sys
import json

# uncomment if you want to pass pdf file from command line arguments
# import sys
 
# read PDF file
# uncomment if you want to pass pdf file from command line arguments
# tables = tabula.read_pdf(sys.argv[1], pages="all")
new_path=os.path.dirname(__file__)

url = sys.argv[1]
tables = tabula.read_pdf(url, pages="all")
# print(tables)
 
 
# convert all tables of a PDF file into a single CSV file
# supported output_formats are "csv", "json" or "tsv"
tabula.convert_into(url, os.path.join(new_path, "output"),'json',pages="all", stream=True)
# pd.read_csv
output  = open(os.path.join(new_path, "output"))
data = json.load(output)
print(data)
# convert all PDFs in a folder into json format
# `pdfs` folder should exist in the current directory
# tabula.convert_into_by_batch("pdfs", output_format="json", pages="all")
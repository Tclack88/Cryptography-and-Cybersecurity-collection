from fpdf import FPDF
import sys


infile = sys.argv[1]
outfile = sys.argv[2]

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=15)
with open(infile,'r') as f:
    for x in f:
        pdf.cell(200, 10, txt=x, ln=1, align='C')

pdf.output(outfile)

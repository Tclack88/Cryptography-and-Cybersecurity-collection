from fpdf import FPDF
from hashlib import md5
import re
import os

def make_pdf(i,outfile):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt=str(i), ln=1, align='C')
    pdf.output(outfile)

collisions = []
integers = []
i = 0
while len(collisions) < 2:
    outfile = f'pdfs/{i}.pdf'
    make_pdf(i,outfile)
    with open(outfile, 'rb') as f:
        data = f.read()
        checksum = md5(data).hexdigest()
        if re.match(r'0e\d+\b',checksum):
            collisions.append(checksum)
            integers.append(i)
            print(f'zero found! "{checksum}" for {i}')
        else:
            os.remove(outfile)
    i +=1

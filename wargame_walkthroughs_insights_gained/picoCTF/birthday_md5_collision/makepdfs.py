from fpdf import FPDF
from hashlib import md5

def make_pdf(i,outfile):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt=str(i), ln=1, align='C')
    pdf.output(outfile)

checksums = {}
i = 0
while i<100:
    outfile = f'pdfs/{i}.pdf'
    make_pdf(i,outfile)
    with open(outfile, 'rb') as f:
        data = f.read()
        checksum = md5(data).hexdigest()
        if checksum in checksums:
            print(f'collision found! "{checksum}" for {i} and {checksums[checksum]}')
            break
        else:
            checksums[checksum] = i

    i +=1

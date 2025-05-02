import PyPDF2,os

def pdf_to_text(pdf_path, output_txt):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    # Write the extracted text to a text file
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

if __name__ == "__main__":
    pdf_path = 'gfg.pdf'
    pdfDir='D://stuff//NLP//2017 Papers//PDF'
    txtDir='D://stuff//NLP//2017 Papers//TXT'
    output_txt = 'gfg.txt'
    flag=0
    for file in os.listdir('D://stuff//NLP//2017 Papers//PDF'):
        '''if file[:-4]!='r1lUOzWCW' and flag==0:
            continue
        else:
            flag=1'''
        print(pdfDir+'//'+file,txtDir+'//'+file[:-4])
        try:
            pdf_to_text(pdfDir+'//'+file,txtDir+'//'+file[:-4]+'.txt')
        except:
            print('ERROR')
            continue

    print("PDF converted to text successfully!")
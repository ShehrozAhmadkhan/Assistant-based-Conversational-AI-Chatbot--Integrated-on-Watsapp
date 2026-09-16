import PyPDF2

def load_data(file_path):
    file = open(file_path,"rb")
    book = PyPDF2.PdfReader(file)
    pdfinstring = ""

    for page in book.pages:
        text = page.extract_text()
        if text:
            pdfinstring += text + "\n"

    file.close()

    return pdfinstring
import os
import textract
from mimetypes import guess_extension
class extractor:
    def __init__(self):
        self.self = None


    def pdfhandler(self,pdfpath):
        text = textract.process(pdfpath,encoding='ascii',extension='pdf')
        if type(text) == type(bytes()):
            return text.decode()
            
        return text
    def htmlhandler(self,htmlpath):
        text = textract.process(htmlpath,encoding='ascii',extension='html')
        return text

    def texthandler(self,txtpath):
        text = open(txtpath,'rt')
        return text.read()

    def dochandler(self,docpath):
        return textract.process(docpath,encoding='ascii',extension="doc")

    def docxhandler(self,docx):
        return textract.process(docx,encoding='ascii',extension='docx')

    def pptxhandler(self,pptx):
        return textract.proxess(pptx,encoding='ascii',extension='pptx')
    
    def csvhandler(self,csv):
        return textract.process(csv,encoding='ascii',extension='csv')

    def epubhandler(self,epub):
        return textract.process(epub,encoding='ascii',extension='epub')

    def emlhandler(self,eml):
        return textract.process(eml,encoding='ascii',extension='eml')

    def msghandler(self,eml):
        return textract.process(eml,encoding='ascii',extension='.msg')

    def jpghandler(self,jpg):
        return textract.process(jpg,encoding='ascii',extension='jpg')

    def mp3handler(self,path):
        return textract.process(path,encoding='ascii',extension='mp3')

    def gifhandler(self,path):
        return textract.process(path,encoding='ascii',extension='gif')
    
    def jsonhandler(self,path):
        return textract.process(path,encoding='ascii',extension='json')
    
    def odthandler(self,path):
        return textract.process(path,encoding='ascii',extension='odt')

    def ogghandler(self,path):
        return textract.process(path,encoding='ascii',extension='ogg')
    
    def pnghandler(self,path):
        return textract.process(path,encoding='ascii',extension='png')
    
    def pshandler(self,path):
        return textract.process(path,encoding='ascii',extension='ps')

    def rtfhandler(self,path):
        return textract.process(path,encoding='ascii',extension='rtf')
    
    def tiffhandler(self,path):
        return textract.process(path,encoding='ascii',extension='tiff')
    
    def wavhandler(self,path):
        return textract.process(path,encoding='ascii',extension='wav')

    def xlsxhandler(self,path):
        return textract.process(path,encoding='ascii',extension='xlsx')
    
    def xlshandler(self,path):
        return textract.process(path,encoding='ascii',extension='xls')

    def defaulthandler(self,_):
        return 'null'

extension_and_determined_handler = {
    ".csv": "csvhandler",
    ".doc": "dochandler",
    ".docx": "docxhandler",
    ".eml": "emlhandler",
    ".epub": "epubhandler",
    ".gif": "gifhandler",
    ".html": "htmlhandler",
    ".jpg": "jpghandler",
    ".json": "jsonhandler",
    ".mp3": "mp3handler",
    ".ogg": "ogghandler",
    ".pdf": "pdfhandler",
    ".png": "pnghandler",
    ".pptx": "pptxhandler",
    ".ps": "pshandler",
    ".rtf": "rtfhandler",
    ".tiff": "tiffhandler",
    ".txt": "texthandler",
    ".wav": "wavhandler",
    ".xls": "xlshandler",
    ".xlsx": "xlsxhandler"
}

def init(filepath,extension=None):
    """
    extract text from file:
    
    Arguements:
        filepath: an string
        extension: an string

    Returns:
        return a dictionary with value content  and extesion which contains 
        extracted text and extenstion respectively.
    """
    if not os.path.isfile(filepath):
            return filepath + "doesn't exist"

    if extension is None:
        mime = os.popen(f"file --mime-type  '{filepath}'").read()
     
        mime_type = mime.split(' ')[-1][:-1]
        
        extension = guess_extension(mime_type)
       
    get_handler = extension_and_determined_handler.get(extension,'defaulthandler')
    raw_text_from_file = getattr(extractor(),get_handler)(filepath)
    output = dict()
    output['content'] = 'null'
    if raw_text_from_file:
        if type(raw_text_from_file) == type(bytes()):
            raw_text_from_file = raw_text_from_file.decode()
            
        ascii_only_string = raw_text_from_file.encode('ascii','ignore').decode()
        output['content'] = " ".join(ascii_only_string.split())

    output['extension'] = extension
    output['mime'] = mime_type
            
    return output



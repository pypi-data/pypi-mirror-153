import os
from pathlib import Path
# import cv2 as cv
# import pytesseract as ts

import pdfkit
from flask import request, make_response


class DataExtractor:
    """
    A resource for extracting invoice data using invoice2data library
    """

    def __init__(self):
        self.file_storage_path = os.environ.get('de_storage_path', '/flask_downloads')
        self.template_folder = os.environ.get('de_templates_path', '/DocDataExtraction') # Changed by Pravin K on 9-JUNE-21 [As per K B sir suggestion changed root folder inv2data_templates to DocDataExtraction ] 

    def get(self):
        final_result = {}

        try:
            invoice_file_part = request.files.get('file_0', None)

            if not invoice_file_part:
                raise Exception('Invoice file not found in request payload')

            #Added By Prain K on 26-APR-21 START
            print("inside get",invoice_file_part)
            given_temp_path = request.args.get('extract_templ', None)
            print("inside get:extract_templ:given_temp_path[",given_temp_path,"]")
            if given_temp_path:
                if given_temp_path != 'DocDataExtraction': # Changed by Pravin K on 9-JUNE-21 [As per K B sir suggestion changed root folder inv2data_templates to DocDataExtraction ] 
                    self.template_folder =  self.template_folder +'/'+given_temp_path+'/'

            print("inside get template_folder[", self.template_folder,"]")
            #Added By Prain K on 26-APR-21 END

            filename = invoice_file_part.filename
            file_path = os.path.join(self.file_storage_path, invoice_file_part.filename)
            print("inside file_path",file_path)
            
            if '.TXT' in filename or '.txt' in filename or '.PDF' in filename or '.pdf' in filename or '.xls' in filename or '.xlsx' in filename:
                input_reader = request.args.get('input_reader', 'pdftotext')

            if '.png' in filename or '.PNG' in filename or '.jpg' in filename or '.JPG' in filename or '.jpeg' in filename or '.JPEG' in filename:
                input_reader = request.args.get('input_reader', 'tesseract')

                print("Read::image:",file_path)
                #custom_oem_psm_config = r' --oem 2, --psm 3 '
                # print("Read::file_path:",file_path)
                # img = cv.imread(file_path,0)
                # image_text = ts.image_to_string(img,config = custom_oem_psm_config)
                # print("Read::image_text:",image_text)
                print("Read Image  file using tesseract::input_reader:",input_reader)

            Path(self.file_storage_path).mkdir(parents=True, exist_ok=True)
            
            invoice_file_part.save(file_path)

            if '.TXT' in filename or '.txt' in filename:
                print("Read Text file")
                dot_ind = filename.rindex('.')
                print('dot index'+str(dot_ind))
                only_name = filename[:dot_ind]
                print('only_name'+only_name)

                html_file_name = self.file_storage_path + "/" + only_name + ".html"
                output_file_name = self.file_storage_path + "/" + only_name + ".pdf"
                with open(file_path) as file:
                    with open(html_file_name, "w") as output:
                        file = file.read()
                        file = file.replace("\n", "<br>")
                        output.write(file)

                pdfkit.from_file(html_file_name, output_file_name)
                try:
                    os.remove(file_path)
                    file_path = os.path.join(html_file_name)
                    os.remove(file_path)
                except Exception as ex:
                    print("DataExtractor: Exception while removing file", ex)

                file_path = os.path.join(self.file_storage_path, output_file_name)
            if '.PDF' in filename or '.pdf' in filename:
                print("Read pdf file")
                # Added by Akshay S on 07-MAY-21 [To extract Images inside PDF] START
                import fitz
                # from PIL import Image
                from pdf2image import convert_from_path
                # import ocrmypdf
                file_path = os.path.join(self.file_storage_path, invoice_file_part.filename)
                pdf_file = fitz.open(file_path)
                for page_index in range(len(pdf_file)):
                    page = pdf_file[page_index]
                    image_list = page.getImageList()
                print(page.getImageList())
                
                if image_list: 
                    print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
                    input_reader = request.args.get('input_reader', 'tesseract')
                    new_img_file_path = os.path.join(self.file_storage_path, 'out.jpg')
                    print("file_path--["+file_path+"],new_img_file_path["+new_img_file_path+"]")
                    images = convert_from_path(file_path, 200)
                 
                    for page in images: 
                        page.save(new_img_file_path, 'JPEG')
                       #file_path = new_img_file_path #Changed by Pravin K on 6-june-21
                    

                else:
                    print("[!] No images found on page", page_index)  
                # Added by Akshay S on 07-MAY-21 [To extract Images inside PDF] END  

            if '.xls' in filename or '.xlsx' in filename:
                print("Read Excel file")

            from invoice2data import extract_data
            from invoice2data.extract.loader import read_templates

            print("Read::self.template_folder:",self.template_folder)
            if os.path.exists(self.template_folder):
                templates = read_templates(self.template_folder)
            print("Read::self.template_folder:",templates)
            input_reader_module = self.get_input_reader_module(input_reader)
            print("input_reader_module :", input_reader_module )
            # Added by Pravin START
            input_document_type = request.args.get('input_document_type', '')
            print("input_document_type [" + input_document_type + "]")
            if input_document_type == 'cheque':
                from proteus_services.resources.read_cheque import ReadCheque
                read_cheque = ReadCheque()
                result = read_cheque.read_cheque_details(file_path, templates, input_reader_module)
            # Added by Pravin END
            else:
                print("extracting data start::",file_path)
                result = extract_data(invoicefile=file_path,
                                      templates=templates,
                                      input_module=input_reader_module)

            try:
                os.remove(file_path)
            except Exception as ex:
                print("DataExtractor: Exception while removing file", ex)

            print('result'+str(result))    
            if not isinstance(result, bool):
                result = self._reform_result(result)

            final_result['status'] = 1
            final_result['result'] = result
        except Exception as ex:
            final_result['status'] = 0
            final_result['error'] = str(ex)

        return final_result # Changed by Pravin k on 27-JAN-20 START
        #return make_response(str(final_result))

    @staticmethod
    def get_input_reader_module(input_reader):
        if input_reader == 'pdftotext':
            from invoice2data.input import pdftotext
            return pdftotext
        elif input_reader == 'pdfminer':
            from invoice2data.input import pdfminer_wrapper
            return pdfminer_wrapper
        elif input_reader == 'tesseract':
            from invoice2data.input import tesseract
            return tesseract

        raise Exception('Invalid input reader "{}"'.format(input_reader))

    @staticmethod
    def _reform_result(result):
        if result is None:
            return '{}'

        result_copy = {}

        for prop in result:
            result_copy[prop] = str(result[prop])

        return result_copy

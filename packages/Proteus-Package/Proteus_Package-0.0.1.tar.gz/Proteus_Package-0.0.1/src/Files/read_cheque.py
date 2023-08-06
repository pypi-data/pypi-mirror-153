import cv2 as cv
import os
import pytesseract as ts
try:
    from PIL import Image
except ImportError:
    import Image
from invoice2data import extract_data
import re

class ReadCheque:
		
	def read_cheque_details(self,file_name, templates, input_reader_module ):
		print("cheque_details for file_name : "+file_name )

		img = cv.imread(file_name,0)
		
		(h, w,) = img.shape[:2]
		bottom_height = int(h - (h * 0.2))
		
		mid_end = int(h-(h-(int(h - (h * 0.15)))))
		mid_width_fo_acc_no = int(w - (w * 0.3))
		
		mid_width_fo_acc_no_img = img[0:mid_end, 0:mid_width_fo_acc_no]
		bottom = img[bottom_height:h, 0:w]
		
		cv.imwrite('mid_width_fo_acc_no.jpg',mid_width_fo_acc_no_img)
		cv.imwrite('bottom_part_cheque.jpg',bottom)
		
		custom_oem_psm_config = r' --oem 2, --psm 3 '
		result = extract_data(invoicefile=file_name,
							  templates=templates,
							  input_module=input_reader_module)
                                  
		cheque_no_details = ts.image_to_string(bottom, lang = 'mcr',config = custom_oem_psm_config)
	
		# read data to show to check the data read using tesseract .
		#mid_cheque_data = ts.image_to_string(mid_width_fo_acc_no_img, lang = 'eng', config = custom_oem_psm_config)
		#print("mid_cheque_data : "+mid_cheque_data)
		print("cheque_result: " + str(result) )
		print("cheque_no_details : "+cheque_no_details)
		
		if isinstance(result, bool):
			result = {}
		else:
			cheque_no = re.search("c(\d*\s*)*c",cheque_no_details)
			if cheque_no is not None:
				cheque_no = cheque_no.group()
				cheque_no = cheque_no.replace("c","").replace("\s","")
			else:
				cheque_no='';

			result["cheque_no"] = cheque_no
			result["ref_no"] = cheque_no

		print(result)
		
		try:
			os.remove("mid_width_fo_acc_no.jpg")
			os.remove("bottom_part_cheque.jpg")
		except Exception as ex:
			print("readCheque: Exception while removing cheque parts file", ex)

		return result;

import re
import pycurl
from StringIO import StringIO
import sys
import argparse
import os

__debug_flag= False

#>>LAYER 0------------------------------------------
def print_debug(text):
	if __debug_flag:
		print text

def get_cmd_arg():
	parser = argparse.ArgumentParser()
	parser.add_argument("dictionary_src_file", type=str,
                    help="Dictionary file is required.")
	parser.add_argument("urls_file", type=str,
                    help="Properties urls file is required.")
	parser.add_argument("text_to_translate", type=str,
                    help="Text to translate requited.")
	parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
	return parser.parse_args()	

def clear_screen():
	os.system('cls')  # For Windows
	os.system('clear')  # For Linux/OS X

def get_all_text_from_file(file_name):
	os.system("touch " + file_name)
	result= ""
	with open(file_name, 'r') as content_file:
		result = content_file.read()
	return result

def get_all_matches(src_text, regular_ex):
	result =re.findall(regular_ex, src_text)
	return result
	
def compile_translate_regx():
	result =re.compile('ltr ">([^\r\n]+)<.*[\r\n]*(.*pos ">\[([\w/]+)\])?', re.UNICODE|re.MULTILINE)
	return result

def compile_dict_translate_regx(tr_text):
	result= re.compile('^(\s*>>\s*{}\s*\|[^\r\n]*[\r\n]+[^<]+)'.format(tr_text), re.UNICODE|re.MULTILINE)
	return result

def compile_pronc_regx():
	result =re.compile('class="SEP PRON-before"> /</span>([^<]+)<' , re.UNICODE|re.MULTILINE)
	return result
	
def compose_url(url, src_text):
	result= url.format(src_text.replace(" ","+"))
	return result
	
def get_text_from_url(url, regx):
  buffer = StringIO()
  c = pycurl.Curl()
  c.setopt(c.URL, url)
  c.setopt(c.FOLLOWLOCATION, True)
  c.setopt(c.WRITEDATA, buffer)
  c.perform()
  c.close()
  body = buffer.getvalue()
  result= re.findall(regx, body)
  return result
	
def update_dictionary(text_src, text_tr, word_pronc, dict_src):

	if len(text_tr) == 0:
		print_debug("Translate text is empty")
		return
	
	word_tr_sort= sorted(text_tr, key=lambda tup: (tup[2]))
	pronc= ""
	if len(word_pronc) > 0:
		pronc= word_pronc[0]
	
	if len(word_tr_sort) > 0:
		with open(dict_src, "a") as myfile:
			myfile.write(">>{}|{}\n".format(text_src, pronc))
			for token in word_tr_sort:
				print_debug(token[0])
				print_debug(token[2])
				myfile.write("  {}{}\n".format(token[0], token[2]))
			myfile.write("<<\n")
#<<

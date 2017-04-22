import re
import urllib2
from StringIO import StringIO
import sys
import argparse
import os
from jproperties import Properties

__debug_flag= False
L1_TAB=""
L0_TAB="  "

#>>LAYER 0
def debug(sep, tag, text):
  if __debug_flag:
    print sep + tag + text

def console(text):
  print text

def get_cmd_arg():
  parser = argparse.ArgumentParser()
  parser.add_argument("text_to_translate", type=str,
                    help="Text to translate requited.")
  parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
  return parser.parse_args()

def clear_screen():
  os.system('cls')  # For Windows
  os.system('clear')  # For Linux/OS X

def get_properties_mng():
  p = Properties()
  with open("config.properties", "rb") as f:
    p.load(f, "utf-8")
  return p

def get_all_text_from_file(file_name):
  os.system("touch " + file_name)
  result= ""
  with open(file_name, 'r') as content_file:
    result = content_file.read()
  return result

def get_all_matches(src_text, regular_ex):
  result =re.findall(regular_ex, src_text)
  return result

def compile_dict_translate_regx(tr_text):
  result= re.compile('^(\s*>>\s*{}\s*\|[^\r\n]*[\r\n]+[^<]+)'.format(tr_text), re.UNICODE|re.MULTILINE)
  return result

def compose_url(url, src_text):
  result= url.format(src_text.replace(" ","+"))
  return result

def get_text_from_url(url, regx):
  hdr= {'User-Agent': 'Mozilla/5.0'}
  req= urllib2.Request(url, headers=hdr)
  response= urllib2.urlopen(req)
  html= response.read()
  result= re.findall(regx, html)
  return result

def update_dictionary(text_src, text_tr, word_pronc, dict_src):
  if len(text_tr) == 0:
    console("Translated text is empty, not updated dicctionary")
    return

  if not isinstance(text_tr[0], tuple):
    text_tr= set(text_tr)

  pronc= ""
  if len(word_pronc) >= 1:
    pronc= word_pronc[0]
#>open dicctionary and update
  with open(dict_src, "a") as myfile:
    myfile.write(">>{}|/{}/\n".format(text_src, pronc))
    for token in text_tr:
      if isinstance(token, tuple):
        myfile.write("  {}:{}\n".format(token[0], token[2].replace(" ", "")))
      else:
        myfile.write("  {}\n".format(token))
    myfile.write("<<\n")
#<
#<<

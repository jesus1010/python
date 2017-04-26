import re
import urllib2
from StringIO import StringIO
import sys
import argparse
import os
from jproperties import Properties
from prettytable import PrettyTable
import unicodedata

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
  parser.add_argument("config_file", type=str,
                    help='File with config data')
  parser.add_argument("text_to_translate", type=str,
                    help="""Simple words like gold, phrasal verbs like turn-off or text like craft-fair (needs - separator)""")
#  parser.add_argument("--help", action="store_true",
#                    help="Valid text, simple word like gold, phrasal verb like turn-off, or simple text  craft-fair")
  return parser.parse_args()

def clear_screen():
  os.system('cls')  # For Windows
  os.system('clear')  # For Linux/OS X

def get_properties_mng(config_file):
  p = Properties()
  with open(config_file, "rb") as f:
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

def compose_url_for_tr(url, src_text):
  src_text= src_text.replace(" ","")
  result= url.format(src_text.replace("-","+"))
  return result

def get_first_html_body_from_url(url_regx):

  hdr= {'User-Agent': 'Mozilla/5.0'}

  result= None
  last_url=None
  html=""
  for item in url_regx:
    if last_url != item[0]:
      console("%s" % item[0])
      req= urllib2.Request(item[0], headers=hdr)
      response= urllib2.urlopen(req)
      html= response.read()
      last_url= item[0]

    result= re.findall(item[1], html)
    if len(result) > 0:
      break

  return result


def clean_pronc_result(pronc):
  result= ""
  if len(pronc) > 0:
    result= pronc[0]
    result= result.replace(" ","")
    result= result.replace("</span>","")
    result= result.replace("<spanclass=\"sp\">" ,"")
    result= result.replace("/" ,"")
    result= result.replace("<spanclass=\"sp\">" ,"")
  return [result]

def update_dictionary(text_src, text_tr, word_pronc, dict_src):
  reload(sys)
  sys.setdefaultencoding('utf8')

  if len(text_tr) == 0:
    console("Translated text is empty, not updated dicctionary")
    return

  if not isinstance(text_tr[0], tuple):
    text_tr= set(text_tr)

  pronc= ""
  if len(word_pronc) >= 1:
    pronc= word_pronc[0]
#>open dicctionary and update
  dict_formater= PrettyTable(border=False, left_padding_width=2)
  dict_formater.field_names = ["1", "2"]
  dict_formater.align["1"]="l"
  dict_formater.align["2"]="l"

  with open(dict_src, "a") as myfile:
    myfile.write("\n")
    myfile.write(">>{}|/{}/\n".format(text_src, pronc))
    for token in text_tr:
      if isinstance(token, tuple):
        dict_formater.add_row([token[0] , token[2].replace(" ", "")])
      else:
        dict_formater.add_row([token[0], ""])

    myfile.write(dict_formater.get_string(header=False))
    myfile.write("\n")
    myfile.write("<<")
#<
#<<

import layer0 as L0
import locale
#>>LAYER 1
SEP= L0.L1_TAB
debug=L0.debug

#-----------------------------
def init_enviroment(env):
#-----------------------------
  locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')
  env['env_init']= False
  try:
    L0.clear_screen()
#<get property sources
    args= L0.get_cmd_arg()
    env['config_file']=args.config_file
    prop_mng= L0.get_properties_mng(env['config_file'])
#<:
#>load propeties into enviroment  
    env['tr_text']=args.text_to_translate
    env['dict_src']=prop_mng['default_dict'][0]
    env['url_pronc']=prop_mng['url_pronc'][0]
    env['url_tr']=prop_mng['url_tr'][0]
    env['url_tr2']=prop_mng['url_tr2'][0]
    env['url_tr3']=prop_mng['url_tr3'][0]
    env['pattern_pronc_uk_word']=prop_mng['pattern_pronc_uk_word'][0]
    env['pattern_pronc_uk_strong_word']=prop_mng['pattern_pronc_uk_strong_word'][0]
    env['pattern_pronc_us_word']=prop_mng['pattern_pronc_us_word'][0]
    env['pattern_pronc_uk_phrasal']=prop_mng['pattern_pronc_uk_phrasal'][0]
    env['pattern_pronc_us_phrasal']=prop_mng['pattern_pronc_us_phrasal'][0]
    env['pattern_pronc_generic']=prop_mng['pattern_pronc_generic'][0]
    env['pattern_pronc_generic2']=prop_mng['pattern_pronc_generic2'][0]
    env['pattern_tr']=prop_mng['pattern_tr'][0]
    env['pattern_tr2']=prop_mng['pattern_tr2'][0]
    env['pattern_tr3']=prop_mng['pattern_tr3'][0]
    env['result']="Not translate"
    env['env_init']= True
    env["env_tr_ok"]= False
#<
  except Exception as ex:
    L0.console(ex)

#-----------------------------
def show_head_banner():
#-----------------------------
  L0.console("------------------------------")
  L0.console("TRANSLATIONS(EN->SPA):")
  L0.console("------------------------------")

#-----------------------------
def translate_text(env):
#-----------------------------
  if not env["env_init"]:
    return

  result = ""
  env["env_tr_ok"]= False
  try:
#>search dictionary  
    dict_data= L0.get_all_text_from_file(env['dict_src'])
    regx= L0.compile_dict_translate_regx(env['tr_text'])
    result=  L0.get_all_matches(dict_data, regx)

    if len(result) == 0:
#>get pronunciation from url
      L0.console(">>Searching pronunciation...")
      url= L0.compose_url(env['url_pronc'], env['tr_text'])
      urls_regx=[]
      urls_regx.append((url, env['pattern_pronc_uk_phrasal']))
      urls_regx.append((url, env['pattern_pronc_us_phrasal']))
      urls_regx.append((url, env['pattern_pronc_uk_strong_word']))
      urls_regx.append((url, env['pattern_pronc_uk_word']))
      urls_regx.append((url, env['pattern_pronc_us_word']))
      urls_regx.append((url, env['pattern_pronc_generic']))
      urls_regx.append((url, env['pattern_pronc_generic2']))

      pronc_result= L0.get_first_html_body_from_url(urls_regx)
      pronc_result= L0.clean_pronc_result(pronc_result)

#>get translation from url
      L0.console(">>Searching translation...")
      regx= env['pattern_tr']
      urls_regx=[]
      #config main tr url
      url= L0.compose_url_for_tr(env['url_tr'], env['tr_text'])
      urls_regx.append((url, regx))

      #config  second tr url
      regx= env['pattern_tr2']
      url= L0.compose_url_for_tr(env['url_tr2'], env['tr_text'])
      urls_regx.append((url, regx))

      #config  second tr url
      regx= env['pattern_tr3']
      url= L0.compose_url_for_tr(env['url_tr3'], env['tr_text'])
      urls_regx.append((url, regx))


      tr_text= L0.get_first_html_body_from_url(urls_regx)
#<    
#>update dictionary
      L0.update_dictionary(env['tr_text'], tr_text, pronc_result, env['dict_src'])
#<
#>update reload from dictionary    
    dict_data= L0.get_all_text_from_file(env['dict_src'])
    regx= L0.compile_dict_translate_regx(env['tr_text'])
    result =L0.get_all_matches(dict_data, regx)
  except Exception as ex:
    L0.console(ex)

  env['result']= result
  env["env_tr_ok"]= True
#<

#-----------------------------
def show_translation(env):
#-----------------------------
  if not env["env_tr_ok"]:
    return

  if len(env["result"]) > 0:
    L0.console("Found!!")
    L0.console("------------------------------")
    L0.console("{}".format(env["result"][0]))
  else:
    L0.console("Text not found")

#-----------------------------
def show_foot_banner():
#-----------------------------
  L0.console("------------------------------")
#<<  

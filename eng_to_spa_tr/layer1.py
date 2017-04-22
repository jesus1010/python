import layer0 as L0
from jproperties import Properties

#>>LAYER 1------------------------------------------
def init_enviroment(env):
	L0.clear_screen()
	args= L0.get_cmd_arg()
	env['tr_text']= args.text_to_translate	
	env['result']= "***Text not found***"
	env['url_pronc']=""
	env['url_tr']=""	
	env['pattern_pronc']=""
	env['pattern_tr']=""	

	p = Properties()
	with open("config.properties", "rb") as f:
		p.load(f, "utf-8")		

	env['dict_src']=p['default_dict'][0]
	env['url_pronc']=p['url_pronc'][0]
	env['url_tr']=p['url_tr'][0]
	env['url_tr2']=p['url_tr2'][0]
	env['pattern_pronc']=p['pattern_pronc'][0]
	env['pattern_tr']=p['pattern_tr'][0]
	env['pattern_tr2']=p['pattern_tr2'][0]

def show_head_banner():
	print("------------------------------")
	print("TRANSLATIONS(EN->SPA):")
	print("------------------------------")
		
def translate_text(env):
	result = ""
	print "Searching..."
#>search dictionary	
	dict_data= L0.get_all_text_from_file(env['dict_src'])
	regx= L0.compile_dict_translate_regx(env['tr_text'])
	result=	L0.get_all_matches(dict_data, regx)
	if len(result) == 0:
#>get pronunciation from url
		url= L0.compose_url(env['url_pronc'], env['tr_text'])
		print "Pronunciation url:%s" % url
		regx= env['pattern_pronc']
		pronc_result= L0.get_text_from_url(url, regx)
#>get translation from url
		url= L0.compose_url(env['url_tr'], env['tr_text'])
		print "Translation url:%s" % url
		regx= env['pattern_tr']
		tr_text= L0.get_text_from_url(url, regx)
#>not found translation, try next url
		if len(tr_text) == 0:
			url= L0.compose_url(env['url_tr2'], env['tr_text'])
			print "Translation not found trying next url:%s" % url
			regx= env['pattern_tr2']
			tr_text= L0.get_text_from_url(url, regx)
#<		
#>update dictionary
		L0.update_dictionary(env['tr_text'], tr_text, pronc_result, env['dict_src'])
#<
#>update reload from dictionary		
		dict_data= L0.get_all_text_from_file(env['dict_src'])
		regx= L0.compile_dict_translate_regx(env['tr_text'])
		result =L0.get_all_matches(dict_data, regx)
	env['result']= result
#<

def show_translation(env):
	if len(env["result"]) > 0:
		print "Found!!"
		print("------------------------------")
		print("{}".format(env["result"][0]))	
	else:
		print "Text not found"	
def show_foot_banner():
	print("------------------------------")
#<<	



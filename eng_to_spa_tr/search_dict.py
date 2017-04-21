import layer1 as L1

def run():
	env={'dict_src':None, 'tr_text':None, 'result':None, 'url_pronc':None, 'url_tr':None}

	#>initialize eviroment
	L1.init_enviroment(env)
	#<
	#>show head banner
	L1.show_head_banner()
	#<
	#>translate text
	L1.translate_text(env)
	#<

	#>show translation text
	L1.show_translation(env)
	#<

	#>show foot banner
	L1.show_foot_banner()
	#<

#>>MAIN RUNTINE------------------------------------------
run()
#<<



import layer1 as L1

def run():
	enviroment={}

	#>initialize eviroment
	L1.init_enviroment(enviroment)
	#<
	#>show head banner
	L1.show_head_banner()
	#<
	#>translate text
	L1.translate_text(enviroment)
	#<

	#>show translation text
	L1.show_translation(enviroment)
	#<

	#>show foot banner
	L1.show_foot_banner()
	#<

#>>MAIN RUNTINE------------------------------------------
run()
#<<



def kill(pid:int):
	import os
	os.system("taskkill /pid "+str(pid))

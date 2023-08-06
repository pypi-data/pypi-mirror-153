from datetime import date
import calendar
from colorama import Fore,Style,Back, init

wh = Back.WHITE+Fore.BLACK
res = Fore.RESET+Back.RESET

init()

def cal(arg1 = 1,arg2 = 0):
	td = date.today()
	td = str(td)
	td = td.split('-')
	td = [int(i) for i in td]
	year = td [0]
	mon = td [1]
	day = td [2]
	calen = (calendar.month(year,mon, arg1, arg2))
	cale = calen [15:-1]
	ca = calen [0:15]
	for i in calen:
		if cale.find(str(day)) != -1:
			calen = cale.replace(str (day),wh + str(day)+res,1)
			print (ca+calen)
			break

import sys
import traceback
import os

def atoi(s):
	try:
		return int(s)
	except Exception as e:
		#print(e)
		return 0

def format_traceback():
	lines = []
	lines.extend(traceback.format_stack())
	lines.extend(traceback.format_tb(sys.exc_info()[2]))
	lines.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

	join_line = ["Traceback (most recent call last):\n"]
	for strg in lines:
		if not isinstance(strg, str):
			join_line.append(strg.decode("utf8"))
		else:
			join_line.append(strg)

	except_str = ''.join(join_line)

	# Removing the last \n
	except_str = except_str[:-1]
	return except_str

def gen_path(STOCK_CODE_PATH):
	if getattr(sys, 'frozen', False):
		pathname = STOCK_CODE_PATH
	else:
		pathname = os.path.join(os.path.dirname(os.path.dirname(__file__)), STOCK_CODE_PATH)
	return pathname

def format_datetime(datetime:str):
	length = len(str(datetime))
	if length == 17:
		return "%s-%s-%s %s:%s:%s.%s" % (
             datetime[:4], datetime[4:6], datetime[6:8], datetime[8:10], datetime[10:12], datetime[12:14], datetime[14:]
		)
	elif length == 9:
		return "%s:%s:%s.%s"% (datetime[0:2],datetime[2:4],datetime[4:6],datetime[6:])
	else:
		return
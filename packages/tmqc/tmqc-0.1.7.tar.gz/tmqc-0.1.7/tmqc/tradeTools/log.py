
"""
日志类
1、支持多进程/线程
2、支持日志按日期分割
3、支持日志打印时间前缀
"""

import io
import os
import sys
import time
import datetime
import platform
import colorama # http://pypi.python.org/pypi/colorama
import chardet
import threading
import queue
from . import func
from . import define
# colorama.init(wrap=False)
#from common import web

_log_mode = 'w'
_log_rotating = False
_log_time_prifix = False
_sys_log = None
# log_queue = queue.Queue()
if os.name == 'nt':
    import win32con, win32file, pywintypes # pip install pypiwin32
    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
    LOCK_SH = 0  # The default value
    LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
    __overlapped = pywintypes.OVERLAPPED()

    def lock(file, flags):
        hfile = win32file._get_osfhandle(file.fileno())
        win32file.LockFileEx(hfile, flags, 0, 0xffff0000, __overlapped)

    def unlock(file):
        hfile = win32file._get_osfhandle(file.fileno())
        win32file.UnlockFileEx(hfile, 0, 0xffff0000, __overlapped)

elif os.name == 'posix':
    import fcntl
    from fcntl import LOCK_EX
    def lock(file, flags):
        fcntl.flock(file.fileno(), flags)

    def unlock(file):
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)
else:
    raise RuntimeError("File Locker only support NT and Posix platforms!")

#class class_thread_print_log(threading.Thread):
#    def __init__(self, log_queue):
#        threading.Thread.__init__(self)
#        self.log_queue = log_queue

#    def run(self):
#        while True:
#            if not self.log_queue.empty():
#                file_name, content = self.log_queue.get()
#                _HandleLog(file_name, content)
#            #else:
#                self.log_queue.task_done()

def set_log_mode(mode:str):
    """设置日志的文件写模式，通常为w或者a"""
    global _log_mode
    _log_mode = mode

def set_log_rotating(value:bool):
    """设置日志是否分割，如果分割则日志名称加当前日期，否则不加"""
    global _log_rotating
    _log_rotating = value
    
def set_log_time_prifix(value:bool):
    """设置日志是否要时间前缀"""
    global _log_time_prifix
    _log_time_prifix = value

class class_log:
    enable = True
    clr_inited = False

    clr_blue =  colorama.Style.BRIGHT + colorama.Fore.BLUE
    clr_green =  colorama.Style.BRIGHT + colorama.Fore.GREEN
    clr_red =  colorama.Style.BRIGHT + colorama.Fore.RED
    clr_yellow =  colorama.Style.BRIGHT + colorama.Fore.YELLOW
    clr_mag = colorama.Style.BRIGHT + colorama.Fore.MAGENTA

    def __init__(self, path):
        self._file_path = path
        self._file = open(path,_log_mode)
        self._fil = sys.stdout
        if hasattr(self._fil, "isatty") and self._fil.isatty() and colorama:
            self._fil = colorama.AnsiToWin32(self._fil).stream

        # if not self.clr_inited :
        #     colorama.init(autoreset=True)

        self.isWindows = ('win32' == sys.platform)

    def __del__(self):
        # if self.clr_inited:
        #     colorama.deinit()
        self.close()

    def _write_file(self, c):
        while True:
            try: # 已经改为及时锁unblock模式，还需要进一步测试可靠性
                lock(self._file, LOCK_EX|LOCK_NB)
                break
            except pywintypes.error as e:
                time.sleep(0.01)
                continue
            except Exception as e:
                with open('log_error.txt', 'a') as f:
                    time_prefix = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f ")
                    f.write('%s %s,%s\n' % (time_prefix, e, c))
                break
        try:
            #stime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            c = '%s\n' % c
            # c = c.encode("gbk")
            self._file.write(c)
            self._file.flush()
        except:
            pass

        while True:
            try:
                unlock(self._file)
                return True
            except:
                time.sleep(0.01)
                continue

    def write_console(self, c):
        # if self.isWindows : c = c.encode('utf8', errors='ignore')
        # else : c = c.encode('utf8')
        # if not sys.stdout.encoding: c = c.encode('utf8')
        type = sys.getfilesystemencoding()
        # c = c.encode(type)

        # pycharm can do
        # sys.stdout.write(c)

        # console can do
        self._fil.write(c)



    def write(self, clr, datetime, c):
        self._write_file(datetime + c)

        if self.enable :
            c = self.clr_yellow + datetime + clr + c + colorama.Style.RESET_ALL + '\n'
            self.write_console(c)

    def write_trace(self, c):
        strg = func.format_traceback()
        if not strg:
            self.write(self.clr_red, 'trace lost.%s'%c)
            return

        self.write(self.clr_red, strg)
        self.write(self.clr_red, c)

    def close(self):
        self._file.close()


# 设置日志是否显示在控制台
_log_console_enable = {}
def SetConsoleEnable(file_name, enable):
    _log_console_enable[file_name] = enable

_log_files = {}
def close_all():
    global _log_files
    for k,v in list(_log_files.items()):
        v.close()
    _log_files = {}
    
    global _sys_log
    if _sys_log:
        _sys_log = None

def WriteLog(file_name, content):
    _HandleLog(file_name, content)
    #log_queue.put((file_name, content))

def WriteData(file_name, content):
    """纯数据类型，不需要时间前缀"""
    _HandleLog(file_name, content, prefix=False)

# 写日志，如果没有日志对象则创建
def _HandleLog(file_name, content, prefix=True):
    global _log_files
    global _log_time_prifix
    global _log_rotating

    if file_name in define.g_log_switch and not define.g_log_switch[file_name]:
        return

    if not isinstance(content, str) and not isinstance(content, str):
        content = content.__str__()

    # 创建log目录
    base_path = os.getcwd()
    base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    root = os.path.join(base_path, "log")
    
    if _log_rotating:
        root = os.path.join(root, datetime.datetime.now().strftime("%Y-%m"))
        date = datetime.datetime.now().strftime("%m-%d")
        path = "%s/%s %s.log" % (root, file_name, date)
    else:
        path = "%s/%s.log" % (root, file_name)

    if not os.path.exists(root): os.makedirs(root)
    if path not in _log_files: _log_files[path] = class_log(path)

    if not isinstance(content, str):
        if chardet.detect(content)["encoding"] == "utf-8":
            content = content.decode("utf-8")
        elif chardet.detect(content)["encoding"] == "GB2312":
            content = content.decode("GB2312")

    try :
        if class_log.enable:
            _log_files[path].write_console("%s: " % file_name)

        time_prefix = ""
        if _log_time_prifix and prefix:
            time_prefix = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f\t")
        _log_files[path].write(class_log.clr_green, time_prefix, content)
    except Exception as e:
        print(e)

##########################################################################################
# 系统日志

def _Get_sys_log():
    global _sys_log
    if not _sys_log: _sys_log = class_log("log/sys.log")
    return _sys_log

def WriteError(strg):
    try :
        time_prefix = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f ")
        _Get_sys_log().write(class_log.clr_mag, time_prefix, strg)
    except Exception as e:
        print(e)

def WriteWarning(strg):
    try :
        _Get_sys_log().write(class_log.clr_mag, strg)
    except : pass

def WriteExcept(strg):
    try :
        _Get_sys_log().write_trace(strg)

    except Exception as e:
        print(e)
    # raise exception.
    # don't put it into try block
    sys.exit()

def WriteBlock(strg):
    _Get_sys_log().write(class_log.clr_blue, '======= %s ========'%strg)

def WriteEntry(strg):
    _Get_sys_log().write(class_log.clr_green, '▶ %s'%strg)

def WriteDetail(strg):
    _Get_sys_log().write(class_log.clr_yellow, ' - %s'%strg)

def WriteRaw(strg):
    if not _Get_sys_log().enable:return
    sys.stdout.write(strg)

def Disable(yes = True):
    _Get_sys_log().enable = not yes

# -*- coding: utf-8 -*-
import os,types,sys,time,stat
import shutil as sh

"""
    函数：try_copytree(src,dst)
    功能：递归拷贝文件夹到另一个文件夹下，如果存在相同的文件夹/文件，则全部覆盖!本函数修改自
    shutil.copytree 原始函数因为不能拷贝已经存在的目录因此不适用本系统
    如果源地址是文件，则目标地址也必须是文件
    如果源地址是目录，则目标地址也必须是目录
    其中的路径格式必须使用 unix 风格路径，已 ‘/’ 分割
"""
def try_copytree(src, dst):
    if os.path.isfile(src):
        dstSeg   = os.path.split(dst)
        dstPath  = ''.join(dstSeg[:-1])
        fileName = dstSeg[-1:]
        if not os.path.exists(dstPath):
            os.makedirs(dstPath)
        sh.copy2(src, dst)
    elif os.path.exists(src):
        names = os.listdir(src)
        if not os.path.isdir(dst):
            os.makedirs(dst)
        for name in names:
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            if os.path.isdir(srcname):
                try_copytree(srcname, dstname)
            else:
                sh.copy2(srcname, dstname)
# 
def cj_copytree(src, dst):
    #print '原文拷贝 '+src+' '+dst
    try_copytree(src,dst)

# 
def try_rename(src, dst):
    try:
        head, tail = os.path.split(dst)
        if head and tail and not os.path.exists(head):
            os.makedirs(head)
        os.rename(src, dst)
        #print '直接重命名 '+src+' '+dst
    except OSError:
        cj_copytree(src,dst)
        
"""
    函数：print_s()
    功能：格式化 PY 的 结构，成一个标准字符串
    参数：obj    -> 一个正规的 Py 结构（字典，列表，元组）
         level  -> 层级缩近的初始值 默认为 0
         s      -> 当前已经序列化完毕的字符串 默认为 空字串
"""
def print_s(obj,level,s):
    dot_tag   = ','         #   定义元素分割符
    ret_tag   = '\n'        #   定义换行符
    quo_tag   = '\''        #   定义字符串引用符号
    cut_tag   = ':'         #   定义键值分割符
    u_s_tuple = ('(',')')   #   定义元组起始结束符
    u_s_list  = ('[',']')   #   定义列表起始结束符
    u_s_dict  = ('{','}')   #   定义字典起始结束符
    fan_all   = u_s_tuple[1]+u_s_list[1]+u_s_dict[1]
    space = ''
    for i in range(0,level):
        space += '  '
    level += 1
    tp = type(obj)
    o_len = len(obj)-1
    if tp == list or tp == set:
        for k in range(len(obj)):
            tp2 = type(obj[k])
            if tp2 == list:
                s.append(ret_tag+space+u_s_list[0])
                s  = [print_s(obj[k],level,s)]
                if s[len(s)-1][-1:] in fan_all:
                    s.append(ret_tag+space)
                s.append(u_s_list[1])
            elif tp2 == set:
                s.append(ret_tag+space+u_s_tuple[0])
                s  = [print_s(obj[k],level,s)]
                if s[len(s)-1][-1:] in fan_all:
                    s.append(ret_tag+space)
                s.append(u_s_tuple[1])
            elif tp2 == dict:
                s.append(u_s_dict[0])
                s  = [print_s(obj[k],level,s)+ret_tag+space+u_s_dict[1]]
            elif tp2 == str:
                s.append(quo_tag+str(obj[k])+quo_tag)
            else:
                s.append(str(obj[k]))
            if k < o_len:
                s.append(dot_tag)
    elif tp == dict:
        ii = 0
        for key in obj:
            tp2 = type(obj[key])
            if type(key) == str:
                keys = quo_tag+key+quo_tag
            else:
                keys = str(key)
            if tp2 == list:
                s.append(ret_tag+space+keys+cut_tag+u_s_list[0])
                s  = [print_s(obj[key],level,s)]
                if s[len(s)-1][-1:] in fan_all:
                    s.append(ret_tag+space)
                s.append(u_s_list[1])
            elif tp2 == set:
                s.append(ret_tag+space+keys+cut_tag+u_s_tuple[0])
                s  = [print_s(obj[key],level,s)]
                if s[len(s)-1][-1:] in fan_all:
                    s.append(ret_tag+space)
                s.append(u_s_tuple[1])
            elif tp2 == dict:
                s.append(ret_tag+space+keys+cut_tag+u_s_dict[0])
                s  = [print_s(obj[key],level,s)+ret_tag+space+u_s_dict[1]]
            elif tp2 == str:
                s.append(ret_tag+space+keys+cut_tag+quo_tag+str(obj[key])+quo_tag)
            else:
                s.append(ret_tag+space+keys+cut_tag+str(obj[key]))
            if ii < o_len:
                s.append(dot_tag)
            ii += 1
    elif tp == str:
        s.append(space+quo_tag+obj+quo_tag)
    else:
        s.append(space+str(obj))
    return ''.join(s)

"""
    格式化输出PYTHON 的结构对象，可以处理字典，列表，元组等类型是仿照PHP 的 print_r 所写的
    ：）
"""
def print_r(obj):
    if type(obj) == dict:
        print('{'+print_s(obj,1,[])+'\n}')
    elif type(obj) == list:
        print('['+print_s(obj,1,[])+']')
    elif type(obj) == set:
        print('('+print_s(obj,1,[])+')')
    else:
        print(str(obj))

class Log:
    """
        日志记录类： Log
        功能： 向指定文件写入 LOG 记录用来用来记载程序执行流程的细节是否顺利
        自动分组，自定义缓存大小，自定义是否输出
    """
    ch_num = 100        #   定时清理缓存
    change = 5000       #   定义文件分组大小
    def __init__(self,f):
        self.f = f      #   记录 LOG 所使用的文件名
        dirs,files = os.path.split(f)
        if dirs and not os.path.isdir(dirs):
            os.makedirs(dirs)
        open(self.f,'w').close()
        self.n = 0      #   记录 LOG 的次数
        self.g = 1      #   记录当前分组次数
        self.c = []     #   记录 LOG 使用的缓存
        self.l = len(f) #   取得当前初始文件名长度
        self.p_map = {
            'yes':self._p,
            'no' :self._f
        }
    def write(self,log,if_print='yes'):
        logt = '\n'+(str(time.localtime()).replace(',','-',2).replace(',',' ',1).replace(',',':',2)[1:-12])+'\n\t'+log
        self.p_map[if_print](log)
        self.c.append(logt)
        self.n += 1
        if self.n % self.ch_num == 0:
            self._r()
    def finish(self):
        self._r()
    def _r(self):
        if self.n / self.change > self.g:
            self.f = self.f[:self.l]+'.'+str(self.n/self.change)+'.txt'
            self.g +=1
        fp = open(self.f,'a+')
        fp.write(''.join(self.c))
        fp.close()
        self.c = []
    def _f(self,log=''):
        pass
    def _p(self,log=''):
        print(log)
        
"""
    函数： error_break(msg)
    功能： 退出程序的执行并在屏幕打印用户字串
"""
def error_break(msg=''):
    l = Log('./error.txt')
    l.write(msg)
    l.finish()    
    anykey = raw_input('按任意键停止程序运行！:')
    sys.exit(0)
#   向后查找一个有效字符
def glt(fs,i):
    i -= 1
    r = fs[i]
    while i>=0 and (r == "\r" or r == "\n" or r == "\t" or r == ' '):
        i -= 1
        r = fs[i]
    return r
#   向前查找一个有效字符    
def gft(fs,i,l):
    i += 1
    r = fs[i]
    while i<l and (r == "\r" or r == "\n" or r == "\t" or r == ' '):
        i += 1
        r = fs[i]
    return r
#   查看当前所在字符是否没有被转义
def fa(ser,fr,ft):
    if ser[fr] != ft:
        return False
    r  = 0
    fr-= 1
    if fr<=0:
        return True
    while ser[fr] == '\\':
        if fr<=0:
            return True
        r += 1
        fr-= 1
    if r%2 == 0:
        return True
    else:
        return False
#   获取一个文件的扩展名
def get_en(file_name):
    fn = file_name.rfind('.')
    if fn >= -1:
        return file_name[fn:]
    else:
        return ''
# End of ms_inc.py

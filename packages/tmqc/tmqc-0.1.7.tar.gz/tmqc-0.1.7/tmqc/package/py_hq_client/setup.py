'''
    编译前要进入环境 python3.6
    F:/ProgramFiles/Anaconda3/Scripts/activate
    conda activate F:\ProgramFiles\Anaconda3

    进入目录
    cd cy/py_hq_client

    使用命令 来编译扩展
    python setup.py build_ext --inplace
    
    Cython 语法复杂
    导出定义等相关资料可参见如下网页

    https://cython.readthedocs.io/en/latest/src/userguide/language_basics.html
    https://cython.readthedocs.io/en/latest/src/userguide/extension_types.html
    https://cython.readthedocs.io/en/latest/src/userguide/wrapping_CPlusPlus.html
    https://python3-cookbook.readthedocs.io/zh_CN/latest/c15/p10_wrap_existing_c_code_with_cython.html
    https://www.jianshu.com/p/4a08fe5225a5
    
    C/C++函数定义时 注意不能使用 python 关键字 
    https://www.w3school.com.cn/python/python_ref_keywords.asp
    
    
'''
import glob
import os

from inc.walk_in_file import *
from inc.ms_inc import *

from distutils.core import setup
from distutils.extension import Extension

from Cython.Distutils import build_ext

ext_modules = [
    Extension(
        'py_hq_client',
        ['_hq_client.pyx'],
        include_dirs = ['./lib',],
        libraries=['hq_client'],
        library_dirs=['./lib',],
        runtime_library_dirs=[],
        language="c++",
        # extra_compile_args=['/MD']
    )
]

setup(
    name='py_hq_client',
    version='0.0.1',
    description='python interface of hq_client',
    author='cjxx',
    license='GPL',
    # packages=['py_hq_client'],
    ext_modules = ext_modules,
    cmdclass={'build_ext':build_ext}
)

# 删除cpp
DeleteFile('_hq_client.cpp')
DeleteFile('cfg_hq_client.ini')
DeleteFile('hq_client.dll')

# 拷贝新dll 和配置文件
CopyFileToDst('./lib/cfg_hq_client.ini', './')
CopyFileToDst('./lib/hq_client.dll', './')

# 改名dll
DeleteFile('py_hq_client.pyd')
try_rename('py_hq_client.cp36-win_amd64.pyd', 'py_hq_client.pyd')
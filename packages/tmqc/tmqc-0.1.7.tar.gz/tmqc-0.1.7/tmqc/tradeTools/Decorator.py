# -*- coding: utf-8 -*-
# @Time    : 2018/8/10 14:01
# @Author  : hc
# @Site    : 
# @File    : Decorator.py
# @Software: PyCharm
from functools import wraps
import os
import pandas as pd

def singleton(cls, *args, **kwargs):
    instance = {}  # 创建字典来保存实例

    def get_instance(*args, **kwargs):
        if cls not in instance:  # 若实例不存在则新建
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return get_instance

# 装饰器，优先加载静态文件
# todo:注意字段的dtype
# def loadData(*dargs, **dkargs):
def loadData(*dargs, **dkargs):
    def outer(func,*args, **kwargs):
        def inner(*args, **kwargs):
            nodeFileName = func.__name__[3:] # 构造文件夹名称
            excelName = f"{nodeFileName}"
            isRealTime = kwargs['isRealTime'] if "isRealTime" in kwargs else False
            excelNames = []
            for k,v in kwargs.items(): # 参数的键值对作为补充文件名
                if k == "isRealTime" or k=="df":
                    continue
                excelNames.append(k)
            excelNames.sort()
            for k in excelNames:
                excelName += f"_{k}[{str(kwargs[k])}]"
            co_filename = os.path.normcase(func.__code__.co_filename)
            # 定位到工作空间目录 workspace
            _paths = co_filename.split("\\")[0:2]

            _paths.append("data")

            if "path" in dkargs and dkargs["path"] == "data":
                # 装饰器传参 path：设置为"data".则读取data路径。用于可复用的数据
                dataPath =""
            else:
                # 获取函数代码所在的文件名称。用于构造读取静态文件的路径
                # 取函数代码所在文件名中 _ 分割的第二个关键字
                dataPath = co_filename.split("\\")[-1].split(".")[0].split("_")[0:1]
                dataPath = "_".join(dataPath)
                _paths.append(dataPath)
            _paths.append(nodeFileName)
            _paths.append(excelName+".xlsx")
            fileName = os.sep.join(_paths)  #
            path = os.path.dirname(fileName)
            if not os.path.exists(path):os.makedirs(path)
            if not os.path.exists(fileName) or isRealTime:
                print(func.__name__ + f"\033[32m开始生成数据[{fileName}]\033[0m")
                df =  func(fileName = fileName,*args,**kwargs )
                df.to_excel(fileName, sheet_name="数据源")
                return df
            print(func.__name__ + f"读取数据[{fileName}]")
            df = pd.read_excel(fileName, sheet_name="数据源", index_col=0,engine="openpyxl")
            # df = pd.read_excel(fileName, sheet_name="数据源", index_col=0,)
            return df
        return inner
    return outer
# -*- coding: utf-8 -*-
import os
import os.path
import shutil
import struct

# 遍历路径
def WalkInDir(nowDir, func):
    i = 0
    for parent,dirnames,filenames in os.walk(nowDir):
        for _dirname in dirnames:
            pass
        for filename in filenames:
            i += 1
            fullFileName = os.path.join(parent, filename)
            func(i, parent, filename, fullFileName)

# 遍历路径包含文件夹,负数为文件夹,正数为文件
def WalkInDirIncludeAll(nowDir, func):
    i = 0
    j = 0
    if os.path.exists(nowDir):
        # 当前路径也算
        j -= 1
        func(j, '', nowDir, nowDir)

    for parent,dirnames,filenames in os.walk(nowDir):
        for dirname in dirnames:
            j -= 1
            fullFileName = os.path.join(parent, dirname)
            func(j, parent, dirname, fullFileName)
        for filename in filenames:
            i += 1
            fullFileName = os.path.join(parent, filename)
            func(i, parent, filename, fullFileName)

# 获取路径下所有文件名 - 不包括路径
def GetDirFiles(dir):
    names = []
    for parent,dirnames,filenames in os.walk(dir):
        for filename in filenames:
            names.append(filename)
    return names

# 判断文件是否存在
def IsHaveFile(fileWithPath):
    return os.path.isfile(fileWithPath)

# 获取文件大小
def GetFileSize(fileWithPath):
    return os.path.getsize(fileWithPath)

# 判断路径是否存在
def IsHaveDir(path):
    return os.path.exists(path)

# 创建路径
def MakeDirs(path):
    if not IsHaveDir(path):
        os.makedirs(path)

# 删除指定路径下面的所有文件和目录
def DeleteAllFilesAndDirs(path):
    if IsHaveDir(path):
        shutil.rmtree(path)

# 删除指定的文件
def DeleteFile(fileWithPath):
    if IsHaveFile(fileWithPath):
        os.remove(fileWithPath)
        
# 拷贝文件到另一个目录下
def CopyFileToDst(fileSrc, dirDst):
    if not IsHaveFile(fileSrc):
        print('[error] copy file['+str(fileSrc)+'] not exist')
        return False
    MakeDirs(dirDst)
    fileName= os.path.split(fileSrc)[1]
    fileDst = os.path.join(dirDst, fileName)
    fr = open(fileSrc, 'rb')
    frInfo = fr.read()
    fw = open(fileDst, 'wb')
    fw.write(frInfo)
    fw.close()
    fr.close()
    return True

# 获取文件内容
def ReadFileData(filePath):
    if not IsHaveFile(filePath):
        print('[错误] 无法读取文件内容 [' + filePath + ']')
        return False
    f = open(filePath, 'rb')
    readInfo = f.read()
    f.close()
    return readInfo

# 获取文件字符内容
def ReadFileStr(filePath):
    if not IsHaveFile(filePath):
        print('[错误] 无法读取文件内容 [' + filePath + ']')
        return False
    f = open(filePath, 'r')
    readInfo = f.read()
    f.close()
    return readInfo

#
def ReadFileDataLines(filePath):
    if not IsHaveFile(filePath):
        print('[err] not found file [' + filePath + ']')
        return []
    try:
        f = open(filePath, 'rb')
        lines = f.readlines()
        f.close()
    except OSError:
        # 读取错误
        return []

    return lines

# 获取文件字符行内容
def ReadFileStrLines(filePath, encoding='utf-8'):
    if not IsHaveFile(filePath):
        print('[err] not found file [' + filePath + ']')
        return []
    try:
        f = open(filePath, 'r', encoding=encoding)
        lines = f.readlines()
        f.close()
    except UnicodeDecodeError:
        # 二进制文件
        return []
    except OSError:
        # 读取错误
        return []

    return lines

#! 注意: 并未检查路径是否存在
def WriteFileInfo(filePath, fileInfo):
    #! 并未检查路径是否存在
    f = open(filePath, 'wb')
    f.write(fileInfo)
    f.close()
    
#! 注意: 并未检查路径是否存在
def WriteFileStrInfo(filePath, fileInfo):
    #! 并未检查路径是否存在
    f = open(filePath, 'w')
    f.write(fileInfo)
    f.close()

#! 注意: 并未检查路径是否存在
def WriteFileLinesInfo(filePath, lines):
    #! 并未检查路径是否存在
    f = open(filePath, 'w')
    for line in lines:
        f.write(line)
        if line[-1] != '\n':
            f.write('\n')
    f.close()        

# 读取二进制整数(网络字节序)
def ReadInt(binData):
    result = struct.unpack('!i', binData)
    print(str(result))
    return result[0]

# 生成二进制整数(网络字节序)
def MakeInt(iVal):
    return struct.pack('!i', iVal)

# 生成二进制浮点数(网络字节序)
def MakeFloatNet(r):
    return struct.pack('!f', r)

# 生成二进制浮点数(本地字节序)
def MakeFloatLocal(r):
    return struct.pack('=f', r)

# 获取文件扩展名
def GetFileExtname(fileName):
    extName = os.path.splitext(fileName)[-1]
    return extName
    

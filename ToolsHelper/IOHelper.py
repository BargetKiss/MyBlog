#coding=utf-8
import hashlib
import os,sys

# 使用Python进行文件Hash计算有两点必须要注意：

# 1、文件打开方式一定要是二进制方式，既打开文件时使用b模式，否则Hash计算是基于文本的那将得到错误的文件Hash(网上看到有人说遇到Python的Hash计算错误在大多是由于这个原因造成的)。

# 2、对于MD5如果需要16位(bytes)的值那么调用对象的digest()而hexdigest(）默认是32位(bytes)，同理Sha1的digest()和hexdigest()分别产生20位(bytes)和40位(bytes)的hash值


#获取文件hash
def GetFileSha1(filepath):
    with open(filepath,'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        print(hash)
        return hash
 
 #获取文件MD5
def GetFileMD5(filepath):
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        print(hash)
        return hash
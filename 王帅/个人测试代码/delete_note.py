# -*- coding: GBK -*-
#py文件去注释

import re
import os
import configparser

Python='CleanNote'
SrcPath='E:\python\py_pick\\result'
DescPath='E:\python\py_pick\\result'

def ReadIni(path,section,option):#文件路径，章节，关键词
  #读取ini
  cf=configparser.ConfigParser()
  cf.read(path)
  value=cf.get(section,option)#如果用getint()则直接读取该数据类型为整数
  return value

def IsPassLine(strLine):
  #是否是可以忽略的行
  #可忽略行的正则表达式列表
  RegularExpressions=["""/'.*#.*/'""","""/".*#.*/""",
            """/'/'/'.*#.*/'/'/'""","""/"/"/".*#.*/"/"/"""]
  for One in RegularExpressions:
    zz=re.compile(One)
    if re.search(zz,strLine)==None:
      continue
    else:
      return True#有匹配 则忽略
    return False

def ReadFile(FileName):
  #读取并处理文件
  fobj=open(FileName,'r',encoding='utf-8')
  AllLines=fobj.readlines()
  fobj.close()
  NewStr=''
  LogStr='/n%20s/n'%(FileName.split('//')[-1])#输出的日志
  nline=0
  for eachline in AllLines:
    index=eachline.find('#')#获取带注释句‘#'的位置索引
    if index==-1 or nline<3 or IsPassLine(eachline):
      if eachline.strip()!='':#排除纯空的行
        NewStr=NewStr+eachline
    else:
      if index!=0:
        #NewStr=NewStr+eachline[:index]+'/n'#截取后面的注释部分
        NewStr = NewStr + eachline[:index]  # 截取后面的注释部分
        LogStr+="ChangeLine: %s/t%s"%(nline,eachline[index:])
    nline+=1
  return NewStr,LogStr

def MakeCleanFile(SrcPath,DescPath,FileList):
  fLog=open(DescPath+'//'+'CleanNoteLog.txt','w',encoding='utf-8')
  for File in FileList:
    curStr,LogStr=ReadFile(SrcPath+'//'+File)
    fNew=open(DescPath+'//without_note_'+File,'w',encoding='utf-8')
    fNew.write(curStr)
    fNew.close()
    fLog.write(LogStr)
  fLog.close()

def Main():
  #可以采用这种方式，暂时不用
  #从ini获取源文件夹及目标文件夹路径
  '''
  IniPath = 'CleanNote.ini'
  SrcPath=ReadIni(IniPath,'CleanNote','SrcPath')#源文件夹
  DescPath=ReadIni(IniPath,'CleanNote','DescPath')#目的文件夹
  '''

  #如果目的文件夹不存在，创建之
  if not os.path.exists(DescPath):
    os.makedirs(DescPath)
  FileList=[]
  for files in os.walk(SrcPath):
    for FileName in files[2]:
      if FileName.split('.')[-1]=='py':
        FileList.append(FileName)
  print(FileList)
  MakeCleanFile(SrcPath,DescPath,FileList)
if __name__=='__main__':
  Main()
  print('>>>End<<<')
  os.system('pause')


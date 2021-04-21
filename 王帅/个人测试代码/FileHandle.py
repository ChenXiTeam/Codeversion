import os

class FileHandle:
    #获取文件内容
    def get_content(self,path):
        f = open(path,"r", encoding='utf-8')   #设置文件对象
        content = f.read()     #将txt文件的所有内容读入到字符串str中
        f.close()   #将文件关闭
        return content
	#获取文件内容
    def get_text(self):
        file_path=os.path.dirname(__file__)                                 #当前文件所在目录
        txt_path=file_path+r'\test'                                      #txt目录
        rootdir=os.path.join(txt_path)                                      #目标目录内容
        local_text={}
        # 读txt 文件
        for (dirpath,dirnames,filenames) in os.walk(rootdir):
            for filename in filenames:
                if os.path.splitext(filename)[1]=='.txt':
                    flag_file_path=dirpath+'\\'+filename                    #文件路径
                    flag_file_content=self.get_content(flag_file_path) #读文件路径
                    if flag_file_content!='':
                        local_text[filename.replace('.txt', '')]=flag_file_content  #键值对内容
        return local_text
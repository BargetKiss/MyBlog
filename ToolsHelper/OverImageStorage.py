#coding=utf8
from django.core.files.storage import FileSystemStorage

class ImageStorage(FileSystemStorage):
    from django.conf import settings
    
    def __doc__(self):
        return  u'重写图片处理程序'
   
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        #初始化
        super(ImageStorage, self).__init__(location, base_url)

    #重写 _save方法        
    def _save(self, name, content): 
   
        #print(content._get_size()) #获取图片大小
        #print(content.__hash__()) #文件的Hash
        import os, time, random
        from django.conf import settings
        #文件扩展名
        ext = os.path.splitext(name)[1]
        #文件目录
        d = os.path.dirname(name)#settings.BASE_DIR+settings.MEDIA_ROOT +

        #定义文件名，年月日时分秒随机数
        #fn = time.strftime('%Y%m%d%H%M%S')
        #fn = fn + '%d' % random.randint(0,1000)
        fn = content.__hash__()
        #重写合成文件名
        name = os.path.join(d, str(fn) + ext) 
        if os.path.exists(name): #如果文件已存在，则删除，防止数据冗余
            os.remove(name)


        #调用父类方法
        return super(ImageStorage, self)._save(name, content)
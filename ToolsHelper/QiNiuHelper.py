#coding=utf-8
##########七牛云帮助类#############
import os
import qiniu
import logging
import json
import datetime,time
from django.conf import settings

logger = logging.getLogger(__name__)

#保存文件到七牛云,两个参数分别表示文件路径、是否上传完毕后删除本地文件
def SaveFileToQiNiu(local_file='',AutoDelFile=False):
    '''保存文件到七牛云'''
    if str(local_file) == '' or local_file is None:
        return (0,'file is None')
    
    if not os.path.exists(local_file):
        return(0,'file is not exists')
    
    if settings.QINIU_ACCESS_KEY == '' or settings.QINIU_ACCESS_KEY is None:
        return (0,'QINIU_ACCESS_KEY is None')
    
    if settings.QINIU_SECRET_KEY =='' or settings.QINIU_SECRET_KEY is None:
        return (0,'QINIU_SECRET_KEY is None')
    
    if settings.QINIU_BUCKET_NAME =='' or settings.QINIU_BUCKET_NAME is None:
        return (0,'QINIU_BUCKET_NAME is None')
    
    if settings.QINIU_BUCKET_DOMAIN =='' or settings.QINIU_BUCKET_DOMAIN is None:
        return (0,'QINIU_BUCKET_DOMAIN is None')
    
    no_ext_name,ext = os.path.splitext(local_file)
    ext = ext[1:]
    try:
        q = qiniu.Auth(settings.QINIU_ACCESS_KEY,settings.QINIU_SECRET_KEY)
        
        key = os.path.basename(local_file)
        from FileMime import GetFileMime
        mime_type = GetFileMime(ext) #'text/plain'
        params = {'x:a':'a'}
        print(mime_type)
        token = q.upload_token(settings.QINIU_BUCKET_NAME, key)
        
        ret, info = qiniu.put_file(token, key, local_file, mime_type = mime_type, check_crc=True)
        
        if ret['key'] != key or ret['hash'] != qiniu.etag(local_file):
            logger.error(u'文件保存七牛云错误，本地文件：%s' % local_file)
            
        if AutoDelFile:
            os.remove(local_file)
            
        qn_file_path = settings.QINIU_BUCKET_DOMAIN + '/' + key + '?v'+ time.strftime('%Y%m%d%H%M%S')
        #logger.info(qn_file_path)
        return (1,qn_file_path)
        
    except Exception as e:
        #logger.error(u'上传错误')
        return (0,'upload is error')
        
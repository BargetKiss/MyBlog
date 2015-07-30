#coding=utf-8

#传入拓展名，得到文件的MIME类型，拓展名不包含“.”，返回值为string
def GetFileMime(ext=''):
    mime_type = ''
    
    ext = ext.lower()
    
    if ext == 'xls' or ext == 'xla':
        mime_type = 'application/msexcel'
    elif ext == 'hlp' or ext == 'chm':
        mime_type = 'application/mshelp'
    elif ext == 'ppt' or ext =='ppz' or ext == 'pps' or ext =='pot':
        mime_type = 'application/mspowerpoint'
    elif ext == 'doc' or ext == 'dot':
        mime_type = 'application/msword'
    elif ext =='exe' or ext =='rar':
        mime_type = 'application/octet-stream'
    elif ext =='pdf':
        mime_type = 'application/pdf'
    elif ext == 'ai' or ext == 'eps' or ext == 'ps':
        mime_type = 'application/postscript'
    elif ext == 'rtf':
        mime_type ='application/rtf'
    elif ext == 'js':
        mime_type ='application/x-javascript'
    elif ext == 'swf' or ext == 'cab':
        mime_type ='application/x-shockwave-flash'
    elif ext == 'zip':
        mime_type ='application/zip'
    elif ext == 'mp3' or ext == 'mp2':
        mime_type ='audio/mpeg'
    elif ext == 'mid' or ext == 'midi':
        mime_type ='audio/x-midi'
    elif ext == 'gif':
        mime_type ='image/gif'
    elif ext == 'jpeg' or ext =='jpg' or ext =='jpe':
        mime_type ='image/jpeg'
    elif ext == 'txt':
        mime_type ='text/plain'
    
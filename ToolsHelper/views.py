#coding=utf-8
import json, os, datetime, time, string
from django.conf import settings
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import requests
import uuid


# Create your views here.

#处理富文本编辑器上传
@csrf_exempt
def upload_textarea(request,spath):
    ext_allowed = ['gif', 'jpg', 'jpeg', 'png','bmp']
    max_size = 2621440
    today = datetime.datetime.today()
    #save_dir = 'image/%d/%d/%d/' % (today.year, today.month, today.day)
    spath = spath+'/'
    save_path = os.path.join(settings.MEDIA_ROOT, spath)
    save_url = os.path.join(settings.MEDIA_URL, spath)
    #print save_dir, save_path, save_url
    
    if request.method == 'POST':
        file = request.FILES['imgFile']

        if not file.name:
            return HttpResponse(json.dumps(
                { 'error': 1, 'message': u'请选择要上传的文件' }
            ))

        ext = file.name.split('.').pop()
        if ext not in ext_allowed:
            return HttpResponse(json.dumps(
                { 'error': 1, 'message': u'请上传后缀为%s的文件' %  ext_allowed}
            ))

        if file.size > max_size:
            return HttpResponse(json.dumps(
                { 'error': 1, 'message': u'上传的文件大小不能超过2.5MB'}
            ))

        if not os.path.isdir(save_path):
            os.makedirs(save_path)
        
        file_name_no_ext = str(uuid.uuid1())
        #new_file = '%s.%s' % (int(time.time()), ext)
        new_file = '%s.%s' % (file_name_no_ext, ext)

        destination = open(save_path+new_file, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        
        import IOHelper
        file_md5 = IOHelper.GetFileMD5(save_path+new_file)
        edit_new_file = '%s.%s' % (file_md5, ext)
        if os.path.exists(save_path+edit_new_file): #如果该文件的MD5已存在，则删除
            os.remove(save_path+new_file)
        else: #否则改名
            os.rename(save_path+new_file, save_path+edit_new_file)
               
        if settings.FILE_SAVE_DISK_TYPE == 1: #保存到七牛云
            from QiNiuHelper import  SaveFileToQiNiu
            status,qiniu_text = SaveFileToQiNiu(settings.BASE_DIR + save_url+edit_new_file,True)
            if status == 0:
                return HttpResponse(json.dumps(
                    { 'error': 0, 'message':qiniu_text }
                ))
            else:
                return HttpResponse(json.dumps(
                    { 'error': 0, 'url': 'http://'+qiniu_text}
                ))
        else:
            return HttpResponse(json.dumps(
                    { 'error': 0, 'url': '/'+save_url+edit_new_file}
            ))
        
        
        # TODO we should show the uploaded file and the manager url   save_url+new_file
        #return  HttpResponse("Upload Succsefull to URL:%s" % (save_url+new_file)  )
        #return HttpResponse(json.dumps(
        #    {'error':0,'message':save_url+new_file}
        #))
    else:
        raise Http404
        # return HttpResponse('hello')
        
#服务器文件浏览  ################有问题，暂不用###################
def view_textarea(request):
    root_url = settings.MEDIA_URL+ 'upload/'
    root_path = os.path.join(settings.MEDIA_ROOT, 'upload') + '/'

    file_types = ["gif", "jpg", "jpeg", "png", "bmp"]
    dir_types = ["image", "flash", "media", "file"]
    
    # get current root dir with GET['dir']
    dir_name = request.GET.get('dir')
    if dir_name:
        root_path += dir_name + '/'
        root_url  += dir_name + '/'
        if not os.path.exists(root_path):
            os.makedirs(root_path)

    # set value of cur_path, cur_dir ... with GET['path']
    path = request.GET.get('path', "")
    current_path = root_path + path
    current_url = root_url + path
    current_dir_path = path

    # XXX We should get the parent path, 
    # but the regxp seems WRONG!
    moveup_dir_path = re.search(r'(.*?)[^\/]+\/',
            current_dir_path).groups(1) if path != "" else ""

    
    order = string.lower(request.GET.get("order", "name"))
    
    if '..' in current_path:
        raise Http404("Access is not allowed.")

    if re.search(r'(\/$)', current_path).group(0) != '/':  
        raise Http404("Parameter is not valid.")

    if not os.path.isdir(current_path):
        raise Http404("Directory does not exist.")
    
    file_list = []

    if os.listdir(current_path):
        for file_name in os.listdir(current_path):
            dicts = {}

            file_path = current_path + file_name

            if os.path.isdir(file_path):  
                dicts["is_dir"] = True  
                dicts["has_file"] = len(os.listdir(file_path)) > 0  
                dicts["filesize"] = 0  
                dicts["is_photo"] = False  
                dicts["filetype"] = ""  
            else:  
                dicts["is_dir"] = False  
                dicts["has_file"] = False  
                dicts["filesize"] = os.path.getsize(file_path)  

                extensions = string.split(file_name, ".")  
                length = len(extensions) - 1  
                if string.lower(extensions[length]) in file_types:  
                    dicts["is_photo"] = True  
                else:  
                    dicts["is_photo"] = False  
                dicts["filetype"] = string.lower(extensions[length])  
            dicts["filename"] = file_name  
            dicts["datetime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
            file_list.append(dicts)  

        results = {}  
        results["moveup_dir_path"] = moveup_dir_path  
        results["current_dir_path"] = current_dir_path  
        results["current_url"] = current_url  
        results["total_count"] = len(file_list)  
        results["file_list"] = file_list  
    
        return HttpResponse(json.dumps(results))  
    else:
        return HttpResponse('Empty dir')
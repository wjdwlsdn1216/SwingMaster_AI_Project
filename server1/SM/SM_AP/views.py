from django.shortcuts import render
from django.shortcuts import redirect
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import cv2 
import sys
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import glob
from django.contrib.auth.models import User
from django.contrib import auth

# def runAlphapose(request) :
#     os.system('inference.sh')
#     return render(request, 'result.html')
percentage = [0,'대기중']

def index(request):
    return render(request,'index.html')

def video(request):
    return render(request,'video.html')

def result(request):
    # os.removedirs(settings.MEDIA_ROOT)
    global percentage
    percentage = [0, '|','프레임 분할중']
    data = request.FILES.get('file')
    if data == None :
        pass 
    else :
        name = data.name.split('.')
        path = default_storage.save('./action.' + name[-1], ContentFile(data.read()))
        cap = cv2.VideoCapture(settings.MEDIA_ROOT + "/action." + name[-1])
        frames = 0
        count = 0
        interval = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / 100
        length = 0
        while(cap.isOpened()):
                frames += 1
                ret, frame = cap.read()
                if frame is None:
                    break
                if length <= frames :
                    percentage[0] += 1
                    length += interval
                    cv2.imwrite(settings.MEDIA_ROOT + "./img/" + str(count).zfill(3) + ".jpg", frame)
                    count += 1

        cap.release()
        

        os.remove(settings.MEDIA_ROOT + "/action." + name[-1])
        from AlphaPose.scripts.demo_inference import alphaposeDemo
        alphapose = alphaposeDemo(percentage)
        alphapose.start()


        
    
        img_array = []
        for filename in glob.glob('./output/vis/*.jpg'):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)
    
        out = cv2.VideoWriter('./SM_AP/static/result.mp4',cv2.VideoWriter_fourcc(*'H264'), 15, size)
        
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
    
    return render(request,'result.html')
@csrf_exempt
def loadingRequest(request) :
    return HttpResponse(percentage)

def upload(request):
    
    return render(request,'result.html')

def signup(request):
    context = {}
    
    if request.method == 'POST':
        if (request.POST['username'] and
            request.POST['password'] and
            request.POST['password'] == request.POST['password_check']):

            new_user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
            )

            auth.login(request, new_user)
            return redirect('index')
        
        else:
            context['error'] = '아이디와 비밀번호를 다시 확인해주세요.'
    
    return render(request, 'signup.html', context)

def login(request):
    context = {}

    if request.method == 'POST':
        if request.POST['username'] and request.POST['password']:

            user =auth.authenticate(
                request,
                username=request.POST['username'],
                password=request.POST['password']
            )

            if user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                context['error'] = '아이디와 비밀번호를 다시 확인해주세요.'

        else:
            context['error'] = '아이디와 비밀번호를 모두 입력해주세요.'

    return render(request, 'login.html',context)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)

    return redirect('index')
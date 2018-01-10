#coding:utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.models import User  #user model
from django.core.urlresolvers import reverse #url逆向解析
from django.views.decorators.csrf import csrf_exempt
import json
from helper.crypto import encrypt,decrypt             #加密解密
from django.core.mail import EmailMultiAlternatives   #发送邮件
import time, re


def me(request):
    return render(request, 'me.html')


def check_is_login(request):
    """check the user is logined"""
    if request.user.is_authenticated():
        username=request.user.first_name
        if not username:
           username=request.user.username

        if request.user.is_active:
            active_state=''
        else:
            active_state=u'(未激活)'

        returnText=u'''
            <li role="presentation" class="dropdown">
                <a class="dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">
                    您好，%s%s <span class="caret"></span>
                </a>

                <ul class="dropdown-menu">
                    <li><a href="%s">退出</a></li>
                </ul>
            </li>''' % (username,active_state,reverse('user_logout'))#用reverse逆向解析user_logout得到网址
    else:
        #登录不成功就返回“登录”、“注册”的菜单
        returnText=u'''
            <li><a href="#" data-toggle="modal" data-target="#LoginModal">登录</a></li>
            <li><a href="#" data-toggle="modal" data-target="#RegModal">注册</a></li>'''
    return HttpResponse(returnText, content_type='application/javascript')

def user_logout(request):
    """logout"""
    logout(request)
    #记住来源的url，如果没有则设置为首页('/')
    returnPath=request.META.get('HTTP_REFERER', '/')
    #重定向到原来的页面，相当于刷新
    return HttpResponseRedirect(returnPath)

#由于用ajax提交，设置不到csrf，就先不进行csrf验证
@csrf_exempt
def user_login(request):
    """login"""
    response_data = {}

    try:
        login_name = request.POST.get('login_name')
        login_pwd = request.POST.get('login_pwd')

        if len(login_name)*len(login_pwd)==0:
            raise Exception(u"用户名或密码为空")

           #判断是否正确
        user = authenticate(username=login_name, password=login_pwd)
        if user is not None:
            login(request, user)#登录
        else:
            raise Exception(u"用户名或密码不正确")

        response_data['success'] = True
        response_data['message'] = 'ok'

    except Exception as e:
        response_data['success'] = False
        response_data['message'] = e.message
    finally:
        #返回json数据
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def user_reg(request):
    response_data = {}
    reg_name = ''

    try:
        reg_name = request.POST.get('reg_name')
        reg_email = request.POST.get('reg_email')
        reg_pwd = request.POST.get('reg_pwd')

        if len(reg_name)*len(reg_pwd)==0:
            raise Exception(u"用户名或密码为空")

        #匹配邮箱格式
        pattern = re.compile(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$')
        match = pattern.match(reg_email)
        if not match:
            raise Exception(u"邮箱格式不正确")

        #验证密码长度
        if len(reg_pwd)<6:
            raise Exception(u"密码不能少于6位")

        #判断用户是否存在
        user=User.objects.filter(email=reg_email)
        if len(user)>0:
            raise Exception(u"该邮箱已经被注册")

        #创建新用户
        user=User(username=reg_name,email=reg_name)
        user.set_password(reg_pwd)  #这样才会对密码加密加盐处理
        user.is_active=False
        user.save()

        response_data['success'] = True
        response_data['message'] = u'注册成功，并发送激活邮件到您的邮箱。'
    except Exception as e:
        response_data['success'] = False
        response_data['message'] = e.message
    finally:
        if response_data['success']:
            try:
                #发送激活邮件
                #不想用uuid模块生成唯一ID保存到数据库中，也不想用django-registration
                #安全级别要求不高，所以简单写个加密解密的方法来处理
                active_code=get_active_code(reg_name)
                send_active_email(reg_name,active_code)
            except Exception as e:
                response_data['message']=u'注册成功，激活邮件发送失败。请稍后重试 '+e.message

            #注册成功，登录用户
            user = authenticate(username=reg_name, password=reg_pwd)
            if user is not None:
                login(request, user)

        return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_active_code(email):
    """get active code by email and current date"""
    key=9
    encry_str='%s|%s' % (email,time.strftime('%Y-%m-%d',time.localtime(time.time())))
    active_code=encrypt(key,encry_str)
    return active_code

def send_active_email(email,active_code):
    """send the active email"""
    url='http://yshblog.com%s' % (reverse('user_active',args=(active_code,)))

    subject=u'[yshblog.com]激活您的帐号'
    message=u'''
        <h2>杨仕航的博客(<a href="http://yshblog.com/" target=_blank>yshblog.com</a>)<h2><br />
        <p>欢迎注册，请点击下面链接进行激活操作(7天后过期)：<a href="%s" target=_balnk>%s</a></p>
        ''' % (url,url)

    send_to=[email]
    fail_silently=True  #发送异常不报错

    msg=EmailMultiAlternatives(subject=subject,body=message,to=send_to)
    msg.attach_alternative(message, "text/html")
    msg.send(fail_silently)


def user_active(request,active_code):
    """user active from the code"""
    #加错误处理，避免出错。出错认为激活链接失效
    #解密激活链接
    key=9
    data={}
    try:
        decrypt_str=decrypt(key,active_code)
        decrypt_data=decrypt_str.split('|')
        email=decrypt_data[0]                                   #邮箱
        create_date=time.strptime(decrypt_data[1], "%Y-%m-%d")  #激活链接创建日期
        create_date=time.mktime(create_date)            #struct_time 转成浮点型的时间戳

        day=int((time.time()-create_date)/(24*60*60))     #得到日期差
        if day>7:
            raise Exception(u'激活链接过期')

        #激活
        user=User.objects.filter(username=email)
        if len(user)==0:
            raise Exception(u'激活链接无效')
        else:
            user=User.objects.get(username=email)

        if user.is_active:
            raise Exception(u'该帐号已激活过了')
        else:
            user.is_active=True
            user.save()

        data['goto_page']=True
        data['message']=u'激活成功，欢迎访问！博主会陆续发表高质量的原创博文。'
    except IndexError as e:
        data['goto_page']=False
        data['message']=u'激活链接无效'
    except Exception as e:
        data['goto_page']=False
        data['message']=e
    finally:
        #激活成功就跳转到首页(message页面有自动跳转功能)
        data['goto_url']='/'
        data['goto_time']=3000
        return render(request,'message.html',data)








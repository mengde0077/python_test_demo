#coding:utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.models import User  #user model
from django.contrib.auth import authenticate #验证密码是否正确
from django.core.urlresolvers import reverse #url逆向解析
from django.views.decorators.csrf import csrf_exempt
import json, time, datetime, random, string, re, logging
from helper.crypto import encrypt,decrypt             #加密解密
from helper import comments_count
from django.core.mail import EmailMultiAlternatives   #发送邮件
from .forms import ChangeNickForm,ChangePwdForm,ForgetPwdForm
from user_ex.models import User_ex
from django.utils import timezone

logger = logging.getLogger(__name__)

def login_page(request):
    return render(request,'user/login_page.html')


#添加用户中心的响应方法
def user_info(request):
    '''show the user infomations'''
    data={}
    user = request.user
    #判断是否登录了
    if request.user.is_authenticated():
        data['user'] = user
        data['comments_count'] = comments_count.get_comments_count(user.id)
        data['replies_count'] = comments_count.get_replies_count(user.id)
        data['replyed_count'] = comments_count.get_to_reply_count(user.id)
        data['last_talk_about'] = comments_count.last_talk_about(user.id)
        data['all_talk_about'] = comments_count.all_talk_about(user.id)
        return render_to_response('user/index.html',data)
    else:
        data['message'] = u'您尚未登录，请先登录! ' #提示消息
        # data['goto_page'] = True #是否跳转
        # data['goto_url'] = 'login'  #跳转页面
        # data['goto_time'] = 3000  #等待多久才跳转
        # return render_to_response('message.html',data)
        return render_to_response('user/login_page.html',data)


def check_is_login(request):
    """check the user is logined"""
    if request.user.is_authenticated():
        #change 2016-5-20
        username = request.user.first_name or request.user.username
        active_state = '' if request.user.is_active else u'(未激活)'
        admin_url = u'<li><a href="%s">后台管理</a></li>' % reverse('admin:index') if request.user.is_superuser else ''

        returnText=u'''
            <li role="presentation" class="dropdown">
                <a class="dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">
                    您好，%s%s <span class="caret"></span>
                </a>
                <ul class="dropdown-menu">
                    <li><a href="%s">用户中心</a></li>
                    %s
                    <!--<li role="separator" class="divider"></li>-->
                    <li><a href="%s">退出</a></li>
                </ul>
            </li>''' % (username, active_state,
                reverse('user_info'),
                admin_url,
                reverse('user_logout'))
    else:
        returnText=u"""
            <li><a href="#" data-toggle="modal" data-target="#LoginModal">登录</a></li>
            <li><a href="#" data-toggle="modal" data-target="#RegModal">注册</a></li>"""
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
    data = {}

    try:
        login_name = request.POST.get('login_name')
        login_pwd = request.POST.get('login_pwd')

        if len(login_name)*len(login_pwd)==0:
            raise Exception(u"用户名或密码为空")

           #判断是否正确
        user = authenticate(username=login_name, password=login_pwd)
        if user is not None:
            login(request, user)#登录
            logger.debug('登录成功')
            print('登录成功2')
        else:
            raise Exception(u"用户名或密码不正确")

        data['success'] = True
        data['message'] = '登录成功！'

    except Exception as e:
        data['success'] = False
        data['message'] = '登录失败,请重试！'
        logger.debug('登录失败:',e.message)
        print "登录失败：" , e.message
    finally:
        #返回json数据
        # return HttpResponse(json.dumps(data), content_type="application/json")
        data['goto_page'] = True #是否跳转
        data['goto_url'] = 'user_info'  #跳转页面
        data['goto_time'] = 1000  #等待多久才跳转
        return render_to_response('message.html',data)

@csrf_exempt
def user_reg(request):
    data = {}
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

        #判断用户名是否存在
        user=User.objects.filter(username=reg_name)
        if len(user)>0:
            raise Exception(u"该用户名已经被注册")

        #判断邮箱是否存在
        user=User.objects.filter(email=reg_email)
        if len(user)>0:
            raise Exception(u"该邮箱已经被注册")

        #创建新用户
        user=User(username=reg_name,email=reg_email)
        user.set_password(reg_pwd)  #这样才会对密码加密加盐处理
        user.is_active=False
        user.save()

        data['success'] = True
        data['message'] = u'注册成功，并发送激活邮件到您的邮箱。'
    except Exception as e:
        data['success'] = False
        data['message'] = e.message
    finally:
        if data['success']:
            try:
                #发送激活邮件
                #不想用uuid模块生成唯一ID保存到数据库中，也不想用django-registration
                #安全级别要求不高，所以简单写个加密解密的方法来处理
                active_code=get_active_code(reg_email)
                send_active_email(reg_email,active_code)
            except Exception as e:
                data['message']=u'注册成功，激活邮件发送失败。请稍后重试 '+e.message

            #注册成功，登录用户
            user = authenticate(username=reg_name, password=reg_pwd)
            if user is not None:
                login(request, user)

        # return HttpResponse(json.dumps(data), content_type="application/json")
        data['goto_page'] = True #是否跳转
        data['goto_url'] = 'user_info'  #跳转页面
        data['goto_time'] = 1000  #等待多久才跳转
        return render_to_response('message.html',data)

def get_active_code(email):
    """get active code by email and current date"""
    key=9
    encry_str='%s|%s' % (email,time.strftime('%Y-%m-%d',time.localtime(time.time())))
    logger.info(encry_str)
    print(encry_str)
    active_code=encrypt(key,encry_str)
    return active_code

def send_active_email(email,active_code):
    """send the active email"""
    url='http://myblog.com%s' % (reverse('user_active',args=(active_code,)))

    subject=u'[myblog.com]激活您的帐号'
    message=u'''
        <h2>的博客(<a href="http://yshblog.com/" target=_blank>yshblog.com</a>)<h2><br />
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



#装饰器，登录判断
def check_login(func):
    def wrapper(request):
        #登录判断，若没登录则跳转到前面写的信息提示页面
        if not request.user.is_authenticated():
            data = {}
            data['goto_url'] = '/user'
            data['goto_time'] = 3000
            data['goto_page'] = True
            data['message'] = u'您尚未登录，请先登录'
            return render_to_response('message.html',data)
        else:
            return func(request)
    return wrapper

@check_login
def nickname_change(request):
    data = {}
    data['form_title'] = u'修改昵称'
    data['submit_name'] = u'　确定　'

    if request.method == 'POST':
        #表单提交
        form = ChangeNickForm(request.POST)

        #验证是否合法
        if form.is_valid():
            #修改数据库
            nickname = form.cleaned_data['nickname']
            request.user.first_name = nickname
            request.user.save()

            #页面提示
            data['goto_url'] = reverse('user_info')
            data['goto_time'] = 3000
            data['goto_page'] = True
            data['message'] = u'修改昵称成功，修改为“%s”' % nickname
            return render_to_response('message.html',data)
    else:
        #正常加载
        nickname = request.user.first_name or request.user.username
        #用initial给表单填写初始值
        form = ChangeNickForm(initial={
            'old_nickname': nickname,
            'nickname': nickname,
            })
    data['form'] = form
    return render(request, 'user/form.html', data)

@check_login
def password_change(request):
    data = {}
    data['form_title'] = u'修改密码'
    data['submit_name'] = u'　确定　'

    if request.method == 'POST':
        #表单提交
        form = ChangePwdForm(request.POST)

        #验证是否合法
        if form.is_valid():
            #修改数据库
            username = request.user.username
            pwd = form.cleaned_data['pwd_2']
            request.user.set_password(pwd)
            request.user.save()

            #重新登录
            user = authenticate(username=username, password=pwd)
            if user is not None:
                login(request, user)

            #页面提示
            data['goto_url'] = reverse('user_info')
            data['goto_time'] = 3000
            data['goto_page'] = True
            data['message'] = u'修改密码成功，请牢记新密码'
            return render_to_response('message.html',data)
    else:
        #正常加载
        username = request.user.username
        form = ChangePwdForm(initial={'username':username})
    data['form'] = form
    return render(request, 'user/form.html', data)


def password_lost(request):
    """forgot password deals"""
    data = {}
    data['form_title'] = u'重置密码'
    data['submit_name'] = u'　确定　'

    if request.method == 'POST':
        #表单提交
        form = ForgetPwdForm(request.POST)

        #验证是否合法
        if form.is_valid():
            #修改数据库
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['pwd_2']
            user = User.objects.get(email = email)
            user.set_password(pwd)
            user.save()

            #删除验证码
            ex = User_ex.objects.filter(user=user)
            if ex.count() > 0:
                ex.delete()

            #重新登录
            user = authenticate(username=user.username, password=pwd)
            if user is not None:
                login(request, user)

            #页面提示
            data['goto_url'] = reverse('user_info')
            data['goto_time'] = 3000
            data['goto_page'] = True
            data['message'] = u'重置密码成功，请牢记新密码'
            return render_to_response('message.html',data)
    else:
        #正常加载
        form = ForgetPwdForm()
    data['form'] = form
    return render(request, 'user/pwd_forget.html', data)


def get_email_code(request):
    """get email code"""
    email = request.GET.get('email', '')
    code = ''.join(random.sample(string.digits + string.letters, 6))

    data = {}
    data['success'] = False
    data['message'] = ''

    try:
        #检查邮箱
        users = User.objects.filter(email = email)
        if len(users)==0:
            data['success'] = False
            data['message'] = u'此邮箱未注册'
            raise Exception, data['message']
        user = users[0]

        #检查短时间内是否有生成过验证码
        user_ex = User_ex.objects.filter(user = user)
        if len(user_ex)>0:
            user_ex = user_ex[0]

            #两个datetime相减，得到datetime.timedelta类型
            create_time = user_ex.valid_time
            td = timezone.now() - create_time
            if td.seconds < 60:
                data['message'] = u'1分钟内发送过一次验证码'
                raise Exception, data['message']
        else:
            #没有则新建
            user_ex = User_ex(user = user)

        #写入数据库
        user_ex.valid_code = code
        user_ex.valid_time = timezone.now()
        user_ex.save()

        #发送邮件
        subject=u'[mengde.com]激活您的帐号'
        message=u"""
            <h2>mengde的博客(<a href='http://mengde.com/' target=_blank>mengde.com</a>)<h2><br />
            <p>重置密码的验证码(有效期10分钟)：%s</p>
            <p><br/>(请保管好您的验证码)</p>
            """ % code

        send_to=[email]
        fail_silently=True  #发送异常不报错

        msg=EmailMultiAlternatives(subject=subject,body=message,to=send_to)
        msg.attach_alternative(message, "text/html")
        msg.send(fail_silently)

        data['success'] = True
        data['message'] = 'OK'
    except Exception as e:
        pass
    finally:
        return HttpResponse(json.dumps(data), content_type="application/json")








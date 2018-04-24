#coding=utf-8
from django.shortcuts import render, render_to_response
from .ldaprz import *
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext

def userauth(username,passwd):
    ldappath = 'ldap://myzero.com:389'
    baseDN = 'ou=People,dc=myzero,dc=com'
    p = ldapc(ldappath, baseDN)
    yanzheng = p.valid_user(username, passwd)
    ziliao = ''
    if yanzheng == True:
        ziliao = p.search_user(username)[0][1]
    else:
        ziliao = 1
    return ziliao

def login(request):
    cn_name = request.COOKIES.get('username', '')
    if cn_name != '':
        return HttpResponseRedirect("/index")
    if request.method == 'POST':
        username = request.POST['user']
        passwd = request.POST['passwd']
        find = userauth(username,passwd)
        if find != 1:
            # email = find['mail'][0]
            cn_name = find['cn'][0]
            response = HttpResponseRedirect("/index")
            # 将username写入浏览器cookie,失效时间为3600
            response.set_cookie('username', cn_name, 3600)
            return response
        else:
            log = '用户名或密码错误'

    return render_to_response('login.html', locals(),context_instance=RequestContext(request))

def logout(request):
    response = HttpResponseRedirect('/login')
    #清理cookie里保存username
    response.delete_cookie('username')
    return response
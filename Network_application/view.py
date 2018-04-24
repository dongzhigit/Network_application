#/usr/bin/python
#-*- coding: utf-8 -*-
from .sql_server import *
from django.utils.datastructures import SortedDict
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from Network_application.models import *
import datetime
import time
import urllib
import re

# 微信告警
# ——————————————————————————————————————————————————#
import urllib2
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import requests

def api_func(username,email):
    url = "http://192.168.50.249:40000/index/vpn_add?username=%s&email=%s" %(username,email)
    req = requests.get(url)
    return req.status_code


def emails(e):
    if len(e)>= 5:
        if re.match("[a-zA-Z0-9._-]+\@+efly-prouav.com",e) != None or re.match("[a-zA-Z0-9._-]+\@+zerotech.com",e) != None:
            return 'yes'
        return 'no'

def timezh(timeStamp):
    dateArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S",dateArray)
    return otherStyleTime

def gettoken(corpid, corpsecret):
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + corpsecret
    try:
        token_file = urllib2.urlopen(gettoken_url)
    except urllib2.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))
        sys.exit()
    token_data = token_file.read().decode('utf-8')
    token_json = json.loads(token_data)
    token_json.keys()
    token = token_json['access_token']
    return token

def senddata(access_token, user, content,topid,agentid):
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
    send_values = {
        "touser": user,  # 企业号中的用户帐号，在zabbix用户Media中配置，如果配置不正常，将按部门发送。
        "toparty": topid,  # 企业号中的部门id
        "msgtype": "text",  # 企业号中的应用id，消息类型。
        "agentid": agentid,
        "text": {
            "content": content
        },
        "safe": "0"
    }
    send_data = json.dumps(send_values, ensure_ascii=False)
    send_request = urllib2.Request(send_url, send_data)
    response = json.loads(urllib2.urlopen(send_request).read())
    print(str(response))

def gonggong(baojing,topid,user,agentid,corpsecret,):
    # topid = 2
    # agentid = 1000002
    # user = "LiDongZhi"
    content = baojing
    corpid = 'wwe87e2d282e6e7e33'
    # corpsecret = 'P9BT8XASfHSeGogNtRqEltPi0Zdq2gNkFmQ6DwQVX3g'
    accesstoken = gettoken(corpid, corpsecret)
    senddata(accesstoken, user, content,topid,agentid)

def network(request):
    if request.method == 'POST':
        username = str(request.POST['username'])
        department = str(request.POST['department'])
        claimant = str(request.POST['claimant'])
        company = str(request.POST['company'])
        mac = str(request.POST['mac'])
        project = str(request.POST['project'])
        begintime = str(request.POST['begintime'])
        endtime = str(request.POST['endtime'])
        # system_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        current_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        urltime = int(time.time())
        system_time = timezh(urltime)
        corpsecret = 'P9BT8XASfHSeGogNtRqEltPi0Zdq2gNkFmQ6DwQVX3g'
        hh = ''
        if username != '' and department != '' and claimant != '' and company != '' and mac != '' and project != '' and begintime != '' and endtime != '':
            log = 1
            current = datetime.datetime.strptime(current_date, '%Y-%m-%d')
            end = datetime.datetime.strptime(endtime, '%Y-%m-%d')
            begin = datetime.datetime.strptime(begintime, '%Y-%m-%d')
            delta1 = begin - current
            delta = end - begin
            sql = AppLog.objects.filter(mac=mac,begintime=begintime,endtime=endtime)
            if len(sql) >= 1:
                log = 5
            else:
                if delta1.days >= 0:
                    if delta.days < 0:
                        log = 3
                    elif delta.days >= 3:
                        log = 2
                    else:
                        sql = AppLog(username=username,
                                     department=department,
                                     claimant=claimant,
                                     company=company,
                                     mac=mac,
                                     project=project,
                                     begintime=begintime,
                                     endtime=endtime,
                                     operation_time=system_time,
                                     stats=0,
                                     comment=None)
                        sql.save()
                        urla = "http://36.110.16.250:818/queren/net?name=%s&department=%s&claimant=%s&company=%s&mac=%s&project=%s&begintime=%s&endtime=%s&system_time=%s" % (
                            urllib.quote(username), urllib.quote(department), urllib.quote(claimant), urllib.quote(company),
                            urllib.quote(mac),urllib.quote(project),urllib.quote(begintime),urllib.quote(endtime),urltime
                            )
                        xinxi = '申请人：' + username + \
                                '\n申请人部门：' + department + \
                                '\n被申请人：' + claimant + \
                                '\n被申请人公司：' + company + \
                                '\n物理地址(MAC)：' + mac + \
                                '\n所在项目名称：' + project + \
                                '\n开始日期：' + begintime + \
                                '\n结束日期：' + endtime + \
                                '\n申请时间：' + system_time + \
                                '\n请点击链接审批：' + urla
                        gonggong(xinxi,2,"LiDongZhi|YangLin",1000002,corpsecret)
                        hh = 1
                else:
                    log = 3
        else:
            log = 0
    return render_to_response('network.html', locals(),context_instance=RequestContext(request))

def openvpn(request):
    xinxi = 1
    log = 0
    corpsecret = 'njHqcndSq8VTRSP973UDIjMlflqDviSm3zWo6RdBvTQ'
    if request.method == 'POST':
        username = str(request.POST['username'])
        department = str(request.POST['department'])
        notes = str(request.POST['notes'])
        mail = str(request.POST['mail'])
        # system_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        urltime = int(time.time())
        system_time = timezh(urltime)
        urla = "http://36.110.16.250:818/queren/open?name=%s&mail=%s&department=%s&notes=%s&system_time=%s" %(urllib.quote(username),urllib.quote(mail),urllib.quote(department),urllib.quote(notes),urltime)
        if username != '' and mail != '' and department != '' and notes != '':
            if emails(mail) == 'yes':
                sql = OpenvpnLog.objects.filter(username=username)
                if len(sql) >= 1:
                    log = 3
                else:
                    sql = OpenvpnLog(
                        username=username,
                        mail=mail,
                        department=department,
                        notes=notes,
                        time=system_time
                    )
                    sql.save()
                    xinxi = '申请人：' + username + \
                            '\n申请人部门：' + department + \
                            '\n申请原因：' + notes + \
                            '\n申请时间：' + str(system_time) + \
                            '\n请点击连接审批：' + urla
                    gonggong(xinxi, 3, "LiDongZhi|YangLin", 1000004, corpsecret)
            else:
                log = 2
        else:
            log = 1
    return render_to_response('openvpn.html', locals(), context_instance=RequestContext(request))

def queren(request,a):
    tishi = ''
    sql = ''
    xinxi = ''
    topid = ''
    agentid = ''
    corpsecret = ''
    username = ''
    mail = ''
    # shnotes = request.POST['shnotes']
    if a == 'open':
        try:
            username = urllib.unquote(request.GET['name'])
            department = urllib.unquote(request.GET['department'])
            notes = urllib.unquote(request.GET['notes'])
            mail = request.GET['mail']
            urltime = int(request.GET['system_time'])
            system_time = timezh(urltime)
            try:
                sql = OpenvpnLog.objects.get(username=username,department=department)
            except:
                return HttpResponseRedirect('/404')
            topid = 2
            agentid = 1000004
            corpsecret = 'njHqcndSq8VTRSP973UDIjMlflqDviSm3zWo6RdBvTQ'
            xinxi = '申请已经审核通过' + \
                    '\n申请人：' + str(username) + \
                    '\n申请人邮箱：' + str(mail) + \
                    '\n申请人部门：' + str(department) + \
                    '\n申请原因：' + str(notes) + \
                    '\n申请时间：' + str(system_time)
                    # '\n审核结果：' + str(shnotes)
        except KeyError:
            return HttpResponseRedirect('/404')
    elif a == 'net':
        try:
            username = urllib.unquote(request.GET['name'])
            department = urllib.unquote(request.GET['department'])
            claimant = urllib.unquote(request.GET['claimant'])
            company = urllib.unquote(request.GET['company'])
            mac = request.GET['mac']
            project = urllib.unquote(request.GET['project'])
            begintime = request.GET['begintime']
            endtime = request.GET['endtime']
            urltime = int(request.GET['system_time'])
            # urltime = request.GET['system_time']
            system_time = timezh(urltime)
            try:
                sql = AppLog.objects.get(mac=mac,begintime=begintime,endtime=endtime)
            except:
                return HttpResponseRedirect('/404')
            topid = 3
            agentid = 1000002
            corpsecret = 'P9BT8XASfHSeGogNtRqEltPi0Zdq2gNkFmQ6DwQVX3g'
            xinxi = '申请已经审核通过' + \
                    '\n申请人：' + str(username) + \
                    '\n申请人部门：' + str(department) + \
                    '\n被申请人：' + str(claimant) + \
                    '\n被申请人公司：' + str(company) + \
                    '\n物理地址(MAC)：' + str(mac) + \
                    '\n所在项目名称：' + str(project) + \
                    '\n开始日期：' + str(begintime) + \
                    '\n结束日期：' + str(endtime) + \
                    '\n申请时间：' + system_time
                    # '\n审核结果：' + str(shnotes)
        except KeyError:
            return HttpResponseRedirect('/404')
    else:
        pass
    try:
        if sql.stats == 1:
            return HttpResponseRedirect('/ok')
    except AttributeError:
        return HttpResponseRedirect('/404')
    if request.method == 'POST':
        name = str(request.POST['submit'])
        notes = str(request.POST['shnotes'])
        if name == 'no':
            if notes != '':
                sql.stats = 1
                sql.comment = notes
                sql.save()
                gonggong(xinxi, topid, "@all", agentid, corpsecret)
                return HttpResponseRedirect('/ok')
            else:
                tishi = '请填写审批意见'
        else:
            create_vpn = api_func(username, mail)
            # if create_vpn == 100:
            sql.stats = 1
            sql.comment = notes
            sql.save()
            gonggong(xinxi, topid,"@all", agentid, corpsecret)
            return HttpResponseRedirect('/ok')
            # else:
            #     tishi = '系统内部错误,请联系管理员'
    return render_to_response('queren.html', locals(), context_instance=RequestContext(request))

def ok(request):
    return render_to_response('ok.html', locals(), context_instance=RequestContext(request))

def error_404(request):
    return render_to_response('404.html', locals(), context_instance=RequestContext(request))

def get_week_day(date):
    # tool_dict = {
    #     '0':'工作日',
    #     '1':'周末',
    #     '2':'假日',
    # }
    week_day_dict = {
    0 : '星期一',
    1 : '星期二',
    2 : '星期三',
    3 : '星期四',
    4 : '星期五',
    5 : '星期六',
    6 : '星期日',
    }
    # url_save = 'http://tool.bitefu.net/jiari/?d=%s' %date
    # s_save = urllib2.urlopen(url_save).read()
    day = datetime.datetime.strptime(date,'%Y%m%d').weekday()
    # return week_day_dict[day],tool_dict[s_save]
    return week_day_dict[day],day

def index(request):
    admin_list = ['李冬志', '徐亚楠', '张敏', '刘晶晶']
    cn_name = request.COOKIES.get('username','')
    begintime = (datetime.date.today().replace(day=1) - datetime.timedelta(1)).replace(day=26).__format__('%Y-%m-%d')
    endtime = datetime.date.today().replace(day=25).__format__('%Y-%m-%d')
    present_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    username = cn_name
    check_box_list = ''
    if cn_name == '':
        return HttpResponseRedirect("/login/")
    if request.method == 'POST':
        # username = request.POST['username'].encode('unicode-escape').decode('string_escape')
        try:
            username = request.POST['username']
        except KeyError:
            pass
        try:
            check_box_list = request.REQUEST.getlist("vehicle")[0]
        except IndexError:
            pass
        begintime = str(request.POST['begintime'])
        endtime = str(request.POST['endtime'])
        if begintime and endtime:
            if begintime <= endtime:
                format_begintime = datetime.datetime.strptime(begintime, '%Y-%m-%d').date()
                format_endtime = datetime.datetime.strptime(endtime,'%Y-%m-%d').date()
                ms = MSSQL()
                select_sql = "SELECT BADGENUMBER,USERID,NAME FROM USERINFO WHERE NAME='%s'" %username
                select_name_sql = ms.ExecQuery(select_sql)
                select_name_list = []
                for i in select_name_sql:
                    select_name_list.append((int(i[0]),i[1],i[2]))
                try:
                    select_name = max(select_name_list)
                    uid = select_name[1]
                    userid = select_name[0]
                # except IndexError:
                except ValueError:
                    exit()

                sql = "select USERID,CHECKTIME from CHECKINOUT where USERID=%s and CHECKTIME >= '%s' and CHECKTIME <= '%s'" %(uid,begintime,endtime+' 23:59:59')
                resList = ms.ExecQuery(sql)
                timelist = []
                for (id, weibocontent) in resList:
                    timelist.append(str(weibocontent).decode("utf8"))

                time_dic = SortedDict()
                for i in range((format_endtime - format_begintime).days + 1):
                    day = format_begintime + datetime.timedelta(days=i)
                    datename = str(day)
                    day_list = []
                    week,day = get_week_day(datename.replace('-', ''))
                    for y in timelist:
                        if datename in y:
                            day_list.append(y)
                    if day_list:
                        time_dic[datename] = {1:min(day_list)[11:16],2:max(day_list)[11:16],'name':username,'uid':uid,'userid':userid,'week':week,'day':day}
                    else:
                        time_dic[datename] = {'name':username,'uid':uid,'userid':userid,'week':week,'day':day}
            else:
                log = '起始日期不能大于结束日期'
        else:
            log = '请选择日期'
    return render_to_response('index.html',locals(),context_instance=RequestContext(request))
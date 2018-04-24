#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import ldap
import pymssql
import smtplib
from email.Header import Header
from email.mime.text import MIMEText

def send_email(eamil,content):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    sender = 'zeromail@zerotech.com'
    subject = '考勤状态提醒'
    smtpserver = 'smtp.zerotech.com'
    username = 'zeromail@zerotech.com'
    password = '123456Aa'

    message = MIMEText(content,'plain','utf-8')
    message['From'] = '人力资源部'
    message['To'] = Header(eamil)
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username, password)
        smtp.sendmail(sender, eamil, message.as_string())
        smtp.quit()
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"

class MSSQL:
    def __init__(self):
        self.host = '192.168.50.243'
        self.user = 'sa'
        self.pwd = '123asd!@#'
        self.db = 'kaoqin'

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def ExecQuery(self,sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        调用示例：
                ms = MSSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
                resList = ms.ExecQuery("SELECT id,NickName FROM WeiBoUser")
                for (id,NickName) in resList:
                    print str(id),NickName
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

ms = MSSQL()

def getYesterday(day): 
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=day) 
    yesterday=today-oneday  
    return yesterday

def get_week_day(date):
    day = date.weekday()
    return day

def search_users(): #模糊查找，返回一个list，使用search_s()
    ldap_path='ldap://myzero.com:389'
    baseDN='ou=People,dc=myzero,dc=com'
    l=ldap.initialize(ldap_path)
    l.protocol_version = ldap.VERSION3
    searchScope = ldap.SCOPE_SUBTREE
    searchFiltername = "uid" #通过samaccountname查找用户
    retrieveAttributes = None
    searchFilter = '(' + searchFiltername + '=*)'
    ldap_result =l.search_s(baseDN, searchScope, searchFilter, retrieveAttributes)
    if len(ldap_result) == 0: #ldap_result is a list.
        return "%s doesn't exist." %username
    else:
        return ldap_result

def select_uid(name):
    sql = "SELECT BADGENUMBER,USERID,NAME FROM USERINFO WHERE NAME='%s'" %name
    select_name1 = ms.ExecQuery(sql)
    select_name_list = []
    for i in select_name1:
        select_name_list.append((int(i[0]),i[1],i[2]))
    select_name = max(select_name_list)
    return select_name

def select_record(uid,day_time):
    sql = "select USERID,CHECKTIME from CHECKINOUT where USERID=%s and convert(varchar(10),CHECKTIME,120)='%s'" %(uid,day_time)
    select_name = ms.ExecQuery(sql)
    return select_name

def create_list(kaoqin_record):
    timelist = []
    for userid,u_number in kaoqin_record:
        timelist.append(str(u_number).decode("utf8"))
    return timelist

def min_value(timelist):
    min_value = str(min(timelist)[11:20])
    return min_value

def max_value(timelist):
    max_value = str(max(timelist)[11:20])
    return max_value

ldap_user_all = search_users()

day_1 = 1
day_2 = day_1 + 1
exclude_list = ['杨建军','杨霖','赵国栋','傅重阳','孙宇','张新璐','黄建','吕全辉','王帅钦','王笑非','代凌君','付家为','张晋华','罗金辉','孙宏涛','史圣卿','王浩','马千里','孙磊','崔红旭']
if get_week_day(getYesterday(day_1)) != 5 and get_week_day(getYesterday(day_1)) != 6:
    for i in ldap_user_all:
        name = str(i[1]['cn'][0])
        gid = str(i[1]['gidNumber'][0])
        email = str(i[1]['mail'][0])
        log = {}
        contrast_name = name in exclude_list
        if gid != '10008' and contrast_name == False:
            number,uid,name = select_uid(name)
            kaoqin_record = select_record(uid,getYesterday(day_1))
            timelist = create_list(kaoqin_record)
            if timelist:
                min_value1 = min_value(timelist)
                max_value1 = max_value(timelist)
                if '08:30:59' < min_value1 < '09:00:59':
                    if get_week_day(getYesterday(day_1)) == 0:
                        day_2 = day_1 + 3
                        kaoqin_record = select_record(uid,getYesterday(day_2))
                        timelist = create_list(kaoqin_record)
                        if timelist:
                            max_value2 = max_value(timelist)
                            if max_value2 < '20:00:59':
                                log[1] = min_value1
                                log[2] = max_value1
                        else:
                            log[1] = min_value1
                            log[2] = max_value1
                elif min_value1 > '08:30:59':
                    log[1] = min_value1
                    log[2] = max_value1

                if max_value1 < '17:29:59':
                    log[1] = min_value1
                    log[2] = max_value1
            else:
                log[3] = '无考勤记录'
            if log:
                content = ''
                zhu = '请于今日下班前提交相关的考勤单据。逾期将严格按考勤制度执行。\n考勤查询地址如下：\n网址：http://192.168.1.55/\n用户名：名字（全拼，小写）\t初始密码：123456\n已修改过密码的请忽略'
                if log.has_key(3):
                    content = 'Hi,零宝%s，%s考勤异常【考勤号：%s 状态：%s】，%s' %(name,getYesterday(day_1),number,log[3],zhu)
                elif log.has_key(1) or log.has_key(2):
                    content = 'Hi，零宝%s，%s考勤异常【考勤号：%s 首次打卡时间为：%s 末次的打卡时间为：%s】，%s' %(name,getYesterday(day_1),number,log[1][0:5],log[2][0:5],zhu)
                send_email(email,content)

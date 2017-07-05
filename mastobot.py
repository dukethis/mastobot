#!/usr/bin/python
# coding: UTF-8
"""
+ Mastodon Robot:
    - Connect & Log to a specific Mastodon instance (according to the application id credentials)
    - Show your timeline
    - Show your notifications
    - Show any account status

+ With https://github.com/halcy/Mastodon.py
$ sudo pip search Mastodon.py
$ sudo pip install [-U] Mastodon.py

+ With https://pypi.python.org/pypi/beautifulsoup4/
$ sudo pip search bs4
$ sudo pip install [-U] bs4

+ When an application APP_NAME is created,
+ it is registered on the Mastodon instance APP_BASE.
+ You can revoke the registration of any app. 
+ from your Mastodon account settings.
"""
import os,sys,re
from mastodon import Mastodon
from optparse import OptionParser
from bs4 import BeautifulSoup

def do_login():
    # Register app - only once!
    if not os.path.isfile( CIDFILE ):
        try: # Create application
            print("Creating application %s for Mastodon %s"%(APPNAME,APPBASE))
            Mastodon.create_app(APPNAME,
                                ['read','write','follow'],
                                api_base_url=APPBASE,
                                to_file=CIDFILE)
        except Exception as this:
            print( this )
            return
    # Create an application instance
    bot = Mastodon( client_id=CIDFILE, api_base_url=APPBASE )
    # Get the Mastodon's account login
    with open(LOGFILE,"r") as f:
        LOGIN = f.readlines()
        LOGIN = [ x.strip() for x in LOGIN ]
        MAIL = LOGIN[0]                 # 'my_login_email@example.com'
        PASS = LOGIN[1]                 # 'incrediblystrongpassword'
    try: bot.log_in( MAIL, PASS )
    except Exception as this:
        print("Mastobot was instantiated but login failed")
        print( this )
    return bot

def show_timeline(bot,n=10,mode=0):
    if   mode==0: rep = bot.timeline_home(limit=n)
    elif mode==1: rep = bot.timeline_local(limit=n)
    else:         rep = bot.timeline_public(limit=n)
    for ans in rep:
        dic = ans['account']
        t = ans['created_at'].encode('utf-8')
        t = re.sub('[TZ]',' ',t)
        u = ans['url'].encode('utf-8')
        c = ans['content']
        toot = BeautifulSoup(c,'lxml').get_text().encode('utf-8')
        print( "%s\n%s\n\033[0;2m%s\033[0;0;0m"%(t,toot,u) )

def show_notif(bot,n):
    notifs = bot.notifications()
    c=0
    for i,notif in enumerate(notifs):
        if notif=='error': return
        TYPE,ID,T = notif['type'],notif['id'],notif['created_at']
        T = re.sub('[TZ]',' ',T)
        USER = notif['account']['display_name'].encode('utf-8')
        USER += ' (%s)'%notif['account']['username'].encode('utf-8')
        print( "%d %s %-50s :%s"%(ID,T,USER,TYPE) )
        try:    CONTENT = notif['status']['content']
        except: continue
        URL = notif['status']['url']
        CONTENT = BeautifulSoup( CONTENT , 'lxml' ).get_text().encode('utf-8')
        print( CONTENT )
        print( "\033[1;1;42m%s\033[0;0;0m"%URL )
        c+=1
        if c >= n: break

def show_status(bot,x):
    try: this = bot.account(x)
    except:
        s = bot.search(x)
        if s and s['accounts']:
            print("%d accounts"%len(s['accounts']))
            this = s['accounts'][0]
    for k,v in this.items():
        print( "%-15s : %s"%(k,v) )

# DEFAULT OPTIONS
APPNAME="bigtoot"
APPBASE="https://octodon.social"
LOGFILE="/home/duke/bot/mastodon/login"
CIDFILE="/home/duke/bot/mastodon/%s_clientid"%APPNAME

# MAIN PROCESS
if __name__ == '__main__':

    # OPTIONS/ARGUMENTS PARSER:
    OP = OptionParser()
    OP.add_option('-n',dest='notif',help="List last notifications",type='int')
    OP.add_option('-t',dest='timeline',help="List timeline",type='int')
    OP.add_option('-m',dest='mode',help="0=Home ; 1=Local ; 2=Public",type='int',default=0)
    OP.add_option('-s',dest='status',help="Show account status (with ID or name)")
    # APPLICATION OPTIONS
    OP.add_option('-b',dest='appbase',help="Mastodon instance base url",default=APPBASE)
    OP.add_option('-x',dest='appname',help="Application name",default=APPNAME)
    OP.add_option('-l',dest='login',help="Application account's login",default=LOGFILE)
    
    opts,args = OP.parse_args()

    # LOG IN MASTODON:
    if args or any(opts.__dict__.values()):
        bot = do_login()
    # PROCESS ACTIONS:
    if   opts.notif:     show_notif(bot,opts.notif)                 # NOTIFICATIONS
    elif opts.timeline:  show_timeline(bot,opts.timeline,opts.mode) # TIMELINE
    elif opts.status:
        for arg in args: show_status(bot,arg)                       # ACCOUNT STATUS
    else:
        print(__doc__)

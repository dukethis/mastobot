#!/usr/bin/python3 -B
# coding: UTF-8
"""
* Mastodon Robot:
+ Connect & Login to a specific Mastodon instance (according to the application id credentials)
+ Show your timeline
+ Show your notifications
+ Show any account status

+ Using https://github.com/halcy/Mastodon.py
$ sudo pip search Mastodon.py
$ sudo pip install [-U] Mastodon.py

+ Using https://pypi.python.org/pypi/beautifulsoup4/
$ sudo pip search bs4
$ sudo pip install [-U] bs4

+ When an application APPNAME is created, it is registered on the Mastodon instance APPBASE.
+ You can revoke the registration of any application from your Mastodon account settings.
"""
import os,sys,re
from mastodon import Mastodon
from optparse import OptionParser
from bs4 import BeautifulSoup

def do_login():
    """ Returns a registered mastodon.Mastodon() instance """
    # CREATE THE INSTANCE
    if not os.path.isfile( CIDFILE ):                     # Register app - only once!
        try:                                              # Create application
            print("Creating application %s for Mastodon %s"%(APPNAME,APPBASE))
            Mastodon.create_app(APPNAME, ['read','write','follow'],
                                api_base_url=APPBASE, to_file=CIDFILE)
        except Exception as this:
            print( this )
            return    
    bot = Mastodon( client_id=CIDFILE,                     # Create an application instance
                    api_base_url=APPBASE )
    # LOGIN WITH THAT INSTANCE
    with open(LOGFILE,"r") as f:                           # Get the Mastodon's account login
        LOGIN = f.readlines()
        LOGIN = [ x.strip() for x in LOGIN ]
        MAIL = LOGIN[0]                                    # 'my_login_email@example.com'
        PASS = LOGIN[1]                                    # 'incrediblystrongpassword'
    try: bot.log_in( MAIL, PASS )
    except Exception as this:
        print("Mastobot was instantiated but login failed")
        print( this )
    return bot

def show_timeline(bot,n=10,mode=0,reverse=True):
    if   mode==0: rep = bot.timeline_home(limit=n)
    elif mode==1: rep = bot.timeline_local(limit=n)
    else:         rep = bot.timeline_public(limit=n)
    rep = rep[::-1] if reverse else rep
    for ans in rep:
        dic = ans['account']
        t = re.sub('[TZ]',' ',ans['created_at'])
        u = ans['url']
        c = ans['content']
        toot = BeautifulSoup(c,'lxml').get_text()
        print( t,toot,u,'\n' )

def show_notif(bot,n,reverse=True):
    notifs = bot.notifications()
    notifs = notifs[::-1] if reverse else notifs
    c=0
    for i,notif in enumerate(notifs):
        if notif=='error': return
        TYPE,ID = notif['type'],notif['id']
        T = re.sub('[TZ]',' ',ans['created_at'])
        USER = notif['account']['display_name']
        USER += ' (%s)'%notif['account']['username']
        print( "%d %s %-50s :%s"%(ID,T,USER,TYPE) )
        try:    CONTENT = notif['status']['content']
        except: continue
        URL = notif['status']['url']
        CONTENT = BeautifulSoup( CONTENT , 'lxml' ).get_text()
        print( CONTENT )
        print( URL )
        c+=1
        if c >= n: break

def show_status(bot,x):
    this = None
    try: this = bot.account(x)
    except:
        try: this = bot.status(x)
        except: pass
    if this:
        for k,v in this.items():
            print( "%-15s: %s"%(k,v) ) 
    else:
        s = bot.search(x)
        if s and s['accounts']:
            nacc = len(s['accounts'])
            if nacc > 1:
                print("%d accounts"%nacc)
                for this in s['accounts']:
                    abstract = ' ; '.join([ str(this[x]) for x in ['id','display_name','username','acct'] ])
                    print( abstract )
            else:
                this = s['accounts'][0]
                for k,v in this.items():
                    print( "%-15s: %s"%(k,v) )
                show_boost(bot, 5, this['id'])
                
def show_boost(bot,n=10,id=20600):
    print("Last boosts given")
    tl = bot.account_statuses(id,limit=n)
    for toot in tl:
        i = toot['id']
        t = re.sub('[TZ]','',toot['created_at'])
        u = toot['url']
        c = BeautifulSoup(toot['content'],'lxml').get_text()
        b = toot['reblogged']
        f = toot['favourited']
        print(i,t,u,"%s"%(int(b!=None)*"boosted "+int(f!=None)*"fav'd"+""))
        print(c+'\n')
    
# DEFAULT OPTIONS
APPNAME="bigtoot"
APPBASE="https://octodon.social"
LOGFILE="/home/duke/bot/mastodon/login"
CIDFILE="/home/duke/bot/mastodon/%s_clientid"%APPNAME

# MAIN PROCESS
if __name__ == '__main__':

    # OPTIONS/ARGUMENTS PARSER:
    OP = OptionParser()
    OP.add_option('-n','--notif',    dest='notif',   help="List last notifications",    type='int')
    OP.add_option('-l','--timeline', dest='timeline',help="List timeline",              type='int')
    OP.add_option('-m','--mode',     dest='mode',    help="Timeline mode: 0=Home,1=Local,2=Public",type='int',default=0)
    OP.add_option('-s','--status',   dest='status',  help="Show account status (with ID or name)", action='store_true')
    OP.add_option('-t','--toot',     dest='toot',    help="Toot this", action='store_true')
    
    # APPLICATION OPTIONS
    OP.add_option('-B',dest='appbase', help="Mastodon instance base url",  default=APPBASE)
    OP.add_option('-X',dest='appname', help="Application name",            default=APPNAME)
    OP.add_option('-L',dest='login',   help="Application account's login", default=LOGFILE)

    # REVERSE ORDER
    OP.add_option('-R',dest='reverse', help="Reverse order of results", action='store_true', default=True)

    opts,args = OP.parse_args()

    # LOG IN MASTODON:
    if not( args or any(opts.__dict__.values()) ):
        print(__doc__)
        sys.exit(0)
        
    bot = do_login()
    
    # PROCESS ACTIONS:
    if opts.notif:
        show_notif(bot,opts.notif,opts.reverse)                 # NOTIFICATIONS
    elif opts.timeline:
        show_timeline(bot,opts.timeline,opts.mode,opts.reverse) # TIMELINE
    elif opts.status:
        for arg in args:
            show_status(bot,arg)                                # ACCOUNT SEARCH/STATUS
    elif opts.toot:                                             # CASUAL TOOTING
        this = ' '.join(args)                     
        if input("%s\nToot this ? [Y/n] "%this) in ['','Y','y']:
            bot.toot( this )


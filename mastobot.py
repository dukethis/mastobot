#!/usr/bin/python
# coding: UTF-8
# https://github.com/halcy/Mastodon.py
"""
Mastodon Robot:
    - Connect & Log to Mastodon according to the application id credentials
    - Show specific toot providing its ID
    - Show your timeline
    - Show your notifications

With https://github.com/halcy/Mastodon.py

"""
import os,sys,re
from mastodon import Mastodon
from optparse import OptionParser
from bs4 import BeautifulSoup
#
# What instance is used ?
# « __DEFAULT_BASE_URL = https://octodon.social/ » in Mastodon.py
# ( mastodon.instance() ; mastodon.api_base_url )
#

LG_MAIL='groduke@gmail.com'                   # 'my_login_email@example.com'
LG_PASS='aquicktestfornow'                    # 'incrediblystrongpassword'
CC_FILE='/home/duke/.pytooter_clientcred.txt' # APPLICATION ID
US_FILE='/home/duke/.pytooter_usercred.txt'   # USER ID

def do_login():
	try: # Log on existing access
		bot = Mastodon( client_id=CC_FILE, access_token=US_FILE )
		#print( "Login is persisting" )
	except: # Create actual instance
		# Register app - only once!
		if not os.path.isfile(CC_FILE):
			print("Registering application for Mastodon") 
			Mastodon.create_app( 'pytooterapp', to_file=CC_FILE )
		bot = Mastodon(client_id=CC_FILE)
		bot.log_in( LG_MAIL, LG_PASS, to_file=US_FILE )
		print( "Login done" )
	return bot

def show_toot(bot,ID):
	dic = bot.status(ID)
	toot = BeautifulSoup(dic['content'],'lxml').get_text().encode('utf-8')
        t,u = dic['created_at'].encode('utf-8'),dic['url'].encode('utf-8')
	print( "%s %s\n%s"%(t,u,toot) )

def show_timeline(bot,n=10,local=True):
	if local: rep = bot.timeline_local(limit=n)
	else: rep = bot.timeline(limit=n)
	for ans in rep:
		dic = ans['account']
		t = ans['created_at'].encode('utf-8')
		u = ans['url'].encode('utf-8')
		c = ans['content'].encode('utf-8')
		toot = BeautifulSoup(c,'lxml').get_text().encode('utf-8')
		print( "\n%s %s\n%s"%(t,u,toot) )

def show_notif(bot,n):
	notifs = bot.notifications()
	c=0
	for i,notif in enumerate(notifs):
		TYPE,ID,T = notif['type'],notif['id'],notif['created_at']
		T = re.sub('[TZ]',' ',T)
		USER = notif['account']['display_name']+' ('+notif['account']['username']+')'
		print( "%d %s %-50s :%s"%(ID,T,USER,TYPE) )
		try:    CONTENT = notif['status']['content']
		except: continue
		URL = notif['status']['url']
		CONTENT = BeautifulSoup( CONTENT , 'lxml' ).get_text().encode('utf-8')
		print( CONTENT )
		print( "\033[1;1;42m%s\033[0;0;0m"%URL )
		c+=1
		if c >= n: break

if __name__ == '__main__':
    
	OP = OptionParser()
	OP.add_option('-n',dest='notif',help="List last notifications")
	OP.add_option('-t',dest='timeline',help="List timeline")
	OP.add_option('-i',dest='tootid',action='store_true',help="Show a specific toot")
	
	opts,args = OP.parse_args()

	# LOG IN MASTODON
	bot = do_login()

	# PROCESS ACTIONS:
	if opts.notif:      show_notif(bot,opts.notif)       # NOTIFICATIONS
	elif opts.timeline: show_timeline(bot,opts.timeline) # ACCOUNT TIMELINE
	elif opts.tootid:                                    # SHOW SPECIFIC TOOT
		for arg in args:
			try:    show_toot(bot,arg)
			except: pass


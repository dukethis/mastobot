# mastobot
<h3>Mastodon Application: A CLI tool to grab toots</h3>

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

When an application APPNAME is created, it is registered on the Mastodon instance APPBASE.
You can revoke the registration of any application from your Mastodon account settings.

<h3>Usage:</h3>
<pre>
$ mastobot.py -h
Usage: mastobot.py [options]

Options:
  -h, --help            show this help message and exit
  -n NOTIF, --notif=NOTIF
                        List last notifications
  -l TIMELINE, --timeline=TIMELINE
                        List timeline
  -m MODE, --mode=MODE  Timeline mode: 0=Home,1=Local,2=Public
  -s, --status          Show account status (with ID or name)
  -t, --toot            Toot this
  -B APPBASE            Mastodon instance base url
  -X APPNAME            Application name
  -L LOGIN              Application account's login
  -R                    Reverse order of results
</pre>

Enjoy :-)

# mastobot
<h3>Mastodon Application: A CLI tool to grab toots</h3>
+ Connect & Log to a specific Mastodon instance (according to the application id credentials)

+ Show your timeline

+ Show your notifications

+ Show any account status

+ Using https://github.com/halcy/Mastodon.py
<pre>
$ sudo pip search Mastodon.py
$ sudo pip install [-U] Mastodon.py
</pre>

+ Using https://pypi.python.org/pypi/beautifulsoup4/
<pre>
$ sudo pip search bs4
$ sudo pip install [-U] bs4
</pre>

When an application APPNAME is created, it is registered on the Mastodon instance APPBASE.
When the client ID is already existing, it's only login in.
You can revoke the registration of any app. from your Mastodon account settings.

<h3>Usage:</h3>
<pre>
$ mastobot.py -h
Usage: mastobot.py [options]

Options:
  -h, --help   show this help message and exit
  -n NOTIF     List last notifications
  -t TIMELINE  List timeline
  -m MODE      0=Home ; 1=Local ; 2=Public
  -s STATUS    Show account status (with ID or name)
  -b APPBASE   Mastodon instance base url
  -x APPNAME   Application instance name
  -l LOGIN     Application account's login
</pre>

Enjoy :-)

# mastobot
<h2>Mastodon simple robot</h2>

<h3>Install:</h3>

+ Download <a href="https://github.com/halcy/Mastodon.py">Mastodon.py</a> or install it via pip:

<pre>
$ sudo pip search mastodon
...
Mastodon.py (1.0.8)  - Python wrapper for the Mastodon API
...

$ sudo pip install Mastodon.py
</pre>

<h3>Usage:</h3>

<h4>Get the current timeline with 4 toots:</h4>
<pre>
$ mastobot.py -t4
</pre>

<h4>Get the 4 last notifications:</h4>
<pre>
$ mastobot.py -n4
</pre>

<pre>
$ mastobot.py -h
Usage: mastobot.py [options]

Options:
  -h, --help   show this help message and exit
  -n NOTIF     List last notifications
  -t TIMELINE  List timeline
  -i           Show a specific toot
</pre>


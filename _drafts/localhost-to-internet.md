---
layout: post
title: Localhost to Internet
categories: [Uncategorized]
tags: [Untagged]
comments: false
show-avatar: true
---

I'll realized this of-late while playing <a href="http://thinkwithportals.com/" target="_blank">Portal 2</a> (oh what a game!) in Co-op mode. People kept on asking my Hamachi IP, and I went ahead and created a subdomain so that it is easy for me and them to remember.

You'll need:
<ul>
	<li><span style="font-family: Arial; font-size: 10pt;"><a href="https://secure.logmein.com/products/hamachi2/download.aspx" target="_blank">Hamachi</a>
</span></li>
	<li><span style="font-family: Arial; font-size: 10pt;"><a href="http://www.apachefriends.org/en/xampp.html" target="_blank">XAMPP</a> or <a href="http://www.wampserver.com/en/" target="_blank">WAMP</a>
</span></li>
	<li><span style="font-family: Arial; font-size: 10pt;">A domain which allows custom name-servers (Free ones include <a href="http://www.dot.tk" target="_blank">.tk</a> &amp; <a href="http://www.co.cc/" target="_blank">.co.cc</a>)
</span></li>
	<li><span style="font-family: Arial; font-size: 10pt;">A webhost (Eg. <a href="http://x10hosting.com/" target="_blank">x10hosting</a>)
</span></li>
</ul>
<span style="font-family: Arial;">
I'm assuming that you are well versed with the tools and technologies I've mentioned above. If not, then comment below and I'll help you out.</span>
<ol>
	<li>Install Hamachi and it'll give you a static IP. This IP is given by Hamachi's VPN</li>
	<li>Create an A record for your domain in your webhost's control panel with the value/subdomain of your choice and Hamachi's IP</li>
	<li>Run XAMPP or WAMP</li>
	<li>Whatever you can see on <a href="http://localhost/">http://localhost/</a> can also be accessed via your new subdomain. In my case, <a href="http://h.pragith.net/">http://h.pragith.net/</a> is similar to <a href="http://localhost/">http://localhost/</a> (here on my laptop)</li>
</ol>
<span style="font-family: Arial;">
This way, you don't have to worry about giving your dynamic IP every time to users. Plus, your IP provided by your ISP also remains protected.</span>
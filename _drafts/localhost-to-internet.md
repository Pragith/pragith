---
layout: post
title: Localhost to Internet
categories: [Uncategorized]
tags: [Untagged]
comments: false
show-avatar: true
---

b'I\'ll realized this of-late while playing [Portal 2](http://thinkwithportals.com/) (oh what a game!) in Co-op mode. People kept on asking my Hamachi IP, and I went ahead and created a subdomain so that it is easy for me and them to remember.\n\nYou\'ll need:\n\n\t* [Hamachi](https://secure.logmein.com/products/hamachi2/download.aspx)\n
\n\t* [XAMPP](http://www.apachefriends.org/en/xampp.html) or [WAMP](http://www.wampserver.com/en/)\n
\n\t* A domain which allows custom name-servers (Free ones include [.tk](http://www.dot.tk) & [.co.cc](http://www.co.cc/))\n
\n\t* A webhost (Eg. [x10hosting](http://x10hosting.com/))\n
\n\n\nI\'m assuming that you are well versed with the tools and technologies I\'ve mentioned above. If not, then comment below and I\'ll help you out.\n\n\t2. Install Hamachi and it\'ll give you a static IP. This IP is given by Hamachi\'s VPN
\n\t4. Create an A record for your domain in your webhost\'s control panel with the value/subdomain of your choice and Hamachi\'s IP
\n\t6. Run XAMPP or WAMP
\n\t8. Whatever you can see on <http://localhost/> can also be accessed via your new subdomain. In my case, <http://h.pragith.net/> is similar to <http://localhost/> (here on my laptop)
\n\n\nThis way, you don\'t have to worry about giving your dynamic IP every time to users. Plus, your IP provided by your ISP also remains protected.'
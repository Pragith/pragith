---
layout: post
title: Easy way to check your Airtel High Speed Broadband usage
categories: [Uncategorized]
tags: [Untagged]
comments: false
show-avatar: true
---

<em>This post is meant for Airtel High Speed Broadband users only. If you're not one of them, then link(s) mentioned below will not work for you.</em>

Airtel has a <a href="http://122.160.230.125:8080/gbod/gb_on_demand.do" target="_blank">promo link</a> for their SmartBytes packages which shows how much you've used your High Speed data. I have it as a bookmark to make sure that I don't cross the limit so that I can enjoy the high speed throughout the month. Though ideally, that's not the case :P

My routine has been to open that page, then open the calculator and divide the total remaining quota by the (billing) days remaining. This is not an efficient way to do the math. At least not for a developer B-)

------Warning - Geeky stuff below this line------

So I hacked a small PHP script that queries the Airtel's URL, fetches the necessary parts like the balance quota and days left in the billing cycle and displays them on my browser, leaving all the flashy graphics.

But this wasn't enough. Because I can't open the browser everytime too. I'm _that_ lazy. I've cURL installed. So, I just do
<blockquote>curl &lt;the url here&gt;</blockquote>
and I get the necessary stuff right on my command prompt.

But typing "curl &lt;the url&gt;" is too much. So, I created a Batch file named, "bw" and it runs that command for me.

I'm right now thinking whether to rename the batch file from "bw" to just "b" ;)

<a href="http://pragith.net/airtel-broadband-usage/airtel-usage/" rel="attachment wp-att-718"><img class="aligncenter size-full wp-image-718" src="http://pragith.net/wp-content/Airtel-Usage.jpg" alt="Airtel Usage" width="596" height="342" /></a>

&nbsp;
<blockquote><a href="http://dl.pragith.net/airtel_usage.php" target="_blank">Download the PHP file from here</a></blockquote>
<em>Remember to run it from your own computer which is connected to Airtel Broadband. Hosting it elsewhere just won't work. This code should work fine until Airtel decides to make its promo page even more uglier.</em>

What you see in the screenshot above are:-
<ul>
	<li><strong>bw</strong> - It's a batch file bw.bat and contains the command <em><strong>curl http://z/airtel_usage.php</strong></em>
How to create a batch file? Type the following in command prompt
<strong>copy con the_file_name.bat</strong> (Enter key)
&lt;enter whatever you want the command prompt to do&gt; (Enter key)
&lt;then hit Ctrl+Z&gt;</li>
	<li><strong>http://z/</strong> - "z" is for "localhost". You should know by now how lazy I am to type "localhost"</li>
</ul>
Will figure out a way to accomplish the same using Javascript, so that Chrome users can have this feature as an extension.
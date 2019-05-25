---
layout: post
title: How-To Popovers with Bootstrap
categories: [Uncategorized]
tags: [Untagged]
comments: false
show-avatar: true
---

<strong>Difficulty</strong>: Beginner

<a href="http://labs.pragith.net/bootstrap-hero/popover/"><span style="font-size: 24pt;">Demo</span></a><span style="font-size: 24pt;"> | <a href="https://github.com/Pragith/pragith.github.com/blob/master/bootstrap-hero/popover/index.html">Source Code</a>
</span>

Popovers are a way to displaying rich content in the form of small overlays. With Twitter Bootstrap, you can easily implement Popovers on your site.

In this tutorial, we will implement Popovers using a simple Anchor tag.
<pre><code>          &lt;a href="#" class="btn example" rel="popover"	data-placement="top" data-content="Content for the popover" data-original-title="Title here"&gt;Popover Top&lt;/a&gt;</code></pre>
Let's breakdown this code and see how it is being implemented.
<ul>
	<li>class="example" – An ID or a CLASS is required for the Javascript code to understand which tag needs to have the popover effect. In this case, we are naming it "example"</li>
	<li>rel="popover" – As the attribute reads, it tells that the relation is a "popover"</li>
	<li>"data-" – Options can be appended to the data- attribute to customize our Popover. You can refer to the "Demo" for all the options available</li>
</ul>
A tiny snippet of Javascript code has to be included anywhere below the anchor tag which calls the Bootstrap's Javascript function and enables the Popover effect.

<span style="color: #333333; font-family: Consolas; font-size: 9pt;">    <span style="color: navy;">&lt;script&gt;</span></span>
<pre><code><span style="color: #333333; font-family: Consolas; font-size: 9pt;">    $(<span style="color: #dd1144;">'.example'<span style="color: #333333;">).popover()  
</span></span></span></code></pre>
<pre><code><span style="color: #333333; font-family: Consolas; font-size: 9pt;">    <span style="color: navy;">&lt;/script&gt;</span></span></code></pre>
As you can see in the Javascript code, we are using the jQuery convention of informing that the "popover" effect has to be applied to the class named, "example".
---
layout: post
title: How-To Hide "Featured Torrent" bar in uTorrent 3.2.2
categories: [Uncategorized]
tags: [Untagged]
comments: false
show-avatar: true
---

I recently updated to uTorrent 3.2.2 only to find an ugly looking advertisement sporting "Featured Torrent".

If you find it annoying too, then here's how you can remove it:
<ol>
	<li>Go <em>Options</em> ->;<em>Preferences</em></li>
	<li>Go to <em>Advanced</em></li>
	<li>In the <em>Filter</em> box, type <em>offer</em></li>
	<li>You'll find <strong><em>offers.sponsored_torrent_offer_enabled</em></strong></li>
	<li>By default it's set to <em>true</em>. Select <strong><em>false</em></strong></li>
	<li>Press <em>OK</em> and restart uTorrent</li>
</ol>
Voila!

<strong>By Fred</strong> from comments:

<blockquote>Also changing offers.left_rail_offer_enabled to "false" gets rid of the advert box on the bottom left and replaces with the standard "upgrade to pro" add
</blockquote>

Thanks Fred!
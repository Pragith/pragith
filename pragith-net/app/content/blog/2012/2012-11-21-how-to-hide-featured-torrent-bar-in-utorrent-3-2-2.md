---
title: "How to Hide the \"Featured Torrent\" Bar in uTorrent 3.2.2"
date: "2012-11-21"
tags: "tech, how-to"
status: "unpublished"
summary: "Quick fix to remove the annoying 'Featured Torrent' advertisement bar in uTorrent."
---

I recently updated to uTorrent 3.2.2 only to find an ugly-looking advertisement sporting "Featured Torrent."

If you find it annoying too, then here's how you can remove it:

1. Go to *Options* → *Preferences*
2. Go to *Advanced*
3. In the *Filter* box, type `offer`
4. You'll find **offers.sponsored_torrent_offer_enabled**
5. By default it's set to *true*. Select **false**
6. Press *OK* and restart uTorrent

Voilà!

**Bonus tip from Fred (via comments):**

> Also, changing `offers.left_rail_offer_enabled` to "false" gets rid of the advert box on the bottom left and replaces it with the standard "upgrade to pro" prompt.

Thanks, Fred!

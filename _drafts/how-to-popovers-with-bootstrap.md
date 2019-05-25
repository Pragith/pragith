---
layout: post
title: [How-To] Popovers with Bootstrap
categories: [Uncategorized]
tags: [Untagged]
comments: false
show-avatar: true
---

b'**Difficulty**: Beginner\r\n\r\n[Demo](http://labs.pragith.net/bootstrap-hero/popover/) | [Source Code](https://github.com/Pragith/pragith.github.com/blob/master/bootstrap-hero/popover/index.html)\r\n\r\n\r\nPopovers are a way to displaying rich content in the form of small overlays. With Twitter Bootstrap, you can easily implement Popovers on your site.\r\n\r\nIn this tutorial, we will implement Popovers using a simple Anchor tag.\r\n\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0<a href="#" class="btn example" rel="popover"\tdata-placement="top" data-content="Content for the popover" data-original-title="Title here">Popover Top</a>\r\nLet\'s breakdown this code and see how it is being implemented.\r\n\r\n\t* class="example" \xe2\x80\x93 An ID or a CLASS is required for the Javascript code to understand which tag needs to have the popover effect. In this case, we are naming it "example"
\r\n\t* rel="popover" \xe2\x80\x93 As the attribute reads, it tells that the relation is a "popover"
\r\n\t* "data-" \xe2\x80\x93 Options can be appended to the data- attribute to customize our Popover. You can refer to the "Demo" for all the options available
\r\n\r\nA tiny snippet of Javascript code has to be included anywhere below the anchor tag which calls the Bootstrap\'s Javascript function and enables the Popover effect.\r\n\r\n\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0<script>\r\n\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0$(\'.example\').popover() \r\n\r\n\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0</script>\r\nAs you can see in the Javascript code, we are using the jQuery convention of informing that the "popover" effect has to be applied to the class named, "example".'
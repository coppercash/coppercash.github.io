---
title: 'Why is SSL Handshake so Complicated?'
layout: post
tags:
  - SSL
---

When I first met SSL, I was finding a way to keep my data secreted while its transmitting between my server and iOS device. Then a mess of file types, such as .key .csr .crt .p12 .der .cer .pem, and the picture below just scared me. Why a data encrypt tech need to be so complicated?

![SSL Handshake Timing Diagram from Wikipedia](http://upload.wikimedia.org/wikipedia/commons/a/ae/SSL_handshake_with_two_way_authentication_with_certificates.svg)

After reading lot of articles and posts, I finally get some clues.

## Master Secret (MS)


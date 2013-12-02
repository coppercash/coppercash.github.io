---
title: 'Why is SSL Handshake so Complicated?'
layout: post
tags:
  - SSL
---

When I first met SSL, I was finding a way to keep my data secreted while its transmitting between my server and iOS device. Then a mess of file types, such as .key .csr .crt .p12 .der .cer .pem, and the picture below just scared me. Why a data encrypt tech need to be so complicated?

![SSL Handshake Timing Diagram from Wikipedia](http://upload.wikimedia.org/wikipedia/commons/a/ae/SSL_handshake_with_two_way_authentication_with_certificates.svg)

After reading lot of articles and posts, I finally get some clues. 
Let's start with a story about Harry wanna send a mail to Sirius through Internet. Umbridge, a super hacker for who Internet is totally transparent, trys to intercept. 

## Master Secret (MS)
When somebody want to send others a secret message, the first thing comes to him maybe to encrypt the message. Toachieve this, we need a pair of encrypt/decrypt methods and a Secret. The message can only be decrypted by the same Secret it be encrypted. 
It's a good idea, but not works in our story. Because Harry can't meet Sirius, so that he have to send the Secret, which used to encrypt the mail, through a mail too. That can be catched by Umbridge too. With the SECRET and the encrypt/decrypt methods is only few and they are all well known, Umbridge can decrypt and read the message.
To deal this problem, the world offers Asymmetric Cryptography

## Asymmetric Cryptography
The difference between Asymmetric Cryptography and traditional cryptograghy, also named Reciprocal cipher, is that it has two secret. And if you encrypt something with SECRET-A you can't decrypt it unless you have SECRET-B. 
The two secrets is well known as PUBLIC-KEY and PRIVATE-KEY. Their relations is like left and right. left is so called left is baecause the other side is called right. If you choose PUBLIC-KEY as PRIVATE-KEY, the PRIVATE-KEY can be used as PUBLIC-KEY too. And in fact we did use them that way.
So, with this fantanstic algorithm. Harry and Sirius both have a pair of keys, firstly they send their PUBLIC-KEY to each other openly. Secondly, the encrypt the message with each other's PULIC-KEY, which is just recieved. Because they know without PRIVATE-KEY, Umbridge is not able to decrypt their message. And the PRIVATE-KEY, of course, they will keep it private.

## Digital Signature
I'd like to tell you the story just get its end, but Umbridge is full of craft and cunning. She disguise herself as Sirius, and sends Harry her PUBLISH-KEY. Harry is so naive that he encrypt message with Umbridge's PUBLIC-KEY and send it out. When Harry and Sirius both find the fact it was too late, but they still needs a way to avoid this kind of attack happen again.
This kinf of attack is well known as Man-in-the-middle attack (MITM). People have invented a way named Digital Signature to avoid it. It is simple. Usually we use each other's PUBLIC-KEY to encrypt message, when do Digital Signature we just use own PRIVATE-KEY to encrypt. And the encrypted message should only can be decrypted with PUBLIC-KEY of whom encrypt it. What is interesting is that we do not need to care what the message is, you just decrypt it and make sure that is what you sent me, then it can prove it is me.

## Random Number
The story is not end yet, 'casuse Umbridge gets something new. She catchs some message, although she can't decrypt it, she find they are all same. This means lazy Harry send same message to Sirius and let him do Digitial Signature. when Sirius send signed message back, Harry succesfully decrypted with Sirius's PUBLIC-KEY, and believe the one on the other side is surely Sirius. Umbridge use Harry's lazy, and wait for Harry send out the old message, she send back Harry the message she kept and can't decrypt. Harry decrypt it once more, and he be fooled by Umbridge again.
Sirius is angry with that, he told Harry never use the same authentication messge, they need use Random Number. OK, there isn't real random in computer's world. The key here is when Umbridge send back an old mock authentication message, Harry will recognize it's not the one he just send out.

## Performance

## Negotiate

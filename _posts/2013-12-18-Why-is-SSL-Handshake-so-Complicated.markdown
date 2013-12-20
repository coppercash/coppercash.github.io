---
title: 'Why is SSL Handshake so Complicated?'
layout: post
tags:
  - SSL
---

When I first met SSL, I was finding a way to keep my data secreted while it's being transmitted between my server and iOS device. Then a mess of file types, such as .key .csr .crt .p12 .der .cer .pem, and the picture below just scared me. Why a data encryption tech need to be so complicated?

![SSL Handshake Timing Diagram from Wikipedia](/media/files/2013/12/18/SSL_handshake_with_two_way_authentication_with_certificates.svg)

After reading lot of articles and posts, I finally get some clues. 
Let's start with a story about Harry wanna send a mail to Sirius through Internet. Umbridge, a super hacker for whom Internet is totally transparent, trys to intercept. 

## Master Secret (MS)
When somebody wants to send others a secretive message, the first thing comes to him maybe is to encrypt the message. To achieve this, we need a pair of encrypt/decrypt methods and a `secret`. The message can only be decrypted using the same `secret` which was used to encrypt it. The diagram should be as simple as: 

![encrypt connection with Master Secret](/media/files/2013/12/18/ssl_01.png)

This is a good idea, but not works in our story. Because Harry can't meet Sirius, so that he has to send the `secret` through Internet too, just like he sends the message itself. We already know everything exposed on Internet can be catched by Umbridge. Since there are only a few encrypt/decrypt methods and they are all well known, Umbridge can decrypt and read the message.
To deal this problem, some wise men invented Asymmetric Cryptography

## Asymmetric Cryptography
One main difference between Asymmetric Cryptography and traditional cryptograghy (also named Reciprocal Cipher) is that the former has two secrets. And if you get something encrypted with SECRET-A, you can't decrypt it unless you have SECRET-B. 
The two secrets are well known as `public-key` and `private-key`. The relationship between them is like left and right. Left is so called left is baecause the other side is called right. If you choose `public-key` as `private-key`, the `private-key` can be used as `public-key` too. And in fact we did use them that way.
So, with this fantanstic algorithm. Harry and Sirius both have a pair of keys, firstly they send their `public-key` to each other openly. Secondly, the encrypt the message with each other's PULIC-KEY, which is just recieved. Because they know without `private-key`, Umbridge is not able to decrypt their message. And the `private-key`, of course, they will keep it private.

![encrypt connection with Master Secret](/media/files/2013/12/18/ssl_02.png)

## Digital Signature
I'd like to tell you the story just get its end, but Umbridge is full of craft and cunning. She disguise herself as Sirius, and sends Harry her PUBLISH-KEY. Harry is so naive that he encrypt message with Umbridge's `public-key` and send it out. When Harry and Sirius both find the fact it was too late, but they still needs a way to avoid this kind of attack happen again.
This kinf of attack is well known as Man-in-the-middle attack (MITM). People have invented a way named Digital Signature to avoid it. It is simple. Usually we use each other's `public-key` to encrypt message, when do Digital Signature we just use own `private-key` to encrypt. And the encrypted message should only can be decrypted with `public-key` of whom encrypt it. What is interesting is that we do not need to care what the message is, you just decrypt it and make sure that is what you sent me, then it can prove it is me.

![encrypt connection with Master Secret](/media/files/2013/12/18/ssl_03.png)

## Random Number
The story is not end yet, 'casuse Umbridge gets something new. She catchs some message, although she can't decrypt it, she find they are all same. This means lazy Harry send same message to Sirius and let him do Digitial Signature. when Sirius send signed message back, Harry succesfully decrypted with Sirius's `public-key`, and believe the one on the other side is surely Sirius. Umbridge use Harry's lazy, and wait for Harry send out the old message, she send back Harry the message she kept and can't decrypt. Harry decrypt it once more, and he be fooled by Umbridge again.
Sirius is angry with that, he told Harry never use the same authentication messge, they need use Random Number. OK, there isn't real random in computer's world. The key here is when Umbridge send back an old mock authentication message, Harry will recognize it's not the one he just send out.

![encrypt connection with Master Secret](/media/files/2013/12/18/ssl_04.png)

## Certificate
Using the methods mentioned above, we can ensure the messages are safe while being transfered. But it is not xianshi to just communiate with the people we know. Most time, we need to communicate with stangers. How can we ensure who is trustable and who is not?
Here has to be the forth people, Regulus, Sirius brother. He want to communicate with Harry via Internet too, but Harry doesn't know him. So Regulus write in his message, "I'm brother of Sirius, and he send the message to Sirius, Sirius does Digital Signature on the message and send it back. Next time when Regulus wants write to Harry He just embed this message in the mail, Harry would know it's Regulus someone believable and renzheng by Sirius.
The relationship message signed by Sirius is called CERTIFICATE, consists of TRUST CHAIN and the owner's `public-key`, and it is signed (digital) by Certificate Authority (CA, here Sirius). The TRUST CHAIN prove that the owner is trusted by the CA, and the taker can use the `public-key` to verify if it is truly the one in the CHAIN.

![encrypt connection with Master Secret](/media/files/2013/12/18/ssl_05.png)

## Performance
To here, we get all the tech/注意 we need. It seeds we should use CERTIFICATE to  verify the identity of each other, and use the a... Encrypt to encrypt message, our communication will be safe enough. But it still do not look like diagram above. Because there are two more things we need to do. Performance and Negotiate.
A en is safer than the traditional en, but it cost more time about 6 times more. So the solution is we use CERTIFICATE, a en and all tech mentioned above to ensure the safety of traditional en MASTER-KEY process. And use traditional en to finish communication.
According to the diagram, the protocol leave most of a en/de work to the client, so that server, which's amount and 性能 are limited.

![encrypt connection with Master Secret](/media/files/2013/12/18/ssl_06.png)

## Negotiate
SSL exists and improve for years. During these time, many different tra a en method version of certificate were invented and used. So the server and the client need to negotiate a group of the highest version method they both supported to garrunttee the highest safety of communication

## Final
So the process becaome what it is like in the diagram above finally.
Phase 1
Server and client send Random Number to each other and negotiiate the 算法 they will use later.
Phase 2
Server send its certificate, and demand client's certificate. After receive server's certificate, client will check if he knows this guy, or some CA knows this guy.

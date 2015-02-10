---
title: 'TCP/IP Summary'
layout: post
---

## Layers and Protocols
### Physical
+ RJ45
### Link
+ Ethernet 
	+ Frame: Head (18B) + Data (46-1500B)
	+ MAC (48b or 12x = 6x + 6x)
+ ARP (An Ethernet packet with FF:FF:FF:FF:FF:FF as destination MAC)
### Network
+ IP 
	+ Address (32b)
	+ Frame (65535): Head (20-60B) + Data
### Transport
+ Socket: Host + Port (0-1023-65535)
+ UDP
	+ Frame (65535): Head (8B) + Data
+ TCP 
	+ Frame (Infinite but better as long as IP, 65535): Head (20B)
### Application



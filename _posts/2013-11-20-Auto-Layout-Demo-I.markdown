---
title: 'Auto Layout Demo I'
layout: post
tags:
  - ios 
  - autolayout 
---

I implement some complex and typical ciucumstances in this [demo][http://github.com]

Case I - Buttons with multileve priorities

These three buttons obey rules in order:
1. Maintain (and try to extend) spaces between them
2. Try to display content completely
3. Try to keep equal width with each other

In other (auto layout's) words:
1. Horizontal Space (Greater Than or Equal) - priority 1000
2. Content Compression Resistance (Horizontal) - priority 750
3. Equal Widths - priority 700

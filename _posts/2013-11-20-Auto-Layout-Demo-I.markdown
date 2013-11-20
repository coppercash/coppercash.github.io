---
title: 'Auto Layout Demo I'
layout: post
tags:
  - ios 
  - autolayout 
---

I implement some complex and typical ciucumstances in this [demo](http://github.com)

### Case I - Buttons with multileve priorities

These three buttons obey rules in order:

1. Maintain (and try to extend) spaces between them
2. Try to display content completely
3. Try to keep equal width with each other

In other (auto layout's) words:

1. Horizontal Space (Greater Than or Equal) - priority 1000
2. Content Compression Resistance (Horizontal) - priority 750
3. Equal Widths - priority 700

See? If there is enough room all three buttons will has equal width

![SreenShot_00](https://raw.github.com/coppercash/Demo_AutoLayout/master/Github/ScreenShot_00.png)

If room is insufficient, spaces will be shrank, then the titles of buttons. But there is always some spaces left.

![ScreenShot_01](https://raw.github.com/coppercash/Demo_AutoLayout/master/Github/ScreenShot_01.png)

### Case II - Right edges keep space to superview's left edge

The array of labels aligned by right edge, and the longest one will always keep 20px from superview.

![SreenShot_02](https://raw.github.com/coppercash/Demo_AutoLayout/master/Github/ScreenShot_02.png)

When one label become too long, instaed of occupying the right space, that label will be shrank.

![SreenShot_03](https://raw.github.com/coppercash/Demo_AutoLayout/master/Github/ScreenShot_03.png)

To achieve this,

1. "Align Right Edges" to all the labels
2. "Pin Horizontal Spacing" (Greater Than or Equal, min value)  between one of the label (I pick the first one) and superview
3. "Pin Horizontal Spacing" (Equal, min value) to both left edge and right edge
4. The fatal, change the priorities of constraints added in step 3 to 200, which are lower than the label's "Content Huging Priority"

#!/usr/bin/env python
# ex: set ts=8 noet:
#
# Ryan 'pizza' Flynn (http://parseerror.com/)
#
# display Venn-diagram data in a "beachball" format, yuck!
# don't blame me, blame Ben Fry by way of unquietwiki
# <URL: http://www.reddit.com/r/SomebodyMakeThis/comments/bpb0y/smt_a_beach_ball_chart_maker/ >
#
# Requirements:
# 	python (http://python.org)
# 	cairo (http://cairographics.org)
# 	py2cairo (http://cairographics.org/pycairo/)
# 
# enter your data here
# ('NameX NameY', Pct, Color)
# whatever Pct is left over is considered 'None'

# original data
data = [
	('Palin',		 10.36, 'yellow'),
	('Palin Romney',	 15.54, 'green' ),
	('Romney', 		  6.66, 'red'   ),
	('Huckabee Romney',	 17.64, 'gray'  ),
	('Huckabee',		  7.56, 'red'   ),
	('Huckabee Palin',	 11.34, 'blue'  ),
	('Huckabee Palin Romney',26.46, 'yellow'), # 'All', center
]

filename = 'beachball'
width = 500.0
height = 500.0
fontsize = 20
fontname = "Times New Roman"

colors = { # available colors: 'color' : (r, g, b)
	'black': (0.0, 0.0, 0.0),
	'white': (1.0, 1.0, 1.0),
	'yellow':(1.0, 1.0, 0.0),
	'green': (0.0, 0.8, 0.0),
	'red':	 (0.8, 0.0, 0.0),
	'gray':	 (0.9, 0.9, 0.9),
	'blue':	 (0.0, 0.0, 0.9),
}

#####################################################

import cairo
from math import pi,radians,sin,cos
import sys

# secondary data
xc = width / 2
yc = width / 2
radius = width / 4
line = width / 3

#print('xc=%f yc=%f radius=%f line=%f' % (xc, yc, radius, line))

# display centered text as given position
def center_text(cr, x, y, bgrgb, names):
	set_text_color(cr, bgrgb)
	y -= fontsize / 2 # HACK
	for n in names.split(' '):
		_, _, width, height, _, _ = cr.text_extents(n)
		cr.move_to(x - width/2, y)
		cr.show_text(n)
		cr.stroke()
		y += height + 4

# figure out whether the fg color should be black or white based on bg color
def set_text_color(cr, bgrgb):
	if sum(bgrgb) < 1 and max(bgrgb) <= 0.9 and not (sum(bgrgb) == bgrgb[1]): # sufficiently dark
		cr.set_source_rgb(1, 1, 1)
	else:
		cr.set_source_rgb(0, 0, 0)

# set up
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(width), int(height))

cr = cairo.Context(surface)
cr.select_font_face(fontname)
cr.set_font_size(fontsize)

# white bg
cr.set_source_rgb(1.0, 1.0, 1.0)
cr.rectangle(0, 0, width, height)
cr.fill()
cr.stroke()

# black ball bg
cr.set_source_rgb(0,0,0)
cr.arc(xc, yc, radius+(line/2)+1, 0, 2 * pi)
cr.fill()
cr.stroke()

cr.set_line_width(line)

# graph data
pctMinusAll = sum([pct for _,pct,_ in data[:-1]]) # arc pct total
namepos = []
start = 0.0
for i in range(len(data)-1):
	name,pct,c = data[i]
	c = colors[c]
	# arc width in degrees
	w = (360.0 - (len(data)-1)) * (pct / pctMinusAll)
	if i == 0: # first arc display center top
		start = 270 - w/2
	# draw arc
	cr.set_source_rgba(c[0], c[1], c[2], 1)
	cr.arc(xc, yc, radius, radians(start), radians(start + w))
	cr.stroke()
	# calc name
	namepos.append((start, w, c, name + ' %4.2f%%' % (pct)))
	# loop
	start += w + 1

for start,w,rgb,name in namepos:
	x = xc + cos(radians(start + w/2)) * radius
	y = yc + sin(radians(start + w/2)) * radius
	center_text(cr, x, y, rgb, name)

# draw center
# circle
allName,allPct,allColor = data[-1:][0]
c = colors[allColor]
cr.set_source_rgba(c[0], c[1], c[2], 1)
cr.set_line_width(1)
cr.arc(xc, yc, radius/(100.0/allPct/2), 0, 2 * pi)
cr.fill()
cr.stroke()
# bg
cr.set_source_rgba(0,0,0,1)
cr.set_line_width(1)
cr.arc(xc, yc, radius/(100.0/allPct/2)+1, 0, 2 * pi)
# names
cr.set_source_rgb(0,0,0)
center_text(cr, xc, yc - fontsize / 2, c, '%s %4.2f%%' % (allName, allPct))

# display "None" in corner
nonePct = 100.0 - pctMinusAll - allPct
noneText = 'None %4.2f%%' % (nonePct)
_, _, noneWidth, noneHeight, _, _ = cr.text_extents(noneText)
cr.move_to(width - noneWidth - 20, height - noneHeight - 10)
cr.show_text(noneText)
cr.stroke()

# save
surface.write_to_png(filename + '.png')
surface.finish()


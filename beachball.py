#!/usr/bin/env python
# ex: set ts=8 noet:
# Ryan 'pizza' Flynn (http://parseerror.com/)
# display Venn-diagram data in a "beachball" format, yuck!
# don't blame me, blame
# <URL: http://www.reddit.com/r/SomebodyMakeThis/comments/bpb0y/smt_a_beach_ball_chart_maker/ >
# generates beachball.svg and beachball.png files
# required:
# python (http://python.org)
# cairo (http://cairographics.org)
# py2cairo (http://cairographics.org/pycairo/)
# 
# enter your data here
# ('NameX NameY', Pct, Color)
# whatever Pct is left over is considered 'None'
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
	'yellow':(0xf0, 0xde, 0x00),
	'green': (0x00, 0xbc, 0x00),
	'red':	 (0xc5, 0x00, 0x00),
	'gray':	 (0xce, 0xcf, 0xcd),
	'blue':	 (0x00, 0x00, 0xc2),
}

#####################################################

import cairo
from math import pi,radians,sin,cos
import sys

# secondary data
xc = width / 2
yc = width / 2
radius = width / 4
line = width / 4

#print('xc=%f yc=%f radius=%f line=%f' % (xc, yc, radius, line))

def center_text(cr, x, y, names):
	y -= fontsize / 2 # HACK
	for n in names.split(' '):
		_, _, width, height, _, _ = cr.text_extents(n)
		cr.move_to(x - width/2, y)
		cr.show_text(n)
		cr.stroke()
		y += height + 4

# set up
surface = cairo.SVGSurface(filename + '.svg', width, height)

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
	cr.set_source_rgba(c[0], c[1], c[2], 0.98)
	cr.arc(xc, yc, radius, radians(start), radians(start + w))
	cr.stroke()
	# calc name
	namepos.append((start, w, name + ' %4.2f%%' % (pct)))
	# loop
	start += w + 1

cr.set_source_rgb(0,0,0)
for start,w,name in namepos:
	x = xc + cos(radians(start + w/2)) * radius
	y = yc + sin(radians(start + w/2)) * radius
	center_text(cr, x, y, name)

# draw center
# circle
allName,allPct,allColor = data[-1:][0]
c = colors[allColor]
cr.set_source_rgba(c[0], c[1], c[2], 0.98)
cr.set_line_width(1)
cr.arc(xc, yc, line/2.1, 0, 2 * pi)
cr.fill()
cr.stroke()
# names
cr.set_source_rgb(0,0,0)
center_text(cr, xc, yc - fontsize / 2, '%s %4.2f%%' % (allName, allPct))

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


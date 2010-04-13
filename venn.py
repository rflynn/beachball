#!/usr/bin/env python
# ex: set ts=8 noet:
#
# Ryan 'pizza' Flynn (http://parseerror.com/)
#
# generate symmetrical Venn diagrams for 2,3,4 items

circles = [
	('Palin',		10.36, 'red'  ),
	('Romney', 		 6.66, 'green'),
	('Huckabee',		 7.56, 'blue' ),
]
# concatenated 'circles' key
# names must match circles names, must be separated with a space and appear in the order
# they do in 'circles'
overlap = {
	'Palin Romney'    :	15.54,
	'Romney Huckabee' :	17.64,
	'Huckabee Palin'  :	11.34,
	'Palin Romney Huckabee':26.46,
}

filename = 'venn'
width = 500.0
height = 500.0
fontname = 'Times New Roman'

#####################################################

# secondary data
isize = min([width,height])
fontsize = isize / 25 # scale fontsize accordingly
xc = isize / 2
yc = isize / 2
radius = isize / 3.75

colors = { # available colors: 'color' : (r, g, b)
	'black': (0.0, 0.0, 0.0),
	'white': (1.0, 1.0, 1.0),
	'red':	 (1.0, 0.0, 0.0),
	'green': (0.0, 1.0, 0.0),
	'blue':	 (0.0, 0.0, 1.0),
}

import cairo, itertools
from math import pi,radians,sin,cos

# display centered text as given position
def center_text(cr, x, y, c, names):
	cr.set_source_rgba(c[0],c[1],c[2],1)
	for n in names.split(' '):
		_, _, width, height, _, _ = cr.text_extents(n)
		cr.move_to(x - width/2, y)
		cr.show_text(n)
		cr.stroke()
		y += height + 4

# set up
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(width), int(height))

cr = cairo.Context(surface)
cr.select_font_face(fontname)
cr.set_font_size(fontsize)
cr.set_line_width(1)

# white bg
cr.set_source_rgb(1, 1, 1)
cr.rectangle(0, 0, width, height)
cr.fill()
cr.stroke()

# return (cos, sin) tuple
def cossin(xc, yc, deg, rad):
	return (xc + cos(radians(deg)) * rad, \
		yc + sin(radians(deg)) * rad)

start = 90
w = 360.0 / len(circles) # degrees in layout circle to each circle...
# draw circles
for name,pct,c in circles:
	# bg color
	c = colors[c]
	cr.set_source_rgba(c[0], c[1], c[2], 0.4)
	# draw circle
	x,y = cossin(xc, yc, start + w/2, radius * 0.75)
	cr.arc(x, y, radius, 0, 2*pi)
	cr.fill()
	cr.stroke()
	# circle label
	x,y = cossin(xc, yc, start + w/2, radius * 0.9)
	center_text(cr, x, y, colors['black'], '%s %4.2f%%' % (name, pct))
	# loop
	start += w

# label overlapping regions
if len(circles) > 2:
	start = 90 + w/2 # offset 1/2 of circles start
	for i,j in [(i, (i+1) % len(circles)) for i in range(len(circles))]:
		x,y = cossin(xc, yc, start + w/2, radius * 0.5)
		pct = overlap['%s %s' % (circles[i][0], circles[j][0])]
		center_text(cr, x, y, colors['black'], '%4.2f%%' % (pct))
		start += w

# label center region
allkey = ' '.join([name for name,_,_ in circles])
pct = overlap[allkey]
center_text(cr, xc, yc, colors['white'], '%4.2f%%' % (pct))

# save
surface.write_to_png(filename + '.png')
surface.finish()


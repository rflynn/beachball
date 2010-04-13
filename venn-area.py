#!/usr/bin/env python
# ex: set ts=8 noet:
#
# Ryan 'pizza' Flynn (http://parseerror.com/)
#
# generate symmetrical Venn diagrams for 2,3,4 items via smaller circles whose area reflects the data

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

filename = 'venn-area'
width = 500.0
height = 500.0
fontname = 'Times New Roman'

#####################################################

# secondary data
isize = min([width,height])
xc = isize / 2
yc = isize / 2
radius = isize / 2
maxfontsize = isize / 10

colors = { # available colors: 'color' : (r, g, b)
	'black': (0.0, 0.0, 0.0),
	'white': (1.0, 1.0, 1.0),
	'gray':  (0.9, 0.9, 0.9),
	'red':	 (1.0, 0.0, 0.0),
	'green': (0.0, 1.0, 0.0),
	'blue':	 (0.0, 0.0, 1.0),
	'yellow':(1.0, 1.0, 0.0),
}

import cairo, itertools
from math import pi,radians,sin,cos,sqrt

def scale_fontsize(pct):
	global maxfontsize
	# fontsize effects two axis, so we need sqrt to balance area
	return sqrt(maxfontsize * (pct / 100) * 36)

# display centered text as given position
def center_text(cr, x, y, c, names, pct):
	fontsize = scale_fontsize(pct)
	cr.set_font_size(fontsize)
	cr.set_source_rgba(c[0],c[1],c[2],1)
	y -= (fontsize / 1.5) * (names.count(' ') - 1)
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

# 
def scale_radius(pct):
	global isize
	return sqrt(isize * (pct / 100)) * 6

# label center region
allkey = ' '.join([name for name,_,_ in circles])
pct = overlap[allkey]
# draw center circle
alpha = 0.8
for name,_,c in circles:
	c = colors[c]
	cr.set_source_rgba(c[0], c[1], c[2], alpha)
	cr.arc(xc, yc, scale_radius(pct), 0, 2*pi)
	cr.fill()
	cr.stroke()
	alpha *= 0.8
center_text(cr, xc, yc, colors['white'], 'All %4.2f%%' % (pct), pct)

w = 360.0 / len(circles) # degrees in layout circle to each circle...

# label overlapping regions
if len(circles) > 2:
	start = 90 + w/2 # offset 1/2 of circles start
	for i,j in [(i, (i+1) % len(circles)) for i in range(len(circles))]:
		x,y = cossin(xc, yc, start + w/2, radius * 0.5)
		names = '%s %s' % (circles[i][0], circles[j][0])
		pct = overlap[names]
		# draw overlap circles
		for _,_,c in [circles[i], circles[j]]:
			c = colors[c]
			cr.set_source_rgba(c[0], c[1], c[2], 0.5)
			cr.arc(x+i, y, scale_radius(pct), 0, 2*pi)
			cr.fill()
		cr.stroke()
		# text
		center_text(cr, x, y, colors['black'], '%s %4.2f%%' % (names, pct), pct)
		start += w

start = 90
# draw circles
for name,pct,c in circles:
	# bg color
	c = colors[c]
	cr.set_source_rgba(c[0], c[1], c[2], 0.7)
	# draw circle
	x,y = cossin(xc, yc, start + w/2, radius * 0.75)
	cr.arc(x, y, scale_radius(pct), 0, 2*pi)
	cr.fill()
	cr.stroke()
	# circle label
	x,y = cossin(xc, yc, start + w/2, radius * 0.75)
	center_text(cr, x, y, colors['black'], '%s %4.2f%%' % (name, pct), pct)
	# loop
	start += w

# save
surface.write_to_png(filename + '.png')
surface.finish()


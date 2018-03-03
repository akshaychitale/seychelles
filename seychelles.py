from __future__ import print_function
from PIL import Image
import argparse
import math
import os

# By Akshay Chitale for r/vexillology on Reddit

# For Python 3
try:
	xrange
except NameError:
	xrange = range

class Seychelles:
	def __init__(self, name_in, size_out=None, name_out=None, ext_out=None):
		# Set up input
		self.name_in, self.ext_in = os.path.splitext(name_in)
		self.img_raw = Image.open(name_in)
		self.img_raw = self.img_raw.convert('RGB')
		self.size_in = self.img_raw.size
		# Flip so that colors are measured from top left
		self.img_in = self.img_raw.transpose(Image.FLIP_TOP_BOTTOM)

		# Set up output
		self.size_out = size_out if size_out else self.size_in
		self.name_out = name_out if name_out else self.name_in + '_out'
		self.ext_out = '.' + ext_out if ext_out else self.ext_in
		self.img_out = Image.new('RGB', self.size_out)
		self.pixels_out = self.img_out.load()

		# Set up image to print
		self.img_print = None

	def _angle_transfer(self, diagonal, seychelles):
		# Define transfer curve as a parabola
		x1, y1 = 0, 0
		x2, y2 = (diagonal, math.pi/4)
		x3, y3 = math.pi/2, math.pi/2
		# Below code from http://chris35wills.github.io/parabola_python/
		denom = (x1-x2) * (x1-x3) * (x2-x3);
		A     = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / denom;
		B     = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / denom;
		# C = 0 guaranteed because parabola goes through (0,0)
		if seychelles:
			# Going forward, use parabola
			return (lambda x: A*x*x + B*x)
		else:
			# Inverse, solve parabola y=ax^2+bx
			# Watch out for squares, where diagonal is pi/4 so A=0
			if abs(diagonal - math.pi/4) < 1E-9:
				return (lambda x: x)
			else:
				return (lambda x: (-1*B + math.sqrt(B*B - 4*A*(-x)))/(2*A))

	def seychelles(self, verbose=False):
		# Diagonal angle of output image
		out_diagonal = math.atan2(self.size_out[1], self.size_out[0])
		angle_transfer = self._angle_transfer(out_diagonal, True)
		# Find output color for each output pixel
		if verbose:
			print(' Progress:   0%', end='\r')
		for x in xrange(self.size_out[0]):
			if verbose:
				print('\r Progress: ' + str(int(100*x/self.size_out[0])).rjust(3) + '%', end='\r')
			for y in xrange(self.size_out[1]):
				# First, get the angle
				out_angle = math.atan2(y, x)

				# Then, follow the vector to the end of the flag
				out_x, out_y = x, y
				if x == 0 and y == 0:
					out_x, out_y = 1.0, 1.0
				elif out_angle < out_diagonal:
					# Scale by x
					out_x *= self.size_out[0]*1.0/x
					out_y *= self.size_out[0]*1.0/x
				else:
					# Scale by y
					out_x *= self.size_out[1]*1.0/y
					out_y *= self.size_out[1]*1.0/y

				# Get ratio of point radius to full radius
				point_rad = math.sqrt(x*x + y*y)
				out_rad = math.sqrt(out_x*out_x + out_y*out_y)
				rad_ratio = point_rad / out_rad

				# Coordinates on the input are:
				# x = radius, scaled by width of input
				in_x = rad_ratio * self.size_in[0]
				# y = angle, scaled by height of input
				in_y = angle_transfer(out_angle) * self.size_in[1] * 2.0 / math.pi

				# Ensure coordinates are within range
				in_x_int = int(round(in_x))
				if in_x_int < 0:
					in_x_int = 0
				elif in_x_int >= self.size_in[0]:
					in_x_int = self.size_in[0] - 1
				in_y_int = int(round(in_y))
				if in_y_int < 0:
					in_y_int = 0
				elif in_y_int >= self.size_in[1]:
					in_y_int = self.size_in[1] - 1

				# Assign input color to output color
				self.pixels_out[x,y] = self.img_in.getpixel((in_x_int, in_y_int))
		if verbose:
				print('\r Progress: 100%')
		# Flip so that seychelles is from bottom left
		self.img_print = self.img_out.transpose(Image.FLIP_TOP_BOTTOM)


	def inverse_seychelles(self, verbose=False):
		# Diagonal angle of input image
		in_diagonal = math.atan2(self.size_in[1], self.size_in[0])
		angle_transfer = self._angle_transfer(in_diagonal, False)
		# Find output color for each output pixel
		if verbose:
			print(' Progress:   0%', end='\r')
		for x in xrange(self.size_out[0]):
			if verbose:
				print('\r Progress: ' + str(int(100*x/self.size_out[0])).rjust(3) + '%', end='\r')
			for y in xrange(self.size_out[1]):
				# First, get the angle
				in_angle = angle_transfer(y * math.pi / 2.0 / self.size_out[1])

				# Get ratio of point to full width
				rad_ratio = x * 1.0 / self.size_out[0]

				# Then, follow the vector to the end of the flag
				if in_angle < in_diagonal:
					# Find by x
					in_x = self.size_in[0] * 1.0
					in_y = in_x * math.tan(in_angle)
				else:
					# Find by y
					in_y = self.size_in[1] * 1.0
					in_x = in_y / math.tan(in_angle)
				# Scale by radius ratio
				in_x, in_y = rad_ratio*in_x, rad_ratio*in_y

				# Ensure coordinates are within range
				in_x_int = int(round(in_x))
				if in_x_int < 0:
					in_x_int = 0
				elif in_x_int >= self.size_in[0]:
					in_x_int = self.size_in[0] - 1
				in_y_int = int(round(in_y))
				if in_y_int < 0:
					in_y_int = 0
				elif in_y_int >= self.size_in[1]:
					in_y_int = self.size_in[1] - 1

				# Assign input color to output color
				self.pixels_out[x,y] = self.img_in.getpixel((in_x_int, in_y_int))
		if verbose:
				print('\r Progress: 100%')
		# Flip so that seychelles is from bottom left
		self.img_print = self.img_out.transpose(Image.FLIP_TOP_BOTTOM)

	def save(self, name_out=None, ext_out=None):
		if self.img_print is None: raise Exception('No processing done yet')
		name = name_out if name_out else self.name_out
		ext = '.' + ext_out if ext_out else self.ext_out
		self.img_print.save(name + ext)

	def show(self):
		if self.img_print is None: raise Exception('No processing done yet')
		self.img_print.show()	

if __name__ == "__main__":
	# Parse args
	parser = argparse.ArgumentParser()
	parser.add_argument('image_in', type=str, help='Image file to process')
	parser.add_argument('-i', '--inverse', action='store_true', default=False, help='Do inverse seychelles')
	parser.add_argument('-s', '--size', type=int, nargs=2, default=None, help='Output image width and height')
	parser.add_argument('-n', '--name', type=str, default=None, help='Output file name')
	parser.add_argument('-e', '--ext', type=str, default=None, help='Output file extension')
	parser.add_argument('-d', '--display', action='store_true', default=False, help='Display output instead of saving to file')
	parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Display progress while processing')
	args = parser.parse_args()

	# Run Seychelles
	s = Seychelles(args.image_in, size_out=args.size, name_out=args.name, ext_out=args.ext)
	if(args.inverse):
		s.inverse_seychelles(verbose=args.verbose)
	else:
		s.seychelles(verbose=args.verbose)
	if(args.display):
		s.show()
	else:
		s.save()


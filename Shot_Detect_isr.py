#Practice Interrupt
# Author: Brendan Le Foll <brendan.le.foll@intel.com>
# Copyright (c) 2014 Intel Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE

import alsaaudio
import mraa
import time
import sys

class Counter:
  count = 0

c = Counter()

# inside a python interrupt you cannot use 'basic' types so you'll need to use
# objects
def test(gpio):
  print "Gunshot"
  print c.count
  print("pin " + repr(gpio.getPin(True)) + " = " + repr(gpio.read()))
  c.count+=1

pin = 4;
if (len(sys.argv) == 2):
  try:
    pin = int(sys.argv[1], 10)
  except ValueError:
    printf("Invalid pin " + sys.argv[1])
try:
	x = mraa.Gpio(pin)
	print("Starting ISR for pin " + repr(pin))
	x.dir(mraa.DIR_IN)
	x.isr(mraa.EDGE_BOTH, test, x)
	print'are we looping?'
	#
	var = raw_input("Press ENTER to stop")
	#arecord -f cd output_stereo.wav
	x.isrExit()
except ValueError as e:
    print(e)

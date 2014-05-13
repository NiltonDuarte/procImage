# -*- coding: utf-8 -*-

from math import *

def gaussianFunc(dp, d):
	gF = (1.0/(sqrt(2.0*pi)*(dp))) * exp(-(d**2)/(2.0*(dp**2)))
	return gF

from proc_img import *


myImg = MyImg("gaussianRGB--gaussianRGB--face2.JPG")

simple3CFilters = Simple3ChannelsFilters()

myImg.applySimple3ChannelsFilters(simple3CFilters.skin,[])
myImg.save()

#complex3CFilters = Complex3ChannelsFilters()

#myImg.applyComplex3ChannelsFilters(complex3CFilters.gaussianRGB, [], 5)
#myImg.save()


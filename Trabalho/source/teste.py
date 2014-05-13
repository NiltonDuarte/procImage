from proc_img import *


myImg = MyImg("../img/face.png")

simple3CFilters = Simple3ChannelsFilters()

complexFilters = ComplexFilters()

"""myImg.setColorGrayScale()
myImg.applyComplexFilter(complexFilters.gaussian, [1.5], 5)
myImg.save()
myImg.applyComplexFilter(complexFilters.gaussian, [1.5], 5)
myImg.save()
myImg.applyComplexFilter(complexFilters.gaussian, [1.5], 5)
myImg.save()
myImg.applyComplexFilter(complexFilters.gaussian, [1.5], 5)
myImg.save()
myImg.applyComplexFilter(complexFilters.sobel,[])
myImg.save()"""

complex3CFilters = Complex3ChannelsFilters()

myImg.applyComplex3ChannelsFilters(complex3CFilters.gaussianRGB, [], 5)
myImg.save()
myImg.applyComplex3ChannelsFilters(complex3CFilters.gaussianRGB, [], 5)
myImg.save()
myImg.applySimple3ChannelsFilters(simple3CFilters.skin,[])
myImg.save()


"""RGB=[123,121,158]
Y = 16 + (0.257*RGB[0] + 0.504*RGB[1] + 0.098*RGB[2]);
Cb = 128 + (-0.148*RGB[0] - 0.291*RGB[1] + 0.439*RGB[2]);
Cr = 128 + (0.439*RGB[0] - 0.368*RGB[1] - 0.071*RGB[2]);
YCbCr = (Y, Cb, Cr)
print YCbCr"""


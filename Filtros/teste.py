from proc_img import *


myImg = MyImg("face.png")

simple3CFilters = Simple3ChannelsFilters()

myImg.Simple3ChannelsFilters(simple3CFilters.skin)
myImg.save()


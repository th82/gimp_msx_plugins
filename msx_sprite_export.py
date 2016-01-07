#!/usr/bin/env python


import math
from gimpfu import *
from struct import *

def msx_sprite_export(timg, tdrawable):
    print('Starting msx_sprite_export procedure...')
    
    #get the dimensions of the drawable (layer)
    width = tdrawable.width
    height = tdrawable.height
    
    img_filename = timg.filename    #get the image filename
   
    #check if the selected drawable (layer) is a small (8x8) or big (16x16) sprite
    if width == height:
        if width == 8:
            bBigSprite = False
            gimp.message("Small sprite...\n")
        elif width == 16:
            bBigSprite = TRUE
            gimp.message("Big sprite....\n")
        else:
            gimp.message("Wrong sprite dimensions. Sprite must be either 8x8 or 16x16 pixels.\n")
    else:
        gimp.message("Wrong sprite dimensions. Sprite must be either 8x8 or 16x16 pixels.\n")
        
    #check if the drawable is an indexed image with an alpha channel (transparency)
    #
    #tbd
    #
        
    #create pixel region (with the size of the entire drawable)
    px_region = tdrawable.get_pixel_rgn(0, 0, width, height, FALSE, FALSE) 
    
    #open file for output
    sprite_filename = ('{filename}.bin'.format(filename = img_filename))    #appends .bin to the image file
    #print(sprite_filename)
    sprite_file = open(sprite_filename, 'wb')
    
    #initailize the variable for byte data and counter
    SPTbyte = 0
    byteCounter = 0
    
    #set the numbers of blocks to export based on the sprite size
    if bBigSprite:
        xblocks = 2
        yblocks = 2
    else:
        xblocks = 1
        yblocks = 1
    
    #loop through the image data to create a calculate a byte for each row (8x1 px) of the image    
    for i in range(0, xblocks):     #for each xblock (8px wide)
        for j in range(0, yblocks): #for each yblock (8px high)
            for k in range(0, 8):   #for each row    (8 rows per block)
                
                SPTbyte = 0         #reset the data byte
                for l in range(0, 8):   #for each pixel (8 pixels per row)
                    px_data = px_region[i*8+l, j*8+k]   #for indexed drawables with alpha channel each pixel holds color and alpha
                    px_alpha = px_data[1]   #alpha is index 1 (color is index 0)
                    #print('pixel color', px_alpha)
                    if px_alpha == '\xff':
                        #if the pixel is not transparent
                        SPTbyte = SPTbyte + 2**(7-l)
                print('xblock = {0:d}, yblock = {1:d}, byteno. = {2:d}, data = {3:x}'.format(i, j, k, SPTbyte))    
                #gimp.message("read block ({0:d},{0:d}) - byte {0:d} = {0:x}".format(i, j, k, SPTbyte))
                        
                byteCounter = byteCounter + 1
                byteToWrite = pack("B",SPTbyte)     #pack to unsigned char
                sprite_file.write(byteToWrite)
    
    #close file
    sprite_file.flush()
    sprite_file.close()                    
    
    gimp.message("{0:d} bytes exported to {1:s}.".format(byteCounter, sprite_filename))
    print('Finished msx_sprite_export procedure.')

register(
        "msx_sprite_export",
        "Export sprite binary data for MSX1 VDP",
        "Export sprite binary data for MSX1 VDP",
        "Thies Hecker",
        "Thies Hecker",
        "2016",
        "<Image>/Filters/Misc/_MSXspriteEx...",
        "GRAY*, INDEXED*",
        [],
        [],
        msx_sprite_export)

main()
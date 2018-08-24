#!/usr/bin/python

import argparse
import glob
import os
import re
import sys

import cv2
import numpy as np

import __main__ as main


def loadImage(src):
    img = cv2.imread(src)
    if not img is None:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def findCoins(img, showCoins = False):
    scaling = 800.0/max(img.shape[0:2])
    print scaling
    img_gray = cv2.resize(img, None, fx=scaling, fy=scaling)
    img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.blur(img_gray, (5,5))
    coins = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1.2, 30, param2 = 35, minRadius = 20, maxRadius = 50)
    coins = (np.round(coins[0,:]) / scaling).astype("int")
    return coins

if hasattr(main, '__file__'):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("glob", help="a glob pattern of source images to process")
    parser.add_argument("-o", "--output", default="classified", help="output directory")
    parser.add_argument("-v", "--verbose", action = "store_true")
    parser.add_argument("--format", default="jpg", choices=["png","jpg"], help="output format")
    parser.add_argument("--size", default="150", type=int, help="dimension of output images")
    parser.add_argument("--slice-size", default=None, type=int, help="size of slice in source image")
    args = parser.parse_args()

    for srcImage in glob.glob(args.glob):
        (imgPath, imgName) = os.path.split(srcImage)
        (imgBase, srcExt) = os.path.splitext(imgName)
        (typePath, typeName) = os.path.split(imgPath)
        img = loadImage(srcImage)
        if img is None:
            break
        coins = findCoins(img, showCoins = True)
        if args.verbose:
            print('{} ({} coins)'.format(srcImage, coins.shape[0]))
        if coins is None:
            break

        maxRadius = args.slice_size/2 if args.slice_size else np.amax(coins,0)[2]
        for ix,(x,y,r) in enumerate(coins):
            img_coin = img[y-maxRadius:y+maxRadius, x-maxRadius:x+maxRadius]
            if img_coin.shape[0]==0 or img_coin.shape[1]==0:
                continue
            img_coin = cv2.resize(img_coin, (args.size,args.size))
            outDir = os.path.join(args.output, typeName)
            if not os.path.exists(outDir):
                os.makedirs(outDir)
            outName = "%s_%s.%s" % (imgBase, ix, args.format)
            outName = os.path.join(outDir, outName)
            cv2.imwrite(outName, cv2.cvtColor(img_coin, cv2.COLOR_RGB2BGR))
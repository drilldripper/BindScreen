# coding: UTF-8
from PIL import ImageGrab
from PIL import Image, ImageChops
import time
import win32com.client
import hashlib
import os
import re
import shutil
import argparse

def md5(filename):
	with open(filename, "rb") as f:
		data = f.read()
	return hashlib.md5(data).hexdigest()

def take_picture(direction, initTime, intervalTime, path):
    """画面が変化しなくなるまでスクリーンショットを撮る"""
    shell = win32com.client.Dispatch("WScript.Shell")
    time.sleep(initTime)
    img = ImageGrab.grab()

    spread_path = path + "/spread_image/"
    os.mkdir(spread_path)
    img.save(spread_path + "1.png")

    i = 2
    while(1):
        shell.SendKeys(direction)
        time.sleep(intervalTime)
        img = ImageGrab.grab()
        img.save(spread_path + str(i)+".png")

        # 一つ前のスクリーンショットと同じ画像なら終了する
        if md5(spread_path + str(i) + ".png") == md5(spread_path + str(i-1) + ".png"):
            break
        i += 1 
        print("next")
    print("end")

def split_image(path, direction = "RIGHT"):
    """画像を横に２分割する"""
    spread_path = path + "/spread_image/"
    files = os.listdir(spread_path)
    split_path = path + "/split_image/"
    os.mkdir(split_path)
    # ファイルの長さを考慮に入れて数値順にファイルをソートする
    sorted_files = sorted(files, key=lambda x: (len(x), x))
    for file in sorted_files:
        img = Image.open(spread_path + file)
        index, ext = file.split(".")
        if direction == "RIGHT":
            # print("R")
            img.crop((0, 0, int(img.size[0]/2), img.size[1])).save(split_path+index+'_2.png')
            img.crop((int(img.size[0]/2), 0, img.size[0], img.size[1])).save(split_path+index+'_1.png')
        else :
            # print("L")
            img.crop((0, 0, int(img.size[0]/2), img.size[1])).save(split_path+index+'_1.png')
            img.crop((int(img.size[0]/2), 0, img.size[0], img.size[1])).save(split_path+index+'_2.png')


def trim(path):
    """余白を消去する"""
    split_path = path + "/split_image/"
    files = os.listdir(split_path)
    trim_path = path + "/trim_images/"
    os.mkdir(trim_path)
    # ファイルの長さを考慮に入れて数値順にファイルをソート
    sorted_files = sorted(files, key=lambda x: (len(x), x))
    for file in sorted_files:
        img = Image.open(split_path + file)
        bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
        diff = ImageChops.difference(img, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            img.crop(bbox).save(trim_path + file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script is to automate screen shot function")
    parser.add_argument("dstPath", help="出力するファイルのパスを指定する。")
    parser.add_argument("instruction", help="キーボードの命令を指定する。←なら'{LEFT}'を指定する")
    parser.add_argument("openingDirection", help="見開き方向を指定する。右開きなら'RIGHT'を指定する")
    parser.add_argument("initTime", nargs='?',
                        help="プログラムが最初に実行されるまでの時間を指定する(秒)", type=int)
    parser.add_argument("intervalTime", nargs='?',
                        help="命令を送る間隔を指定する", type=int)
    parser.add_argument("--zip",
                        help="指定すると最終的な出力ファイルを圧縮して出力する",
                        action="store_true",)
    
    args = parser.parse_args()

    if args.initTime:
        initTime = args.initTime
    else:
        initTime = 10

    if args.intervalTime:
        intervalTime = args.intervalTime
    else:
        intervalTime = 0.5
    
    take_picture(args.instruction, initTime, intervalTime, args.dstPath)
    split_image(args.dstPath, args.openingDirection)
    trim_img = trim(args.dstPath)
    shutil.make_archive(args.dstPath+"/complete", 'zip', args.dstPath + "/trim_images")

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

def countdown(t):
    while t:
        mins, secs = divmod(int(t), 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1


def take_picture(direction, init_time, interval_time, path):
    """画面が変化しなくなるまでスクリーンショットを撮る"""
    if direction == "NoneSendKey":
        sendFlag = False
    else:
        sendFlag = True

    shell = win32com.client.Dispatch("WScript.Shell")
    countdown(init_time)
    print("start to shot screen")
    img = ImageGrab.grab()

    spread_path = path + "/spread_image/"
    os.mkdir(spread_path)
    img.save(spread_path + "1.png")
    print("1.png")

    i = 2
    while(1):
        if sendFlag == True:
            shell.SendKeys(direction)
        time.sleep(interval_time)
        img = ImageGrab.grab()
        img.save(spread_path + str(i)+".png")
        print(str(i) + ".png")


        # 一つ前のスクリーンショットと同じ画像なら終了する
        if md5(spread_path + str(i) + ".png") == md5(spread_path + str(i-1) + ".png"):
            break
        i += 1 
    print("To capture screen is complete")

def split_image(path, direction = "RIGHT"):
    """画像を横に２分割する"""
    print("start to split images")
    spread_path = path + "/spread_image/"
    files = os.listdir(spread_path)
    split_path = path + "/split_image/"
    os.mkdir(split_path)
    # ファイルの長さを考慮に入れて数値順にファイルをソートする
    sorted_files = sorted(files, key=lambda x: (len(x), x))
    for file in sorted_files:
        print(file)
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
    print("start to trim images")
    split_path = path + "/split_image/"
    files = os.listdir(split_path)
    trim_path = path + "/trim_image/"
    os.mkdir(trim_path)
    # ファイルの長さを考慮に入れて数値順にファイルをソート
    sorted_files = sorted(files, key=lambda x: (len(x), x))
    for file in sorted_files:
        print(file)
        img = Image.open(split_path + file)
        bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
        diff = ImageChops.difference(img, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            img.crop(bbox).save(trim_path + file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script is to automate screen shots")
    parser.add_argument("dst_path", help="出力するファイルのパスを指定する。")
    parser.add_argument("instruction", help="キーボードの命令をwin32API(SendKey)で指定する。←なら'{LEFT}'を指定する")
    parser.add_argument("opening_direction", help="見開き方向を指定する。右開きなら'RIGHT'を指定する")
    parser.add_argument("init_time", nargs='?',
                        help="プログラムが最初に実行されるまでの時間を指定する(秒)", type=float)
    parser.add_argument("interval_time", nargs='?',
                        help="命令を送る間隔を指定する(秒)", type=float)
    parser.add_argument("--zip",
                        help="最終的な出力ファイルを圧縮して出力する",
                        action="store_true",)
    parser.add_argument("--trim",
                        help="画像の分割とトリミングを行う",
                        action="store_true",)
    
    args = parser.parse_args()

    if args.init_time:
        init_time = args.init_time
    else:
        init_time = 10

    if args.interval_time:
        interval_time = args.interval_time
    else:
        interval_time = 0.5
    
    take_picture(args.instruction, init_time, interval_time, args.dst_path)
    # ファイルの加工
    if args.trim:
        split_image(args.dst_path, args.opening_direction)
        trim_img = trim(args.dst_path)
    # zipで圧縮
    if args.zip and args.trim:
        shutil.make_archive(args.dst_path+"/trim_complete", 'zip', args.dst_path + "/trim_image")
    elif args.zip and not args.trim:
        shutil.make_archive(args.dst_path+"/spread_comlete", 'zip', args.dst_path + "/spread_image")

    print("processing is complete")



# 用来生成训练数据
# 在train_data文件夹会生成以数字顺序命名的图片
# time.npz文件用数组方式保存了每个图片对应的应该去按压的时间（毫秒）
# 可以使用两个手指同时按两个手机获取跳跃时间，其中一个手机写个app监听按压屏幕时间


import numpy as np
from PIL import Image
import time as time
import random
import os

def random_press_position(press_time):
    y_position = random.randint(160, 1000)
    x_position = random.randint(500,600)
    press_position = 'adb shell input swipe '+ str(x_position) +' '+str(y_position)+' '+str(x_position)+' '+str(y_position)+' '+str(press_time)
    os.system(press_position)
#    print(press_position)
def get_screenshot(num):
    os.system('adb shell screencap -p /sdcard/jump_temp.png')
    os.system('adb pull /sdcard/jump_temp.png .')
    im = Image.open(r"./jump_temp.png")
    w, h = im.size
    # 将图片压缩，并截取中间部分，截取后为100*100
    im = im.resize((108, 192), Image.ANTIALIAS)
    region = (4, 65, 104, 165)
    im = im.crop(region)
    # 转换为jpg
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bg.paste(im, im)
    file_name = str(num) + ".jpg"
    bg.save(r"./train_data/" + file_name)


#touch_time_arr = []
# count = 0
npzfile = './train_data/time.npz'
#if os.path.isfile(npzfile):
#    pass
#     os.remove(npzfile)
if  (not(os.path.exists(npzfile))):
    touch_time_arr = []
    npr = np.array(touch_time_arr)
    np.savez("./train_data/time", abc=npr)   
 
touch_time_arr = np.load("./train_data/time.npz")["abc"].tolist()
# count 当前到第几张图片
count = len(touch_time_arr)
print("list_size : " + str(count))
print("list_context : " )
print(touch_time_arr)
def  deletefile(filecount):
    file_name = str(filecount) + ".jpg"
    picfile =("./train_data/" + file_name)
    if os.path.exists(picfile):
        os.remove(picfile)

# 当输入为-1，重新生成图片；输入-2结束并保存; 输入-3重新开始 
RESHOT = -1
FINISH = -2
RESTART = -3

while True:
    #打印初始
    print("shoting.....")
    get_screenshot(count)
    
    # 进行按压屏幕并输入时间
    input_press_time = input("pic"+str(count) + " input touch time(ms): ")
    if len(input_press_time)==0:
        deletefile(count)
        touchtime=RESHOT
    else:
        touchtime = int(input_press_time)
    #print('touchtime: '+str(touchtime))
    # 图片已生成，开始输入时间
    #input_time = input(str(count) + " input touch time(ms): ")
    #touchtime = int(input_time)
     
    # 如果输入-1，则重新生成图片
    if touchtime == RESHOT:
        continue

    # 如果输入-2，则保存并退出，此时多截了一张图，可以手动把最后一张删掉
    elif touchtime == FINISH:
        deletefile(count)
        deletefile(count-1)
        count = count-1
        cnum = touch_time_arr.pop(count)
        print(cnum)
        npr = np.array(touch_time_arr)
        np.savez("./train_data/time", abc=npr)
        break
    # 如果输入-3，重新开始 因为在之前已经将数字加入到数组中了，已经开始下一轮了，所以要删除最后一个  
    elif touchtime == RESTART:
        deletefile(count)
        deletefile(count-1)   
        #npr = np.array(touch_time_arr)
        #np.savez("./train_data/time", abc=npr)
        touch_time_arr.pop(count)
        touch_time_arr.pop(count-1)
        count=count-1
        continue
    # 输入的是需要按压时间，保存到arr数组
    else:
        touchtime = touchtime / 1000
        touch_time_arr.append(touchtime)
    random_press_position(input_press_time)
    time.sleep(touchtime / 1000 + 2)
    count = count + 1
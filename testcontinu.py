def random_press_position(press_time):
    print(press_time)
def get_screenshot(num):
    print(num)
RESHOT = -1
FINISH = -2
RESTART = -3
count = 0
touch_time_arr = []
try:
    while True:
        #打印初始
        print("shoting.....")
        get_screenshot(count)
        
        # 进行按压屏幕并输入时间
        input_press_time = input("pic"+str(count) + " input touch time(ms): ")
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
            print("break")
            break
        # 如果输入-3，重新开始
        elif touchtime == RESTART:
            touch_time_arr.remove(count)
            print(touch_time_arr)
            continue
            print("continue")
        # 输入的是需要按压时间，保存到arr数组
        else:
            touch_time_arr.append(touchtime)
            print("touchtime "+str(touchtime))
            
            print("else")
        random_press_position(input_press_time)
        count = count + 1
except KeyboardInterrupt:
    pass
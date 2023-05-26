import numpy as np
from cv2 import cv2
import asyncio
import telegram
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
cam = cv2.VideoCapture(0)
rectangle = [[0, 0], [0, 0]]
avg_blue = [40.0, 40.0]
work_state = [False, False]
bang = [False]


def fix_cords():
    if rectangle[1][0] < rectangle[0][0]:
        if rectangle[1][1] < rectangle[0][1]:
            (rectangle[0], rectangle[1]) = (rectangle[1], rectangle[0])
        else:
            (rectangle[0][0], rectangle[1][0]) = (rectangle[1][0], rectangle[0][0])
    if rectangle[1][1] < rectangle[0][1]:
        (rectangle[0][1], rectangle[1][1]) = (rectangle[1][1], rectangle[0][1])


def find_mean(area):
    return np.average(area[:, :, 0])


def draw_rectangle(image, cords, color, cutout):
    orig = cutout[cords[0][1] + 10:cords[1][1] - 10, cords[0][0] + 10:cords[1][0] - 10]
    cv2.imshow('Cutout', orig)
    print(work_check(avg_blue, work_state, 40, find_mean(orig)))
    image[cords[0][1]:cords[1][1], cords[0][0]:cords[1][0]] = color
    image[cords[0][1] + 10:cords[1][1] - 10, cords[0][0] + 10:cords[1][0] - 10] = orig


def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        rectangle[0] = [x, y]

    if event == cv2.EVENT_RBUTTONDOWN:
        rectangle[1] = [x, y]


def work_check(avg_arr, state_arr, avg_diff, new_avg):
    # FINISH THIS
    print(new_avg)
    print(avg_arr[1] - avg_arr[0], avg_diff)
    print(state_arr)
    (avg_arr[0], avg_arr[1]) = (avg_arr[1], new_avg)
    if avg_arr[1] - avg_arr[0] > avg_diff:  # IF IT STARTS WORKING
        (state_arr[0], state_arr[1]) = (state_arr[1], True)
    elif avg_arr[1] - avg_arr[0] < -avg_diff:  # IF IT STOPS WORKING
        (state_arr[0], state_arr[1]) = (state_arr[1], False)
    else:
        if state_arr[1]:
            state_arr[0] = True
        else:
            state_arr[0] = False

    if state_arr == [True, False]:
        bang[0] = True
        return True
    else:
        bang[0] = False
        return False


async def main():
    bot = telegram.Bot(TOKEN)
    async with bot:
        await bot.send_message(chat_id=CHAT_ID, text="started working")
        while True:
            ret, frame = cam.read()
            temp = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            fix_cords()
            draw_rectangle(frame, rectangle, (68, 54, 189), temp)
            cv2.imshow('Input', frame)
            cv2.setMouseCallback('Input', click_event)
            if bang[0]:
                await bot.send_document(chat_id=CHAT_ID, document='wawa.gif', caption="wawa")

            c = cv2.waitKey(1)
            if c == 27:
                break
        cam.release()
        cv2.destroyAllWindows()

        await bot.send_message(chat_id=CHAT_ID, text="bb")


if __name__ == '__main__':
    asyncio.run(main())

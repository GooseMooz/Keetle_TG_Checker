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


def fix_cords():
    if rectangle[1][0] < rectangle[0][0]:
        if rectangle[1][1] < rectangle[0][1]:
            (rectangle[0], rectangle[1]) = (rectangle[1], rectangle[0])
        else:
            (rectangle[0][0], rectangle[1][0]) = (rectangle[1][0], rectangle[0][0])
    if rectangle[1][1] < rectangle[0][1]:
        (rectangle[0][1], rectangle[1][1]) = (rectangle[1][1], rectangle[0][1])


def find_mean(area):
    pass


def draw_rectangle(image, cords, color, cutout):
    orig = cutout[cords[0][1] + 10:cords[1][1] - 10, cords[0][0] + 10:cords[1][0] - 10]
    cv2.imshow('Cutout', orig)
    image[cords[0][1]:cords[1][1], cords[0][0]:cords[1][0]] = color
    image[cords[0][1] + 10:cords[1][1] - 10, cords[0][0] + 10:cords[1][0] - 10] = orig


def click_event(event, x, y, flags, params):
    # FIX THIS
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ' ', y)
        rectangle[0] = [x, y]

    if event == cv2.EVENT_RBUTTONDOWN:
        print(x, ' ', y)
        rectangle[1] = [x, y]


while True:
    ret, frame = cam.read()
    temp = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    print(frame[10, 10])
    fix_cords()
    cv2.imshow('Input', frame)
    cv2.setMouseCallback('Input', click_event)

    c = cv2.waitKey(1)
    if c == 27:
        break

cam.release()
cv2.destroyAllWindows()

# async def main():
#     bot = telegram.Bot(TOKEN)
#     async with bot:
#         await bot.send_message(text="wawa", chat_id=CHAT_ID)
#         await bot.send_document(chat_id=CHAT_ID, document='wawa.gif')
#
#
# if __name__ == '__main__':
#     asyncio.run(main())

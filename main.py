from cv2 import cv2
import asyncio
import telegram
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
img = cv2.imread('dog.png', 0)
print(cv2.__version__)
rows, cols = img.shape

cv2.imshow('dog', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


async def main():
    bot = telegram.Bot(TOKEN)
    async with bot:
        await bot.send_message(text="wawa", chat_id=CHAT_ID)
        await bot.send_document(chat_id=CHAT_ID, document='wawa.gif')


if __name__ == '__main__':
    asyncio.run(main())

from cv2 import cv2
import asyncio
import telegram

token = ""
img = cv2.imread('dog.png', 0)
rows, cols, _ = img.shape


async def main():
    bot = telegram.Bot(token)
    print(cv2.__version__)

    cv2.imshow('dog', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    async with bot:
        print(await bot.get_me())


if __name__ == '__main__':
    asyncio.run(main())

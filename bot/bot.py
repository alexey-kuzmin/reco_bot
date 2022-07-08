from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# Для чтения токена из среды окружения и удаления временных файлов
from os import getenv, path, remove
from time import sleep


bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot)


def on_startup():
    print('Вышел в онлайн')


def del_tmp_file(save_path: str):
    if path.isfile(save_path):
        remove(save_path)
    else:
        print("File doesn't exists!")


# для теста
@dp.message_handler(commands=['start'])
async def test(message: types.Message):
    await message.answer('Шли мне фото, распознаю')


@dp.message_handler(content_types=["photo"])
async def test(message: types.Message):
    save_path = 'tmp\\' + str(message.photo[-1].file_unique_id) + '.jpg'
    await message.photo[-1].download(destination=save_path)

    # ТУТ ОБРАБОТКА
    sleep(10)

    await message.answer_photo()
    # УДАЛЯЕМ ВРЕМЕННЫЙ
    del_tmp_file(save_path)


@dp.message_handler(content_types=['document'])
async def photo_handler(message: types.Message):
    if message.document.mime_base == 'image':
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_extension = message.document.file_name.split('.')[-1]
        save_path = '{}{}.{}'.format('tmp\\', str(message.document.file_unique_id), file_extension)
        await bot.download_file(file_path, save_path)

        # ТУТ ОТПРАВЛЯЕМ НА ОБРАБОТКУ
        sleep(10)

        # УДАЛЯЕМ ВРЕМЕННЫЙ ФАЙЛ
        del_tmp_file(save_path)
    else:
        await message.answer('Это же не картинка!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup())


import shutil, threading
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os; os.system('cls')
from config import *
from factories.replies import * 
from handlers import *
from db_conn import *
from builder import *
from searchHistory_observer import *

myBot = Bot(Token)
dp = Dispatcher(myBot)

conn = ConnectDB().connect()
cursor = conn.cursor()
cnt = Carousel()

#for searchHistory
historyObserver = searchObserver()

@dp.message_handler(commands = ['start'])
async def startUp(message: types.Message):
    global currUser
    currUser = message.from_user.id
    await ReplyWelcome().reply(message)

@dp.message_handler(content_types = ['text'])
async def handleText(message: types.Message):

    if message.text == '💰 Buying':
        global isCustomer, isSeller
        isCustomer = True; isSeller = False
        print('isCustomer =',isCustomer)
        await Main4Customer().reply(message)

    elif message.text == '📈 Selling':
        isSeller = True; isCustomer = False
        print('isSeller =', isSeller)
        await Reply2Seller().reply(message, cursor, conn)

    elif message.text == '🔎 Start searching':
        if isCustomer:
            await MainCategory().reply(message)
        elif isSeller: pass

    elif message.text == '🧾 See promoted adverts':
        if isCustomer:
            global randStrategy
            randStrategy = randint(1,3)
            await GetFeatured().reply(carouselCnt = 0, message = message, cursor = cursor, obj_arg = historyObserver, uuId = currUser, sN = randStrategy)
        elif isSeller: pass

    elif message.text == '➕ Add new advert':
        if isSeller:
            await Main4Seller().reply(message)
        elif isCustomer: pass

    elif message.text == 'eDevices':
        if isCustomer: 
            await EDeviceMenu4Customer().reply(message)
        elif isSeller: 
            await EDeviceMenu4Seller().reply(message)
    
    elif message.text == 'Cars':
        if isCustomer: 
            await CarsMenu4Customer().reply(message)
        elif isSeller: 
            await CarsMenu4Seller().reply(message)

    elif message.text == '🔙 E.Back':
        if isCustomer: 
            await Main4Customer().reply(message)
        elif isSeller: 
            await EDeviceMenu4Seller().reply(message)

    elif message.text == '🔙 Cars.Back':
        if isCustomer: 
            await CarsMenu4Customer().reply(message)
        elif isSeller: 
            await CarsMenu4Seller().reply(message)

    elif message.text == '🖥️ PCs':
        if isCustomer:
            global cat, subCat
            cat = 'eDevices'; subCat = 'PC' 
            historyObserver.react(cursor, conn, int(message.from_user.id), cat, subCat)
            await GiveResult().reply(carouselCnt = 0, message = message, cursor = cursor, cat = cat, subcat = subCat)    #carousel!
        elif isSeller:
            cat = 'eDevices'; subCat = 'PC'
            await AddNewAdvert().reply(message)
    
    elif message.text == '💻 Laptops':
        if isCustomer:
            cat = 'eDevices'; subCat = 'Laptop' 
            historyObserver.react(cursor, conn, int(message.from_user.id), cat, subCat)
            await GiveResult().reply(carouselCnt = 0, message = message, cursor = cursor, cat = cat, subcat = subCat)    #carousel!
        elif isSeller:
            cat = 'eDevices'; subCat = 'Laptop'
            await AddNewAdvert().reply(message)

    elif message.text == '📱 Smartphones':
        if isCustomer:
            cat = 'eDevices'; subCat = 'Smartphone'
            historyObserver.react(cursor, conn, int(message.from_user.id), cat, subCat) 
            await GiveResult().reply(carouselCnt = 0, message = message, cursor = cursor, cat = cat, subcat = subCat)    #carousel!
        elif isSeller:
            cat = 'eDevices'; subCat = 'Smartphone'
            await AddNewAdvert().reply(message)

    elif message.text == '👜 Accessories':
        if isCustomer:
            cat = 'eDevices'; subCat = 'Accessory' 
            historyObserver.react(cursor, conn, int(message.from_user.id), cat, subCat)
            await GiveResult().reply(carouselCnt = 0, message = message, cursor = cursor, cat = cat, subcat = subCat)    #carousel!
        elif isSeller:
            cat = 'eDevices'; subCat = 'Accessory'
            await AddNewAdvert().reply(message)

    elif message.text == '®️ Register':
        await RegisterSeller().reply(message)
        @dp.message_handler(content_types = ['contact'])
        async def getContact(message: types.Message):
            await RegisterSeller().regData(message, cursor, conn)

    elif message.text.startswith('N:'):
        if isSeller:
            global itemName
            itemName = message.text.split(':')[1]
            print(itemName)
        elif isCustomer: pass

    elif message.text.startswith('P:'):
        if isSeller:
            global itemPrice
            itemPrice = message.text.split(':')[1]
            print(itemPrice)
        elif isCustomer: pass

    elif message.text.startswith('D:'):
        if isSeller:
            global itemDescr
            itemDescr = message.text.split(':')[1]
            print(itemDescr)
        elif isCustomer: pass

    elif message.text == '🖼️ Add image':
        if isSeller:
            global itemImg
            await AddImage().reply(message)
            @dp.message_handler(content_types = ['photo'])
            async def add_photo(message):
                photo = message.photo.pop()
                file = await photo.download()
                global tmpPath
                tmpPath = str(file).split(' ')[1].split("'")[1]
                print(tmpPath)
                global itemImg
                itemImg = img2bin(tmpPath)
        elif isCustomer: pass

    elif message.text == '⌛ Upload to the store':
        if isSeller:
            tempAdv = ADV_Build().getName(itemName).getPrice(itemPrice).getCategory(cat).getSubCategory(subCat).getSeller(message.from_user.username).getSellerPhone(cursor, conn, currUser).getDescription(itemDescr).getPhoto(itemImg).build().push2DB(cursor, conn)
            os.remove(tmpPath)
            shutil.rmtree('./photos')
            print('All temporary files has been removed!')
        elif isCustomer: pass

    elif message.text == '🧾 See my adverts':
        if isSeller:
            global sUserNameName
            sUserNameName = message.from_user.username
            await GiveResult2Seller().reply(carouselCnt = 0, message = message, cursor = cursor, username = sUserNameName)
        elif isCustomer: pass

    else:
        await message.answer('Sorry!')

@dp.callback_query_handler(lambda c: c.data)
async def itemMenu(callback_query: types.CallbackQuery):
    call = callback_query.data
    
    if call == 'forward':
        try:
            count = cnt.up()
            await GiveResult().reply(myBot, call = call, cb = callback_query, carouselCnt = count, cursor = cursor, cat = cat, subcat = subCat)
        except IndexError: await callback_query.message.answer('The list has finished! Try another direction 😉')
    if call == 'back':
        count = cnt.down()
        if count <= 0:
            await callback_query.message.answer('The list has finished! Try another direction 😉')
        elif count == 0:
            await GiveResult().reply(myBot, call = call, cb = callback_query, carouselCnt = count, cursor = cursor, cat = cat, subcat = subCat)
    if call == 'get_seller':
        count = cnt.current()
        await GiveResult().reply(myBot, call = call, cb = callback_query, cursor = cursor, cat = cat, subcat = subCat, carouselCnt = count)
    if call == 'f':
        try:
            count = cnt.up()
            await GiveResult2Seller().reply(myBot, call = call, cb = callback_query, cursor = cursor, carouselCnt = count, username = sUserNameName)
        except IndexError: await callback_query.message.answer('The list has finished! Try another direction 😉')
    if call == 'b':
        count = cnt.down()
        if count <= 0:
            await callback_query.message.answer('The list has finished! Try another direction 😉')
        elif count == 0:
            await GiveResult2Seller().reply(myBot, call = call, cb = callback_query, cursor = cursor, carouselCnt = count, username = sUserNameName)
    if call == 'r':
        count = cnt.current()
        await GiveResult2Seller().reply(myBot, call = call, cb = callback_query, cursor = cursor, carouselCnt = count, username = sUserNameName, connect = conn)
    if call == 'dp':
        count = cnt.current()
        await GiveResult2Seller().reply(myBot, call = call, cb = callback_query, cursor = cursor, carouselCnt = count, username = sUserNameName, connect = conn)
    if call == 'dq':
        count = cnt.current()
        await GiveResult2Seller().reply(myBot, call = call, cb = callback_query, cursor = cursor, carouselCnt = count, username = sUserNameName, connect = conn)
    if call == 'Fforward':
        try:
            count = cnt.up()
            await GetFeatured().reply(myBot, call = call, cb = callback_query, carouselCnt = count, cursor = cursor, sN = randStrategy, uuId = currUser)
        except IndexError: await callback_query.message.answer('The list has finished! Try another direction 😉')
    if call == 'Fback':
        count = cnt.down()
        if count <= 0:
            await callback_query.message.answer('The list has finished! Try another direction 😉')
        elif count == 0:
            await GetFeatured().reply(myBot, call = call, cb = callback_query, carouselCnt = count, cursor = cursor, sN = randStrategy, uuId = currUser)
    if call == 'Fget_seller':
        count = cnt.current()
        await GetFeatured().reply(myBot, call = call, cb = callback_query, cursor = cursor, carouselCnt = count, sN = randStrategy, uuId = currUser)

if __name__ == "__main__":
    th = threading.Thread(target = executor.start_polling(dp), daemon=True)
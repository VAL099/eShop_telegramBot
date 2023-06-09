
from aiogram import Bot, types
from abc import ABC, abstractmethod

from factories.menus import *
from handlers import *
from builder import *
from proxyDB import *
from promoterDecorator import *
from featuredStrategy import *
from searchHistory_observer import *

class IReply(ABC):

    @abstractmethod
    async def reply(self):
        pass

class ReplyWelcome(IReply):
    async def reply(self, message):
        menu = WelcomeMenu().createMenu()    #creating reply menu by -> Factory Method <-
        msg = await message.answer('Hi. You are here for ...', reply_markup = menu)
        return msg

class Main4Customer(IReply):
    async def reply(self, message):
        user = message.from_user.first_name
        greeting = 'Hi {}! \nWelcome to our platform...'.format(user)
        menu = MainMenu4Customer().createMenu()
        msg1 = await message.answer(greeting)
        msg2 = await message.answer('Hi. What do you wanna do?', reply_markup = menu)
        return msg1, msg2

class MainCategory(IReply):
    async def reply(self, message):
        menu = MainCategories().createMenu()
        msg = await message.answer('What are you here for?', reply_markup = menu)
        return msg

class EDeviceMenu4Customer(IReply):
    async def reply(self, message):
        menu = EDevicesTypes().createMenu()
        msg = await message.answer('What exactly do you need?', reply_markup = menu) 
        return msg

class CarsMenu4Customer(IReply):
    async def reply(self, message):
        menu = CarsTypes().createMenu()
        msg = await message.answer('What exactly do you need?', reply_markup = menu) 
        return msg

class EDeviceMenu4Seller(IReply):
    async def reply(self, message):
        menu = EDevicesTypes().createMenu()
        msg = await message.answer('What do you wanna sell?', reply_markup = menu)
        return msg

class CarsMenu4Seller(IReply):
    async def reply(self, message):
        menu = CarsTypes().createMenu()
        msg = await message.answer('What do you wanna sell?', reply_markup = menu)
        return msg

class AddNewAdvert(IReply):
    async def reply(self, message):
        menu = AddImageMenu().createMenu()
        msg = await message.answer('To add a product you should specify its Name, Price(in euros) and Description in a specific form! WARNING! Separate messages! After all press "Add image button". Gook Luck!'
            '\nName → N:<product_name>\nPrice → P:<product_price>\nDescription → D:<product_description>\n', reply_markup = menu)
        return msg

class Main4Seller(IReply):

    async def reply(self, message):
        menu = MainCategories().createMenu()
        msg = await message.answer('What type is your product?', reply_markup = menu)
        return msg

class Reply2Seller(IReply):
    async def reply(self, message, conn, cursor):
        uId = message.from_user.id
        res = cursor.execute('select userId from sellers where userId = ?', (uId,)).fetchall()
        if res != []:
            menu = MainMenu4Seller().createMenu()
            msg = await message.answer('Hi. What do you wanna do?', reply_markup = menu)
            return msg
        elif res == []: 
            user = message.from_user.first_name
            greeting = 'Hi {}! \nWelcome to our platform!\nFor trading here you should first register!\nPlease make sure you have set you Telegram usename in settings. Otherwise,you will not be able to register. Sorry! That is the life =)'.format(user)
            menu = SellerReg().createMenu()
            msg = await message.answer(greeting, reply_markup = menu)
            return msg

class RegisterSeller(IReply):
    async def reply(self, message):
        phoneNBtn = ReqPhone().createMenu()
        msg = await message.answer('Please, give us your contact data!', reply_markup = phoneNBtn)
        return msg

    async def regData(self, message, cursor, conn):
        userId = message.from_user.id
        user_Name = message.from_user.first_name
        userName = message.from_user.username
        num = '+' + message.contact.phone_number
        print(userId, user_Name, userName, num)
        userReg(cursor, conn, userId, user_Name, userName, num)
        print('reg!')
        menu = MainMenu4Seller().createMenu()
        msg = await message.answer('Hi. What do you wanna do?', reply_markup = menu)
        return msg

class AddImage(IReply):
    async def reply(self, message):
        menu = Upload2DB().createMenu()
        msg = await message.answer('Waiting for image...', reply_markup = menu)
        return msg

class SellerMenu(IReply):
    async def reply(self, message):
        menu = ShowSelfADV().createMenu()
        await message.answer('Succesfuly posted!', reply_markup = menu)

class GiveResult(IReply):
    async def reply(self, bot = None, call = None, cb = None, carouselCnt = None, message = None, cat = None, subcat = None, cursor = None):
        #recv data from DB
        #goodsList = handleUserRequest(cursor, cat, subcat) # querying
        proxy = ProxyDB().storeList4Customer(cursor, cat, subcat)
        id, name, price, ___cat, ___subcat, seller, sellerPhone, description, photo, priceLabel, qualityLabel = proxy.goodsList[carouselCnt]

        if call == 'forward':
            await bot.answer_callback_query(cb.id)
            menu = RResult().createMenu()
            dlt = await cb.message.delete()
            msg = await cb.message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}').format(price, description), reply_markup = menu)
            return dlt, msg
        elif call == 'back':
            await bot.answer_callback_query(cb.id)
            menu = RResult().createMenu()
            dlt = await cb.message.delete()
            msg = await cb.message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}').format(price, description), reply_markup = menu)
            return dlt, msg
        elif call == 'get_seller':
        
            act = await bot.send_message(cb.from_user.id, text= 'Telegram: @{}\nContact number: {}'.format(seller, sellerPhone))
            return act
        else:
            menu = RResult().createMenu()
            msg = await message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}').format(price, description), reply_markup = menu)
            return msg

class GiveResult2Seller(IReply):
    async def reply(self, bot = None, call = None, cb = None, carouselCnt = None, message = None, username = None, cursor = None, connect = None):
        #recv data from DB
        proxy = ProxyDB().storeList4Seller(cursor, username) # querying
        #aId, name, price, ___cat, ___subcat, seller, sellerPhone, description, photo, priceLabel, qualityLabel = proxy.goodsList[carouselCnt]
        if proxy.goodsList != []:
            aId, name, price, ___cat, ___subcat, seller, sellerPhone, description, photo, priceLabel, qualityLabel = proxy.goodsList[carouselCnt]
            if call == 'f':
                menu = RResult4Seller().createMenu()
                dlt = await cb.message.delete()
                msg = await cb.message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}\nPriceLabel: ' + str(priceLabel) + '\nQualityLabel: ' + str(qualityLabel)).format(price, description), reply_markup = menu)
                return dlt, msg
            elif call == 'b':
                menu = RResult4Seller().createMenu()
                dlt = await cb.message.delete()
                msg = await cb.message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}\nPriceLabel: ' + str(priceLabel) + '\nQualityLabel: ' + str(qualityLabel)).format(price, description), reply_markup = menu)
                return dlt, msg
            elif call == 'dp':
                menu = RResult4Seller().createMenu()
                PriceDecor(True, aId).decorate(cursor, connect)
                msg1 = await cb.message.answer('Decorated!', reply_markup = menu)
                dlt = await cb.message.delete()
                msg2 = await cb.message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}\nPriceLabel: ' + str(priceLabel) + '\nQualityLabel: ' + str(qualityLabel)).format(price, description), reply_markup = menu)
                return msg1, dlt, msg2
            elif call == 'dq':
                menu = RResult4Seller().createMenu()
                QualityDecor(True, aId).decorate(cursor, connect)
                msg1 = await cb.message.answer('Decorated!', reply_markup = menu)
                dlt = await cb.message.delete()
                msg2 = await cb.message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}\nPriceLabel: ' + str(priceLabel) + '\nQualityLabel: ' + str(qualityLabel)).format(price, description), reply_markup = menu)
                return msg1, dlt, msg2
            elif call == 'r':
                rmADV(cursor, connect, aId)
                menu = RResult4Seller().createMenu()
                dlt = await cb.message.delete()
                msg = await cb.message.answer('Deleted!', reply_markup = menu)
                return dlt, msg
            else:
                menu = RResult4Seller().createMenu()
                msg = await message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}\nPriceLabel: ' + str(priceLabel) + '\nQualityLabel: ' + str(qualityLabel)).format(price, description), reply_markup = menu)
                return msg
        elif proxy.goodsList == []:
            menu = RResult4Seller().createMenu()
            msg = await message.answer('You havent posted anything yet', reply_markup = menu)

class GetFeatured(IReply):
    async def reply(self, bot = None, call = None, cb = None, carouselCnt = None, message = None, cat = None, subcat = None, cursor = None, uuId = None, obj_arg = None, sN = None):
        #recv data from DB
        #goodsList = handleUserRequest(cursor, cat, subcat) # querying
        strateg = sN
        if strateg == 1:
            strategy = Context(PromoteByQualityLabel).select_alg(cursor, None)
            id, name, price, ___cat, ___subcat, seller, sellerPhone, description, photo, priceLabel, qualityLabel = strategy[carouselCnt]

            if call == 'Fforward':
                menu = RResultFeatured().createMenu()
                dlt = await cb.message.delete()
                msg = await cb.message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}').format(price, description), reply_markup = menu)
                return dlt, msg
            elif call == 'Fback':
                menu = RResultFeatured().createMenu()
                dlt = await cb.message.delete()
                msg = await cb.message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}').format(price, description), reply_markup = menu)
                return dlt, msg
            elif call == 'Fget_seller':
                act = await bot.send_message(cb.from_user.id, text= 'Telegram: @{}\nContact number: {}'.format(seller, sellerPhone))
                return act
            else:
                menu = RResultFeatured().createMenu()
                msg = await message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}').format(price, description), reply_markup = menu)
                return msg
            
        elif strateg == 2:
            strategy = Context(PromoteByPriceLabel).select_alg(cursor, None)
            id, name, price, ___cat, ___subcat, seller, sellerPhone, description, photo, priceLabel, qualityLabel = strategy[carouselCnt]

            if call == 'Fforward':
                menu = RResultFeatured().createMenu()
                dlt = await cb.message.delete()
                msg = await cb.message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}').format(price, description), reply_markup = menu)
                return dlt, msg
            elif call == 'Fback':
                menu = RResultFeatured().createMenu()
                dlt = await cb.message.delete()
                msg = await cb.message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}').format(price, description), reply_markup = menu)
                return dlt, msg
            elif call == 'Fget_seller':
                act = await bot.send_message(cb.from_user.id, text= 'Telegram: @{}\nContact number: {}'.format(seller, sellerPhone))
                return act
            else:
                menu = RResultFeatured().createMenu()
                msg = await message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}').format(price, description), reply_markup = menu)
                return msg

        elif strateg == 3:
            strategy = Context(PromoteByHistory).select_alg(cursor, uuId)
            id, name, price, ___cat, ___subcat, seller, sellerPhone, description, photo, priceLabel, qualityLabel = strategy[carouselCnt]

            if call == 'Fforward':
                menu = RResultFeatured().createMenu()
                dlt = await cb.message.delete()
                msg = await cb.message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}').format(price, description), reply_markup = menu)
                return dlt, msg
            elif call == 'Fback':
                menu = RResultFeatured().createMenu()
                dlt = await cb.message.delete()
                msg = await cb.message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}').format(price, description), reply_markup = menu)
                return dlt, msg
            elif call == 'Fget_seller':
                act = await bot.send_message(cb.from_user.id, text= 'Telegram: @{}\nContact number: {}'.format(seller, sellerPhone))
                return act
            else:
                menu = RResultFeatured().createMenu()
                msg = await message.answer_photo(photo, caption =('📛 ' + name + '\n💶 Price:{}\n' + '📝 {}').format(price, description), reply_markup = menu)
                return msg
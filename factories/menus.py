from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from abc import ABC, abstractmethod

class IMenu(ABC):
    
    @abstractmethod
    def createMenu(self): pass

class WelcomeMenu(IMenu):

    def createMenu(self):
        buying = KeyboardButton('💰 Buying')
        selling = KeyboardButton('📈 Selling')
        welcomeMenu = ReplyKeyboardMarkup(resize_keyboard = True, selective = True).row(buying, selling)
        return welcomeMenu

class MainMenu4Customer(IMenu):

    def createMenu(self):
        searching = KeyboardButton('🔎 Start searching')
        featured = KeyboardButton('🧾 See promoted adverts')
        mainMenu = ReplyKeyboardMarkup(resize_keyboard = True, selective = True).row(searching).row(featured)
        return mainMenu

class MainMenu4Seller(IMenu):

    def createMenu(self):
        searching = KeyboardButton('➕ Add new advert')
        featured = KeyboardButton('🧾 See my adverts')
        mainMenu = ReplyKeyboardMarkup(resize_keyboard = True, selective = True).row(searching).row(featured)
        return mainMenu

class MainCategories(IMenu):

    def createMenu(self):
        cat1 = KeyboardButton('eDevices')
        cat2 = KeyboardButton('Cars')
        cat3 = KeyboardButton('...[not available]...')
        menu = ReplyKeyboardMarkup(resize_keyboard = True, selective = True).row(cat1).row(cat2).row(cat3)
        return menu

class EDevicesTypes(IMenu):

    def createMenu(self):
        subcat1 = KeyboardButton('🖥️ PCs')
        subcat2 = KeyboardButton('💻 Laptops')
        subcat3 = KeyboardButton('📱 Smartphones')
        subcat4 = KeyboardButton('👜 Accessories')
        btn5 = KeyboardButton('🔙 E.Back')
        menu = ReplyKeyboardMarkup(resize_keyboard = True, selective = True).row(subcat1, subcat2).row(subcat3, subcat4).row(btn5)
        return menu

class CarsTypes(IMenu):

    def createMenu(self):
        subcat1 = KeyboardButton('🚗 Saloon')
        subcat3 = KeyboardButton('Estate')
        subcat2 = KeyboardButton('🚙 SUV')
        subcat4 = KeyboardButton('Coupe')
        btn5 = KeyboardButton('🔙 Cars.Back')
        menu = ReplyKeyboardMarkup(resize_keyboard = True, selective = True).row(subcat1, subcat2).row(subcat3, subcat4).row(btn5)
        return menu

class RResult(IMenu):

    def createMenu(self):
        btn1 = InlineKeyboardButton('←', callback_data = 'back')
        btn2 = InlineKeyboardButton('→', callback_data = 'forward')
        btn3 = KeyboardButton('🛒 Contact Seller', callback_data = 'get_seller')
        arrowMenu = InlineKeyboardMarkup(resize_keyboard = True).row(btn1, btn2).row(btn3)
        return arrowMenu

class RResultFeatured(IMenu):

    def createMenu(self):
        btn1 = InlineKeyboardButton('←', callback_data = 'Fback')
        btn2 = InlineKeyboardButton('→', callback_data = 'Fforward')
        btn3 = KeyboardButton('🛒 Contact Seller', callback_data = 'Fget_seller')
        arrowMenu = InlineKeyboardMarkup(resize_keyboard = True).row(btn1, btn2).row(btn3)
        return arrowMenu

class RResult4Seller(IMenu):

    def createMenu(self):
        btn1 = InlineKeyboardButton('←', callback_data = 'b')
        btn2 = InlineKeyboardButton('→', callback_data = 'f')
        btn3 = InlineKeyboardButton('Set price label', callback_data = 'dp')
        btn5 = InlineKeyboardButton('Set quality label', callback_data = 'dq')
        btn4 = InlineKeyboardButton('Remove', callback_data = 'r')
        arrowMenu = InlineKeyboardMarkup(resize_keyboard = True).row(btn1, btn2).row(btn3, btn5).row(btn4)
        return arrowMenu

class SellerReg(IMenu):

    def createMenu(self):
        regBtn = KeyboardButton('®️ Register')
        menu = ReplyKeyboardMarkup(resize_keyboard = True, selective = True).row(regBtn)
        return menu

class ReqPhone(IMenu):

    def createMenu(self):
        btn = KeyboardButton('📱 Send phone number', request_contact = True)
        menu = ReplyKeyboardMarkup(resize_keyboard = True, selective = True).row(btn)
        return menu

class AddImageMenu(IMenu):
    
    def createMenu(self):
        btn = KeyboardButton('🖼️ Add image')
        menu = ReplyKeyboardMarkup(resize_keyboard = True, selective = True).row(btn)
        return menu

class Upload2DB(IMenu):

    def createMenu(self):
        btn = KeyboardButton('⌛ Upload to the store')
        menu = ReplyKeyboardMarkup(resize_keyboard = True, selective = True).row(btn)
        return menu

class ShowSelfADV(IMenu):

    def createMenu(self):
        btn = KeyboardButton('📰 My adverts')
        menu = ReplyKeyboardMarkup(resize_keyboard = True, selective = True).row(btn)
        return menu
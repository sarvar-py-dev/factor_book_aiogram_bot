# from aiogram.types import CallbackQuery
# from redis_dict import RedisDict

#
# def korzina(callback: CallbackQuery, soni, tavar_narxi):
#     # product = {}
#     # product['soni'] = soni
#     # product['tavar_narxi'] = tavar_narxi
#     data[str(callback.from_user.id)] = f'''🛒 Savat
#
# 1. IKAR to'plami
# {soni} x 259,000 ={tavar_narxi * soni} so'm
#
# Jami: {tavar_narxi * soni} so'm'''
#     return data[str(callback.from_user.id)]

# ikb = InlineKeyboardBuilder()
#     ikb.row(InlineKeyboardButton(text='⚡️ IKAR', callback_data='ikar'),
#             InlineKeyboardButton(text='📚 Factor books kitoblari', callback_data='kitoblar'))
#     ikb.row(InlineKeyboardButton(text='💸 Biznes kitoblar', callback_data='kitoblar'),
#             InlineKeyboardButton(text='☪️ Diniy kitoblar', callback_data='kitoblar'))
#     ikb.row(InlineKeyboardButton(text='📚 Boshqa kitoblar', callback_data='kitoblar'),
#             InlineKeyboardButton(text='🔮 Psihologik kitoblar', callback_data='kitoblar'))
#     ikb.row(InlineKeyboardButton(text='👨‍👩‍👧‍👦 Tarbiyaviy-oilaviy kitoblar', callback_data='kitoblar'),
#             InlineKeyboardButton(text='🇹🇷 Turk badiy-mar\'ifiy kitoblar', callback_data='kitoblar'))
#     ikb.row(InlineKeyboardButton(text='📚 Badiy Ramanlar', callback_data='kitoblar'),
#             InlineKeyboardButton(text='📚 Qissa va Romanlar', callback_data='kitoblar'))
#     ikb.row(InlineKeyboardButton(text='📚 Badiy kitoblar va Qissalar', callback_data='kitoblar'),
#             InlineKeyboardButton(text='🔍 Qidirish', callback_data='inline_mode'))

# database = {}
#
# database['categories'] = {
#     'category_id': 'title'
# }
#
# database['products'] = {
#     'products_id': {
#         'name': 'product_name',
#         'text': """🔹 Nomi: IKAR to'plami
# "Ikar" to'plami — Usmon Azim: "Bir parcha osmon";
#  Erkin A'zam: "Anoyining jaydari olmasi";
#  Murod Muhammad Do'st: "Galatepaga qaytish";
#  Xurshid Davron: "Samarqand xayoli" kitoblari
# Janri; Adabiy-badiiy,ma'rifiy
# Muqova; Yumshoq
# Kitob haqida;
# 💸 Narxi: 259,000 so'm""",
#         'image': 'image_id',
#         'price': 259_000,
#         'category_id': 4651321
#     },
# }
#
# print([item for item in database['categories'].items() if item[1] == 'title'])
#
# adsaf = {'categories': {
#     '6f613e68-5774-42f2-aa8d-80aaafc0313f': '⚡️IKAR',
#     'bbbb5b97-0d21-48a1-b2a8-9fc280203f02': '📚 Factor books kitoblari',
#     'b15c9887-36e3-4738-b1e1-fa0d412f394d': 'Biznes kitoblar',
#     'e6f5306d-4395-4543-b53f-7daa30b4034c': 'Diniy kitoblar',
#     '02f8ef29-4a87-46ca-a130-1c0541715e9b': '📚 Boshqa kitoblar',
#     '3212c27c-370e-4e7a-afdb-bb26682e39f5': 'Psixologik kitoblar',
#     '6f4143c4-5173-4f90-8716-cf73c2826d53': 'Tarbiyaviy-oilaviy kitoblar',
#     '96f2bc9c-7381-4a97-ac08-ffb37a346da1': "Turk badiiy-ma'rifiy kitoblar",
#     'b82fb26d-ad98-4e2b-ada7-5be62c1ca429': 'Badiiy Romanlar',
#     'b2df56a8-5290-43a7-b406-e44a541b52f4': 'Qissa va Romanlar',
#     '0c5a0bcf-f5bf-41ba-b4ce-1cf7aba3b30d': 'Badiiy kitoblar va qissalar'}, 'products': []
# }


# basket = {
#     'user_id': {
#         'product_id': {
#             'products_name': '',
#             'quantity': '4',
#             'price': ''
#         }
#     }
# }
#
# basket['user_id']['product_id']['quantity'] = str(int(basket['user_id']['product_id']['quantity']) + 1)
# print(basket)


f = """🔹 Nomi: ,,Seni sevaman dema, his ettir''
Muallifi; Mirach Chag'ri Oqtosh
Janri; Turkiy, badiiy-ma'rifiy
Tarjimon; Zarona Tojiyeva
Bet; 216
Muqova; Yumshoq
Kitob haqida;
💸 Narxi: 34,000 so'm"""

print(f[f.index('Muallifi'): f.index('Narxi') - 2])
# print(f)

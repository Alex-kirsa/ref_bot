from dispather import bot


async def send_mailing(users: list, data: list):
    count = 0
    for user in users:
        try:
            await bot.send_photo(user[0], photo=data[0], caption=data[1])
            count += 1
        except Exception :
            pass
    return count
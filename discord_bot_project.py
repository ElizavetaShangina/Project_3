import asyncio
import discord
from discord.ext import commands
import logging
import sqlite3

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class USER(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_in = False
        self.login = ''
        self.level = -1

    @commands.command(name='start')
    async def start(self, ctx):
        await ctx.send('Если вы уже зарегистрированы, напишите боту "/sign in Ваш логин Ваш пароль". \n'
                       'Если вы новый пользователь, напишите "/sign up Ваш логин Ваш пароль"')

    @commands.command(name='sign')
    async def sign(self, ctx, operation, login, password):
        con = sqlite3.connect('Discord_maze.db')
        cur = con.cursor()
        if operation == 'in':
            result = cur.execute(f"""SELECT * FROM Users""").fetchall()
            for i in result:
                if i[0] == login:
                    if i[1] == password:
                        self.level = int(cur.execute(f"""SELECT Level FROM Levels WHERE Login = '{login}'""").fetchall()[0][0])
                        self.log_in = True
                        self.login = login
                        await ctx.send('Поздравляем, вы успешно авторизовались. \n'
                                       'Для выбора уровня сложности введите "/level номер уровня(1, 2 или 3)". \n'
                                       'Для начала прохождения введите "/maze"')
                    else:
                        await ctx.send('Ваш пароль неверен. Попробуйте еще раз или создайте новую учетную запись.')
                    return
            if not self.log_in:
                await ctx.send('Похоже, у нас нет данных об учетной записи с таким логином. '
                               'Попробуйте еще раз или создайте новую учетную запись.')
                return
        elif operation == 'up':
            cur.execute(f"""INSERT INTO Users (Login, Password) VALUES ('{login}', '{password}')""").fetchall()
            con.commit()
            con.close()
            self.log_in = True
            self.login = login
            await ctx.send(f'Вы успешно зарегистрировались. Ваш логин: {login} \n'
                           f'Для выбора уровня сложности введите "/level номер уровня(1, 2 или 3)".')
            return
        else:
            await ctx.send('Похоже, произошла ошибка. Проверьте правильность ввода операции')
            return
        return

    @commands.command(name='level')
    async def set_level(self, ctx, level):
        if int(level) not in [1, 2, 3]:
            await ctx.send(f'Необходимо выбрать один из трех уровней сложности. \n'
                           f'Для этого введите "/level 1", "/level 2" или "/level 3"')
            return
        if self.log_in:
            con = sqlite3.connect('Discord_maze.db')
            cur = con.cursor()
            result = cur.execute(f"""SELECT * FROM Levels""").fetchall()
            set_level = False
            self.level = int(level[0])
            for i in result:
                if i[0] == self.login:
                    set_level = True
                    cur.execute(f"UPDATE Levels SET Level = {self.level} WHERE Login = '{self.login}'")
                    con.commit()
            if not set_level:
                cur.execute(f"""INSERT INTO Levels (Login, Level) VALUES ('{self.login}', {level})""").fetchall()
                con.commit()
                con.close()
            await ctx.send(f'Уровень сложности лабиринта: {level}. Для начала прохождения введите "/maze"')
        else:
            await ctx.send('Для выбора уровня сложности необходимо авторизоваться.')
        return

    @commands.command(name='maze')
    async def maze(self, ctx):
        if self.login:
            if self.level in [1, 2, 3]:
                await ctx.send('Добро пожаловать в игру.')
            else:
                await ctx.send('Для начала прохождения необходимо выбрать уровень сложности.')
        else:
            await ctx.send('Для начала прохождения необходимо авторизоваться.')
        return


bot = commands.Bot(command_prefix='/', intents=intents)
TOKEN = "BOT_TOKEN"


async def main():
    await bot.add_cog(USER(bot))
    await bot.start(TOKEN)


asyncio.run(main())

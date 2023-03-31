import sqlite3
import disnake
from disnake.ext import commands
from typing import Optional

level = -1

class Dropdown(disnake.ui.StringSelect):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Уровень 1", description="Для новичков и неуверенных в себе личностей", emoji="🟩"),
            disnake.SelectOption(label="Уровень 2", description="Для продвинутых игроков", emoji="🟨"),
            disnake.SelectOption( label="Уровень 3", description="Для тех, у кого слишком много времени и нервов", emoji="🟥"),]
        super().__init__(
            placeholder="Уровень сложности", min_values=1,  max_values=1, options=options,)

    async def callback(self, inter: disnake.MessageInteraction):
        global level
        level = int(self.values[0].split()[1])
        await inter.response.send_message(f'Ваш уровень: {self.values[0]}. Для начала прохождения введите "/maze"')

class DropdownView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

class ThreeDirectionButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=100.0)
        self.value: Optional[str] = ''

    @disnake.ui.button(label="Направо", style=disnake.ButtonStyle.green)
    async def confirm(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.value = 'направо'
        self.stop()

    @disnake.ui.button(label="Прямо", style=disnake.ButtonStyle.danger)
    async def cancel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.value = 'прямо'
        self.stop()

    @disnake.ui.button(label="Налево", style=disnake.ButtonStyle.blurple)
    async def cancel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.value = 'налево'
        self.stop()

class TwoDirectionButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=100.0)
        self.value: Optional[str] = ''

    @disnake.ui.button(label="Направо", style=disnake.ButtonStyle.green)
    async def confirm(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.value = 'направо'
        self.stop()

    @disnake.ui.button(label="Налево", style=disnake.ButtonStyle.blurple)
    async def cancel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.value = 'налево'
        self.stop()


class ThreeDoorButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=100.0)
        self.value: Optional[int] = 0

    @disnake.ui.button(label='1', style=disnake.ButtonStyle.green)
    async def one(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        self.value = 1
        self.stop()

    @disnake.ui.button(label='2', style=disnake.ButtonStyle.danger)
    async def two(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        self.value = 2
        self.stop()

    @disnake.ui.button(label='3', style=disnake.ButtonStyle.blurple)
    async def three(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        self.value = 3
        self.stop()

class TwoDoorButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=100.0)
        self.value: Optional[int] = 0

    @disnake.ui.button(label='1', style=disnake.ButtonStyle.green)
    async def one(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        self.value = 1
        self.stop()

    @disnake.ui.button(label='2', style=disnake.ButtonStyle.danger)
    async def two(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        self.value = 2
        self.stop()


class USER(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_in = False
        self.login = ''
        self.death_reason = ''
        self.first_time = True
        self.stone = False

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
                        self.log_in = True
                        self.login = login
                        await ctx.send(f'Вы успешно авторизовались.')
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
            await ctx.send(f'Вы успешно зарегистрировались. Ваш логин: {self.login}')
        else:
            await ctx.send('Похоже, произошла ошибка. Проверьте правильность ввода операции')
            return
        if self.log_in:
            view = DropdownView()
            """async def dropdown_callback(interaction):
                print(dropdown.values)
                await ctx.send(f'Уровень: {dropdown.values}. Для того чтобы начать введите "/maze"')



            dropdown = Select(placeholder='Уровень сложности', options=[option1, option2, option3], min_values=1, max_values=1)
            dropdown.callback = dropdown_callback
            view = View(timeout=10000)
            view.add_item(dropdown)"""
            await ctx.send('Прежде чем начать, выберите уровень сложности', view=view)


    @commands.command(name='maze')
    async def maze(self, ctx):
        if self.login:
            global level
            self.level = level
            if self.level in [1, 2, 3]:
                if self.first_time:
                    await ctx.send('Добро пожаловать в игру.')
                if self.level == 1:
                    if self.first_time:
                        await ctx.send(
                            'Вы очнулись в помещении, из которого есть 2 выхода. '
                            'Подойдя к одной из дерей и подергав ручку вы убеждаетесь, что она заперта. '
                            'Вы открываете вторую дверь и видите лестницу. Поднявшись по ней и открыв железную дверь, вы '
                            'оказываетесь на улице. Не удержавшись, делаете несколько шагов вперед, вдыхая полной грудью. ')
                        self.first_time = False
                    direction = ThreeDirectionButtons()
                    message = await ctx.send(
                        'Перед вами лабиринт из живой изгороди, высота кустов - около 4 метров. '
                        'Вы стоите на развилке из 3 дорог. Теперь вам нужно выбрать направление.', view=direction)
                    await direction.wait()
                    for child in direction.children:
                        if isinstance(child, disnake.ui.Button):
                            child.disabled = True
                    await message.edit(view=direction)

                    if direction.value == 'направо':
                        direction_1 = TwoDirectionButtons()
                        message = await ctx.send(
                            'Вы решаете следовать технике прохождения подобных лабиринтов и идти, держась правой стороны. '
                            'Вы идете всего несколько минут и встаете на следующей развилке, правда, на ней есть всего 2 '
                            'направления. Куда теперь?', veiw=direction_1)
                        await direction_1.wait()
                        for child in direction_1.children:
                            if isinstance(child, disnake.ui.Button):
                                child.disabled = True
                        await message.edit(view=direction_1)
                        if direction_1.value == 'направо':
                            await ctx.send(
                                "Упорно продолжаете следовать специальной технике. "
                                "Вы идете все дальше и дальше... Пока, наконец, не видите конец зеленой ограды. "
                                "Вы буквально бежите к долгожданному выходу... \n"
                                "Вы замираете, заметив, что земля под вашими ногами сменилась песком. "
                                "Озираетесь по сторонам, но вокруг лишь пустыня... "
                                "Оборачиваетесь и видите, что лабиринт закрыт и назад пути нет. "
                                "Ваш конец очевиден, сожалеем, но для вас квест завершен.")
                            self.death_reason = 'пустыня'
                        elif direction_1.value == 'налево':
                            await ctx.send(
                                "Поколебавшись, вы решаете не повторять свой выбор и направляетесь налево. "
                                "Проходит некоторое время, начинает смеркаться, "
                                "а вы все продолжаете идти вперед по зеленому коридору... \n"
                                "Наконец, совсем стемнело. Вам холодно, вы устали и решаете сделать небольшой привал. "
                                "Сев на землю, вы задумались: Зачем вы вообще здесь? Что будет, если вы все-таки найдете выход? "
                                "Незаметно для себя вы засыпаете. \n "
                                "Посреди ночи вас будит странный звук - будто скрежет металла... "
                                "Вы открываете глаза, и ваш взгляд привлекает 2 красных огонька. "
                                "Кажется, что это 2 светодиода и расположены они на чем-то очень массивном... Что это? \n "
                                "Вдруг чудовище начинает приближаться к вам. "
                                "Вы в ужасе бросаетесь бежать, но вскоре оно вас нагоняет. "
                                "Сожалеем, но на этом ваш квест завершен.")
                            self.death_reason = 'чудовище'

                    elif direction.value == 'прямо':
                        direction_2 = TwoDirectionButtons()
                        message = await ctx.send(
                            "Не долго думая, вы решаете идти вперед - зачем мудрить? "
                            "Вы идете довольно долго, однообразные стены вас утомляют. "
                            "Наконец, вы выходите к следующей развилке. Правда, здесь так легко "
                            "выбрать не получится - можно пойти направо или налево. Что ж, решайте.", view=direction_2)
                        await direction_2.wait()
                        for child in direction_2.children:
                            if isinstance(child, disnake.ui.Button):
                                child.disabled = True
                        await message.edit(view=direction_2)
                        if direction_2.value == 'направо':
                            await ctx.send(
                                'Проходит некоторое время, прежде чем вы выходите к развилке. '
                                'Для продолжения квеста введите волшебную комбинацию символов "/maze"')
                        elif direction_2.value == 'налево':
                            await ctx.send(
                                "Проходит еще некоторое время, вас начинает мучить нарастающий голод. "
                                "Ваш взор привлекает что-то красное... Это же ягоды! Они растут прямо на зеленой изгороди. "
                                "Забыв о здравом смысле, вы срываете их и отправляете в рот. "
                                "Они оказываются сладкими и немного притупляют мучавший вас голод. Вы отправляетесь дальше. \n"
                                "Через какое-то время вы чувствуете, что ваше самочувствие ухудшается."
                                "Вы осознаете свою ошибку - ягоды были ядовитыми... "
                                "Вас начинает бить конвульсия, изо рта идет пена... "
                                "В таком виде вы явно не способны продолжить свое путешествие. Сожалеем, но ваш квест завершен.")
                            self.death_reason = 'ядовитые ягоды'

                    elif direction.value == 'налево':
                        direction_3 = TwoDirectionButtons()
                        message = await ctx.send(
                            'Воодушевившись, вы выбираете левую дорогу, и направляетесь вперед по зеленому коридору. Через '
                            'какое-то время вы выходите к очередной развилке. Здесь есть всего 2 дороги и вы замираете на '
                            'мнгновение в нерешительности: направо или налево?', view=direction_3)
                        await direction_3.wait()
                        for child in direction_3.children:
                            if isinstance(child, disnake.ui.Button):
                                child.disabled = True
                        await message.edit(view=direction_3)
                        if direction_3.value == 'направо':
                            await ctx.send(
                                'Недолго думая, вы сворачиваете направо. Проходит какое-то время, начинает '
                                'смеркаться, а вы все продолжаете идти вперед... в какой-то момент вы спотыкаетесь о камень,'
                                ' лежащий на дороге, но вместо того, чтобы удариться о землю, вы продолжаете лететь вниз'
                                ' и вниз... лишь через полторы минуты вы наконец достигаете земли, но такое приземление '
                                'оказалось слишком жестким для ваших костей. Сожалеем, но на этом ваш квест завершен.')
                            self.death_reason = 'падение с высоты'
                        elif direction_3.value == 'налево':
                            await ctx.send(
                                "Вы решаете снова идти налево. Что ж, будь, что будет. "
                                "Вы проходите еще несколько поворотов и утыкаетесь в огромные ворота. "
                                "Внимательно осматриваете их и обнаруживаете, что в них нет обычной замочной скважины, "
                                "но зато есть 2 углубления - одно квадратной, а другое треугольной формы.\n"
                                "Вы вспоминаете, что в вашем рюкзаке лежат артефакты, которые вы зачем-то подобрали во время экспедиции. "
                                "А вдруг они и есть ключи к этим вратам? С надеждой "
                                "вы достаете их из рюкзака и... О, чудо! Они подошли! Врата жутко заскрипели и начали "
                                "медленно открываться... Вы застыли в изумлении - из-за ворот бьёт ослепляющий белый "
                                "свет. Неужели это конец квеста? \n"
                                "Поздравляем, вы нашли выход из этого лабиринта бесконечных случайностей!")
                            self.death_reason = 'win'

                elif self.level == 2:
                    door = TwoDoorButtons()
                    message = await ctx.send(
                        'Вы очнулись в помещении, из которого есть три выхода. '
                        'Подойдя к третьей двери и подергав ручку, вы убеждаетесь в том, что она заперта. '
                        'Выберите дверь и чтобы узнать, что за ней.', view=door)
                    await door.wait()
                    for child in door.children:
                        if isinstance(child, disnake.ui.Button):
                            child.disabled = True
                    await message.edit(view=door)
                    # Локация Подземелье
                    if door.value == '1':
                        door_1 = ThreeDoorButtons()
                        message = await ctx.send(
                            'Открыв дверь вы видите за ней еще одно похожее помещение, '
                            'из него также ведет 3 двери. Вы неосмотрительно отпускаете дверь, '
                            'из которой вошли, и слышите, как закрываются засовы. Прекрасно. '
                            'Вам остается только выбрать следующую дверь.', view=door_1)
                        await door1.wait()
                        for child in door_1.children:
                            if isinstance(child, disnake.ui.Button):
                                child.disabled = True
                        await message.edit(view=door_1)
                        if door_1.value == '1':
                            door_2 = ThreeDoorButtons()
                            message = await ctx.send(
                                'Вы решаетесь открыть дверь под номером 1, гадая, что ждет вас за ней... Но за ней оказывается лишь '
                                'еще одна комната, сильно напоминающая предыдущую. В ней есть всего 4 двери, включая ту, из которой '
                                'вы вошли. Вы слышите, как она закрывается на засов. Прекрасно. Все, что вам остается, выбрать '
                                'следующую дверь... ', view=door_2)
                            await door_2.wait()
                            for child in door_2.children:
                                if isinstance(child, disnake.ui.Button):
                                    child.disabled = True
                            await message.edit(view=door_2)
                            if door_2.value == '1':
                                await ctx.send(
                                    'Вы открываете следующую дверь. Из помещения, скрывавшегося за ней, слышится угрожающее '
                                    'рычание... Кажется, вы потревожили местных охранников. Сожалеем, но вас растерзала стая '
                                    'голодных псов. На этом ваш квест завершен.')
                                self.death_reason = 'псы'
                            elif door_2.value == '2':
                                await ctx.send(
                                    'Вы открываете следующую дверь и делаете несколько шагов вперед. Дверь за вами захлопывается, '
                                    'лишая последнего источника света. Все, что вам остается - идти вперед и надеяться, что коридор '
                                    'не бесконечен...')
                                self.death_reason = 'бесконечный коридор'
                            elif door_2.value == '3':
                                    if not self.stone:
                                        await ctx.send(
                                            'За дверью под номером 3 вы видите коридор. Делать нечего, так что вы решаете посмотреть, '
                                            'куда он ведет. Пройдя несколько метров по слабо освещенному коридору, вы видите драгоценный '
                                            'камень, лежащий у вас под ногами, на земле. Красивый... Решаете оставить его себе и идете '
                                            'дальше. Проходит некорое время, и вы доходите до двери, закрытой на электронный замок.'
                                            ' Видимо, именно он не позволит впоследствии открыть эту дверь с другой стороны. Вы все же '
                                            'решаете посмотреть, что скрывается за дверью. Странно, но вы вновь оказываетесь в первой '
                                            'комнате...')
                                    else:
                                        await ctx.send(
                                            'За дверью под номером 3 вы видите коридор. Делать нечего, так что вы решаете посмотреть, '
                                            'куда он ведет. Проходит некорое время, и вы доходите до двери, закрытой на электронный '
                                            'замок. Видимо, именно он не позволит впоследствие открыть эту дверь с другой стороны. Вы '
                                            'все же решаете посмотреть, что скрывается за дверью. Странно, но вы вновь оказываетесь в '
                                            'первой комнате...'
                                        )
                                    await ctx.send('Для продолжения игры введите "/maze"')
                        elif door_1.value == '2':
                            door_3 = TwoDoorButtons()
                            message = await ctx.send(
                                'Вы выбираете дверь под номером 2. За ней скрывалась еще одна комната, '
                                'но в ней всего две двери. Вам остается лишь выбрать следующую дверь.', view=door_3)
                            await door_3.wait()
                            for child in door_3.children:
                                if isinstance(child, disnake.ui.Button):
                                    child.disabled = True
                            await message.edit(view=door_3)
                            if door_3.value == '1':
                                await ctx.send(
                                    'Вы открываете следующую дверь и чувствуете сильный запах миндаля. '
                                    'Что это? Неужели, циан?')
                                self.death_reason = 'циан'
                            elif door_3.value == '2':
                                await ctx.send(
                                    'Вы открываете следующую дверь и, не глядя, делаете шаг вперед. Дверь за вами захлопывается, а '
                                    'вы оказываетесь на краю обрыва. От бесконечной пропасти вас отделяет лишь несколько сантиметров'
                                    ' земли. Ваша судьба очевидна и, как скоро бы она не наступила, ваш квест завершен.')
                                self.death_reason = 'обрыв'
                        elif door_1.value == '3':
                            async def on_message():
                                pass
                            await ctx.send(
                                'За следующей дверью оказался коридор. Вы решаетесь посмотреть, куда же он ведет. Проходит какое-то'
                                ' время, и вы утыкаетесь в стену. Растеряно оглядываетесь - неужели вы шли столько времени лишь для '
                                'того, чтобы погибнуть в запертом коридоре... \n'
                                'Вдруг ваш взгляд привлекает одна из плит на стене коридора. Вам кажется, или она немного выпирает? '
                                'Вы решаетесь нажать на нее. О, чудо! Плита отодвигается, и за ней оказывается сейф. Подле него '
                                'лежит бумажка с инструкцией. Вы берете ее и подносите к глазам, силясь разобрать в полумраке,'
                                ' что на ней написано. К сожалению, на ней написано лишь несколько слов: "№", "3 двери, 4 цифры", '
                                '"10 попыток", "И пусть удача всегда будет с вами". Вы пытаетесь понять, о чем идет речь. '
                                'Здесь явно сказано о том, что на то, чтобы угадать пинкод, у вас есть лишь 10 попыток. Вероятно, '
                                'цифры - номера дверей, которые вы выбирали. Проблема заключается лишь в том, что вы выбирали лишь 2'
                                ' двери в этом лабиринте... В вашей голове мелькает мысль о том, что вы подписывали договор на '
                                'прохождение данного квеста в комнате, под номером 9. Возможно, именно это - 3 дверь. Значит, вам '
                                'осталось угадать лишь 1 цифру, и у вас есть целых 10 попыток! Воодушевившись, вы подходите к сейфу. '
                                'Введите последовательность из четырех цифр, которая, по вашему мнению, является паролем, '
                                'открывающим сейф (например, "/password 1111")')
                    # Локация Сад
                    elif door.value == '2':
                        pass


                elif self.level == 3:
                    pass
            else:
                await ctx.send('Для начала прохождения необходимо выбрать уровень сложности.')
        else:
            await ctx.send('Для начала прохождения необходимо авторизоваться.')
        return


bot = commands.Bot(command_prefix='/', intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print('Лабиринт закручен, ключи перепрятаны')

bot.add_cog(USER(bot))
bot.run(TOKEN)

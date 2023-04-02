import sqlite3
import disnake
from disnake.ext import commands

level = -1

class ThreeDirectionButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(label="Налево", style=disnake.ButtonStyle.green)
    async def right(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        await inter.edit_original_response()
        self.value = 'налево'
        self.stop()

    @disnake.ui.button(label="Прямо", style=disnake.ButtonStyle.danger)
    async def straight(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        await inter.edit_original_response()
        self.value = 'прямо'
        self.stop()

    @disnake.ui.button(label="Направо", style=disnake.ButtonStyle.blurple)
    async def left(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        await inter.edit_original_response()
        self.value = 'направо'
        self.stop()

class TwoDirectionButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(label="Налево", style=disnake.ButtonStyle.green)
    async def right(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        await inter.edit_original_response()
        self.value = 'налево'
        self.stop()

    @disnake.ui.button(label="Направо", style=disnake.ButtonStyle.blurple)
    async def left(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        await inter.edit_original_response()
        self.value = 'направо'
        self.stop()


class ThreeDoorButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(label='1', style=disnake.ButtonStyle.green)
    async def one(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.defer()
        await inter.edit_original_response()
        self.value = '1'
        self.stop()

    @disnake.ui.button(label='2', style=disnake.ButtonStyle.danger)
    async def two(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.defer()
        await inter.edit_original_response()
        self.value = '2'
        self.stop()

    @disnake.ui.button(label='3', style=disnake.ButtonStyle.blurple)
    async def three(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.defer()
        await inter.edit_original_response()
        self.value = "3"
        self.stop()

class TwoDoorButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @disnake.ui.button(label='1', style=disnake.ButtonStyle.green)
    async def one(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.defer()
        await inter.edit_original_response()
        self.value = '1'
        self.stop()

    @disnake.ui.button(label='2', style=disnake.ButtonStyle.danger)
    async def two(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.defer()
        await inter.edit_original_response()
        self.value = "2"
        self.stop()

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


class USER(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='start')
    async def start(self, ctx):
        await ctx.send('Если вы уже зарегистрированы, напишите боту "/sign in Ваш логин Ваш пароль". \n'
                       'Если вы новый пользователь, напишите "/sign up Ваш логин Ваш пароль"')

    @commands.command(name='/restart')
    async def restart(self, ctx, ):
        await ctx.send('Если вы уже зарегистрированы, напишите боту "/sign in Ваш логин Ваш пароль". \n'
                       'Если вы новый пользователь, напишите "/sign up Ваш логин Ваш пароль"')

    @commands.command(name='sign')
    async def sign(self, ctx, operation, login, password):
        self.log_in = False
        self.login = ''
        con = sqlite3.connect('Discord_maze.db')
        cur = con.cursor()
        if operation == 'in':
            result = cur.execute(f"""SELECT * FROM Users""").fetchall()
            for i in result:
                if i[0] == login:
                    if str(i[1]) == password:
                        self.log_in = True
                        self.login = login
                        await ctx.send(f'Вы успешно авторизовались.')
                    else:
                        await ctx.send('Ваш пароль неверен. Попробуйте еще раз или создайте новую учетную запись.')
                        return
            if not self.log_in:
                await ctx.send('Похоже, у нас нет данных об учетной записи с таким логином. '
                               'Попробуйте еще раз или создайте новую учетную запись.')
        elif operation == 'up':
            cur.execute(f"""INSERT INTO Users (Login, Password) VALUES ('{login}', '{password}')""").fetchall()
            cur.execute(f"""INSERT INTO Passed_Levels (Login, Level_1, Level_2, Level_3) VALUES ('{login}', False, False, False)""").fetchall()
            con.commit()
            con.close()
            self.log_in, self.login = True, login
            await ctx.send(f'Вы успешно зарегистрировались. Ваш логин: {self.login}')
        else:
            await ctx.send('Похоже, произошла ошибка. Проверьте правильность ввода операции')
            return
        if self.log_in:
            self.death_reason = None
            self.first_time, self.stone, self.triangle = True, False, False
            self.attempt_number = 10
            view = DropdownView()
            await ctx.send('Прежде чем начать, выберите уровень сложности', view=view)

    @commands.command(name='password')
    async def password(self, ctx, attempt):
        if self.attempt_number == 0:
            return
        else:
            self.attempt_number -= 1
            await ctx.send(str(self.attempt_number) + '...')
            if attempt == '9413':
                await ctx.send('Вы слышите заветный писк - сейф взломан! На вашем лице появляется глупая улыбка - вы счастливы. '
                          'Вдруг в сейфе окажется карта, ведущая к выходу... От этой мысли вы замираете на несколько '
                          'секунд. Неужели, вы завершили квест? Вы выиграли в этой игре, длившейся, кажется, бесконечно '
                          'долго? \n Вы тряхнули головой. Зачем гадать? Вы же можете просто открыть сейф... Ваша рука тянется к '
                          'дверце сейфа. Взявшись за ручку, вы медлите еще буквально мгновение и открываете дверцу. '
                          'Раздается выстрел. Прежде, чем ваши глаза закроются навсегда, вы понимаете, что ваш квест '
                          'завершен, а сейф был лишь очередной ловушкой создателей...')
                self.death_reason = 'Сейф'
            elif self.attempt_number == 0:
                await ctx.send('Ноль. НОЛЬ! Попытки кончились, а вы так и не отгадали пароль! Надежда еще теплится в вашем '
                          'сознании, вы пробуете еще одну комбинацию, и еще одну... Но все тщетно! В какой-то момент, в '
                          'приливе неистовой ярости, вы начинаете колотить по сейфу до тех пор, пока не разбиваете руки в '
                          'кровь. Все, чего вы этим добились - дисплей сейфа погас. Теперь все бесполезно... Вы решаетесь '
                          'вернуться к двери, которая вела в этот коридор. \n'
                          'Через какое-то время вы дошли до двери. Подергав ручку, вы понимаете, что дверь заперта. Вы '
                          'разражаетесь безумным смехом - вы заперты в этом коридоре... заперты навечно. Ваша судьба '
                          'очевидна, как скоро бы она не наступила, и на этом ваш квест завершен.')
                self.death_reason = 'С сейфом навсегда'
            if self.death_reason:
                ctx.send('Для продолжения введите "/maze"')
            return

    @commands.command(name='garden')
    async def garden(self, ctx):
        global level
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
                'направления. Куда теперь?', view=direction_1)
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
                self.death_reason = 'Пустыня'
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
                self.death_reason = 'Неудачный привал'

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
                    'Проходит некоторое время, прежде чем вы выходите к первой развилке. '
                    'Для продолжения квеста введите волшебную комбинацию символов "/garden"')
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
                self.death_reason = 'Вкусные ягоды'

        elif direction.value == 'налево':
            direction_3 = TwoDirectionButtons()
            message = await ctx.send(
                'Воодушевившись, вы выбираете левую дорогу, и направляетесь вперед по зеленому коридору. Через '
                'какое-то время вы выходите к очередной развилке. Здесь есть всего 2 дороги и вы замираете на '
                'мгновение в нерешительности: направо или налево?', view=direction_3)
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
                self.death_reason = 'Подлый камень'
            elif direction_3.value == 'налево':
                if level == 1:
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
                    self.death_reason = 'Огромные врата'
                elif level == 2:
                    await ctx.send(
                        "Вы решаете снова идти налево. Что ж, будь, что будет. "
                        "Вы проходите еще несколько поворотов и утыкаетесь в огромные ворота. "
                        "Внимательно осматриваете их и обнаруживаете, что в них нет обычной замочной скважины, "
                        "но зато есть углубление квадратной формы.\n")
                    if self.stone:
                        await ctx.send(
                            "Вы вспоминаете, что в вашем рюкзаке лежит камень квадратной формы, который вы зачем-то подобрали в подземелье. "
                            "А вдруг он и есть ключ к этим вратам? С надеждой вы достаете его из рюкзака и... О, чудо! "
                            "Он подошел! Врата жутко заскрипели и начали медленно открываться... "
                            "Вы застыли в изумлении - из-за ворот бьёт ослепляющий белый свет. Неужели это конец квеста? \n"
                            "Поздравляем, вы нашли выход из этого лабиринта бесконечных случайностей!")
                        self.death_reason = 'Огромные врата'
                    else:
                        await ctx.send(
                            'Треугольник и квадрат... что должно выступать в роли ключа? В вашей голове мелькает '
                            'догадка, что при прохождении квеста вы должны были найти какие-то ключи, которые помогли '
                            'бы вам сейчас открыть дверь... \n'
                            'Вы можете вернуться в начало игры, введя "/maze"')
                elif level == 3:
                    await ctx.send(
                        "Вы решаете снова идти налево. Что ж, будь, что будет. "
                        "Вы проходите еще несколько поворотов и утыкаетесь в огромные ворота. "
                        "Внимательно осматриваете их и обнаруживаете, что в них нет обычной замочной скважины, "
                        "но зато есть углубления квадратной и треугольной формы.\n")
                    if self.stone and self.triangle:
                        await ctx.send(
                            'Вы вспоминаете, что в вашем рюкзаке лежат артефакты, которые вы зачем-то подобрали в '
                            'лабиринтах подземелья и у фонтана. А вдруг они и есть ключи к этим вратам? С надеждой '
                            'вы достаете их из рюкзака и... О, чудо! Они подошли! Врата жутко заскрипели и начали '
                            'медленно открываться... Вы застыли в изумлении - из-за ворот бьёт ослепляющий белый '
                            'свет. Неужели это конец квеста?\n'
                            'Поздравляем, вы нашли выход из этого лабиринта бесконечных случайностей!')
                        self.death_reason = 'Огромные врата'
                    elif self.triangle:
                        await ctx.send(
                            'Вы вспоминаете, что в вашем рюкзаке есть артефакт треугольной формы. Вдруг он подойдет?'
                            ' Вставив его в подходящее отверстие, вы осознаете, что вам не хватает второй детали. Но '
                            'где вы должны были её найти? Неужели, путь, который вы проделали, был недостаточен '
                            'для того, чтобы выиграть?\nВы можете вернуться в начало игры, введя "/maze"')
                    elif self.stone:
                        await ctx.send(
                            'Вы вспоминаете, что в вашем рюкзаке есть артефакт квадратной формы. Вдруг он подойдет?'
                            'Вставив его в подходящее отверстие, вы осознаете, что вам не хватает второй детали. Но '
                            'где вы должны были её найти? Неужели, путь, который вы проделали, был недостаточен для '
                            'того, чтобы выиграть?\nВы можете вернуться в начало игры, введя "/maze"')
                    else:
                        await ctx.send(
                            'Треугольник и квадрат... что должно выступать в роли ключа? В вашей голове мелькает '
                            'догадка, что при прохождении квеста вы должны были найти какие-то ключи, которые помогли '
                            'бы вам сейчас открыть дверь... \n'
                            'Вы можете вернуться в начало игры, введя "/maze"')
        if self.death_reason:
            await ctx.send('Для продолжения введите "/maze"')

    @commands.command(name='dungeon')
    async def dungeon(self, ctx):
        door_1 = ThreeDoorButtons()
        message = await ctx.send(
            'Открыв дверь, вы видите за ней еще одно похожее помещение, '
            'из него также ведет 3 двери. Вы неосмотрительно отпускаете дверь, '
            'из которой вышли, и слышите, как закрываются засовы. Прекрасно. '
            'Вам остается только выбрать следующую дверь.', view=door_1)
        await door_1.wait()
        for child in door_1.children:
            if isinstance(child, disnake.ui.Button):
                child.disabled = True
        await message.edit(view=door_1)

        if door_1.value == '1':
            door_2 = ThreeDoorButtons()
            message = await ctx.send(
                'Вы решаетесь открыть дверь под номером 1, гадая, что ждет вас за ней... Но за ней оказывается лишь '
                'еще одна комната, сильно напоминающая предыдущую. В ней есть всего 4 двери, включая ту, из которой '
                'вы вышли. Вы слышите, как она закрывается на засов. Прекрасно. Все, что вам остается, выбрать '
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
                self.death_reason = 'Псы'
            elif door_2.value == '2':
                await ctx.send(
                    'Вы открываете следующую дверь и делаете несколько шагов вперед. Дверь за вами захлопывается, '
                    'лишая последнего источника света. Все, что вам остается - идти вперед и надеяться, что коридор '
                    'не бесконечен...')
                self.death_reason = 'Бесконечный коридор'
            elif door_2.value == '3':
                if not self.stone:
                    await ctx.send(
                        'За дверью под номером 3 вы видите коридор. Делать нечего, так что вы решаете посмотреть, '
                        'куда он ведет. Пройдя несколько метров по слабо освещенному коридору, вы видите драгоценный '
                        'камень, лежащий у вас под ногами, на земле. Красивый... Решаете оставить его себе и идете '
                        'дальше. Проходит некоторое время, и вы доходите до двери, закрытой на электронный замок.'
                        ' Видимо, именно он не позволит впоследствии открыть эту дверь с другой стороны. Вы все же '
                        'решаете посмотреть, что скрывается за дверью. Странно, но вы вновь оказываетесь в первой '
                        'комнате...')
                    self.stone = True
                else:
                    await ctx.send(
                        'За дверью под номером 3 вы видите коридор. Делать нечего, так что вы решаете посмотреть, '
                        'куда он ведет. Проходит некоторое время, и вы доходите до двери, закрытой на электронный '
                        'замок. Видимо, именно он не позволит впоследствии открыть эту дверь с другой стороны. Вы '
                        'все же решаете посмотреть, что скрывается за дверью. Странно, но вы вновь оказываетесь в '
                        'первой комнате...')
                await ctx.send('Для продолжения введите "/maze"')

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
                self.death_reason = 'Циан'
            elif door_3.value == '2':
                await ctx.send(
                    'Вы открываете следующую дверь и, не глядя, делаете шаг вперед. Дверь за вами захлопывается, а '
                    'вы оказываетесь на краю обрыва. От бесконечной пропасти вас отделяет лишь несколько сантиметров'
                    ' земли. Ваша судьба очевидна и, как скоро бы она не наступила, ваш квест завершен.')
                self.death_reason = 'Обрыв'

        elif door_1.value == '3':
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
        if self.death_reason:
            await ctx.send('Для продолжения введите "/maze"')

    @commands.command(name='fountain')
    async def fountain(self, ctx):
        move = TwoDoorButtons()
        message = await ctx.send(
            'Вы решаете открыть третью дверь. За ней оказывается лестница, и вы решаете посмотреть, куда она ведет.'
            ' Спустившись вниз, вы попадаете в огромное помещение, в котором царит приятный полумрак. По центру '
            'расположен невероятной красоты фонтан. Вы решаете посмотреть поближе и подходите к бассейну, '
            'окружающему фонтан. Вдруг вы замечаете вооруженного человека, направляющегося к вам. В его руке '
            'блестит сабля. Вы инстинктивно начинаете пятиться назад. Воин замирает, как только вы отходите от '
            'фонтана. Кажется, что он его охраняет... Вам предстоит сделать выбор: сразиться с воином или '
            'попытаться вернуться наверх. Выберите "1" для побега или "2" для того, чтобы вступить в бой.', view=move)
        await move.wait()
        for child in move.children:
            if isinstance(child, disnake.ui.Button):
                child.disabled = True
        await message.edit(view=move)
        if move.value == '2':
            weapon = TwoDoorButtons()
            message = await ctx.send(
                'Вы решаете сразиться с воином. Совпадение ли это, но под ногами вы находите саблю и камень. '
                'Теперь вам предстоит выбрать свое оружие: "1" - сабля или "2" - камень.', view=weapon)
            await weapon.wait()
            for child in weapon.children:
                if isinstance(child, disnake.ui.Button):
                    child.disabled = True
            await message.edit(view=weapon)
            if weapon.value == '1':
                await ctx.send(
                    'Конечно, сабля! Схватив ее в правую руку, вы смело направляетесь к воину. Увы, это был неверный '
                    'ход - в первую же секунду боя охранник выбивает из ваших рук оружие. Ваша судьба очевидна. '
                    'Сожалеем, но на этом ваш квест завершен.')
                self.death_reason = 'Конечно, сабля'
            elif weapon.value == '2':
                water = TwoDoorButtons()
                message = await ctx.send(
                    'Как жаль, что вы не стали ходить на фехтование... Решаете взять камень - с ним у вас точно '
                    'больше шансов, чем с мечом... Очень нерешительно вы направляетесь в сторону воина. Вам '
                    'показалось, или на его лице промелькнула улыбка? Он принял воинственную позу, поудобнее '
                    'перехватив свое оружие. Вы же приготовились к смерти - и о чем вы только думали... Охранник '
                    'начал приближаться. Вы же, недолго думая, бросили в него камнем. Вдруг человек пошатнулся, из '
                    'его рук с металлическим звоном выпал меч, он упал... Вы бросились к нему. Нет, он жив, просто '
                    'потерял сознание. Это ваш шанс. Вы быстрым шагом направляетесь к фонтану, про себя благодаря '
                    'всех богов, что не убили воина. Оказалось, что бассейн, окружающий фонтан, исчерчен дорожками,'
                    ' ведущими к подножию статуи в центре. А вода такая чистая, прозрачная... Вас мучает жажда, '
                    'а вода так манит... Выберите "1" - да или "2" - нет, чтобы выпить воды из бассейна.', view=water)
                await water.wait()
                for child in water.children:
                    if isinstance(child, disnake.ui.Button):
                        child.disabled = True
                await message.edit(view=water)
                if water.value == '1':
                    await ctx.send(
                        'Решившись, вы набираете пригоршню воды и жадно пьете. Вам кажется, что вода имеет '
                        'сладковатый вкус... Наверное, просто кажется.\n'
                        'Напившись, вы отправляетесь к статуе. Но, к сожалению, до нее вы не дошли. Вас неожиданно '
                        'скручивает от сильной боли. Видимо, вода все-таки была отравлена... Сожалеем, но на этом'
                        ' ваш квест завершен.')
                    self.death_reason = 'Вода'
                elif water.value == '2':
                    self.triangle = True
                    to_continue = TwoDoorButtons()
                    message = await ctx.send(
                        'Вы стараетесь не смотреть на такую манящую вас воду и отправляетесь к статуе. Подле нее вы '
                        'обнаруживаете драгоценный камень треугольной формы. Поднимаете его и внимательно '
                        'рассматриваете. Красивый... Решаете ставить его себе и убираете в карман. Также вы '
                        'обнаруживаете записку, в которой говорится о том, что теперь вы можете перенестись в самую'
                        ' первую комнату. Для этого вам нужно пройти к противоположной стене. Теперь у вас есть'
                        ' 2 пути. Выберите "1", чтобы вернуться в первую комнату, или "2", чтобы продолжить '
                        'исследовать подножие фонтана.', view=to_continue)
                    await to_continue.wait()
                    for child in to_continue.children:
                        if isinstance(child, disnake.ui.Button):
                            child.disabled = True
                    await message.edit(view=to_continue)
                    if to_continue.value == '2':
                        await ctx.send(
                            'Вы продолжили ходить около фонтана, но больше ничего интересного не нашли. Наверное, '
                            'вам стоило вернуться наверх... Но вы упорно продолжали ходить вокруг фонтана до тех '
                            'пор, пока не закружилась голова. Вы все же решили вернуться в первую комнату')
                    await ctx.send('Для продолжения введите "/maze"')
        elif move.value == '1':
            await ctx.send(
                'Вы решаете не испытывать судьбу и уйти от фонтана. Но теперь, для того, чтобы вернуться к лестнице, '
                'вам нужно пройти мимо воина, но вас это не останавливает, и вы направляетесь к лестнице. Сожалеем,'
                ' но это был неверный выбор - воин решает, что вы вновь посягнули на его сокровище, и убивает вас. '
                'На этом ваш квест завершен.')
            self.death_reason = 'Побег'
        if self.death_reason:
            await ctx.send('Для продолжения введите "/maze"')

    @commands.command(name='maze')
    async def maze(self, ctx):
        global level
        if self.death_reason == 'Огромные врата':
            con = sqlite3.connect('Discord_maze.db')
            cur = con.cursor()
            cur.execute(f"""UPDATE Passed_Levels SET Level_{str(level)} = True WHERE Login = '{self.login}'""").fetchall()
            con.commit()
            con.close()
            await ctx.send('К сожалению, ваш квест завершен. Результаты игры можно будет в будущем посмотреть по ссылке.')
        elif self.death_reason:
            await ctx.send(f'Причина вашей смерти: {self.death_reason}. К сожалению, ваш квест завершен. '
                           'Результаты игры можно будет в будущем посмотреть по ссылке.')
        if self.death_reason:
            with open('data/User_data.txt', mode='w') as f:
                f.write(' '.join([self.login, self.death_reason]))
            await ctx.send('Для того чтобы еще раз пройти лабиринт введите "/sign in Ваш логин Ваш пароль". \n'
                           'Если вы хотите пройти лабиринт под именем уже существующего пользователя, этого будет достаточно. \n'
                           'Если вы хотите создать новую учетную запись, введите "/sign up Ваш логин Ваш пароль".')
        elif self.login:
            if level in [1, 2, 3]:
                if self.first_time:
                    await ctx.send('Добро пожаловать в игру.')

                if level == 1:
                    if self.first_time:
                        await ctx.send(
                            'Вы очнулись в помещении, из которого есть 2 выхода. '
                            'Подойдя к одной из дверей и подергав ручку вы убеждаетесь, что она заперта. '
                            'Вы открываете вторую дверь и видите лестницу. Поднявшись по ней и открыв железную дверь, вы '
                            'оказываетесь на улице. Не удержавшись, делаете несколько шагов вперед, вдыхая полной грудью. ')
                        self.first_time = False
                    await ctx.send('Для продолжения введите "/garden"')

                elif level == 2:
                    self.first_time = False
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
                        await ctx.send('Для продолжения введите "/dungeon"')
                    # Локация Сад
                    elif door.value == '2':
                        await ctx.send('Для продолжения введите "/garden"')

                elif level == 3:
                    self.first_time = False
                    door = ThreeDoorButtons()
                    message = await ctx.send(
                        'Вы очнулись в помещении, из которого есть четыре выхода. '
                        'Подойдя к четвертой двери и подергав ручку, вы убеждаетесь в том, что она заперта. '
                        'Выберите дверь чтобы узнать, что за ней.', view=door)
                    await door.wait()
                    for child in door.children:
                        if isinstance(child, disnake.ui.Button):
                            child.disabled = True
                    await message.edit(view=door)
                    # Локация Подземелье
                    if door.value == '1':
                        await ctx.send('Для продолжения введите "/dungeon"')
                    # Локация Сад
                    elif door.value == '2':
                        await ctx.send('Для продолжения введите "/garden"')
                    # Локация Фонтан
                    elif door.value == '3':
                        await ctx.send('Для продолжения введите "/fountain"')
            else:
                await ctx.send('Для начала прохождения необходимо выбрать уровень сложности.')
        else:
            await ctx.send('Для начала прохождения необходимо авторизоваться.')
        return

bot = commands.Bot(command_prefix='/', intents=disnake.Intents.all())
TOKEN = "bot token"

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f'Добро пожаловать, {member.mention}! Для начала введите "/start"'
        await guild.system_channel.send(to_send)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id}, Chat: {bot.guilds})')
    print('Лабиринт закручен, ключи перепрятаны')

bot.add_cog(USER(bot))
bot.run(TOKEN)

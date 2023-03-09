from list import DoublyLinkedList
from random import randint
from ctypes import *
import time
from memory_profiler import profile
import xml.etree.ElementTree as ET
import numpy as np
import telebot
from telebot import types
from threading import Thread
from datetime import datetime
import ast
import sys
from AnalyzAndAlgs import alg_1
import multiprocessing

CORE_LIST = {}
LAST_ANAMALS = {}


mainMar = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1_ = types.KeyboardButton("Список текущих акций")
btn2_ = types.KeyboardButton("Добавить новую акцию")
btn3_ = types.KeyboardButton("Проверить стратегию")
mainMar.add(btn1_, btn2_, btn3_)


bot = None
Telegramm_th = None

KFS = (3, 4, 5, 6)

TIME_MES_CHANGE = 10






class deal:
    def __init__(self, seccode_, tradetime_, price_, quantity_):
        self.seccode = seccode_
        self.tradetime = tradetime_
        self.price = price_
        self.quantity = quantity_




def start_strategy(message):
    data = message.text
    data = data.replace(", ", ",")
    data = data.split(",")
    th = Thread(target=alg_1, args=(bot, message.chat.id, data[0], int(data[1]), float(data[2]), float(data[3]), float(data[4]), float(data[5])))
    th.start()











def load_tools():
    file = open("toolsSUB.txt", "r")
    data = file.read().split("|")
    for i in data:
        add_sub(i)
    file.close()

def strt_bot_tg():
    global bot

    bot = telebot.TeleBot('6040110578:AAFsj0CeS8LNXFd2nGN9TM7UUI6DCTcdc7Q')


    def add_chat_id(id):
        file = open("chats.txt", "r")
        old_info = file.read()
        file.close()
        if str(id) not in old_info:
            file = open("chats.txt", "w")
            old_info += str(id) + "|"
            file.write(old_info)
            file.close()



    def add_new_seccode(seccode):
        if (str(seccode.text).upper() not in CORE_LIST):
            f = open("tools.txt", "r")
            all_deals = f.read()
            f.close()
            if str(seccode.text).upper() in all_deals.split("\n"):
                file = open("toolsSUB.txt", "w")
                s = ""
                for i in CORE_LIST:
                    s += i + "|"
                s += str(seccode.text).upper() + "|"
                file.write(s)
                file.close()
                add_sub(str(seccode.text).upper())
        bot.send_message(seccode.from_user.id, "Ready", reply_markup=mainMar)

    # Изменить на бд
    def add_subscription(mess):
        if (str(mess.text).upper() not in CORE_LIST):
            bot.send_message(mess.from_user.id, "Ошибка, акция либо не отслеживается и небходимо добавить ее в гл. меню, либо такой акции не существует", reply_markup=mainMar)
            return


        file = open("users.txt", "r")
        old_data = file.read()
        file.close()
        file = open("users.txt", "a")
        new_data = old_data.replace(str(mess.chat.id) + "|", str(mess.chat.id) + "|" + str(mess.text).upper() + "|")
        if (new_data == old_data):
            new_data = old_data + str(mess.chat.id) + "|" + str(mess.text).upper() + "|\n"
        file.truncate()
        file.write(new_data)
        file.close()

    @bot.message_handler(commands=['start'])
    def start(message):

        add_chat_id(str(message.chat.id))

        bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!")
        bot.send_message(message.from_user.id, "Что вас интересует?", reply_markup=mainMar)

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):

        if message.text == 'Список текущих акций':
            mess = ""
            for i in CORE_LIST:
                mess += i + "\n"
            if len(CORE_LIST) != 0:
                bot.send_message(message.from_user.id, mess)  # ответ бота
            else:
                bot.send_message(message.from_user.id, "empty")  # ответ бота


        elif message.text == 'Добавить новую акцию':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Ввести seccode")
            btn2 = types.KeyboardButton("Получить полный список")
            markup.add(btn1, btn2)
            bot.send_message(message.from_user.id, "Что необходимо сделать?", reply_markup=markup)

        elif message.text == 'Проверить стратегию':
            bot.send_message(message.from_user.id, "Временно доступна только 1 стратегия\nВведите данные в таком формате (используйте . в вещ. числаз): seccode_, interval_big_, rejection_in_proc_BUY_, rejection_in_proc_SELL_, money_, commission_proc")
            bot.register_next_step_handler(message, start_strategy)

        elif message.text == "Ввести seccode":

            bot.reply_to(message, 'seccode:')
            bot.register_next_step_handler(message, add_new_seccode)

        elif message.text == "Получить полный список":

            bot.send_document(message.chat.id, open(r'tools.txt', 'rb'), reply_markup=mainMar)


        # elif message.text == "Подписка":
        #     mar = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #     btn1 = types.KeyboardButton("Мои подписки")
        #     btn2 = types.KeyboardButton("Добавить новую акцию в подписку")
        #     mar.add(btn1, btn2)
        #     bot.send_message(message.chat.id, "Действие:", reply_markup=mar)
        #
        # elif message.text == "Мои подписки":
        #     pass
        #
        # elif message.text == "Добавить новую акцию в подписку":
        #     bot.reply_to(message, 'seccode:')
        #     bot.register_next_step_handler(message, add_subscription)


    bot.polling(none_stop=True, interval=0)  # обязательная для работы бота часть













def callBack(data):
    global file
    data = data.decode("utf-8")
    root = ET.fromstring(data)

    if (root.tag == "alltrades"):


        inf = deal(root[0][6].text, root[0][2].text, float(root[0][3].text), int(root[0][4].text))

        if inf.seccode not in CORE_LIST:
            CORE_LIST[inf.seccode] = Buffer(inf.seccode)
        CORE_LIST[inf.seccode].add_deal(inf)
        # print(inf.seccode)
        return 1



def send_to_all_anamal(deal_seccode, AVERAGE_X, AVERAGE_10X, AVERAGE_100X, AVERAGE_1000X, AVERAGE_10000X, AVERAGE_X_VALUE, AVERAGE_10X_VALUE, AVERAGE_100X_VALUE, AVERAGE_1000X_VALUE, AVERAGE_10000X_VALUE):
    global bot
    global LAST_ANAMALS
    print(LAST_ANAMALS)
    file = open("chats.txt", "r")
    old_info = file.read()
    file.close()
    ids = old_info.split("|")

    strr = "Бот зафиксировал аномальный объем❗❗\n"
    strr += "Инструмент " + deal_seccode + "\n"
    strr += "Средний объем за " + str(AVERAGE_X) + " сделок: " + str(round(AVERAGE_X_VALUE, 2)) + "\n"
    strr += "Средний объем за " + str(AVERAGE_10X) + " сделок: " + str(round(AVERAGE_10X_VALUE, 2)) + "\n"
    strr += "Средний объем за " + str(AVERAGE_100X) + " сделок: " + str(round(AVERAGE_100X_VALUE, 2)) + "\n"
    strr += "Средний объем за " + str(AVERAGE_1000X) + " сделок: " + str(
        round(AVERAGE_1000X_VALUE, 2)) + "\n"
    strr += "Средний объем за " + str(AVERAGE_10000X) + " сделок: " + str(round(AVERAGE_10000X_VALUE, 2))


    for i in ids:
        #LAST_ANAMALS[i][deal_seccode][0] id сообщения
        #LAST_ANAMALS[i][deal_seccode][1] время отправки сообщения
        #LAST_ANAMALS[i][deal_seccode][2] объем
        if int(i) not in LAST_ANAMALS:
            mes = bot.send_message(int(i), strr)
            LAST_ANAMALS[int(i)] = {deal_seccode: [mes.id, time.time(), AVERAGE_X_VALUE]}
            continue
        if deal_seccode not in LAST_ANAMALS[int(i)]:
            mes = bot.send_message(int(i), strr)
            LAST_ANAMALS[int(i)][deal_seccode] = [mes.id, time.time(), AVERAGE_X_VALUE]
            continue
        if time.time() - LAST_ANAMALS[int(i)][deal_seccode][1] > 100:
            mes = bot.send_message(int(i), strr)
            LAST_ANAMALS[int(i)][deal_seccode] = [mes.id, time.time(), AVERAGE_X_VALUE]
            continue
        # print("tt", AVERAGE_X_VALUE, LAST_ANAMALS[int(i)][deal_seccode][2])
        if (AVERAGE_X_VALUE > LAST_ANAMALS[int(i)][deal_seccode][2]):
            bot.edit_message_text(chat_id=int(i), message_id=LAST_ANAMALS[int(i)][deal_seccode][0], text=strr)
            LAST_ANAMALS[int(i)][deal_seccode][1] = time.time()
            LAST_ANAMALS[int(i)][deal_seccode][2] = AVERAGE_X_VALUE


class Buffer:
    def __init__(self, name):
        self.l = DoublyLinkedList()

        # self.X = 10
        # self.AVERAGE_X = self.X
        # self.AVERAGE_10X = 10 * self.X
        # self.AVERAGE_100X = 100 * self.X
        # self.AVERAGE_1000X = 1_000 * self.X
        # self.AVERAGE_10000X = 10_000 * self.X

        self.X = 10
        self.AVERAGE_X = self.X
        self.AVERAGE_10X = 4 * self.X
        self.AVERAGE_100X = 16 * self.X
        self.AVERAGE_1000X = 64 * self.X
        self.AVERAGE_10000X = 256 * self.X

        self.AVERAGE_X_NODE = None
        self.AVERAGE_10X_NODE = None
        self.AVERAGE_100X_NODE = None
        self.AVERAGE_1000X_NODE = None
        self.AVERAGE_10000X_NODE = None

        self.AVERAGE_X_VALUE = 0
        self.AVERAGE_10X_VALUE = 0
        self.AVERAGE_100X_VALUE = 0
        self.AVERAGE_1000X_VALUE = 0
        self.AVERAGE_10000X_VALUE = 0
        self.summ = 0
        self.i = 1

    def add_deal(self, deal):
        if (self.i % 1_000 == 0):
            print(self.i)

        if (self.i % (self.AVERAGE_10000X) == 0):
            self.l.add_to_file()


        # print(l.count + 1)
        self.summ += deal.quantity
        new_node = self.l.insert_at_end(deal)

        if self.l.count == self.AVERAGE_X:
            self.AVERAGE_X_NODE = self.l.start_node
            self.AVERAGE_X_VALUE = self.summ / self.AVERAGE_X

        if self.l.count == self.AVERAGE_10X:
            self.AVERAGE_10X_NODE = self.l.start_node
            self.AVERAGE_10X_VALUE = self.summ / self.AVERAGE_10X

        if self.l.count == self.AVERAGE_100X:
            self.AVERAGE_100X_NODE = self.l.start_node
            self.AVERAGE_100X_VALUE = self.summ / self.AVERAGE_100X

        if self.l.count == self.AVERAGE_1000X:
            self.AVERAGE_1000X_NODE = self.l.start_node
            self.AVERAGE_1000X_VALUE = self.summ / self.AVERAGE_1000X


        if self.l.count == self.AVERAGE_10000X:
            self.AVERAGE_10000X_NODE = self.l.start_node
            self.AVERAGE_10000X_VALUE = self.summ / self.AVERAGE_10000X


        if self.l.count > self.AVERAGE_X:
            self.AVERAGE_X_VALUE = self.AVERAGE_X_VALUE + (new_node.item.quantity - self.AVERAGE_X_NODE.item.quantity) / self.AVERAGE_X
            self.AVERAGE_X_NODE = self.AVERAGE_X_NODE.nref
        if self.l.count > self.AVERAGE_10X:
            self.AVERAGE_10X_VALUE = self.AVERAGE_10X_VALUE + (new_node.item.quantity - self.AVERAGE_10X_NODE.item.quantity) / self.AVERAGE_10X
            self.AVERAGE_10X_NODE = self.AVERAGE_10X_NODE.nref
        if self.l.count > self.AVERAGE_100X:
            self.AVERAGE_100X_VALUE = self.AVERAGE_100X_VALUE + (new_node.item.quantity - self.AVERAGE_100X_NODE.item.quantity) / self.AVERAGE_100X
            self.AVERAGE_100X_NODE = self.AVERAGE_100X_NODE.nref
        if self.l.count > self.AVERAGE_1000X:
            self.AVERAGE_1000X_VALUE = self.AVERAGE_1000X_VALUE + (new_node.item.quantity - self.AVERAGE_1000X_NODE.item.quantity) / self.AVERAGE_1000X
            self.AVERAGE_1000X_NODE = self.AVERAGE_1000X_NODE.nref

        if self.l.count > self.AVERAGE_10000X:
            self.summ -= self.l.start_node.item.quantity
            self.AVERAGE_10000X_VALUE = self.summ / self.AVERAGE_10000X
            self.l.delete_at_start()

        try:
            # print(round(self.AVERAGE_X_VALUE, 2), round(self.AVERAGE_10X_VALUE, 2), round(self.AVERAGE_100X_VALUE, 2), round(self.AVERAGE_1000X_VALUE, 2), round(self.AVERAGE_10000X_VALUE, 2))
            if (self.AVERAGE_X_VALUE / self.AVERAGE_10X_VALUE > KFS[0]):
                print("Анамальная хрень, средний объем за ", self.AVERAGE_X, "ticks is", self.AVERAGE_X_VALUE)
                print("Анамальная хрень, средний объем за ", self.AVERAGE_10X, "ticks is", self.AVERAGE_10X_VALUE)
                send_to_all_anamal(deal.seccode, self.AVERAGE_X, self.AVERAGE_10X, self.AVERAGE_100X, self.AVERAGE_1000X, self.AVERAGE_10000X, self.AVERAGE_X_VALUE, self.AVERAGE_10X_VALUE, self.AVERAGE_100X_VALUE, self.AVERAGE_1000X_VALUE, self.AVERAGE_10000X_VALUE)

            elif (self.AVERAGE_X_VALUE / self.AVERAGE_100X_VALUE > KFS[1]):
                print("Анамальная хрень, средний объем за ", self.AVERAGE_X, "ticks is", self.AVERAGE_X_VALUE)
                print("Анамальная хрень, средний объем за ", self.AVERAGE_100X, "ticks is", self.AVERAGE_100X_VALUE)
                send_to_all_anamal(deal.seccode, self.AVERAGE_X, self.AVERAGE_10X, self.AVERAGE_100X,
                                   self.AVERAGE_1000X, self.AVERAGE_10000X, self.AVERAGE_X_VALUE,
                                   self.AVERAGE_10X_VALUE, self.AVERAGE_100X_VALUE, self.AVERAGE_1000X_VALUE,
                                   self.AVERAGE_10000X_VALUE)


            elif (self.AVERAGE_X_VALUE / self.AVERAGE_1000X_VALUE > KFS[2]):
                print("Анамальная хрень, средний объем за ", self.AVERAGE_X, "ticks is", self.AVERAGE_X_VALUE)
                print("Анамальная хрень, средний объем за ", self.AVERAGE_1000X, "ticks is", self.AVERAGE_1000X_VALUE)
                send_to_all_anamal(deal.seccode, self.AVERAGE_X, self.AVERAGE_10X, self.AVERAGE_100X,
                                   self.AVERAGE_1000X, self.AVERAGE_10000X, self.AVERAGE_X_VALUE,
                                   self.AVERAGE_10X_VALUE, self.AVERAGE_100X_VALUE, self.AVERAGE_1000X_VALUE,
                                   self.AVERAGE_10000X_VALUE)


            elif (self.AVERAGE_X_VALUE / self.AVERAGE_10000X_VALUE > KFS[3]):
                print("Анамальная хрень, средний объем за ", self.AVERAGE_X, "ticks is", self.AVERAGE_X_VALUE)
                print("Анамальная хрень, средний объем за ", self.AVERAGE_10000X, "ticks is", self.AVERAGE_10000X_VALUE)
                send_to_all_anamal(deal.seccode, self.AVERAGE_X, self.AVERAGE_10X, self.AVERAGE_100X,
                                   self.AVERAGE_1000X, self.AVERAGE_10000X, self.AVERAGE_X_VALUE,
                                   self.AVERAGE_10X_VALUE, self.AVERAGE_100X_VALUE, self.AVERAGE_1000X_VALUE,
                                   self.AVERAGE_10000X_VALUE)

            # print(10, AVERAGE_X_VALUE)
            # print(100, AVERAGE_10X_VALUE)
            # print(1000, AVERAGE_100X_VALUE)
            # print(10000, AVERAGE_1000X_VALUE)
            # print(100000, AVERAGE_10000X_VALUE)
            pass
        except:
            pass

        self.i += 1



def parse_line_to_deal(line):
    pass


def reload_server():
    pass





def f():
    l = DoublyLinkedList()

    X = 10
    AVERAGE_X = X
    AVERAGE_10X = 10 * X
    AVERAGE_100X = 100 * X
    AVERAGE_1000X = 1_000 * X
    AVERAGE_10000X = 10_000 * X

    AVERAGE_X_NODE = None
    AVERAGE_10X_NODE = None
    AVERAGE_100X_NODE = None
    AVERAGE_1000X_NODE = None
    AVERAGE_10000X_NODE = None

    AVERAGE_X_VALUE = 0
    AVERAGE_10X_VALUE = 0
    AVERAGE_100X_VALUE = 0
    AVERAGE_1000X_VALUE = 0
    AVERAGE_10000X_VALUE = 0



    summ = 0
    for i in range(1, 220_000):

        if (i % 1_000 == 0):
            print(i)

        if (i % (AVERAGE_10000X + 1) == 0):
            l.add_to_file()


        # print(l.count + 1)
        number = randint(1, 1000)
        if (i == 77_777):
            number = 100_000_000
        summ += number
        new_node = l.insert_at_end(number)

        if l.count == AVERAGE_X:
            AVERAGE_X_NODE = l.start_node
            AVERAGE_X_VALUE = summ / AVERAGE_X

        if l.count == AVERAGE_10X:
            AVERAGE_10X_NODE = l.start_node
            AVERAGE_10X_VALUE = summ / AVERAGE_10X

        if l.count == AVERAGE_100X:
            AVERAGE_100X_NODE = l.start_node
            AVERAGE_100X_VALUE = summ / AVERAGE_100X

        if l.count == AVERAGE_1000X:
            AVERAGE_1000X_NODE = l.start_node
            AVERAGE_1000X_VALUE = summ / AVERAGE_1000X


        if l.count == AVERAGE_10000X:
            AVERAGE_10000X_NODE = l.start_node
            AVERAGE_10000X_VALUE = summ / AVERAGE_10000X


        if l.count > AVERAGE_X:
            AVERAGE_X_VALUE = AVERAGE_X_VALUE + (new_node.item - AVERAGE_X_NODE.item) / AVERAGE_X
            AVERAGE_X_NODE = AVERAGE_X_NODE.nref
        if l.count > AVERAGE_10X:
            AVERAGE_10X_VALUE = AVERAGE_10X_VALUE + (new_node.item - AVERAGE_10X_NODE.item) / AVERAGE_10X
            AVERAGE_10X_NODE = AVERAGE_10X_NODE.nref
        if l.count > AVERAGE_100X:
            AVERAGE_100X_VALUE = AVERAGE_100X_VALUE + (new_node.item - AVERAGE_100X_NODE.item) / AVERAGE_100X
            AVERAGE_100X_NODE = AVERAGE_100X_NODE.nref
        if l.count > AVERAGE_1000X:
            AVERAGE_1000X_VALUE = AVERAGE_1000X_VALUE + (new_node.item - AVERAGE_1000X_NODE.item) / AVERAGE_1000X
            AVERAGE_1000X_NODE = AVERAGE_1000X_NODE.nref

        if l.count > AVERAGE_10000X:
            summ -= l.start_node.item
            AVERAGE_10000X_VALUE = summ / AVERAGE_10000X
            l.delete_at_start()

        try:
            if (AVERAGE_X_VALUE / AVERAGE_10X_VALUE > 10):
                print("Анамальная хрень, средняя цена за ", AVERAGE_X, "ticks is", AVERAGE_X_VALUE)
                print("Анамальная хрень, средняя цена за ", AVERAGE_10X, "ticks is", AVERAGE_10X_VALUE)
            if (AVERAGE_X_VALUE / AVERAGE_100X_VALUE > 10):
                print("Анамальная хрень, средняя цена за ", AVERAGE_X, "ticks is", AVERAGE_X_VALUE)
                print("Анамальная хрень, средняя цена за ", AVERAGE_100X, "ticks is", AVERAGE_100X_VALUE)
            if (AVERAGE_X_VALUE / AVERAGE_1000X_VALUE > 10):
                print("Анамальная хрень, средняя цена за ", AVERAGE_X, "ticks is", AVERAGE_X_VALUE)
                print("Анамальная хрень, средняя цена за ", AVERAGE_1000X, "ticks is", AVERAGE_1000X_VALUE)
            if (AVERAGE_X_VALUE / AVERAGE_10000X_VALUE > 10):
                print("Анамальная хрень, средняя цена за ", AVERAGE_X, "ticks is", AVERAGE_X_VALUE)
                print("Анамальная хрень, средняя цена за ", AVERAGE_10000X, "ticks is", AVERAGE_10000X_VALUE)
            # print(10, AVERAGE_X_VALUE)
            # print(100, AVERAGE_10X_VALUE)
            # print(1000, AVERAGE_100X_VALUE)
            # print(10000, AVERAGE_1000X_VALUE)
            # print(100000, AVERAGE_10000X_VALUE)
            pass
        except:
            pass
        # print()

# b = Buffer("A")
# bb = Buffer("AA")
# bbb = Buffer("AAA")
# bbbb = Buffer("AAAA")
#
# i = 1
# while True:
#     b.add_deal(deal(["A", i]))
#     bb.add_deal(deal(["AA", i]))
#     bbb.add_deal(deal(["AAA", i]))
#     bbbb.add_deal(deal(["AAAA", i]))
#     i += 1



CMPFUNC = CFUNCTYPE(None, c_char_p)

def cnf(data):
    data = data.decode("utf-8")
    root = ET.fromstring(data)
    if (root.tag == "ticks"):
        inf = {"seccode": root[0][2].text, "tradetime": root[0][4].text, "price": float(root[0][5].text), "quantity": int(root[0][6].text)}
        print(inf)
    return 1

cmp_func = CMPFUNC(callBack)



lib = cdll.LoadLibrary(r"C:\libs\txmlconnector64.dll")
lib.Initialize(".", 3)

lib.SetCallback(cmp_func)

com = """<command id="connect">
    <login>FZTC22423A</login>
    <password>rEfF4Xr4</password>
    <host>tr1.finam.ru</host>
    <port>3900</port>
</command>
"""

comConnect = '<command id="server_status"/>'

comHist = """<command id="gethistorydata">
    <security>
        <board>TQBR</board>
        <seccode>GAZP</seccode>
    </security>
    <period>1</period>
    <count>10000</count>
    <reset>true</reset>
    </command>
"""


def add_sub(name):
    comSub = """<command id="subscribe">
        <alltrades>
            <security>
                <board>TQBR</board>
                <seccode>""" + name + """</seccode>
            </security>
        </alltrades>
    </command>
    """
    lib.SendCommand(bytes(comSub, "UTF-8"))


def stop_server():
    for tool in CORE_LIST:
        file = open(tool + ".txt", "r")
        lines = file.readlines()
        if len(lines) > 2:
            time = lines[-1].split("tradetime': '")[1][:-3:]
            datetime_object = datetime.strptime(time, '%m.%d.%Y %H:%M:%S')
        else:
            datetime_object = datetime.strptime("08.03.1999 10:56:10", '%m.%d.%Y %H:%M:%S')
        CORE_LIST[tool].l.add_to_file_start_from_date(datetime_object)

        file.close()
        lines.clear()


def start_server():
    global Telegramm_th
    process = multiprocessing.current_process()

    fMain = open("main_pid.txt", "w")
    fMain.write(str(process.pid))
    fMain.close()




    file = open("toolsSUB.txt", "r")
    data = file.read().split("|")
    file.close()
    for i in data:
        if i == "":
            continue
        buffer = Buffer(i)
        file = open(i + ".txt", "r")
        lines = file.readlines()
        file.close()
        if len(lines) > buffer.AVERAGE_10000X:
            for deal_l in lines[-buffer.AVERAGE_10000X::]:
                data_dict = ast.literal_eval(deal_l[:-1:])
                buffer.add_deal(
                    deal(data_dict["seccode"], data_dict["tradetime"], data_dict["price"], data_dict["quantity"]))
            CORE_LIST[i] = buffer
        else:
            for deal_l in lines:
                data_dict = ast.literal_eval(deal_l[:-1:])
                buffer.add_deal(
                    deal(data_dict["seccode"], data_dict["tradetime"], data_dict["price"], data_dict["quantity"]))
            CORE_LIST[i] = buffer
        lines.clear()
    Telegramm_th = Thread(target=strt_bot_tg)
    Telegramm_th.start()

    print("bot start")
    lib.SendCommand(bytes(com, 'UTF-8'))
    time.sleep(10)
    for i in range(1):
        lib.SendCommand(bytes(comConnect, "UTF-8"))
        time.sleep(1)

    print("ENDDDDDDDDDDDDD\n\n\n\n\n\n\n")
    load_tools()




start_server()


while (True):
    time.sleep(60 * 60 * 45)
    if (19 < datetime.now().hour < 20):
        stop_server()




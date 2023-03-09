import ast
from telebot import types



mainMar_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1_2 = types.KeyboardButton("Список текущих акций")
btn2_2 = types.KeyboardButton("Добавить новую акцию")
btn3_2 = types.KeyboardButton("Проверить стратегию")
mainMar_2.add(btn1_2, btn2_2, btn3_2)

def get_date(seccode):
    file = open(seccode + ".txt", "r")
    lines = file.readlines()
    mas = []
    for i in lines:
        mas.append(ast.literal_eval(i[:-1:]))
    lines.clear()
    return mas

def alg_1(bot, chat_id, seccode_, interval_big_, rejection_in_proc_BUY_, rejection_in_proc_SELL_, money_, commission_proc):
    seccode = seccode_
    interval_big = interval_big_
    rejection_in_proc_buy = rejection_in_proc_BUY_
    rejection_in_proc_sell = rejection_in_proc_SELL_
    money = money_
    data = get_date(seccode)
    QUANTITY_I_HAVE = 0
    if interval_big > len(data):
        return 0

    sred_big_interval = 0
    for i in range(interval_big):
        sred_big_interval += data[i]["price"]

    sred_big_interval = sred_big_interval / interval_big

    start_date_of_traiding = data[interval_big]["tradetime"]
    buys = 0
    sells = 0

    for i in range(interval_big, len(data), 1):
        # print(data[i]["price"], sred_big_interval, sred_big_interval - sred_big_interval * rejection_in_proc_buy / 100)
        if data[i]["price"] <= sred_big_interval - sred_big_interval * rejection_in_proc_buy / 100:
            count_can_buy = data[i]["quantity"]
            count_have_money = money // data[i]["price"]
            if (min(count_can_buy, count_have_money) > 0):
                buys += min(count_can_buy, count_have_money)
            money -= data[i]["price"] * min(count_can_buy, count_have_money)
            money -= commission_proc * data[i]["price"] * min(count_can_buy, count_have_money) / 100
            QUANTITY_I_HAVE += min(count_can_buy, count_have_money)
        if data[i]["price"] >= sred_big_interval + sred_big_interval * rejection_in_proc_sell / 100:
            if QUANTITY_I_HAVE > 0:
                if (min(QUANTITY_I_HAVE, data[i]["quantity"]) > 0):
                    sells += min(QUANTITY_I_HAVE, data[i]["quantity"])
                money += min(QUANTITY_I_HAVE, data[i]["quantity"]) * data[i]["price"]
                money -= commission_proc * min(QUANTITY_I_HAVE, data[i]["quantity"]) * data[i]["price"] / 100
                QUANTITY_I_HAVE -= min(QUANTITY_I_HAVE, data[i]["quantity"])
        sred_big_interval += (data[i]["price"] - data[i - interval_big]["price"]) / interval_big

    result = "Детали стратегии:\n"
    result += "Инструмент: " + seccode_ + "\n"
    result += "Интервал средней цены: " + str(interval_big) + "\n"
    result += "Отклонение цены для покупки/продажи: " + str(rejection_in_proc_BUY_) + "/" + str(rejection_in_proc_SELL_) + "%\n"
    result += "Изначальный банк: " + str(money_) + "руб\n"
    result += "Комиссия брокера: " + str(commission_proc) + "%\n"
    result += "Результаты:\n"

    if ((money + QUANTITY_I_HAVE * data[-1]["price"]) / money_ > 1):
        result += "Стратегия выгодная❗❗\n"
    else:
        result += "Стратегия убыточная❗❗\n"

    result += "Начиная с " + start_date_of_traiding + " вы совершили " + str(int(buys)) + " покупок и " + str(int(sells)) + " продаж" + "\n"
    result += "Ваш баланс не учитывая оставшиеся акции = " + str((round(money, 2))) + "руб + " + str(int(buys - sells)) + " акций\n"
    result += "Учитывая текущую стоимость акции ваш баланс составляет: " + str(round(money + QUANTITY_I_HAVE * data[-1]["price"] - commission_proc * QUANTITY_I_HAVE * data[-1]["price"] / 100, 2)) + "руб\n"
    result += "Начальный банк составлял " + str(money_) + "руб, стал " + str(round(money + QUANTITY_I_HAVE * data[-1]["price"] - commission_proc * QUANTITY_I_HAVE * data[-1]["price"] / 100, 2)) + "руб\n"
    result += "Вы заработали " + str(round((money + QUANTITY_I_HAVE * data[-1]["price"] - commission_proc * QUANTITY_I_HAVE * data[-1]["price"] / 100) * 100 / money_ - 100, 2)) + "%\n"
    result += "Остаточный акции продаются моментально за текущую стоимость!!! (доработать через стакан)"
    # print(result)
    bot.send_message(chat_id, result, reply_markup=mainMar_2)

    return result
    # print(QUANTITY_I_HAVE, money_, money, money + QUANTITY_I_HAVE * data[-1]["price"], (money + QUANTITY_I_HAVE * data[-1]["price"]) / money_)
    #Если бы вы просто купили...
    #Сделать продажу по стакану
# alg_1("GAZP", 10000, 0.5, 0.5, 1_000_000, 0.05)





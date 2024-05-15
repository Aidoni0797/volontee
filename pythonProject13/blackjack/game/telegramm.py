import requests


def send_msg(text):
    token = "7028439538:AAE2J60FhhPSpwbnXB4dq1S_hIU9H5vAxfg"
    chat_id = "1163463444"
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url_req)
    print(results.json())


send_msg("Hello volonteer!")

< div >
< input
type = "text"
placeholder = "Полное имя " / >
< / div >
< div >
< input
type = "text"
placeholder = "Ваш телеграм" / >
< / div >
< div >
< input
type = "text"
placeholder = "Телефон номер" / >
< / div >
< div >
< input
type = "text"


class ="message-box" placeholder="Сообщение" / >

< / div >

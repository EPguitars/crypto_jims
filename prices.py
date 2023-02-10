import requests
import json
import time

ticker = 'XRPUSDT'
base_url = "https://fapi.binance.com"
all_prices = []
data = {
      'prices': [],
      'times': []
      }

requests_interval = 0.026
print("Script started")

while True:   
    try:
        end_point = "/fapi/v1/premiumIndex"
        request_current = requests.get(f"{base_url}{end_point}?symbol={ticker}") # Получаю данные из API
        current_request = json.loads(request_current.text)   # Представляю данные в виде Словаря 
        current_price = float(current_request['markPrice'])    # Сохраняю значение цены из запроса в переменную       
        timestamp = current_request['time']    # Сохраняю отметку времени запроса в переменную
        data['prices'].append(current_price)        # Сохраняю цену и отметку во времени в списки словаря
        data['times'].append(timestamp)             # 
        
        if request_current.status_code == 429:       # Защита от бана. Если слишком много запросов то бинанс может забанить IP 
            requests_interval += 0.001               # соответсвенно я увеличиваю интервал между запросами и даю серверу отдохнуть
            print("Ban alert! To much requests")     # Вывожу уведомление о причине остановки
            time.sleep(60)                           # Останавлвиваю скрипт на минуту

        if len(data['times']) > 2:                                  
            spent_time = data['times'][-1] - data['times'][0]  # Получаю время с момента последнего обновления
            hour = 3600000                    # Час в милисекундах
            
            if spent_time > hour:             # Проверяю что в моей базе не больше часа информации
                data['times'][1:]             # Если больше, то удаляю самые старые данные
                data['prices'][1:]
                if spent_time > hour:         # Повторяю проверку, так как из-за временной погрешности время может всё ещё больше часа
                    data['times'][1:]
                    data['prices'][1:]
        
        max_price = max(data['prices']) # Определяю максимальную цену из имеющегося списка
        
        if max_price - current_price >= max_price / 100 : # Проверяю упала ли текущая цена на 1 процент, или больше от максимальной
            print("""                                           
            ====================
            JIM, IT'S FALLING!!!
            ====================
            """)                    #Вывожу уведомление в консоль
            
            data = {                # Обнуляю хранящиеся данные до следующего инцидента
            'prices': [],
            'times': []
            }
    except:
        print("something went wrong, waiting...")
        time.sleep(5)
    #print(f"{ticker} MAX PRICE: {max_price}")               # Можно выводить текущую и максимальные цены в консоль
    #print(f"{ticker} CURRENT PRICE: {current_price}")       # Опционально, при желании раскоментить


    time.sleep(requests_interval)


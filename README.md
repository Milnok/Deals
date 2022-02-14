# Как установить и запустить сервис RestAPI :

- Скачать [Python 3.8](https://www.python.org/downloads/), [Docker](https://docs.docker.com/engine/install/), 
   [Docker-compose](https://docs.docker.com/compose/install/).
- Открыть CMD
- Перейти в каталог куда качать репризиторий `cd ~`
- Скачать репризиторий `git clone https://github.com/Milnok/Deals.git`
- Перейти в папку Deals `cd Deals`
- Собираем проект командой `docker-compose build`
- Для запуска собранного проекта `docker-compose up`

# Как работать с сервисом RestAPI:

- Для работы можно использовать браузер либо создать запрос с помощью Postman
- `POST` запрос обрабатывает .csv файлы и отвечает результатом этой обработки
- `GET` запрос предоставляет клиенту данные о 5 покупателях, потративших наибольшую сумму
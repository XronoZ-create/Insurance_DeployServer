
# Insurance_DeployServer
Скрипт для автоматического развертывания сервера под микро-бота страхования. 
Используется API Firstbyte для получения данных о серверах(IP:логин:пароль)
**P.S Логика и алгоритм могут быть позаимствованы для развертывания серверов под другие проекты**

## Стек

 - Python 3.9
 - fabric
 - pysftp
 - requests

## Quick Start
```
git clone https://github.com/XronoZ-create/Insurance_DeployServer.git

py -3.9 deploy_async.py
py -3.9 deploy_async_files.py
```

## TO DO

 - [x] Асинхронность
 - [x] API Firstbyte

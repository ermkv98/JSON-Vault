# JSON-Vault
Простой апи-сервис
## Требования
```docker v1.13.1```

```docker-compose v1.19.0``` 

```curl v7.47.0```
## Запуск

```docker-compose build```

```docker-compose up```

### ВНИМАНИЕ! ДОЖДИТЕСЬ ЗАПУСКА ПРИЛОЖЕНИЯ ПЕРЕД СОЗДАНИЕМ ЗАПРОСОВ

## End-point'ы и примеры запросов
## File

### 0.0.0.0/File/save

method = POST

Принимает запрос в виде файла и сохраняет его на сервер, параллельно внося данные в бд

Пример запроса:

```curl -X POST -H "Content-Type: multipart/form-data" -F "file=@some.json" 0.0.0.0/File/save```

### 0.0.0.0/File/get

methpd = GET

Принимает запрос в JSON-формате, возвращая данные файла

Пример запроса:

```sudo curl -H "Content-Type: application/json" -X GET -d '{"link":<file_link>}' 0.0.0.0/File/get```

__file_link__ генерируется на сервере и возвращается при выполнении POST-запроса 

В случае, если файл защищен паролем, необходимо указать данные полей protected & password

### 0.0.0.0/File/delete

method = DELETE

Принимает запрос в JSON-формате, удаляет файл

Пример запроса:

```sudo curl -H "Content-Type: application/json" -X DELETE -d '{"link":<file_link>}' 0.0.0.0/File/delete```

### 0.0.0.0/File/update

method = PUT

Принимает запрос в JSON-формате, обновляет данные файла

Доступны для обновления __protected__, __password__, __content__(содержание файла)

Пример запроса:
 
```sudo curl -H "Content-Type: application/json" -X PUT -d '{"link":<file_link>, "protected":<protected>, "password":<password>, "content":<content>}' 0.0.0.0/File/update```

## FileList

В разработке

## Сохранение данных, сохранение в формате XML

Пример запроса на сохранение данных в формате JSON

```sudo curl -H "Content-Type: application/json" -X GET -d '{"link":<file_link>}' 0.0.0.0/File/get > <some_file.json>```

Пример запроса на сохранение данных в формате XML

```sudo curl -H "Content-Type: application/json" -X GET -d '{"link":<file_link>}' 0.0.0.0/File/xml > <some_file.json>```

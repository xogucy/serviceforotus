# serviceforotus

Минимальный сервис на FastAPI.

## Проверка

```bash
make install
make deploy
make test
make delete
```

## Коллекция Postman

Файл коллекции: `serviceforotus.postman_collection.json`.

Коллекция проверяет:

- `GET http://arch.homework/health/`
- ответ `200 OK`
- тело ответа `{"status":"OK"}`

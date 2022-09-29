# Декораторы и контроль доступа.

* Создана модель и схема пользователя
* Создан CRUD (views с методами GET/POST/PUT/DELETE)
* Добавлены методы генерации хеша пароля пользователя
* В dao Director и Genre добавлены методы POST, PUT, DELETE
* Добавлена регистрация пользователя - `POST /users/` — создает пользователя
* Добавлены эндпоинты аутентификации:

    `POST /auth/` — возвращает access_token и refresh_token или 401

    `PUT /auth/` — возвращает access_token и refresh_token или 401

    `POST /auth` — получает логин и пароль из Body запроса в виде JSON, далее проверяет соотвествие с данными в БД (есть ли такой пользователь, такой ли у него пароль)
и если всё оk — генерит пару access_token и refresh_token и отдает их в виде JSON.

    `PUT /auth` — получает refresh_token из Body запроса в виде JSON, далее проверяет refresh_token и если он не истек и валиден — генерит пару access_token и refresh_token и отдает их в виде JSON.
___

* Защищён (ограничен доступ) к некоторым эндпоинтам для запросов без токена. Для этого создан декоратор `auth_required`

`GET` /directors/ + /directors/id - Authorized Required

`GET` /movies/ + /movies/id - Authorized Required

`GET` /genres/ + /genres/id - Authorized Required

___

* Защищён (ограничен доступ) к некоторым эндпоинтам для запросов без роли admin ( `user.role == admin` ) 


`POST/PUT/DELETE`  /movies/ + /movies/id - Authorized Required + Role admin Required

`POST/PUT/DELETE`  /genres/ + /genres/id - Authorized Required + Role admin Required

`POST/PUT/DELETE`  /directors/ + /directors/id - Authorized Required + Role admin Required

* Созданы пользователи в базе данных user через запрос к api POST /users/, используя postman
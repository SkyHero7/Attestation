# Network Management System

## Описание

Система управления сетевыми элементами, позволяющая добавлять и управлять сетевыми элементами и продуктами, а также отслеживать задолженности между элементами. Реализован REST API для управления поставщиками и фильтрации по странам.

## Установка

### Шаг 1: Клонируйте репозиторий

```bash
git clone https://github.com/SkyHero7/Attestation
cd Attestation
```

### Шаг 2: Запустите локальный сервер

```bash
python manage.py runserver
```

## Описание 

На главной странице отображаются все контрагенты. 
По кнопкам ниже осуществляется переход в админ-панель, api и страницам проекта.

Реализована модель сети с последующим присвоением уровня.
Добавление объектов сети происходит на главной странице, продуктов этих объектов на странице с просмотром всех элементов
так же на странице просмотра всех элементов доступен фильтр.

В карточке объекта отображаются все контакты, выпущенные продукты. Так же был изменен пункт задолженности:
теперь при положительном значении будет отображаться, как остаток, при отрицательном - задолженность. 
Добавлена возможность смотреть все имеющиеся задолженности/остатки у определенного объекта.
Есть гиперссылки к поставщикам/объектам поставки. У объектов, не являющихся "заводами" доступна возможность обнулить задолженность
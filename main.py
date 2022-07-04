from abc import ABC, abstractmethod
import emoji  # pip install emoji
from pprint import pprint


class AbstractStorage(ABC):
    @abstractmethod
    def __init__(self, items, capacity):
        self._items = items
        self._capacity = capacity

    @abstractmethod
    def add(self, item, value):
        pass

    @abstractmethod
    def remove(self, item, value):
        pass

    @property
    @abstractmethod
    def count_value_product(self):
        """Возвращает количество свободных мест"""
        pass

    @property
    @abstractmethod
    def get_unique_items_count(self):
        """Возвращает количество уникальных товаров"""
        pass

    @property
    @abstractmethod
    def items(self):
        """Возвращает содержание склада в словаре"""


class Store(AbstractStorage):
    def __init__(self):
        self._items = {}
        self._capacity = 1_0_0

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, data):
        self._items = data

    # @property
    # def capacity(self):
    #     return self._capacity
    #
    # @capacity.setter
    # def capacity(self, data):
    #     self._capacity = data

    def add(self, item, value):
        if item in self._items:
            self._items[item] += value

        else:
            self._items[item] = value

        self._capacity -= value

    def remove(self, item, value):
        remains = self._items[item] - value
        if remains > 0:
            self._capacity += value
            self._items[item] = remains

        else:
            self._capacity = self._capacity + self._items[item]
            del self._items[item]

    @property
    def count_value_product(self):
        """Возвращает количество товара на складе"""
        count = 0
        for value in self._items.values(): count += int(value)
        return count

    def count_free_space(self):
        """Возвращает количество свободного места на складе"""
        return self._capacity - self.count_value_product

    @property
    def get_unique_items_count(self):
        """Возвращает количество уникальных товаров"""
        return len(self._items.keys())

    @property
    def get_items(self):
        """Возвращает содержание склада в словаре"""
        return self._items

    def check_name_product(self, product: str) -> dict | None:
        """Проверяет наличие записи о товаре на складе. Вернет словарь Товар \ количество
        или None"""
        products_dict = self.items
        if product in products_dict:
            return {product: products_dict[product]}
        else:
            return None

    def check_free_space(self, value: int) -> int:
        """Проверяет наличие свободного места на складе. Если запрос выше, возвращает свободное место"""
        free_space = self.count_free_space()
        if value >= free_space:
            value = free_space
            return value
        else:
            return value


class Shop(Store):
    def __init__(self):
        super().__init__()
        self._capacity = 20


class Request:
    def __init__(self, data):
        self.from_ = data['_from']
        self.to = data['to']
        self.amount = int(data['amount'])
        self.product = data['product']

    def __repr__(self):
        return f'\nИтоговый запрос на перемещение:\n' \
               f'\nПункт отправления: "{self.from_.capitalize()}"\n' \
               f'Пункт назначения: "{self.to.capitalize()}"\n' \
               f'Наименование: "{self.product.capitalize()}"\n' \
               f'Количество: {self.amount} ед.\n'

    @staticmethod
    def _split_data(data):
        return data.split(' ')


def main():
    global _from, to, destination, departure
    store = Store()
    shop = Shop()
    store_items = {
        'кола': 10,
        'фанта': 10,
        'мороженка': 2,
        'печенька': 30,
    }

    store.items = store_items

    name = input('Введите ваше имя:').capitalize()
    print(f'Привет, {name}!\n')
    while (True):
        choise = int(input(f'{name}, доступные действия:\n\n'
                           f'1. Запросить содержимое СКЛАДА\n'
                           f'2. Запросить содержимое МАГАЗИНА\n'
                           f'3. Сделать перемещение товара\n'
                           f'4. Внести изменения на СКЛАДЕ (пополнение/корректировки)\n'
                           f'5. Выход\n\n'
                           f'Введи цифру:'))

        if choise == 1:  # Отображение содержимого склада
            if len((store.items.keys())) > 0:
                print(f'{name}, продукция склада:\n')
                for item, value in store.items.items(): print(f'{item.capitalize()}: {value}')
            else:
                print(f'{name}, склады пустые!!!')
            print(f'Свободного места: {store.count_value_product}')

        if choise == 2:  # Отображение содержимого магазина
            if len((shop.items.keys())) > 0:
                print(f'{name}, продукция магазина:\n')
                for item, value in shop.items.items(): print(f'{item.capitalize()}: {value}')
            else:
                print(f'{name}, в магазине вообще нет продукции!')
            print(f'Свободного места: {shop.count_value_product}')

        if choise == 3:  # Сделать перемещение товара из СКЛАДА в МАГАЗИН (пульнем ООП по воробьям ;)
            print(f'{name}, продукция склада:\n')
            for item, value in store.items.items(): print(f'{item.capitalize()}: {value}')  # Выводим продукцию склада
            print(f'Всего продукции склада: {store.count_value_product}')  # Выводим общие объёмы продукции склада
            print(
                f'Свободного места на складе: {store.count_free_space()}')  # Выводим сколько свободного места на складе
            print(f'\n{name}, продукция магазина:\n')  # Аналогичные принты для магазина
            print(f'Всего продукции магазина: {shop.count_value_product}')
            print(f'Свободного места в магазине: {shop.count_free_space()}\n')
            for item, value in shop.items.items(): print(f'{item.capitalize()}: {value}')

            direct_transin = int(input(f'1. Сделать перемещение СКЛАД --> МАГАЗИН\n'  # Выбираем направление отгрузки
                                       f'2. Сделать перемещение МАГАЗИН --> СКЛАД\n'
                                       f'0. Отмена\n'
                                       f'Введи цифру: '))
            if direct_transin == 0:  # Кнопка "отмена"
                continue
            if direct_transin == 1:  # Формируем переменные для объекта Request
                _from = 'склад'
                to = 'магазин'
                departure = store  # Переменная "пункт отправления"
                destination = shop  # Переменная "пункт прибытия"
            if direct_transin == 2:
                _from = 'магазин'
                to = 'склад'
                departure = shop  # Переменная "пункт отправления"
                destination = store  # Переменная "пункт прибытия"

            product_transit = input(
                f'{name}, введи название товара для перемещения: ').lower()  # Запрашиваем название товара. приводим к нижнему регистру
            value_transit = int(input(
                f'{name}, введи количество товара для перемещения: '))  # Запрашиваем объём отправления. Приводим к integer

            # Производим нужные проверки
            # Проверка вообще наличия позиции на складе отправления
            product = departure.check_name_product(product_transit)  # Или None ли словарь с товаром (имя: количество)
            # Если у отправителя есть эта позиция: проверка наличия места под товар на складе получателя
            if product is not None:  # Если товар таки нашелся
                print(f'{name}, запрашиваемая позиция найдена: {product}')
            else:  # Когда вместо товара вернулся None - записи о товаре нет.
                print(f'\n{name}, увы, на складе "{to}" нет товара с названием: "{product_transit}"')
                continue

            # Проверяем что было запрошено НЕ больше чем есть на складе отправления. Если больше - переписываем запрос.
            if product[product_transit] < value_transit:  # Если остаток склада отправления меньше чем запросили
                value_transit = product[product_transit]  # Отдаём всё что есть на складе
                print(
                    f'\nЗапрашиваемого товара "{product_transit}" на остатках склада "{to}" меньше чем было запрошено.\n'
                    f'Сможем отгрузить только {value_transit} ед.')
            # Проверяем свободное место на складе получения. Если его меньше, запрос будет переписан (чтобы товар влез))
            final_value_transit = destination.check_free_space(value_transit)
            if final_value_transit == 0:  # Если туда попадает число ноль - значит места на складе получения вообще нет. Отбой
                print(f'\n{name}, увы, на складе "{to}" нет свободного места под товар. Операция невозможна!')
                continue
            if final_value_transit != value_transit:  # Свободного места оказалось меньше - уведомляем юзера
                print(f'\n{name}, увы, на складе "{to}" не так много свободного места под товар.\n'
                      f'Запрашиваемое перемещение будет выполнено в объеме: {final_value_transit}')

            # Формируем словарь запроса. Пункт отправления. Пункт назначения. Объем (может быть переписан). Продукция.
            user_request = {
                '_from': _from,
                'to': to,
                'amount': final_value_transit,
                'product': product_transit
            }

            # Формируеум объект запроса на перемещение Request
            request = Request(user_request)
            print(request)

            departure.items[request.product] -= request.amount  # Уменьшаем количество товара на складе отправления
            if not destination.items.get(request.product, None):  # Проверяем наличие записи о товаре на складе прибытия
                destination.items[request.product] = request.amount  # Запси нет. Надо создать.
            else:
                destination.items[request.product] += request.amount

            print(f'Перемещение товара выполнено!')
            print(f'{name}, продукция склада:\n')
            for item, value in store.items.items(): print(f'{item.capitalize()}: {value}')  # Выводим продукцию склада
            print(f'Всего продукции склада: {store.count_value_product}')  # Выводим общие объёмы продукции склада
            print(
                f'Свободного места на складе: {store.count_free_space()}')  # Выводим сколько свободного места на складе
            print(f'\n{name}, продукция магазина:\n')  # Аналогичные принты для магазина
            print(f'Всего продукции магазина: {shop.count_value_product}')
            print(f'Свободного места в магазине: {shop.count_free_space()}\n')
            for item, value in shop.items.items(): print(f'{item.capitalize()}: {value}')

        if choise == 4:  # Внести новые позиции на СКЛАД
            print(f'{name}, продукция склада:\n')
            for item, value in store.items.items(): print(f'{item.capitalize()}: {value}')

            print(f'\n{name}, можно внести изменения в имеющийся товар или добавить новый...')
            item = input(f'Введи название товара: ').lower()
            value = int(input(f'{name} введи количество товара: '))

            store.items.update({item: value})

        if choise == 5:  # Завершение работы программы
            print(f'{name}, хорошего дня. Завершение программы...')
            break
        input(f'\n{name}, нажми ENTER для продолжения... ')


if __name__ == '__main__':
    main()

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
    def get_free_space(self):
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
    def get_free_space(self):
        """Возвращает количество свободных мест"""
        count = 0
        for value in self._items.values(): count += int(value)
        self._capacity -= count
        return self._capacity

    @property
    def get_unique_items_count(self):
        """Возвращает количество уникальных товаров"""
        return len(self._items.keys())

    @property
    def get_items(self):
        """Возвращает содержание склада в словаре"""
        return self._items


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
        return f'Перемещение из: {self.from_}\nв: {self.to}\nнаименование: {self.product}\nколичество: {self.amount}'

    @staticmethod
    def _split_data(data):
        return data.split(' ')


def main_0():
    product_status = ['В наличии', 'Отсутствует', 'Нужное количество есть', 'Нужного количества нет']
    # while(True):
    print('Введите ваш запрос')
    # user_input = input('Введите ваш запрос:')
    user_input = 'Доставить 40 печенька из склад в магазин'
    print(f'Ваш запрос:\n{user_input}')
    store = Store()
    shop = Shop()
    request = Request(user_input)
    store_items = {
        'кола': 10,
        'фанта': 20,
        'мороженка': 40,
        'печенька': 40,
    }

    store.items = store_items

    print(f'На складе содержится: {store.items}')

    from_ = store if request.from_ == 'склад' else shop
    to_ = store if request.to == 'склад' else shop

    print(f'Продукция: {request.product.capitalize()}. \n'
          f'Хранилище: {request.from_.capitalize()}. \n'
          f'Статус: {product_status[0] if request.product in from_.items else product_status[1]}. \n'
          f'Остаток: {product_status[2] if request.amount < from_.items[request.product] else product_status[3]}.')

    # print(emoji.emojize(':OK_hand:'))


def main():
    global _from, to
    store = Store()
    shop = Shop()
    store_items = {
        'кола': 10,
        'фанта': 10,
        'мороженка': 30,
        'печенька': 20,
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
            print(f'Свободного места: {store.get_free_space}')

        if choise == 2:  # Отображение содержимого магазина
            if len((shop.items.keys())) > 0:
                print(f'{name}, продукция магазина:\n')
                for item, value in shop.items.items(): print(f'{item.capitalize()}: {value}')
            else:
                print(f'{name}, в магазине вообще нет продукции!')
            print(f'Свободного места: {shop.get_free_space}')

        if choise == 3:  # Сделать перемещение товара из СКЛАДА в МАГАЗИН (пульнем ООП по воробьям ;)
            print(f'{name}, продукция склада:\n')
            for item, value in store.items.items(): print(f'{item.capitalize()}: {value}')
            print(f'\n{name}, продукция магазина:\n')
            for item, value in shop.items.items(): print(f'{item.capitalize()}: {value}')

            direct_transin = int(input(f'1. Сделать перемещение СКЛАД --> МАГАЗИН\n'
                                       f'2. Сделать перемещение МАГАЗИН --> СКЛАД\n'
                                       f'0. Отмена\n'
                                       f'Введи цифру: '))
            if direct_transin == 0:
                continue
            if direct_transin == 1:
                _from = 'склад'
                to = 'магазин'
            if direct_transin == 2:
                _from = 'магазин'
                to = 'склад'


            item_transit = input(f'{name}, введи название товара для перемещения: ')
            value_transit = int(input(f'{name}, введи количество товара для перемещения: '))

            #TODO Check value prodict
            user_request = {
                '_from': _from,
                'to': to,
                'amount': value_transit,
                'product': item_transit
            }

            request = Request(user_request)
            print(request)
            # TODO Transfer of product prodict
        if choise == 4:  # Сделать перемещение товара из МАГАЗИНА на СКЛАД (пульнем ООП по воробьям ;)
            pass

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



from abc import ABC, abstractmethod
import emoji # pip install emoji


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
        self.data = self._split_data(data)
        self.from_ = self.data[4]
        self.to = self.data[6]
        self.amount = int(self.data[1])
        self.product = self.data[2]

    @staticmethod
    def _split_data(data):
        return data.split(' ')

    def __repr__(self):
        return f'{self.data[0]} {self.data[1]} {self.data[2]} ' \
               f'{self.data[3]}{self.data[4]}{self.data[5]} {self.data[6]}'


def main():
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

if __name__ == '__main__':
    main()

import random
import re
import hashlib
from typing import Dict

""" Класс, в котором хранится генератор значений id """
class IdCounter:
    def __init__(self):
        self._value = 0

    def get_next_id(self):
        self._value += 1
        return self._value

""" Класс, который возвращает хэш-значение введенного пароля """
class Password:
    def __init__(self):
        self._password_hash = None

    def set_password(self, password):
        # Проверка соответствия пароля минимальным требованиям
        if not isinstance(password, str):
            raise TypeError("Пароль должен быть строкой")
        if len(password) < 8:
            raise ValueError("Пароль должен быть не менее 8 символов")
        if not any(char.isdigit() for char in password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not any(char.isalpha() for char in password):
            raise ValueError("Пароль должен содержать хотя бы одну букву")
        # Хэшируем пароль и сохраняем хэш
        self._password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Метод для проверки пароля
    def check_password(self, password):
        # Если пароль не является строкой или хэш ещё не установлен, возвращаем False
        if not isinstance(password, str) or self._password_hash is None:
            return False
        # Проверяем, совпадает ли хэш пароля с сохранённым хэшем
        return self._password_hash == hashlib.sha256(password.encode()).hexdigest()

""" Класс, в котором хранится информация о продукте """
class Product:
    def __init__(self, brand, name, rating, price):
        self.brand = brand
        self.name = name
        self.rating = rating
        if price <= 0:
            raise ValueError("Price should be > 0")
        self.price = price
        self._rating = float(rating)
        if not 0 <= self._rating <= 5:
            raise ValueError("Рейтинг должен быть в диапазоне от 0 до 5.")

    # Возвращает id товара
    def get_id(self):
        return self._id

    # Возвращает имя товара
    def get_name(self):
        return self._name

    # Возвращает цену товара
    def get_price(self):
        return self._price

    def set_price(self, price):
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Цена должна быть положительным числом.")
        self._price = float(price)

    # Возвращает рейтинг товара
    def get_rating(self):
        return self._rating

    def set_rating(self, rating):
        if not isinstance(rating, (int, float)) or not 0 <= rating <= 5:
            raise ValueError("Рейтинг должен быть в диапазоне от 0 до 5.")
        self._rating = float(rating)

    # Возвращает строку, содержащую id и имя товара
    def __str__(self):
        return f"{self._id}_{self._name}"

    def __repr__(self):
        return f"Product(id={self._id}, name='{self._name}', price={self._price}, rating={self._rating})"

""" Класс с корзиной в которой хранится информация о списке товаров """
class Cart:
    def __init__(self):
        self._items: Dict[Product, int] = {}

    def add_item(self, product: Product, quantity: int = 1):
        if not isinstance(product, Product) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Некорректный товар или количество.")
        if product in self._items:
            self._items[product] += quantity
        else:
            self._items[product] = quantity

    def remove_item(self, product: Product, quantity: int = 1):
        if not isinstance(product, Product) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Некорректный товар или количество.")
        if product in self._items:
            if self._items[product] <= quantity:
                del self._items[product]
            else:
                self._items[product] -= quantity

    def get_items(self):
        return self._items.copy()

""" Класс, который описывает пользователя """
class User:
    def __init__(self, username, password):
        self._id = IdCounter().get_next_id()
        if not isinstance(username, str) or not re.match(r'^[a-zA-Z]{3,16}$', username):
            raise ValueError("Некорректное имя пользователя.")
        self._username = username
        self._password = Password()
        self._password.set_password(password)
        self._cart = Cart()

    def get_id(self):
        return self._id

    @property
    def username(self):
        return self._username

    def __str__(self):
        return f"User(id={self._id}, username={self._username})"

    def __repr__(self):
        return f"User(id={self._id}, username='{self._username}', password='password1', cart={self._cart})"

""" Класс генерации для создания продуктов"""
class ProductGenerator:
    brands = ["Samsung", "LG", "Bosch", "Philips", "Panasonic"]
    names = ["Холодильник", "Стиральная машина", "Пылесос", "Мультиварка", "Тостер", "Электрочайник"]
    min_rating = 1
    max_rating = 5
    min_price = {"Холодильник": 100000, "Стиральная машина": 40000, "Пылесос": 5000,
                 "Мультиварка": 3000, "Тостер": 1500, "Электрочайник": 1000}
    max_price = {"Холодильник": 200000, "Стиральная машина": 70000, "Пылесос": 15000,
                 "Мультиварка": 8000, "Тостер": 3000, "Электрочайник": 5000}

    @staticmethod
    def generate():
        brand = random.choice(ProductGenerator.brands)
        name = random.choice(ProductGenerator.names)
        rating = round(random.uniform(ProductGenerator.min_rating, ProductGenerator.max_rating), 2)
        price = round(random.uniform(ProductGenerator.min_price[name], ProductGenerator.max_price[name]), 2)
        return Product(brand, name, rating, price)

""" Класс, описывающий магазин """
class Store:
    def __init__(self):
        self._products = []
        for _ in range(20):
            self._products.append(ProductGenerator.generate())
        self._current_user = None

    def login(self):
        print("Аутентификация")
        username = input("Логин: ")
        password = input("Пароль: ")
        self._current_user = User(username, password)
        print(f"Пользователь: {self._current_user.username}, пароль: password1")
        print(f"Пользователь {self._current_user.username} авторизован.")
    def add_product_to_cart(self):
        if self._current_user is None:
            print("Для добавления товара в корзину необходимо авторизоваться.")
            return

        product = random.choice(self._products)
        self._current_user._cart.add_item(product)
        print("Товар добавлен в корзину пользователя.")

    def show_cart(self):
        if self._current_user is None:
            print("Для просмотра корзины необходимо авторизоваться.")
            return

        items = self._current_user._cart.get_items()
        if not items:
            print("Корзина пуста.")
        else:
            print(f"Корзина пользователя {self._current_user.username}:")
            for product, quantity in items.items():
                print(f"{product.brand} {product.name} - {product.price} руб., - {product.rating} рейтинг (кол-во: {quantity})")
            total_price = round(sum([product.price * quantity for product, quantity in items.items()]), 2)
            print(f"Итого: {total_price} руб.\n")

if __name__ == '__main__':
    store = Store()
    store.show_cart()  # Для просмотра корзины необходимо авторизоваться
    store.add_product_to_cart()  # Для добавления товара в корзину необходимо авторизоваться
    store.login()
    store.show_cart()  # Корзина пуста
    store.add_product_to_cart()  # Товар добавлен в корзину пользователя
    store.show_cart()  # Корзина пользователя с товарами


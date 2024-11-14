from collections import namedtuple, OrderedDict, Counter, ChainMap
Item = namedtuple('Item', 'name price category')
store_items = OrderedDict()
store_items['item1'] = Item(name='Laptop', price=1000, category='Electronics')
store_items['item2'] = Item(name='Desk', price=150, category='Furniture')
store_items['item3'] = Item(name='Chair', price=85, category='Furniture')
category_counter = Counter(item.category for item in store_items.values())
default_settings = {'currency': 'USD', 'discounts_enabled': False}
store_settings = {'currency': 'EUR'}
settings = ChainMap(store_settings, default_settings)
print("1. namedtuple- Item:", store_items['item1'])
print("2. OrderedDict- All Items:", list(store_items.values()))
print("3. Counter- Category Counts:", category_counter)
print("4. ChainMap- Combined Settings:", settings)

from collection import namedtuple, OrderedDict, Counter, ChainMap
Item = namedtuple('Item', 'name price category')
store_items = OrderedDict()
store_items['item1'] = Item(name='Laptop', price=1000, category='Electronic')
store_items['item1'] = Item(name='Laptop', price=1000, category='Electronic')
store_items['item1'] = Item(name='Laptop', price=1000, category='Electronic')
category_counter = Counter(store_settings, default_settings)
default_settings = {'currency': 'USD', 'discounts_enabled': False}
store_settings = {'currency': 'EUR'}
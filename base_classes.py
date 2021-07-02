from abc import ABC, abstractmethod
import abc

class FormalStockClass(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls,subclass):
        return  (hasattr(subclass,'__init__') and
            callable(subclass.__init__) and
            hasattr(subclass,'purchase_stock') and
            callable(subclass.purchase_stock) and
            hasattr(subclass,'sell_stock') and
            callable(subclass.sell_stock) and
            hasattr(subclass,'get_price') and
            callable(subclass.get_price) and
            hasattr(subclass,'check_dividend') and
            callable(subclass.check_dividend) and
            hasattr(subclass,'get_dividend_strategy') and
            callable(subclass.get_dividend_strategy) and
            hasattr(subclass,'reinvest_dividend') and
            callable(subclass.reinvest_dividend) and
            hasattr(subclass,'sell_dividend') and
            callable(subclass.sell_dividend) and
            hasattr(subclass,'get_stock_data') and
            callable(subclass.get_stock_data))

    @abc.abstractmethod
    def __init__(self,placeholder: float):
        """Placeholder description"""
        raise NotImplementedError

    @abc.abstractmethod
    def purchase_stock(self,placeholder: float):
        """Placeholder description"""
        raise NotImplementedError

    @abc.abstractmethod
    def sell(self,placeholder: float):
        """Placeholder description"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_price(self, placeholder):
        """Placeholder description"""
        raise NotImplementedError

    @abc.abstractmethod
    def check_dividend(self,placeholder: float):
        """Placeholder description"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_dividend_strategy(self,placeholder: float):
        """Placeholder description"""
        raise NotImplementedError

    @abc.abstractmethod
    def reinvest_dividend(self,placeholder: float):
        """Placeholder description"""
        raise NotImplementedError

    @abc.abstractmethod
    def sell_dividend(self,placeholder: float):
        """Placeholder description"""
        raise NotImplementedError    

    @abc.abstractmethod
    def get_forecast(self,placeholder: str):
        """Placeholder description"""
        raise NotImplementedError

class FormalHouseClass(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls,subclass):
        return (hasattr(subclass,'__init__') and
        callable(subclass.__init__) and
        hasattr(subclass,'check_loan') and
        callable(subclass.check_loan) and
        hasattr(subclass,'get_loan') and
        callable(subclass.get_loan) and
        hasattr(subclass,'get_price') and
        callable(subclass.get_price) and
        hasattr(subclass,'sell') and
        callable(subclass.sell) and
        hasattr(subclass,'get_forecast') and
        callable(subclass.get_forecast) and
        hasattr(subclass,'get_expenses') and
        callable(subclass.get_expenses))

    @abc.abstractclassmethod
    def __init__(self,initial_price: float = 0, start_date = '1900-01-01'):
        """Placeholder description"""
        raise NotImplementedError

    @abc.abstractmethod
    def check_loan(self):
        """Placeholder description"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_loan(self):
        """Placeholder description"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_price(self, placeholder):
        """Placeholder description"""
        raise NotImplementedError

    @abc.abstractmethod
    def sell(self,placeholder: float):
        """Placeholder description"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_forecast(self,placeholder: float):
        """Placeholder description"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_expenses(self,placeholder: float):
        """Placeholder description"""
        raise NotImplementedError


class FormalCSVImport(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls,subclass):
        return (hasattr(subclass,'__init__') and
        callable(subclass.__init__) and
        hasattr(subclass,'get') and
        callable(subclass.get) and
        hasattr(subclass,'display_headers') and
        callable(subclass.display_headers) and
        hasattr(subclass,'display_units') and
        callable(subclass.display_units))
    
    @abc.abstractclassmethod
    def __init__(self,initial_price: float = 0, start_date = '1900-01-01'):
        """Placeholder description"""
        raise NotImplementedError

    @abc.abstractmethod
    def get(self):
        """Placeholder description"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def display_headers(self):
        """Placeholder description"""
        raise NotImplementedError

    @abc.abstractmethod
    def display_units(self, placeholder):
        """Placeholder description"""
        raise NotImplementedError


# class HouseClass(FormalHouseClass):
#     def __init__(self,initial_price,start_date):
#         self.initial_price = initial_price
#         self.start_date = start_date

#     def check_loan():
#         return None
#     def get_loan():
#         return None
#     def get_price():
#         return None
#     def sell():
#         return None
#     def get_forecast():
#         return None
#     def get_expenses():
#         return None

    
# Home = HouseClass(500_000,'2015-12-26')
# print(Home.initial_price)
# print(Home.start_date)
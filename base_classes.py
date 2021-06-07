from abc import ABC, abstractmethod
import abc

class StockClass(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls,subclass):
        return  (hasattr(subclass,'__init__') and
            callable(subclass.__init__) and
            hasattr(subclass,'withdraw') and
            callable(subclass.withdraw) and
            hasattr(subclass,'deposit') and
            callable(subclass.deposit_) and
            hasattr(subclass,'setBalance') and
            callable(subclass.setBalance))

    @abc.abstractmethod
    def __init__(self,balance: float):
        """Set purchase date, cost base, ongoing cost, deductions"""
        raise NotImplementedError

    @abc.abstractmethod
    def purchase_stock(self,amount: float):
        """Withdraw a user defined amount"""
        raise NotImplementedError

    @abc.abstractmethod
    def sell_stock(self,amount: float):
        """Deposit a user defined amount"""
        raise NotImplementedError

    @abc.abstractmethod
    def check_dividend(self,newBalance: float):
        """Set a new account balance"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_dividend_strategy(self,newBalance: float):
        """Set a new account balance"""
        raise NotImplementedError

    @abc.abstractmethod
    def reinvest_dividend(self,newBalance: float):
        """Set a new account balance"""
        raise NotImplementedError

    @abc.abstractmethod
    def sell_dividend(self,newBalance: float):
        """Set a new account balance"""
        raise NotImplementedError    

    @abc.abstractmethod
    def get_stock_data(self,name: str):
        """Set a new name"""
        raise NotImplementedError

class DataCollector(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls,subclass):
        return hasattr(subclass,'__init__') and
            callable(subclass,__init__)
    

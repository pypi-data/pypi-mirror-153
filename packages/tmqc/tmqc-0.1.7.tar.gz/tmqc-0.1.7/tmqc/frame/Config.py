import abc
import re
from common import Decorator
from collections import namedtuple


class ConfigBase:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_mutil(self, code):
        return 0

    @abc.abstractmethod
    def get_open_fee(self, code):
        return 0

    @abc.abstractmethod
    def get_close_fee(self, code):
        return 0

    @abc.abstractmethod
    def get_close_today_fee(self, code):
        return 0

    @abc.abstractmethod
    def get_margin_rate(self, code):
        return 0

    @abc.abstractmethod
    def get_slippage(self, code):
        return 0.000

    @abc.abstractmethod
    def init(self, datacenter):
        pass


@Decorator.singleton
class cStock(ConfigBase):
    def __init__(self):
        super().__init__()

    def get_mutil(self, code):
        return 1

    def get_open_fee(self, code):
        """返回率，值"""
        return 0.0002, 0

    def get_close_fee(self, code):
        """返回率，值"""
        # return 0.0002, 0
        return 0.0002, 0

    def get_close_today_fee(self, code):
        """返回率，值"""
        # return 0.0002, 0
        return 0.0000, 0

    def get_margin_rate(self, code):
        return 1
    
    def get_slippage(self, code):
        return 0.000    

    def get_slippage(self, code):
        return 0.001
    
    def init(self, datacenter):
        pass


@Decorator.singleton
class cFurture(ConfigBase):
    def __init__(self):
        super().__init__()
        self.com_mar = {}
        self.pt_mul = {}
        self.slippage ={}

        ContractFee = namedtuple('ContractFee', ['open_fee', 'close_fee', 'close_today_fee', 'margin_rate'])
        with open("conf/contract_com_mar.ini", "rt") as f:
            l = f.readline()
            while l:
                arrs = re.split(r"\s+", l)
                if arrs[0][0] != "#":
                    self.com_mar[arrs[0]] = ContractFee(open_fee=float(arrs[1]),
                                                        close_fee=float(arrs[2]),
                                                        close_today_fee=float(arrs[3]),
                                                        margin_rate=float(arrs[4]))
                l = f.readline()

        ContractMutil = namedtuple('ContractMutil', ['mutil', 'mintick'])
        with open("conf/contract_pt_mul.ini", "rt") as f:
            l = f.readline()
            while l:
                arrs = re.split(r"\s+", l)
                if arrs[0][0] != "#":
                    self.pt_mul[arrs[0]] = ContractMutil(mintick=float(arrs[1])/10000.0, mutil=float(arrs[2]))
                l = f.readline()
                
        ContractSlippage = namedtuple('ContractSlippage', ['slippage'])
        with open("conf/contract_slippage.ini", "rt") as f:
            l = f.readline()
            while l:
                arrs = re.split(r"\s+", l)
                if arrs[0][0] != "#":
                    self.slippage[arrs[0]] = ContractSlippage(slippage=float(arrs[1])/100)
                l = f.readline()
                
    def get_mutil(self, code):
        if code[-2:] == 'L0': code = code[:-2]
        code = ''.join([i for i in code if not i.isdigit()])
        c = self.pt_mul.get(code)
        if c is None:
            return 1
        return c.mutil

    def get_open_fee(self, code):
        if code[-2:] == 'L0': code = code[:-2]
        code = ''.join([i for i in code if not i.isdigit()])
        c = self.com_mar.get(code)
        if c is None:
            return 0,0
        if c.open_fee > 1e7:
            return 0, c.open_fee / 1e7
        return c.open_fee / 1e7, 0

    def get_close_fee(self, code):
        if code[-2:] == 'L0': code = code[:-2]
        code = ''.join([i for i in code if not i.isdigit()])
        c = self.com_mar.get(code)
        if c is None:
            return 0,0
        if c.close_fee > 1e7:
            return 0, c.close_fee / 1e7
        return c.close_fee / 1e7, 0

    def get_close_today_fee(self, code):
        if code[-2:] == 'L0': code = code[:-2]
        code = ''.join([i for i in code if not i.isdigit()])
        c = self.com_mar.get(code)
        if c is None:
            return 0,0
        if c.close_today_fee > 1e7:
            return 0, c.close_today_fee / 1e7
        return c.close_today_fee / 1e7, 0

    def get_margin_rate(self, code):
        if code[-2:] == 'L0': code = code[:-2]
        code = ''.join([i for i in code if not i.isdigit()])
        c = self.com_mar.get(code)
        if c is None:
            return 1
        return c.margin_rate / 1e3
    
    def get_slippage(self, code):
        return 0.000    

    def get_slippage(self, code):
        if code[-2:] == 'L0': code = code[:-2]
        code = ''.join([i for i in code if not i.isdigit()])
        c1 = self.slippage.get(code)
        if c1 is None:
            return 1
        
        c2 = self.pt_mul.get(code)
        if c2 is None:
            return 1
        
        return c1.slippage * c2.mintick

    def init(self, datacenter):
        pass


@Decorator.singleton
class cOption(ConfigBase):
    def __init__(self):
        super().__init__()
        self.info = None
        self.mutils = {}

    def get_mutil(self, code):
        mutil = self.info[self.info['code'] == code].iloc[-1]['contract_unit']
        return mutil

    def get_open_fee(self, code):
        """返回率，值"""
        return 0, 2

    def get_close_fee(self, code):
        """返回率，值"""
        return 0, 2

    def get_close_today_fee(self, code):
        """返回率，值"""
        return 0, 2

    def get_margin_rate(self, code):
        return 1

    def get_slippage(self, code):
        return 0.0001

    def init(self, datacenter):
        self.info = datacenter.option.info


stock = cStock()
future = cFurture()
option = cOption()

if __name__ == '__main__':
    import sys, os

    # sys.path.append('..')
    os.chdir('..')

    sc = stock
    fc = future
    oc = option

    print(fc.get_mutil("FG"))
    print(fc.get_open_fee("FG"))
    print(fc.get_close_fee("FG"))

#!/usr/bin/env python3
from collections.abc import Iterable
from typing import List, Tuple

from abc import ABC, abstractmethod

class BaseComplement(ABC):
    """
        Radix-wise representation of negative integers, as seen in binary with
        2s complement numbers, but extended to other bases
    """
    def __init__(self, number: int, base: int, slots: int, symbols: str):
        """ Takes a number in base 10 and turns it into the internal
            representation. The number given must fall within the range
            supported by the representation. """

        self.BASE = base
        self.SLOTS = slots
        self.SYMBOLS = symbols

        if number < self.MIN or number > self.MAX:
            raise ValueError(f"Number out of range: {number}")

        if number >= 0:
            self.digits = self.num2digs(number)
        else:
            complement = self.SIZE + number
            self.digits = self.num2digs(complement)

    def __add__(self, other):
        """ Performs a radixwise summation of the digits given by two
        BaseComplements. Given the nature of BaseCompelement numbers, simply
        adding the digits one by one will automatically deal with the signs of
        each number, without having to do anything. Note that the resulting
        list of digits will be the internal representation of our format. """
        carry = 0
        radixwise = [0] * self.SLOTS

        if self.BASE != other.BASE or self.SLOTS < other.SLOTS:
            raise ValueError("Can't sum together different BaseComplement types")

        for idx, (i, j) in enumerate(zip(self, other)):
            s = i + j + carry
            radixwise[idx] = s % self.BASE
            carry = s // self.BASE

        sum_num = self.digs2num(radixwise)

        if sum_num >= self.SIZE // 2:
            sum_num -= self.SIZE

        return type(self)(sum_num)

    def num2digs(self, num: int) -> List[int]:
        """ Transforms a signed decimal number into the internal representation
        of our BaseComplement """
        digs = [0] * self.SLOTS
        for pos in range(self.SLOTS):
            digs[pos] = num % self.BASE
            num //= self.BASE
        return digs

    def digs2num(self, nums: Iterable[int]) -> int:
        """ Transforms our list of internal representation digits into a
        decimal number """
        num = 0
        for dig in reversed(nums):
            num = num * self.BASE + dig
        return num

    def digs2str(self, nums: Iterable[int]) -> str:
        return "".join(self.SYMBOLS[n] for n in nums)

    def __getitem__(self, idx: int) -> int:
        """ Takes care of indexing: we prefer LSB ordering for numbers, it
        feels more natural due to carry """
        return self.digits[-(idx + 1)]

    def __len__(self) -> int:
        return self.SLOTS

    def __iter__(self):
        return iter(self.digits)

    def __repr__(self) -> str:
        """ Displays the internal represenation """
        return "Complement<Base:{base}, {digs}>".format(digs=self.digs2str(self.digits), base=self.BASE)

    def __str__(self) -> str:
        """ Turns the numbers into a signed decimal number (aka including the
        minus sign lol lmao) """
        raw = self.digs2num(self.digits)
        if raw >= self.SIZE // 2:
            raw -= self.SIZE
        return str(raw)

    def __eq__(self, other) -> bool:
        if isinstance(other, BaseComplement):
            if other.BASE == self.BASE and other.SLOTS < self.SLOTS:
                return self.digits == other.digits
            else:
                return NotImplemented
        elif isinstance(other, int):
            return int(self) == other
        else:
            return NotImplemented

    def __int__(self) -> int:
        raw = self.digs2num(self.digits)
        if raw >= self.SIZE // 2:
            raw -= self.SIZE
        return raw

    @property
    def SIZE(self) -> int:
        return self.BASE ** self.SLOTS

    @property
    def MIN(self) -> int:
        return -(self.SIZE // 2)

    @property
    def MAX(self) -> int:
        return self.SIZE // 2 - 1

    @property
    def RANGE(self) -> Tuple[int,int]:
        return self.MIN, self.MAX

class BinComplement(BaseComplement):
    BASE = 2
    SLOTS = 32
    SYMBOLS = "01"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, base=self.BASE, slots=self.SLOTS, symbols=self.SYMBOLS)

class HexComplement(BaseComplement):
    BASE = 16
    SLOTS = 4
    SYMBOLS = "0123456789abcdef"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, base=self.BASE, slots=self.SLOTS, symbols=self.SYMBOLS)

class SexComplement(BaseComplement):
    BASE = 6
    SLOTS = 6
    SYMBOLS = "012345"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, base=self.BASE, slots=self.SLOTS, symbols=self.SYMBOLS)

class TenComplement(BaseComplement):
    BASE = 10
    SLOTS = 4
    SYMBOLS = "0123456789"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, base=self.BASE, slots=self.SLOTS, symbols=self.SYMBOLS)



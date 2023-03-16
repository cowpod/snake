from uuid import UUID
from typing import Type

WEIGHT_SNAKE = -128
WEIGHT_FOOD = 64
WEIGHT_HAZARD = -129

class Position:
    def __init__(self, x:int, y:int, weight:int):
        assert(type(x) is int)
        assert(type(y) is int)
        assert(type(weight) is int)
        self._x = x
        self._y = y
        self._weight = weight
    def x(self)->int:
        return self._x
    def y(self)->int:
        return self._y
    def tuple(self)->tuple:
        return (self._x,self._y)
    def weight(self)->int:
        return self._weight
    def setWeight(self, weight)->None:
        self._weight=weight
    def addWeight(self, add)->None:
        assert(add>=0)
        self._weight=self._weight+add
    def subtractWeight(self, subtract)->None:
        assert(subtract>=0)
        self._weight=self._weight-subtract
    def __str__(self):
        return(str(self._weight))
        
class Food(Position):
    def __init__(self, x:int, y:int):
        assert(type(x) is int)
        assert(type(y) is int)
        super().__init__(x, y, WEIGHT_FOOD)

class Hazard(Position):
    def __init__(self, x:int, y:int, type:str):
        assert(type(x) is int)
        assert(type(y) is int)
        assert(type(type) is str)
        super().__init__(x, y, WEIGHT_HAZARD)
        self._type=type
    def type(self)->str:
        return self._type

class Snake(Position):
    def __init__(self, x:int, y:int, id:UUID, length:int, health:int, head:bool):
        assert(type(x) is int)
        assert(type(y) is int)
        assert(type(id) is UUID)
        assert(type(length) is int)
        assert(type(health) is int)
        assert(type(head) is bool)
        super().__init__(x, y, WEIGHT_SNAKE)
        self._id = id
        self._length = length
        self._health = health
        self._head = head
    def id(self)->UUID:
        return self._id
    def length(self)->int:
        return self._length
    def health(self)->int:
        return self._health
    def isHead(self)->bool:
        return self._head

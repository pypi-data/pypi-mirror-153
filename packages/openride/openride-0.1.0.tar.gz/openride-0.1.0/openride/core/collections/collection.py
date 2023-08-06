from openride.core.transform import Transform

from abc import ABC, abstractclassmethod
from typing import Any



class Collection(ABC):

    @abstractclassmethod
    def __len__(self) -> int:
        """Amount of objects in the collection"""


    @abstractclassmethod
    def append(self, obj:Any):
        """Add an object to the collection"""


    @abstractclassmethod
    def extend(self, collection:'Collection'):
        """Add another collection to this collection"""


    @abstractclassmethod
    def pop(self, index:int) -> Any:
        """Remove and return the object at index"""
        

    def __repr__(self):
        s = f'{self.__class__.__name__}: (N={len(self)}) \n'
        for i, obj in enumerate(self):
            s += f'{i}: {obj} \n'
        return s[:-2]


    @abstractclassmethod
    def __getitem__(self, index:int) -> Any:
        """Return the object at index"""


    @abstractclassmethod
    def transform(self, transform:Transform) -> 'Collection':        
        """Return a transformed copy of this collection"""

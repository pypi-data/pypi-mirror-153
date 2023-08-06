from __future__ import annotations
from ctypes import Union
from typing import Dict, Generic, Iterable, Iterator, List, Set, Optional, Tuple, Type, TypeVar, Callable, overload

T = TypeVar("T")
R = TypeVar("R")

K = TypeVar("K")
V = TypeVar("V")


class Iter(Generic[T]):
    _iter: Iterable[T]

    def __init__(self, v: Iterable[T]) -> None:
        super().__init__()
        self._iter = v

    def filter(self, predicate: Callable[[T], bool]) -> Iter[T]:
        """
        Returns a Iter containing only elements matching the given [predicate].

         Example 1:
        >>> lst = [ 'a1', 'b1', 'b2', 'a2']
        >>> Iter(lst).filter(lambda x: x.startswith('a'))
        ['a1', 'a2']
        """
        return Iter(filter(predicate, self._iter))

    def filter_is_instance(self, r_type: Type[R]) -> Iter[R]:
        """
         Returns a Iter containing all elements that are instances of specified type parameter r_type.

        Example 1:
        >>> lst = [ 'a1', 1, 'b2', 3]
        >>> Iter(lst).filter_is_instance(int)
        [1, 3]

        """
        return self.filter(lambda x: type(x) == r_type)

    def filter_not(self, predicate: Callable[[T], bool]) -> Iter[T]:
        """
         Returns a Iter containing all elements not matching the given [predicate].

         Example 1:
        >>> lst = [ 'a1', 'b1', 'b2', 'a2']
        >>> Iter(lst).filter_not(lambda x: x.startswith('a'))
        ['b1', 'b2']
        """
        return Iter(filter(lambda x: not predicate(x), self._iter))

    def filter_not_none(self) -> Iter[T]:
        """
         Returns a Iter containing all elements that are not `None`.

         Example 1:
        >>> lst = [ 'a', None, 'b']
        >>> Iter(lst).filter_not_none()
        ['a', 'b']
        """
        return self.filter(lambda x: x is not None)

    def map(self, transform: Callable[[T], R]) -> Iter[R]:
        """
         Returns a Iter containing the results of applying the given [transform] function
         to each element in the original Iter.

         Example 1:
        >>> lst = [{ 'name': 'A', 'age': 12}, { 'name': 'B', 'age': 13}]
        >>> Iter(lst).map(lambda x: x['age'])
        [12, 13]
        """
        return Iter(map(transform, self._iter))
    
    def map_not_none(self, transform: Callable[[T], Optional[R]]) -> Iter[R]:
        """
         Returns a list containing only the non-none results of applying the given [transform] function
        to each element in the original collection.

         Example 1:
        >>> lst = [{ 'name': 'A', 'age': 12}, { 'name': 'B', 'age': None}]
        >>> Iter(lst).map_not_none(lambda x: x['age'])
        [12]
        """
        return self.map(transform).filter_not_none()

    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """
         Returns the first element matching the given [predicate], or `None` if no such element was found.
        
         Example 1:
        >>> lst = ['a', 'b', 'c']
        >>> Iter(lst).find(lambda x: x == 'b')
        'b'
        """
        return self.first_or_none(predicate)
    
    def find_last(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """
         Returns the last element matching the given [predicate], or `None` if no such element was found.
        
         Example 1:
        >>> lst = ['a', 'b', 'c']
        >>> Iter(lst).find_last(lambda x: x == 'b')
        'b'
        """
        return self.last_or_none(predicate)

    @overload
    def first(self) -> T:
        """
         Returns first element.

         Example 1:
        >>> lst = ['a', 'b', 'c']
        >>> Iter(lst).first()
        'a'

         Example 2:
        >>> lst = []
        >>> Iter(lst).first()
        Traceback (most recent call last):
        ...
        ValueError: Iter is empty.

         Example 3:
        >>> lst = ['a', 'b', 'c']
        >>> Iter(lst).first(lambda x: x == 'b')
        'b'

         Example 4:
        >>> lst = ['a', 'b', 'c']
        >>> Iter(lst).first(lambda x: x == 'd')
        Traceback (most recent call last):
        ...
        ValueError: Iter is empty.

         Example 5:
        >>> lst = [None]
        >>> Iter(lst).first() is None
        True
        """
        ...

    @overload
    def first(self, predicate: Callable[[T], bool]) -> T:
        ...

    def first(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        for e in self:
            if predicate is None or predicate(e):
                return e
        raise ValueError("Iter is empty.")
    
    def first_not_none_of(self, transform: Callable[[T], Optional[R]]) -> R:
        """
         Returns the first non-`None` result of applying the given [transform] function to each element in the original collection.

         Example 1:
        >>> lst = [{ 'name': 'A', 'age': None}, { 'name': 'B', 'age': 12}]
        >>> Iter(lst).first_not_none_of(lambda x: x['age'])
        12

         Example 2:
        >>> lst = [{ 'name': 'A', 'age': None}, { 'name': 'B', 'age': None}]
        >>> Iter(lst).first_not_none_of(lambda x: x['age'])
        Traceback (most recent call last):
        ...
        ValueError: No element of the Iter was transformed to a non-none value.
        """
        v = self.first_not_null_of_or_none(transform)
        if v is None:
            raise ValueError('No element of the Iter was transformed to a non-none value.')
        return v
    
    def first_not_null_of_or_none(self, transform: Callable[[T], Optional[R]]) -> Optional[R]:
        """
         Returns the first non-`None` result of applying the given [transform] function to each element in the original collection.

         Example 1:
        >>> lst = [{ 'name': 'A', 'age': None}, { 'name': 'B', 'age': 12}]
        >>> Iter(lst).first_not_null_of_or_none(lambda x: x['age'])
        12

         Example 2:
        >>> lst = [{ 'name': 'A', 'age': None}, { 'name': 'B', 'age': None}]
        >>> Iter(lst).first_not_null_of_or_none(lambda x: x['age']) is None
        True
        """
        return self.map_not_none(transform).first_or_none()

    @overload
    def first_or_none(self) -> Optional[T]:
        """
         Returns the first element, or `None` if the Iter is empty.

         Example 1:
        >>> lst = []
        >>> Iter(lst).first_or_none() is None
        True

         Example 2:
        >>> lst = ['a', 'b', 'c']
        >>> Iter(lst).first_or_none()
        'a'

         Example 2:
        >>> lst = ['a', 'b', 'c']
        >>> Iter(lst).first_or_none(lambda x: x == 'b')
        'b'
        """
        ...

    @overload
    def first_or_none(self, predicate: Callable[[T], bool]) -> Optional[T]:
        ...

    def first_or_none(self, predicate: Optional[Callable[[T], bool]] = None) -> Optional[T]:
        return next(iter(self if predicate is None else self.filter(predicate)), None)


    @overload
    def first_or_default(self, default: T) -> T :
        """
         Returns the first element, or the given [default] if the Iter is empty.

         Example 1:
        >>> lst = []
        >>> Iter(lst).first_or_default('a')
        'a'

         Example 2:
        >>> lst = ['b']
        >>> Iter(lst).first_or_default('a')
        'b'
        
         Example 3:
        >>> lst = ['a', 'b', 'c']
        >>> Iter(lst).first_or_default(lambda x: x == 'b', 'd')
        'b'

         Example 4:
        >>> lst = []
        >>> Iter(lst).first_or_default(lambda x: x == 'b', 'd')
        'd'
        """
        ...

    @overload
    def first_or_default(self, predicate: Callable[[T], bool], default: T) -> T :
        ...
    
    def first_or_default(self, predicate: Union[Callable[[T], bool], T], default: T) -> T:
        if isinstance(predicate, Callable):
            return self.first_or_none(predicate) or default
        else:
            default = predicate
        return self.first_or_none() or default

    @overload
    def last(self) -> T:
        """
         Returns last element.

         Example 1:
        >>> lst = ['a', 'b', 'c']
        >>> Iter(lst).last()
        'c'

         Example 2:
        >>> lst = []
        >>> Iter(lst).last()
        Traceback (most recent call last):
        ...
        ValueError: Iter is empty.
        """
        ...

    @overload
    def last(self, predicate: Callable[[T], bool]) -> T:
        ...

    def last(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        v = self.last_or_none(predicate)
        if v is None:
            raise ValueError('Iter is empty.')
        return v

    @overload
    def last_or_none(self) -> Optional[T]:
        """
         Returns the last element matching the given [predicate], or `None` if no such element was found.

         Exmaple 1:
        >>> lst = ['a', 'b', 'c']
        >>> Iter(lst).last_or_none()
        'c'

         Exmaple 2:
        >>> lst = ['a', 'b', 'c']
        >>> Iter(lst).last_or_none(lambda x: x != 'c')
        'b'

         Exmaple 3:
        >>> lst = []
        >>> Iter(lst).last_or_none(lambda x: x != 'c') is None
        True
        """
        ...

    @overload
    def last_or_none(self, predicate: Callable[[T], bool]) -> Optional[T]:
        ...

    def last_or_none(self, predicate: Optional[Callable[[T], bool]] = None) -> Optional[T]:
        last: Optional[T] = None
        for i in self if predicate is None else self.filter(predicate):
            last = i
        return last

    @overload
    def single(self) -> T:
        """
        Returns the single element matching the given [predicate], or throws exception if there is no
        or more than one matching element.

         Exmaple 1:
        >>> lst = ['a']
        >>> Iter(lst).single()
        'a'

         Exmaple 2:
        >>> lst = []
        >>> Iter(lst).single() is None
        Traceback (most recent call last):
        ...
        ValueError: Iter contains no element matching the predicate.

         Exmaple 2:
        >>> lst = ['a', 'b']
        >>> Iter(lst).single() is None
        Traceback (most recent call last):
        ...
        ValueError: Iter contains more than one matching element.

        """
        ...

    @overload
    def single(self, predicate: Callable[[T], bool]) -> T:
        ...

    def single(self, predicate: Optional[Callable[[T], bool]] = None) -> T:
        single: Optional[T] = None
        found = False
        for i in self if predicate is None else self.filter(predicate):
            if found:
                raise ValueError('Iter contains more than one matching element.')
            single = i
            found = True
        if not found:
            raise ValueError('Iter contains no element matching the predicate.')
        return single

    @overload
    def single_or_none(self) -> Optional[T]:
        """
         Returns the single element matching the given [predicate], or `None` if element was not found
        or more than one element was found.

         Exmaple 1:
        >>> lst = ['a']
        >>> Iter(lst).single_or_none()
        'a'

         Exmaple 2:
        >>> lst = []
        >>> Iter(lst).single_or_none() is None
        True

         Exmaple 2:
        >>> lst = ['a', 'b']
        >>> Iter(lst).single_or_none() is None
        True
        """
        ...

    @overload
    def single_or_none(self, predicate: Callable[[T], bool]) -> Optional[T]:
        ...

    def single_or_none(self, predicate: Optional[Callable[[T], bool]] = None) -> Optional[T]:
        single: Optional[T] = None
        found = False
        for i in self if predicate is None else self.filter(predicate):
            if found:
                return None
            single = i
            found = True
        if not found:
            return None
        return single

    # noinspection PyShadowingNames
    def drop(self, n: int) -> Iter[T]:
        """
         Returns a Iter containing all elements except first [n] elements.

         Example 1:
        >>> lst = ['a', 'b', 'c']
        >>> Iter(lst).drop(0)
        ['a', 'b', 'c']

         Example 2:
        >>> lst = ['a', 'b', 'c']
        >>> Iter(lst).drop(1)
        ['b', 'c']


         Example 2:
        >>> lst = ['a', 'b', 'c']
        >>> Iter(lst).drop(4)
        []
        """
        if n < 0:
            raise ValueError(f'Requested element count {n} is less than zero.')
        if n == 0:
            return self

        lst = []
        for i, e in enumerate(self):
            if i < n:
                continue
            lst.append(e)
        return Iter(lst)

    # noinspection PyShadowingNames
    def drop_while(self, predicate: Callable[[T], bool]) -> Iter[T]:
        """
         Returns a Iter containing all elements except first elements that satisfy the given [predicate].

         Example 1:
        >>> lst = [1, 2, 3, 4, 5]
        >>> Iter(lst).drop_while(lambda x: x < 3 )
        [3, 4, 5]
        """
        lst = []
        for e in self:
            if predicate(e):
                continue
            lst.append(e)
        return Iter(lst)

    def take(self, n: int) -> Iter[T]:
        """
         Returns an Iter containing first [n] elements.

         Example 1:
        >>> a = ['a', 'b', 'c']
        >>> Iter(a).take(0)
        []


         Example 2:
        >>> a = ['a', 'b', 'c']
        >>> Iter(a).take(2)
        ['a', 'b']

        """
        if n < 0:
            raise ValueError(f'Requested element count {n} is less than zero.')
        if n == 0:
            return Iter([])
        lst = []
        for i, e in enumerate(self, 1):
            lst.append(e)
            if i == n:
                break
        return Iter(lst)

    # noinspection PyShadowingNames
    def take_while(self, predicate: Callable[[T], bool]) -> Iter[T]:
        """
         Returns an Iter containing first elements satisfying the given [predicate].

         Example 1:
        >>> lst = ['a', 'b', 'c', 'd']
        >>> Iter(lst).take_while(lambda x: x in ['a', 'b'])
        ['a', 'b']

        """

        lst = []
        for e in self:
            if not predicate(e):
                break
            lst.append(e)

        return Iter(lst)

    # noinspection PyShadowingNames
    def sorted(self) -> Iter[T]:
        """
         Returns an Iter that yields elements of this Iter sorted according to their natural sort order.

         Example 1:
        >>> lst = ['b', 'a', 'e', 'c']
        >>> Iter(lst).sorted()
        ['a', 'b', 'c', 'e']

         Example 2:
        >>> lst = [2, 1, 4, 3]
        >>> Iter(lst).sorted()
        [1, 2, 3, 4]
        """
        lst = list(self)
        lst.sort()
        return Iter(lst)

    # noinspection PyShadowingNames
    def sorted_by(self, key_selector: Callable[[T], R]) -> Iter[T]:
        """
         Returns a sequence that yields elements of this sequence sorted according to natural sort
        order of the value returned by specified [key_selector] function.

         Example 1:
        >>> lst = [ {'name': 'A', 'age': 12 }, {'name': 'C', 'age': 10 }, {'name': 'B', 'age': 11 } ]
        >>> Iter(lst).sorted_by(lambda x: x['name'])
        [{'name': 'A', 'age': 12}, {'name': 'B', 'age': 11}, {'name': 'C', 'age': 10}]
        >>> Iter(lst).sorted_by(lambda x: x['age'])
        [{'name': 'C', 'age': 10}, {'name': 'B', 'age': 11}, {'name': 'A', 'age': 12}]

        """
        lst = list(self)
        lst.sort(key=key_selector)
        return Iter(lst)

    def sorted_descending(self) -> Iter[T]:
        """
         Returns a Iter of all elements sorted descending according to their natural sort order.

         Example 1:
        >>> lst = ['b', 'c', 'a']
        >>> Iter(lst).sorted_descending()
        ['c', 'b', 'a']
        """
        return self.sorted().reversed()

    def sorted_by_descending(self, key_selector: Callable[[T], R]) -> Iter[T]:
        """
         Returns a sequence that yields elements of this sequence sorted descending according
        to natural sort order of the value returned by specified [key_selector] function.

         Example 1:
        >>> lst = [ {'name': 'A', 'age': 12 }, {'name': 'C', 'age': 10 }, {'name': 'B', 'age': 11 } ]
        >>> Iter(lst).sorted_by_descending(lambda x: x['name'])
        [{'name': 'C', 'age': 10}, {'name': 'B', 'age': 11}, {'name': 'A', 'age': 12}]
        >>> Iter(lst).sorted_by_descending(lambda x: x['age'])
        [{'name': 'A', 'age': 12}, {'name': 'B', 'age': 11}, {'name': 'C', 'age': 10}]
        """
        return self.sorted_by(key_selector).reversed()

    # noinspection PyShadowingNames
    def sorted_with(self, comparator: Callable[[T, T], int]) -> Iter[T]:
        """
         Returns a sequence that yields elements of this sequence sorted according to the specified [comparator].

        Example 1:
        >>> lst = ['aa', 'bbb', 'c']
        >>> Iter(lst).sorted_with(lambda a, b: len(a)-len(b))
        ['c', 'aa', 'bbb']
        """
        from functools import cmp_to_key
        lst = list(self)
        lst.sort(key=cmp_to_key(comparator))
        return Iter(lst)

    def associate(self, transform: Callable[[T], Tuple[K, V]]) -> Dict[K, V]:
        """
         Returns a [Dict] containing key-value Tuple provided by [transform] function
        applied to elements of the given Iter.

         Example 1:
        >>> lst = ['1', '2', '3']
        >>> Iter(lst).associate(lambda x: (int(x), x))
        {1: '1', 2: '2', 3: '3'}

        """
        dic = dict()
        for i in self:
            k, v = transform(i)
            dic[k] = v
        return dic

    @overload
    def associate_by(self, key_selector: Callable[[T], K]) -> Dict[K, T]:
        """
         Returns a [Dict] containing key-value Tuple provided by [transform] function
        applied to elements of the given Iter.

         Example 1:
        >>> lst = ['1', '2', '3']
        >>> Iter(lst).associate_by(lambda x: int(x))
        {1: '1', 2: '2', 3: '3'}

         Example 2:
        >>> lst = ['1', '2', '3']
        >>> Iter(lst).associate_by(lambda x: int(x), lambda x: x+x)
        {1: '11', 2: '22', 3: '33'}

        """
        ...

    @overload
    def associate_by(self, key_selector: Callable[[T], K], value_transform: Callable[[T], V]) -> Dict[K, V]:
        ...

    def associate_by(self, key_selector: Callable[[T], K],
                     value_transform: Optional[Callable[[T], V]] = None) -> Dict[K, Union[V, T]]:
        dic = dict()
        for i in self:
            k = key_selector(i)
            dic[k] = i if value_transform is None else value_transform(i)
        return dic

    @overload
    def associate_by_to(self, destination: Dict[K, T], key_selector: Callable[[T], K]) -> Dict[K, T]:
        """
         Returns a [Dict] containing key-value Tuple provided by [transform] function
        applied to elements of the given Iter.

         Example 1:
        >>> lst = ['1', '2', '3']
        >>> Iter(lst).associate_by_to({}, lambda x: int(x))
        {1: '1', 2: '2', 3: '3'}

         Example 2:
        >>> lst = ['1', '2', '3']
        >>> Iter(lst).associate_by_to({}, lambda x: int(x), lambda x: x+'!' )
        {1: '1!', 2: '2!', 3: '3!'}

        """
        ...

    @overload
    def associate_by_to(self, destination: Dict[K, V], key_selector: Callable[[T], K],
                        value_transform: Callable[[T], V]) -> Dict[K, V]:
        ...

    def associate_by_to(self, destination: Dict[K, V], key_selector: Callable[[T], K],
                        value_transform: Optional[Callable[[T], V]] = None) -> Dict[K, Union[V, T]]:
        for i in self:
            k = key_selector(i)
            destination[k] = i if value_transform is None else value_transform(i)
        return destination
    
    def all(self, predicate: Callable[[T], bool]) -> bool:
        """
         Returns True if all elements of the Iter satisfy the specified [predicate] function.

         Example 1:
        >>> lst = [1, 2, 3]
        >>> Iter(lst).all(lambda x: x > 0)
        True
        >>> Iter(lst).all(lambda x: x > 1)
        False

        """
        for i in self:
            if not predicate(i):
                return False
        return True
    
    def any(self, predicate: Callable[[T], bool]) -> bool:
        """
         Returns True if any elements of the Iter satisfy the specified [predicate] function.

         Example 1:
        >>> lst = [1, 2, 3]
        >>> Iter(lst).any(lambda x: x > 0)
        True
        >>> Iter(lst).any(lambda x: x > 3)
        False

        """
        for i in self:
            if predicate(i):
                return True
        return False
    
    def count(self, predicate: Optional[Callable[[T], bool]] = None) -> int:
        """
         Returns the number of elements in the Iter that satisfy the specified [predicate] function.

         Example 1:
        >>> lst = [1, 2, 3]
        >>> Iter(lst).count()
        3
        >>> Iter(lst).count(lambda x: x > 0)
        3
        >>> Iter(lst).count(lambda x: x > 2)
        1

        """
        if predicate is None:
            return len(self)
        return sum(1 for i in self if predicate(i))
    
    def contains(self, value: T) -> bool:
        """
         Returns True if the Iter contains the specified [value].

         Example 1:
        >>> lst = [1, 2, 3]
        >>> Iter(lst).contains(1)
        True
        >>> Iter(lst).contains(4)
        False

        """
        return value in self
    
    def distinct(self) -> Iter[T]:
        """
         Returns a new Iter containing the distinct elements of the given Iter.

         Example 1:
        >>> lst = [1, 2, 3, 1, 2, 3]
        >>> Iter(lst).distinct()
        [1, 2, 3]

        """
        return Iter(set(self))
    
    def distinct_by(self, key_selector: Callable[[T], K]) -> Iter[T]:
        """
         Returns a new Iter containing the distinct elements of the given Iter.

         Example 1:
        >>> lst = [1, 2, 3, 1, 2, 3]
        >>> Iter(lst).distinct_by(lambda x: x%2)
        [3, 2]

        """
        return Iter(self.associate_by(key_selector).values())
    
    def reduce(self, accumulator: Callable[[T, T], T], initial: Optional[T] = None) -> T:
        """
         Returns the result of applying the specified [accumulator] function to the given Iter's elements.

         Example 1:
        >>> lst = [1, 2, 3]
        >>> Iter(lst).reduce(lambda x, y: x+y)
        6

        """
        result = initial
        for i, e in enumerate(self):
            if i == 0 and initial is None:
                result = e
                continue
            result = accumulator(result, e)
        return result
    
    def fold(self, initial: R, accumulator: Callable[[R, T], T]) -> R:
        """
         Returns the result of applying the specified [accumulator] function to the given Iter's elements.

         Example 1:
        >>> lst = [1, 2, 3]
        >>> Iter(lst).fold(0, lambda x, y: x+y)
        6

        """
        return self.reduce(accumulator, initial)
    
    @overload
    def sum_of(self, selector: Callable[[T], int]) -> int:
        """
         Returns the sum of the elements of the given Iter.

         Example 1:
        >>> lst = [1, 2, 3]
        >>> Iter(lst).sum_of(lambda x: x)
        6

        """
        ...
    @overload
    def sum_of(self, selector: Callable[[T], float]) -> float:
        ...
    def sum_of(self, selector: Callable[[T], Union[int, float]]) -> Union[int, float]:
        return sum(selector(i) for i in self)
    
    @overload
    def max_of(self, selector: Callable[[T], int]) -> int:
        """
         Returns the maximum element of the given Iter.

         Example 1:
        >>> lst = [1, 2, 3]
        >>> Iter(lst).max_of(lambda x: x)
        3

        """
        ...
    @overload
    def max_of(self, selector: Callable[[T], float]) -> float:
        ...
    def max_of(self, selector: Callable[[T], Union[int, float]]) -> Union[int, float]:
        return max(selector(i) for i in self)
    
    @overload
    def min_of(self, selector: Callable[[T], int]) -> int:
        """
         Returns the minimum element of the given Iter.

         Example 1:
        >>> lst = [1, 2, 3]
        >>> Iter(lst).min_of(lambda x: x)
        1

        """
        ...
    @overload
    def min_of(self, selector: Callable[[T], float]) -> float:
        ...
    def min_of(self, selector: Callable[[T], Union[int, float]]) -> Union[int, float]:
        return min(selector(i) for i in self)
    

    # noinspection PyShadowingNames
    def reversed(self) -> Iter[T]:
        """
         Returns a list with elements in reversed order.

         Example 1:
        >>> lst = ['b', 'c', 'a']
        >>> Iter(lst).reversed()
        ['a', 'c', 'b']
        """
        lst = list(self)
        lst.reverse()
        return Iter(lst)

    def flat_map(self, transform: Callable[[T], Iter[R]]) -> Iter[R]:
        """
         Returns a single list of all elements yielded from results of [transform]
        function being invoked on each element of original collection.

         Example 1:
        >>> lst = [['a', 'b'], ['c'], ['d', 'e']]
        >>> Iter(lst).flat_map(lambda x: x)
        ['a', 'b', 'c', 'd', 'e']
        """
        import itertools
        return Iter(itertools.chain.from_iterable(map(transform, self)))

    def foreach(self, action: Callable[[T], None]) -> None:
        """
         Invokes [action] function on each element of the given Iter.

         Example 1:
        >>> lst = ['a', 'b', 'c']
        >>> Iter(lst).foreach(lambda x: print(x))
        a
        b
        c
        """
        for i in self:
            action(i)

    def to_set(self) -> Set[T]:
        """
         Returns a set containing all elements of this Iter.

         Example 1:
        >>> Iter(['a', 'b', 'c', 'c']).to_set() == {'a', 'b', 'c'}
        True
        """
        return set(self)

    def to_dict(self, transform: Callable[[T], Tuple[K, V]]) -> Dict[K, V]:
        """
         Returns a [Dict] containing key-value Tuple provided by [transform] function
        applied to elements of the given Iter.

         Example 1:
        >>> lst = ['1', '2', '3']
        >>> Iter(lst).to_dict(lambda x: (int(x), x))
        {1: '1', 2: '2', 3: '3'}

        """
        return self.associate(transform)

    def to_list(self) -> List[T]:
        """
         Returns a list with elements of the given Iter.

         Example 1:
        >>> Iter(['b', 'c', 'a']).to_list()
        ['b', 'c', 'a']
        """
        return list(self)
    
    def __len__(self) -> int:
        return len(self._iter)

    def __repr__(self) -> str:
        return str(self.to_list())

    def __iter__(self) -> Iterator[T]:
        return iter(self._iter)


def it(iterable: Iterable[T]) -> Iter[T]:
    """
     Returns an Iter with elements of the given Iterable.

     Example 1:
    >>> it(['a', 'b', 'c'])
    ['a', 'b', 'c']
    """
    return Iter(iterable)

if __name__ == "__main__":
    import doctest

    doctest.testmod()

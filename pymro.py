from typing import Any, Dict, Callable, Iterable, List
from functools import partial


class BadInheritanceError(Exception):
    pass


def linearize(cls: str, bases: Dict[str, List[str]]) -> List[str]:
    if cls not in bases:
        return [cls]
    return list(merge([[cls]] + list(map(partial(linearize, bases=bases), bases[cls])) + [bases[cls]]))


def merge(l_seqs: List[List[str]]) -> Iterable[str]:
    for seq in l_seqs:
        h = head(seq)

        if if_any(lambda x: h in tail(x), l_seqs) >= 0:
            continue

        l_seqs = list(filter_map(lambda x: tail(x) if x[0] == h else x, is_not_empty, l_seqs))
        yield h
        break
    else:
        raise BadInheritanceError('Bad inheritance')

    if len(l_seqs) > 0:
        yield from merge(l_seqs)


# ************** helper functions *****************

def tail(lst: List[Any]) -> List[Any]:
    return lst[1:]


def head(lst: List[Any]) -> Any:
    return lst[0]


def is_empty(lst: List[Any]) -> bool:
    return len(lst) == 0


def is_not_empty(lst: List[Any]) -> bool:
    return not is_empty(lst)


def if_any(func: Callable[[Any], bool], iter1: Iterable[Any]) -> int:
    for i, item in enumerate(iter1):
        if func(item) is True:
            return i
    return -1


def filter_map(func_map: Callable[[Any], Any],
               func_filter: Callable[[Any], bool],
               iter1: Iterable[Any]) -> Iterable[Any]:
    for item in iter1:
        val = func_map(item)
        if func_filter(val) is True:
            yield val


def take_if(func: Callable[[Any], bool], iter1: Iterable[Any]) -> Iterable[Any]:
    for item in iter1:
        if func(item) is True:
            yield item


if __name__ == '__main__':
    try:
        mro = linearize('A', {
            'F': ['O'],
            'E': ['O'],
            'D': ['O'],
            'C': ['D', 'F'],
            'B': ['D', 'E'],
            'A': ['B', 'C'],
        })
    except BadInheritanceError as e:
        print(e)
    else:
        print(mro)

    try:
        mro = linearize('A', {
            'F': ['O'],
            'E': ['O'],
            'D': ['O'],
            'C': ['D', 'F'],
            'B': ['E', 'D'],
            'A': ['B', 'C'],
        })
    except BadInheritanceError as e:
        print(e)
    else:
        print(mro)

    try:
        mro = linearize('A', {
            'F': ['O'],
            'E': ['O'],
            'D': ['O'],
            'C': ['D', 'E'],
            'B': ['E', 'D'],
            'A': ['B', 'C'],
        })
    except BadInheritanceError as e:
        print(e)
    else:
        print(mro)

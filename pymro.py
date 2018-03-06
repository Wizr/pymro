from typing import Any, Dict, Callable, Iterable, List, Tuple
from functools import partial


def linearize(cls: str, bases: Dict[str, List[str]]) -> List[str]:
    if cls not in bases:
        return [cls]
    l_bases = list(map(lambda key: linearize(key, bases), bases[cls]))
    l_bases.append(bases[cls])
    return [cls] + list(merge(*l_bases))


def merge(*l_seqs: List[List[str]]) -> Iterable[str]:
    for i, seq in enumerate(l_seqs):
        h = head(seq)
        l_rest = list(take_if(lambda x: x[0] != i, enumerate(l_seqs)))

        if if_any(lambda x: h in tail(x[1]), l_rest) >= 0:
            continue

        l_seqs = list(filter_map(lambda x: partial(cut_head, h)(x), l_seqs))
        yield h
        break
    else:
        raise Exception('Bad inheritance')

    if len(l_seqs) > 0:
        yield from merge(*l_seqs)


# こわい
def cut_head(hd: str, lst: List[str]):
    if hd == lst[0]:
        if len(lst) == 1:
            return False, None
        else:
            return True, lst[1:]
    else:
        return True, lst


# ************** helper functions *****************

def tail(lst: List[Any]) -> List[Any]:
    return lst[1:] if len(lst) > 1 else []


def head(lst: List[Any]) -> Any:
    return lst[0]


def if_any(func: Callable[[Any], bool], iter1: Iterable[Any]) -> int:
    for item in iter1:
        if func(item) is True:
            return item[0]
    return -1


def filter_map(func: Callable[[Any], Tuple[bool, Any]], iter1: Iterable[Any]) -> Iterable[Any]:
    for item in iter1:
        ok, val = func(item)
        if ok is True:
            yield val


def take_if(func: Callable[[Any], bool], iter1: Iterable[Any]) -> Iterable[Any]:
    for item in iter1:
        if func(item) is True:
            yield item


if __name__ == '__main__':
    mro = linearize('A', {
        'F': ['O'],
        'E': ['O'],
        'D': ['O'],
        'C': ['D', 'F'],
        'B': ['D', 'E'],
        'A': ['B', 'C'],
    })
    print(mro)

    mro = linearize('A', {
        'F': ['O'],
        'E': ['O'],
        'D': ['O'],
        'C': ['D', 'F'],
        'B': ['E', 'D'],
        'A': ['B', 'C'],
    })
    print(mro)

    mro = linearize('A', {
        'F': ['O'],
        'E': ['O'],
        'D': ['O'],
        'C': ['D', 'E'],
        'B': ['E', 'D'],
        'A': ['B', 'C'],
    })
    print(mro)

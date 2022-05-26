from typing import List
from .formats.position import Position


def update_deep(source: dict, other: dict, *no_dict_key) -> None:
    for k, v in other.items():
        if k not in source or not isinstance(v, dict) or k in no_dict_key:
            try:
                source[k] = v.copy()
            except AttributeError:
                source[k] = v
        else:
            source_copy = source[k].copy()
            update_deep(source_copy, v, *no_dict_key)
            source[k] = source_copy


def in_bound(feature: dict, bound: List[float], **kwargs) -> bool:
    return Position(feature['geometry']['coordinates']).in_bound(bound)


if __name__ == '__main__':
    a = {'a': 1, 'b': {'test': 1, 'lolo': 2}}
    b = {'a': 2, 'c': 4, 'b': {'lolo': 'ok'}}
    update_deep(a, b)
    print(a)

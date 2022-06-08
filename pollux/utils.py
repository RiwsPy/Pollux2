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


def in_bound(feature: dict, position__within: List[float], **kwargs) -> bool:
    return Position(feature['geometry']['coordinates']).in_bound(position__within)


def linestring_to_polygon(line: List[List[float]], width: float) -> List[List[List[Position]]]:
    if width < 0.0:
        raise ValueError

    for position1, position2 in Position(line).iter_pos():
        if position1 == position2:
            continue
        position1 = Position(position1)
        position2 = Position(position2)
        orientation = position1.orientation(position2)
        p0 = position1.projection(distance=width / 2, orientation=orientation + 270)
        p1 = position1.projection(distance=width / 2, orientation=orientation + 90)
        p2 = position2.projection(distance=width / 2, orientation=orientation + 90)
        p3 = position2.projection(distance=width / 2, orientation=orientation + 270)
        return [[p0, p1, p2, p3, p0]]

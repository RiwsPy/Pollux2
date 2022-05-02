from . import Default_works
from formats.position import Position


class Works(Default_works):
    filename = 'highways'
    COPYRIGHT_LICENSE = 'ODbL'
    fake_request = True

    def _can_be_output(self, obj: Default_works.Model, bound=None, **kwargs) -> bool:
        if obj['geometry']:
            bound = bound or self.bound
            for lines in obj.position:
                if type(lines[0]) is list:
                    for position in lines:
                        if Position(position).in_bound(bound):
                            return True
                else:
                    position = lines
                    if Position(position).in_bound(bound):
                        return True
        return False

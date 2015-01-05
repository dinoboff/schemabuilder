import collections


def _to_camel_case(s):
    """Convert a property attribute name to camel case.

    """
    return s[0] + s.title().replace("_", "")[1:]


class ToDictMixin(object):
    """Convert the object properties to a dictionary.

    Recursively walks the dict and sequences properties to convert them.

    """
    def to_dict(self):
        """Return the schema as a `dict`, ready to be serialized by
        :mod:`json`.

        """
        result = {}
        stack = collections.deque()
        stack.append(
            (
                result,
                {_to_camel_case(k): v for k, v in self.__dict__.iteritems()},
            )
        )
        while stack:
            dest, source = stack.pop()
            if isinstance(dest, dict):
                self._process_dict(dest, source, stack)
            else:
                self._process_list(dest, source, stack)
        return result

    @staticmethod
    def _process_dict(dest, source, stack):
        for k, v in source.iteritems():
            if v is None or k[0] == "_":
                continue
            if isinstance(v, dict):
                dest[k] = {}
                stack.append((dest[k], v,))
            elif isinstance(v, (list, tuple,)):
                dest[k] = []
                stack.append((dest[k], v,))
            elif hasattr(v, "to_dict"):
                dest[k] = v.to_dict()
            else:
                dest[k] = v

    @staticmethod
    def _process_list(dest, source, stack):
        for v in source:
            if v is None:
                continue

            if isinstance(v, dict):
                dest.append({})
                stack.append((dest[-1], v,))
            if isinstance(v, (list, tuple,)):
                dest.append([])
                stack.append((dest[-1], v,))
            elif hasattr(v, "to_dict"):
                dest.append(v.to_dict())
            else:
                dest.append(v)

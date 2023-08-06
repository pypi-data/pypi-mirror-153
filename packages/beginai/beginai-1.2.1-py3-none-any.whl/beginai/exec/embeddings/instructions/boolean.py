class Boolean(object):

    def __init__(self, true, false, _GB_EMPTY):
        self.true = true
        self.false = false
        self._GB_EMPTY = _GB_EMPTY

    def apply(self, value):
        if value is None and value != 0:
            return self._GB_EMPTY

        if value == True or str(value).lower() == "true":
            return self.true
        return self.false

instructions_map = {
    "Boolean": Boolean
}

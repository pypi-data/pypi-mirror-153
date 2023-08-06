class Sequence(object):

    def __init__(self, sequence_map: dict):
        self.seq_map = sequence_map

    def apply(self, value):
        # sequence dict keys are always strings.
        if value is None or value == '':
            # handle empty values
            return self.seq_map.get(str("_GB_EMPTY"))
        return self.seq_map.get(str(value).lower())

instructions_map = {
    "Sequence": Sequence
}

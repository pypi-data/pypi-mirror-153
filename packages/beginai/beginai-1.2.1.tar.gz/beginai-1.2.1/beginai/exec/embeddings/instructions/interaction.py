
class InteractionEncoding(object):

    def __init__(self, sequence_map: dict):
        self.seq_map = sequence_map

    def apply(self, values):
        empty_value = float(self.seq_map.get("_GB_EMPTY"))

        values = list(dict.fromkeys(values))

        parsed_values = []

        for action in self.seq_map:
            if action != '_GB_EMPTY':
                if action in values:
                    parsed_values.append(self.seq_map.get(action))
                else:
                    parsed_values.append(empty_value)

        highest_interaction = max(parsed_values)
        label = 'POSITIVE'

        if highest_interaction == empty_value or highest_interaction == 4:
            label = 'NEUTRAL'
        elif highest_interaction < 4:
            label = 'NEGATIVE'

        return {
            'sent_bin': 2 if highest_interaction > 4 else 1,
            'sentiment': highest_interaction,
            'label': label
        }


instructions_map = {
    "InteractionEncoding": InteractionEncoding
}

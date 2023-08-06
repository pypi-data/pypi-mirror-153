from .utils import sequence_encoder
from math import log

class Slice(object):
    def __init__(self, minv, maxv, num_slices):
        self.minv = minv
        self.maxv = maxv
        self.number_slices = num_slices

    def generate_bands_for_numerical_feature(self):
        """
        this function splits symetrically which means it can only split 2**
        i.e. 2,4,8,16,32,.. etc. slices.
        """
        slices = []
        def slice_one(minp, maxp):
            midpoint = int((minp + maxp) / 2)
            return [minp, midpoint], [midpoint, maxp]

        s1, s2 = slice_one(self.minv, self.maxv)
        slices.append(s1)
        slices.append(s2)

        num_splits = 1
        max_splits = log(self.number_slices, 2)
        while num_splits < max_splits:
            # slice the last one?
            # you have to slice ALL OF THEM.
            # meaning slices grow at a rate of 2 (power 2)
            # so if we want 16 slices that should be 4 splits. log(16) base 2.
            new_layer = slices.copy()
            for index, s in enumerate(slices):
                # replace the slice with its two halves
                s1, s2 = slice_one(s[0], s[1])
                del new_layer[new_layer.index(s)]

                new_layer.append(s1)
                new_layer.append(s2)

            slices = new_layer.copy()
            num_splits += 1

        return slices

    def find_my_position_in_numerical_band(self, my_number):
        all_slices = self.generate_bands_for_numerical_feature()
        slices_encoding = sequence_encoder(all_slices)

        # find index of range for my_number
        for i, s in enumerate(all_slices):
            
            # return if it belongs to current slice
            if my_number<=s[1] and my_number>=s[0]:
                return slices_encoding[i]
            
        # if values goes beyond maxv
        return len(slices_encoding) + 1 

    def apply(self, value):
        # force it to be a number
        value = float(value)
        return self.find_my_position_in_numerical_band(value)


class CompareToField(object):
    def __init__(self):
        pass

    def apply(self, value, compare_to_field_value):
        try:
            return int(value) == int(compare_to_field_value)
        except ValueError:
            return False


class CompareToNumber(object):
    def __init__(self, compare_to_number):
        self.compare_to_number = compare_to_number

    def apply(self, value):
        return value == self.compare_to_number


instructions_map = {
    "Slice": Slice,
    "CompareToField": CompareToField,
    "CompareToNumber": CompareToNumber
}

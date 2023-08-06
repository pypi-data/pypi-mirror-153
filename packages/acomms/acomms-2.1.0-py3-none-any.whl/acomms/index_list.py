from collections import UserList

class IndexList(UserList):
    ''' Class to contain list of start/end index pairs'''
    def __init__(self, index_list=None):
        if index_list is not None:
            if not any(isinstance(i, list) for i in index_list):
                if len(index_list) == 2:
                    self.data = [index_list]
                elif len(index_list) == 0:
                    self.data = []
                else:
                    raise Exception('index_list argument must be one or more [start,end] index pairs')
            elif all(isinstance(i, list) for i in index_list) and all((len(i) == 2) for i in index_list):
                self.data = index_list
            else:
                raise Exception('index_list argument must be one or more [start,end] index pairs')
        else:
            self.data = []

    @classmethod
    def from_list(cls, flatlist):
        data = []

        # Opposite of flat, takes a flat list and turns it into 2d index list
        if len(flatlist) % 2:
            raise Exception('list argument must have even number of entry pairs')

        for i in range(0, len(flatlist), 2):
            if flatlist[i] > flatlist[i+1]:
                raise Exception('list argument must be in ordered start:end pairs')

            data.append([flatlist[i], flatlist[i+1]])

        return cls(data)

    @property
    def flat(self):
        flat = []
        for pair in self.data:
            flat.append(pair[0])
            flat.append(pair[1])

        if len(flat) % 2:
            raise Exception('IndexList has odd number of elements')

        return flat

    def append(self, items):
        #If list is a list of multiple start/end pairs
        if all(isinstance(i, list) for i in items):
            for i in items:
                if len(i) != 2:
                    raise Exception('list argument must be one or more [start,end] index pairs')
                self._safe_append(i)
        else:
            if len(items) != 2:
                raise Exception('list argument must be one or more [start,end] index pairs')
            self._safe_append(items)

    def _safe_append(self, new_index):
        self.simplify()

        expanded = self._expand()
        expanded = expanded + list(range(new_index[0], new_index[-1]))
        self.data = self._contract(expanded)

    def inverse(self, limits):
        if any(isinstance(i, list) for i in limits):
            raise Exception('Limits cannot be nested list')
        if len(limits) != 2:
            raise Exception('Limits must be single [start,end] pair')

        inverse_index = []

        self.sort()

        #Check empty
        if not self.data:
            inverse_index = limits
        else:
            # Check beginning
            if self.data[0][0] > limits[0]:
                inverse_index.append([limits[0], self.data[0][0]])

            # Check middle
            if len(self.data) > 1:
                for i in range(len(self.data) - 2):
                    inverse_index.append([self.data[i][-1], self.data[i+1][0]])

            # Check end
            if self.data[-1][-1] < limits[-1]:
                inverse_index.append([self.data[-1][-1], limits[-1]])

        self._simplify(inverse_index)

        return inverse_index

    def simplify(self):
        if len(self.data) > 0:
            self.data = self._simplify(self.data)

        return self.data

    def _simplify(self, index_list):
        i = 0

        index_list.sort()

        while i < len(index_list) - 1:
            a = index_list[i][0]
            b = index_list[i][-1]
            c = index_list[i + 1][0]
            d = index_list[i + 1][-1]
            if b == c:
                index_list[i:i + 2] = [[a, d]]
            else:
                i = i + 1

        return index_list

    def _expand(self):
        expanded = []

        for index in self.data:
            expanded = expanded + list(range(index[0], index[1]))

        return expanded

    def _ranges(self, nums):
        nums = sorted(set(nums))
        gaps = [[s+1, e] for s, e in zip(nums, nums[1:]) if s + 1 < e]
        begin = nums[:1]
        end = [nums[-1:][0]+1]
        edges = iter(begin + sum(gaps, []) + end)

        return list(map(list, zip(edges, edges)))

    def _contract(self, expanded_form):
        expanded_form.sort()

        expanded_form = list(dict.fromkeys(expanded_form))

        return self._ranges(expanded_form)


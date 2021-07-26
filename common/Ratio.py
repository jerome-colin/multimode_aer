import numpy as np


class Ratio:

    def __init__(self, step):
        # Moche, mais fonctionne
        bound_min = 0
        bound_max = 1 + step
        self.list = []
        for a in np.arange(bound_min, bound_max, step):
            for b in np.arange(bound_min, bound_max, step):
                for c in np.arange(bound_min, bound_max, step):
                    for d in np.arange(bound_min, bound_max, step):
                        for e in np.arange(bound_min, bound_max, step):
                            for f in np.arange(bound_min, bound_max, step):
                                for g in np.arange(bound_min, bound_max, step):
                                    if (a + b + c + d + e + f + g) == 1:
                                        self.list.append([a, b, c, d, e, f, g])


it_list = Ratio(0.25)
print(it_list.list)
print(len(it_list.list))

import numpy as np

def get_ratio_7species(step):
    # Moche, mais fonctionne
    bound_min = 0
    bound_max = 1 + step
    list = []
    for a in np.arange(bound_min, bound_max, step):
        for b in np.arange(bound_min, bound_max, step):
            for c in np.arange(bound_min, bound_max, step):
                for d in np.arange(bound_min, bound_max, step):
                    for e in np.arange(bound_min, bound_max, step):
                        for f in np.arange(bound_min, bound_max, step):
                            for g in np.arange(bound_min, bound_max, step):
                                if (a + b + c + d + e + f + g) == 1:
                                    list.append([a, b, c, d, e, f, g])

    return list


it_list = get_ratio_7species(0.25)
print(it_list)
print(len(it_list))




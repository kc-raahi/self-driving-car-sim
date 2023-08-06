import random

from refactor.constants import SENSOR_ANGLES
from refactor.utils import mutate_value


class WLT:
    def __init__(self, wts=None, hi_t=None, lo_t=None):
        if wts is not None:
            self.wts = wts
        else:
            self.wts = [random.random() * 2 - 1 for i in range(len(SENSOR_ANGLES))]
        if hi_t is not None:
            self.hi_t = hi_t
        else:
            self.hi_t = random.random() * 2 - 1
        if lo_t is not None:
            self.lo_t = lo_t
        else:
            self.lo_t = random.random() * 2 - 1

        if self.lo_t > self.hi_t:
            tmp = self.hi_t
            self.hi_t = self.lo_t
            self.lo_t = tmp

    def __str__(self):
        return f"{self.lo_t, self.hi_t, self.wts}"

    def feed_fwd(self, inputs):
        weighted_sum, sum_weights = 0, 0
        for i, o in enumerate(inputs):
            weighted_sum += o * self.wts[i]
            sum_weights += self.wts[i]

        v = weighted_sum / sum_weights
        v = -1 if v < self.lo_t else 1 if v > self.hi_t else 0
        return v

    def mutate(self, max_perturb=1):
        wts = [mutate_value(w, max_perturb) for w in self.wts]
        m_hi = mutate_value(self.hi_t, max_perturb)
        m_lo = mutate_value(self.lo_t, max_perturb)
        return WLT(wts, m_hi, m_lo)


class Level:
    def __init__(self, wlt_arr):
        self.wlt_arr = wlt_arr

    def __str__(self):
        return f"{self.wlt_arr}"

    def feed_fwd(self, inputs):
        return [w.feed_fwd(inputs) for w in self.wlt_arr]

    def mutate(self, max_perturb=1):
        wlt_arr = [w.mutate(max_perturb) for w in self.wlt_arr]
        return Level(wlt_arr)


class NeuralNetwork:
    def __init__(self, level_arr):
        self.level_arr = level_arr

    def __str__(self):
        s = ""
        for lv in self.level_arr:
            s += lv + "\n"

    def feed_fwd(self, inputs):
        curr_inputs = inputs
        for level in self.level_arr:
            curr_inputs = level.feed_fwd(curr_inputs)
        return curr_inputs

    def mutate(self, max_perturb=1):
        level_arr = [lv.mutate(max_perturb) for lv in self.level_arr]
        return NeuralNetwork(level_arr)

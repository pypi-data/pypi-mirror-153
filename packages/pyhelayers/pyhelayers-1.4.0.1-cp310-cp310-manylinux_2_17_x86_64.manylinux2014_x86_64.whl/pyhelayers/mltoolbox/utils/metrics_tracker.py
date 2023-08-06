import pandas as pd

class MetricsTracker:
    def __init__(self, *metrics, mode):
        self.metrics = metrics
        self.mode = mode
        self._df = pd.DataFrame(index=metrics, columns=['total', 'num'])
        self.reset()

    def get_avg(self, key):
        return self._df.total[key] / self._df.num[key]
    
    
    def reset(self):
        for col in self._df.columns:
            self._df[col].values[:] = 0

    def update(self, key, value):
        self._df.total[key] += value
        self._df.num[key] += 1
    
    def update_all(self, values_dict):
        for key in values_dict:
            self.update(key, values_dict[key])

    
    def print_all(self):
        s = ''
        d = dict(self._df.avg)
        for key in d:
            s += "{} {:.4f}\t".format(key, d[key])

        return s


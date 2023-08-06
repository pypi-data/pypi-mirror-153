import multiprocessing

import tqdm


class parallel_tqdm(tqdm.tqdm):

    def __init__(self, *args):
        super(parallel_tqdm, self).__init__(*args)
        self.correct_count = multiprocessing.Value('i', 0)

    def update(self, n=1):
        with self.correct_count.get_lock():
            self.n = self.correct_count.value
            super(parallel_tqdm, self).update(n)
            self.correct_count.value += n

    def close(self):
        if self.disable:
            return
        self.n = self.correct_count.value
        super(parallel_tqdm, self).close()


if __name__ == '__main__':
    a = range(1000)
    with parallel_tqdm(a) as pbar:
        for i in a:
            pbar.update()
    pbar.close()

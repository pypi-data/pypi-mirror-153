import numpy as np
import os

def esm_download():
    pass

class esm_mean:
    def __init__(self,seqs=None):
        esm_download()
        self.esm_mean = None
    
    def __getitem__(self,index):
        if self.esm_mean == None:
            self.esm_mean = np.load(f"{os.environ['HOME']}/.local/zzd/lib/esm_mean.pkl", allow_pickle=True)
        return self.esm_mean[index]

if __name__ == "__main__":
    test = esm_mean()['AT3G17090']
    print(test,test.shape)

import numpy as np
import os

def ara_node2vec_init():
    zzd_lib = f"{os.environ['HOME']}/.local/zzd/lib"
    if not os.path.exists(zzd_lib):
        os.system(f"mkdir -p {zzd_lib}")

    if not os.path.exists(f"{zzd_lib}/ara_node2vec_feature.txt"):
        os.system(f"wget https://github.com/miderxi/zzd_lib/raw/main/zzd/lib/ara_node2vec_feature.tar.gz\
            -O {zzd_lib}/ara_node2vec_feature.tar.gz")
        os.system(f"tar -xvf {zzd_lib}/ara_node2vec_feature.tar.gz -C {zzd_lib}")

class ara_node2vec:
    def __init__(self):
        zzd_lib = f"{os.environ['HOME']}/.local/zzd/lib"
        ara_node2vec_init()
        self.node2vec = {line[0]:np.array(line[1:],float) 
                for line in np.genfromtxt(f"{zzd_lib}/ara_node2vec_feature.txt",str,skip_header=1)}     
    
    def __getitem__(self,index):
        if index in self.node2vec.keys():
            v =  self.node2vec[index]
        else:
            v = np.zeros(128)
        return v




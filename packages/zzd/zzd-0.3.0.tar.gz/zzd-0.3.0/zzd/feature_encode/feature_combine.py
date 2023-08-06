import numpy as np
from zzd.feature_encode.ac import ac
from zzd.feature_encode.dpc import dpc
from zzd.feature_encode.ct import ct
from zzd.feature_encode.cksaap import cksaap
from zzd.feature_encode.ara_node2vec import ara_node2vec 
from zzd.feature_encode.esm_mean import esm_mean 
from zzd.feature_encode.pdb2dpc import pdb2dpc_dict
#from ara2vec import ara2vec
#from dmi2vec import dmi2vec

class feature_combine:
    def __init__(self,a_features, b_features,seqs,pdb2dpc_file=None):
        self.features = {
                "ac":ac,
                "dpc":dpc,
                "ct":ct,
                "cksaap":cksaap,
                "esm_mean":esm_mean(),
                "ara2vec":ara_node2vec(),
                "pdb2dpc":pdb2dpc_dict(pdb2dpc_file)
                }
        self.feature_shape = {
                "ac":210,
                "dpc":400,
                "ct":343,
                "cksaap":1600,
                "esm_mean":1280,
                "ara2vec":128,
                "pdb2dpc":400
                }

        self.seqs = seqs
        self.a_features = a_features
        self.b_features = b_features

    def encode(self,ppis):
        x = []
        for a,b in ppis:
            temp_a = []
            temp_b = []
            for feature in self.a_features:
                if feature == 'ara2vec' or feature == 'esm_mean' or feature == "pdb2dpc":
                    temp_a.append(self.features[feature][a])
                else:
                    temp_a.append(self.features[feature](self.seqs[a]))
            
            for feature in self.b_features:
                if feature == 'ara2vec' or feature == 'esm_mean' or feature == "pdb2dpc":
                    temp_b.append(self.features[feature][b])
                else:
                    temp_b.append(self.features[feature](self.seqs[b]))

            temp_a = np.hstack(temp_a)
            temp_b = np.hstack(temp_b)
            x.append(np.hstack((temp_a,temp_b)))
        return np.array(x)


if __name__ == "__main__":
    ppis = [('NP123','NP123'),('NP123','NP123')]
    seqs = {'NP123':"AGVAGVAGV"}
    features = ['dpc','ct']
    encode = feature_combine(features,features,seqs)
    print(encode.encode(ppis).shape)


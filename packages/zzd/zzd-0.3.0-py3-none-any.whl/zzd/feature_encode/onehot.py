import numpy as np

def onehot(seq, fix_len=2000):
    amino2num = { i:idx for idx,i in enumerate("AGVCDEFILPHNQWKRMSTYX")}

    if fix_len:
        seq =np.array([amino2num[i] for i in seq[:fix_len]])
        v = np.zeros((fix_len,21))
        v[:len(seq)] = np.eye(21)[seq]
    else:
        seq = np.array([amino2num[i] for i in seq])
        v =  np.eye(21)[seq]
    return v

if __name__ == "__main__":
    seq="MIRRISPGAVPPSLPSAPVASHHHADAPQAGVQPPADTAHHAPRLRPAPPRKRRRGMRSLDGMDDELDATELEEAEA"
    print(onehot(seq), onehot(seq).shape)


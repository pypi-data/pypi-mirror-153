"""
test_ppi.txt train_ppi.txt 
encode:onehot,pssm

"""
import numpy as np
from torch.utils.data import Dataset

def load_data(ppi_file,seqs_file,features):
    """
    pass
    """
    ppis = np.genfromtxt(ppi_file,str)
    X,Y = np.array(ppis[:,:2],str), np.array(ppis[:,2],int)
    seqs = {i.id:str(i.seq) for i in SeqIO.parse(seqs_file,'fasta')}
    encode = feature_combine(features,features,seqs)
    return encode.encode(X),Y

class ppis_dataset(Dataset):
	"""
	encode a protein to onehot matrix
	every pair protein of ppi return pair onehot feature
	"""
	def __init__(self, ppis, target, seqs):
		self.ppis = ppis
		self.target = target
		self.seqs = seqs
	
	def __len__(self):
		return self.ppis.__len__()
	
	def __getitem__(self,index):
		x1 = torch.from_numpy(self.seqs[self.ppis[index][0]].toarray())
		x2 = torch.from_numpy(self.seqs[self.ppis[index][1]].toarray())
		y  = torch.tensor(self.target[index])
		return x1, x2, y


def ppi_cnn(test_file,train_file,seqs_file,feature_encode='onehot',n_jobs=-1,**argv):
    """
    test_file:for pred
    train_file:fro train
    seqs_file: fasta sequence
    feature: onehot
    """
    x_train, y_train = load_data(train_file,seqs_file,feature_encode)
    x_test, y_test = load_data(test_file,seqs_file,feature_encode)

    model = cnn()
    model.fit(x_train,y_train)
    
    y_test_pred = model.predict_proba(x_test)[:, 1]
    return y_test_pred


if __name__ == "__main__":
    test_file = "../../../atppi/B2_train_and_test/p1n10_10folds/test_0.txt"
    train_file = "../../../atppi/B2_train_and_test/p1n10_10folds/train_0.txt"
    seqs_file = "../../../atppi/B1_ppis_and_seqs/ppis_ara_and_eff.fasta"
    pred = ppi_bayesian(test_file,train_file,seqs_file,feature_encode=['dpc'],pca=False)

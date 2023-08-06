from Bio import SeqIO
import numpy as np
import scipy.sparse as sp
from torch.utils.data import Dataset, DataLoader
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
from zzd.utils.assess import multi_scores as scores
from zzd.utils.assess import  mean_accuray
import sys

def onehot_encode(seq, max_len=2000):
    amino2num = {i: idx for idx, i in enumerate("AGVCDEFILPHNQWKRMSTYX")}
    seqnum = np.array([amino2num[i] for i in seq[:max_len]])
    v = np.zeros((max_len, 21),dtype=np.float32)
    v[:len(seqnum)] = np.eye(21)[seqnum]
    return torch.from_numpy(v.T)

class OnehotFeatures():
    def __init__(self, seq_file=None, max_len=2000):
        self.features = {i.id: onehot_encode(
            str(i.seq)) for i in SeqIO.parse(seq_file, "fasta")}

    def __getitem__(self, index):
        return self.features[index]

    def keys(self):
        return self.features.keys()

    def values(self):
        return self.features.values()

class PPIDataset(Dataset):
    def __init__(self, ppis, target, features):
        self.ppis = ppis
        self.target = target
        self.features = features

    def __len__(self):
        return self.ppis.__len__()

    def __getitem__(self, index):
        x1 = self.features[self.ppis[index][0]]
        x2 = self.features[self.ppis[index][1]]
        y = torch.tensor(self.target[index])
        return x1, x2, y


class cnn_block(nn.Module):
    def __init__(self) -> None:
        super(cnn_block,self).__init__()
        self.conv1 = nn.Conv1d(21,64, kernel_size=5, stride=1)
        self.pool1 = nn.MaxPool1d(2)
        self.norm1 = nn.BatchNorm1d(64,affine=True)
        
        self.conv2 = nn.Conv1d(64, 128, kernel_size=3, stride=1)
        self.pool2 = nn.MaxPool1d(2)
        self.norm2= nn.BatchNorm1d(128,affine=True)

        self.conv3 = nn.Conv1d(128, 256, kernel_size=3, stride=1)
        self.pool3 = nn.MaxPool1d(2)
        self.norm3 = nn.BatchNorm1d(256,affine=True)

        self.conv4 = nn.Conv1d(256, 512, kernel_size=3, stride=1)
        self.pool4 = nn.MaxPool1d(2)
        self.norm4 = nn.BatchNorm1d(512,affine=True)

        self.conv5 = nn.Conv1d(512, 512, kernel_size=3, stride=1)
        self.pool5 = nn.MaxPool1d(2)
        self.norm5 = nn.BatchNorm1d(512,affine=True)

    def forward(self,x):
        x = self.conv1(x)
        x = self.norm1(x)
        x = F.relu(x)
        x = self.pool1(x)

        x = self.conv2(x)
        x = self.norm2(x)
        x = F.relu(x)
        x = self.pool2(x)

        x = self.conv3(x)
        x = self.norm3(x)
        x = F.relu(x)
        x = self.pool3(x)

        x = self.conv4(x)
        x = self.norm4(x)
        x = F.relu(x)
        x = self.pool4(x)

        x = self.conv5(x)
        x = self.norm5(x)
        x = F.relu(x)
        x = self.pool5(x)
        return x


class siamese_cnn(nn.Module):
    def __init__(self) -> None:
        super(siamese_cnn,self).__init__()
        self.cnn_block = cnn_block()
        inshape = cnn_block()(torch.randn(1,21,2000)).shape
        self.fc1 = nn.Linear(inshape[-2]*inshape[-1]*2,128)
        self.fc2 = nn.Linear(128,1)
        self.flatten = nn.Flatten()
        self.dropout = nn.Dropout(0.2)


    def forward(self,x1,x2):
        x1 = self.cnn_block(x1)
        x1 = self.flatten(x1)
        x2 = self.cnn_block(x2)
        x2 = self.flatten(x2)

        x = torch.cat((x1,x2),1)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        x = torch.sigmoid(x)
        return x

def weights_init(m):
    if isinstance(m, (nn.Conv1d, nn.Linear)):
        nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')
        # nn.init.constant(m.bias, 0.0)


def train( model, device, train_loader, optimizer, epoch):
    model.train()
    criterion = nn.BCELoss()

    train_loss = 0
    train_acc = 0
    outputs = np.empty(0)
    targets = np.empty(0)
    for batch_idx, (x1, x2, target) in enumerate(train_loader):
        x1, x2, target = x1.to(device), x2.to(device), target.to(device)
        output = model(x1, x2)
        output = output.squeeze(dim=-1)
        loss = criterion(output, target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 计算损失和平均准确率
        with torch.no_grad():
            train_loss += loss.item()
            mean_loss = train_loss/(batch_idx+1)
            outputs = np.concatenate((outputs, output.cpu().numpy()))
            targets = np.concatenate((targets, target.cpu().numpy()))
            train_acc = mean_accuray(targets, outputs)
        print(
            f"\r Train Epoch:{epoch} {batch_idx*len(x1)} {len(train_loader.dataset)}  train_loss:{mean_loss:.4f} train_acc:{train_acc:.4f}", end="")
        sys.stdout.flush()
    print("")
    #scores(targets, outputs,show=True)
    # print(targets)

def test(model, device, test_loader):
    model.eval()
    criterion = nn.BCELoss()

    test_loss = 0
    outputs = np.empty(0)
    targets = np.empty(0)
    with torch.no_grad():
        for x1, x2, target in test_loader:
            x1, x2, target = x1.to(device), x2.to(device), target.to(device)
            output = model(x1, x2)
            output = output.squeeze(dim=-1)

            test_loss += criterion(output, target).item()  # sum up batch loss
            outputs = np.concatenate((outputs, output.cpu().numpy()))
            targets = np.concatenate((targets, target.cpu().numpy()))
            test_acc = mean_accuray(targets, outputs)
    mean_loss = test_loss/len(test_loader.dataset)

    print(f"\rTest set: {test_loss:.4f} {test_acc}", end="")
    sys.stdout.flush()
    print("")
    return outputs


def ppi_cnn_torch(train_file, test_file, seq_file,lr=0.01,epochs=14):
    train_kw = {'batch_size':16,'shuffle':True}
    test_kw = {'batch_size':1,'shuffle':False}

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.manual_seed(1)
    if torch.cuda.is_available(): 
        train_kw.update({'num_workers': 1, 'pin_memory': True })
        test_kw.update( {'num_workers': 1, 'pin_memory': True })
    #
    features = OnehotFeatures(seq_file)
    ppis_train = np.genfromtxt(train_file, str)
    ppis_test = np.genfromtxt(test_file, str)

    X_train, Y_train = np.array(ppis_train[:, :2], str), np.array(ppis_train[:, 2], np.float32)
    X_test, Y_test = np.array(ppis_test[:, :2], str), np.array(ppis_test[:, 2], np.float32)

    train_data = PPIDataset(X_train, Y_train, features)
    test_data = PPIDataset(X_test, Y_test, features)

    train_loader = DataLoader(train_data, **train_kw )
    test_loader = DataLoader(test_data, **test_kw)
    
    #
    model = siamese_cnn().to(device)
    model.apply(weights_init)
    optimizer = optim.Adadelta(model.parameters(), lr=lr)
    scheduler = StepLR(optimizer, step_size=1, gamma=0.7)

    #
    model = siamese_cnn().to(device)
    model.apply(weights_init)
    optimizer = optim.Adadelta(model.parameters(), lr=0.01)
    scheduler = StepLR(optimizer, step_size=1, gamma=0.7)

    #
    for epoch in range(1, epochs + 1):
        train( model, device, train_loader, optimizer, epoch)
        #test(model, device, test_loader)
        scheduler.step()

    #
    y_pred = test(model, device, test_loader)

    return y_pred


from zzd.utils.assess import multi_scores as scores
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Model
from tensorflow.keras.utils import Sequence
from Bio import SeqIO

class PPI_DataGenerator(Sequence):
    def onehot(self,seq, max_len=2000):
        amino2num = {v: k for k, v in enumerate("AGVCDEFILPHNQWKRMSTYX")}
        seq = np.array([amino2num[i] for i in seq[:max_len]])
        re = np.zeros((2000, 21),dtype=np.float32)
        re[:len(seq)] = np.eye(21)[seq]
        return re

    def __init__(self, ppi_file=None, seq_file=None, input_size=(2000, 20), shuffle=True, batch_size=16):
        self.features = {i.id: self.onehot(str(i.seq)) for i in SeqIO.parse(seq_file, "fasta")}
        self.ppi_table = np.genfromtxt(ppi_file,str)
        self.ppis = self.ppi_table[:,:2]
        self.labels = self.ppi_table[:,2]
        self.input_size = input_size
        self.shuffle = shuffle
        self.batch_size = batch_size
        self.n = len(self.ppis)
        self.indices = np.arange(len(self.ppis))
        self.on_epoch_end()

    def __len__(self):
        return self.n // self.batch_size

    def on_epoch_end(self):
        self.indices = np.arange(len(self.ppis))
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __getitem__(self, index):
        batches_indices = self.indices[index * self.batch_size: (index + 1) * self.batch_size]
        batches_id_pair = [self.ppis[i] for i in batches_indices]
        x1 = np.asarray([self.features[i] for i, j in batches_id_pair])
        x2 = np.asarray([self.features[j] for i, j in batches_id_pair])
        y = np.asarray([self.labels[i] for i in batches_indices],float)

        return tuple([x1, x2]), y

    def get_labels(self,):
        return self.labels


def siamese_cnn(length=2000, chanels=21, dropout_rate=0.2, lr=0.001):
    In = layers.Input(shape=(length, chanels))
    x = layers.Conv1D(filters=32, kernel_size=3, padding='same',
                      input_shape=(length, chanels))(In)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = layers.AvgPool1D(pool_size=4, padding='same')(x)

    x = layers.Conv1D(filters=64, kernel_size=3, strides=1, padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = layers.AvgPool1D(pool_size=4, padding='same')(x)

    x = layers.Conv1D(filters=128, kernel_size=3, padding='same')(x)
    x = layers.ReLU()(x)
    x = layers.AvgPool1D(pool_size=4, padding='same')(x)

    x = layers.Conv1D(filters=256, kernel_size=3, padding='same')(x)
    x = layers.ReLU()(x)
    x = layers.MaxPool1D(pool_size=4, strides=4, padding='same')(x)

    x = layers.Conv1D(filters=512, kernel_size=3, padding='same')(x)
    x = layers.ReLU()(x)
    x = layers.MaxPool1D(pool_size=4, strides=4, padding='same')(x)
    x = layers.Flatten()(x)
    convs = Model(In, x)
    In1 = layers.Input(shape=(length, chanels))
    In2 = layers.Input(shape=(length, chanels))
    x1 = convs(In1)
    x2 = convs(In2)
    x_merge = layers.Concatenate()([x1, x2])
    fc1 = layers.Dense(512, activation='relu')(x_merge)
    fc1 = layers.Dropout(dropout_rate)(fc1)
    fc2 = layers.Dense(1, activation='sigmoid')(fc1)
    model = Model([In1, In2], [fc2])

    model.compile(loss=tf.keras.losses.BinaryCrossentropy(),
                  optimizer=tf.keras.optimizers.Adam(learning_rate=lr), metrics=['accuracy'])

    return model


def ppi_cnn_onehot(train_file, test_file, seq_file,epochs=14):
    train_gen =  PPI_DataGenerator(train_file,seq_file,shuffle=True)
    test_gen = PPI_DataGenerator(test_file,seq_file,shuffle=False,batch_size=1)
    model = siamese_cnn()

    #callback1 = tf.keras.callbacks.EarlyStopping(
    #monitor='val_loss', patience=4, restore_best_weights=False)
    #callback2 = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=2, verbose=0,
    #                                             mode='auto', min_delta=0.0001, cooldown=0, min_lr=0)

    model.fit(train_gen,  epochs=epochs, verbose=1)

    y_test_pred = model.predict(test_gen)
    return y_test_pred.ravel()



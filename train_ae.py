#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import tensorflow as tf
from model import SMILESautoencoder

flags = tf.app.flags
flags.DEFINE_string("dataset", "data/chembl24_10uM_20-100.csv", "dataset file (expecting csv or pickled file)")
flags.DEFINE_string("run_name", "test", "run name for log and checkpoint files")
flags.DEFINE_string("tokenizer", "default", "Tokenizer for one-hot encoding: 'default': 71 tokens;"
                                            "'generate': generate new tokenizer from input data")
flags.DEFINE_integer("layers", 2, "number of LSTM layers in the network")
flags.DEFINE_float("dropout", 0.2, "fraction of dropout to apply; layer 1 gets 1*dropout, layer 2 2*dropout etc.")
flags.DEFINE_integer("neurons", 256, "number of neurons per layer")
flags.DEFINE_float("learning_rate", 0.001, "learning rate")
flags.DEFINE_integer("batch_size", 128, "batch size")
flags.DEFINE_integer("step", 2, "step size")
flags.DEFINE_integer("sample_after", 5, "sample after how many epochs")
flags.DEFINE_integer("epochs", 10, "epochs to train")
flags.DEFINE_integer("n_mols", 0, "number of molecules to take for training every epoch (if 0, use all)")
flags.DEFINE_integer("augment", 1, "whether different SMILES strings should generated for the same molecule, [1-n]")
flags.DEFINE_boolean("preprocess", False, "whether to pre-process stereo chemistry/salts etc.")
flags.DEFINE_integer("stereochemistry", 1, "whether stereo chemistry information should be included [0, 1]")
flags.DEFINE_float("validation", 0.2, "fraction of the data to use as a validation set")

FLAGS = flags.FLAGS


def main(_):
    print("Running SMILES LSTM model...")
    model = SMILESautoencoder(batch_size=FLAGS.batch_size, dataset=FLAGS.dataset,
                              num_epochs=FLAGS.epochs, lr=FLAGS.learning_rate, n_mols=FLAGS.n_mols,
                              run_name=FLAGS.run_name, sample_after=FLAGS.sample_after, validation=FLAGS.validation)
    model.load_data(preprocess=FLAGS.preprocess, stereochem=FLAGS.stereochemistry, augment=FLAGS.augment)
    model.build_tokenizer(tokenize=FLAGS.tokenizer, pad_char='A')
    model.build_model(layers=FLAGS.layers, neurons=FLAGS.neurons, dropoutfrac=FLAGS.dropout)
    model.train_model()
    # json.dump(FLAGS.__flags.items(), open('./checkpoint/%s/flags.json' % FLAGS.run_name, 'w'))  # save used flags


if __name__ == '__main__':
    tf.app.run()

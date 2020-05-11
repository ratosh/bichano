import argparse
import yaml
import glob
import random
import os

from training_chunk_pb2 import Chunk
from training_config import TrainingConfig


def get_chunks(data_prefix):
    return glob.glob(data_prefix + "*.bch")


def get_all_chunks(path):
    chunks = []
    for d in glob.glob(path):
        chunks += get_chunks(d)
    random.shuffle(chunks)
    return chunks


def train(args):
    yaml_file = yaml.safe_load(args.cfg)
    print(yaml.dump(yaml_file, default_flow_style=False))
    cfg = TrainingConfig(yaml_file)

    output_dir = cfg.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    chunks = get_all_chunks(cfg.input)
    print("Found {} chunk files".format(len(chunks)))
    num_train_chunks = int(len(chunks) * cfg.train_ratio)
    training_chunks = chunks[:num_train_chunks]
    test_chunks = chunks[num_train_chunks:]
    print("Games in first chunk {}".format(len(training_chunk.games)))


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Tensorflow pipeline for training Leela Chess.')
    argparser.add_argument('--cfg',
                           type=argparse.FileType('r'),
                           help='yaml configuration with training parameters')

    train(argparser.parse_args())

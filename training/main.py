import argparse
import yaml
import glob
import random
import os

from chunkloader import ChunkLoader
from training_config import TrainingConfig


def get_chunks(directory):
    files = []
    iterator = glob.iglob(directory + "*.bch")
    for file in iterator:
        files.append(file)
    return files


def get_all_chunks(path):
    chunks = []
    iterator = glob.iglob(path)
    for directory in iterator:
        chunks += get_chunks(directory)
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
    print("Chunks Training({}) Testing({})".format(len(training_chunks), len(test_chunks)))
    train_loader = ChunkLoader(training_chunks, cfg)
    test_loader = ChunkLoader(test_chunks, cfg)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Tensorflow pipeline for training.')
    argparser.add_argument('--cfg',
                           type=argparse.FileType('r'),
                           help='yaml configuration with training parameters')

    train(argparser.parse_args())

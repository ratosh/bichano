import argparse
import yaml
import glob
import random
import os


class TrainingConfig:

    # name: 'name'
    # gpu: 0
    # training:
    #   train_test_ratio: 0.8
    #   batch_size: 1024
    #   input: 'D:\nn\ccrl\*\'
    #   output: 'D:\nn\training\'
    #   steps: 100000
    #   learning_rate:
    #       - 0.01
    #       - 0.001
    #       - 0.0001
    #   learning_rate_bounds:
    #       - 50000
    #       - 80000
    # model:
    #   filters: 64
    #   blocks: 6
    # ...
    def __init__(self, cfg):
        self.gpu = cfg['gpu']
        self.train_ratio = cfg['training'].get('train_test_ratio', 0.8)
        self.batch_size = cfg['training'].get('batch_size', 1024)
        self.input = cfg['training']['input']
        self.output = os.path.join(cfg['training']['output'], cfg['name'])
        self.steps = cfg['training'].get('steps', 100000)
        self.lr = cfg['training'].get('learning_rate', [0.01, 0.001, 0.0001])
        self.lr_bounds = cfg['training'].get('learning_rate_bounds', [50000, 70000])
        self.filters = cfg['model'].get('filters', 64)
        self.blocks = cfg['training'].get('blocks', 6)


def get_chunks(data_prefix):
    return glob.glob(data_prefix + "*.chk")


def get_all_chunks(path):
    chunks = []
    for d in glob.glob(path):
        chunks += get_chunks(d)
    random.shuffle(chunks)
    pass


def train(args):
    yaml_file = yaml.safe_load(args.cfg)
    print(yaml.dump(yaml_file, default_flow_style=False))
    cfg = TrainingConfig(yaml_file)

    root_dir = cfg.output
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Tensorflow pipeline for training Leela Chess.')
    argparser.add_argument('--cfg',
                           type=argparse.FileType('r'),
                           help='yaml configuration with training parameters')

    train(argparser.parse_args())

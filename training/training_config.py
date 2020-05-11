import os


class TrainingConfig:

    # name: 'name'
    # gpu: 0
    # training:
    #   train_test_ratio: 0.8
    #   batch_size: 1024
    #   input: 'D:\nn\ccrl\*\'
    #   output: 'D:\nn\training_output\'
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
    def __init__(self, yaml_file):
        self.gpu = yaml_file['gpu']
        self.train_ratio = yaml_file['training'].get('train_test_ratio', 0.8)
        self.batch_size = yaml_file['training'].get('batch_size', 1024)
        self.input = yaml_file['training']['input']
        self.output = os.path.join(yaml_file['training']['output'], yaml_file['name'])
        self.steps = yaml_file['training'].get('steps', 100000)
        self.lr = yaml_file['training'].get('learning_rate', [0.01, 0.001, 0.0001])
        self.lr_bounds = yaml_file['training'].get('learning_rate_bounds', [50000, 70000])
        self.filters = yaml_file['model'].get('filters', 64)
        self.blocks = yaml_file['training'].get('blocks', 6)

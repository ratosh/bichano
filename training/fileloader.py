import argparse
import numpy as np

from simple_board_encoder import SimpleBoardEncoder
from simple_policy_encoder import SimplePolicyEncoder
from training_chunk_pb2 import GameChunk


class FileLoader:

    def __init__(self, file):
        self.current_index = 0
        print("Loading {} file".format(file))
        in_file = open(file, "rb")
        self.game_chunk = GameChunk.FromString(in_file.read())
        in_file.close()
        if self.game_chunk.board_encoding == GameChunk.BoardEncodingType.SIMPLE_BOARD:
            self.board_encoder = SimpleBoardEncoder()
        if self.game_chunk.policy_encoding == GameChunk.PolicyEncodingType.SIMPLE_POLICY:
            self.policy_encoder = SimplePolicyEncoder()

    def next(self):
        self.current_index += 1
        for position in self.game_chunk.positions:
            yield position.planes, position.policy

    def result(self):
        return self.game_chunk.result


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Training file loader')
    argparser.add_argument('--file',
                           type=argparse.FileType('r'),
                           help='Training file')

    args = argparser.parse_args()
    file_loader = FileLoader(args.file.name)

    for position, policy in file_loader.next():
        print(file_loader.board_encoder.to_string(position))
        print(file_loader.policy_encoder.to_string(policy))

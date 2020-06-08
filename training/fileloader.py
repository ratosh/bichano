import argparse
import numpy as np

from simple_board_encoder import SimpleBoardEncoder
from simple_policy_encoder import SimplePolicyEncoder
from training_chunk_pb2 import PositionChunk


class FileLoader:

    def __init__(self, file):
        print("Loading {} file".format(file))
        in_file = open(file, "rb")
        self.position_chunk = PositionChunk.FromString(in_file.read())
        in_file.close()
        if self.position_chunk.board_encoding == PositionChunk.BoardEncodingType.SIMPLE_BOARD:
            self.board = SimpleBoardEncoder(self.position_chunk.planes)
        if self.position_chunk.policy_encoding == PositionChunk.PolicyEncodingType.SIMPLE_POLICY:
            self.policy = SimplePolicyEncoder(self.position_chunk.policy, self.position_chunk.games)

    def to_numpy(self):
        return self.board.to_numpy(), \
               self.policy.to_numpy(), \
               np.float32(self.position_chunk.points / self.position_chunk.games)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Training file loader')
    argparser.add_argument('--file',
                           type=argparse.FileType('r'),
                           help='Training file')

    args = argparser.parse_args()
    FileLoader(args.file.name)

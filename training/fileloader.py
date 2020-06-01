import argparse

from simple_board_encoder import SimpleBoardEncoder
from training_chunk_pb2 import PositionChunk


class FileLoader:

    def __init__(self, file):
        print("Loading {} file".format(file))
        in_file = open(file, "rb")
        self.position_chunk = PositionChunk.FromString(in_file.read())
        in_file.close()
        if self.position_chunk.board_encoding == PositionChunk.BoardEncodingType.SIMPLE_BOARD:
            board = SimpleBoardEncoder(self.position_chunk.planes)
            print(board.display())


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Training file loader')
    argparser.add_argument('--file',
                           type=argparse.FileType('r'),
                           help='Training file')

    args = argparser.parse_args()
    FileLoader(args.file.name)

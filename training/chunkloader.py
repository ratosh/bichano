from training_chunk_pb2 import PositionChunk


class ChunkLoader:

    def __init__(self, file):
        in_file = open(file, "rb")
        self.position_chunk = PositionChunk()
        self.position_chunk.ParseFromString(in_file.read())
        in_file.close()

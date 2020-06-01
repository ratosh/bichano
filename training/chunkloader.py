from training_chunk_pb2 import PositionChunk


class ChunkLoader:

    def __init__(self, files, cfg):
        print("Creating loader for {} files using in {} batch size".format(len(files), cfg.batch_size))
        # TODO: Load a file

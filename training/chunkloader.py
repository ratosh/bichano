from fileloader import FileLoader
from training_chunk_pb2 import PositionChunk
import numpy as np


class ChunkLoader:

    def __init__(self, files, cfg):
        print("Creating loader for {} files using in {} batch size".format(len(files), cfg.batch_size))
        self.files = files
        self.cfg = cfg
        self.current_file_index = 0


    def load_batch(self):
        for b in self.batch_output(self.load_next_batch()):
            yield b

    def batch_output(self, input):
        input_planes = np.unpackbits(np.frombuffer(input.planes, dtype=np.uint8)).astype(np.float32)
        policy = np.array(ndim=1858, dtype=np.float32)
        for policy_entry in input.game_chunk.policy:
            np.put(policy, policy_entry.move_index, policy_entry.times_played / input.games)
        winner = np.unpackbits(input.points / input.games, dtype=np.float32)
        return input_planes, policy, winner

    def load_next_batch(self):
        s = []
        for i in range(self.cfg.batch_size):
            s.append(FileLoader(self.files[self.current_file_index + i]))

        self.current_file_index += self.cfg.batch_size
        while True:
            if s is None:
                return
            yield s

    def translate_to_tf(self, input_planes, policy, winner):
        input_planes = 0
        policy = 0
        winner = 0
        return input_planes, policy, winner
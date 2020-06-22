import numpy as np

from file_loader import FileLoader


class BatchLoader:

    def __init__(self, files, cfg):
        print("Creating loader for {} files using in batches of {} positions".format(len(files), cfg.batch_size))
        self.files = files
        self.cfg = cfg
        self.current_file_index = 0

    def iterator(self):
        for file_loader, position, policy in self.load_next_batch():
            yield self.batch_output(file_loader, position, policy)

    def batch_output(self, file_loader, position, policy):
        input_planes = file_loader.board_encoder.to_numpy(position)
        policy = file_loader.policy_encoder.to_numpy(policy)
        winner = np.single(file_loader.result() * 2 - 1)
        return input_planes, policy, winner

    def load_next_batch(self):
        positions = 0
        for _ in range(self.cfg.batch_size):
            file_loader = FileLoader(self.files[self.current_file_index])
            self.current_file_index += 1
            if self.current_file_index >= len(self.files):
                self.current_file_index = 0
            for position, policy in file_loader.next():
                positions += 1
                if positions > self.cfg.batch_size:
                    return
                yield file_loader, position, policy

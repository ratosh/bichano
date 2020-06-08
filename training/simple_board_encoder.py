import numpy as np


class SimpleBoardEncoder:

    def __init__(self, planes):
        self.planes = []
        for plane in planes:
            self.planes.append(plane)

    def game_bitboard(self):
        return self.planes[0] | self.planes[1]

    def piece_type(self, bit):
        if self.planes[2] & bit != 0:
            return 'p'
        if self.planes[3] & bit != 0:
            return 'n'
        if self.planes[4] & bit != 0:
            return 'b'
        if self.planes[5] & bit != 0:
            return 'r'
        if self.planes[6] & bit != 0:
            return 'q'
        if self.planes[7] & bit != 0:
            return 'k'
        return '.'

    def to_numpy(self):
        return np.unpackbits(np.array(self.planes, dtype='>u8').view(np.uint8)).view(np.float32)

    def display(self):
        output = "BOARD\n"
        for rank in range(8):
            for file in range(8):
                bit = 1 << ((7 - rank) << 3) + file
                piece = self.piece_type(bit)
                if self.planes[0] & bit != 0:
                    output += piece.upper()
                else:
                    output += piece
            output += "\n"
        output += "EP\n" + display_bitboard(self.planes[8])
        output += "Castling\n" + display_bitboard(self.planes[9])
        return output


def display_bitboard(bitboard):
    output = ""
    for rank in range(8):
        for file in range(8):
            bit = 1 << ((7 - rank) << 3) + file
            if bitboard & bit != 0:
                output += "1"
            else:
                output += "."
        output += "\n"
    return output

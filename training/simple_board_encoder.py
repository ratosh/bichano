import numpy as np


class SimpleBoardEncoder:

    def to_numpy(self, planes):
        return np.unpackbits(np.array(planes, dtype='>u8').view(np.uint8)).view(np.float32)

    def game_bitboard(self, planes):
        return planes[0] | planes[1]

    def piece_type(self, planes, bit):
        if planes[2] & bit != 0:
            return 'p'
        if planes[3] & bit != 0:
            return 'n'
        if planes[4] & bit != 0:
            return 'b'
        if planes[5] & bit != 0:
            return 'r'
        if planes[6] & bit != 0:
            return 'q'
        if planes[7] & bit != 0:
            return 'k'
        return '.'

    def to_string(self, planes):
        output = "BOARD\n"
        for rank in range(8):
            for file in range(8):
                bit = 1 << ((7 - rank) << 3) + file
                piece = self.piece_type(planes, bit)
                if planes[0] & bit != 0:
                    output += piece.upper()
                else:
                    output += piece
            output += "\n"
        output += "EP\n" + display_bitboard(planes[8])
        output += "Castling\n" + display_bitboard(planes[9])
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

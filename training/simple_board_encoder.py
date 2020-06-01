from training_chunk_pb2 import PositionChunk


class SimpleBoardEncoder:

    def __init__(self, planes):
        self.color_bitboard = [0, 0]
        self.piece_bitboard = [0, 0, 0, 0, 0, 0, 0]
        self.color_bitboard[0] = planes[0]
        self.color_bitboard[1] = planes[1]
        self.piece_bitboard[1] = planes[2]
        self.piece_bitboard[2] = planes[3]
        self.piece_bitboard[3] = planes[4]
        self.piece_bitboard[4] = planes[5]
        self.piece_bitboard[5] = planes[6]
        self.piece_bitboard[6] = planes[7]
        self.ep_bitboard = planes[8]
        self.castling_bitboard = planes[9]

    def game_bitboard(self):
        return self.color_bitboard[0] | self.color_bitboard[1]

    def piece_type(self, bit):
        if self.piece_bitboard[1] & bit != 0:
            return 'p'
        if self.piece_bitboard[2] & bit != 0:
            return 'n'
        if self.piece_bitboard[3] & bit != 0:
            return 'b'
        if self.piece_bitboard[4] & bit != 0:
            return 'r'
        if self.piece_bitboard[5] & bit != 0:
            return 'q'
        if self.piece_bitboard[6] & bit != 0:
            return 'k'
        return '.'

    def display(self):
        output = ""
        for rank in range(8):
            for file in range(8):
                bit = 1 << ((7 - rank) << 3) + file
                piece = self.piece_type(bit)
                if self.color_bitboard[0] & bit != 0:
                    output.append(piece.upper())
                else:
                    output.append(piece)
            output.append("\n")
        return output

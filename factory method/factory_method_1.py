"""
Паттерн Фабричный меод применяется, когда мы хотим, чтобы
подклассы выбрали, какой класс инстанциировать, когда запрашивается объект

Это полезно само по себе, но можно пойти дальше и использовать в случае, каогда
класс заранее неизвестен (например, зависит от информации, прочитанной из файла
или введенных пользователей)


"""
import io
import itertools
import os
import sys
import tempfile
import unicodedata

DRAUGHT, PAWN, ROOK, KNIGHT, BISHOP, KING, QUEEN = ("DRAUGHT", "PAWN",
        "ROOK", "KNIGHT", "BISHOP", "KING", "QUEEN")
BLACK, WHITE = ("BLACK", "WHITE")


def main():
    checkers = CheckersBoard()
    print(checkers)

    chess = ChessBoard()
    print(chess)

    if sys.platform.startswith("win"):
        filename = os.path.join(tempfile.gettempdir(), "gameboard.txt")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(sys.stdout.getvalue())
        print("wrote '{}'".format(filename), file=sys.__stdout__)


if sys.platform.startswith("win"):
    def console(char, background):
        return char or " "
    sys.stdout = io.StringIO()
else:
    def console(char, background):
        return "\x1B[{}m{}\x1B[0m".format(
                43 if background == BLACK else 47, char or " ")


class AbstractBoard:

    __classForPiece = {(DRAUGHT, BLACK): BlackDraught,
            (PAWN, BLACK): BlackChessPawn,
            (ROOK, BLACK): BlackChessRook,
            (KNIGHT, BLACK): BlackChessKnight,
            (BISHOP, BLACK): BlackChessBishop,
            (KING, BLACK): BlackChessKing,
            (QUEEN, BLACK): BlackChessQueen,
            (DRAUGHT, WHITE): WhiteDraught,
            (PAWN, WHITE): WhiteChessPawn,
            (ROOK, WHITE): WhiteChessRook,
            (KNIGHT, WHITE): WhiteChessKnight,
            (BISHOP, WHITE): WhiteChessBishop,
            (KING, WHITE): WhiteChessKing,
            (QUEEN, WHITE): WhiteChessQueen}

    def __init__(self, rows, columns):
        self.board = [[None for _ in range(columns)] for _ in range(rows)]
        self.populate_board()

    def create_piece(self, kind, color):
        return AbstractBoard.__classForPiece[kind, color]()

    def populate_board(self):
        raise NotImplementedError()

    def __str__(self):
        squares = []
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                square = console(piece, BLACK if (y+x) % 2 else WHITE)
                squares.append(square)
            squares.append("\n")
        return "".join(squares)


class CheckersBoard(AbstractBoard):
    def __init__(self):
        super().__init__(10,10)

    def populate_board(self):
        for x in range(0, 9, 2):
            for y in range(4):
                column = x + ((y + 1) % 2)
                for row, color in ((y, BLACK), (y + 6, WHITE)):
                    self.board[row][column] = self.create_piece(DRAUGHT, color)


class ChessBoard(AbstractBoard):

    def __init__(self):
        super().__init__(8, 8)

    def populate_board(self):
        for row, color in ((0, BLACK), (7, WHITE)):
            for columns, kind in (((0, 7), ROOK), ((1, 6), KNIGHT),
                    ((2, 5), BISHOP), ((3,), QUEEN), ((4,), KING)):
                for column in columns:
                    self.board[row][column] = self.create_piece(kind,
                            color)
        for column in range(8):
            for row, color in ((1, BLACK), (6, WHITE)):
                self.board[row][column] = self.create_piece(PAWN, color)


class Piece(str):
    __slots__ = ()


def make_new_method(char):
    def new(cls):
        return Piece.__new__(cls, char)
    return new


for code in itertools.chain((0x26C0, 0x26C2), range(0x2654, 0x2660)):
    char = chr(code)
    name = unicodedata.name(char).title().replace(" ", "")
    if name.endswith("sMan"):
        name = name[:-4]
    new = make_new_method(char)
    cls = type(name, (Piece,), dict(__slots__=(), __new__=new))

    setattr(sys.modules[__name__], name, cls)  # Can be done better!

# class BlackDraught(Piece):
#     __slots__ = ()
#
#     def __new__(cls):
#         return super().__new__(cls, "\N{black draughts man}")
#
#
# class WhiteChessKing(Piece):
#     __slots__ = ()
#
#     def __new__(cls):
#         return super().__new__(cls, "\N{white chess king}")

    # def populate_board(self):
    #     """Фабричная функция, так как в неё не зашиты классы"""
    #     for x in range(0, 9, 2):
    #         for y in range(4):
    #             column = x + ((y + 1) % 2)
    #             for row, color in ((y, "black"), (y + 6, "white")):
    #                 self.board[row][column] = create_piece("draught", color)
    #
    # def create_piece(kind, color):
    #     if kind == "draught":
    #         return eval("{}{}()".format(color.title(), kind.title()))
    #     return eval("{}Chess{}()".format(color.title(), kind.title()))
    #
    # for code in itertools.chain((0x26C0, 0x26C2), range(0x2654, 0x2660)):
    #     char = chr(code)
    #     name = unicodedata.name(char).title().replace(" ", "")
    #     if name.endswith("sMan"):
    #         name = name[:-4]
    #     exec("""        class {}(Piece):
    #         __slots__ = ()
    #         def __new__(cls):
    #             return super().__new__(cls, "{}")
    #     """.format(name, char))


if __name__ == "__main__":
    main()
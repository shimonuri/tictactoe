import board
import abc


class Player(object, metaclass=abc.ABCMeta):
    EXIT_CHAR = 'q'

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self._name = name

    @property
    def name(self):
        return self._name

    @abc.abstractmethod
    def get_next_turn(self, current_board):
        raise NotImplementedError('get_next_turn not implemented')


class HumanPlayer(Player):
    def get_next_turn(self, current_board):
        row = None
        column = None
        while row is None or column is None:
            try:
                row = input('Row: ')
                if row == self.EXIT_CHAR:
                    return None

                row = int(row)
                column = input('Column: ')
                if column == self.EXIT_CHAR:
                    return None

                column = int(column)
            except ValueError:
                print('column and row must be a decimal number')
                row = None
                column = None

        return board.SquareAddress(row=row, column=column)

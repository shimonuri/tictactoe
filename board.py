import collections
import enum
import prettytable

SquareAddress = collections.namedtuple(typename='BoardAddress', field_names=['column', 'row'])


class SquareValue(enum.Enum):
    CROSS = 'X'
    NOUGHT = 'O'
    EMPTY = ''


class TicTacToeError(Exception):
    pass


class IllegalTicTacToeTurnError(TicTacToeError):
    def __init__(self, board, square_address, square_value, **kwargs):
        super().__init__(**kwargs)
        self._board = board
        self._square_address = square_address
        self._square_value = square_value

    def __str__(self):
        return 'Adding {} to {} is illegal'.format(self.square_value, self.square_address)

    @property
    def board(self):
        return self._board

    @property
    def square_address(self):
        return self._square_address

    @property
    def square_value(self):
        return self._square_value


class SquareAlreadyInUseError(IllegalTicTacToeTurnError):
    def __str__(self):
        return 'Cant add symbol {} to {} because the address is already in use by {}'.format(
            self.square_value,
            self.square_address,
            self.board[self.square_address]
        )


class InvalidSquareAddressError(IllegalTicTacToeTurnError):
    def __str__(self):
        return 'The address {} is invalid (negative or exceeds board size {})'.format(
            self.square_address,
            self.board.size
        )


class Board(object):
    def __init__(self, size=3, starting_symbol=SquareValue.CROSS):
        if size <= 0:
            raise ValueError('Given size {} is lower or equal to zero'.format(size))

        self._size = size
        self._square_address_to_value = {}
        self._current_symbol = starting_symbol
        self._initialize_board_dict()

    def __str__(self):
        table = prettytable.PrettyTable(
            padding_width=4,
            header=False,
            border=True,
            vrules=prettytable.ALL,
            hrules=prettytable.ALL
        )
        for row in range(self.size):
            table.add_row(
                [
                    self[SquareAddress(row=row, column=column)].value for column in range(self.size)
                ]
            )

        return str(table)

    def __getitem__(self, square_address):
        return self._square_address_to_value[square_address]

    @property
    def size(self):
        return self._size

    @property
    def current_symbol(self):
        return self._current_symbol

    def play_turn(self, address):
        self._validate_turn(address)
        self._square_address_to_value[address] = self.current_symbol
        self._current_symbol = SquareValue.CROSS if self.current_symbol is SquareValue.NOUGHT else SquareValue.NOUGHT

    @property
    def has_winner(self):
        return self.get_winner() is not None

    @property
    def full_squares_amount(self):
        return len(
            [
                square_value for square_value in self._square_address_to_value.values() if square_value != SquareValue.EMPTY
            ]
        )

    @property
    def squares_amount(self):
        return self.size ** 2

    @property
    def is_last_turn(self):
        return self.squares_amount - self.full_squares_amount == 1

    @property
    def is_winnable(self):
        if self.has_winner:
            return True

        for winnable_square_group in self._iter_winnable_square_groups():
            winnable_square_group_values = set([self[address] for address in winnable_square_group])
            if len(winnable_square_group_values - {SquareValue.EMPTY}) <= 1:
                if self.is_last_turn:
                    return True if self.current_symbol in winnable_square_group_values else False
                else:
                    return True

        return False

    def get_winner(self):
        for winnable_square_group in self._iter_winnable_square_groups():
            winnable_square_group_values = set([self[address] for address in winnable_square_group])
            if len(winnable_square_group_values) == 1:
                winnable_square_group_value = winnable_square_group_values.pop()
                if winnable_square_group_value != SquareValue.EMPTY:
                    return winnable_square_group_value
                else:
                    return None

    def _iter_winnable_square_groups(self):
        for position in range(self.size):
            yield set(((SquareAddress(row=position, column=column) for column in range(self.size))))
            yield set(((SquareAddress(row=row, column=position) for row in range(self.size))))

        yield set(((SquareAddress(row=position, column=position) for position in range(self.size))))
        yield set(((SquareAddress(row=self.size - 1 - position, column=position) for position in range(self.size))))

    def _validate_turn(self, address):
        if not isinstance(address, SquareAddress):
            raise TypeError('Address must be of type {}'.format(SquareAddress))

        if any([position > self.size - 1 or position < 0 for position in (address.row, address.column)]):
            raise InvalidSquareAddressError(board=self, square_address=address, square_value=self.current_symbol)

        if self[address] != SquareValue.EMPTY:
            raise SquareAlreadyInUseError(board=self, square_address=address, square_value=self.current_symbol)

    def _initialize_board_dict(self):
        for row in range(self.size):
            for column in range(self.size):
                self._square_address_to_value[SquareAddress(column=column, row=row)] = SquareValue.EMPTY

import board
import cmd
import player
import click


class TicTacToeConsole(cmd.Cmd):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._board = None
        self._cross_player = None
        self._nought_player = None

    @property
    def current_player(self):
        return self._get_player_by_square_value(self.board.current_symbol)

    def _get_player_by_square_value(self, square_value):
        return {
            board.SquareValue.CROSS: self.cross_player,
            board.SquareValue.NOUGHT: self.nought_player
        }[square_value]

    @property
    def board(self):
        return self._board

    @property
    def cross_player(self):
        return self._cross_player

    @property
    def nought_player(self):
        return self._nought_player

    def do_init_game(self, arg):
        if arg == '':
            board_size = 3
        else:
            board_size = int(arg)

        print('Creating board of size {}'.format(board_size))
        player_1_name = input('Nought Player Name (player_1): ')
        player_2_name = input('Cross Player Name (player_2: ')

        if len(player_1_name) == 0:
            player_1_name = 'player_1'

        if len(player_2_name) == 0:
            player_2_name = 'player_2'

        self._nought_player = player.HumanPlayer(player_1_name)
        self._cross_player = player.HumanPlayer(player_2_name)
        print('{} versus {}'.format(self.nought_player.name, self.cross_player.name))
        self._board = board.Board(size=board_size)

    def do_start_game(self, arg):
        if self.board is None:
            print('Game was not initialized (use init_game)')
            return

        while not self.board.has_winner and self.board.is_winnable:
            click.clear()
            print(self.board)
            print(
                'Its {} turn! (symbol={})'.format(
                    self.current_player.name,
                    self.board.current_symbol
                )
            )
            address = self.current_player.get_next_turn(current_board=self.board)
            if address is None:
                print('Game was terminated by {}'.format(self.current_player.name))
                break
            try:
                self.board.play_turn(address)
            except board.IllegalTicTacToeTurnError as error:
                print(str(error))
                continue

        if not self.board.is_winnable:
            print(self.board)
            print('board is not winnable')
            print('Its a tie!')

        if self.board.has_winner:
            print(self.board)
            print(
                'Congratulations {}, You have WON the game!'.format(
                    self._get_player_by_square_value(
                        self.board.get_winner()
                    ).name
                )
            )

    def do_print_board(self, arg):
        if self.board is None:
            print('No Board')
        else:
            print(self.board)

    def do_clear(self, arg):
        click.clear()

    def do_exit(self, arg):
        return True


if __name__ == '__main__':
    TicTacToeConsole().cmdloop()

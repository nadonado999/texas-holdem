# game_session.py - 複数ラウンドにわたるゲームセッションの管理

from game import Game
from player import Player, INITIAL_CHIPS


class GameSession:
    """複数ラウンドにわたるゲームセッションを管理するクラス。"""

    def __init__(self) -> None:
        self.player = Player('あなた')
        self.cpu = Player('CPU', is_cpu=True)
        self.round_number: int = 0

    def run(self) -> None:
        """チップが0になるまでラウンドを繰り返す。"""
        print('=' * 40)
        print('  テキサスホールデムポーカー')
        print('=' * 40)

        while self.player.chips > 0 and self.cpu.chips > 0:
            self.round_number += 1
            print(f'\n--- ラウンド {self.round_number} ---')
            self._play_round()

        self._display_final_result()

    def _play_round(self) -> None:
        """1ラウンドをプレイする。"""
        self.player.reset_round()
        self.cpu.reset_round()
        game = Game(self.player, self.cpu)
        game.start()

    def _display_final_result(self) -> None:
        """ゲーム終了時の最終結果を表示する。"""
        print('\n' + '=' * 40)
        print('  ゲーム終了')
        if self.player.chips == 0:
            print(f'  {self.cpu.name}の勝利！')
        else:
            print(f'  {self.player.name}の勝利！')
        print(f'  {self.player.name}: {self.player.chips} チップ')
        print(f'  {self.cpu.name}: {self.cpu.chips} チップ')
        print('=' * 40)

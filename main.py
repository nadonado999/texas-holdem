# main.py - エントリーポイント。ゲームを生成して開始する

from game import Game


def main() -> None:
    """ゲームを生成して1ラウンドを開始する。"""
    game = Game()
    game.start()


if __name__ == '__main__':
    main()

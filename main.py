# main.py - エントリーポイント。ゲームセッションを生成して開始する

from game_session import GameSession


def main() -> None:
    """ゲームセッションを生成して開始する。"""
    session = GameSession()
    session.run()


if __name__ == '__main__':
    main()

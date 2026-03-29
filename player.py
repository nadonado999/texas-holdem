# player.py - プレイヤー・CPU 共通の状態管理

from card import Card

# 初期チップ枚数
INITIAL_CHIPS = 1000


class Player:
    """プレイヤー・CPU 共通の状態を管理するクラス。"""

    def __init__(self, name: str, is_cpu: bool = False) -> None:
        self.name = name
        self.chips: int = INITIAL_CHIPS
        self.hole_cards: list[Card] = []
        self.current_bet: int = 0
        self.is_folded: bool = False
        self.is_cpu: bool = is_cpu

    def bet(self, amount: int) -> None:
        """指定額をベットし、チップを減らす。"""
        self.chips -= amount
        self.current_bet += amount

    def reset_bet(self) -> None:
        """ベッティングラウンド開始時にベット額をリセットする。"""
        self.current_bet = 0

    def reset_round(self) -> None:
        """ラウンド開始時に手札・ベット・フォールド状態をリセットする。"""
        self.hole_cards = []
        self.is_folded = False
        self.reset_bet()

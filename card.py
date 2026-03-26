# card.py - カード1枚の表現と52枚デッキの管理

import random


# スートの一覧
SUITS = ['♠', '♥', '♦', '♣']

# ランクの一覧（2〜9, T=10, J, Q, K, A）
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

# ランク文字列から比較用数値へのマッピング
RANK_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
    '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14,
}


class Card:
    """トランプ1枚を表すクラス。"""

    def __init__(self, suit: str, rank: str) -> None:
        self.suit = suit
        self.rank = rank
        self.rank_value: int = RANK_VALUES[rank]

    def __str__(self) -> str:
        """表示用文字列を返す。例: 'A♠'"""
        return f'{self.rank}{self.suit}'

    def __repr__(self) -> str:
        """デバッグ用文字列を返す。"""
        return f'Card({self.rank}{self.suit})'


class Deck:
    """標準52枚のトランプデッキを表すクラス。"""

    def __init__(self) -> None:
        # 4スート × 13ランクで52枚を生成する
        self.cards: list[Card] = [
            Card(suit, rank) for suit in SUITS for rank in RANKS
        ]

    def shuffle(self) -> None:
        """デッキをシャッフルする。"""
        random.shuffle(self.cards)

    def deal(self) -> Card:
        """デッキの先頭から1枚引いて返す。"""
        return self.cards.pop(0)

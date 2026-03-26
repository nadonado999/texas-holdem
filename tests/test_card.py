# test_card.py - Card・Deck クラスの単体テスト

import sys
import os

# texas_holdem/ をインポートパスに追加する
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from card import Card, Deck, SUITS, RANKS


# --- フィクスチャ ---

@pytest.fixture
def deck() -> Deck:
    """テスト用の52枚デッキを返す。"""
    return Deck()


# --- Card のテスト ---

def test_card_str_returns_rank_and_suit() -> None:
    """str(card) がランクとスートを結合した文字列を返すこと。"""
    card = Card('♠', 'A')
    assert str(card) == 'A♠'


def test_card_str_ten_uses_t() -> None:
    """10のランク表記が 'T' であること。"""
    card = Card('♥', 'T')
    assert str(card) == 'T♥'


def test_card_rank_value_two() -> None:
    """2のrank_valueが2であること。"""
    card = Card('♠', '2')
    assert card.rank_value == 2


def test_card_rank_value_ace() -> None:
    """AのrankValueが14であること。"""
    card = Card('♠', 'A')
    assert card.rank_value == 14


def test_card_rank_value_ten() -> None:
    """TのrankValueが10であること。"""
    card = Card('♦', 'T')
    assert card.rank_value == 10


def test_card_rank_value_jack() -> None:
    """JのrankValueが11であること。"""
    card = Card('♣', 'J')
    assert card.rank_value == 11


def test_card_rank_value_queen() -> None:
    """QのrankValueが12であること。"""
    card = Card('♠', 'Q')
    assert card.rank_value == 12


def test_card_rank_value_king() -> None:
    """KのrankValueが13であること。"""
    card = Card('♥', 'K')
    assert card.rank_value == 13


# --- Deck のテスト ---

def test_deck_has_52_cards(deck: Deck) -> None:
    """生成直後のデッキが52枚であること。"""
    assert len(deck.cards) == 52


def test_deck_has_no_duplicates(deck: Deck) -> None:
    """デッキに重複したカードが含まれていないこと。"""
    # (スート, ランク) のペアをセットに変換して重複を確認する
    identifiers = {(card.suit, card.rank) for card in deck.cards}
    assert len(identifiers) == 52


def test_deck_contains_all_suits_and_ranks(deck: Deck) -> None:
    """全スート × 全ランクの組み合わせが存在すること。"""
    expected = {(suit, rank) for suit in SUITS for rank in RANKS}
    actual = {(card.suit, card.rank) for card in deck.cards}
    assert actual == expected


def test_deal_reduces_deck_by_one(deck: Deck) -> None:
    """deal() を1回呼ぶとデッキが51枚になること。"""
    deck.deal()
    assert len(deck.cards) == 51


def test_deal_returns_card(deck: Deck) -> None:
    """deal() が Card インスタンスを返すこと。"""
    card = deck.deal()
    assert isinstance(card, Card)


def test_deal_52_times_empties_deck(deck: Deck) -> None:
    """deal() を52回呼んだ後にデッキが0枚になること。"""
    for _ in range(52):
        deck.deal()
    assert len(deck.cards) == 0


def test_shuffle_preserves_52_cards(deck: Deck) -> None:
    """shuffle() 後もデッキが52枚であること。"""
    deck.shuffle()
    assert len(deck.cards) == 52


def test_shuffle_preserves_all_cards(deck: Deck) -> None:
    """shuffle() 後も全カードが含まれること（カードの紛失・追加がないこと）。"""
    deck.shuffle()
    identifiers = {(card.suit, card.rank) for card in deck.cards}
    assert len(identifiers) == 52

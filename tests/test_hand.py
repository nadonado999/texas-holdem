# test_hand.py - 手役判定の単体テスト

import sys
import os

# texas_holdem/ をインポートパスに追加する
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from card import Card
from hand import HandRank, HandResult, evaluate


def make_card(rank: str, suit: str) -> Card:
    """テスト用に Card を簡易生成するヘルパー。"""
    rank_values = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
        '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14,
    }
    return Card(suit, rank)


# --- 役判定（全10種）---

def test_evaluate_high_card() -> None:
    """ハイカードを正しく判定すること。"""
    cards = [
        make_card('A', '♠'), make_card('K', '♥'),
        make_card('J', '♦'), make_card('9', '♣'), make_card('7', '♠'),
        make_card('5', '♥'), make_card('3', '♦'),
    ]
    result = evaluate(cards)
    assert result.rank == HandRank.HIGH_CARD


def test_evaluate_one_pair() -> None:
    """ワンペアを正しく判定すること。"""
    cards = [
        make_card('A', '♠'), make_card('A', '♥'),
        make_card('K', '♦'), make_card('Q', '♣'), make_card('J', '♠'),
        make_card('9', '♥'), make_card('7', '♦'),
    ]
    result = evaluate(cards)
    assert result.rank == HandRank.ONE_PAIR


def test_evaluate_two_pair() -> None:
    """ツーペアを正しく判定すること。"""
    cards = [
        make_card('A', '♠'), make_card('A', '♥'),
        make_card('K', '♦'), make_card('K', '♣'), make_card('Q', '♠'),
        make_card('J', '♥'), make_card('9', '♦'),
    ]
    result = evaluate(cards)
    assert result.rank == HandRank.TWO_PAIR


def test_evaluate_three_of_a_kind() -> None:
    """スリーオブアカインドを正しく判定すること。"""
    cards = [
        make_card('A', '♠'), make_card('A', '♥'), make_card('A', '♦'),
        make_card('K', '♣'), make_card('Q', '♠'),
        make_card('J', '♥'), make_card('9', '♦'),
    ]
    result = evaluate(cards)
    assert result.rank == HandRank.THREE_OF_A_KIND


def test_evaluate_straight() -> None:
    """通常のストレートを正しく判定すること。"""
    cards = [
        make_card('9', '♠'), make_card('8', '♥'), make_card('7', '♦'),
        make_card('6', '♣'), make_card('5', '♠'),
        make_card('A', '♥'), make_card('K', '♦'),
    ]
    result = evaluate(cards)
    assert result.rank == HandRank.STRAIGHT


def test_evaluate_straight_wheel() -> None:
    """A-2-3-4-5（最小ストレート）を正しく判定すること。"""
    cards = [
        make_card('A', '♠'), make_card('2', '♥'), make_card('3', '♦'),
        make_card('4', '♣'), make_card('5', '♠'),
        make_card('K', '♥'), make_card('Q', '♦'),
    ]
    result = evaluate(cards)
    assert result.rank == HandRank.STRAIGHT


def test_evaluate_flush() -> None:
    """フラッシュを正しく判定すること。"""
    cards = [
        make_card('A', '♠'), make_card('J', '♠'), make_card('9', '♠'),
        make_card('7', '♠'), make_card('3', '♠'),
        make_card('K', '♥'), make_card('Q', '♦'),
    ]
    result = evaluate(cards)
    assert result.rank == HandRank.FLUSH


def test_evaluate_full_house() -> None:
    """フルハウスを正しく判定すること。"""
    cards = [
        make_card('A', '♠'), make_card('A', '♥'), make_card('A', '♦'),
        make_card('K', '♣'), make_card('K', '♠'),
        make_card('Q', '♥'), make_card('J', '♦'),
    ]
    result = evaluate(cards)
    assert result.rank == HandRank.FULL_HOUSE


def test_evaluate_four_of_a_kind() -> None:
    """フォーオブアカインドを正しく判定すること。"""
    cards = [
        make_card('A', '♠'), make_card('A', '♥'),
        make_card('A', '♦'), make_card('A', '♣'),
        make_card('K', '♠'), make_card('Q', '♥'), make_card('J', '♦'),
    ]
    result = evaluate(cards)
    assert result.rank == HandRank.FOUR_OF_A_KIND


def test_evaluate_straight_flush() -> None:
    """ストレートフラッシュを正しく判定すること。"""
    cards = [
        make_card('9', '♠'), make_card('8', '♠'), make_card('7', '♠'),
        make_card('6', '♠'), make_card('5', '♠'),
        make_card('A', '♥'), make_card('K', '♦'),
    ]
    result = evaluate(cards)
    assert result.rank == HandRank.STRAIGHT_FLUSH


def test_evaluate_royal_flush() -> None:
    """ロイヤルフラッシュを正しく判定すること。"""
    cards = [
        make_card('A', '♠'), make_card('K', '♠'), make_card('Q', '♠'),
        make_card('J', '♠'), make_card('T', '♠'),
        make_card('2', '♥'), make_card('3', '♦'),
    ]
    result = evaluate(cards)
    assert result.rank == HandRank.ROYAL_FLUSH


# --- 役の比較 ---

def test_hand_rank_flush_beats_straight() -> None:
    """HandRank の大小比較でフラッシュがストレートより強いこと。"""
    assert HandRank.FLUSH > HandRank.STRAIGHT


def test_hand_rank_ordering_all() -> None:
    """HandRank の全順序が正しいこと（弱い順に並んでいること）。"""
    ranks = [
        HandRank.HIGH_CARD, HandRank.ONE_PAIR, HandRank.TWO_PAIR,
        HandRank.THREE_OF_A_KIND, HandRank.STRAIGHT, HandRank.FLUSH,
        HandRank.FULL_HOUSE, HandRank.FOUR_OF_A_KIND,
        HandRank.STRAIGHT_FLUSH, HandRank.ROYAL_FLUSH,
    ]
    assert ranks == sorted(ranks)


def test_hand_result_name_high_card() -> None:
    """ハイカードの HandResult.name が日本語であること。"""
    cards = [
        make_card('A', '♠'), make_card('K', '♥'), make_card('J', '♦'),
        make_card('9', '♣'), make_card('7', '♠'),
        make_card('5', '♥'), make_card('3', '♦'),
    ]
    result = evaluate(cards)
    assert result.name == 'ハイカード'


def test_hand_result_name_royal_flush() -> None:
    """ロイヤルフラッシュの HandResult.name が日本語であること。"""
    cards = [
        make_card('A', '♠'), make_card('K', '♠'), make_card('Q', '♠'),
        make_card('J', '♠'), make_card('T', '♠'),
        make_card('2', '♥'), make_card('3', '♦'),
    ]
    result = evaluate(cards)
    assert result.name == 'ロイヤルフラッシュ'


# --- エッジケース ---

def test_evaluate_picks_strongest_hand_from_7_cards() -> None:
    """7枚中に複数の役が成立する場合、最強の役が選ばれること。

    手札: A♠ K♠  コミュニティ: Q♠ J♠ T♠ 2♥ 3♦
    ワンペア・ストレート・フラッシュなど複数が成立するが、
    ロイヤルフラッシュが最強として選ばれること。
    """
    cards = [
        make_card('A', '♠'), make_card('K', '♠'),
        make_card('Q', '♠'), make_card('J', '♠'), make_card('T', '♠'),
        make_card('2', '♥'), make_card('3', '♦'),
    ]
    result = evaluate(cards)
    assert result.rank == HandRank.ROYAL_FLUSH


def test_evaluate_straight_ace_high() -> None:
    """A が最高位（A-K-Q-J-T）のストレートを正しく判定すること。"""
    cards = [
        make_card('A', '♥'), make_card('K', '♦'), make_card('Q', '♣'),
        make_card('J', '♠'), make_card('T', '♥'),
        make_card('2', '♦'), make_card('3', '♣'),
    ]
    result = evaluate(cards)
    assert result.rank == HandRank.STRAIGHT


def test_evaluate_straight_ace_low() -> None:
    """A が最低位（A-2-3-4-5）のストレートを正しく判定すること。"""
    cards = [
        make_card('A', '♥'), make_card('2', '♦'), make_card('3', '♣'),
        make_card('4', '♠'), make_card('5', '♥'),
        make_card('K', '♦'), make_card('Q', '♣'),
    ]
    result = evaluate(cards)
    assert result.rank == HandRank.STRAIGHT


def test_evaluate_best_cards_has_5_cards() -> None:
    """evaluate() の best_cards が常に5枚であること。"""
    cards = [
        make_card('A', '♠'), make_card('K', '♥'), make_card('J', '♦'),
        make_card('9', '♣'), make_card('7', '♠'),
        make_card('5', '♥'), make_card('3', '♦'),
    ]
    result = evaluate(cards)
    assert len(result.best_cards) == 5


# --- タイブレーク ---

def test_tiebreaker_one_pair_higher_pair_wins() -> None:
    """同じワンペアでも、ペアの数字が大きい方が勝つこと（KK > 66）。"""
    cards_kk = [
        make_card('K', '♠'), make_card('K', '♥'),
        make_card('A', '♦'), make_card('Q', '♣'), make_card('J', '♠'),
        make_card('9', '♥'), make_card('7', '♦'),
    ]
    cards_66 = [
        make_card('6', '♠'), make_card('6', '♥'),
        make_card('A', '♦'), make_card('Q', '♣'), make_card('J', '♠'),
        make_card('9', '♥'), make_card('7', '♦'),
    ]
    result_kk = evaluate(cards_kk)
    result_66 = evaluate(cards_66)
    assert result_kk.rank == HandRank.ONE_PAIR
    assert result_66.rank == HandRank.ONE_PAIR
    assert result_kk.tiebreaker > result_66.tiebreaker


def test_tiebreaker_one_pair_same_pair_kicker_decides() -> None:
    """同じペアならキッカーの大きい方が勝つこと（ペアA + Kキッカー > ペアA + Qキッカー）。"""
    cards_ak = [
        make_card('A', '♠'), make_card('A', '♥'),
        make_card('K', '♦'), make_card('J', '♣'), make_card('9', '♠'),
        make_card('7', '♥'), make_card('5', '♦'),
    ]
    cards_aq = [
        make_card('A', '♠'), make_card('A', '♥'),
        make_card('Q', '♦'), make_card('J', '♣'), make_card('9', '♠'),
        make_card('7', '♥'), make_card('5', '♦'),
    ]
    result_ak = evaluate(cards_ak)
    result_aq = evaluate(cards_aq)
    assert result_ak.rank == HandRank.ONE_PAIR
    assert result_ak.tiebreaker > result_aq.tiebreaker


def test_tiebreaker_two_pair_higher_top_pair_wins() -> None:
    """ツーペアで上のペアが大きい方が勝つこと（KK+22 > QQ+JJ）。"""
    cards_kk22 = [
        make_card('K', '♠'), make_card('K', '♥'),
        make_card('2', '♦'), make_card('2', '♣'), make_card('A', '♠'),
        make_card('9', '♥'), make_card('7', '♦'),
    ]
    cards_qqjj = [
        make_card('Q', '♠'), make_card('Q', '♥'),
        make_card('J', '♦'), make_card('J', '♣'), make_card('A', '♠'),
        make_card('9', '♥'), make_card('7', '♦'),
    ]
    result_kk22 = evaluate(cards_kk22)
    result_qqjj = evaluate(cards_qqjj)
    assert result_kk22.rank == HandRank.TWO_PAIR
    assert result_qqjj.rank == HandRank.TWO_PAIR
    assert result_kk22.tiebreaker > result_qqjj.tiebreaker


def test_tiebreaker_straight_higher_high_card_wins() -> None:
    """ストレートで最高位カードが大きい方が勝つこと（9ハイ > 8ハイ）。"""
    cards_9high = [
        make_card('9', '♠'), make_card('8', '♥'), make_card('7', '♦'),
        make_card('6', '♣'), make_card('5', '♠'),
        make_card('A', '♥'), make_card('K', '♦'),
    ]
    cards_8high = [
        make_card('8', '♠'), make_card('7', '♥'), make_card('6', '♦'),
        make_card('5', '♣'), make_card('4', '♠'),
        make_card('A', '♥'), make_card('K', '♦'),
    ]
    result_9 = evaluate(cards_9high)
    result_8 = evaluate(cards_8high)
    assert result_9.rank == HandRank.STRAIGHT
    assert result_8.rank == HandRank.STRAIGHT
    assert result_9.tiebreaker > result_8.tiebreaker


def test_tiebreaker_flush_compared_by_cards() -> None:
    """フラッシュで最高位カードから順に比較されること。"""
    cards_high = [
        make_card('A', '♠'), make_card('K', '♠'), make_card('Q', '♠'),
        make_card('J', '♠'), make_card('9', '♠'),
        make_card('2', '♥'), make_card('3', '♦'),
    ]
    cards_low = [
        make_card('A', '♠'), make_card('K', '♠'), make_card('Q', '♠'),
        make_card('J', '♠'), make_card('8', '♠'),
        make_card('2', '♥'), make_card('3', '♦'),
    ]
    result_high = evaluate(cards_high)
    result_low = evaluate(cards_low)
    assert result_high.rank == HandRank.FLUSH
    assert result_high.tiebreaker > result_low.tiebreaker


def test_tiebreaker_full_house_higher_three_wins() -> None:
    """フルハウスでスリーカードが大きい方が勝つこと（999+AA > 888+KK）。"""
    cards_999aa = [
        make_card('9', '♠'), make_card('9', '♥'), make_card('9', '♦'),
        make_card('A', '♣'), make_card('A', '♠'),
        make_card('2', '♥'), make_card('3', '♦'),
    ]
    cards_888kk = [
        make_card('8', '♠'), make_card('8', '♥'), make_card('8', '♦'),
        make_card('K', '♣'), make_card('K', '♠'),
        make_card('2', '♥'), make_card('3', '♦'),
    ]
    result_999 = evaluate(cards_999aa)
    result_888 = evaluate(cards_888kk)
    assert result_999.rank == HandRank.FULL_HOUSE
    assert result_888.rank == HandRank.FULL_HOUSE
    assert result_999.tiebreaker > result_888.tiebreaker


def test_tiebreaker_four_of_a_kind_higher_wins() -> None:
    """フォーオブアカインドで数字が大きい方が勝つこと（AAAA > KKKK）。"""
    cards_aaaa = [
        make_card('A', '♠'), make_card('A', '♥'),
        make_card('A', '♦'), make_card('A', '♣'),
        make_card('K', '♠'), make_card('Q', '♥'), make_card('J', '♦'),
    ]
    cards_kkkk = [
        make_card('K', '♠'), make_card('K', '♥'),
        make_card('K', '♦'), make_card('K', '♣'),
        make_card('A', '♠'), make_card('Q', '♥'), make_card('J', '♦'),
    ]
    result_aaaa = evaluate(cards_aaaa)
    result_kkkk = evaluate(cards_kkkk)
    assert result_aaaa.rank == HandRank.FOUR_OF_A_KIND
    assert result_kkkk.rank == HandRank.FOUR_OF_A_KIND
    assert result_aaaa.tiebreaker > result_kkkk.tiebreaker


def test_tiebreaker_royal_flush_always_tie() -> None:
    """ロイヤルフラッシュは tiebreaker が空タプルで常に同点であること。"""
    cards = [
        make_card('A', '♠'), make_card('K', '♠'), make_card('Q', '♠'),
        make_card('J', '♠'), make_card('T', '♠'),
        make_card('2', '♥'), make_card('3', '♦'),
    ]
    result = evaluate(cards)
    assert result.rank == HandRank.ROYAL_FLUSH
    assert result.tiebreaker == ()


def test_tiebreaker_identical_hands_true_tie() -> None:
    """完全に同一の手はtiebreaker も等しく真の引き分けになること。"""
    cards_a = [
        make_card('A', '♠'), make_card('K', '♥'), make_card('J', '♦'),
        make_card('9', '♣'), make_card('7', '♠'),
        make_card('5', '♥'), make_card('3', '♦'),
    ]
    cards_b = [
        make_card('A', '♣'), make_card('K', '♦'), make_card('J', '♣'),
        make_card('9', '♥'), make_card('7', '♦'),
        make_card('5', '♣'), make_card('3', '♥'),
    ]
    result_a = evaluate(cards_a)
    result_b = evaluate(cards_b)
    assert result_a.rank == result_b.rank
    assert result_a.tiebreaker == result_b.tiebreaker

# hand.py - 手役の判定ロジック

from dataclasses import dataclass
from enum import IntEnum
from itertools import combinations

from card import Card


class HandRank(IntEnum):
    """役の強さを表す列挙型。値が大きいほど強い。"""
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10


# HandRank と日本語役名のマッピング
_HAND_NAMES = {
    HandRank.HIGH_CARD: 'ハイカード',
    HandRank.ONE_PAIR: 'ワンペア',
    HandRank.TWO_PAIR: 'ツーペア',
    HandRank.THREE_OF_A_KIND: 'スリーオブアカインド',
    HandRank.STRAIGHT: 'ストレート',
    HandRank.FLUSH: 'フラッシュ',
    HandRank.FULL_HOUSE: 'フルハウス',
    HandRank.FOUR_OF_A_KIND: 'フォーオブアカインド',
    HandRank.STRAIGHT_FLUSH: 'ストレートフラッシュ',
    HandRank.ROYAL_FLUSH: 'ロイヤルフラッシュ',
}


@dataclass
class HandResult:
    """役判定の結果を格納するデータクラス。"""
    rank: HandRank
    name: str
    best_cards: list[Card]
    tiebreaker: tuple[int, ...]  # 同役時の比較キー（役ごとに異なる数値タプル）


def evaluate(cards: list[Card]) -> HandResult:
    """7枚のカードから最強の5枚の組み合わせを選び、役を判定して返す。"""
    # C(7,5) = 21通りの組み合わせの中から最高スコアのものを選ぶ
    best_five = max(combinations(cards, 5), key=_score_five)
    five = list(best_five)
    rank = _classify(five)
    tiebreaker = _compute_tiebreaker(five, rank)
    return HandResult(rank=rank, name=_HAND_NAMES[rank], best_cards=five, tiebreaker=tiebreaker)


def _score_five(five: tuple[Card, ...]) -> tuple[int, ...]:
    """5枚の組み合わせを比較用タプルに変換する。タプルのレキシコグラフィカル順で強さを比較できる。"""
    five_list = list(five)
    rank = _classify(five_list)
    return (rank.value, *_compute_tiebreaker(five_list, rank))


def _compute_tiebreaker(five: list[Card], rank: HandRank) -> tuple[int, ...]:
    """役に応じた同役比較用の数値タプルを返す。値が大きいほど強い。"""
    counts = _rank_counts(five)
    sorted_values = sorted([c.rank_value for c in five], reverse=True)

    if rank == HandRank.ROYAL_FLUSH:
        # ロイヤルフラッシュは常に同点
        return ()

    if rank in (HandRank.STRAIGHT_FLUSH, HandRank.STRAIGHT):
        # ストレートはホイール（最高位=5）を含めてストレート最高位で比較する
        high = _straight_high(five)
        return (high,)  # type: ignore[arg-type]

    if rank == HandRank.FOUR_OF_A_KIND:
        four_rank = next(v for v, cnt in counts.items() if cnt == 4)
        kicker = next(v for v, cnt in counts.items() if cnt == 1)
        return (four_rank, kicker)

    if rank == HandRank.FULL_HOUSE:
        three_rank = next(v for v, cnt in counts.items() if cnt == 3)
        pair_rank = next(v for v, cnt in counts.items() if cnt == 2)
        return (three_rank, pair_rank)

    if rank in (HandRank.FLUSH, HandRank.HIGH_CARD):
        # 降順5枚をそのまま比較キーにする
        return tuple(sorted_values)

    if rank == HandRank.THREE_OF_A_KIND:
        three_rank = next(v for v, cnt in counts.items() if cnt == 3)
        kickers = sorted([v for v, cnt in counts.items() if cnt == 1], reverse=True)
        return (three_rank, *kickers)

    if rank == HandRank.TWO_PAIR:
        pairs = sorted([v for v, cnt in counts.items() if cnt == 2], reverse=True)
        kicker = next(v for v, cnt in counts.items() if cnt == 1)
        return (*pairs, kicker)

    # ONE_PAIR
    pair_rank = next(v for v, cnt in counts.items() if cnt == 2)
    kickers = sorted([v for v, cnt in counts.items() if cnt == 1], reverse=True)
    return (pair_rank, *kickers)


def _classify(five: list[Card]) -> HandRank:
    """5枚のカードの役を判定して HandRank を返す。"""
    is_flush = _is_flush(five)
    straight_high = _straight_high(five)

    if is_flush and straight_high == 14:
        return HandRank.ROYAL_FLUSH
    if is_flush and straight_high is not None:
        return HandRank.STRAIGHT_FLUSH
    counts = _rank_counts(five)
    if 4 in counts.values():
        return HandRank.FOUR_OF_A_KIND
    if sorted(counts.values()) == [2, 3]:
        return HandRank.FULL_HOUSE
    if is_flush:
        return HandRank.FLUSH
    if straight_high is not None:
        return HandRank.STRAIGHT
    if 3 in counts.values():
        return HandRank.THREE_OF_A_KIND
    if list(counts.values()).count(2) == 2:
        return HandRank.TWO_PAIR
    if 2 in counts.values():
        return HandRank.ONE_PAIR
    return HandRank.HIGH_CARD


def _is_flush(five: list[Card]) -> bool:
    """5枚が全て同じスートであれば True を返す。"""
    return len({c.suit for c in five}) == 1


def _straight_high(five: list[Card]) -> int | None:
    """ストレートであれば最高位のrank_valueを返す。ストレートでなければ None を返す。

    A-2-3-4-5（ホイール）は最高位を5として扱う。
    """
    values = sorted({c.rank_value for c in five})
    # 重複があればストレートではない
    if len(values) < 5:
        return None
    # 通常のストレート: 最小値〜最大値が連続しているか確認する
    if values[-1] - values[0] == 4:
        return values[-1]
    # A-2-3-4-5（ホイール）: Aを1として扱うケース
    if values == [2, 3, 4, 5, 14]:
        return 5
    return None


def _rank_counts(five: list[Card]) -> dict[int, int]:
    """各rank_valueの出現回数を辞書で返す。"""
    counts: dict[int, int] = {}
    for card in five:
        counts[card.rank_value] = counts.get(card.rank_value, 0) + 1
    return counts

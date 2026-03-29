# test_game.py - Game クラスの結合テスト（主要パスのみ）

import sys
import os

# texas_holdem/ をインポートパスに追加する
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from card import Card
from game import Game, BIG_BLIND, SMALL_BLIND
from player import Player


# --- フィクスチャ ---

@pytest.fixture
def game() -> Game:
    """テスト用の Game インスタンスを返す。"""
    return Game(Player('あなた'), Player('CPU', is_cpu=True))


# --- ブラインド投票 ---

def test_post_blinds_player_chips(game: Game) -> None:
    """_post_blinds() 後にプレイヤーのチップが INITIAL_CHIPS - SMALL_BLIND になること。"""
    game._post_blinds()
    assert game.player.chips == 990  # 1000 - 10


def test_post_blinds_cpu_chips(game: Game) -> None:
    """_post_blinds() 後に CPU のチップが INITIAL_CHIPS - BIG_BLIND になること。"""
    game._post_blinds()
    assert game.cpu.chips == 980  # 1000 - 20


def test_post_blinds_pot(game: Game) -> None:
    """_post_blinds() 後にポットが SMALL_BLIND + BIG_BLIND になること。"""
    game._post_blinds()
    assert game.pot == 30  # 10 + 20


def test_post_blinds_current_bet(game: Game) -> None:
    """_post_blinds() 後に current_bet がビッグブラインド額（20）になること。"""
    game._post_blinds()
    assert game.current_bet == BIG_BLIND


# --- カード配布 ---

def test_deal_hole_cards_player_has_2(game: Game) -> None:
    """_deal_hole_cards() 後にプレイヤーが2枚の手札を持つこと。"""
    game._deal_hole_cards()
    assert len(game.player.hole_cards) == 2


def test_deal_hole_cards_cpu_has_2(game: Game) -> None:
    """_deal_hole_cards() 後に CPU が2枚の手札を持つこと。"""
    game._deal_hole_cards()
    assert len(game.cpu.hole_cards) == 2


def test_deal_community_3_cards(game: Game) -> None:
    """_deal_community(3) 後にコミュニティカードが3枚になること。"""
    game.deck.shuffle()
    game._deal_community(3)
    assert len(game.community_cards) == 3


def test_deal_community_flop_turn_river_total(game: Game) -> None:
    """フロップ・ターン・リバー合計でコミュニティカードが5枚になること。"""
    game.deck.shuffle()
    game._deal_community(3)  # フロップ
    game._deal_community(1)  # ターン
    game._deal_community(1)  # リバー
    assert len(game.community_cards) == 5


# --- ショーダウン ---

def test_showdown_winner_gets_pot(game: Game, capsys) -> None:
    """強い手役を持つ側がポットを獲得すること。

    プレイヤー: A♠ K♠（フラッシュが成立）
    CPU: 2♥ 3♦（ハイカード）
    コミュニティ: Q♠ J♠ 9♠ 5♣ 7♦
    """
    game.pot = 100
    # プレイヤーにフラッシュが成立する手札を設定する
    game.player.hole_cards = [Card('♠', 'A'), Card('♠', 'K')]
    game.cpu.hole_cards = [Card('♥', '2'), Card('♦', '3')]
    game.community_cards = [
        Card('♠', 'Q'), Card('♠', 'J'), Card('♠', '9'),
        Card('♣', '5'), Card('♦', '7'),
    ]
    chips_before = game.player.chips
    game._showdown()
    assert game.player.chips == chips_before + 100


def test_showdown_cpu_wins(game: Game, capsys) -> None:
    """CPUの手役が強い場合、CPUがポットを獲得すること。

    CPU: A♠ K♠（フラッシュが成立）
    プレイヤー: 2♥ 3♦（ハイカード）
    コミュニティ: Q♠ J♠ 9♠ 5♣ 7♦
    """
    game.pot = 100
    game.cpu.hole_cards = [Card('♠', 'A'), Card('♠', 'K')]
    game.player.hole_cards = [Card('♥', '2'), Card('♦', '3')]
    game.community_cards = [
        Card('♠', 'Q'), Card('♠', 'J'), Card('♠', '9'),
        Card('♣', '5'), Card('♦', '7'),
    ]
    chips_before = game.cpu.chips
    game._showdown()
    assert game.cpu.chips == chips_before + 100


def test_showdown_tie_splits_pot(game: Game, capsys) -> None:
    """引き分けの場合にポットが折半されること。

    両者ともコミュニティの A-K-Q-J-T ストレートが最強手となり引き分け。
    """
    game.pot = 100
    # どちらの手札もコミュニティのストレートを超えない
    game.player.hole_cards = [Card('♥', '2'), Card('♦', '3')]
    game.cpu.hole_cards = [Card('♦', '4'), Card('♣', '5')]
    game.community_cards = [
        Card('♠', 'A'), Card('♥', 'K'), Card('♦', 'Q'),
        Card('♣', 'J'), Card('♠', 'T'),
    ]
    player_chips_before = game.player.chips
    cpu_chips_before = game.cpu.chips
    game._showdown()
    assert game.player.chips == player_chips_before + 50   # 100 // 2
    assert game.cpu.chips == cpu_chips_before + 50


def test_showdown_player_fold_cpu_wins(game: Game, capsys) -> None:
    """フォールドしたプレイヤーが負け、CPUがポットを獲得すること。"""
    game._post_blinds()
    game._deal_hole_cards()
    pot = game.pot
    cpu_chips_before = game.cpu.chips
    game.player.is_folded = True
    game._showdown()
    assert game.cpu.chips == cpu_chips_before + pot


def test_showdown_cpu_fold_player_wins(game: Game, capsys) -> None:
    """CPUがフォールドした場合、プレイヤーがポットを獲得すること。"""
    game._post_blinds()
    game._deal_hole_cards()
    pot = game.pot
    player_chips_before = game.player.chips
    game.cpu.is_folded = True
    game._showdown()
    assert game.player.chips == player_chips_before + pot


# --- _betting_round() / フォールド（monkeypatch 使用）---

def test_player_fold_sets_is_folded(monkeypatch, game: Game) -> None:
    """プレイヤーが '4'（フォールド）を入力すると is_folded が True になること。"""
    # current_bet > player.current_bet にしてコール状況を作る（チェック無効化）
    game._post_blinds()
    game._deal_hole_cards()
    monkeypatch.setattr('builtins.input', lambda _: '4')
    game._betting_round()
    assert game.player.is_folded is True


def test_player_call_deducts_chips(monkeypatch, game: Game) -> None:
    """プレイヤーが '2'（コール）を入力するとチップが減ること。"""
    game._post_blinds()
    game._deal_hole_cards()
    chips_before = game.player.chips
    # コール額 = current_bet(20) - player.current_bet(10) = 10
    monkeypatch.setattr('builtins.input', lambda _: '2')
    game._betting_round()
    assert game.player.chips == chips_before - 10


# --- _cpu_action() のアクション選択ガード ---

def test_cpu_action_no_raise_when_chips_equal_call(game: Game) -> None:
    """CPUのチップがコール額と同じときは raise が返らないこと。"""
    game.current_bet = 100
    game.cpu.current_bet = 0
    game.cpu.chips = 100  # call_amount(100) == chips(100) → レイズ不可
    results = {game._cpu_action() for _ in range(200)}
    assert 'raise' not in results


def test_cpu_action_no_fold_when_no_bet(game: Game) -> None:
    """call_amount == 0 のときは fold が返らないこと。"""
    game.current_bet = 0
    game.cpu.current_bet = 0
    results = {game._cpu_action() for _ in range(200)}
    assert 'fold' not in results

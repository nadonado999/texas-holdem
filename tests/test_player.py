# test_player.py - Player クラスの単体テスト

import sys
import os

# texas_holdem/ をインポートパスに追加する
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from player import Player, INITIAL_CHIPS


# --- フィクスチャ ---

@pytest.fixture
def player() -> Player:
    """テスト用のプレイヤーを返す。"""
    return Player('あなた')


@pytest.fixture
def cpu() -> Player:
    """テスト用のCPUを返す。"""
    return Player('CPU', is_cpu=True)


# --- 初期状態 ---

def test_initial_chips(player: Player) -> None:
    """初期チップが INITIAL_CHIPS（1000）であること。"""
    assert player.chips == INITIAL_CHIPS


def test_initial_is_folded(player: Player) -> None:
    """初期状態で is_folded が False であること。"""
    assert player.is_folded is False


def test_initial_current_bet(player: Player) -> None:
    """初期状態で current_bet が 0 であること。"""
    assert player.current_bet == 0


def test_initial_hole_cards(player: Player) -> None:
    """初期状態で hole_cards が空リストであること。"""
    assert player.hole_cards == []


# --- is_cpu フラグ ---

def test_player_is_not_cpu(player: Player) -> None:
    """プレイヤーの is_cpu が False であること。"""
    assert player.is_cpu is False


def test_cpu_is_cpu(cpu: Player) -> None:
    """CPU の is_cpu が True であること。"""
    assert cpu.is_cpu is True


# --- bet() メソッド ---

def test_bet_reduces_chips(player: Player) -> None:
    """bet(amount) 後にチップが amount 分減ること。"""
    player.bet(100)
    assert player.chips == INITIAL_CHIPS - 100


def test_bet_increases_current_bet(player: Player) -> None:
    """bet(amount) 後に current_bet が amount 分増えること。"""
    player.bet(100)
    assert player.current_bet == 100


def test_bet_accumulates_current_bet(player: Player) -> None:
    """複数回 bet() を呼んだ場合に current_bet が累積されること。"""
    player.bet(100)
    player.bet(200)
    assert player.current_bet == 300


def test_bet_accumulates_chips_deduction(player: Player) -> None:
    """複数回 bet() を呼んだ場合にチップが累積して減ること。"""
    player.bet(100)
    player.bet(200)
    assert player.chips == INITIAL_CHIPS - 300


# --- reset_bet() メソッド ---

def test_reset_bet_clears_current_bet(player: Player) -> None:
    """reset_bet() 後に current_bet が 0 になること。"""
    player.bet(100)
    player.reset_bet()
    assert player.current_bet == 0


def test_reset_bet_does_not_change_chips(player: Player) -> None:
    """reset_bet() 後にチップは変化しないこと。"""
    player.bet(100)
    chips_after_bet = player.chips
    player.reset_bet()
    assert player.chips == chips_after_bet


# --- reset_round() メソッド ---

def test_reset_round_clears_hole_cards(player: Player) -> None:
    """reset_round() 後に hole_cards が空になること。"""
    from card import Card
    player.hole_cards = [Card('♠', 'A'), Card('♥', 'K')]
    player.reset_round()
    assert player.hole_cards == []


def test_reset_round_clears_is_folded(player: Player) -> None:
    """reset_round() 後に is_folded が False になること。"""
    player.is_folded = True
    player.reset_round()
    assert player.is_folded is False


def test_reset_round_clears_current_bet(player: Player) -> None:
    """reset_round() 後に current_bet が 0 になること。"""
    player.bet(100)
    player.reset_round()
    assert player.current_bet == 0


def test_reset_round_does_not_change_chips(player: Player) -> None:
    """reset_round() 後にチップは変化しないこと。"""
    player.bet(100)
    chips_after_bet = player.chips
    player.reset_round()
    assert player.chips == chips_after_bet

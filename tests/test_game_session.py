# test_game_session.py - GameSession クラスの結合テスト

import sys
import os

# texas_holdem/ をインポートパスに追加する
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from game_session import GameSession
from player import INITIAL_CHIPS


# --- フィクスチャ ---

@pytest.fixture
def session() -> GameSession:
    """テスト用の GameSession インスタンスを返す。"""
    return GameSession()


# --- 初期状態 ---

def test_initial_player_chips(session: GameSession) -> None:
    """プレイヤーの初期チップが INITIAL_CHIPS であること。"""
    assert session.player.chips == INITIAL_CHIPS


def test_initial_cpu_chips(session: GameSession) -> None:
    """CPU の初期チップが INITIAL_CHIPS であること。"""
    assert session.cpu.chips == INITIAL_CHIPS


# --- ラウンド間のチップ引き継ぎ ---

def test_chips_carry_over_between_rounds(monkeypatch, session: GameSession) -> None:
    """Game に渡される player/cpu が session と同一オブジェクトであること。

    _play_round() 内で Game に渡す player と cpu は session が保持するものと
    同一インスタンスであるため、ラウンド後のチップ変動がそのまま引き継がれる。
    """
    captured = {}

    original_init = __import__('game').Game.__init__

    def mock_init(self, player, cpu):
        captured['player'] = player
        captured['cpu'] = cpu
        original_init(self, player, cpu)

    monkeypatch.setattr('game.Game.__init__', mock_init)
    # フォールドを入力してラウンドをすぐ終了させる
    monkeypatch.setattr('builtins.input', lambda _: '4')
    session._play_round()

    assert captured['player'] is session.player
    assert captured['cpu'] is session.cpu


# --- ゲーム終了条件 ---

def test_session_ends_when_player_chips_zero(monkeypatch, session: GameSession, capsys) -> None:
    """プレイヤーのチップが0になったらループが終了すること。"""
    session.player.chips = 0
    monkeypatch.setattr('builtins.input', lambda _: '4')
    session.run()
    output = capsys.readouterr().out
    assert 'ゲーム終了' in output


def test_session_ends_when_cpu_chips_zero(monkeypatch, session: GameSession, capsys) -> None:
    """CPU のチップが0になったらループが終了すること。"""
    session.cpu.chips = 0
    monkeypatch.setattr('builtins.input', lambda _: '4')
    session.run()
    output = capsys.readouterr().out
    assert 'ゲーム終了' in output


# --- ラウンド番号 ---

def test_round_number_increments(monkeypatch, session: GameSession) -> None:
    """ラウンドをプレイするたびに round_number が加算されること。"""
    call_count = [0]

    def mock_play_round():
        call_count[0] += 1
        # 2ラウンド後にCPUのチップを0にしてループを止める
        if call_count[0] >= 2:
            session.cpu.chips = 0

    monkeypatch.setattr(session, '_play_round', mock_play_round)
    monkeypatch.setattr('builtins.input', lambda _: '4')
    session.run()
    assert session.round_number == 2

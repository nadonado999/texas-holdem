# game.py - ゲーム進行全体の制御（ブラインド・ベッティング・ショーダウン）

import random

from card import Card, Deck
from hand import evaluate
from player import Player

SMALL_BLIND = 10   # スモールブラインド額（プレイヤー固定）
BIG_BLIND = 20     # ビッグブラインド額（CPU固定）


class Game:
    """ゲーム進行全体を管理するクラス。"""

    def __init__(self) -> None:
        self.player = Player('あなた')
        self.cpu = Player('CPU', is_cpu=True)
        self.deck = Deck()
        self.community_cards: list[Card] = []
        self.pot: int = 0
        self.current_bet: int = 0

    def start(self) -> None:
        """ゲームを開始し、1ラウンドを進行する。"""
        print('=' * 40)
        print('  テキサスホールデムポーカー')
        print('=' * 40)

        # ブラインド投票・手札配布
        self._post_blinds()
        self._deal_hole_cards()

        # プリフロップ
        self._betting_round()
        if self._is_game_over():
            self._showdown()
            return

        # フロップ
        self._reset_street()
        self._deal_community(3)
        self._betting_round()
        if self._is_game_over():
            self._showdown()
            return

        # ターン
        self._reset_street()
        self._deal_community(1)
        self._betting_round()
        if self._is_game_over():
            self._showdown()
            return

        # リバー
        self._reset_street()
        self._deal_community(1)
        self._betting_round()

        # ショーダウン（フォールドの有無に関わらず呼ぶ）
        self._showdown()

    def _post_blinds(self) -> None:
        """ブラインド投票を行う。プレイヤーがスモール、CPUがビッグに固定。"""
        self.player.bet(SMALL_BLIND)
        self.pot += SMALL_BLIND
        self.cpu.bet(BIG_BLIND)
        self.pot += BIG_BLIND
        self.current_bet = BIG_BLIND
        print(f'  {self.player.name}: スモールブラインド {SMALL_BLIND} チップ')
        print(f'  {self.cpu.name}: ビッグブラインド {BIG_BLIND} チップ')
        print(f'  ポット: {self.pot} チップ')

    def _deal_hole_cards(self) -> None:
        """デッキをシャッフルし、各プレイヤーに手札を2枚配る。"""
        self.deck.shuffle()
        for _ in range(2):
            self.player.hole_cards.append(self.deck.deal())
            self.cpu.hole_cards.append(self.deck.deal())

    def _deal_community(self, n: int) -> None:
        """コミュニティカードをn枚デッキから公開する。"""
        for _ in range(n):
            self.community_cards.append(self.deck.deal())

    def _betting_round(self) -> None:
        """1回のベッティングラウンドを処理する。"""
        self._display_state()
        self._process_player_action()
        if self.player.is_folded:
            return
        self._process_cpu_action()

    def _process_player_action(self) -> None:
        """プレイヤーのアクションを受け取り、状態に反映する。"""
        action = self._player_action()
        call_amount = self.current_bet - self.player.current_bet

        if action == '1':  # チェック
            print(f'  {self.player.name}: チェック')
        elif action == '2':  # コール
            self.player.bet(call_amount)
            self.pot += call_amount
            print(f'  {self.player.name}: コール（{call_amount} チップ）')
        elif action == '3':  # レイズ
            raise_amount = self._input_raise_amount()
            total = call_amount + raise_amount
            self.player.bet(total)
            self.pot += total
            self.current_bet = self.player.current_bet
            print(f'  {self.player.name}: レイズ（+{raise_amount} チップ）')
        elif action == '4':  # フォールド
            self.player.is_folded = True
            print(f'  {self.player.name}: フォールド')

    def _process_cpu_action(self) -> None:
        """CPUのアクションを決定し、状態に反映する。"""
        action = self._cpu_action()
        call_amount = self.current_bet - self.cpu.current_bet

        if action == 'check':
            print(f'  {self.cpu.name}: チェック')
        elif action == 'call':
            self.cpu.bet(call_amount)
            self.pot += call_amount
            print(f'  {self.cpu.name}: コール（{call_amount} チップ）')
        elif action == 'raise':
            # レイズ額はCPUの残りチップの範囲でランダムに決定する
            max_raise = self.cpu.chips - call_amount
            raise_amount = random.randint(1, max(1, max_raise // 2))
            total = call_amount + raise_amount
            self.cpu.bet(total)
            self.pot += total
            self.current_bet = self.cpu.current_bet
            print(f'  {self.cpu.name}: レイズ（+{raise_amount} チップ）')
        elif action == 'fold':
            self.cpu.is_folded = True
            print(f'  {self.cpu.name}: フォールド')

    def _player_action(self) -> str:
        """プレイヤーのアクション入力を受け取る。不正な入力は再入力を促す。"""
        call_amount = self.current_bet - self.player.current_bet
        while True:
            print('アクションを選択してください:')
            print('  1: チェック  2: コール  3: レイズ  4: フォールド')
            choice = input('> ').strip()
            if choice not in ('1', '2', '3', '4'):
                print('  ※ 1〜4 の数字を入力してください。')
                continue
            # チェックはベットがない場合のみ有効
            if choice == '1' and call_amount > 0:
                print('  ※ ベットされているのでチェックできません。')
                continue
            # コールはベットがある場合のみ有効
            if choice == '2' and call_amount == 0:
                print('  ※ ベットがないのでコールできません。')
                continue
            return choice

    def _input_raise_amount(self) -> int:
        """レイズ額の入力を受け取る。不正な入力は再入力を促す。"""
        call_amount = self.current_bet - self.player.current_bet
        max_raise = self.player.chips - call_amount
        while True:
            try:
                amount = int(input(f'レイズ額を入力してください (1〜{max_raise}): '))
            except ValueError:
                print('  ※ 数値を入力してください。')
                continue
            if amount <= 0 or amount > max_raise:
                print(f'  ※ 1〜{max_raise} の範囲で入力してください。')
                continue
            return amount

    def _cpu_action(self) -> str:
        """CPUのアクションをランダムに選択して返す。"""
        call_amount = self.current_bet - self.cpu.current_bet
        # チップが足りない場合はフォールド
        if call_amount > self.cpu.chips:
            return 'fold'
        # ベットされている場合はチェックを選択肢から除外する
        if call_amount > 0:
            return random.choice(['call', 'raise', 'fold'])
        else:
            return random.choice(['check', 'raise', 'fold'])

    def _showdown(self) -> None:
        """役を比較して勝者を決定し、ポットを分配する。"""
        # フォールドによる決着を先に確認する
        if self.player.is_folded:
            self.cpu.chips += self.pot
            self._display_state(reveal_cpu=True)
            print(f'\n{self.cpu.name}の勝ち（{self.player.name}がフォールド）')
            return
        if self.cpu.is_folded:
            self.player.chips += self.pot
            self._display_state(reveal_cpu=True)
            print(f'\n{self.player.name}の勝ち（{self.cpu.name}がフォールド）')
            return

        # 手役の判定（手札2枚 + コミュニティ5枚）
        player_result = evaluate(self.player.hole_cards + self.community_cards)
        cpu_result = evaluate(self.cpu.hole_cards + self.community_cards)

        self._display_state(reveal_cpu=True)
        print(f'\n  {self.player.name}の役: {player_result.name}')
        print(f'  {self.cpu.name}の役:  {cpu_result.name}')

        if player_result.rank > cpu_result.rank:
            self.player.chips += self.pot
            print(f'\n{self.player.name}の勝ち！ {self.pot} チップ獲得')
        elif cpu_result.rank > player_result.rank:
            self.cpu.chips += self.pot
            print(f'\n{self.cpu.name}の勝ち！ {self.pot} チップ獲得')
        else:
            # 同役は引き分け。端数は切り捨て
            half = self.pot // 2
            self.player.chips += half
            self.cpu.chips += half
            print(f'\n引き分け！ ポットを折半（各 {half} チップ）')

    def _reset_street(self) -> None:
        """ストリート間のベット状態をリセットする。"""
        self.current_bet = 0
        self.player.reset_bet()
        self.cpu.reset_bet()

    def _is_game_over(self) -> bool:
        """いずれかのプレイヤーがフォールドしていれば True を返す。"""
        return self.player.is_folded or self.cpu.is_folded

    def _display_state(self, reveal_cpu: bool = False) -> None:
        """現在の盤面をターミナルに表示する。

        reveal_cpu が True のときCPUの手札を公開する（ショーダウン時に使用）。
        """
        print('\n' + '=' * 40)
        print(f'【ポット】 {self.pot} チップ')
        print()

        # コミュニティカード（5枚分のスロットを表示）
        community_str = ''
        for i in range(5):
            if i < len(self.community_cards):
                community_str += f'[{str(self.community_cards[i]):3s}]'
            else:
                community_str += '[   ]'
        print('【コミュニティカード】')
        print(f'  {community_str}')
        print()

        # CPUの手札（ショーダウン前はマスク表示）
        if reveal_cpu and self.cpu.hole_cards:
            cpu_cards = ' '.join(f'[{str(c):3s}]' for c in self.cpu.hole_cards)
        else:
            cpu_cards = '[???] [???]'
        print(f'【{self.cpu.name}の手札】')
        print(f'  {cpu_cards}   チップ: {self.cpu.chips}')
        print()

        # プレイヤーの手札
        if self.player.hole_cards:
            player_cards = ' '.join(f'[{str(c):3s}]' for c in self.player.hole_cards)
        else:
            player_cards = '（未配布）'
        print(f'【{self.player.name}の手札】')
        print(f'  {player_cards}   チップ: {self.player.chips}')
        print('-' * 40)

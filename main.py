import tkinter
import tkinter.font as tf
import tkinter.messagebox as msg
import datetime
import time
import math
import voice


class TimerFrame(tkinter.Frame):
    is_stop = False

    def parse_input(self):
        """
        エントリーから時間を取得
        :return: list[int]
        :raises ValueError: entry_1の入力が不正
        """
        str_input = self.entry_1.get().split(':')
        min_sec = list(map(lambda num: int(num), str_input))

        if len(min_sec) > 2:
            raise ValueError

        return min_sec

    def update_entry(self, delta):
        """
        エントリーを更新
        :param delta: time.timedelta
        :return:
        """
        # エントリーをクリア
        self.entry_1.delete(0, tkinter.END)
        # タイムデルタがマイナスの場合は0:00にして終了
        if delta.days == -1:
            self.entry_1.insert(0, '0:00')
            self.update()
            return

        # タイムデルタから秒とマイクロ秒を取得
        sec = delta.seconds
        m_sec = delta.microseconds
        # マイクロ秒を秒に変換し、secに加算（小数点以下切り上げ)
        sec += math.ceil(m_sec * 10**-6)

        # エントリーに表示する文字列を作成
        str_time = '{0:d}:{1:02d}'.format(sec // 60, sec % 60)
        self.entry_1.insert(0, str_time)

        # GUIを更新
        self.update()

    def start_timer(self):
        # エントリーから時間を取得
        try:
            input_time = self.parse_input()
        except ValueError:
            # エラーダイアログを表示
            msg.showerror('入力エラー', '時間が正しく入力されていません。')
            return

        # 入力から目標時刻を計算する
        target_time = datetime.datetime.now()
        if len(input_time) == 2:
            target_time += datetime.timedelta(minutes=input_time[0])
        target_time += datetime.timedelta(seconds=input_time[-1])

        while True:
            if self.is_stop:
                self.is_stop = False
                return

            # 現在時刻を取得
            current_time = datetime.datetime.now()
            # 目標時刻と現在時刻のタイムデルタを取得
            time_delta = target_time - current_time
            # エントリー更新
            self.update_entry(time_delta)
            # 目標時刻に到達したか判定
            if time_delta < datetime.timedelta():
                # ボイス再生
                self.akane_player.play('akane.wav')
                return

            # 0.1秒待機
            time.sleep(0.1)

    def stop_timer(self):
        self.is_stop = True

    def resize_font(self, event):
        """
        ウィンドウサイズに合わせてフォントサイズを変更する
        :param event:
        :return:
        """
        height = self.master.winfo_height()
        if height < 40:
            self.font.configure(size=10)
        elif height < 60:
            self.font.configure(size=20)
        elif height < 100:
            self.font.configure(size=30)
        else:
            self.font.configure(size=40)

    def close(self):
        self.akane_player.__del__()

    def __init__(self, master=None):
        # 基底クラスのコンストラクタ呼び出し
        super().__init__(master)
        # masterのプロパティ設定
        self.master.title('茜ちゃんタイマー')
        self.master.geometry('400x200')
        self.master.protocol("WM_DELETE_WINDOW", self.close)

        # フォント
        self.font = tf.Font(family='Lucida Console', size=40)

        # ラベル
        self.label_1 = tkinter.Label(text='時間')
        self.label_1.place(relx=0, relheight=0.5, relwidth=0.3)
        # エントリー
        self.entry_1 = tkinter.Entry(font=self.font)
        self.entry_1.place(relx=0.3, relheight=0.5, relwidth=0.7)
        # ボタン
        self.start_button = tkinter.Button(text='開始', command=self.start_timer)
        self.start_button.place(relx=0, rely=0.5, relheight=0.5, relwidth=0.5)
        self.stop_button = tkinter.Button(text='停止', command=self.stop_timer)
        self.stop_button.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=0.5)

        # イベント
        self.bind('<Configure>', self.resize_font)

        self.akane_player = voice.AkanePlayer()


if __name__ == '__main__':
    app = TimerFrame()
    app.pack()
    app.mainloop()

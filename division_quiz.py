import random  # 乱数を生成するためのライブラリ
import time     # 時間を扱うためのライブラリ
from IPython.display import clear_output  # 画面をクリアするためのライブラリ
import ipywidgets as widgets  # ボタンなどのウィジェットを使うためのライブラリ
from IPython.display import display  # ウィジェットを表示するための関数

def main():
    """ゲームのメイン処理を行う関数"""
    # 変数の初期化
    divided_numbers = []  # 割られる数を保存するリスト
    divisor_numbers = []  # 割る数を保存するリスト
    current_problem = 0   # 現在の問題番号
    correct_answers = 0   # 正解数
    total_problems = 10   # 問題の総数

    # YESとNOのボタンを作成（ウィジェット）
    yes_button = widgets.Button(
        description="YES (割り切れる)",  # ボタンに表示するテキスト
        button_style='success',          # ボタンの色（緑色）
        layout=widgets.Layout(width='200px')  # ボタンの幅
    )

    no_button = widgets.Button(
        description="NO (割り切れない)",  # ボタンに表示するテキスト
        button_style='danger',           # ボタンの色（赤色）
        layout=widgets.Layout(width='200px')  # ボタンの幅
    )

    # その他のボタンを作成
    start_button = widgets.Button(
        description="ゲーム開始",
        button_style='info',             # ボタンの色（青色）
        layout=widgets.Layout(width='200px')
    )

    next_button = widgets.Button(
        description="次の問題へ",
        button_style='info',
        layout=widgets.Layout(width='200px')
    )

    # 結果表示用のテキスト領域
    result_text = widgets.Output()

    # 10問分の問題を生成
    for i in range(total_problems):
        # ランダムな数字を生成
        divided_num = random.randint(10, 1000)          # 10から1000までのランダムな数
        divisor_num = random.randint(2, i + 3)          # 2から問題番号+3までのランダムな数

        # 生成した数字をリストに保存
        divided_numbers.append(divided_num)
        divisor_numbers.append(divisor_num)

    def show_problem(problem_num):
        """問題を表示する関数

        引数:
            problem_num: 表示する問題の番号
        """
        nonlocal current_problem  # 外側の関数の変数にアクセスする宣言
        current_problem = problem_num

        # すべての問題が終了した場合
        if problem_num >= total_problems:
            show_final_results()  # 最終結果を表示する関数を呼び出す
            return

        clear_output(wait=True)  # 画面をクリア

        # 現在の問題の数字を取得
        divided_num = divided_numbers[problem_num]
        divisor_num = divisor_numbers[problem_num]

        # 問題を表示
        print(f"問題 {problem_num + 1}/{total_problems}")
        print(f"{divided_num} ÷ {divisor_num}")
        print("割り切れる？ 割り切れない？")
        print("YESは「y」キー、NOは「n」キーを押してください")

        # キー入力処理用のテキスト入力ボックス
        text_input = widgets.Text(
            description='回答:',
            placeholder='yかnを入力'
        )

        # キー入力を処理する関数
        def on_text_submit(sender):
            value = text_input.value.lower()  # 小文字に変換
            if value == 'y':
                check_answer(True)  # YESの場合
            elif value == 'n':
                check_answer(False)  # NOの場合
            else:
                # 無効な入力の場合はメッセージを表示
                with result_text:
                    result_text.clear_output()
                    print("「y」か「n」を入力してください")

        # Enterキーが押されたときの処理を設定
        text_input.on_submit(on_text_submit)

        # ウィジェットを表示
        display(text_input)
        display(result_text)

    def check_answer(user_answer):
        """ユーザーの回答が正しいかチェックする関数

        引数:
            user_answer: ユーザーの回答（TrueがYES、FalseがNO）
        """
        nonlocal correct_answers  # 外側の関数の変数にアクセスする宣言

        # 現在の問題の数字を取得
        divided_num = divided_numbers[current_problem]
        divisor_num = divisor_numbers[current_problem]

        # 割り切れるかどうかを計算
        is_divisible = (divided_num % divisor_num == 0)  # 余りが0なら割り切れる

        # 回答が正しいかチェック
        is_correct = (user_answer == is_divisible)

        # 以前の結果表示をクリア
        result_text.clear_output()

        # 結果を表示
        with result_text:
            print("うーん...")
            time.sleep(1)  # 演出のための1秒待機

            if is_correct:
                print("正解!!")
                correct_answers += 1  # 正解数を1増やす
            else:
                print("不正解")

            # 正しい計算結果を表示
            remainder = divided_num % divisor_num  # 余りを計算
            if remainder == 0:
                print(f"{divided_num} ÷ {divisor_num} = {divided_num // divisor_num} (余り 0)")
                print("割り切れます！")
            else:
                print(f"{divided_num} ÷ {divisor_num} = {divided_num // divisor_num} (余り {remainder})")
                print("割り切れません！")

        # 現在の問題表示をクリアして結果と次へボタンを表示
        clear_output(wait=True)
        print(f"問題 {current_problem + 1}/{total_problems}")
        print(f"{divided_num} ÷ {divisor_num}")
        display(result_text)  # 結果を表示
        display(next_button)  # 次へボタンを表示

    def show_final_results():
        """最終結果を表示する関数"""
        clear_output(wait=True)  # 画面をクリア
        print("クイズ終了!")
        print(f"正解数: {correct_answers}/{total_problems}")
        print(f"正解率: {(correct_answers/total_problems)*100:.1f}%")

        # 正解数に応じたバッジ（称号）を表示
        badges = [
            "アキレスを追い越せない亀",       # 0-1問正解
            "ピタゴラス音階の調律師",         # 2-3問正解
            "フェルマーの弟子",               # 4-5問正解
            "オイラーの計算機",               # 6-7問正解
            "ガウスの後継者",                 # 8-9問正解
            "ガロアの継承者"                  # 10問正解
        ]

        # 正解数に応じたバッジの索引を計算（2問正解ごとに1ランクアップ）
        badge_index = min(correct_answers // 2, 5)
        badge = badges[badge_index]

        print("\n≪ 獲得称号 ≫")
        print("＊" * 20)
        print(f"★ {badge} ★")
        print("＊" * 20)

        # ランクごとのコメントを表示
        comments = [
            "数学の世界はまだ謎だらけ...もう一度挑戦してみよう！",
            "基本が見えてきました。これからが楽しみです！",
            "なかなかの才能の持ち主！さらに高みを目指そう！",
            "かなりの腕前！計算の達人になれる素質があります！",
            "素晴らしい！あなたの頭脳は一般人を超えています！",
            "天才的！あなたは数学の申し子です！"
        ]
        print(comments[badge_index])

        # もう一度プレイするボタン
        restart_button = widgets.Button(
            description="もう一度プレイする",
            button_style='primary',
            layout=widgets.Layout(width='200px')
        )

        # もう一度プレイボタンがクリックされたときの処理
        def on_restart_click(b):
            """ゲームを再開する関数"""
            main()  # メイン関数を再度呼び出す

        restart_button.on_click(on_restart_click)  # ボタンにクリック時の動作を設定
        display(restart_button)  # ボタンを表示

    def on_yes_click(b):
        """YESボタンがクリックされたときの処理を行う関数"""
        check_answer(True)  # 回答をチェック（YES=True）

    def on_no_click(b):
        """NOボタンがクリックされたときの処理を行う関数"""
        check_answer(False)  # 回答をチェック（NO=False）

    def on_start_click(b):
        """スタートボタンがクリックされたときの処理を行う関数"""
        clear_output(wait=True)  # 画面をクリア
        print("割切れる？割切れない？電卓クイズ!!")
        print("クイズスタート!!")
        time.sleep(1)  # 1秒待機
        show_problem(0)  # 最初の問題を表示

    def on_next_click(b):
        """次へボタンがクリックされたときの処理を行う関数"""
        show_problem(current_problem + 1)  # 次の問題を表示

    # ボタンにクリック時の動作を設定
    yes_button.on_click(on_yes_click)
    no_button.on_click(on_no_click)
    start_button.on_click(on_start_click)
    next_button.on_click(on_next_click)

    # 初期画面の表示
    print("割切れる？割切れない？電卓クイズ!!")
    print("各問題で数字が表示されます。最初の数が2番目の数で割り切れるかどうかを答えてください。")
    print("準備ができたらゲーム開始ボタンを押してください。")
    display(start_button)  # スタートボタンを表示

# ゲームを実行
main()

import streamlit as st
import random
import time

def main():
    # セッション状態の初期化（ページのリロード時にも状態を保持するため）
    if 'initialized' not in st.session_state:
        initialize_game()

    # ゲームの状態に応じた画面表示
    if st.session_state.game_state == 'start':
        show_start_screen()
    elif st.session_state.game_state == 'problem':
        show_problem()
    elif st.session_state.game_state == 'result':
        show_result()
    elif st.session_state.game_state == 'final':
        show_final_results()

def initialize_game():
    """ゲームの状態を初期化する関数"""
    st.session_state.initialized = True
    st.session_state.game_state = 'start'
    st.session_state.divided_numbers = []
    st.session_state.divisor_numbers = []
    st.session_state.current_problem = 0
    st.session_state.correct_answers = 0
    st.session_state.total_problems = 10
    st.session_state.user_answer = None
    st.session_state.answer_checked = False
    
    # 10問分の問題を生成
    for i in range(st.session_state.total_problems):
        # ランダムな数字を生成
        divided_num = random.randint(10, 1000)  # 10から1000までのランダムな数
        divisor_num = random.randint(2, i + 3)  # 2から問題番号+3までのランダムな数
        
        # 生成した数字をリストに保存
        st.session_state.divided_numbers.append(divided_num)
        st.session_state.divisor_numbers.append(divisor_num)

def show_start_screen():
    """初期画面を表示する関数"""
    st.title("割切れる？割切れない？電卓クイズ!!")
    st.write("各問題で数字が表示されます。最初の数が2番目の数で割り切れるかどうかを答えてください。")
    
    if st.button("ゲーム開始", key="start_button"):
        st.session_state.game_state = 'problem'
        st.rerun()

def show_problem():
    """問題を表示する関数"""
    # すべての問題が終了した場合
    if st.session_state.current_problem >= st.session_state.total_problems:
        st.session_state.game_state = 'final'
        st.rerun()
        return
    
    # 現在の問題の数字を取得
    divided_num = st.session_state.divided_numbers[st.session_state.current_problem]
    divisor_num = st.session_state.divisor_numbers[st.session_state.current_problem]
    
    # 問題を表示
    st.title(f"問題 {st.session_state.current_problem + 1}/{st.session_state.total_problems}")
    st.subheader(f"{divided_num} ÷ {divisor_num}")
    st.write("割り切れる？ 割り切れない？")
    
    # 回答ボタン（すでに回答がチェックされていなければ表示）
    if not st.session_state.answer_checked:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("YES (割り切れる)", type="primary"):
                check_answer(True)
                st.rerun()
        with col2:
            if st.button("NO (割り切れない)", type="secondary"):
                check_answer(False)
                st.rerun()
    
    # 回答がチェック済みなら結果を表示
    if st.session_state.answer_checked:
        show_result()

def check_answer(user_answer):
    """ユーザーの回答が正しいかチェックする関数"""
    # 現在の問題の数字を取得
    divided_num = st.session_state.divided_numbers[st.session_state.current_problem]
    divisor_num = st.session_state.divisor_numbers[st.session_state.current_problem]
    
    # 割り切れるかどうかを計算
    is_divisible = (divided_num % divisor_num == 0)  # 余りが0なら割り切れる
    
    # 回答が正しいかチェック
    is_correct = (user_answer == is_divisible)
    
    # 結果を保存
    st.session_state.user_answer = user_answer
    st.session_state.is_correct = is_correct
    st.session_state.is_divisible = is_divisible
    st.session_state.answer_checked = True
    
    # 正解数を更新
    if is_correct:
        st.session_state.correct_answers += 1
    
    # ゲーム状態を結果表示に変更
    st.session_state.game_state = 'result'

def show_result():
    """回答結果を表示する関数"""
    divided_num = st.session_state.divided_numbers[st.session_state.current_problem]
    divisor_num = st.session_state.divisor_numbers[st.session_state.current_problem]
    
    # 正しい計算結果を取得
    remainder = divided_num % divisor_num  # 余りを計算
    quotient = divided_num // divisor_num  # 商を計算
    
    # 結果を表示
    if st.session_state.is_correct:
        st.success("正解!!")
    else:
        st.error("不正解")
    
    # 計算結果の詳細を表示
    if remainder == 0:
        st.write(f"{divided_num} ÷ {divisor_num} = {quotient} (余り 0)")
        st.write("割り切れます！")
    else:
        st.write(f"{divided_num} ÷ {divisor_num} = {quotient} (余り {remainder})")
        st.write("割り切れません！")
    
    # 次の問題へ進むボタン
    if st.button("次の問題へ", key="next_button"):
        st.session_state.current_problem += 1
        st.session_state.answer_checked = False
        st.session_state.game_state = 'problem'
        st.rerun()

def show_final_results():
    """最終結果を表示する関数"""
    st.title("クイズ終了!")
    
    # 正解数と正解率を表示
    correct = st.session_state.correct_answers
    total = st.session_state.total_problems
    percentage = (correct / total) * 100
    
    st.write(f"正解数: {correct}/{total}")
    st.write(f"正解率: {percentage:.1f}%")
    
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
    badge_index = min(correct // 2, 5)
    badge = badges[badge_index]
    
    # 称号とコメントを表示
    st.subheader("≪ 獲得称号 ≫")
    st.markdown(f"### ★ {badge} ★")
    
    # ランクごとのコメントを表示
    comments = [
        "数学の世界はまだ謎だらけ...もう一度挑戦してみよう！",
        "基本が見えてきました。これからが楽しみです！",
        "なかなかの才能の持ち主！さらに高みを目指そう！",
        "かなりの腕前！計算の達人になれる素質があります！",
        "素晴らしい！あなたの頭脳は一般人を超えています！",
        "天才的！あなたは数学の申し子です！"
    ]
    st.write(comments[badge_index])
    
    # もう一度プレイするボタン
    if st.button("もう一度プレイする", key="restart_button"):
        initialize_game()
        st.rerun()

if __name__ == "__main__":
    # ページの設定
    st.set_page_config(
        page_title="割切れる？割切れない？電卓クイズ",
        page_icon="🧮",
        layout="centered"
    )
    
    # メイン処理を実行
    main()
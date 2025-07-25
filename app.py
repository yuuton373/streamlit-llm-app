# ----------------------------------------------------------------
# 1. 必要なライブラリをインポートする
# ----------------------------------------------------------------
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

# ----------------------------------------------------------------
# 2. 環境変数を読み込む
# ----------------------------------------------------------------
# .envファイルから環境変数（OPENAI_API_KEY）を読み込む
load_dotenv() 

# ----------------------------------------------------------------
# 3. LLMに回答を生成させる関数を定義する
# ----------------------------------------------------------------
# この関数は、ユーザーの入力(user_question)と、専門家の選択(expert_choice)を
# 引数として受け取り、LLMからの回答を返す
def get_llm_response(user_question, expert_choice):
    
    # ラジオボタンの選択に応じて、LLMの役割（システムメッセージ）を変える
    if expert_choice == "ITコンサルタント":
        system_message = "あなたは優秀なITコンサルタントです。専門用語を避け、初心者にも分かりやすく回答してください。"
    elif expert_choice == "恋愛カウンセラー":
        system_message = "あなたは経験豊富な恋愛カウンセラーです。親身に、そして具体的なアドバイスをしてください。"
    elif expert_choice == "シェフ":
        system_message = "あなたは一流のシェフです。家庭でも作れる簡単なレシピのアイデアを提案してください。"
    else:
        # 万が一、予期せぬ選択があった場合のデフォルト設定
        system_message = "あなたは親切なアシスタントです。"

    # --- LangChainのコード（Lesson8参考） ---
    # LLMモデル（gpt-4o-mini）を準備する
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
    
    # LLMに渡すメッセージを作成する
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_question),
    ]
    
    # LLMに質問を投げて、結果を受け取る
    result = llm.invoke(messages)
    
    # 結果からテキスト部分だけを取り出して返す
    return result.content

# ----------------------------------------------------------------
# 4. Streamlitアプリの画面を作成する
# ----------------------------------------------------------------

# アプリのタイトルを設定
st.title("専門家AIチャットボット")

# アプリの概要や操作方法を説明
st.write("##### 概要")
st.write("このアプリは、さまざまな分野の専門家として振る舞うAIに質問できるチャットボトットです。")
st.write("##### 操作方法")
st.markdown("""
1. 相談したい専門家をラジオボタンから選択してください。
2. 下のテキストエリアに、専門家への質問や相談事を入力してください。
3. 「AIに相談する」ボタンを押すと、AIからの回答が表示されます。
""")

st.divider() # 区切り線

# ラジオボタンで専門家を選択させる
expert_choice = st.radio(
    "どの専門家に相談しますか？",
    ("ITコンサルタント", "恋愛カウンセラー", "シェフ")
)

# ユーザーが質問を入力するためのテキストエリア
user_question = st.text_area("相談したい内容を入力してください。")

# 実行ボタン
if st.button("AIに相談する"):
    st.divider() # 区切り線

    # ユーザーが何か入力した場合のみ、処理を実行
    if user_question:
        # 処理中であることをユーザーに知らせる
        with st.spinner("AIが回答を考えています..."):
            # 上で定義した関数を使って、LLMからの回答を取得
            response = get_llm_response(user_question, expert_choice)
        
        # 結果を表示する
        st.subheader("🤖 AIからの回答")
        st.markdown(response)

    else:
        # 入力がない場合はエラーメッセージを表示
        st.error("相談したい内容を入力してください。")
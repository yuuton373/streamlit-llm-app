import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

# .envファイルから環境変数（OPENAI_API_KEY）を読み込む
load_dotenv() 

# この関数は、ユーザーの入力(user_question)と、専門家の選択(expert_choice)を
# 引数として受け取り、LLMからの回答を返す
def get_llm_response(user_question, expert_choice):
    
    # StreamlitのSecretsからAPIキーを直接読み込む
    try:
        # Streamlit CloudのSecretsから読み込みを試みる
        api_key = st.secrets["OPENAI_API_KEY"]
    except (KeyError, FileNotFoundError):
        # 失敗した場合（ローカル実行時など）は、.envから読み込まれた環境変数を使う
        # このためには import os が必要
        import os
        api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        st.error("OpenAIのAPIキーが設定されていません。")
        return "APIキーが設定されていないため、回答を生成できません。"
    # ★★★ ここまで修正 ★★★

    if expert_choice == "ITコンサルタント":
        system_message = "あなたは優秀なITコンサルタントです。専門用語を避け、初心者にも分かりやすく回答してください。"
    elif expert_choice == "恋愛カウンセラー":
        system_message = "あなたは経験豊富な恋愛カウンセラーです。親身に、そして具体的なアドバイスをしてください。"
    elif expert_choice == "シェフ":
        system_message = "あなたは一流のシェフです。家庭でも作れる簡単なレシピのアイデアを提案してください。"
    else:
        system_message = "あなたは親切なアシスタントです。"

    # ★★★ ChatOpenAIの初期化部分を修正 ★★★
    llm = ChatOpenAI(
        api_key=api_key, 
        model_name="gpt-4o-mini", 
        temperature=0.7
    )
    
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_question),
    ]
    
    result = llm.invoke(messages)
    return result.content

# --- Streamlitアプリの画面 ---
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

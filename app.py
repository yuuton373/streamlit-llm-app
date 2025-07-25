import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

# ローカル実行のために.envファイルを読み込む
load_dotenv()

def get_llm_response(user_question, expert_choice, api_key):
    
    system_message = "" # システムメッセージを初期化
    if expert_choice == "ITコンサルタント":
        system_message = "あなたは優秀なITコンサルタントです。専門用語を避け、初心者にも分かりやすく回答してください。"
    elif expert_choice == "恋愛カウンセラー":
        system_message = "あなたは経験豊富な恋愛カウンセラーです。親身に、そして具体的なアドバイスをしてください。"
    elif expert_choice == "シェフ":
        system_message = "あなたは一流のシェフです。家庭でも作れる簡単なレシピのアイデアを提案してください。"
    
    # ChatOpenAIの初期化時に、受け取ったAPIキーを明示的に渡す
    llm = ChatOpenAI(
        api_key=api_key, 
        model_name="gpt-4o-mini", 
        temperature=0.7
    )
    
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_question),
    ]
    
    try:
        result = llm.invoke(messages)
        return result.content
    except Exception as e:
        st.error(f"LLMからの回答取得中にエラーが発生しました: {e}")
        return None

# --- Streamlitアプリの画面 ---

st.title("専門家AIチャットボット")
st.write("専門家を選択し、質問を入力してください。")
st.divider()

# --- APIキーの取得ロジック ---
# まず、Streamlit CloudのSecretsから取得を試みる
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    key_source = "Streamlit Secrets"
# Secretsがなければ、ローカルの環境変数（.envから読み込まれたもの）から取得を試みる
except (KeyError, FileNotFoundError):
    api_key = os.getenv("OPENAI_API_KEY")
    key_source = "ローカルの .env ファイル"

# --- UIの表示 ---
if api_key:
    # st.success(f"APIキーを「{key_source}」から読み込みました。") # デバッグ用
    
    expert_choice = st.radio(
        "どの専門家に相談しますか？",
        ("ITコンサルタント", "恋愛カウンセラー", "シェフ")
    )
    user_question = st.text_area("相談したい内容を入力してください。")

    if st.button("AIに相談する"):
        st.divider()
        if user_question:
            with st.spinner("AIが回答を考えています..."):
                response = get_llm_response(user_question, expert_choice, api_key)
            
            if response:
                st.subheader("🤖 AIからの回答")
                st.markdown(response)
        else:
            st.error("相談したい内容を入力してください。")
else:
    st.error("エラー: OpenAIのAPIキーが設定されていません。")
    st.info("ローカル実行の場合は.envファイル、Streamlit Cloudの場合はSecretsにAPIキーを設定してください。")
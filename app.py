import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

def get_llm_response(user_question, expert_choice, api_key_from_secrets):
    
    system_message = "" # 初期化
    if expert_choice == "ITコンサルタント":
        system_message = "あなたは優秀なITコンサルタントです。専門用語を避け、初心者にも分かりやすく回答してください。"
    elif expert_choice == "恋愛カウンセラー":
        system_message = "あなたは経験豊富な恋愛カウンセラーです。親身に、そして具体的なアドバイスをしてください。"
    elif expert_choice == "シェフ":
        system_message = "あなたは一流のシェフです。家庭でも作れる簡単なレシピのアイデアを提案してください。"
    
    llm = ChatOpenAI(
        api_key=api_key_from_secrets, # Secretsから受け取ったキーを明示的に渡す
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
        # エラーが発生した場合、より詳細な情報を表示する
        st.error(f"LLMからの回答取得中にエラーが発生しました: {e}")
        return None

# --- Streamlitアプリの画面 ---
st.title("専門家AIチャットボット")
st.write("専門家を選択し、質問を入力してください。")
st.divider()

# Secretsが正しく読み込めているかを確認
try:
    # SecretsからAPIキーを読み込む
    my_api_key = st.secrets["OPENAI_API_KEY"]

    # 画面にデバッグメッセージを表示
    st.success("SecretsからAPIキーを読み込みました。アプリは正常に動作する準備ができています。")
    
    # UIを表示
    expert_choice = st.radio(
        "どの専門家に相談しますか？",
        ("ITコンサルタント", "恋愛カウンセラー", "シェフ")
    )
    user_question = st.text_area("相談したい内容を入力してください。")

    if st.button("AIに相談する"):
        st.divider()
        if user_question:
            with st.spinner("AIが回答を考えています..."):
                response = get_llm_response(user_question, expert_choice, my_api_key)
            
            if response:
                st.subheader("🤖 AIからの回答")
                st.markdown(response)
        else:
            st.error("相談したい内容を入力してください。")

except (KeyError, FileNotFoundError):
    st.error("エラー: StreamlitのSecretsに 'OPENAI_API_KEY' が設定されていません。")
    st.info("アプリ管理画面の「Settings > Secrets」で、正しいAPIキーを設定してください。")
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# この関数は、ユーザーの入力、専門家の選択、そしてAPIキーを受け取る
def get_llm_response(user_question, expert_choice, api_key_from_secrets):
    
    system_message = "" # システムメッセージを初期化
    if expert_choice == "ITコンサルタント":
        system_message = "あなたは優秀なITコンサルタントです。専門用語を避け、初心者にも分かりやすく回答してください。"
    elif expert_choice == "恋愛カウンセラー":
        system_message = "あなたは経験豊富な恋愛カウンセラーです。親身に、そして具体的なアドバイスをしてください。"
    elif expert_choice == "シェフ":
        system_message = "あなたは一流のシェフです。家庭でも作れる簡単なレシピのアイデアを提案してください。"
    
    # ChatOpenAIの初期化時に、受け取ったAPIキーを明示的に渡す
    llm = ChatOpenAI(
        api_key=api_key_from_secrets, 
        model_name="gpt-4o-mini", 
        temperature=0.7
    )
    
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_question),
    ]
    
    try:
        # LLMに質問を投げて結果を取得
        result = llm.invoke(messages)
        return result.content
    except Exception as e:
        # エラーが発生した場合、画面に詳細なエラーメッセージを表示する
        st.error(f"LLMからの回答取得中にエラーが発生しました: {e}")
        return None

# --- Streamlitアプリの画面 ---

st.title("専門家AIチャットボット")
st.write("専門家を選択し、質問を入力してください。")
st.divider()

# Secretsが正しく読み込めているかを確認する
try:
    # SecretsからAPIキーを読み込む
    my_api_key = st.secrets["OPENAI_API_KEY"]

    # 画面にデバッグメッセージを表示（デプロイ成功確認用）
    # st.success("SecretsからAPIキーを読み込みました。") # 成功したらこの行はコメントアウトしてもOK
    
    # UI（ユーザーインターフェース）を表示
    expert_choice = st.radio(
        "どの専門家に相談しますか？",
        ("ITコンサルタント", "恋愛カウンセラー", "シェフ")
    )
    user_question = st.text_area("相談したい内容を入力してください。")

    if st.button("AIに相談する"):
        st.divider()
        if user_question:
            with st.spinner("AIが回答を考えています..."):
                # 関数にAPIキーを渡す
                response = get_llm_response(user_question, expert_choice, my_api_key)
            
            if response:
                st.subheader("🤖 AIからの回答")
                st.markdown(response)
        else:
            st.error("相談したい内容を入力してください。")

except (KeyError, FileNotFoundError):
    # Secretsの読み込みに失敗した場合
    st.error("エラー: StreamlitのSecretsに 'OPENAI_API_KEY' が設定されていません。")
    st.info("アプリ管理画面の「Settings > Secrets」で、正しいAPIキーを設定してください。")
    st.code("OPENAI_API_KEY = \"sk-xxxxxxxx...\"")
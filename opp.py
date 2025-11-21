import streamlit as st
import google.generativeai as genai
from PIL import Image

# ------------------------------------------------
# 1. 設定部分
# ------------------------------------------------
st.title("🐶 ワンにゃんプロフィール帳 🐱")
st.write("写真をアップすると、最新AI（Gemini 2.5）がプロフィールを作ります！")

api_key = st.text_input("APIキーを入れてね", type="password")

# ★追加機能：性格を選ぶセレクトボックス
# 左側が「画面に出る文字」、右側が「AIに送る命令」になるようにリストを作ってもいいですが
# 今回はシンプルに「命令そのもの」を選ばせます。
tone = st.selectbox(
    "🤖 AIの性格を選んでね",
    [
        "ユーモアたっぷりの楽しい感じで",
        "上から目線の『超毒舌』キャラで",
        "デレデレの『甘えん坊』キャラで",
        "コテコテの『関西弁』で",
        "古風な『武士』のような口調で",
        "カッコつけた『中二病』キャラで"
    ]
)

# ------------------------------------------------
# 2. 画面を作る部分
# ------------------------------------------------
uploaded_file = st.file_uploader("ペットの写真をアップロードしてね", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption='アップロードされた写真', use_container_width=True)

    # ------------------------------------------------
    # 3. AIにお願いする部分
    # ------------------------------------------------
    if st.button("AI診断スタート！"):
        with st.spinner(f"AIが『{tone}』考え中..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-pro') 

                # ★ここがポイント！
                # ユーザーが選んだ `tone` (性格) をプロンプトの中に埋め込みます
                prompt = f"""
                この画像を分析して、以下の項目を答えてください。
                
                【重要】
                口調や態度は、必ず「{tone}」徹底してください。
                
                もし犬や猫でない場合は「犬か猫の写真を見せてくれ！」とそのキャラになりきって答えてください。
                
                1. 【種類】（犬種・猫種）
                2. 【推定年齢】（見た目からの勝手な推測）
                3. 【性別】（雰囲気からの推測）
                4. 【性格】（顔つきから想像する性格）
                5. 【今の気持ち】（セリフ風に）
                """

                response = model.generate_content([prompt, image])
                st.success("診断完了！")
                st.write(response.text)

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

elif not api_key:
    st.info("まずはAPIキーを入力してね！")
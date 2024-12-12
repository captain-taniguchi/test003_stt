# dokidoki_diary_proto3.py
import streamlit as st
import datetime
import os
from openai import OpenAI
from stt017whis2 import get_recognized_text

# OpenAIクライアントの初期化（必要に応じて）
# client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# 左上のロゴ（さやさんデザインを仮で使用）
st.image(
    "images/team_dokidoki_logo.png",
    use_container_width=True,  # use_column_width を use_container_width に変更
)

# 徳井風のイケメン（DALL-E3作※2回作ったら1日分のトークンが無くなった）
st.image("images/tokui_ver1.png", use_container_width=True)  # use_column_width を use_container_width に変更

# 小さい列と大きい列を作成
question_col, date_col = st.columns([25, 5])  # [25, 5]は列の比率

# question列に日記記入を促す文を入れる
with question_col:
    st.markdown('<div style="font-size: 24px; text-align: center;">お疲れ様。今日はどんな1日だった？</div>', unsafe_allow_html=True)

# date列に日付入力欄を入れる
with date_col:
    date = st.date_input("日付を選択", value=datetime.date.today())

st.markdown("----")  # 区切り線

# 子モジュールから音声認識結果を取得
recognized_text = get_recognized_text()

# 日記を入力する欄を入れる。openaiに渡したり、日記内容を反映した画像と合わせて日記を表示するためにdiary_inputに日記内容を代入する。
diary_input = st.text_area(
    "日記を入力する", 
    height=150,
    label_visibility="hidden", 
    placeholder="マイクを押して話しかけてね。話し終わったらもう1回マイクを押してね。ちょっと違う部分は手動で編集してね。ごめんね。",
    value=recognized_text  # 音声認識結果をデフォルト値として設定
)

# 送信ボタンを入れる
submit_btn = st.button("今日の日記生成")

# 送信ボタンが押されると以下の処理が走る
if submit_btn:
    # 列を2つに分割する
    col1, col2 = st.columns(2)

    # 左の列には絵日記を表示。imageのところにopenaiで生成した画像を渡す。
    with col1:
        # OpenAIクライアントの初期化
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        
        # DALL-E 3で日記内容を反映したイラストを作成
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"Create a cute illustration based on the following text.\n#text\n{diary_input}",
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        st.image(image_url, width=300, use_container_width=False)  # use_container_width=False に設定（幅を固定）

    # 右の列には日記とフィードバックを表示
    with col2:
        st.write("### Your Diary（日記に入力した内容がそのまま表示される）")
        # 文章を枠で囲う処理を入れています。
        st.markdown(f"""                    
            <div style="background-color: #F0F2F6; padding: 15px; border-radius: 5px;">
                今日の天気：晴れ（天気予報APIから取ってくる）<br>
                {diary_input}
            </div>
            """, unsafe_allow_html=True)

        st.write("### Feedback from Tokui")
        feedback = "フィードバック（OpenAI APIで生成したフィードバックをここに格納する）"
        st.markdown(f"""                    
            <div style="background-color: #F0F2F6; padding: 15px; border-radius: 5px;">
                {feedback}
            </div>
            """, unsafe_allow_html=True)

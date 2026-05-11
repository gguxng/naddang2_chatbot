import streamlit as st
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

# 페이지 설정
st.set_page_config(
    page_title="저녁 메뉴 추천 챗봇",
    page_icon="👨‍🍳",
    layout="centered"
)

# 식당 스타일 CSS
st.markdown("""
<style>

.stApp {
    background-color: #f5e6cc;
}

.block-container {
    background-color: #fff8ee;
    padding: 2rem;
    border-radius: 25px;
    border: 6px solid #8b5a2b;
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

h1 {
    color: #5c3317;
    text-align: center;
}

[data-testid="stChatMessage"] {
    background-color: #fff3e0;
    border-radius: 18px;
    padding: 12px;
    margin-bottom: 12px;
    border: 2px solid #d2a679;
}

</style>
""", unsafe_allow_html=True)

# 제목
st.title("👨‍🍳 오늘의 저녁 식당")

st.write(
    "오늘 먹고 싶은 느낌을 말해보세요 🍽️\n"
    "AI 셰프가 메뉴와 음식 사진을 함께 추천해드립니다!"
)

# API 키 입력
openai_api_key = st.text_input(
    "OpenAI API 키 입력",
    type="password"
)

if not openai_api_key:
    st.info("API 키를 입력해주세요 🔑")

else:
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 이전 메시지 출력
    for message in st.session_state.messages:

        avatar = "🍔" if message["role"] == "user" else "👨‍🍳"

        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

            # 이미지가 저장되어 있으면 출력
            if "images" in message:
                cols = st.columns(len(message["images"]))

                for idx, img_url in enumerate(message["images"]):
                    cols[idx].image(
                        img_url,
                        use_container_width=True
                    )

    # 사용자 입력
    if prompt := st.chat_input("예: 매콤한 음식 먹고 싶어 🌶️"):

        # 사용자 메시지 저장
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user", avatar="🍔"):
            st.markdown(prompt)

        # 시스템 프롬프트
        system_prompt = """
        너는 친절한 레스토랑 셰프 AI다.

        사용자의 취향에 맞춰 메뉴 3개를 추천해라.

        규칙:
        - 메뉴 이름 앞에는 번호를 붙인다.
        - 메뉴 이름은 한 줄로 작성한다.
        - 메뉴마다 짧은 설명을 추가한다.
        - 마지막에 추가 질문을 한다.

        예시:

        1. 김치찌개
        - 얼큰하고 뜨끈해서 스트레스 풀기 좋아요!

        2. 스테이크
        - 육즙 가득한 고기로 든든한 저녁 추천!

        3. 크림파스타
        - 부드럽고 고소해서 편안한 기분에 딱이에요!
        """

        # GPT 응답 생성
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                *[
                    {
                        "role": m["role"],
                        "content": m["content"]
                    }
                    for m in st.session_state.messages
                ]
            ]
        )

        assistant_reply = response.choices[0].message.content

        # 메뉴 이름 추출
        menu_names = []

        for line in assistant_reply.split("\n"):
            line = line.strip()

            if line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
                menu = line.split(".", 1)[1].strip()
                menu_names.append(menu)

        # 음식 이미지 URL 생성
        # Unsplash Source 사용
        image_urls = []

        for menu in menu_names:
            query = menu.replace(" ", "%20")
            image_url = f"https://source.unsplash.com/600x400/?{query},food"
            image_urls.append(image_url)

        # 챗봇 메시지 출력
        with st.chat_message("assistant", avatar="👨‍🍳"):

            st.markdown(assistant_reply)

            cols = st.columns(len(image_urls))

            for idx, img_url in enumerate(image_urls):
                cols[idx].image(
                    img_url,
                    caption=menu_names[idx],
                    use_container_width=True
                )

        # 저장
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_reply,
            "images": image_urls
        })

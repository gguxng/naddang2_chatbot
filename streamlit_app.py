import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="저메추 쉐프",
    page_icon="👨‍🍳",
    layout="centered"
)

# 식당 느낌 커스텀 CSS
st.markdown("""
<style>

/* 전체 배경 */
.stApp {
    background-color: #f5e6cc;
    background-image: linear-gradient(
        rgba(255,255,255,0.15),
        rgba(255,255,255,0.15)
    );
}

/* 메인 컨테이너 */
.block-container {
    background-color: #fff8ee;
    padding: 2rem;
    border-radius: 25px;
    border: 6px solid #8b5a2b;
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

/* 제목 */
h1 {
    color: #5c3317;
    text-align: center;
    font-size: 42px !important;
}

/* 설명글 */
p {
    color: #4b2e1e;
    font-size: 18px;
}

/* 채팅 말풍선 */
[data-testid="stChatMessage"] {
    background-color: #fff3e0;
    border-radius: 18px;
    padding: 12px;
    margin-bottom: 12px;
    border: 2px solid #d2a679;
}

/* 사용자 채팅 */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background-color: #ffe0b2;
}

/* 입력창 */
.stChatInputContainer {
    background-color: #fff8ee;
    border-top: 3px solid #8b5a2b;
}

/* 텍스트 입력 */
input {
    border-radius: 15px !important;
    border: 2px solid #8b5a2b !important;
}

/* 버튼 */
.stButton button {
    background-color: #8b5a2b;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
}

.stButton button:hover {
    background-color: #6f451f;
}

/* 정보 박스 */
[data-testid="stInfo"] {
    border-radius: 15px;
    background-color: #fff0d9;
}

</style>
""", unsafe_allow_html=True)

# 제목 및 설명
st.title("👨‍🍳 오늘의 저녁 식당")

st.write(
    "🍽️ 어서오세요!\n\n"
    "오늘 기분과 취향에 맞는 저녁 메뉴를 추천해드리는 AI 셰프입니다 😄"
)

# API 키 입력
openai_api_key = st.text_input(
    "OpenAI API 키 입력",
    type="password"
)

if not openai_api_key:
    st.info("API 키를 입력하면 메뉴 추천을 시작할 수 있어요! 🔑")

else:
    # OpenAI 클라이언트
    client = OpenAI(api_key=openai_api_key)

    # 채팅 저장
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 메시지 출력
    for message in st.session_state.messages:

        # 사용자 = 햄버거
        if message["role"] == "user":
            avatar = "🍔"

        # 챗봇 = 요리사
        else:
            avatar = "👨‍🍳"

        with st.chat_message(
            message["role"],
            avatar=avatar
        ):
            st.markdown(message["content"])

    # 입력창
    if prompt := st.chat_input("먹고 싶은 느낌을 말해주세요 🍕"):

        # 사용자 메시지 저장
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        # 사용자 메시지 출력
        with st.chat_message("user", avatar="🍔"):
            st.markdown(prompt)

        # 시스템 프롬프트
        system_prompt = """
        너는 친절한 레스토랑 셰프 AI다.

        규칙:
        - 사용자의 기분과 취향에 맞는 메뉴를 추천한다.
        - 항상 3가지 메뉴를 추천한다.
        - 메뉴마다 음식 이모지를 사용한다.
        - 맛 표현을 풍부하게 한다.
        - 친절한 셰프처럼 말한다.
        - 마지막에는 추가 질문으로 대화를 이어간다.

        예시:
        1. 스테이크 🥩
        - 육즙 가득한 고기로 든든한 저녁 어떠세요?

        2. 크림파스타 🍝
        - 부드럽고 고소해서 편안한 기분에 잘 어울려요.

        마지막:
        "오늘은 따뜻한 국물도 함께 드시고 싶으신가요? 😊"
        """

        # GPT 응답 생성
        stream = client.chat.completions.create(
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
            ],
            stream=True,
        )

        # 챗봇 응답 출력
        with st.chat_message(
            "assistant",
            avatar="👨‍🍳"
        ):
            response = st.write_stream(stream)

        # 응답 저장
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

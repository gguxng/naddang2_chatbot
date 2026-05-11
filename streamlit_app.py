import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="저녁 메뉴 추천 챗봇", page_icon="🍽️")

# 제목 및 설명
st.title("🍽️ 저녁 메뉴 추천 챗봇")
st.write(
    "오늘 저녁 뭐 먹을지 고민된다면 물어보세요! 😋 "
    "기분, 날씨, 음식 취향에 맞춰 메뉴를 추천해드립니다."
)

# OpenAI API 키 입력
openai_api_key = st.text_input("OpenAI API 키", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요!", icon="🗝️")

else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 채팅 기록 저장
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 이전 메시지 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("예: 매운 음식 먹고 싶어"):

        # 사용자 메시지 저장
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        # 사용자 메시지 출력
        with st.chat_message("user"):
            st.markdown(prompt)

        # 시스템 프롬프트
        system_prompt = """
        너는 저녁 메뉴를 추천해주는 AI 챗봇이다.

        규칙:
        - 사용자의 기분, 날씨, 상황, 음식 취향을 고려해서 추천한다.
        - 항상 3가지 메뉴를 추천한다.
        - 각 메뉴마다 짧은 이유를 설명한다.
        - 친근하고 맛있어 보이게 설명한다.
        - 마지막에는 한 줄 질문으로 대화를 이어간다.

        예시:
        1. 김치찌개 🍲
        - 얼큰하고 따뜻해서 스트레스 풀기 좋아!

        2. 치킨 🍗
        - 바삭한 치킨은 언제 먹어도 실패 없음 ㅎㅎ

        마지막:
        "오늘은 밥류가 땡겨? 면류가 땡겨?"
        """

        # GPT 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                *[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            ],
            stream=True,
        )

        # 응답 출력
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # 응답 저장
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

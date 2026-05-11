import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="고세구 챗봇", page_icon="🦊")

# 제목 및 설명
st.title("🦊 고세구 챗봇")
st.write(
    "이세계아이돌 멤버 고세구 컨셉의 AI 챗봇입니다! "
    "세구 특유의 귀엽고 장난기 있는 말투로 대화해보세요 💜"
)

# API 키 입력
openai_api_key = st.text_input("OpenAI API 키", type="password")

if not openai_api_key:
    st.info("OpenAI API 키를 입력해주세요!", icon="🗝️")
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
    if prompt := st.chat_input("세구랑 대화하기..."):

        # 사용자 메시지 저장
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        # 사용자 메시지 출력
        with st.chat_message("user"):
            st.markdown(prompt)

        # 시스템 프롬프트 (고세구 캐릭터 설정)
        system_prompt = """
        너는 이세계아이돌의 고세구처럼 말하는 AI 챗봇이다.

        특징:
        - 밝고 귀엽고 장난기 많은 성격
        - 인터넷 밈과 드립을 자주 사용
        - 반말 위주로 친근하게 말함
        - 리액션이 크고 감정 표현이 풍부함
        - 가끔 웃음을 위해 엉뚱한 말을 함
        - 시청자와 친구처럼 대화함
        - 문장 끝에 ㅋㅋ, ㅎㅎ, !!! 등을 자주 사용

        절대 하지 말 것:
        - 너무 딱딱한 말투
        - AI라고 반복해서 말하기
        - 지나치게 진지한 설명만 하기
        """

        # OpenAI 응답 생성
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

import streamlit as st
import google.generativeai as genai

# 1. Gọi API Key từ hệ thống bảo mật của Streamlit
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Thiết lập Chỉ dẫn và Tài liệu
chi_dan_he_thong = """
Bạn là một trợ lý học tập thân thiện. Nhiệm vụ của bạn là hướng dẫn học sinh 
tìm hiểu kiến thức dựa trên nội dung bài học. Tuyệt đối không làm hộ bài tập, 
hãy đưa ra gợi ý từng bước.
"""

# 3. Khởi tạo AI
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash-latest",
    system_instruction=chi_dan_he_thong
)

st.title("🤖 Trợ lý Học tập AI")

# 4. Quản lý lịch sử trò chuyện
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Xử lý câu hỏi của học sinh
if prompt := st.chat_input("Em có câu hỏi gì cần hỗ trợ?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        chat = model.start_chat()
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

import streamlit as st
from google import genai
import os

# 1. Cấu hình trang web
st.set_page_config(page_title="Trợ lý Học tập AI", page_icon="🤖")
st.title("🤖 Trợ lý Học tập AI")

# 2. Khởi tạo Client API từ Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("Chưa tìm thấy GEMINI_API_KEY trong phần bảo mật.")
    st.stop()

# 3. Chỉ dẫn hệ thống
chi_dan_he_thong = """
Bạn là một trợ lý học tập thân thiện. Nhiệm vụ của bạn là hướng dẫn học sinh 
tìm hiểu kiến thức dựa trên nội dung bài học. Tuyệt đối không làm hộ bài tập, 
hãy đưa ra gợi ý từng bước.
"""

# 4. Quản lý trạng thái trò chuyện
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Hiển thị lịch sử trò chuyện
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Xử lý đầu vào của người dùng
if prompt := st.chat_input("Em có câu hỏi gì cần hỗ trợ?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            # Gửi yêu cầu tới mô hình Gemini bằng API mới
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=chi_dan_he_thong,
                    temperature=0.7,
                ),
            )
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Lỗi kết nối: {e}")

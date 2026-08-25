import streamlit as st
import google.generativeai as genai
import os

# 1. Cấu hình trang web (tùy chọn)
st.set_page_config(page_title="Trợ lý Học tập AI", page_icon="🤖")
st.title("🤖 Trợ lý Học tập AI")

# 2. Lấy API Key từ Secrets của Streamlit
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("Chưa tìm thấy GEMINI_API_KEY. Vui lòng kiểm tra lại phần Advanced Settings trên Streamlit Cloud.")
    st.stop()

# 3. Chỉ dẫn hệ thống
chi_dan_he_thong = """
Bạn là một trợ lý học tập thân thiện. Nhiệm vụ của bạn là hướng dẫn học sinh 
tìm hiểu kiến thức dựa trên nội dung bài học. Tuyệt đối không làm hộ bài tập, 
hãy đưa ra gợi ý từng bước.
"""

# 4. Khởi tạo mô hình an toàn (Sử dụng 'gemini-1.5-flash' theo cách khai báo mới nhất)
try:
    model = genai.GenerativeModel('gemini-pro', system_instruction=chi_dan_he_thong)
except Exception as e:
    st.error(f"Lỗi khởi tạo mô hình AI: {e}")
    st.stop()

# 5. Quản lý trạng thái trò chuyện
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Hiển thị lịch sử trò chuyện
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Xử lý đầu vào của người dùng
if prompt := st.chat_input("Em có câu hỏi gì cần hỗ trợ?"):
    # Hiển thị tin nhắn của người dùng
    with st.chat_message("user"):
        st.markdown(prompt)
    # Lưu tin nhắn của người dùng vào lịch sử
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Hiển thị phản hồi của AI
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # Tạo không gian trống để hiển thị tin nhắn (nếu cần hiệu ứng gõ phím)
        
        try:
            # Tạo một phiên chat mới, chứa lịch sử
            chat = model.start_chat(history=[])
            
            # Khôi phục lịch sử chat (nếu có) vào phiên chat mới
            for msg in st.session_state.messages[:-1]: # Bỏ qua câu hỏi cuối cùng vừa lưu
                 if msg["role"] == "user":
                     chat.history.append({"role": "user", "parts": [msg["content"]]})
                 elif msg["role"] == "assistant":
                     chat.history.append({"role": "model", "parts": [msg["content"]]})

            # Gửi tin nhắn và nhận phản hồi
            response = chat.send_message(prompt)
            full_response = response.text
            
            message_placeholder.markdown(full_response)
            
            # Lưu phản hồi của AI vào lịch sử
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Đã xảy ra lỗi khi kết nối với AI: {e}")

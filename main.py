import streamlit as st
from src.assistant import Assistant

title_name = "胖均的金融小助手"


def main():
    st.image(image='image/backgrounds.jpg', width=700, caption='')
    st.title(title_name)
    
    # Initialize the Assistant
    assistant = Assistant()

    # Get user input and display the conversation
    user_input = st.text_input("User:","")
    if st.button("Send"):
        check = assistant.check_field(user_input)
        if check == "相關":
            stock_code = assistant.check_analysis(user_input)
            if stock_code != None:
                reply_msg = assistant.analysis_stock(stock_code)
                assistant.add_msg(reply_msg, "ai")
                st.text("Assistant:")
                st.write(reply_msg)
            else:
                assistant.add_msg(user_input, "user")
                reply_msg = assistant.get_response()
                assistant.add_msg(reply_msg, "ai")
                st.text("Assistant:")
                st.write(reply_msg)
        else:
            st.text("Assistant:")
            st.write("我是專門為金融領域而生的AI，您可以詢問金融相關問題！")

if __name__ == "__main__":
    main()

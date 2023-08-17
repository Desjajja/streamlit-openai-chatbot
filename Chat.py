import streamlit as st
import json
import openai
import extra_streamlit_components as stx
# import datetime

st.set_page_config(
    page_title="究极神奇海螺",
    page_icon="🐚",
)

def init_chat_history(current_profile):
    with st.chat_message("assistant", avatar='🤖'):
        st.markdown(f"您好，我是{current_profile}，很高兴为您服务🥰")

    if current_messages := st.session_state.get("current_messages"):
        _, message_pair = current_messages
        for message in message_pair[1]:
            avatar = '🧑‍💻' if message["role"] == "user" else '🤖'
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
    else:
        st.session_state.current_messages = [None, [None, []]] # id, sentence_pair => (conclusion, messages)

    return st.session_state.current_messages


def clear_chat_history():
    del st.session_state.current_messages


def init_chat_dict():
    if "message_dict" in st.session_state:
        message_dict = st.session_state.message_dict
        print(message_dict)
        with st.sidebar:
            for id, chat in message_dict.copy().items():
                with st.expander(
                    label=chat[0]
                ):
                    col1, col2 = st.columns(2)
                    with col1:
                        if id == st.session_state.current_messages[0]:
                            select_state = "selected"
                            disabled = True
                        else:
                            select_state = "select"
                            disabled = False
                        btn_select = st.button(label=select_state, key=f"{id}-select", disabled=disabled)
                    with col2:
                        btn_delete = st.button(label="delete", key=f"{id}-delete")
                    if btn_select:
                        select_chat(id)
                        st.experimental_rerun()
                    if btn_delete:
                        delete_chat(id)
                        st.experimental_rerun()


    else:
        st.session_state.message_dict = {}

def init_upload():
    with st.sidebar:
        with st.form("my-form", clear_on_submit=True):
            file = st.file_uploader("FILE UPLOADER")
            submitted = st.form_submit_button("UPLOAD!")
            if submitted and file is not None:
                uploaded_list = json.load(file)
                st.session_state.message_dict[str(hash(str(uploaded_list)))] = [file.name, uploaded_list] # (filename, upload_list)
                st.experimental_rerun()

def select_chat(id):
    new_chat()
    conclusion, messages = st.session_state.message_dict[id]
    st.session_state.current_messages[0] = id
    st.session_state.current_messages[1][0] = conclusion
    st.session_state.current_messages[1][1] = messages

def delete_chat(id):
    del st.session_state.message_dict[id]

def new_chat():
    id, message_pair = st.session_state.current_messages
    # if messages := st.session_state.current_messages:
    if not id and message_pair[1]: # No id is assigned, then add conclusion.
        current_profile = st.session_state.get('current_profile')
        auth = st.session_state['profiles'][current_profile]
        conclusion_enquiry = message_pair[1].copy()
        conclusion_enquiry.append(
            dict(
            role="user",
            content="give the conversation a title based on the context:")
            )
        # print(conclusion_enquiry)
        conclusion = gpt_chat(conclusion_enquiry
        , auth)['choices'][0]['message']['content'].strip('\"').strip()
        message_pair[0] = conclusion
        st.session_state.message_dict[str(hash(str(message_pair[1])))] = message_pair
    st.session_state.current_messages = [None, [None, []]] 

def gpt_chat_stream(messages, hyparams, auth):
    return openai.ChatCompletion.create(messages=messages,
                                        frequency_penalty=0,
                                        presence_penalty=0,
                                        stop=None,
                                        stream=True, **auth, **hyparams)

def gpt_chat(messages, auth):
    return openai.ChatCompletion.create(messages=messages, **auth)
def get_manager():
    return stx.CookieManager()

def main():
    current_profile = st.session_state.get('current_profile')
    st.header("🐚究极神奇海螺")

    if not current_profile:
        st.markdown("No profile is selected.")
        return
    # else:
    #     print(st.session_state['profiles'])
    with st.expander("Hyperparameters"):
        temperature = st.slider("temperature", 0.0, 1.0, 0.6)
        top_p = st.slider("top_p", 0.0, 1.0, 0.6)
        hyparams = dict(
            temperature=temperature,
            top_p=top_p
        )
    current_messages = init_chat_history(current_profile)
    auth = st.session_state['profiles'][current_profile]
    if prompt := st.chat_input("Shift + Enter 换行, Enter 发送"):
        with st.chat_message("user", avatar='🧑‍💻'):
            st.markdown(prompt)
        current_messages[1][1].append({"role": "user", "content": prompt})
        report = []
        with st.chat_message("assistant", avatar='🤖'):
            placeholder = st.empty()
            for response in gpt_chat_stream(current_messages[1][1], hyparams, auth):
                report.append(response.choices[0]['delta'].get('content', ''))
                result = "".join(report)
                placeholder.markdown(result)
        current_messages[1][1].append(dict(
            role="assistant",
            content=result
        ))

    init_chat_dict()
    init_upload()

    col1, col2= st.columns(2)
    @st.cache_data
    def dump_message(m):
        return json.dumps(m, ensure_ascii=False)
    
    data = dump_message(current_messages[1][1])
    with col1:
        # st.button("Clear chat", on_click=clear_chat_history)
        st.button("New chat", on_click=new_chat)
    with col2:
        st.download_button(
            label="Download chat",
            data=data,
            file_name='chat_histoy.json',
            mime="text/plain"
        )       

if __name__ == "__main__":
    st.session_state['cookie_manager'] = get_manager()
    main()

import streamlit as st
import json
import openai
import extra_streamlit_components as stx

st.set_page_config(
    page_title="究极神奇海螺",
    page_icon="🐚",
)

def init_chat_history(current_profile):
    with st.chat_message("assistant", avatar='🤖'):
        st.markdown(f"您好，我是{current_profile}，很高兴为您服务🥰")

    if "messages" in st.session_state:
        for message in st.session_state.messages:
            avatar = '🧑‍💻' if message["role"] == "user" else '🤖'
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
    else:
        st.session_state.messages = []

    return st.session_state.messages


def clear_chat_history():
    del st.session_state.messages


def gpt_chat_stream(messages, hyparams, auth):
    return openai.ChatCompletion.create(messages=messages,
                                        frequency_penalty=0,
                                        presence_penalty=0,
                                        stop=None,
                                        stream=True, **auth, **hyparams)

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
    messages = init_chat_history(current_profile)
    auth = st.session_state['profiles'][current_profile]
    if prompt := st.chat_input("Shift + Enter 换行, Enter 发送"):
        with st.chat_message("user", avatar='🧑‍💻'):
            st.markdown(prompt)
        messages.append({"role": "user", "content": prompt})
        # print(f"[user] {prompt}", flush=True)
        report = []
        # print(hyparams)
        with st.chat_message("assistant", avatar='🤖'):
            placeholder = st.empty()
            for response in gpt_chat_stream(messages, hyparams, auth):
                report.append(response.choices[0]['delta'].get('content', ''))
                result = "".join(report)
                placeholder.markdown(result)
        messages.append(dict(
            role="assistant",
            content=result
        ))
        # print(json.dumps(messages, ensure_ascii=False), flush=True)

    st.button("清空对话", on_click=clear_chat_history)


if __name__ == "__main__":
    st.session_state['cookie_manager'] = get_manager()
    main()

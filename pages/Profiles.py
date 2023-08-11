import streamlit as st
st.set_page_config(
    page_title="信息配置",
    page_icon="📝"
)


def main():
    st.header("📝信息配置")
    col1, col2 = st.columns(2)
    with col1:
        with st.form("new profile", clear_on_submit=True):
            name = st.text_input("name").strip()
            engine = st.text_input("engine").strip()
            api_type = st.text_input("api type").strip()
            api_base = st.text_input("api base").strip()
            api_version = st.text_input("api version").strip()
            api_key = st.text_input("api key").strip()

            added = st.form_submit_button("Add")
            if added:
                st.session_state['profiles'][name] = dict(
                            engine=engine,
                            api_type=api_type,
                            api_base=api_base,
                            api_version=api_version,
                            api_key=api_key
                        )

                st.success(f"profile {name} added!")
    with col2:
        for name, auth in st.session_state['profiles'].items():
            with st.expander(name):
                text_fields = {}
                for k, v in auth.items():
                    text_fields[k] = st.text_input(k, v)
                col1, col2, col3 = st.columns(3)
                with col1:
                    if name == st.session_state['current_profile']:
                        select_state = "selected"
                        disabled = True
                    else:
                        select_state = "select"
                        disabled = False
                    btn_select = st.button(label=select_state, key=f"{name}_select", disabled=disabled)
                with col2:
                    btn_del = st.button(label="delete", key=f"{name}_delete")
                with col3:
                    btn_update = st.button(label="update", key=f"{name}_update")
                if btn_select:
                    st.session_state['current_profile'] = name
                    st.experimental_rerun()
                if btn_del:
                    del st.session_state['profiles'][name]
                    st.session_state['current_profile'] = ''
                    st.experimental_rerun()
                if btn_update:
                    st.session_state['profiles'][name] = text_fields

if __name__ == "__main__":
    if not st.session_state.get('profiles'):
        st.session_state['profiles'] = {}
    if not st.session_state.get('current_profile'):
        st.session_state['current_profile'] = ''
    main()

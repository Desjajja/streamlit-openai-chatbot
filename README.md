# streamlit-openai-chatbot
Fluent and easy-to-use chatbot web app. Built with [Streamlit](https://docs.streamlit.io/), [Extra-Streamlit-Components](https://pypi.org/project/extra-streamlit-components/) and [Openai](https://pypi.org/project/openai/).
## Update
* Aug 17, 2023: _implemented mutiple chat messages management, including switching, downloading and deletion_
* Aug 12, 2023: *added masked input field for api token, configurable expire date for cookies*

## Quick Start
1. clone this repo, install dependencies with `pip install -r requiremnents.txt`
2. execute `streamlit run Chat.py`
3. configure api token and other auth info
4. enjoy chatting

## Features
* fully implemeted chatting history
* single-round-dialogue-wise hyperparamters configuration[^hyp]
* Managing multiple profiles by `Add/Select/Update/Delete` them
* cookies-enabled profile memorization[^security][^duration]

## Screenshots
* Chat page
![image](https://github.com/Desjajja/streamlit-openai-chatbot/assets/58029489/2a45068e-dd54-4789-8075-25e1b07161cd)
* configuring hyperparameters[^conf_hyp]
![image](https://github.com/Desjajja/streamlit-openai-chatbot/assets/58029489/296a2cd9-ef94-44a9-98af-408397bc68e8)
* configuring profiles
<img width="960" alt="Profiles" src="https://github.com/Desjajja/streamlit-openai-chatbot/assets/58029489/60d47ba5-235c-4a7d-899c-a0599bd99822">


## Potential Malfunctions
1. Profile deleting sometimes may not response in time, if so, try deleting it again.
2. Profiles stored in cookies will be initialized only after `Chat` page is opened for once.

[^hyp]: Up to today, supported hyperparameters includes `temperature` and `top_p`
[^conf_hyp]: Screenshot was taken before 8.17 update, hence no multiple chat management shown in the sidebar
[^security]: This app does not store or upload user messages by any means on purpose. Cookies are stored only on your local device.
[^duration]: The current expiring duration is set to **5 days**. You can modify it in `config.yaml`

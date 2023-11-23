from typing import Any

import streamlit as st
from loguru import logger

from client import OpenAIClient
from config import settings
from utils import get_image_price

chatbot = OpenAIClient()


def page_setup() -> None:
    st.set_page_config(page_title="ChatGPT - Presentation")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": "Would you care to chat, m8?", "mode": "text"}]


def sidebar() -> None:
    with st.sidebar:
        st.radio("Chat mode", ["text", "image"], key="mode")
        st.divider()

        st.title("Chat params")
        st.selectbox(
            label="Text Engine",
            options=[
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-0301",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-1106",
                "gpt-3.5-turbo-16k-0613",
                "gpt-3.5-turbo-16k",
                "gpt-4-0314",
                "gpt-4-0613",
                "gpt-4-1106-preview",
                "gpt-4-32k-0314",
                "gpt-4-32k-0613",
                "gpt-4-32k",
                "gpt-4-vision-preview",
                "gpt-4",
            ],
            key="text_engine",
        )
        st.text_input(label="System Message", value=settings.system_message, key="system_message")
        st.number_input(label="Temperature", value=settings.temperature, key="temperature")
        st.divider()

        st.title("Image params")
        st.selectbox(label="Image Model", options=["dall-e-2", "dall-e-3"], key="image_model")
        st.selectbox(
            label="Image Size",
            options=["256x256", "512x512", "1024x1024", "1024x1792", "1792x1024"],
            key="image_size",
        )
        st.selectbox(label="Image Quality", options=["standard", "hd"], key="image_quality")
        st.text(f"${get_image_price(st.session_state)}")


def generate_message(message: dict[str, Any]) -> None:
    if "mode" in message and message["mode"] == "image":
        st.image(message["content"])
    else:
        st.markdown(message["content"])


def update_chat_messages() -> None:
    for message in st.session_state.messages:
        avatar = settings.avatar if message["role"] == "ai" else None
        with st.chat_message(message["role"], avatar=avatar):
            generate_message(message)


def main_window() -> None:
    logger.debug(st.session_state)

    update_chat_messages()

    if question := st.chat_input("Type in your question..."):
        st.session_state.messages.append({"role": "user", "content": question, "mode": "text"})

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant", avatar=settings.avatar):
            with st.spinner(text="Inventing an answer..."):
                chatbot_response = chatbot.get_response(question, st.session_state)
                new_message = {"role": "ai", "content": chatbot_response, "mode": st.session_state["mode"]}
                st.session_state.messages.append(new_message)
                generate_message(new_message)


if __name__ == "__main__":
    page_setup()
    sidebar()
    main_window()

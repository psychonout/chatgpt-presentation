from typing import Any

import streamlit as st
from loguru import logger

from client import OpenAIClient
from config import settings

chatbot = OpenAIClient()


def page_setup() -> None:
    st.set_page_config(page_title="ChatGPT - Presentation")


def calculate_image_price(params: dict[str, Any]) -> None:
    if params.get("image_model") == "dall-e-2":
        match params.get("image_size"):
            case "256x256":
                return 0.016
            case "512x512":
                return 0.018
            case "1024x1024":
                return 0.02

    if params.get("image_model") == "dall-e-3":
        if params.get("image_quality") == "standard" and params.get("image_resolution") == "1024x1024":
            return 0.04
        if params.get("image_quality") == "hd" and set(params["image_resolution"].split("x")) == set(["1024", "1792"]):
            return 0.12
        else:
            return 0.08


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
            label="Image Size", options=["256x256", "512x512", "1024x1024", "1024x1792", "1792x1024"], key="image_size"
        )
        st.selectbox(label="Image Quality", options=["standard", "hd"], key="image_quality")
        st.text(calculate_image_price(st.session_state))


def main_window() -> None:
    logger.info(st.session_state)

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": "Would you care to chat, m8?"}]

    for message in st.session_state.messages:
        avatar = settings.avatar if message["role"] == "ai" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if question := st.chat_input("Type in your question..."):
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant", avatar=settings.avatar):
            with st.spinner(text="Inventing an answer..."):
                chatbot_response = chatbot.get_response(question, st.session_state)
                st.session_state.messages.append({"role": "ai", "content": chatbot_response})

                st.markdown(chatbot_response)


if __name__ == "__main__":
    page_setup()
    sidebar()
    main_window()

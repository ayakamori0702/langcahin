
import gradio as gr
from chatbot_engine import chat
from dotenv import load_dotenv

from langchain.memory import ChatMessageHistory
import os

def respond(message, chat_history):
    history = ChatMessageHistory()
    for [user_message, ai_message] in chat_history:
        history.add_user_message(user_message)
        history.add_ai_message(ai_message)

    bot_message = chat(message, history)
    chat_history.append((message, bot_message))
    return "", chat_history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    load_dotenv()

    app_env = os.environ.get("APP ENV" , "production")
# 環境変数にApp Envが設定されていない場合は、productionとして認証
    if app_env == "production":
        username = os.environ["GRADIO_USERNAME"]
        password = os.environ["GRADIO_PASSWORD"]
        auth = (username, password)
    else:
        auth = None

    demo.launch()

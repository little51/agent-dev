import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread

device = "cuda" if torch.cuda.is_available() else "auto"
model_path = './dataroot/models/NousResearch/Meta-Llama-3-8B-Instruct'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map=device,
    torch_dtype=torch.float16).eval()

terminators = [
    128001, 128009
]


def chat_llama3(message: str,
                   history: list,
                   temperature: float,
                   max_new_tokens: int,
                   top_p: float
                   ) -> str:
    chat_history = []
    for user, assistant in history:
        chat_history.extend([{"role": "user", "content": user}, {
                            "role": "assistant", "content": assistant}])
    chat_history.append({"role": "user", "content": message})
    input_ids = tokenizer.apply_chat_template(
        chat_history, return_tensors="pt").to(model.device)
    streamer = TextIteratorStreamer(
        tokenizer, timeout=10.0, skip_prompt=True, skip_special_tokens=True)
    generate_kwargs = dict(
        input_ids=input_ids,
        streamer=streamer,
        max_new_tokens=1024,
        do_sample=True,
        temperature=0.6,
        top_p=0.8,
        eos_token_id=terminators
    )
    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()
    outputs = []
    for text in streamer:
        outputs.append(text)
        yield "".join(outputs)


def chat_bot():
    chatbot = gr.Chatbot(height=450, label='chat_llama3')
    with gr.Blocks(fill_height=True) as demo:
        gr.ChatInterface(
            fn=chat_llama3,
            chatbot=chatbot,
            fill_height=True
        )
    return demo


if __name__ == "__main__":
    demo = chat_bot()
    demo.launch(server_name="0.0.0.0", server_port=6006)

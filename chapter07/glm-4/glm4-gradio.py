from transformers import AutoModel, AutoTokenizer
import gradio as gr
# 置模型路径和加载模型
model_path = "dataroot/models/THUDM/glm-4-9b-chat"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModel.from_pretrained(model_path, trust_remote_code=True).cuda()
model = model.eval()


def predict(input, chatbot, max_length, top_p, temperature, history, past_key_values):
    """预测函数"""
    chatbot.append(input)
    for response, history, past_key_values in model.stream_chat(
            tokenizer, input, history,
            past_key_values=past_key_values,
            return_past_key_values=True,
            max_length=max_length,
            top_p=top_p,
            temperature=temperature):
        chatbot[-1] = (input, response)
        yield chatbot, history, past_key_values


def reset_state():
    """清除Chat历史"""
    return [], [], None


with gr.Blocks() as demo:
    """创建Gradio应用程序"""
    gr.HTML("""<h1 align="center">GLM-4 Demo</h1>""")
    with gr.Row():
        with gr.Column(scale=5):
            chatbot = gr.Chatbot()
            user_input = gr.Textbox(
                show_label=False, placeholder="请输入问题...", max_lines=1)
        with gr.Column(scale=1):
            clearBtn = gr.Button("清除历史")
            max_length = gr.Slider(
                0, 32768, value=8192, step=1.0,
                label="最大生成长度", interactive=True)
            top_p = gr.Slider(0, 1, value=0.8, step=0.01,
                              label="Top P", interactive=True)
            temperature = gr.Slider(
                0, 1, value=0.95, step=0.01, label="Temperature",
                interactive=True)

    history = gr.State([])
    past_key_values = gr.State(None)
    user_input.submit(predict, [user_input, chatbot, max_length, top_p,
                                temperature, history, past_key_values],
                      [chatbot, history, past_key_values])
    user_input.submit(lambda x: "", user_input, user_input)
    clearBtn.click(reset_state, outputs=[
                   chatbot, history, past_key_values])

# 启动Gradio应用程序
demo.queue().launch(server_name="0.0.0.0")

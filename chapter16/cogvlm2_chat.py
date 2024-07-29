import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = "dataroot/models/" + \
    "THUDM/cogvlm2-llama3-chinese-chat-19B-int4"
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
TORCH_TYPE = torch.bfloat16 if torch.cuda.is_available() \
    and torch.cuda.get_device_capability()[
    0] >= 8 else torch.float16
model = None
tokenizer = None


def load_model():
    global model
    global tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH,
        trust_remote_code=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        torch_dtype=TORCH_TYPE,
        trust_remote_code=True,
        low_cpu_mem_usage=True,
    ).eval()


def generate(image_path: str):
    image = Image.open(image_path).convert('RGB')
    input_by_model = model.build_conversation_input_ids(
        tokenizer,
        query="图里是什么？只需要输出图里的文本本身",
        history=[],
        images=[image],
        template_version='chat'
    )
    inputs = {
        'input_ids': input_by_model['input_ids']
        .unsqueeze(0).to(DEVICE),
        'token_type_ids': input_by_model['token_type_ids']
        .unsqueeze(0).to(DEVICE),
        'attention_mask': input_by_model['attention_mask']
        .unsqueeze(0).to(DEVICE),
        'images': [[input_by_model['images'][0].to(DEVICE)
                    .to(TORCH_TYPE)]],
    }
    gen_kwargs = {
        "max_new_tokens": 2048,
        "pad_token_id": 128002,
    }
    with torch.no_grad():
        outputs = model.generate(**inputs, **gen_kwargs)
        outputs = outputs[:, inputs['input_ids'].shape[1]:]
        response = tokenizer.decode(outputs[0])
        response = response.split("<|end_of_text|>")[0]
        return response


if __name__ == '__main__':
    load_model()
    response = generate('test1.png')
    print(response)

import torch
from datasets import load_dataset
from trl import SFTTrainer
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig
import time
import argparse


def load_model(load_in_8bit, model_path, data_file):
    # 装载模型和数据集
    data = load_dataset(
        "json", data_files=data_file)
    # 数据切分成2000条的验证集和剩余的训练集
    dataset = data["train"].train_test_split(
        test_size=2000, shuffle=True, seed=42
    )
    # 根据load_in_8bit判断是否使用8bit量化装载
    bnb_config = BitsAndBytesConfig(
        load_in_8bit=load_in_8bit
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        quantization_config=bnb_config if load_in_8bit else None,
        torch_dtype=torch.float16,
        device_map='auto')
    # 启用输入的梯度需求，允许模型输入的梯度被计算和存储
    model.enable_input_require_grads()

    tokenizer = AutoTokenizer.from_pretrained(
        model_path, pad_token="<|endoftext|>")
    return model, tokenizer, dataset


def formatting_prompts_func(examples):
    # 重新整理数据集格式（按单轮会话处理）
    output_text = []
    instruction = examples["instruction"]
    response = examples["output"]
    text = f'''Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request. 
    ### Instruction:
    {instruction}  
    ### Response:
    {response}
    '''
    output_text.append(text)
    return output_text


def prepareTrainer(model, tokenizer, dataset):
    # 准备训练器，设定训练参数
    train_args = TrainingArguments(
        num_train_epochs=3,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=1,
        gradient_checkpointing=True,
        warmup_steps=5,
        learning_rate=2e-4,
        fp16=False,
        bf16=True,
        logging_steps=1,
        max_grad_norm=0.5,
        weight_decay=0.01,
        lr_scheduler_type="linear",
        optim="paged_adamw_32bit",
        seed=8888,
        output_dir="output/PEFT/model",
        save_steps=50,
        save_total_limit=3
    )

    peft_params = LoraConfig(
        lora_alpha=16,
        lora_dropout=0.1,
        r=8,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj",
                        "o_proj", "gate_proj", "up_proj", "down_proj"]
    )

    trainer = SFTTrainer(
        model,
        tokenizer=tokenizer,
        train_dataset=dataset['train'],
        eval_dataset=dataset['test'],
        max_seq_length=512,
        peft_config=peft_params,
        formatting_func=formatting_prompts_func,
        args=train_args
    )
    return trainer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--load_in_8bit', default=False,
                        action='store_true', required=False)
    parser.add_argument('--model_path',
                        default="./dataroot/models/NousResearch/Meta-Llama-3-8B-Instruct",
                        type=str, required=False)
    parser.add_argument('--data_file',
                        default="alpaca_data.json",
                        type=str, required=False)
    args = parser.parse_args()
    model, tokenizer, dataset = load_model(
        args.load_in_8bit, args.model_path, args.data_file)
    trainer = prepareTrainer(model, tokenizer, dataset)
    trainer.train()
    trainer.model.save_pretrained(trainer.args.output_dir)
    tokenizer.save_pretrained(trainer.args.output_dir)

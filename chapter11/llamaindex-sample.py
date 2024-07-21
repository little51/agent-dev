import os
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Settings
)
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent

llm = OpenAI(model="gpt-4",
             api_base="http://172.16.62.167:8000/v1",
             api_key="EMPTY")

Settings.llm = llm
Settings.embed_model = HuggingFaceEmbedding(
    model_name="dataroot/models/BAAI/bge-small-en-v1.5"
)


def build_index(source_path, index_path):
    if len(os.listdir(source_path)) == 0:
        print("文档文件夹为空")
        return False
    if len(os.listdir(index_path)) > 0:
        print("索引已存在")
        return False
    reader = SimpleDirectoryReader(input_dir=source_path)
    documents = reader.load_data()
    parser = SimpleNodeParser.from_defaults(chunk_size=1024,
                                            chunk_overlap=20)
    nodes = parser.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes)
    index.storage_context.persist(persist_dir=index_path)
    return True


def load_index(index_path):
    if not os.path.exists(index_path + "/docstore.json"):
        return None
    storage_context = StorageContext.from_defaults(
        persist_dir=index_path
    )
    return load_index_from_storage(storage_context)


def init_tool(index):
    engine = index.as_query_engine(similarity_top_k=3)
    return [
        QueryEngineTool(
            query_engine=engine,
            metadata=ToolMetadata(
                name="文档检索",
                description=(
                    "从本地的文档索引中检索数据"
                    "使用详细的纯文本问题作为工具的输入"
                ),
            ),
        )
    ]


def prepare_folder():
    source_path = "./documents"
    if not os.path.exists(source_path):
        os.makedirs(source_path)
    index_path = "./indexs"
    if not os.path.exists(index_path):
        os.makedirs(index_path)
    return source_path, index_path


def init_agent():
    # 准备文件夹
    source_path, index_path = prepare_folder()
    # 建立索引
    build_index(source_path, index_path)
    # 装载索引
    index = load_index(index_path)
    if index is None:
        return None
    # 初始化工具
    query_engine_tool = init_tool(index)
    # 初始化Agent
    agent = OpenAIAgent.from_tools(query_engine_tool, verbose=True)
    return agent


if __name__ == "__main__":
    agent = init_agent()
    if agent is None:
        print("索引装载失败")
        exit()
    response = agent.chat("LlamaIndex")
    print(response)

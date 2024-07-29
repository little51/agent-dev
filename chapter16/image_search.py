import os
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from cogvlm2_chat import load_model, generate
import gradio as gr

vectorstore = None


def load_docs(directory):
    images = os.listdir(directory)
    documents = []
    for image in images:
        if image.endswith(".png"):
            doc = Document(
                page_content=generate(image),
                metadata={"source": image}
            )
            documents.append(doc)
    print("======CogVLM2识图结果======")
    print(documents)
    return documents


def split_docs(documents):
    text_splitter = CharacterTextSplitter(chunk_size=150,
                                          chunk_overlap=20)
    split_docs = text_splitter.split_documents(documents)
    return split_docs


def create_vectorstore(split_docs):
    embeddings = SentenceTransformerEmbeddings(
        model_name="./dataroot/models/" +
        "shibing624/text2vec-base-chinese")
    vectorstore = Chroma.from_documents(split_docs, embeddings)
    return vectorstore


def init_searchengine():
    global vectorstore
    load_model()
    documents = load_docs("./")
    splited_docs = split_docs(documents)
    vectorstore = create_vectorstore(splited_docs)


def search_from_vectorstore(vectorstore, query):
    matching_docs = vectorstore.similarity_search_with_score(query, k=2)
    return matching_docs


def search_by_text(query):
    global vectorstore
    matching_docs = search_from_vectorstore(vectorstore, query)
    print("======从向量库检索结果======")
    print(matching_docs)
    search_results = []
    for doc, _ in matching_docs:
        search_results.append(doc.metadata["source"])
    return search_results


def webui():
    with gr.Blocks() as demo:
        gr.HTML("""<h1 align="center">图片搜索Demo</h1>""")
        with gr.Column():
            with gr.Row():
                user_input = gr.Textbox(
                    show_label=False,
                    placeholder="请输入...",
                    max_lines=1)
            with gr.Row():
                gallery = gr.Gallery(
                    label="图片列表",
                    show_label=False,
                    elem_id="gallery",
                    columns=[3],
                    object_fit="contain",
                    height="auto",
                    interactive=False
                )
        user_input.submit(search_by_text, inputs=user_input, outputs=gallery)
        user_input.submit(lambda x: "", user_input, user_input)
    demo.launch(server_name="0.0.0.0")


if __name__ == "__main__":
    init_searchengine()
    webui()

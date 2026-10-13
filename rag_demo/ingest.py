import os

import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI

from config import  API_KEY_SILICON, BASE_KEY_SILICON, EMBED_MODEL, DB_PATH


embed_oai = OpenAI(
    api_key=API_KEY_SILICON, 
    base_url=BASE_KEY_SILICON
)



def read_doc(path):
    """读文档，先支持 txt 和 md。"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def ingest_file(path, collection):
    """把文档切分入库，带来源信息。"""
    if embed_oai is None:
        raise RuntimeError("未配置 SiliconFlow API Key，无法进行文档向量化")

    text = read_doc(path)
    filename = os.path.basename(path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", "。", "!", "?", " ", ""],
    )
    chunks = splitter.split_text(text)
    print(f"文档{filename}切分为{len(chunks)}段")

    for i, chunk in enumerate(chunks):
        vec = embed_oai.embeddings.create(model=EMBED_MODEL,input="passage: "+chunk).data[0].embedding
        collection.add(
            documents=[chunk],
            embeddings=[vec],
            ids=[f"{filename}_{i}"],
            metadatas=[{"source": filename, "chunk": i}],
        )


if __name__ == "__main__":
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name="knowledge")

    folder = ".docs"
    if not os.path.isdir(folder):
        print(f"文档目录不存在: {folder}，跳过导入。")
    else:
        for name in os.listdir(folder):
            if name.endswith((".txt", ".md")):
                ingest_file(os.path.join(folder, name), collection)

    print(f"全部导入完成，共:{collection.count()}段")
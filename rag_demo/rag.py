import chromadb
from openai import OpenAI
from config import API_KEY,BASE_URL,API_KEY_SILICON,BASE_KEY_SILICON,CHAT_MODEL,EMBED_MODEL,DB_PATH

oai = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

embed_oai = OpenAI(
    api_key=API_KEY_SILICON,
    base_url=BASE_KEY_SILICON
)


def retreieve(question,n=3):
    """检索最相关的n个片段，返回内容加来源"""
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name="knowledge")
    vec = embed_oai.embeddings.create(
        model = EMBED_MODEL,
        input = "query: " + question
    ).data[0].embedding
    result = collection.query(query_embeddings=[vec],n_results=n)
    print("检索到的文档:",result["documents"])
    print("相似度距离:",result["distances"])

    hits = []
    for doc,meta in zip(result["documents"][0],result["metadatas"][0]):
        hits.append({"text":doc,"source":meta["source"]})
    return hits

def answer(question):
    """检索+生成回答"""
    hits = retreieve(question)

    context = "\n\n".join(
        f"[{i+1}] (来自 {h['source']}) \n{h['text']}"
        for i,h in enumerate(hits)
    )

    prompt = f"""你是一个严谨的知识库助手。请只根据下面的资料回答问题。
要求：
1.资料里面没有提到的内容，直接回答"资料中没有相关内容",不要编造。
2.回答时在句末标注依据来源，格式如[1]。
3.回答要用中文，条理清晰，不超过300字

资料：
{context}

问题：
{question}
"""
    response = oai.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role":"user","content":prompt}]
    )
    return response.choices[0].message.content,hits
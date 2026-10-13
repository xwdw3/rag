from rag import answer

print("知识库助手已就绪，请输入问题开始(输入 退出 结束)")

while True:
    question =  input("\n你：")
    if question == "退出":
        break
    if not question:
        continue

    result,hits = answer(question)
    print("\nAI:",result)

    print("\n---依据来源---")
    for i,h in enumerate(hits,1):
        print(f"[{i}] {h['source']}")
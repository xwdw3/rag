README.md
 
markdown
  
# RAG Demo
ChromaDB + BGE-M3 + DeepSeek 简易RAG检索问答

## 依赖安装
```bash
pip install chromadb openai langchain-text-splitters fastapi uvicorn
 
 
项目结构
 
-  config.py ：API与模型配置
-  ingest.py ：文档入库脚本
-  rag.py ：检索+问答核心逻辑
-  app.py ：FastAPI服务入口
-  chroma_db/ ：向量数据库
-  __pycache__/ ：缓存文件
 
运行
 
1. 配置  config.py  填入API密钥
2. 文档入库： python ingest.py 
3. 启动服务： uvicorn app:app --reload 
 
注意
1. BGE-M3：查询加 query: ，入库文本加 passage: 

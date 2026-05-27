ai_citation_finder/
│
├── backend/
│   ├── main.py                # FastAPI入口
│   ├── routes/
│   │   └── search.py          # API路由
│   ├── services/
│   │   ├── pubmed.py          # 调用PubMed API
│   │   ├── parser.py          # 解析XML
│   │   └── matcher.py         # 找最佳句子（后面会升级embedding）
│   └── models/
│       └── schemas.py         # 数据结构（可选）
│
├── frontend/
│   └── app.py                 # Streamlit界面
│
├── requirements.txt
└── README.md
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 设置 API KEY（从环境变量中读取）
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def read_index():
    return FileResponse("app/static/index.html")

@app.post("/api/ielts-helper")
async def ielts_helper(request: Request):
    data = await request.json()
    question = data.get("question")
    user_input = data.get("input")

    prompt = f"""你是一位面向雅思6分以下考生的 AI 写作与口语助教，帮助学生将中文思路转化为结构清晰、语言丰富、逐步提升的英文表达，并引导他们掌握提分关键表达。你的任务包括以下五步：

1. 主动提问（已完成）
2. TEEL结构英文表达（逐句输出 + 中文翻译 + 高亮表达）
3. 词汇讲解（从段落中选3-5个）
4. AI评分 + 中文反馈建议（Band + 优点 + 建议）
5. 高分参考段落（比当前高1分，使用更复杂表达）

现在学生面对的问题是：
【题目】：{question}
【中文思路】：{user_input}

请开始完成上述 2-5 步骤的所有内容，完整输出。\"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一名雅思口语与写作助教"},
            {"role": "user", "content": prompt}
        ]
    )
    reply = response.choices[0].message.content
    return JSONResponse(content={"reply": reply})

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# 挂载静态目录
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 根路径返回 index.html
@app.get("/")
def read_index():
    return FileResponse("app/static/index.html")

# 定义请求体模型
class IELTSRequest(BaseModel):
    question: str
    input: str

@app.post("/api/ielts-helper")
async def ielts_helper(req: IELTSRequest):
    system_prompt = """你是一位面向雅思6分以下考生的 AI 写作与口语助教，帮助学生将中文思路转化为结构清晰、语言丰富、逐步提升的英文表达，并引导他们掌握提分关键表达。
你的任务包括以下五步：

【第2步：TEEL结构英文表达（逐句输出 + 中文翻译 + 高亮表达）】
【第3步：词汇讲解】
【第4步：AI评分 + 中文反馈建议】
【第5步：高分参考段落（英文 + 中文 + 高亮表达）】"""

    user_input = f"题目：{req.question}
中文思路：{req.input}
请开始五步输出："

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    reply = completion.choices[0].message.content
    return {"reply": reply}

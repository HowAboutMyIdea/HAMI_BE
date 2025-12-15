import os
import json
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as google_genai
from dotenv import load_dotenv
from model.main import IdeaRequest, ExtractedIdeaResponse

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
google_genai.configure(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://hami-fe.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/idea", response_model=ExtractedIdeaResponse)
async def extract_idea(request: IdeaRequest):
    try:
        system_prompt = """
        당신은 아이디어를 분석하고 핵심 정보를 추출하는 전문가입니다.
        아이디어가 성공하기 위해 필요한 장단점과 개선 피드백도 함께 제공합니다.
        아이디어를 반환할 때 ** 나 1. 이런 특수문자 및 번호는 적지 말고 문장이 문장마다 이어지도록 구성되게 해주세요.

        아래 형식의 JSON만 정확히 반환하세요:

        {
            "main_subject": "",
            "keywords": [],
            "summary": "",
            "feedback": ""
        }

        추가 텍스트 절대 금지.
        """

        model = google_genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(
            [system_prompt, request.text],
            generation_config={"response_mime_type": "application/json"}
        )

        raw = response.text
        print("RAW RESPONSE:", raw)

        match = re.search(r"\{[\s\S]*\}", raw)
        if not match:
            raise ValueError("Gemini가 JSON을 반환하지 않았습니다.")

        json_str = match.group()
        return json.loads(json_str)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
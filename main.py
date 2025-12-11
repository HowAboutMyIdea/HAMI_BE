import os
import json
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv
from model.main import IdeaRequest, ExtractedIdeaResponse

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/idea", response_model=ExtractedIdeaResponse)
async def extract_idea(request: IdeaRequest):
    try:
        system_prompt = """
        당신은 아이디어를 분석하고 핵심 정보를 추출하는 전문가입니다.

        아래 형식의 JSON만 반환하세요:
        {
            "main_subject": "",
            "keywords": [],
            "summary": ""
        }

        추가 텍스트 절대 금지.
        """

        model = genai.GenerativeModel("gemini-2.5-flash")

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
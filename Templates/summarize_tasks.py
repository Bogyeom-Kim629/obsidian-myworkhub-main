import os
import re
import openai
from dotenv import load_dotenv

# ===== 1. 환경변수 로드 =====
# 프로젝트 루트(.env 파일 있는 곳)에 다음 라인을 추가하세요:
# OPENAI_API_KEY=sk-...
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path=env_path)
openai.api_key = os.getenv("OPENAI_API_KEY")

# ===== 2. OpenAI 호출 함수 =====
def call_openai(prompt_text: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_text}],
            max_tokens=1024,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ OpenAI API 호출 실패:", e)
        return ""

# ===== 3. 프롬프트 생성 =====
def build_prompt(markdown_text: str) -> str:
    return f"""
다음은 Obsidian의 업무 Task 노트입니다. 이 정보를 기반으로 다음 내용을 요약해줘:

- 한 문장으로 정리한 핵심 Summary
- Problem Statement
- Business Impact
- Action Items (번호 형식)

내용:
{markdown_text}
"""

# ===== 4. Summary 섹션 업데이트 =====
def update_summary_section(filepath: str, summary_text: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    summary_block = f"## 🧠 Summary\n{summary_text}\n"
    if "## 🧠 Summary" in content:
        new_content = re.sub(
            r"## 🧠 Summary[\s\S]*?(?=##|$)",
            summary_block,
            content
        )
    else:
        new_content = content + "\n\n" + summary_block

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

# ===== 5. 전체 Task 폴더 순회 및 요약 =====
def summarize_tasks(folder_name: str = "Tasks"):
    task_folder = os.path.join(base_dir, folder_name)
    for filename in os.listdir(task_folder):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(task_folder, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            md_content = f.read()

        prompt = build_prompt(md_content)
        summary = call_openai(prompt)
        if summary:
            update_summary_section(filepath, summary)
            print(f"✅ '{filename}' 요약 완료")
        else:
            print(f"⚠️ '{filename}' 요약 실패")

# ===== ▶ 스크립트 실행 =====
if __name__ == "__main__":
    summarize_tasks()

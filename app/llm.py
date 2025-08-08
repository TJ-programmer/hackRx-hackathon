import os
from app.logging_config import setup_logger
from dotenv import load_dotenv

load_dotenv()

logger = setup_logger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY not set in environment.")
    raise RuntimeError("OPENAI_API_KEY not found.")

try:
    from openai import OpenAI
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENAI_API_KEY"),
    )
    use_new_sdk = True
    logger.info("Using OpenAI SDK >= 1.0")
except ImportError:
    import openai
    openai.api_key = OPENAI_API_KEY
    use_new_sdk = False
    logger.info("Using legacy OpenAI SDK < 1.0")

def generate_answer(context: str, question: str, model: str = "deepseek/deepseek-chat-v3-0324:free", max_tokens: int = 300) -> str:
    if not context.strip() or not question.strip():
        logger.warning("Empty context or question.")
        return "Error: Context or question is missing."

    messages = [
            {
                "role": "system",
                "content": "You are a concise assistant. Always respond with a single-sentence answer based only on the provided context."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}\n\nRespond briefly in one sentence."
            }
        ]

    try:
        logger.debug(f"Calling OpenAI with model={model}, max_tokens={max_tokens}")
        if use_new_sdk:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.2,
            )
            answer = response.choices[0].message.content.strip()
        else:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.2,
            )
            answer = response["choices"][0]["message"]["content"].strip()

        logger.info("OpenAI response received.")
        return answer

    except Exception as e:
        logger.exception("OpenAI API call failed.")
        return f"Error: Failed to generate answer due to API error. {str(e)}"

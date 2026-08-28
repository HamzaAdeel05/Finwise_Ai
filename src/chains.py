from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.chains import LLMChain

from .config import OPENAI_API_KEY
from .prompts import CHAT_PROMPT_TEMPLATE, NARRATIVE_CHAT_TEMPLATE, PROMPT_TEMPLATE

def get_llm(model="gpt-4o-mini"):
    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Put it in your local .env file."
        )

    return ChatOpenAI(
        model=model,
        api_key=OPENAI_API_KEY,
        temperature=0.2,
    )

def build_llm_chain(llm):
    """Reusable LLMChain required by the assignment."""
    return LLMChain(
        llm=llm,
        prompt=PROMPT_TEMPLATE,
        output_key="text",
    )

def analyze_finances(llm, data, goal, currency):
    chain = LLMChain(
        llm=llm,
        prompt=CHAT_PROMPT_TEMPLATE,
        output_key="text",
    )
    result = chain.invoke({
        **data,
        "financial_goal": goal,
        "currency": currency,
    })
    return result["text"]

def stream_recommendations(llm, inputs):
    messages = NARRATIVE_CHAT_TEMPLATE.format_messages(**inputs)
    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content

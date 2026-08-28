from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

SYSTEM_PROMPT = """
You are FinWise AI, an educational personal budgeting assistant.

Safety rules:
- Provide informational budgeting education only.
- Do not provide guaranteed investment returns or guaranteed financial outcomes.
- Do not recommend specific securities or execute financial transactions.
- Do not claim to be a financial advisor.
- Encourage the user to consult a qualified financial professional for important decisions.
- Base observations on the supplied numbers and clearly distinguish facts from suggestions.
- Never invent missing financial data.

Return ONLY valid JSON matching the requested schema.
"""

HUMAN_PROMPT = """
Analyze this monthly budget:

Monthly income: {monthly_income}
Total expenses: {total_expenses}
Remaining income: {remaining_income}
Current monthly savings: {savings}
Savings ratio: {savings_ratio}%
Expense ratio: {expense_ratio}%
Financial goal: {financial_goal}
Expense breakdown: {expense_breakdown}

Return exactly this JSON structure:
{{
  "financial_summary": "",
  "financial_health_score": 0,
  "spending_analysis": [
    {{"category": "", "observation": "", "recommendation": ""}}
  ],
  "risk_level": "",
  "top_priorities": [],
  "budget_recommendations": [],
  "savings_strategy": [],
  "next_month_action_plan": []
}}

Score bands are educational only:
80-100 strong
60-79 generally healthy
40-59 needs improvement
below 40 high attention
"""

PROMPT_TEMPLATE = PromptTemplate(
    input_variables=[
        "monthly_income", "total_expenses", "remaining_income",
        "savings", "savings_ratio", "expense_ratio",
        "financial_goal", "expense_breakdown"
    ],
    template=HUMAN_PROMPT,
)

CHAT_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", HUMAN_PROMPT),
])

NARRATIVE_CHAT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT + """
For this response, write a short educational recommendation in normal text.
Do not use JSON. Do not make guarantees.
"""),
    ("human", """
Income: {monthly_income}
Expenses: {total_expenses}
Remaining: {remaining_income}
Savings: {savings}
Savings ratio: {savings_ratio}%
Expense ratio: {expense_ratio}%
Goal: {financial_goal}
Expense breakdown: {expense_breakdown}

Give a concise, practical educational recommendation for next month.
"""),
])

def message_demo():
    """Shows the three core LangChain message types requested by the assignment."""
    return [
        SystemMessage(content="You are an educational financial assistant."),
        HumanMessage(content="Please analyze my monthly budget."),
        AIMessage(content="I can provide informational budgeting insights based on your numbers."),
    ]

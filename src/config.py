import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CURRENCY_OPTIONS = ["USD", "PKR", "EUR", "GBP", "AED", "SAR"]

GOAL_OPTIONS = [
    "Save money",
    "Emergency fund",
    "Pay off debt",
    "Vacation",
    "Start a business",
    "Improve budgeting",
]

EXPENSE_CATEGORIES = [
    "housing/rent",
    "food",
    "transportation",
    "utilities",
    "education",
    "healthcare",
    "entertainment",
    "loan/debt",
    "other",
]

def calculate_financials(monthly_income, expenses, savings):
    """Deterministic financial calculations. No AI is used here."""

    total_expenses = sum(float(v) for v in expenses.values())
    remaining_income = float(monthly_income) - total_expenses

    if monthly_income > 0:
        savings_ratio = (float(savings) / monthly_income) * 100
        expense_ratio = (total_expenses / monthly_income) * 100
    else:
        savings_ratio = 0.0
        expense_ratio = 0.0

    debt = float(expenses.get("loan/debt", 0))
    debt_ratio = (debt / monthly_income * 100) if monthly_income > 0 else 0.0

    # Educational heuristic only — not a financial-industry scoring model.
    savings_score = min(savings_ratio, 30) / 30 * 35
    leftover_score = max(0, min(remaining_income / monthly_income * 100, 30)) / 30 * 25 if monthly_income > 0 else 0
    expense_score = max(0, min(100 - expense_ratio, 30)) / 30 * 25
    debt_score = max(0, min(100 - debt_ratio, 20)) / 20 * 15

    preliminary_score = round(
        max(0, min(100, savings_score + leftover_score + expense_score + debt_score))
    )

    return {
        "monthly_income": float(monthly_income),
        "total_expenses": round(total_expenses, 2),
        "remaining_income": round(remaining_income, 2),
        "savings": float(savings),
        "savings_ratio": round(savings_ratio, 2),
        "expense_ratio": round(expense_ratio, 2),
        "debt_ratio": round(debt_ratio, 2),
        "preliminary_score": preliminary_score,
        "expense_breakdown": {k: round(float(v), 2) for k, v in expenses.items()},
    }

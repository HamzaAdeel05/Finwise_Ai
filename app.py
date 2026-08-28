from dotenv import load_dotenv

# rest of your imports...
import streamlit as st
from src.config import CURRENCY_OPTIONS, EXPENSE_CATEGORIES, GOAL_OPTIONS
from src.financial_calculator import calculate_financials
from src.chains import get_llm, analyze_finances, stream_recommendations
from src.cache_manager import configure_cache
from src.utils import safe_parse_json

load_dotenv()
st.set_page_config(page_title="FinWise AI", page_icon="💰", layout="wide")

DISCLAIMER = (
    "⚠️ **Educational prototype only.** FinWise AI provides informational "
    "budgeting insights, not financial, investment, tax, or legal advice. "
    "It does not execute transactions or connect to bank accounts. "
    "Consult a qualified financial professional before making financial decisions."
)

st.title("💰 FinWise AI")
st.caption("AI-Powered Personal Financial Analysis & Smart Budget Assistant")
st.info(DISCLAIMER)

with st.sidebar:
    st.header("FinWise AI")
    st.caption("LangChain + Streamlit FinTech assignment")
    st.warning(DISCLAIMER)
    st.divider()

    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4.1-mini"])
    cache_type = st.selectbox("LLM cache", ["InMemoryCache", "SQLiteCache"])
    configure_cache(cache_type)

    if st.button("🔄 Reset session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.divider()
    st.caption("For informational/educational purposes only.")

with st.form("financial_form"):
    st.subheader("1. Your monthly financial information")

    c1, c2, c3 = st.columns(3)
    with c1:
        currency = st.selectbox("Currency", CURRENCY_OPTIONS)
        income = st.number_input("Monthly income", min_value=0.0, step=100.0)
    with c2:
        savings = st.number_input("Current monthly savings", min_value=0.0, step=100.0)
        goal = st.selectbox("Financial goal", GOAL_OPTIONS)
    with c3:
        st.write("Expense categories")
        st.caption("Enter your approximate monthly amounts.")

    expenses = {}
    cols = st.columns(2)
    for i, category in enumerate(EXPENSE_CATEGORIES):
        with cols[i % 2]:
            expenses[category] = st.number_input(
                category.title(), min_value=0.0, step=50.0, key=f"expense_{category}"
            )

    submitted = st.form_submit_button("📊 Analyze my finances", type="primary")

if submitted:
    data = calculate_financials(income, expenses, savings)

    st.session_state["financial_data"] = data
    st.session_state["currency"] = currency
    st.session_state["goal"] = goal

    st.subheader("2. Financial overview")
    a, b, c, d = st.columns(4)
    a.metric("Income", f"{currency} {income:,.2f}")
    b.metric("Total expenses", f"{currency} {data['total_expenses']:,.2f}")
    c.metric("Remaining", f"{currency} {data['remaining_income']:,.2f}")
    d.metric("Savings", f"{currency} {savings:,.2f}")

    st.caption(
        f"Python preliminary score: **{data['preliminary_score']}/100** · "
        f"Savings ratio: **{data['savings_ratio']:.1f}%** · "
        f"Expense ratio: **{data['expense_ratio']:.1f}%**"
    )

    if data["remaining_income"] < 0:
        st.error("Your expenses currently exceed your monthly income.")
    elif data["remaining_income"] == 0:
        st.warning("Your income is fully allocated. There is currently no monthly buffer.")
    else:
        st.success("Your expenses are below your income, leaving a monthly buffer.")

    st.subheader("3. AI financial analysis")
    try:
        llm = get_llm(model)
        with st.spinner("FinWise AI is analyzing your numbers..."):
            result_text = analyze_finances(llm, data, goal, currency)
        result = safe_parse_json(result_text)

        if result is None:
            st.error("The model returned invalid JSON. Try submitting again.")
            st.code(result_text)
        else:
            score = max(0, min(100, int(result.get("financial_health_score", 0))))
            st.metric("AI financial health score", f"{score}/100")
            st.progress(score / 100)

            st.markdown("### Summary")
            st.write(result.get("financial_summary", ""))

            risk = result.get("risk_level", "Unknown")
            if str(risk).lower() in {"high", "high risk"}:
                st.error(f"Risk level: {risk}")
            elif str(risk).lower() in {"medium", "medium risk"}:
                st.warning(f"Risk level: {risk}")
            else:
                st.success(f"Risk level: {risk}")

            tabs = st.tabs([
                "Spending analysis", "Priorities",
                "Budget recommendations", "Savings strategy",
                "Next month plan"
            ])

            with tabs[0]:
                for item in result.get("spending_analysis", []):
                    with st.expander(item.get("category", "Category")):
                        st.write("**Observation:**", item.get("observation", ""))
                        st.write("**Recommendation:**", item.get("recommendation", ""))

            with tabs[1]:
                for item in result.get("top_priorities", []):
                    st.write("•", item)

            with tabs[2]:
                for item in result.get("budget_recommendations", []):
                    st.write("•", item)

            with tabs[3]:
                for item in result.get("savings_strategy", []):
                    st.write("•", item)

            with tabs[4]:
                for item in result.get("next_month_action_plan", []):
                    st.write("•", item)

            st.subheader("4. Streaming recommendation")
            st.caption("This section demonstrates LangChain's .stream() API.")
            inputs = {
                "monthly_income": data["monthly_income"],
                "total_expenses": data["total_expenses"],
                "remaining_income": data["remaining_income"],
                "savings": data["savings"],
                "savings_ratio": data["savings_ratio"],
                "expense_ratio": data["expense_ratio"],
                "financial_goal": goal,
                "expense_breakdown": data["expense_breakdown"],
            }
            st.write_stream(stream_recommendations(llm, inputs))

    except Exception as exc:
        st.error("Something went wrong while calling the AI model.")
        st.exception(exc)

st.divider()
st.info(DISCLAIMER)

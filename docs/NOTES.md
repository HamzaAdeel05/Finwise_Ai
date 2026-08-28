# Assignment implementation notes

## Why calculate with Python first?

Financial ratios and totals are deterministic. Given identical inputs, they should produce identical values. Python is therefore responsible for arithmetic.

The LLM receives the calculated values and explains them in educational language.

## Why structured JSON?

The UI needs predictable fields. Instead of trying to extract arbitrary text, the app asks the model for a fixed schema and validates it with `safe_parse_json()`.

## Why two scores?

The Python preliminary score demonstrates deterministic business logic.

The AI financial health score demonstrates LLM-generated qualitative interpretation.

Neither score is a professional financial rating.

## Message classes

SystemMessage = assistant's role and rules.

HumanMessage = user's request/data.

AIMessage = assistant's response.

`message_demo()` in `src/prompts.py` demonstrates all three.

## LLMChain

`build_llm_chain()` demonstrates the reusable LLMChain requested by the assignment. The main analysis also uses the same LangChain chain concept with the chat prompt.

## Streaming

The narrative recommendation uses `llm.stream()`. Streamlit consumes the generator with `st.write_stream()` so text appears progressively.

import subprocess
import shlex
import pandas as pd
import streamlit as st

try:
    from langchain_ollama import OllamaLLM
except Exception:
    try:
        from langchain_community.llms import Ollama as OllamaLLM
    except Exception:
        OllamaLLM = None

from langchain_experimental.agents import create_pandas_dataframe_agent

def list_local_ollama_models():
    """Return a list of local Ollama models."""
    try:
        out = subprocess.check_output(shlex.split("ollama list"), text=True, stderr=subprocess.STDOUT)
        models = []
        for line in out.splitlines():
            line = line.strip()
            if not line or line.lower().startswith("name") or line.lower().startswith("----"):
                continue
            models.append(line.split()[0])
        return models if models else ["llama3"]
    except Exception:
        return ["llama3"]

def create_agent(df: pd.DataFrame, model_name="llama3"):
    """
    Creates an optimized Ollama-based DataFrame agent.
    Uses smaller context and disables strict JSON parsing to avoid output errors.
    """
    if OllamaLLM is None:
        raise ImportError(
            "No Ollama LLM wrapper found. Install 'langchain-ollama' or 'langchain-community'."
        )

    llm = OllamaLLM(
        model=model_name,
        options={
            "num_ctx": 1024,
            "num_predict": 256,
            "temperature": 0.3,
            "repeat_penalty": 1.1,
        }
    )

    return create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=False,
        allow_dangerous_code=True,
        handle_parsing_errors=True,        
        return_intermediate_steps=False,   
    )

def run_query(agent, query: str):
    """
    Executes a query on the DataFrame agent.
    Displays the response in Streamlit without breaking on parsing errors.
    """
    try:
        if not query.strip():
            return "⚠️ Please enter a valid question."

        with st.spinner("🤖 Generating response..."):
            if hasattr(agent, "invoke"):
                result = agent.invoke(query)
                if isinstance(result, dict):
                    return result.get("output", str(result))
                return str(result)

            elif hasattr(agent, "run"):
                return str(agent.run(query))

            else:
                return "⚠️ Unsupported agent interface."

    except Exception as e:
        return f"⚠️ Error while processing query: {str(e)}"

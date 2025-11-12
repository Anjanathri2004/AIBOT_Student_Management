import streamlit as st
import json
from data_loader import load_and_concat_csvs
from role_access import get_accessible_data
from query_engine import list_local_ollama_models, create_agent, run_query

st.set_page_config(page_title="Dumroo.ai – AI Data Query System", layout="wide")
st.title("🎓 Dumroo.ai – AI Data Query System")

def load_admins(path="admins.json"):
    """Load admin credentials from a JSON file."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return []

def login_screen(admins):
    """Display login form and return logged-in admin info."""
    st.sidebar.title("🔐 Admin Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    login_button = st.sidebar.button("Login")

    if login_button:
        for admin in admins:
            if admin.get("username") == username and admin.get("password") == password:
                st.session_state["logged_in"] = True
                st.session_state["admin"] = admin
                st.sidebar.success(f"✅ Welcome {username}!")
                return admin
        st.sidebar.error("❌ Invalid credentials")

    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        return st.session_state["admin"]
    return None


admins = load_admins()
admin_info = login_screen(admins)

if not admin_info:
    st.stop()

st.sidebar.markdown(f"👤 **Logged in as:** `{admin_info['username']}`")

if st.sidebar.button("🚪 Logout"):
    for key in ["logged_in", "admin", "agent", "model"]:
        if key in st.session_state:
            del st.session_state[key]
    st.sidebar.success("Logged out successfully! Please login again.")
    st.rerun()

df_all = load_and_concat_csvs()
if df_all.empty:
    st.error("No CSV files found in the `data/` folder.")
    st.stop()

filtered_df = get_accessible_data(admin_info, df_all)
st.markdown(f"**Visible Rows for {admin_info['username']}:** {len(filtered_df)}")

with st.expander("📄 Preview Accessible Data"):
    st.dataframe(filtered_df.head(10))

models = list_local_ollama_models()
model_choice = st.sidebar.selectbox("🤖 Select Ollama Model", models)

if "agent" not in st.session_state or st.session_state.get("model") != model_choice:
    with st.spinner("🚀 Initializing Ollama Agent..."):
        agent = create_agent(filtered_df, model_name=model_choice)
        st.session_state["agent"] = agent
        st.session_state["model"] = model_choice

st.subheader("💬 Ask the AI about your dataset")
query = st.text_input("Enter your question:", placeholder="e.g. Which students scored above 90?")

if st.button("Run Query"):
    if query.strip():
        with st.spinner("🤖 Thinking..."):
            answer = run_query(st.session_state["agent"], query)
            st.success("✅ Answer:")
            st.write(answer)
    else:
        st.warning("⚠️ Please enter a question.")

st.markdown("---")
st.caption("Powered by 🧠 Ollama + LangChain + Streamlit")

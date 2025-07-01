import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
api_key = os.getenv("OPENAI_API_KEY")

# Load data
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "simulated", "all_sessions.parquet"))
df = pd.read_parquet(DATA_PATH)

# LLM setup
llm = OpenAI(api_token=api_key, model="gpt-3.5-turbo")
sdf = SmartDataframe(df, config={"llm": llm})

def ask_motogp_ai(query: str) -> str:
    try:
        return str(sdf.chat(query))
    except Exception as e:
        return f"⚠️ Error: {e}"

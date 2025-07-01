# 🏁 MotoGP AI Strategist

An interactive AI-powered race strategy dashboard for MotoGP. This project combines **Streamlit**, **PandasAI**, and **OpenAI’s GPT-3.5 Turbo** to let you visualize simulated race data, analyze trends like lap times, tyre strategies, and pit stops — and ask natural language questions to an intelligent AI agent.

---

## 📂 Project Structure

```
motogp_AI_strategist/
│
├── .env                       # OpenAI API key (not tracked in Git)
├── simulated/
│   └── all_sessions.parquet   # Simulated MotoGP session data
│
├── src/
│   ├── strategy_dashboard.py  # Streamlit dashboard interface
│   └── ai_strategy_agent.py   # AI query logic using PandasAI
│
└── README.md                  # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd motogp_AI_strategist
```

### 2. (Optional) Create a virtual environment
```bash
conda create -n motogp-ai python=3.10
conda activate motogp-ai
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up the API key
Create a `.env` file in the root of the project:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Launch the dashboard
```bash
streamlit run src/strategy_dashboard.py
```

---

## 💡 What You Can Ask the AI Strategist

You can ask natural language strategy queries like:

- **Performance Analysis**
  - “Which rider had the fastest lap in qualifying?”
  - “Who had the most consistent sector 3 times?”

- **Tyre & Pit Strategy**
  - “Compare tyre choices of all riders in the race.”
  - “Which riders made more than 2 pit stops?”

- **Advanced Strategy**
  - “Did tyre choice impact lap performance?”
  - “Which rider gained the most time after a pit stop?”
  - “Who had the best lap progression in FP2?”

---

## 🧠 Technologies Used

- [Streamlit](https://streamlit.io/) — interactive dashboards
- [PandasAI](https://github.com/gventuri/pandas-ai) — natural language querying of DataFrames
- [OpenAI GPT-3.5 Turbo](https://platform.openai.com/) — AI reasoning engine
- [Matplotlib](https://matplotlib.org/) — data visualization
- [Python 3.10](https://www.python.org/) — core programming

---

## 📌 Notes

- This project uses **simulated** MotoGP data for demonstration.
- You must have valid **OpenAI API credits** to use the AI strategist features.

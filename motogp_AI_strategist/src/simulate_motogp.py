import os
import random
import pandas as pd
import numpy as np

# Set reproducibility
random.seed(42)
np.random.seed(42)

# Real MotoGP 2023 rider roster
riders = [
    {"rider": "Francesco Bagnaia", "team": "Ducati Lenovo Team", "constructor": "Ducati"},
    {"rider": "Fabio Quartararo", "team": "Monster Energy Yamaha MotoGP", "constructor": "Yamaha"},
    {"rider": "Marc Marquez", "team": "Repsol Honda Team", "constructor": "Honda"},
    {"rider": "Brad Binder", "team": "Red Bull KTM Factory Racing", "constructor": "KTM"},
    {"rider": "Aleix Espargaro", "team": "Aprilia Racing", "constructor": "Aprilia"},
    {"rider": "Jorge Martin", "team": "Prima Pramac Racing", "constructor": "Ducati"},
    {"rider": "Jack Miller", "team": "Red Bull KTM Factory Racing", "constructor": "KTM"},
    {"rider": "Maverick Viñales", "team": "Aprilia Racing", "constructor": "Aprilia"},
    {"rider": "Joan Mir", "team": "Repsol Honda Team", "constructor": "Honda"},
    {"rider": "Enea Bastianini", "team": "Ducati Lenovo Team", "constructor": "Ducati"},
    {"rider": "Marco Bezzecchi", "team": "Mooney VR46 Racing Team", "constructor": "Ducati"},
    {"rider": "Luca Marini", "team": "Mooney VR46 Racing Team", "constructor": "Ducati"},
    {"rider": "Takaaki Nakagami", "team": "LCR Honda IDEMITSU", "constructor": "Honda"},
    {"rider": "Alex Rins", "team": "LCR Honda CASTROL", "constructor": "Honda"},
    {"rider": "Johann Zarco", "team": "Prima Pramac Racing", "constructor": "Ducati"},
    {"rider": "Fabio Di Giannantonio", "team": "Gresini Racing MotoGP", "constructor": "Ducati"},
    {"rider": "Alex Marquez", "team": "Gresini Racing MotoGP", "constructor": "Ducati"},
    {"rider": "Raul Fernandez", "team": "CryptoDATA RNF MotoGP Team", "constructor": "Aprilia"},
    {"rider": "Miguel Oliveira", "team": "CryptoDATA RNF MotoGP Team", "constructor": "Aprilia"},
    {"rider": "Augusto Fernandez", "team": "GASGAS Factory Racing Tech3", "constructor": "KTM"},
    {"rider": "Pol Espargaro", "team": "GASGAS Factory Racing Tech3", "constructor": "KTM"},
    {"rider": "Franco Morbidelli", "team": "Monster Energy Yamaha MotoGP", "constructor": "Yamaha"}
]

tracks = [
    "Qatar", "Portimao", "Austin", "Jerez", "Le Mans", "Mugello", "Assen",
    "Silverstone", "Spielberg", "Catalunya", "Misano", "Motegi", "Buriram",
    "Phillip Island", "Sepang", "Valencia", "Sachsenring", "India", "Indonesia", "Argentina"
]

sessions = ["FP1", "FP2", "FP3", "Qualifying", "Warm-Up", "Race"]
weather_options = ["Dry", "Wet", "Mixed"]
tyres = ["Soft", "Medium", "Hard"]
incidents = [None, None, None, "Crash", "Long Lap Penalty", "Mechanical Failure"]

season_data = []

def simulate_session(race, session, laps_per_rider):
    session_data = []
    weather = random.choices(weather_options, weights=[0.7, 0.15, 0.15])[0]
    for rider in riders:
        base_lap = random.uniform(95, 105)
        degradation = random.uniform(0.02, 0.1)
        for lap in range(1, laps_per_rider + 1):
            lap_time = base_lap + degradation * lap + np.random.normal(0, 0.3)
            entry = {
                "year": 2024,
                "race_id": race.replace(" ", "_"),
                "track": race,
                "session": session,
                "rider": rider["rider"],
                "team": rider["team"],
                "constructor": rider["constructor"],
                "lap": lap,
                "lap_time_sec": round(lap_time, 3),
                "position": None,
                "weather": weather,
                "tyre": random.choice(tyres),
                "pit_stop": int(random.random() < 0.02),
                "incident": random.choice(incidents),
                "avg_speed_kph": round(170 + np.random.normal(0, 5), 2),
                "sector1": round(lap_time * 0.33 + np.random.normal(0, 0.1), 3),
                "sector2": round(lap_time * 0.34 + np.random.normal(0, 0.1), 3),
                "sector3": round(lap_time * 0.33 + np.random.normal(0, 0.1), 3)
            }
            session_data.append(entry)
    return session_data

# Simulate all tracks and sessions
for track in tracks:
    for session in sessions:
        laps = 25 if session == "Race" else 5 if session == "Qualifying" else 12
        session_result = simulate_session(track, session, laps)
        season_data.extend(session_result)

df_all = pd.DataFrame(season_data)
df_all["position"] = df_all.groupby(["race_id", "session", "lap"])["lap_time_sec"].rank(method="min").astype(int)

# Save everything under ./simulated/
output_path = "simulated/"
os.makedirs(output_path + "events", exist_ok=True)

# Save all sessions
df_all.to_parquet(output_path + "all_sessions.parquet", index=False)

# Race summary
race_results = df_all[df_all["session"] == "Race"]
summary = (
    race_results
    .groupby(["race_id", "rider"])
    .agg(total_time=("lap_time_sec", "sum"))
    .reset_index()
    .sort_values(["race_id", "total_time"])
)
summary["position"] = summary.groupby("race_id")["total_time"].rank(method="min").astype(int)
summary.to_csv(output_path + "race_results.csv", index=False)

# Save per-session
for (race, session), group in df_all.groupby(["race_id", "session"]):
    fname = f"{race}__{session}.parquet"
    group.to_parquet(output_path + f"events/{fname}", index=False)

print("✅ Simulation complete. Files saved in ./simulated/")

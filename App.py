import streamlit as st
import pandas as pd
import random

# ---- Mock Data ----
mock_data = [
    {"Account": "Fort Defiance BIA", "Contact": "John Smith", "Department": "Maintenance", "State": "AZ", "Last Product Bought": "PPE", "Days Since Last Order": 42, "Tier": 1},
    {"Account": "Whiteriver IHS", "Contact": "Lisa Lopez", "Department": "Facilities", "State": "AZ", "Last Product Bought": "Lighting", "Days Since Last Order": 30, "Tier": 2},
    {"Account": "Seminole Public Works", "Contact": "Robert Davis", "Department": "Fleet", "State": "FL", "Last Product Bought": "Tools", "Days Since Last Order": 55, "Tier": 1},
    {"Account": "Crownpoint IHS", "Contact": "Ashley Brown", "Department": "Purchasing", "State": "NM", "Last Product Bought": "Safety", "Days Since Last Order": 60, "Tier": 3},
    {"Account": "Ak-Chin Public Works", "Contact": "Carlos Martinez", "Department": "Maintenance", "State": "AZ", "Last Product Bought": "PPE", "Days Since Last Order": 75, "Tier": 1},
    {"Account": "Gallup Service Center", "Contact": "Megan Johnson", "Department": "Facilities", "State": "NM", "Last Product Bought": "Lighting", "Days Since Last Order": 25, "Tier": 2},
    {"Account": "Zuni Pueblo IHS", "Contact": "Robert Lopez", "Department": "Fleet", "State": "NM", "Last Product Bought": "Tools", "Days Since Last Order": 80, "Tier": 2},
    {"Account": "Laguna Pueblo Facilities", "Contact": "Ashley Davis", "Department": "Purchasing", "State": "NM", "Last Product Bought": "Safety", "Days Since Last Order": 15, "Tier": 3},
    {"Account": "Standing Rock IHS", "Contact": "Carlos Brown", "Department": "Maintenance", "State": "SD", "Last Product Bought": "PPE", "Days Since Last Order": 90, "Tier": 1},
    {"Account": "Pine Ridge BIA", "Contact": "Megan Lopez", "Department": "Facilities", "State": "SD", "Last Product Bought": "Lighting", "Days Since Last Order": 45, "Tier": 2}
]

df = pd.DataFrame(mock_data)

# Assign weights
df["Weight"] = df.apply(
    lambda x: (4 if x["Tier"] == 1 else 2 if x["Tier"] == 2 else 1) + (1 if x["Days Since Last Order"] > 45 else 0),
    axis=1
)

# Product recommendations
recommend_map = {
    "PPE": ["Hand Tools", "Spill Kits", "Safety Signage"],
    "Lighting": ["Electrical Supplies", "Ladders", "Emergency Lighting"],
    "Tools": ["Storage Cabinets", "Fasteners", "Lubricants"],
    "Safety": ["Fall Protection", "First Aid Kits", "Work Boots"]
}

# Functions
def generate_call_block(dataframe, n=3):
    sample = dataframe.sample(n=n, weights=dataframe["Weight"], replace=False)
    calls = []
    for _, row in sample.iterrows():
        category = row["Last Product Bought"]
        suggested = random.choice(recommend_map.get(category, ["General MRO Supplies"]))
        calls.append({
            "Account": row["Account"],
            "Contact": row["Contact"],
            "Department": row["Department"],
            "State": row["State"],
            "Last Product": category,
            "Suggested Product": suggested,
            "Days Since Last Order": row["Days Since Last Order"],
            "Tier": row["Tier"]
        })
    return pd.DataFrame(calls)

def generate_talk_tracks(call_block):
    tracks = []
    for _, row in call_block.iterrows():
        opener = (
            f"Hi {row['Contact']}, this is Alex from Grainger. "
            f"I noticed you recently ordered {row['Last Product'].lower()}. "
            f"Many teams like yours also stock up on {row['Suggested Product'].lower()} around this time. "
            f"How are things looking for your crew’s upcoming projects?"
        )
        tracks.append({"Account": row["Account"], "Talk Track": opener})
    return pd.DataFrame(tracks)

# ---- Streamlit UI ----
st.set_page_config(page_title="Mock Call Block Generator", page_icon="📞", layout="wide")
st.title("📞 Mock Call Block Generator (Demo Version)")

if st.button("Generate Call Block"):
    st.session_state["call_block"] = generate_call_block(df, n=3)
    st.subheader("🎯 Call Block")
    st.write(st.session_state["call_block"])

if "call_block" in st.session_state and st.button("Generate Talk Tracks"):
    talk_tracks = generate_talk_tracks(st.session_state["call_block"])
    st.subheader("🗣️ Mock AI Talk Tracks")
    st.write(talk_tracks)

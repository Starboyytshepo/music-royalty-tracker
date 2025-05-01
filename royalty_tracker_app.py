import streamlit as st
import pandas as pd
import os

# Set page config
st.set_page_config(page_title="Music Royalty Tracker", page_icon="🎧", layout="wide")

DATA_FILE = 'earnings.csv'
COVERS_DIR = 'covers'

# Ensure covers folder exists
os.makedirs(COVERS_DIR, exist_ok=True)

# Load or create data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=['Month', 'Platform', 'Song', 'Amount'])
        df.to_csv(DATA_FILE, index=False)
        return df

def add_earning(month, platform, song, amount):
    new_data = pd.DataFrame([[month, platform, song, amount]], columns=['Month', 'Platform', 'Song', 'Amount'])
    df = load_data()
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# --- UI ---
st.title("🎵 Music Royalty Tracker")
st.markdown("Track your royalties. Add song covers. Export data. Simple and powerful.")
st.markdown("---")

# Entry form
with st.form("Add Earning"):
    st.subheader("➕ Add New Earning")
    month = st.selectbox("Month", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    platform = st.text_input("Streaming Platform")
    song = st.text_input("Song Title")
    amount = st.number_input("Amount Earned ($)", min_value=0.0, format="%.2f")
    cover = st.file_uploader("Upload Song Cover (Optional)", type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        add_earning(month, platform, song, amount)
        st.success("✅ Earning added!")
        if cover:
            cover_path = os.path.join(COVERS_DIR, f"{song}.jpg")
            with open(cover_path, "wb") as f:
                f.write(cover.read())

# Clear data button
with st.expander("⚠️ Clear All Data (for testing only)"):
    if st.button("Delete all earnings"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.warning("All earnings deleted! Refresh the app.")

# Load and show data
df = load_data()
st.markdown("---")

if not df.empty:
    # Stats
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 Total Earnings")
        st.metric("Total", f"${df['Amount'].sum():.2f}")

    with col2:
        st.subheader("🎶 Top Songs")
        top_songs = df.groupby('Song')['Amount'].sum().sort_values(ascending=False)
        st.bar_chart(top_songs)

    # Trends
    st.subheader("📈 Monthly Trends")
    monthly = df.groupby('Month')['Amount'].sum().reindex(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    st.line_chart(monthly.fillna(0))

    # Covers
    st.subheader("🖼️ Song Covers")
    for song in df['Song'].unique():
        cover_path = os.path.join(COVERS_DIR, f"{song}.jpg")
        if os.path.exists(cover_path):
            st.image(cover_path, width=150, caption=song)

    # Editable Table
    st.subheader("✏️ Manage Entries")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    if st.button("📂 Save Changes"):
        edited_df.to_csv(DATA_FILE, index=False)
        st.success("Changes saved!")

    # Export Button
    st.download_button(
        label="📄 Export as CSV",
        data=edited_df.to_csv(index=False),
        file_name="royalty_data.csv",
        mime="text/csv"
    )

    # Auto Insights
    st.subheader("🤖 Quick Insights")
    most_profitable_song = df.groupby('Song')['Amount'].sum().idxmax()
    highest_platform = df.groupby('Platform')['Amount'].sum().idxmax()
    best_month = df.groupby('Month')['Amount'].sum().idxmax()

    st.markdown(f"- 🎵 **Top-Earning Song**: `{most_profitable_song}`")
    st.markdown(f"- 💸 **Most Profitable Platform**: `{highest_platform}`")
    st.markdown(f"- 🌟 **Best Month**: `{best_month}`")

else:
    st.info("No earnings data yet. Add some to get started!")

# Footer
st.markdown("---")
st.caption("Built with ❤️ by Starboyytshepo — v1.0")

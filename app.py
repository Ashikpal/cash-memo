import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Cash Memo", page_icon="💰")

# 2. Define Denominations
denominations = [1000, 500, 200, 100, 50, 20, 10, 5, 2, 1]

# --- RESET FUNCTION ---
def reset_all():
    for note in denominations:
        st.session_state[f"note_{note}"] = 0

# --- PRE-CALCULATION ---
# We calculate the total first using saved data so we can display it at the top
current_total = 0
for note in denominations:
    key = f"note_{note}"
    # If the app knows this number, add it to the total
    if key in st.session_state:
        current_total += note * st.session_state[key]

# 3. Top Layout: Title, Reset, and Grand Total
col_header, col_reset = st.columns([3, 1])

with col_header:
    st.title("💰 Cash Memo")

with col_reset:
    st.button("🔄 Reset All", on_click=reset_all, type="primary")

# *** GRAND TOTAL DISPLAY AT THE TOP ***
st.metric(label="GRAND TOTAL", value=f"{current_total:,}")

st.markdown("---")

# 4. Input Table Headers
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.markdown("**NOTE**")
with col2:
    st.markdown("**COUNT**")
with col3:
    st.markdown("**TOTAL**")

# 5. Input Rows Loop
ledger_data = []

for note in denominations:
    with st.container():
        c1, c2, c3 = st.columns([1, 1, 1])
        
        with c1:
            st.info(f"{note}")
        
        with c2:
            # Create the key name (e.g., "note_1000")
            key_name = f"note_{note}"
            
            # Ensure the key exists in memory
            if key_name not in st.session_state:
                st.session_state[key_name] = 0
                
            # The input box
            count = st.number_input(
                f"Count for {note}", 
                min_value=0, 
                step=1, 
                key=key_name, 
                label_visibility="collapsed"
            )
        
        with c3:
            total = note * count
            st.success(f"{total:,}")
            
            if count > 0:
                ledger_data.append({"Note": note, "Count": count, "Total": total})

# Optional: Summary Table at the bottom
if current_total > 0:
    st.markdown("---")
    st.write("### Summary Ticket")
    df = pd.DataFrame(ledger_data)
    st.dataframe(df, hide_index=True, use_container_width=True)

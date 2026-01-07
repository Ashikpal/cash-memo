import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Cash Memo", page_icon="💰")

# 2. Define Denominations
denominations = [1000, 500, 200, 100, 50, 20, 10, 5, 2, 1]

# --- RESET FUNCTION ---
# This function sets all the input keys back to 0
def reset_all():
    for note in denominations:
        # The key for each input is formatted as "note_1000", "note_500", etc.
        st.session_state[f"note_{note}"] = 0

# 3. Title and Reset Button Layout
col_header, col_reset = st.columns([3, 1])

with col_header:
    st.title("💰 Cash Memo")

with col_reset:
    # This button triggers the reset_all function when clicked
    st.button("🔄 Reset All", on_click=reset_all, type="primary")

st.markdown("Enter the count for each note below. Calculations update automatically.")
st.markdown("---")

# 4. Create Input Columns (Header)
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.markdown("**NOTE**")
with col2:
    st.markdown("**COUNT**")
with col3:
    st.markdown("**TOTAL**")

grand_total = 0
ledger_data = []

# 5. Loop through notes to create rows
for note in denominations:
    with st.container():
        c1, c2, c3 = st.columns([1, 1, 1])
        
        with c1:
            st.info(f"{note}")
        
        with c2:
            # IMPORTANT: We verify the key exists in session_state, if not set to 0
            key_name = f"note_{note}"
            if key_name not in st.session_state:
                st.session_state[key_name] = 0
                
            # The number_input is linked to st.session_state via the 'key' argument
            count = st.number_input(
                f"Count for {note}", 
                min_value=0, 
                step=1, 
                key=key_name, 
                label_visibility="collapsed"
            )
        
        with c3:
            total = note * count
            grand_total += total
            st.success(f"{total:,}")
            
            if count > 0:
                ledger_data.append({"Note": note, "Count": count, "Total": total})

st.markdown("---")

# 6. Grand Total Display
st.metric(label="GRAND TOTAL", value=f"{grand_total:,}")

# Summary Ticket
if grand_total > 0:
    st.write("### Summary Ticket")
    df = pd.DataFrame(ledger_data)
    st.dataframe(df, hide_index=True, use_container_width=True)

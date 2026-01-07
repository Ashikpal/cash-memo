import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Cash Memo", page_icon="💰")

# 2. Title and styling
st.title("💰 Cash Memo Calculator")
st.markdown("Enter the count for each note below. Calculations update automatically.")

# 3. Define Denominations
denominations = [1000, 500, 200, 100, 50, 20, 10, 5, 2, 1]

# 4. Create Input Columns
# We use a dictionary to store the user's inputs
counts = {}

# Use Streamlit columns to make it look like a table
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("**NOTE**")
with col2:
    st.markdown("**COUNT**")
with col3:
    st.markdown("**TOTAL**")

grand_total = 0
ledger_data = []

# Loop through each note to create input rows
for note in denominations:
    with st.container():
        c1, c2, c3 = st.columns([1, 1, 1])
        
        with c1:
            # Display the Note value
            st.info(f"{note}")
        
        with c2:
            # Input field for Count
            # defaults to 0, min value 0
            count = st.number_input(f"Count for {note}", min_value=0, step=1, key=f"note_{note}", label_visibility="collapsed")
        
        with c3:
            # Calculate and display total
            total = note * count
            grand_total += total
            st.success(f"{total:,}") # Display with comma separator
            
            if count > 0:
                ledger_data.append({"Note": note, "Count": count, "Total": total})

st.markdown("---")

# 5. Grand Total Display
st.metric(label="GRAND TOTAL", value=f"{grand_total:,}")

# Optional: Show a clean table summary at the bottom if data exists
if grand_total > 0:
    st.write("### Summary Ticket")
    df = pd.DataFrame(ledger_data)
    st.dataframe(df, hide_index=True, use_container_width=True)

import streamlit as st
import pandas as pd
import io

st.image("/Users/kubratoka/Desktop/MeasureUp App/logo.jpg", width=300)  # path to your logo file


st.set_page_config(page_title="MeasureUp Estimator App", layout="centered")
st.title("MeasureUp Estimator App")

# Step 0: User input for stakeholders, activity, outcomes
st.markdown("<h3 style='color: green;'>Step 1: Determine the Stakeholders, and Describe Activity and Outcomes</h3>", unsafe_allow_html=True)

stakeholders = st.text_area("Stakeholders (Who do you have an effect on? Describe your stakeholder.)")
activity = st.text_area("Activity (Description of your activity)")
outcomes = st.text_area("Outcomes (What is the change experienced by stakeholders?)")

# Load Excel file safely
file_path = "/Users/kubratoka/Desktop/MeasureUp App/value_list.xlsx"
try:
    df = pd.read_excel(file_path)
except Exception as e:
    st.error(f"Error loading Excel file: {e}")
    st.stop()

st.markdown("<h3 style='color: orange;'>Step 2: Match the activities or outcomes with MeasureUp values</h3>", unsafe_allow_html=True)

# Step 1: Dropdown for Value Name
categories = sorted(df["Value name"].dropna().unique())
selected_category = st.selectbox("Select MeasureUp Value Name:", categories)

# Step 2: Dropdown for Level
level_options = ["Silver", "Bronze"]
selected_level = st.selectbox("Select Level:", level_options)

# Step 3: Handle display based on level
if selected_level == "Silver":
    silver_rows = df[df["Value name"] == selected_category]
    
    # Silver Adjustment Factors
    if "Silver adjustment factors" in silver_rows.columns:
        silver_factors = silver_rows["Silver adjustment factors"].dropna().unique()
        factors_text = ", ".join(map(str, silver_factors)) if len(silver_factors) > 0 else "None"
        st.write(f"Silver Adjustment Factors: {factors_text}")
    
    # Filter Silver options (exclude 'NA')
    silver_options = silver_rows["Silver name"].dropna().unique()
    silver_options = [s for s in silver_options if s != "NA"]

    if len(silver_options) > 0:
        selected_silver = st.selectbox("Select Silver Differentiation:", silver_options)
        row_data = df[(df["Value name"] == selected_category) & (df["Silver name"] == selected_silver)]
    else:
        st.info("No Silver levels available. Showing Description and Bronze value by default.")
        row_data = df[df["Value name"] == selected_category]

    available_cols = [col for col in df.columns if col.strip().lower() in 
                      ["description", "unit 1", "unit 2", "silver values", "fiscal", "economic", "social", "environmental"]]
else:  # Bronze level
    st.info("Showing Bronze level information.")
    row_data = df[(df["Value name"] == selected_category) & (df["Level"].str.strip().str.lower() == "bronze")]
    available_cols = [col for col in df.columns if col.strip().lower() in 
                      ["description", "unit 1", "unit 2", "bronze value", "fiscal", "economic", "social", "environmental"]]

# Step 4: Display the data
st.markdown("<p style='font-size:18px; font-weight:bold; color:orange;'>MeasureUp Value Information:</p>", unsafe_allow_html=True)

if not row_data.empty:
    for col in available_cols:
        if col in row_data.columns and pd.notna(row_data[col].iloc[0]):
            st.markdown(f"- **{col}:** {row_data[col].iloc[0]}")
else:
    st.warning("No MeasureUp row selected.")

# Step 5: Log Quantity and Duration
st.markdown("<h3 style='color: teal;'>Step 3: Record the details of your activity/outcome and the MeasureUp value</h3>", unsafe_allow_html=True)
indicator_spurce = st.text_area("Indicator and source",
                               help="Describe how you will measure the described outcome or  activity (including any sources used).")

if not row_data.empty:
    col1, col2 = st.columns(2)

    with col1:
        unit1_label = f"Unit 1 ({row_data['Unit 1'].iloc[0]})" if 'Unit 1' in row_data else "Unit 1"
        unit1 = st.number_input(unit1_label, min_value=0, step=1,
                                help="Enter the first key unit of measurement (i.e. Unit 1 in the MeasureUp Information Table above)")

    unit2_value = row_data['Unit 2'].iloc[0] if 'Unit 2' in row_data else None
    if pd.notna(unit2_value):
        with col2:
            unit2_label = f"Unit 2 ({unit2_value})"
            unit2 = st.number_input(unit2_label, min_value=0.0, step=0.5,
                                    help="If the duration of your activity is less than a year, convert it to a fraction of a year (e.g. 3 months = 0.25).")
    else:
        unit2 = 1
else:
    st.warning("No MeasureUp row selected. Cannot display Unit 1 or Unit 2 inputs.")
    unit1 = 0
    unit2 = 1

# Step 6: Impact Discount
st.markdown("<p style='font-size:18px; font-weight:bold; color:teal;'>Impact Discount</p>", unsafe_allow_html=True)

impact_evidence = st.text_area("Impact Discount Evidence Explanation",
                               help="Describe the evidence and source for why the impact discount is applied.")

impact_level = st.selectbox("Estimate of what would have happened anyway (defines amount of discount to your value):",
                            ["Low", "Medium", "High"])
impact_discount_mapping = {"Low": 0.25, "Medium": 0.5, "High": 0.75}
impact_discount_percentage = impact_discount_mapping.get(impact_level, 0)
st.write(f"**Impact Discount (decimal):** {impact_discount_percentage}")

# Step 7: Monetised Value Calculation


st.markdown("<h3 style='color: purple;'>Step 4: Calculate the monetised value of your impact</h3>", unsafe_allow_html=True)
value_columns = [col for col in available_cols if "value" in col.lower()]
base_value_per_unit = row_data[value_columns[0]].iloc[0] if value_columns else 0
if base_value_per_unit == 0:
    st.warning("No monetary value column found in the selected row. Using 0 as default.")

monetised_value_per_unit = base_value_per_unit * (1 - impact_discount_percentage)
total_monetised_value = monetised_value_per_unit * unit1 * (unit2 if pd.notna(unit2_value) else 1)

st.write(f"**Base value per unit in £:** {base_value_per_unit}")
st.write(f"**Impact discount applied:** {impact_discount_percentage}")
st.write(f"**Monetised value per unit (discount applied) in £:** {monetised_value_per_unit:.2f}")
st.write(f"**Total monetised value (discount applied and multiplied with unit 1 and unit 2) in £:** {total_monetised_value:.2f}")


# Step 8: Type of Monetised Value
value_type = st.selectbox("Select Type of Monetised Value:",
                          ["Economic", "Fiscal", "Wellbeing", "Environmental"])
value_type_column_mapping = {"Economic": "Economic", "Fiscal": "Fiscal", "Wellbeing": "Social", "Environmental": "Environmental"}
selected_value_column = value_type_column_mapping.get(value_type, None)

if selected_value_column and selected_value_column in row_data.columns:
    base_value_type = row_data[selected_value_column].iloc[0]
else:
    base_value_type = 0
    st.warning(f"No value found for {value_type}. Using 0 as default.")

total_value_by_type = base_value_type * unit1 * unit2 * (1 - impact_discount_percentage)
st.write(f"**Base value for {value_type} in £:** {base_value_type}")
st.write(f"**Total Monetised Value ({value_type}) after discount and multiplied with unit 1 and unit 2 in £:** {total_value_by_type:.2f}")

# Step 9: Generate Report

st.markdown("<h3 style='color: orchid;'> Final: Generate Report</h3>", unsafe_allow_html=True)
report_data = {
    "Stakeholders": stakeholders,
    "Activity": activity,
    "Outcomes": outcomes,
    "Selected Value Name": selected_category,

}
if selected_level == "Silver" and 'selected_silver' in locals():
    report_data["Silver Level"] = selected_silver

if not row_data.empty:
    report_data["Description"] = row_data['Description'].iloc[0] if 'Description' in row_data else ""
    report_data[f"Unit 1 ({row_data['Unit 1'].iloc[0]})"] = unit1
    if pd.notna(unit2_value):
        report_data[f"Unit 2 ({unit2_value})"] = unit2
# Add impact discount and monetised values
report_data["Impact Discount Level"] = impact_level
report_data["Impact Discount (decimal)"] = impact_discount_percentage
report_data["Total Monetised Value"] = total_monetised_value
report_data["Type of Monetised Value"] = value_type
report_data[f"Total Monetised Value ({value_type})"] = total_value_by_type



# Convert to DataFrame and CSV
report_df = pd.DataFrame(report_data.items(), columns=["Item", "Value"])
csv_buffer = io.StringIO()
report_df.to_csv(csv_buffer, index=False)
csv_data = csv_buffer.getvalue()

st.download_button(
    label="Download Report as CSV",
    data=csv_data,
    file_name="measureup_report.csv",
    mime="text/csv"
)

st.markdown("<p style='font-size:18px; font-weight:bold; color:orchid;'>Report Preview</p>", unsafe_allow_html=True)

st.table(report_df)

import streamlit as st
import pandas as pd
import io
import os

# Page configuration
st.set_page_config(page_title="MeasureUp Estimator App", layout="centered")

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

# Initialize session state variables for data persistence
if 'stakeholders' not in st.session_state:
    st.session_state.stakeholders = ""
if 'activity' not in st.session_state:
    st.session_state.activity = ""
if 'outcomes' not in st.session_state:
    st.session_state.outcomes = ""
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'selected_level' not in st.session_state:
    st.session_state.selected_level = "Bronze"
if 'selected_silver' not in st.session_state:
    st.session_state.selected_silver = None
if 'unit1' not in st.session_state:
    st.session_state.unit1 = 0
if 'unit2' not in st.session_state:
    st.session_state.unit2 = 1
if 'indicator_source' not in st.session_state:
    st.session_state.indicator_source = ""
if 'impact_level' not in st.session_state:
    st.session_state.impact_level = "Low"
if 'impact_evidence' not in st.session_state:
    st.session_state.impact_evidence = ""
if 'value_type' not in st.session_state:
    st.session_state.value_type = "Economic"
if 'row_data' not in st.session_state:
    st.session_state.row_data = pd.DataFrame()
# Add new session state variables for calculated values
if 'base_value_per_unit' not in st.session_state:
    st.session_state.base_value_per_unit = 0
if 'impact_discount_percentage' not in st.session_state:
    st.session_state.impact_discount_percentage = 0
if 'monetised_value_per_unit' not in st.session_state:
    st.session_state.monetised_value_per_unit = 0
if 'total_monetised_value' not in st.session_state:
    st.session_state.total_monetised_value = 0
if 'base_value_type' not in st.session_state:
    st.session_state.base_value_type = 0
if 'total_value_by_type' not in st.session_state:
    st.session_state.total_value_by_type = 0
if 'unit2_value' not in st.session_state:
    st.session_state.unit2_value = None

# Get folder where this script lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Paths relative to the repo
logo_path = os.path.join(BASE_DIR, "logo.jpg")
excel_path = os.path.join(BASE_DIR, "value_list.xlsx")

st.image(logo_path, width=300)
st.title("MeasureUp Estimator App")

try:
    df = pd.read_excel(excel_path)
except Exception as e:
    st.error(f"Error loading Excel file: {e}")
    st.stop()


# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1  # 1 = Start page


# Navigation function MUST be defined before it's used
def go_to_page(page_num):
    st.session_state.current_page = page_num
    st.rerun()

# ============== PAGE 1: Start / Guidance ==============
if st.session_state.current_page == 1:
    st.markdown("<h2 style='color:#4b0082;'>Welcome to the MeasureUp Estimator App</h2>", unsafe_allow_html=True)

    st.markdown("""
    This app helps you estimate the monetised and non-monetised value of your activities using MeasureUp values.
    """)
    
    st.markdown("### Key steps:")
    st.markdown("""
<p style='font-size:20px; font-weight:bold; color:green;'>
Step 1: Define who and what
</p>
                
- Stakeholders: Describe the people, groups, or organisations affected by your activity (or influencing it), and give any relevant details about them.
                
- Activities: Briefly describe the activity or intervention you want to value.
                
- Outcomes: Describe the key changes your stakeholders experience (e.g. changes in wellbeing, income, carbon emissions).
                
<p style='font-size:20px; font-weight:bold; color:orange;'>
Step 2: Match with MeasureUp values
</p>
                
- Choose the MeasureUp value that best matches either your activity or your main outcome.
                
- If you are unsure, you can review the full list of values on the [MeasureUp values page](https://measure-up.org/values/).
    
<p style='font-size:20px; font-weight:bold; color:teal;'>
Step 3: Record activity details
</p>
           
- Indicator and source: Explain how you will measure the activity or outcome and where the data comes from.
           
- Quantity: Enter how many people are affected, or how many units are delivered.
           
- Duration: Enter how long the activity or outcome lasts (in years or fractions of a year).
           
- Unit of value: Check whether the value is per person per year, or uses another unit (such as “per hazard repaired”).   
    
 <p style='font-size:20px; font-weight:bold; color:purple;'>
Step 4: Calculate the monetised value
</p>
                
Think about attribution and deadweight: how much of the change is really due to your activity, and how much would have happened anyway or because of someone else.
           
Choose an impact discount level:
               
- Low (25%) if most of the change is due to your activity.
               
- Medium (50%) if about half is due to your activity.
               
- High (75%) if only a small share is due to your activity.

<p style='font-size:20px; font-weight:bold; color:orchid;'>
Final Step: Review and download your results.
</p>

    """,
       unsafe_allow_html=True,)

    st.markdown("### Tips")
    st.markdown("""
    - Save or download your report after each run if you are testing multiple activities.
    - Use clear, specific descriptions for stakeholders and outcomes.
    - If you are unsure which level to pick, start with Bronze.
    """)
    st.markdown(
    "<p style='font-size:18px; font-weight:bold; color:#008080;'>"
    "Ready to begin the MeasureUp estimation? Click Start to go to Step 1."
    "</p>",
    unsafe_allow_html=True,)

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Start", type="primary", use_container_width=True):
            go_to_page(2)

# ============== PAGE 2: Stakeholders, Activity, Outcomes ==============
if st.session_state.current_page == 2:
    st.markdown("<h3 style='color: green;'>Step 1: Determine the Stakeholders, and Describe Activity and Outcomes</h3>", unsafe_allow_html=True)
    
    st.session_state.stakeholders = st.text_area(
        "Stakeholders (Who do you have an effect on? Describe your stakeholder.)",
        value=st.session_state.stakeholders,
        key="stakeholders_input"
    )
    
    st.session_state.activity = st.text_area(
        "Activity (Description of your activity)",
        value=st.session_state.activity,
        key="activity_input"
    )
    
    st.session_state.outcomes = st.text_area(
        "Outcomes (What is the change experienced by stakeholders?)",
        value=st.session_state.outcomes,
        key="outcomes_input"
    )
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Previous", use_container_width=True):
            go_to_page(1)
    with col3:
        if st.button("Next →", type="primary", use_container_width=True):
            go_to_page(3)

# ============== PAGE 3: Match with MeasureUp Value ==============
elif st.session_state.current_page == 3:
    st.markdown("<h3 style='color: orange;'>Step 2: Match the activities or outcomes with MeasureUp values</h3>", unsafe_allow_html=True)
    
    # Dropdown for Value Name
    categories = sorted(df["Value name"].dropna().unique())
    if st.session_state.selected_category not in categories and len(categories) > 0:
        st.session_state.selected_category = categories[0]
    
    st.session_state.selected_category = st.selectbox(
        "Select MeasureUp Value Name:",
        categories,
        index=categories.index(st.session_state.selected_category) if st.session_state.selected_category in categories else 0,
        key="category_select"
    )
    
    # Dropdown for Level
    level_options = ["Bronze", "Silver"]
    st.session_state.selected_level = st.selectbox(
        "Select Level:",
        level_options,
        index=level_options.index(st.session_state.selected_level),
        key="level_select"
    )
    
    # Handle display based on level
    if st.session_state.selected_level == "Silver":
        silver_rows = df[df["Value name"] == st.session_state.selected_category]
        
        if "Silver adjustment factors" in silver_rows.columns:
            silver_factors = silver_rows["Silver adjustment factors"].dropna().unique()
            factors_text = ", ".join(map(str, silver_factors)) if len(silver_factors) > 0 else "None"
            st.write(f"**Silver Adjustment Factors:** {factors_text}")
        
        silver_options = silver_rows["Silver name"].dropna().unique()
        silver_options = [s for s in silver_options if s != "NA"]
        
        if len(silver_options) > 0:
            if st.session_state.selected_silver not in silver_options:
                st.session_state.selected_silver = silver_options[0]
            
            st.session_state.selected_silver = st.selectbox(
                "Select Silver Differentiation:",
                silver_options,
                index=list(silver_options).index(st.session_state.selected_silver) if st.session_state.selected_silver in silver_options else 0,
                key="silver_select"
            )
            st.session_state.row_data = df[(df["Value name"] == st.session_state.selected_category) & 
                                          (df["Silver name"] == st.session_state.selected_silver)]
        else:
            st.info("No Silver levels available. Showing Description and Bronze value by default.")
            st.session_state.row_data = df[df["Value name"] == st.session_state.selected_category]
        
        available_cols = [col for col in df.columns if col.strip().lower() in 
                         ["key","description", "unit 1", "unit 2", "silver values", "fiscal", "economic", "social", "environmental"]]
    else:  # Bronze level
        st.session_state.row_data = df[(df["Value name"] == st.session_state.selected_category) & 
                                       (df["Level"].str.strip().str.lower() == "bronze")]
        available_cols = [col for col in df.columns if col.strip().lower() in 
                         ["key","description", "unit 1", "unit 2", "bronze value", "fiscal", "economic", "social", "environmental","URL"]]
    
    # Display the data
    with st.expander("MeasureUp Value Information", expanded=True):
        if not st.session_state.row_data.empty:
            box_html = """
            <div style="
                background-color:#fffaf0;
                padding:15px;
                border-radius:10px;
                border:1px solid #ffcc80;
                box-shadow:0 2px 8px rgba(255,140,0,0.15);
                margin-top:10px;
            ">
            """
            
            for col in available_cols:
                if col in st.session_state.row_data.columns and pd.notna(st.session_state.row_data[col].iloc[0]):
                    box_html += f"<div style='margin:6px 0;'><b style='color:#ff8c00;'>{col}:</b> {st.session_state.row_data[col].iloc[0]}</div>"
             # Add URL link if it exists
            if 'URL' in st.session_state.row_data.columns and pd.notna(st.session_state.row_data['URL'].iloc[0]):
                url = st.session_state.row_data['URL'].iloc[0]
                box_html += f"""<div style='margin:10px 0 0 0;'>
                 <b style='color:#ff8c00;'>More information:</b> 
                    <a href="{url}" target="_blank" 
                    style="color:#0066cc; text-decoration:underline;">Click here</a></div>"""
             
            # Close the box
            box_html += "</div>"
            st.markdown(box_html, unsafe_allow_html=True)
        else:
            st.warning("No MeasureUp row selected.")
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Previous", use_container_width=True):
            go_to_page(2)
    with col3:
        if st.button("Next →", type="primary", use_container_width=True):
            go_to_page(4)

# ============== PAGE 4: Record Activity Details ==============
elif st.session_state.current_page == 4:
    st.markdown("<h3 style='color: teal;'>Step 3: Record the details of your activity/outcome and the MeasureUp value</h3>", unsafe_allow_html=True)
    
    st.session_state.indicator_source = st.text_area(
        "Indicator and source",
        value=st.session_state.indicator_source,
        help="Describe how you will measure the described outcome or activity (including any sources used).",
        key="indicator_input"
    )
    
    if not st.session_state.row_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            unit1_label = f"Unit 1 ({st.session_state.row_data['Unit 1'].iloc[0]})" if 'Unit 1' in st.session_state.row_data else "Unit 1"
            st.session_state.unit1 = st.number_input(
                unit1_label,
                min_value=0,
                step=1,
                value=st.session_state.unit1,
                help="Enter the first key unit of measurement (i.e. Unit 1 in the MeasureUp Information Table above)",
                key="unit1_input"
            )
        
        st.session_state.unit2_value = st.session_state.row_data['Unit 2'].iloc[0] if 'Unit 2' in st.session_state.row_data else None
        if pd.notna(st.session_state.unit2_value):
            with col2:
                unit2_label = f"Unit 2 ({st.session_state.unit2_value})"
                st.session_state.unit2 = st.number_input(
                    unit2_label,
                    min_value=0.0,
                    step=0.5,
                    value=float(st.session_state.unit2),
                    help="If the duration of your activity is less than a year, convert it to a fraction of a year (e.g. 3 months = 0.25).",
                    key="unit2_input"
                )
        else:
            st.session_state.unit2 = 1
    else:
        st.warning("No MeasureUp row selected. Please go back to Step 2.")
    
    # Impact Discount
    st.markdown("<p style='font-size:18px; font-weight:bold; color:teal;'>Impact Discount</p>", unsafe_allow_html=True)
    
    st.session_state.impact_evidence = st.text_area(
        "Impact Discount Evidence Explanation",
        value=st.session_state.impact_evidence,
        help="Describe the evidence and source for why the impact discount is applied.",
        key="impact_evidence_input"
    )
    
    st.session_state.impact_level = st.selectbox(
        "Estimate of what would have happened anyway (defines amount of discount to your value):",
        ["No discount","Low", "Medium", "High"],
        index=["No discount","Low", "Medium", "High"].index(st.session_state.impact_level),
        key="impact_level_select"
    )
    
    impact_discount_mapping = {"No discount": 0, "Low": 0.25, "Medium": 0.5, "High": 0.75}
    st.session_state.impact_discount_percentage = impact_discount_mapping.get(st.session_state.impact_level, 0)
    st.write(f"**Impact Discount (decimal):** {st.session_state.impact_discount_percentage}")
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Previous", use_container_width=True):
            go_to_page(3)
    with col3:
        if st.button("Next →", type="primary", use_container_width=True):
            go_to_page(5)

# ============== PAGE 5: Calculate Monetised Value ==============
elif st.session_state.current_page == 5:
    st.markdown("<h3 style='color: purple;'>Step 4: Calculate the monetised value of your impact</h3>", unsafe_allow_html=True)
    
    if not st.session_state.row_data.empty:
        # Get available columns based on level
        if st.session_state.selected_level == "Silver":
            available_cols = [col for col in df.columns if col.strip().lower() in 
                             ["description", "unit 1", "unit 2", "silver values", "fiscal", "economic", "social", "environmental"]]
        else:
            available_cols = [col for col in df.columns if col.strip().lower() in 
                             ["description", "unit 1", "unit 2", "bronze value", "fiscal", "economic", "social", "environmental"]]
        
        value_columns = [col for col in available_cols if "value" in col.lower()]
        st.session_state.base_value_per_unit = st.session_state.row_data[value_columns[0]].iloc[0] if value_columns else 0
        
        if st.session_state.base_value_per_unit == 0:
            st.warning("No monetary value column found in the selected row. Using 0 as default.")
        
        st.session_state.monetised_value_per_unit = st.session_state.base_value_per_unit * (1 - st.session_state.impact_discount_percentage)
        st.session_state.total_monetised_value = st.session_state.monetised_value_per_unit * st.session_state.unit1 * (st.session_state.unit2 if pd.notna(st.session_state.unit2_value) else 1)
        
        st.write(f"**Base value per unit in £:** {st.session_state.base_value_per_unit}")
        st.write(f"**Impact discount applied:** {st.session_state.impact_discount_percentage}")
        st.write(f"**Monetised value per unit (discount applied) in £:** {st.session_state.monetised_value_per_unit:.2f}")
        st.write(f"**Total monetised value (discount applied and multiplied with unit 1 and unit 2) in £:** {st.session_state.total_monetised_value:.2f}")
        
        st.markdown("---")
        if 'kg_co2_value' not in st.session_state:
         st.session_state.kg_co2_value = 0
        if 'wellby_value' not in st.session_state:
         st.session_state.wellby_value = 0
        # Type of Monetised Value
        st.session_state.value_type = st.selectbox(
            "Select Type of Monetised Value:",
            ["Economic", "Fiscal", "Wellbeing", "Environmental"],
            index=["Economic", "Fiscal", "Wellbeing", "Environmental"].index(st.session_state.value_type),
            key="value_type_select"
        )
        
        value_type_column_mapping = {"Economic": "Economic", "Fiscal": "Fiscal", "Wellbeing": "Social", "Environmental": "Environmental"}
        selected_value_column = value_type_column_mapping.get(st.session_state.value_type, None)
        
        if selected_value_column and selected_value_column in st.session_state.row_data.columns:
            st.session_state.base_value_type = st.session_state.row_data[selected_value_column].iloc[0]
        else:
            st.session_state.base_value_type = 0
            st.warning(f"No value found for {st.session_state.value_type}. Using 0 as default.")
        
        st.session_state.total_value_by_type = st.session_state.base_value_type * st.session_state.unit1 * st.session_state.unit2 * (1 - st.session_state.impact_discount_percentage)
        st.write(f"**Base value for {st.session_state.value_type} in £:** {st.session_state.base_value_type}")
        st.write(f"**Total Monetised Value ({st.session_state.value_type}) after discount and multiplied with unit 1 and unit 2 in £:** {st.session_state.total_value_by_type:.2f}")
        
    else:
        st.error("No data available. Please complete Steps 2 and 3.")
    
    st.markdown("---")
    # If Environmental: Calculate kg CO2
    if st.session_state.value_type == "Environmental":
        st.markdown("<p style='font-size:16px; font-weight:bold; color:green;'>Carbon Emissions</p>", unsafe_allow_html=True)
    
        if 'kg CO2e' in st.session_state.row_data.columns and pd.notna(st.session_state.row_data['kg CO2e'].iloc[0]):
            kg_co2_per_unit = st.session_state.row_data['kg CO2e'].iloc[0]
            st.session_state.kg_co2_value = kg_co2_per_unit * st.session_state.unit1 * st.session_state.unit2 * (1 - st.session_state.impact_discount_percentage)
        
            st.write(f"**kg CO2 per unit:** {kg_co2_per_unit}")
            st.write(f"**Total kg CO2 (kg CO2 x unit 1 x unit 2) after discount:** {st.session_state.kg_co2_value:.2f}")
            st.write(f"**Total tonnes CO2:** {st.session_state.kg_co2_value / 1000:.2f}")
        else:
            st.session_state.kg_co2_value = 0
            st.info("No kg CO2 data available in the selected row.")
    # If Wellbeing: Calculate WELLBY
    elif st.session_state.value_type == "Wellbeing":
        st.markdown("<p style='font-size:16px; font-weight:bold; color:purple;'>WELLBY Value</p>", unsafe_allow_html=True)

        has_col = 'WELLBY' in st.session_state.row_data.columns
        val = st.session_state.row_data['WELLBY'].iloc[0] if has_col else None

        if has_col and pd.notna(val) and val != 0:
            wellby_per_unit = val
            st.session_state.wellby_value = wellby_per_unit * st.session_state.unit1 * st.session_state.unit2 * (1 - st.session_state.impact_discount_percentage)
            st.write(f"**WELLBY per unit:** {wellby_per_unit}")
            st.write(f"**Total WELLBYs (WELLBY per unit × Unit 1 × Unit 2) after discount:** {st.session_state.wellby_value:.2f}")
            st.info("One WELLBY represents a one-point increase in life satisfaction (0–10 scale) for one person for one year.")
        else:
            st.info("No wellbeing data available for this value or this wellbeing value is not calculated using the WELLBY methodology.")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Previous", use_container_width=True):
            go_to_page(4)
    with col3:
        if st.button("Next →", type="primary", use_container_width=True):
            go_to_page(6)

# ============== PAGE 6: Generate Report ==============
elif st.session_state.current_page == 6:
    st.markdown("<h3 style='color: orchid;'>Final: Generate Report</h3>", unsafe_allow_html=True)
    
    if not st.session_state.row_data.empty:
        report_data = {
            "Stakeholders": st.session_state.stakeholders,
            "Activity": st.session_state.activity,
            "Outcomes": st.session_state.outcomes,
            "Selected Value Name": st.session_state.selected_category,
        }
        
        if st.session_state.selected_level == "Silver" and st.session_state.selected_silver:
            report_data["Silver Level"] = st.session_state.selected_silver
        
        report_data["Key"] = st.session_state.row_data['Key'].iloc[0] if 'Key' in st.session_state.row_data else ""

        report_data["Description"] = st.session_state.row_data['Description'].iloc[0] if 'Description' in st.session_state.row_data else ""
        report_data[f"Unit 1 ({st.session_state.row_data['Unit 1'].iloc[0]})"] = st.session_state.unit1
        if pd.notna(st.session_state.unit2_value):
            report_data[f"Unit 2 ({st.session_state.unit2_value})"] = st.session_state.unit2
        
        report_data["Indicator and Source"] = st.session_state.indicator_source
        report_data["Impact Evidence"] = st.session_state.impact_evidence
        report_data["Impact Discount Level"] = st.session_state.impact_level
        report_data["Impact Discount (decimal)"] = st.session_state.impact_discount_percentage
        report_data["Base Value Per Unit (£)"] = st.session_state.base_value_per_unit
        report_data["Monetised Value Per Unit (£)"] = st.session_state.monetised_value_per_unit
        report_data["Total Monetised Value (£)"] = st.session_state.total_monetised_value
        report_data["Type of Monetised Value"] = st.session_state.value_type
        report_data[f"Total Monetised Value ({st.session_state.value_type}) (£)"] = st.session_state.total_value_by_type
        # Add Environmental metrics if applicable
        if st.session_state.value_type == "Environmental" and st.session_state.kg_co2_value > 0:
            report_data["Total kg CO2"] = st.session_state.kg_co2_value
            report_data["Total tonnes CO2"] = st.session_state.kg_co2_value / 1000

        # Add Wellbeing metrics if applicable
        if st.session_state.value_type == "Wellbeing" and st.session_state.wellby_value > 0:
            report_data["Total WELLBYs"] = st.session_state.wellby_value
        # Convert to DataFrame and CSV
        report_df = pd.DataFrame(report_data.items(), columns=["Item", "Value"])
        csv_buffer = io.StringIO()
        report_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Download Report as CSV",
            data=csv_data,
            file_name="measureup_report.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown("---")
        st.markdown("<p style='font-size:18px; font-weight:bold; color:orchid;'>Report Preview</p>", unsafe_allow_html=True)
        st.table(report_df)
    else:
        st.error("No data available. Please complete all previous steps.")
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Previous", use_container_width=True):
            go_to_page(5)
    with col2:
        if st.button("🏠 Start Over", use_container_width=True):
            # Reset all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

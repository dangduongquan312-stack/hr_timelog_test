import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ============================================
# CONFIG
# ============================================
st.set_page_config(
    page_title="HR Time Log - Test",
    page_icon="⏰",
    layout="centered"
)

DATA_FILE = "timelog_data.csv"

# 8 categories
CATEGORIES = [
    "1. Sourcing & Pipeline Building",
    "2. Selection & Hiring Execution",
    "3. Onboarding & Lifecycle Transition",
    "4. Employee Case Management",
    "5. Manager Advisory & Coaching",
    "6. HR Program Delivery",
    "7. Data, Reporting & Compliance",
    "8. Strategic Projects & Improvement"
]

# Activities mapped to categories
ACTIVITIES = {
    "1. Sourcing & Pipeline Building": [
        "1.1 Active sourcing (LinkedIn, job boards)",
        "1.2 Passive candidate networking",
        "1.3 Talent pool / pipeline building",
        "1.4 Recruitment events and career fairs",
        "1.5 Referral program management",
        "1.6 Vendor / agency engagement",
        "1.7 Market mapping and intelligence"
    ],
    "2. Selection & Hiring Execution": [
        "2.1 Resume screening",
        "2.2 Initial phone/video screening",
        "2.3 Interview coordination and scheduling",
        "2.4 Interview conduct (HR rounds)",
        "2.5 Candidate assessment consolidation",
        "2.6 Offer preparation and benchmarking",
        "2.7 Offer negotiation and acceptance",
        "2.8 Background check and verification"
    ],
    "3. Onboarding & Lifecycle Transition": [
        "3.1 Pre-boarding coordination",
        "3.2 Day 1 onboarding execution",
        "3.3 Probation period management",
        "3.4 Internal transfer and mobility",
        "3.5 Promotion workflow administration",
        "3.6 Exit management and offboarding",
        "3.7 Exit interview and feedback"
    ],
    "4. Employee Case Management": [
        "4.1 Policy and benefits queries",
        "4.2 ER cases (Tier 1 - low complexity)",
        "4.3 ER cases (Tier 2 - medium complexity)",
        "4.4 Disciplinary case handling",
        "4.5 Grievance management",
        "4.6 Leave and absence issue resolution",
        "4.7 Compensation and payroll query"
    ],
    "5. Manager Advisory & Coaching": [
        "5.1 Performance management coaching",
        "5.2 Team dynamics coaching",
        "5.3 Talent decision consultation",
        "5.4 Compensation and recognition advisory",
        "5.5 Leadership development discussions",
        "5.6 Difficult conversation preparation",
        "5.7 Change management support"
    ],
    "6. HR Program Delivery": [
        "6.1 Performance review cycle",
        "6.2 Calibration session facilitation",
        "6.3 Talent review and succession",
        "6.4 Engagement survey rollout",
        "6.5 Culture and values program",
        "6.6 Compensation cycle execution",
        "6.7 L&D program coordination"
    ],
    "7. Data, Reporting & Compliance": [
        "7.1 HRIS data entry and update",
        "7.2 Monthly/quarterly HR report",
        "7.3 Ad-hoc data request",
        "7.4 Headcount and workforce tracking",
        "7.5 Regulatory compliance reporting",
        "7.6 Audit support and documentation",
        "7.7 Data quality monitoring"
    ],
    "8. Strategic Projects & Improvement": [
        "8.1 Workforce planning and org design",
        "8.2 HR process redesign projects",
        "8.3 Employer branding strategy",
        "8.4 HR technology adoption",
        "8.5 COE collaboration on programs",
        "8.6 Cross-functional HR initiatives",
        "8.7 Capability building for HR and managers"
    ]
}

TIERS = [
    "Tier 1 - Junior staff",
    "Tier 2 - Mid-level (Manager, Senior Officer)",
    "Tier 3 - Senior banker (Senior Manager, Expert)",
    "Tier 4 - Head / Director",
    "N/A - No specific person"
]

VA_TAGS = [
    "VA - Value-Add (only I can do this)",
    "NNVA - Necessary but could be simplified",
    "Waste - Rework, waiting, duplication"
]

# ============================================
# DATA FUNCTIONS
# ============================================
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "Timestamp", "User", "Category", "Activity",
            "Tier", "VA_Tag", "Note"
        ])

def save_entry(user, category, activity, tier, va_tag, note):
    df = load_data()
    new_entry = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "User": user,
        "Category": category,
        "Activity": activity,
        "Tier": tier,
        "VA_Tag": va_tag,
        "Note": note if note else ""
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# ============================================
# UI
# ============================================
st.title("⏰ HR Time Log")
st.caption("Test version - Techcombank People Partner")

# Sidebar for name
with st.sidebar:
    st.header("Thông tin")
    user_name = st.text_input("Tên của bạn:", placeholder="VD: Anh Minh")
    st.divider()
    st.caption("Version: Test v0.1")

if not user_name:
    st.info("👈 Vui lòng nhập tên ở sidebar bên trái để bắt đầu")
    st.stop()

# Main tabs
tab1, tab2 = st.tabs(["📝 Log activity", "📊 Xem data"])

# ============================================
# TAB 1 - LOG ACTIVITY
# ============================================
with tab1:
    st.subheader(f"Xin chào, {user_name}")
    st.write("Log hoạt động trong 2 giờ vừa qua:")

    with st.form("timelog_form"):
        # Step 1: Category
        category = st.selectbox(
            "**Bước 1:** Chọn category",
            options=CATEGORIES,
            index=None,
            placeholder="Chọn 1 trong 8 categories..."
        )

        # Step 2: Activity (filtered by category)
        if category:
            activity = st.selectbox(
                "**Bước 2:** Chọn activity cụ thể",
                options=ACTIVITIES[category],
                index=None,
                placeholder="Chọn activity..."
            )
        else:
            activity = None
            st.selectbox(
                "**Bước 2:** Chọn activity cụ thể",
                options=["Chọn category trước"],
                disabled=True
            )

        # Step 3: Tier
        tier = st.selectbox(
            "**Bước 3:** Tier của CBNV/candidate liên quan",
            options=TIERS,
            index=None,
            placeholder="Chọn tier..."
        )

        # Step 4: VA tag
        va_tag = st.selectbox(
            "**Bước 4:** Value tag",
            options=VA_TAGS,
            index=None,
            placeholder="Chọn tag..."
        )

        # Step 5: Optional note
        note = st.text_input(
            "**Bước 5 (optional):** Ghi chú (max 50 ký tự)",
            max_chars=50,
            placeholder="Optional..."
        )

        submitted = st.form_submit_button("✅ Submit", use_container_width=True)

        if submitted:
            if not all([category, activity, tier, va_tag]):
                st.error("⚠️ Vui lòng điền đủ 4 trường bắt buộc (Bước 1-4)")
            else:
                save_entry(user_name, category, activity, tier, va_tag, note)
                st.success("✅ Đã lưu! Cảm ơn bạn.")
                st.balloons()

# ============================================
# TAB 2 - VIEW DATA
# ============================================
with tab2:
    st.subheader("📊 Data của bạn")

    df = load_data()

    if df.empty:
        st.info("Chưa có entry nào. Log activity đầu tiên ở tab 'Log activity'!")
    else:
        user_df = df[df["User"] == user_name].sort_values("Timestamp", ascending=False)

        if user_df.empty:
            st.info(f"Chưa có entry nào cho {user_name}")
        else:
            st.metric("Tổng số entries", len(user_df))

            st.write("**5 entries gần nhất:**")
            st.dataframe(
                user_df.head(5)[["Timestamp", "Category", "Activity", "Tier", "VA_Tag"]],
                use_container_width=True,
                hide_index=True
            )

            # Simple distribution
            st.write("**Phân bổ theo category:**")
            cat_counts = user_df["Category"].value_counts()
            st.bar_chart(cat_counts)

    # Admin section
    st.divider()
    with st.expander("🔑 Admin view (toàn bộ data)"):
        admin_pin = st.text_input("Admin PIN:", type="password", key="admin")
        if admin_pin == "1234":
            st.success("Admin access granted")
            st.dataframe(df, use_container_width=True)
            st.download_button(
                "📥 Download all data (CSV)",
                data=df.to_csv(index=False),
                file_name=f"timelog_export_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        elif admin_pin:
            st.error("Wrong PIN")

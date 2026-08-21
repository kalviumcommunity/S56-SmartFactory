import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SmartFactory",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.html(
    """
    <style>

    #MainMenu,
    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    .stApp {
        background: #f7f8fa;
    }

    .block-container {
        max-width: 1180px;
        padding: 42px 52px 55px 52px;
    }


    /* ========================================================
       ANIMATIONS
       ======================================================== */

    @keyframes sfFadeUp {
        from {
            opacity: 0;
            transform: translateY(22px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes sfFadeIn {
        from {
            opacity: 0;
        }

        to {
            opacity: 1;
        }
    }

    .sf-hero {
        animation: sfFadeUp 0.7s ease-out;
    }

    .sf-feature {
        animation: sfFadeUp 0.8s ease-out;
    }

    .sf-footer {
        animation: sfFadeIn 1.2s ease-out;
    }


    /* ========================================================
       BRAND
       ======================================================== */

    .sf-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 82px;
    }

    .sf-brand-mark {
        width: 46px;
        height: 46px;
        border-radius: 11px;
        background: #2563eb;
        color: #ffffff;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 20px;
        font-weight: 700;

        box-shadow:
            0 6px 16px rgba(37, 99, 235, 0.20);
    }

    .sf-brand-name {
        color: #101828;
        font-size: 20px;
        font-weight: 700;
        line-height: 1.2;
    }

    .sf-brand-subtitle {
        color: #667085;
        font-size: 12px;
        margin-top: 3px;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .sf-hero {
        max-width: 850px;
    }

    .sf-eyebrow {
        display: inline-flex;
        align-items: center;

        padding: 7px 12px;
        border-radius: 999px;

        background: #edf3ff;
        color: #2563eb;

        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.06em;

        margin-bottom: 20px;
    }

    .sf-title {
        color: #101828;

        font-size: 54px;
        line-height: 1.08;

        font-weight: 750;
        letter-spacing: -2.4px;

        max-width: 850px;
    }

    .sf-title-accent {
        color: #2563eb;
    }

    .sf-description {
        color: #667085;

        font-size: 17px;
        line-height: 1.65;

        max-width: 680px;

        margin-top: 22px;
    }


    /* ========================================================
       DASHBOARD BUTTON
       ======================================================== */

    div.stButton {
        margin-top: 30px;
    }

    div.stButton > button {
        min-height: 44px;

        padding: 0 21px;

        border-radius: 8px;

        font-size: 14px;
        font-weight: 600;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            background 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 8px 18px rgba(37, 99, 235, 0.18);
    }


    /* ========================================================
       FEATURE SECTION
       ======================================================== */

    .sf-features {
        margin-top: 78px;
    }

    .sf-feature {
        min-height: 190px;

        padding: 25px;

        background: #ffffff;

        border: 1px solid #e4e7ec;
        border-radius: 13px;

        box-shadow:
            0 1px 2px rgba(16, 24, 40, 0.03);

        transition:
            transform 0.22s ease,
            box-shadow 0.22s ease,
            border-color 0.22s ease;
    }

    .sf-feature:hover {
        transform: translateY(-5px);

        border-color: #c7d7fe;

        box-shadow:
            0 12px 28px rgba(16, 24, 40, 0.08);
    }

    .sf-feature-icon {
        width: 42px;
        height: 42px;

        border-radius: 10px;

        background: #edf3ff;
        color: #2563eb;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 15px;
        font-weight: 700;

        margin-bottom: 18px;
    }

    .sf-feature-title {
        color: #101828;

        font-size: 15px;
        font-weight: 650;

        margin-bottom: 8px;
    }

    .sf-feature-text {
        color: #667085;

        font-size: 13px;
        line-height: 1.6;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .sf-footer {
        color: #98a2b3;

        text-align: center;

        font-size: 12px;

        margin-top: 62px;
    }

    </style>
    """
)


# ============================================================
# BRAND
# ============================================================

st.html(
    """
    <div class="sf-brand">

        <div class="sf-brand-mark">
            S
        </div>

        <div>
            <div class="sf-brand-name">
                SmartFactory
            </div>

            <div class="sf-brand-subtitle">
                Manufacturing Analytics Platform
            </div>
        </div>

    </div>
    """
)


# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div class="sf-hero">

        <div class="sf-eyebrow">
            MANUFACTURING INTELLIGENCE
        </div>

        <div class="sf-title">
            Turn factory data into
            <span class="sf-title-accent">
                actionable insight.
            </span>
        </div>

        <div class="sf-description">
            SmartFactory brings machine performance,
            uptime, defects, maintenance activity and
            operational risks into one unified analytics
            platform.
        </div>

    </div>
    """
)


# ============================================================
# DASHBOARD BUTTON
# ============================================================

if st.button(
    "Open Dashboard",
    type="primary",
    icon=":material/arrow_forward:",
):
    st.switch_page("app.py")


# ============================================================
# FEATURES
# ============================================================

st.html(
    """
    <div class="sf-features"></div>
    """
)

col1, col2, col3 = st.columns(
    3,
    gap="large",
)


with col1:
    st.html(
        """
        <div class="sf-feature">

            <div class="sf-feature-icon">
                M
            </div>

            <div class="sf-feature-title">
                Machine Intelligence
            </div>

            <div class="sf-feature-text">
                Monitor machine records, models,
                performance and uptime using live
                factory data.
            </div>

        </div>
        """
    )


with col2:
    st.html(
        """
        <div class="sf-feature">

            <div class="sf-feature-icon">
                P
            </div>

            <div class="sf-feature-title">
                Predictive Maintenance
            </div>

            <div class="sf-feature-text">
                Track preventive and corrective
                maintenance activity and identify
                operational patterns.
            </div>

        </div>
        """
    )


with col3:
    st.html(
        """
        <div class="sf-feature">

            <div class="sf-feature-icon">
                A
            </div>

            <div class="sf-feature-title">
                Quality Analytics
            </div>

            <div class="sf-feature-text">
                Analyze defects, machine trends and
                early-warning indicators to support
                faster decisions.
            </div>

        </div>
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="sf-footer">
        SmartFactory Analytics Platform
        &nbsp;&middot;&nbsp;
        Manufacturing Intelligence
    </div>
    """
)
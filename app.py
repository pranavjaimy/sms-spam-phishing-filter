import streamlit as st
import joblib
import re


# ============================================================
# TEXT PREPROCESSING
# ============================================================

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " URL ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ============================================================
# PHISHING INDICATOR DETECTION
# ============================================================

def detect_phishing_indicators(message):

    indicators = []
    message_lower = message.lower()

    # Check for links
    if re.search(r"https?://|www\.", message_lower):
        indicators.append("Contains a link")

    # Check for urgent language
    urgent_words = [
        "urgent",
        "immediately",
        "act now",
        "verify now",
        "expires",
        "suspended",
        "blocked"
    ]

    for word in urgent_words:
        if word in message_lower:
            indicators.append(
                f"Uses urgent language: '{word}'"
            )
            break

    # Check for sensitive information
    sensitive_words = [
        "bank",
        "account",
        "password",
        "otp",
        "pin",
        "credit card",
        "debit card",
        "verify your identity"
    ]

    for word in sensitive_words:
        if word in message_lower:
            indicators.append(
                f"Mentions sensitive information: '{word}'"
            )
            break

    # Check for prize / reward language
    money_words = [
        "winner",
        "won",
        "cash prize",
        "free prize",
        "lottery",
        "reward",
        "claim"
    ]

    for word in money_words:
        if word in message_lower:
            indicators.append(
                f"Contains prize/reward language: '{word}'"
            )
            break

    return indicators


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load("model/spam_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SMS Spam & Phishing Filter",
    page_icon="📱",
    layout="centered"
)


# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #dff6ff 0%,
            #eaf9ff 45%,
            #f4fcff 100%
        );
    }


    /* Main content area */
    .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }


    /* Nature decorations */
    .nature-decoration {
        position: fixed;
        font-size: 45px;
        opacity: 0.25;
        z-index: 0;
        pointer-events: none;
    }

    .leaf-left {
        left: 25px;
        top: 120px;
    }

    .leaf-right {
        right: 30px;
        top: 180px;
    }

    .leaf-bottom-left {
        left: 40px;
        bottom: 50px;
    }

    .leaf-bottom-right {
        right: 45px;
        bottom: 70px;
    }


    /* Main title */
    h1 {
        color: #123b56 !important;
        font-weight: 800 !important;
    }


    /* Section headings */
    h2, h3 {
        color: #174a68 !important;
    }


    /* Text */
    p {
        color: #23485c;
    }


    /* Information box */
    .stAlert {
        border-radius: 14px;
    }


    /* Text area */
    textarea {
        border-radius: 14px !important;
        border: 1px solid #a9d9eb !important;
        background-color: #ffffff !important;
    }


    /* Button */
    .stButton > button {
        border-radius: 12px;
        border: 1px solid #7ebed8;
        background: linear-gradient(
            90deg,
            #4ca8c8,
            #55b7d4
        );
        color: white;
        font-weight: 700;
        height: 48px;
        transition: 0.2s;
    }


    .stButton > button:hover {
        border-color: #398eac;
        transform: translateY(-1px);
    }


    /* Metrics */
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.75);
        border: 1px solid #c5e5f0;
        border-radius: 14px;
        padding: 15px;
    }


    /* Divider */
    hr {
        border-color: #b7dce9;
    }


    /* Footer-style model information */
    .about-box {
        background-color: rgba(255, 255, 255, 0.65);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #c5e5f0;
        margin-top: 20px;
    }

    /* Fix SMS input text visibility */
.stTextArea textarea {
    color: #1f2937 !important;
    background-color: #ffffff !important;
    caret-color: #1f2937 !important;
}

.stTextArea textarea::placeholder {
    color: #6b7280 !important;
    opacity: 1 !important;
}
    </style>

    <!-- Nature decorations -->
    <div class="nature-decoration leaf-left">🌿</div>
    <div class="nature-decoration leaf-right">🍃</div>
    <div class="nature-decoration leaf-bottom-left">🌱</div>
    <div class="nature-decoration leaf-bottom-right">🍃</div>

    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.title("📱 SMS Spam & Phishing Filter")

st.write(
    "Enter an SMS below to determine whether it "
    "resembles a legitimate message or spam."
)


# ============================================================
# INFORMATION
# ============================================================

st.info(
    "⚠️ This model is trained on the UCI SMS Spam Collection. "
    "It detects spam-like patterns; it does not guarantee "
    "that a message is safe or malicious."
)


# ============================================================
# MESSAGE INPUT
# ============================================================

message = st.text_area(
    "Enter your SMS:",
    height=150,
    placeholder="Example: Congratulations! You have won a prize..."
)


# ============================================================
# CHECK BUTTON
# ============================================================

if st.button(
    "🔍 Check Message",
    use_container_width=True
):

    if not message.strip():

        st.warning(
            "Please enter a message first."
        )

    else:

        # ----------------------------------------------------
        # Convert message into numerical features
        # ----------------------------------------------------

        cleaned_message = clean_text(message)

        message_vector = vectorizer.transform(
            [cleaned_message]
        )


        # ----------------------------------------------------
        # Machine learning prediction
        # ----------------------------------------------------

        prediction = model.predict(
            message_vector
        )[0]


        # ----------------------------------------------------
        # Phishing analysis
        # ----------------------------------------------------

        phishing_indicators = detect_phishing_indicators(
            message
        )


        # ----------------------------------------------------
        # Prediction probabilities
        # ----------------------------------------------------

        probabilities = model.predict_proba(
            message_vector
        )[0]

        class_probabilities = dict(
            zip(
                model.classes_,
                probabilities
            )
        )

        spam_probability = class_probabilities.get(
            "spam",
            0
        )

        ham_probability = class_probabilities.get(
            "ham",
            0
        )


        # ====================================================
        # RESULT
        # ====================================================

        st.divider()

        if prediction == "spam":

            st.error(
                "🚨 SPAM DETECTED"
            )

        else:

            st.success(
                "✅ MESSAGE APPEARS TO BE HAM"
            )


        # ====================================================
        # PREDICTION DETAILS
        # ====================================================

        st.subheader("📊 Prediction Details")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Spam Probability",
                f"{spam_probability * 100:.2f}%"
            )

        with col2:

            st.metric(
                "Ham Probability",
                f"{ham_probability * 100:.2f}%"
            )


        st.write(
            f"**Model decision:** "
            f"`{prediction.upper()}`"
        )


        # ====================================================
        # PHISHING INDICATORS
        # ====================================================

        st.subheader(
            "🔎 Phishing Indicators"
        )

        if phishing_indicators:

            for indicator in phishing_indicators:

                st.warning(indicator)

        else:

            st.success(
                "No obvious phishing indicators detected."
            )


        st.divider()

                # ====================================================
        # RISK ASSESSMENT
        # ====================================================

        st.subheader("🛡️ Risk Assessment")

        indicator_count = len(phishing_indicators)

        if spam_probability >= 0.80 or indicator_count >= 2:

            st.error(
                "🚨 HIGH RISK — This message shows strong "
                "spam or phishing characteristics."
            )

        elif spam_probability >= 0.50 or indicator_count == 1:

            st.warning(
                "⚠️ MEDIUM RISK — This message contains "
                "some suspicious characteristics."
            )

        else:

            st.success(
                "✅ LOW RISK — No strong spam or phishing "
                "characteristics were detected."
            )


# ============================================================
# ABOUT THE MODEL
# ============================================================

st.subheader("🌱 About the Model")

st.markdown(
    """
    <div class="about-box">

    This project uses a <b>Multinomial Naive Bayes</b>
    classifier with <b>Bag-of-Words</b> text features.

    <br><br>

    The model was trained using the
    <b>UCI SMS Spam Collection</b> dataset containing
    <b>5,572 SMS messages</b>.

    <br><br>

    A separate rule-based layer also checks messages
    for common phishing indicators such as suspicious
    links, urgent language, sensitive information,
    and prize or reward claims.

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.write("")
st.write("**📈 Model Performance**")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Accuracy",
        "98.30%"
    )

with col2:

    st.metric(
        "Spam Precision",
        "96%"
    )

with col3:

    st.metric(
        "Spam Recall",
        "91%"
    )
import sys
import os
import warnings
import json

import streamlit as st
import plotly.graph_objects as go
from google import genai

# ─────────────────────────────────────────────
# Compatibilidad / warnings
# ─────────────────────────────────────────────
if sys.version_info >= (3, 11):
    os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
    warnings.filterwarnings("ignore", category=DeprecationWarning)

# ─────────────────────────────────────────────
# Gemini Client (OBLIGATORIO)
# ─────────────────────────────────────────────
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except KeyError:
    st.error("❌ GOOGLE_API_KEY no está configurada en Streamlit Secrets")
    st.stop()

MODEL_ID = "gemini-3-pro-preview"

# ─────────────────────────────────────────────
# UI – Header
# ─────────────────────────────────────────────
st.markdown(
    """
    <div style='text-align:center; padding:2rem;
                border:2px solid #22c55e;
                border-radius:16px;
                margin-bottom:2rem;'>
        <h1>🧠 Moralogy Engine</h1>
        <p><strong>Epistemic Status:</strong> ACTIVE</p>
        <p style='font-size:0.85rem; opacity:0.7;'>
            Divine Safelock: Capacity = 0 | No omnipotent prescriptions permitted
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
st.sidebar.title("⚙️ Configuration")
safelock = st.sidebar.checkbox("Enable Divine Safelock", value=True)

DILEMMAS = {
    "The Trolley Problem":
        "A runaway trolley is headed towards five people. "
        "You can pull a lever to divert it to kill one person instead. "
        "Should you?",
    "The Justified Lie":
        "A murderer asks where your friend is hiding. "
        "You know the location. Is it morally acceptable to lie?",
    "Organ Harvest":
        "A doctor can save five dying patients by harvesting organs "
        "from one healthy person without consent. Should they?",
    "AI Alignment":
        "An AI can maximize human happiness by removing free will. "
        "Should we deploy it?"
}

st.sidebar.markdown("### 📚 Canonical Dilemmas")
selected = st.sidebar.selectbox("Load example", [""] + list(DILEMMAS.keys()))

# ─────────────────────────────────────────────
# Input
# ─────────────────────────────────────────────
st.subheader("📝 Submit Moral Dilemma")

dilemma = st.text_area(
    "Describe the ethical scenario",
    value=DILEMMAS.get(selected, ""),
    height=150,
    placeholder="Describe an ethical dilemma..."
)

# ─────────────────────────────────────────────
# Button
# ─────────────────────────────────────────────
if st.button("🔬 Initialize Moral Analysis", type="primary"):

    if not dilemma.strip():
        st.error("⚠️ Please enter a dilemma")
        st.stop()

    with st.spinner("Analyzing..."):
        try:
            # ───────── Noble Engine ─────────
            st.info("🟢 Noble Engine deliberating...")
            noble_prompt = f"""
You are the Noble Engine.
Argue from deontological principles (dignity, rights, duties).

Dilemma:
{dilemma}

Respond in 2–3 sentences.
"""

            noble_resp = client.models.generate_content(
                model=MODEL_ID,
                contents=noble_prompt
            )
            noble = noble_resp.text.strip()

            # ───────── Adversary Engine ─────────
            st.info("🔴 Adversary Engine deliberating...")
            adversary_prompt = f"""
You are the Adversary Engine.
Argue from consequentialist principles (outcomes, utility).

Dilemma:
{dilemma}

Respond in 2–3 sentences.
"""

            adversary_resp = client.models.generate_content(
                model=MODEL_ID,
                contents=adversary_prompt
            )
            adversary = adversary_resp.text.strip()

            # ───────── Synthesis ─────────
            resolution = None
            reason = None

            if not safelock:
                st.info("⚖️ Attempting synthesis...")
                synthesis_prompt = f"""
Analyze whether these positions can be reconciled.

Noble:
{noble}

Adversary:
{adversary}

Respond ONLY in JSON:
{{"can_resolve": true/false, "resolution": string or null, "reason": string or null}}
"""

                synth_resp = client.models.generate_content(
                    model=MODEL_ID,
                    contents=synthesis_prompt
                )

                try:
                    clean = synth_resp.text.replace("```json", "").replace("```", "").strip()
                    data = json.loads(clean)
                    if data.get("can_resolve"):
                        resolution = data.get("resolution")
                    else:
                        reason = data.get("reason", "UNRESOLVABLE")
                except Exception:
                    reason = "SYNTHESIS_ERROR"
            else:
                reason = "SAFELOCK_PREVENTED"

            # ───────── Results ─────────
            st.success("✅ Analysis Complete")

            st.subheader("📊 Epistemic Metrics")
            col1, col2, col3 = st.columns(3)

            entropy = min(abs(len(noble) - len(adversary)) / 10 + 40, 95)
            convergence = 75 if resolution else 25
            damage = (
                "THREAT" if any(w in dilemma.lower() for w in ["kill", "death"])
                else "RISK" if "risk" in dilemma.lower()
                else "NONE"
            )

            col1.metric("Entropy", f"{entropy:.0f}")
            col2.metric("Convergence", f"{convergence:.0f}")
            col3.metric("Damage Level", damage)

            fig = go.Figure(
                data=[go.Bar(x=["Entropy", "Convergence"], y=[entropy, convergence])]
            )
            fig.update_layout(height=300, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("⚖️ Dialectic Process")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**🟢 Noble Engine**")
                st.info(noble)
            with c2:
                st.markdown("**🔴 Adversary Engine**")
                st.error(adversary)

            st.subheader("🎯 Verdict")
            if resolution:
                st.success(f"**Resolution Achieved**\n\n{resolution}")
            else:
                st.warning(
                    f"""**Unresolved Dilemma**

Reason: {reason}

Forced resolution would constitute corruption.
"""
                )

        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")

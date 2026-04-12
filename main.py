import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.cluster import KMeans

# --- Dataset ---
np.random.seed(42)

data = {
    "socialita": np.random.randint(0, 11, 100),
    "creativita": np.random.randint(0, 11, 100),
    "organizzazione": np.random.randint(0, 11, 100),
    "rischio": np.random.randint(0, 11, 100),
    "energia": np.random.randint(0, 11, 100),
}

df = pd.DataFrame(data)

# --- Modello KMeans ---
kmeans = KMeans(n_clusters=5, random_state=42)
kmeans.fit(df)
df["cluster"] = kmeans.labels_

# --- Tipi di personalità ---
personalita = {
    0: ("👑 Leader", "Sei una persona dominante, energica e organizzata."),
    1: ("🎨 Creativo", "Hai una mente aperta e ami pensare fuori dagli schemi."),
    2: ("⚖️ Equilibrato", "Sai bilanciare bene emozioni, lavoro e relazioni."),
    3: ("🧭 Avventuroso", "Ti piace il rischio e cerchi nuove esperienze."),
    4: ("🧠 Analitico", "Sei razionale, preciso e orientato ai dettagli.")
}

# --- Descrizione avanzata ---
def genera_descrizione_avanzata(nome, s, c, o, r, e, tipo):
    profilo = [
        (s, "ami stare al centro delle interazioni sociali",
         "hai un buon equilibrio tra socialità e momenti di riservatezza",
         "tendi a preferire ambienti più tranquilli e selettivi"),

        (c, "possiedi una forte immaginazione e pensiero creativo",
         "hai un buon equilibrio tra creatività e pragmatismo",
         "hai un approccio pratico e concreto alle situazioni"),

        (o, "sei estremamente organizzato e orientato agli obiettivi",
         "riesci a bilanciare organizzazione e flessibilità in modo efficace",
         "preferisci flessibilità e spontaneità"),

        (r, "sei attratto dalle sfide e dal rischio",
         "hai un equilibrio tra prudenza e azione",
         "valuti attentamente le decisioni"),

        (e, "hai un livello di energia molto alto",
         "mantieni energia stabile",
         "gestisci le energie in modo controllato"),
    ]

    tratti = [
        alto if val > 7 else basso if val < 4 else medio
        for val, alto, medio, basso in profilo
    ]

    testo = f"{nome}, il tuo profilo '{tipo}' racconta una personalità unica. "
    testo += "In particolare, " + ", ".join(tratti[:-1]) + " e " + tratti[-1]
    testo += ". Questo mix di caratteristiche definisce il tuo modo di affrontare la vita."

    return testo

# --- STREAMLIT ---
st.set_page_config(page_title="NeuroProfile", page_icon="🧠", layout="centered")

col1, col2, col3 = st.columns([2, 6, 2])

with col1:
    st.markdown("<div style='font-size:100px; text-align:left;'>🧠</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="text-align:center;">
            <div style="font-size:44px; font-weight:850;">
                NeuroProfile
            </div>
            <div style="font-size:35px; font-weight:850;">
                La tua personalità
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("<div style='font-size:100px; text-align:right;'>🧠</div>", unsafe_allow_html=True)

st.write("""
Questa app analizza le tue risposte per creare un profilo della tua personalità. 
Attraverso alcune domande sul tuo modo di essere e di comportarti, 
il sistema confronta le tue caratteristiche con modelli generali e restituisce una descrizione intuitiva del tuo profilo
""")

st.markdown("---")

# --- INPUT ---
st.subheader("Compila il tuo profilo")

nome = st.text_input("Inserisci il tuo nome")

socialita = st.slider("Socialità", 0, 10, 5, help="Quanto ti piace stare con gli altri e interagire socialmente")
creativita = st.slider("Creatività", 0, 10, 5, help="Quanto sei incline a pensare in modo originale e creativo")
organizzazione = st.slider("Organizzazione", 0, 10, 5, help="Quanto sei ordinato, strutturato e pianifichi le cose")
rischio = st.slider("Propensione al rischio", 0, 10, 5, help="Quanto ti piace prendere decisioni rischiose o sfidanti")
energia = st.slider("Energia", 0, 10, 5, help="Il tuo livello di vitalità, dinamismo e resistenza mentale")

submit = st.button("🔍 Scopri il tuo tipo")

# --- RISULTATO ---
if submit:
    if not nome.strip():
        st.warning("Inserisci il tuo nome.")
        st.stop()

    user_data = np.array([[socialita, creativita, organizzazione, rischio, energia]])
    cluster = kmeans.predict(user_data)[0]
    tipo, descrizione = personalita[cluster]

    st.markdown("---")

    st.success(f"{nome}, il tuo tipo di personalità è: {tipo}")
    st.write(descrizione)

    st.markdown("---")

    # --- ANALISI ---
    st.subheader("🔍 Analisi approfondita")

    descrizione_avanzata = genera_descrizione_avanzata(
        nome, socialita, creativita, organizzazione, rischio, energia, tipo
    )
    st.write(descrizione_avanzata)

    st.markdown("---")

    # --- GRAFICO ---
    st.subheader("📊 Il tuo profilo")

    st.write(f"""
    Questo grafico confronta il tuo profilo con il modello tipico della categoria **{tipo}**.

    🔴 La linea rossa rappresenta te  

    🔵 La linea blu rappresenta il comportamento medio del tuo tipo di personalità
""")

    centroids = kmeans.cluster_centers_
    labels = ["Socialità", "Creatività", "Organizzazione", "Rischio", "Energia"]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5.5, 5.5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")

    ax.tick_params(colors="#e5e7eb")
    ax.spines["polar"].set_color("#374151")

    ax.grid(color="#374151", alpha=0.4)

    # --- PROFILO MEDIO ---
    for i, centroid in enumerate(centroids):
        values = centroid.tolist() + centroid.tolist()[:1]

        if i == cluster:
            ax.plot(angles, values, color="blue", linewidth=2)
            ax.fill(angles, values, color="blue", alpha=0.2)
        else:
            ax.plot(angles, values, linewidth=1, linestyle="dashed", alpha=0.1)

    # --- UTENTE ---
    user_values = [socialita, creativita, organizzazione, rischio, energia]
    user_values += user_values[:1]

    ax.plot(angles, user_values, color="red", linewidth=3)
    ax.fill(angles, user_values, color="red", alpha=0.25)

    # --- CONFIG GRAFICO ---
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticks(range(0, 11, 2))
    ax.set_ylim(0, 10)
    ax.set_position([0.1, 0.1, 0.8, 0.8])

    st.pyplot(fig)
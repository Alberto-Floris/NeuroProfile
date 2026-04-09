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
# Divide i dati in 5 gruppi assegnando ogni punto al centroide più vicino.
# Il centroide è la media di tutte le coordinate dei punti del cluster.

kmeans = KMeans(n_clusters=5, random_state=42)
kmeans.fit(df)
df["cluster"] = kmeans.labels_

# --- Tipi di personalità ---

personalita = {
    0: ("Leader",      "Sei una persona dominante, energica e organizzata."),
    1: ("Creativo",    "Hai una mente aperta e ami pensare fuori dagli schemi."),
    2: ("Equilibrato", "Sai bilanciare bene emozioni, lavoro e relazioni."),
    3: ("Avventuroso", "Ti piace il rischio e cerchi nuove esperienze."),
    4: ("Analitico",   "Sei razionale, preciso e orientato ai dettagli.")
}

# --- Descrizione narrativa ---


def genera_descrizione_avanzata(nome, s, c, o, r, e, tipo):
    # (valore, frase_alta, frase_media, frase_bassa)
    profilo = [
        (s, "ami stare al centro delle interazioni sociali",
         "hai un buon equilibrio tra socialità e momenti di riservatezza",
         "tendi a preferire ambienti più tranquilli e selettivi"),
        (c, "possiedi una forte immaginazione e pensiero creativo",
         "hai un buon equilibrio tra creatività e pragmatismo",
         "hai un approccio pratico e concreto alle situazioni"),
        (o, "sei estremamente organizzato e orientato agli obiettivi",
         "riesci a bilanciare organizzazione e flessibilità in modo efficace",
         "preferisci flessibilità e spontaneità rispetto alla rigidità"),
        (r, "sei attratto dalle sfide e dal rischio",
         "hai un approccio equilibrato tra prudenza e voglia di metterti in gioco",
         "valuti attentamente le decisioni evitando rischi inutili"),
        (e, "hai un livello di energia molto alto e trascinante",
         "mantieni un livello di energia stabile e ben distribuito",
         "gestisci le tue energie in modo più riflessivo e controllato"),
    ]

    tratti = [
        alto if val > 7 else basso if val < 4 else medio
        for val, alto, medio, basso in profilo
    ]

    testo = f"{nome}, il tuo profilo '{tipo}' racconta una personalità unica. "
    testo += "In particolare, " + ", ".join(tratti[:-1]) + " e " + tratti[-1]
    testo += ". Questo mix di caratteristiche definisce il tuo modo distintivo di affrontare il mondo, le relazioni e le sfide quotidiane."

    return testo

# --- Interfaccia Streamlit ---


st.set_page_config(page_title="NeuroProfile", page_icon="🧬", layout="centered")

st.title("🧬 NeuroProfile: Il Codice della Tua Personalità")

st.write("""
Questa app utilizza un algoritmo di clustering (KMeans) per determinare
il tuo tipo di personalità in base alle tue caratteristiche.
""")

nome = st.text_input("Inserisci il tuo nome")
socialita = st.slider("Socialità", 0, 10)
creativita = st.slider("Creatività", 0, 10)
organizzazione = st.slider("Organizzazione", 0, 10)
rischio = st.slider("Propensione al rischio", 0, 10)
energia = st.slider("Energia", 0, 10)

sliders_non_impostati = (socialita + creativita +
                         organizzazione + rischio + energia == 0)

if st.button("Scopri il tuo tipo", disabled=sliders_non_impostati):
    if not nome.strip():
        st.warning("Inserisci il tuo nome per personalizzare il risultato.")
        st.stop()

    user_data = np.array(
        [[socialita, creativita, organizzazione, rischio, energia]])
    cluster = kmeans.predict(user_data)[0]
    tipo, descrizione = personalita[cluster]

    st.success(f"{nome}, il tuo tipo di personalità è: {tipo}")
    st.write(descrizione)

    descrizione_avanzata = genera_descrizione_avanzata(
        nome, socialita, creativita, organizzazione, rischio, energia, tipo
    )
    st.subheader("🔍 Analisi approfondita")
    st.write(descrizione_avanzata)

    # --- Grafico radar ---

    centroids = kmeans.cluster_centers_
    labels = ["Socialità", "Creatività",
              "Organizzazione", "Rischio", "Energia"]
    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for i, centroid in enumerate(centroids):
        values = centroid.tolist() + centroid.tolist()[:1]
        nome_cluster = personalita[i][0]
        if i == cluster:
            ax.plot(angles, values, linewidth=2,
                    label=f"Profilo medio {nome_cluster}")
            ax.fill(angles, values, alpha=0.25)
        else:
            ax.plot(angles, values, linewidth=1, linestyle="dashed", alpha=0.2)

    user_values = [socialita, creativita, organizzazione, rischio, energia]
    user_values += user_values[:1]
    ax.plot(angles, user_values, color="red",
            linewidth=3, label="Il tuo profilo")
    ax.fill(angles, user_values, color="red", alpha=0.3)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticks(range(0, 11, 2))
    ax.set_title(f"Confronto con il profilo '{tipo}'")
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    st.pyplot(fig)

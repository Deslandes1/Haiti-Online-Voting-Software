import streamlit as st
import sqlite3
import datetime
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import hashlib
import random
from PIL import Image
import base64

st.set_page_config(page_title="Haiti Online Voting Software", layout="wide")

# -----------------------------
# Language dictionary
# -----------------------------
lang_dict = {
    "en": {
        "title": "Haiti Online Voting Software",
        "subtitle": "Presidential Election – Choose your future",
        "select_dept": "Select your department",
        "departments": ["Artibonite", "Centre", "Grand'Anse", "Nippes", "Nord", "Nord-Est", "Nord-Ouest", "Ouest", "Sud", "Sud-Est"],
        "neutral": "Neutral (no candidate)",
        "vote_btn": "Vote",
        "already_voted": "You have already voted. Thank you for participating!",
        "vote_success": "Your vote has been recorded. Thank you for exercising your civic duty!",
        "election_over": "Election is over. Results are now available.",
        "election_active": "Election is active. Cast your vote before the deadline.",
        "time_remaining": "Time remaining until polls close",
        "winner_announcement": "🏆 WINNER ANNOUNCEMENT 🏆",
        "winner_text": "The winner of the presidential election is:",
        "votes_count": "votes",
        "results_title": "Final Results (sorted by votes)",
        "candidate_col": "Candidate",
        "party_col": "Party",
        "votes_col": "Votes",
        "slogan_col": "Slogan",
        "download_report": "Download Official Report (PDF)",
        "private_section": "🔐 CEP Private Section",
        "private_password": "Enter CEP password to view results before public release",
        "private_results": "Confidential Results – For CEP Use Only",
        "invalid_password": "Invalid password. Access denied.",
        "footer": "© 2026 GlobalInternet.py – Made in Haiti"
    },
    "fr": {
        "title": "Logiciel de Vote en Ligne d'Haïti",
        "subtitle": "Élection présidentielle – Choisissez votre avenir",
        "select_dept": "Sélectionnez votre département",
        "departments": ["Artibonite", "Centre", "Grand'Anse", "Nippes", "Nord", "Nord-Est", "Nord-Ouest", "Ouest", "Sud", "Sud-Est"],
        "neutral": "Neutre (aucun candidat)",
        "vote_btn": "Voter",
        "already_voted": "Vous avez déjà voté. Merci de votre participation !",
        "vote_success": "Votre vote a été enregistré. Merci d'avoir exercé votre devoir civique !",
        "election_over": "L'élection est terminée. Les résultats sont maintenant disponibles.",
        "election_active": "L'élection est active. Votez avant la date limite.",
        "time_remaining": "Temps restant avant la fermeture des bureaux de vote",
        "winner_announcement": "🏆 ANNONCE DU GAGNANT 🏆",
        "winner_text": "Le vainqueur de l'élection présidentielle est :",
        "votes_count": "votes",
        "results_title": "Résultats finaux (triés par nombre de votes)",
        "candidate_col": "Candidat",
        "party_col": "Parti",
        "votes_col": "Votes",
        "slogan_col": "Devise",
        "download_report": "Télécharger le rapport officiel (PDF)",
        "private_section": "🔐 Section privée du CEP",
        "private_password": "Entrez le mot de passe du CEP pour voir les résultats avant publication",
        "private_results": "Résultats confidentiels – Usage exclusif du CEP",
        "invalid_password": "Mot de passe incorrect. Accès refusé.",
        "footer": "© 2026 GlobalInternet.py – Fabriqué en Haïti"
    },
    "es": {
        "title": "Software de Voto en Línea de Haití",
        "subtitle": "Elección presidencial – Elige tu futuro",
        "select_dept": "Seleccione su departamento",
        "departments": ["Artibonite", "Centre", "Grand'Anse", "Nippes", "Nord", "Nord-Est", "Nord-Ouest", "Ouest", "Sud", "Sud-Est"],
        "neutral": "Neutral (ningún candidato)",
        "vote_btn": "Votar",
        "already_voted": "Ya has votado. ¡Gracias por participar!",
        "vote_success": "Tu voto ha sido registrado. ¡Gracias por ejercer tu deber cívico!",
        "election_over": "La elección ha terminado. Los resultados ya están disponibles.",
        "election_active": "La elección está activa. Vota antes de la fecha límite.",
        "time_remaining": "Tiempo restante para el cierre de las urnas",
        "winner_announcement": "🏆 ANUNCIO DEL GANADOR 🏆",
        "winner_text": "El ganador de la elección presidencial es:",
        "votes_count": "votos",
        "results_title": "Resultados finales (ordenados por votos)",
        "candidate_col": "Candidato",
        "party_col": "Partido",
        "votes_col": "Votos",
        "slogan_col": "Lema",
        "download_report": "Descargar informe oficial (PDF)",
        "private_section": "🔐 Sección privada del CEP",
        "private_password": "Ingrese la contraseña del CEP para ver los resultados antes de la publicación",
        "private_results": "Resultados confidenciales – Solo para uso del CEP",
        "invalid_password": "Contraseña incorrecta. Acceso denegado.",
        "footer": "© 2026 GlobalInternet.py – Hecho en Haití"
    },
    "ht": {
        "title": "Lojisyèl Vòt sou Entènèt Ayiti",
        "subtitle": "Eleksyon prezidansyèl – Chwazi avni w",
        "select_dept": "Chwazi depatman w",
        "departments": ["Atibonit", "Sant", "Grandans", "Nip", "Nò", "Nòdès", "Nòdwès", "Lwès", "Sid", "Sidès"],
        "neutral": "Net (pa gen kandida)",
        "vote_btn": "Vote",
        "already_voted": "Ou deja vote. Mèsi pou patisipasyon w!",
        "vote_success": "Vòt ou anrejistre. Mèsi pou egzèse dwa sivik ou!",
        "election_over": "Eleksyon an fini. Rezilta yo disponib kounye a.",
        "election_active": "Eleksyon an aktive. Vote anvan dat limit la.",
        "time_remaining": "Tan ki rete anvan biwo vòt yo fèmen",
        "winner_announcement": "🏆 ANONS GANYAN 🏆",
        "winner_text": "Ganyan eleksyon prezidansyèl la se :",
        "votes_count": "vòt",
        "results_title": "Rezilta final yo (klase pa kantite vòt)",
        "candidate_col": "Kandida",
        "party_col": "Patri",
        "votes_col": "Vòt",
        "slogan_col": "Deviz",
        "download_report": "Telechaje rapò ofisyèl (PDF)",
        "private_section": "🔐 Seksyon prive CEP",
        "private_password": "Antre modpas CEP la pou wè rezilta yo anvan piblikasyon",
        "private_results": "Rezilta konfidansyèl – Sèlman pou itilizasyon CEP",
        "invalid_password": "Modpas pa bon. Aksè refize.",
        "footer": "© 2026 GlobalInternet.py – Fèt an Ayiti"
    }
}

# -----------------------------
# Database setup
# -----------------------------
def init_db():
    conn = sqlite3.connect("election.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        party TEXT,
        slogan TEXT,
        symbol TEXT,
        votes INTEGER DEFAULT 0
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        voter_id TEXT,
        department TEXT,
        candidate_id INTEGER,
        timestamp TEXT,
        UNIQUE(voter_id)
    )""")
    conn.commit()
    conn.close()

# -----------------------------
# Helper functions
# -----------------------------
def hash_voter_id(voter_id):
    return hashlib.sha256(voter_id.encode()).hexdigest()

def add_candidate(name, party, slogan, symbol):
    conn = sqlite3.connect("election.db")
    c = conn.cursor()
    c.execute("INSERT INTO candidates (name, party, slogan, symbol, votes) VALUES (?,?,?,?,0)", (name, party, slogan, symbol))
    conn.commit()
    conn.close()

def get_candidates():
    conn = sqlite3.connect("election.db")
    df = pd.read_sql_query("SELECT * FROM candidates ORDER BY id", conn)
    conn.close()
    return df

def record_vote(voter_id, department, candidate_id):
    hashed = hash_voter_id(voter_id)
    conn = sqlite3.connect("election.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO votes (voter_id, department, candidate_id, timestamp) VALUES (?,?,?,?)",
                  (hashed, department, candidate_id, datetime.datetime.now().isoformat()))
        if candidate_id != -1:  # -1 is neutral
            c.execute("UPDATE candidates SET votes = votes + 1 WHERE id = ?", (candidate_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def has_voted(voter_id):
    hashed = hash_voter_id(voter_id)
    conn = sqlite3.connect("election.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM votes WHERE voter_id = ?", (hashed,))
    result = c.fetchone()
    conn.close()
    return result is not None

def get_results():
    conn = sqlite3.connect("election.db")
    df = pd.read_sql_query("SELECT name, party, slogan, votes FROM candidates ORDER BY votes DESC", conn)
    conn.close()
    return df

def get_total_votes():
    conn = sqlite3.connect("election.db")
    c = conn.cursor()
    c.execute("SELECT SUM(votes) FROM candidates")
    total = c.fetchone()[0] or 0
    conn.close()
    return total

def get_neutral_votes():
    conn = sqlite3.connect("election.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM votes WHERE candidate_id = -1")
    neutral = c.fetchone()[0] or 0
    conn.close()
    return neutral

def generate_report(results_df, neutral_votes, total_votes, winner_name, winner_votes, lang):
    t = lang_dict[lang]
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(t["title"], styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"{t['winner_text']} {winner_name} ({winner_votes} {t['votes_count']})", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(t["results_title"], styles['Heading3']))
    story.append(Spacer(1, 6))

    data = [[t["candidate_col"], t["party_col"], t["votes_col"], t["slogan_col"]]]
    for _, row in results_df.iterrows():
        data.append([row["name"], row["party"], str(row["votes"]), row["slogan"]])
    data.append(["Neutral", "-", str(neutral_votes), "-"])
    data.append(["Total", "-", str(total_votes), "-"])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(table)
    doc.build(story)
    buffer.seek(0)
    return buffer

# -----------------------------
# Generate demo candidates (10 AI candidates)
# -----------------------------
def generate_demo_candidates():
    conn = sqlite3.connect("election.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM candidates")
    count = c.fetchone()[0]
    conn.close()
    if count == 0:
        candidates_data = [
            ("Jean-Claude Pierre", "Unity Party", "For a united Haiti", "https://randomuser.me/api/portraits/men/1.jpg"),
            ("Marie-Louise Duval", "Hope Alliance", "Hope for tomorrow", "https://randomuser.me/api/portraits/women/2.jpg"),
            ("Joseph Bernard", "Liberty Movement", "Freedom and justice", "https://randomuser.me/api/portraits/men/3.jpg"),
            ("Anne-Sophie Michel", "Green Leaf Party", "Ecology and progress", "https://randomuser.me/api/portraits/women/4.jpg"),
            ("Luc Saint-Vil", "Peasant Front", "Land for all", "https://randomuser.me/api/portraits/men/5.jpg"),
            ("Michele Delatour", "Women's Power", "Strength in unity", "https://randomuser.me/api/portraits/women/6.jpg"),
            ("Pierre Richard", "Workers' Party", "Dignity through work", "https://randomuser.me/api/portraits/men/7.jpg"),
            ("Claudette Jean", "Education First", "Knowledge is power", "https://randomuser.me/api/portraits/women/8.jpg"),
            ("Emmanuel Charles", "New Deal", "A new beginning", "https://randomuser.me/api/portraits/men/9.jpg"),
            ("Rosemie Baptiste", "Social Justice", "Equality for all", "https://randomuser.me/api/portraits/women/10.jpg")
        ]
        for name, party, slogan, symbol in candidates_data:
            add_candidate(name, party, slogan, symbol)

# -----------------------------
# Election deadline (example: 5 minutes from now for demo, but you can set a fixed date)
# -----------------------------
def get_election_deadline():
    # For demo, election ends 5 minutes after app start. Change to a fixed date for real use.
    if "deadline" not in st.session_state:
        st.session_state.deadline = datetime.datetime.now() + datetime.timedelta(minutes=5)
    return st.session_state.deadline

def is_election_over():
    return datetime.datetime.now() >= get_election_deadline()

# -----------------------------
# Main app
# -----------------------------
init_db()
generate_demo_candidates()

# Language selection
lang = st.sidebar.selectbox("🌐 Language", options=["en", "fr", "es", "ht"], format_func=lambda x: {"en":"English","fr":"Français","es":"Español","ht":"Kreyòl"}[x])
t = lang_dict[lang]

# Main header
st.image("https://flagcdn.com/w320/ht.png", width=100)
st.title(t["title"])
st.markdown(f"### {t['subtitle']}")

# Election timer
deadline = get_election_deadline()
now = datetime.datetime.now()
if is_election_over():
    st.error(t["election_over"])
else:
    remaining = deadline - now
    hours = remaining.seconds // 3600
    minutes = (remaining.seconds % 3600) // 60
    seconds = remaining.seconds % 60
    st.info(f"{t['time_remaining']}: {hours:02d}h {minutes:02d}m {seconds:02d}s")

# Check if user has voted
voter_id = st.session_state.get("voter_id", None)
if voter_id is None:
    import uuid
    voter_id = str(uuid.uuid4())
    st.session_state.voter_id = voter_id

if has_voted(voter_id):
    st.warning(t["already_voted"])
elif is_election_over():
    st.error(t["election_over"])
else:
    # Voting form
    col1, col2 = st.columns([2, 1])
    with col1:
        department = st.selectbox(t["select_dept"], t["departments"])
    with col2:
        st.write("")
        st.write("")
        neutral_vote = st.checkbox(t["neutral"])

    candidates_df = get_candidates()
    if not neutral_vote:
        st.subheader("🗳️ Choose your candidate")
        cols = st.columns(3)
        selected_candidate = None
        for idx, row in candidates_df.iterrows():
            with cols[idx % 3]:
                st.image(row["symbol"], width=100)
                st.markdown(f"**{row['name']}**")
                st.caption(f"{row['party']}")
                st.caption(f"*{row['slogan']}*")
                if st.button(f"Vote for {row['name']}", key=f"vote_{row['id']}"):
                    selected_candidate = row["id"]
        if selected_candidate:
            if record_vote(voter_id, department, selected_candidate):
                st.success(t["vote_success"])
                st.rerun()
            else:
                st.error("Error recording vote. You may have already voted.")
    else:
        if st.button(t["vote_btn"]):
            if record_vote(voter_id, department, -1):
                st.success(t["vote_success"])
                st.rerun()
            else:
                st.error("Error recording vote. You may have already voted.")

# Results section (only if election over or private section)
if is_election_over():
    st.markdown("---")
    st.header("📊 Election Results")
    results_df = get_results()
    neutral_votes = get_neutral_votes()
    total_votes = get_total_votes() + neutral_votes
    if not results_df.empty:
        winner = results_df.iloc[0]
        winner_name = winner["name"]
        winner_votes = winner["votes"]
        st.markdown(f"## {t['winner_announcement']}")
        st.markdown(f"### {t['winner_text']} **{winner_name}** – {winner_votes} {t['votes_count']}")
        st.subheader(t["results_title"])
        st.dataframe(results_df[["name", "party", "votes", "slogan"]])
        st.write(f"**Neutral votes:** {neutral_votes}")
        st.write(f"**Total votes cast:** {total_votes}")

        # Download report
        report_buffer = generate_report(results_df, neutral_votes, total_votes, winner_name, winner_votes, lang)
        st.download_button(t["download_report"], data=report_buffer, file_name=f"election_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", mime="application/pdf")

# Private section for CEP
st.markdown("---")
with st.expander(t["private_section"]):
    pwd = st.text_input(t["private_password"], type="password")
    if st.button("Access Private Results"):
        if pwd == "18032026":
            st.success("Access granted. Confidential results below.")
            private_results = get_results()
            private_neutral = get_neutral_votes()
            private_total = get_total_votes() + private_neutral
            if not private_results.empty:
                private_winner = private_results.iloc[0]
                st.markdown(f"### {t['winner_text']} **{private_winner['name']}** – {private_winner['votes']} {t['votes_count']}")
                st.dataframe(private_results[["name", "party", "votes", "slogan"]])
                st.write(f"**Neutral votes:** {private_neutral}")
                st.write(f"**Total votes cast:** {private_total}")
                # Option to generate report for CEP
                report_buffer = generate_report(private_results, private_neutral, private_total, private_winner["name"], private_winner["votes"], lang)
                st.download_button("Download Confidential Report (PDF)", data=report_buffer, file_name=f"confidential_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", mime="application/pdf")
        else:
            st.error(t["invalid_password"])

st.markdown("---")
st.markdown(f"<center>{t['footer']}</center>", unsafe_allow_html=True)

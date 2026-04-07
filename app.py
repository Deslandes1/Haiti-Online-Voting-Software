import streamlit as st
import sqlite3
import datetime
import pandas as pd
import io
import os
import hashlib
import uuid
import json
import random
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from PIL import Image

st.set_page_config(page_title="Haiti Online Voting Software", layout="wide")

# -----------------------------
# Language dictionary (full)
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
        "private_password": "Enter CEP private password",
        "private_results": "Confidential Results – For CEP Use Only",
        "invalid_password": "Invalid password. Access denied.",
        "footer": "© 2026 GlobalInternet.py – Made in Haiti",
        "choose_candidate": "Choose your candidate",
        "vote_for": "Vote for",
        "not_specified": "Not specified",
        # Admin dashboard strings
        "admin_dashboard": "👑 CEP President Dashboard",
        "admin_welcome": "Welcome, President of the CEP. You can manage candidates below.",
        "admin_candidate_list": "📋 Current Candidates",
        "admin_id": "ID",
        "admin_name": "Name",
        "admin_party": "Party",
        "admin_slogan": "Slogan",
        "admin_votes": "Votes",
        "admin_symbol": "Symbol",
        "admin_update_symbol": "✏️ Update Symbol",
        "admin_delete": "🗑️ Delete",
        "admin_new_symbol_url": "New image URL (or upload file below)",
        "admin_upload_image": "Or upload an image file (JPEG/PNG)",
        "admin_update_btn": "Update Symbol",
        "admin_delete_confirm": "Are you sure you want to delete this candidate? This action cannot be undone and will remove all votes for them.",
        "admin_delete_btn": "Yes, delete candidate",
        "admin_add_candidate": "➕ Add New Candidate",
        "admin_name_en": "Name (English)",
        "admin_name_fr": "Name (French)",
        "admin_name_es": "Name (Spanish)",
        "admin_name_ht": "Name (Kreyòl)",
        "admin_party_en": "Party (English)",
        "admin_party_fr": "Party (French)",
        "admin_party_es": "Party (Spanish)",
        "admin_party_ht": "Party (Kreyòl)",
        "admin_slogan_en": "Slogan (English)",
        "admin_slogan_fr": "Slogan (French)",
        "admin_slogan_es": "Slogan (Spanish)",
        "admin_slogan_ht": "Slogan (Kreyòl)",
        "admin_symbol_url": "Candidate image URL (or upload file)",
        "admin_upload_symbol": "Upload image file",
        "admin_add_btn": "Add Candidate",
        "admin_add_success": "Candidate added successfully!",
        "admin_update_success": "Symbol updated successfully!",
        "admin_delete_success": "Candidate deleted successfully!",
        "admin_error": "An error occurred.",
        # Live monitoring strings
        "live_monitoring": "📡 Live Election Monitoring",
        "current_leader": "🏅 Current Leader",
        "total_votes_cast": "🗳️ Total votes cast",
        "neutral_votes": "⚪ Neutral votes",
        "quick_report": "📄 Download Quick Progress Report (PDF)",
        "last_refresh": "Last refresh",
        "refresh_button": "🔄 Refresh Live Results",
        "election_end_time": "Election ends at",
        "current_time": "Current server time",
        # Detailed votes
        "detailed_votes": "🔍 Detailed Votes (Anonymized)",
        "voter_id_col": "Voter ID (Hashed)",
        "candidate_voted": "Candidate Voted",
        "department_col": "Department",
        "timestamp_col": "Timestamp",
        # Company info
        "company_name": "GlobalInternet.py",
        "company_owner": "Owner: Gesner Deslandes",
        "company_contact": "Contact: (509)-47385663",
        "company_email": "Email: deslandes78@gmail.com",
        "company_rights": "All rights reserved - Proprietary License",
        "company_sale": "This software is for sale: $2,000 USD for online presidential elections.",
        "company_note": "When you are ready to experiment this online process, contact us.",
        # Password change
        "change_password": "🔐 Change Passwords",
        "change_app_password": "Change App Login Password (current: hidden)",
        "change_private_password": "Change Private Section Password (current: hidden)",
        "new_password": "New password",
        "confirm_password": "Confirm new password",
        "request_code": "Request verification code",
        "verification_code": "Enter 6-digit code",
        "submit_change": "Change password",
        "code_sent": "A verification code has been sent to your email (simulated). Code: {code}",
        "code_mismatch": "Invalid verification code.",
        "password_mismatch": "Passwords do not match.",
        "password_changed": "Password changed successfully!",
        "email_placeholder": "Your email address",
        "change_logout": "Logout from CEP Dashboard",
        # Login screen
        "login_title": "CEP President Login",
        "login_subtitle": "Enter your credentials to access the voting system",
        "app_password_label": "App Password (default: 20082010)",
        "login_button": "Login",
        "wrong_app_password": "Wrong password. Access denied."
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
        "private_password": "Entrez le mot de passe privé du CEP",
        "private_results": "Résultats confidentiels – Usage exclusif du CEP",
        "invalid_password": "Mot de passe incorrect. Accès refusé.",
        "footer": "© 2026 GlobalInternet.py – Fabriqué en Haïti",
        "choose_candidate": "Choisissez votre candidat",
        "vote_for": "Voter pour",
        "not_specified": "Non spécifié",
        "admin_dashboard": "👑 Tableau de bord du Président du CEP",
        "admin_welcome": "Bienvenue, Président du CEP. Vous pouvez gérer les candidats ci-dessous.",
        "admin_candidate_list": "📋 Candidats actuels",
        "admin_id": "ID",
        "admin_name": "Nom",
        "admin_party": "Parti",
        "admin_slogan": "Devise",
        "admin_votes": "Votes",
        "admin_symbol": "Symbole",
        "admin_update_symbol": "✏️ Mettre à jour le symbole",
        "admin_delete": "🗑️ Supprimer",
        "admin_new_symbol_url": "Nouvelle URL d'image (ou déposer un fichier ci-dessous)",
        "admin_upload_image": "Ou déposer une image (JPEG/PNG)",
        "admin_update_btn": "Mettre à jour",
        "admin_delete_confirm": "Voulez-vous vraiment supprimer ce candidat ? Cette action est irréversible et supprimera tous ses votes.",
        "admin_delete_btn": "Oui, supprimer",
        "admin_add_candidate": "➕ Ajouter un candidat",
        "admin_name_en": "Nom (anglais)",
        "admin_name_fr": "Nom (français)",
        "admin_name_es": "Nom (espagnol)",
        "admin_name_ht": "Nom (kreyòl)",
        "admin_party_en": "Parti (anglais)",
        "admin_party_fr": "Parti (français)",
        "admin_party_es": "Parti (espagnol)",
        "admin_party_ht": "Parti (kreyòl)",
        "admin_slogan_en": "Devise (anglais)",
        "admin_slogan_fr": "Devise (français)",
        "admin_slogan_es": "Devise (espagnol)",
        "admin_slogan_ht": "Devise (kreyòl)",
        "admin_symbol_url": "URL de l'image du candidat (ou déposer fichier)",
        "admin_upload_symbol": "Déposer une image",
        "admin_add_btn": "Ajouter",
        "admin_add_success": "Candidat ajouté avec succès !",
        "admin_update_success": "Symbole mis à jour !",
        "admin_delete_success": "Candidat supprimé !",
        "admin_error": "Une erreur est survenue.",
        "live_monitoring": "📡 Surveillance en direct du vote",
        "current_leader": "🏅 Leader actuel",
        "total_votes_cast": "🗳️ Total des votes exprimés",
        "neutral_votes": "⚪ Votes neutres",
        "quick_report": "📄 Télécharger le rapport de progression (PDF)",
        "last_refresh": "Dernier rafraîchissement",
        "refresh_button": "🔄 Actualiser les résultats",
        "election_end_time": "L'élection se termine à",
        "current_time": "Heure actuelle du serveur",
        "detailed_votes": "🔍 Détail des votes (anonymisé)",
        "voter_id_col": "ID votant (haché)",
        "candidate_voted": "Candidat choisi",
        "department_col": "Département",
        "timestamp_col": "Horodatage",
        "company_name": "GlobalInternet.py",
        "company_owner": "Propriétaire: Gesner Deslandes",
        "company_contact": "Contact: (509)-47385663",
        "company_email": "Courriel: deslandes78@gmail.com",
        "company_rights": "Tous droits réservés - Licence propriétaire",
        "company_sale": "Ce logiciel est à vendre : 2 000 $ US pour des élections présidentielles en ligne.",
        "company_note": "Quand vous serez prêts à expérimenter ce processus en ligne, contactez-nous.",
        "change_password": "🔐 Changer les mots de passe",
        "change_app_password": "Changer le mot de passe de l'application (actuel: caché)",
        "change_private_password": "Changer le mot de passe de la section privée (actuel: caché)",
        "new_password": "Nouveau mot de passe",
        "confirm_password": "Confirmer le nouveau mot de passe",
        "request_code": "Demander un code de vérification",
        "verification_code": "Entrez le code à 6 chiffres",
        "submit_change": "Changer le mot de passe",
        "code_sent": "Un code de vérification a été envoyé à votre adresse e-mail (simulé). Code : {code}",
        "code_mismatch": "Code de vérification invalide.",
        "password_mismatch": "Les mots de passe ne correspondent pas.",
        "password_changed": "Mot de passe changé avec succès !",
        "email_placeholder": "Votre adresse e-mail",
        "change_logout": "Déconnexion du tableau de bord CEP",
        "login_title": "Connexion Président du CEP",
        "login_subtitle": "Entrez vos identifiants pour accéder au système de vote",
        "app_password_label": "Mot de passe application (défaut: 20082010)",
        "login_button": "Se connecter",
        "wrong_app_password": "Mot de passe incorrect. Accès refusé."
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
        "private_password": "Ingrese la contraseña privada del CEP",
        "private_results": "Resultados confidenciales – Solo para uso del CEP",
        "invalid_password": "Contraseña incorrecta. Acceso denegado.",
        "footer": "© 2026 GlobalInternet.py – Hecho en Haití",
        "choose_candidate": "Elija su candidato",
        "vote_for": "Votar por",
        "not_specified": "No especificado",
        "admin_dashboard": "👑 Panel del Presidente del CEP",
        "admin_welcome": "Bienvenido, Presidente del CEP. Puede gestionar los candidatos abajo.",
        "admin_candidate_list": "📋 Candidatos actuales",
        "admin_id": "ID",
        "admin_name": "Nombre",
        "admin_party": "Partido",
        "admin_slogan": "Lema",
        "admin_votes": "Votos",
        "admin_symbol": "Símbolo",
        "admin_update_symbol": "✏️ Actualizar símbolo",
        "admin_delete": "🗑️ Eliminar",
        "admin_new_symbol_url": "Nueva URL de imagen (o subir archivo abajo)",
        "admin_upload_image": "O subir una imagen (JPEG/PNG)",
        "admin_update_btn": "Actualizar",
        "admin_delete_confirm": "¿Está seguro de eliminar este candidato? Se eliminarán también todos sus votos.",
        "admin_delete_btn": "Sí, eliminar",
        "admin_add_candidate": "➕ Agregar candidato",
        "admin_name_en": "Nombre (inglés)",
        "admin_name_fr": "Nombre (francés)",
        "admin_name_es": "Nombre (español)",
        "admin_name_ht": "Nombre (kreyòl)",
        "admin_party_en": "Partido (inglés)",
        "admin_party_fr": "Partido (francés)",
        "admin_party_es": "Partido (español)",
        "admin_party_ht": "Partido (kreyòl)",
        "admin_slogan_en": "Lema (inglés)",
        "admin_slogan_fr": "Lema (francés)",
        "admin_slogan_es": "Lema (español)",
        "admin_slogan_ht": "Lema (kreyòl)",
        "admin_symbol_url": "URL de la imagen del candidato (o subir archivo)",
        "admin_upload_symbol": "Subir imagen",
        "admin_add_btn": "Agregar",
        "admin_add_success": "¡Candidato agregado!",
        "admin_update_success": "¡Símbolo actualizado!",
        "admin_delete_success": "¡Candidato eliminado!",
        "admin_error": "Ocurrió un error.",
        "live_monitoring": "📡 Monitoreo en vivo de la votación",
        "current_leader": "🏅 Líder actual",
        "total_votes_cast": "🗳️ Total de votos emitidos",
        "neutral_votes": "⚪ Votos neutrales",
        "quick_report": "📄 Descargar informe de progreso (PDF)",
        "last_refresh": "Última actualización",
        "refresh_button": "🔄 Actualizar resultados",
        "election_end_time": "La elección termina a las",
        "current_time": "Hora actual del servidor",
        "detailed_votes": "🔍 Votos detallados (anonimizados)",
        "voter_id_col": "ID votante (hash)",
        "candidate_voted": "Candidato votado",
        "department_col": "Departamento",
        "timestamp_col": "Marca de tiempo",
        "company_name": "GlobalInternet.py",
        "company_owner": "Propietario: Gesner Deslandes",
        "company_contact": "Contacto: (509)-47385663",
        "company_email": "Correo: deslandes78@gmail.com",
        "company_rights": "Todos los derechos reservados - Licencia privada",
        "company_sale": "Este software está en venta: $2,000 USD para elecciones presidenciales en línea.",
        "company_note": "Cuando estén listos para experimentar este proceso en línea, contáctenos.",
        "change_password": "🔐 Cambiar contraseñas",
        "change_app_password": "Cambiar contraseña de acceso a la app (actual: oculta)",
        "change_private_password": "Cambiar contraseña de sección privada (actual: oculta)",
        "new_password": "Nueva contraseña",
        "confirm_password": "Confirmar nueva contraseña",
        "request_code": "Solicitar código de verificación",
        "verification_code": "Ingrese código de 6 dígitos",
        "submit_change": "Cambiar contraseña",
        "code_sent": "Se ha enviado un código de verificación a su correo (simulado). Código: {code}",
        "code_mismatch": "Código de verificación inválido.",
        "password_mismatch": "Las contraseñas no coinciden.",
        "password_changed": "¡Contraseña cambiada exitosamente!",
        "email_placeholder": "Su correo electrónico",
        "change_logout": "Cerrar sesión del panel CEP",
        "login_title": "Inicio de sesión Presidente del CEP",
        "login_subtitle": "Ingrese sus credenciales para acceder al sistema de votación",
        "app_password_label": "Contraseña de aplicación (predeterminada: 20082010)",
        "login_button": "Iniciar sesión",
        "wrong_app_password": "Contraseña incorrecta. Acceso denegado."
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
        "private_password": "Antre modpas prive CEP la",
        "private_results": "Rezilta konfidansyèl – Sèlman pou itilizasyon CEP",
        "invalid_password": "Modpas pa bon. Aksè refize.",
        "footer": "© 2026 GlobalInternet.py – Fèt an Ayiti",
        "choose_candidate": "Chwazi kandida w",
        "vote_for": "Vote pou",
        "not_specified": "Pa espesifye",
        "admin_dashboard": "👑 Tablodbò Prezidan CEP la",
        "admin_welcome": "Byenveni, Prezidan CEP la. Ou ka jere kandida yo anba a.",
        "admin_candidate_list": "📋 Kandida aktyèl yo",
        "admin_id": "ID",
        "admin_name": "Non",
        "admin_party": "Patri",
        "admin_slogan": "Deviz",
        "admin_votes": "Vòt",
        "admin_symbol": "Senbòl",
        "admin_update_symbol": "✏️ Mete ajou senbòl",
        "admin_delete": "🗑️ Efase",
        "admin_new_symbol_url": "Nouvo URL imaj (oswa telechaje yon fichye anba a)",
        "admin_upload_image": "Oswa telechaje yon fichye imaj (JPEG/PNG)",
        "admin_update_btn": "Mete ajou",
        "admin_delete_confirm": "Èske w sèten w vle efase kandida sa a? Aksyon sa a pap ka anile epi l ap efase tout vòt li yo.",
        "admin_delete_btn": "Wi, efase kandida",
        "admin_add_candidate": "➕ Ajoute yon kandida",
        "admin_name_en": "Non (angle)",
        "admin_name_fr": "Non (fransè)",
        "admin_name_es": "Non (espanyòl)",
        "admin_name_ht": "Non (kreyòl)",
        "admin_party_en": "Patri (angle)",
        "admin_party_fr": "Patri (fransè)",
        "admin_party_es": "Patri (espanyòl)",
        "admin_party_ht": "Patri (kreyòl)",
        "admin_slogan_en": "Deviz (angle)",
        "admin_slogan_fr": "Deviz (fransè)",
        "admin_slogan_es": "Deviz (espanyòl)",
        "admin_slogan_ht": "Deviz (kreyòl)",
        "admin_symbol_url": "URL imaj kandida a (oswa telechaje fichye)",
        "admin_upload_symbol": "Telechaje imaj",
        "admin_add_btn": "Ajoute",
        "admin_add_success": "Kandida ajoute avèk siksè!",
        "admin_update_success": "Senbòl mete ajou!",
        "admin_delete_success": "Kandida efase!",
        "admin_error": "Yon erè te rive.",
        "live_monitoring": "📡 Siveyans vòt an dirè",
        "current_leader": "🏅 Moun ki gen plis vòt kounye a",
        "total_votes_cast": "🗳️ Total vòt yo",
        "neutral_votes": "⚪ Vòt net",
        "quick_report": "📄 Telechaje rapò pwogrè (PDF)",
        "last_refresh": "Dènye rafrechisman",
        "refresh_button": "🔄 Rafrechi rezilta yo",
        "election_end_time": "Eleksyon an fini a",
        "current_time": "Lè aktyèl serve a",
        "detailed_votes": "🔍 Detay vòt (anonim)",
        "voter_id_col": "ID votan (hash)",
        "candidate_voted": "Kandida vote",
        "department_col": "Depatman",
        "timestamp_col": "Dat/ Lè",
        "company_name": "GlobalInternet.py",
        "company_owner": "Pwopriyetè: Gesner Deslandes",
        "company_contact": "Kontak: (509)-47385663",
        "company_email": "Imèl: deslandes78@gmail.com",
        "company_rights": "Tout dwa rezève - Lisans pwopriyetè",
        "company_sale": "Lojisyèl sa a ap vann: $2,000 USD pou eleksyon prezidansyèl sou entènèt.",
        "company_note": "Lè nou pare pou fè eksperyans pwosesis sa a sou entènèt, kontakte nou.",
        "change_password": "🔐 Chanje modpas yo",
        "change_app_password": "Chanje modpas koneksyon aplikasyon an (aktyèl: kache)",
        "change_private_password": "Chanje modpas seksyon prive a (aktyèl: kache)",
        "new_password": "Nouvo modpas",
        "confirm_password": "Konfime nouvo modpas",
        "request_code": "Mande yon kòd verifikasyon",
        "verification_code": "Antre kòd 6 chif yo",
        "submit_change": "Chanje modpas",
        "code_sent": "Yon kòd verifikasyon te voye nan imèl ou (simile). Kòd: {code}",
        "code_mismatch": "Kòd verifikasyon pa bon.",
        "password_mismatch": "Modpas yo pa matche.",
        "password_changed": "Modpas chanje avèk siksè!",
        "email_placeholder": "Adrès imèl ou",
        "change_logout": "Dekonekte tablodbò CEP",
        "login_title": "Koneksyon Prezidan CEP",
        "login_subtitle": "Antre enfòmasyon ou pou aksè sistèm vòt la",
        "app_password_label": "Modpas aplikasyon (default: 20082010)",
        "login_button": "Konekte",
        "wrong_app_password": "Modpas pa bon. Aksè refize."
    }
}

# -----------------------------
# Password management (config.json)
# -----------------------------
CONFIG_FILE = "config.json"

def load_passwords():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("app_password", "20082010"), config.get("private_password", "18032026")
    else:
        config = {"app_password": "20082010", "private_password": "18032026"}
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
        return "20082010", "18032026"

def save_passwords(app_pwd, private_pwd):
    config = {"app_password": app_pwd, "private_password": private_pwd}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# -----------------------------
# Database functions (unchanged)
# -----------------------------
def init_db():
    conn = sqlite3.connect("election.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_en TEXT,
        name_fr TEXT,
        name_es TEXT,
        name_ht TEXT,
        party_en TEXT,
        party_fr TEXT,
        party_es TEXT,
        party_ht TEXT,
        slogan_en TEXT,
        slogan_fr TEXT,
        slogan_es TEXT,
        slogan_ht TEXT,
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

def migrate_db():
    conn = sqlite3.connect("election.db")
    c = conn.cursor()
    c.execute("PRAGMA table_info(candidates)")
    existing = [col[1] for col in c.fetchall()]
    required = ["name_en", "name_fr", "name_es", "name_ht",
                "party_en", "party_fr", "party_es", "party_ht",
                "slogan_en", "slogan_fr", "slogan_es", "slogan_ht"]
    for col in required:
        if col not in existing:
            c.execute(f"ALTER TABLE candidates ADD COLUMN {col} TEXT")
    conn.commit()
    conn.close()

def add_candidate(name_en, name_fr, name_es, name_ht, party_en, party_fr, party_es, party_ht, slogan_en, slogan_fr, slogan_es, slogan_ht, symbol):
    conn = sqlite3.connect("election.db")
    c = conn.cursor()
    c.execute("""INSERT INTO candidates 
        (name_en, name_fr, name_es, name_ht, party_en, party_fr, party_es, party_ht, slogan_en, slogan_fr, slogan_es, slogan_ht, symbol, votes) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,0)""",
        (name_en, name_fr, name_es, name_ht, party_en, party_fr, party_es, party_ht, slogan_en, slogan_fr, slogan_es, slogan_ht, symbol))
    conn.commit()
    conn.close()

def update_candidate_symbol(candidate_id, new_symbol):
    conn = sqlite3.connect("election.db")
    c = conn.cursor()
    c.execute("UPDATE candidates SET symbol = ? WHERE id = ?", (new_symbol, candidate_id))
    conn.commit()
    conn.close()

def delete_candidate(candidate_id):
    conn = sqlite3.connect("election.db")
    c = conn.cursor()
    c.execute("DELETE FROM votes WHERE candidate_id = ?", (candidate_id,))
    c.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
    conn.commit()
    conn.close()

def get_all_candidates_admin():
    conn = sqlite3.connect("election.db")
    df = pd.read_sql_query("SELECT id, name_en, name_fr, name_es, name_ht, party_en, party_fr, party_es, party_ht, slogan_en, slogan_fr, slogan_es, slogan_ht, symbol, votes FROM candidates ORDER BY id", conn)
    conn.close()
    return df

def get_candidates(lang):
    conn = sqlite3.connect("election.db")
    df = pd.read_sql_query("SELECT id, name_en, name_fr, name_es, name_ht, party_en, party_fr, party_es, party_ht, slogan_en, slogan_fr, slogan_es, slogan_ht, symbol, votes FROM candidates ORDER BY id", conn)
    conn.close()
    df["name"] = df[f"name_{lang}"].fillna(lang_dict[lang]["not_specified"])
    df["party"] = df[f"party_{lang}"].fillna(lang_dict[lang]["not_specified"])
    df["slogan"] = df[f"slogan_{lang}"].fillna(lang_dict[lang]["not_specified"])
    return df[["id", "name", "party", "slogan", "symbol", "votes"]]

def record_vote(voter_id, department, candidate_id):
    hashed = hashlib.sha256(voter_id.encode()).hexdigest()
    conn = sqlite3.connect("election.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO votes (voter_id, department, candidate_id, timestamp) VALUES (?,?,?,?)",
                  (hashed, department, candidate_id, datetime.datetime.now().isoformat()))
        if candidate_id != -1:
            c.execute("UPDATE candidates SET votes = votes + 1 WHERE id = ?", (candidate_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def has_voted(voter_id):
    hashed = hashlib.sha256(voter_id.encode()).hexdigest()
    conn = sqlite3.connect("election.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM votes WHERE voter_id = ?", (hashed,))
    result = c.fetchone()
    conn.close()
    return result is not None

def get_results(lang):
    conn = sqlite3.connect("election.db")
    df = pd.read_sql_query("SELECT id, name_en, name_fr, name_es, name_ht, party_en, party_fr, party_es, party_ht, slogan_en, slogan_fr, slogan_es, slogan_ht, votes FROM candidates ORDER BY votes DESC", conn)
    conn.close()
    df["name"] = df[f"name_{lang}"].fillna(lang_dict[lang]["not_specified"])
    df["party"] = df[f"party_{lang}"].fillna(lang_dict[lang]["not_specified"])
    df["slogan"] = df[f"slogan_{lang}"].fillna(lang_dict[lang]["not_specified"])
    return df[["name", "party", "slogan", "votes"]]

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

def get_detailed_votes():
    conn = sqlite3.connect("election.db")
    query = """
        SELECT v.voter_id, v.department, v.timestamp, 
               CASE 
                   WHEN v.candidate_id = -1 THEN 'Neutral'
                   ELSE c.name_en 
               END as candidate_name
        FROM votes v
        LEFT JOIN candidates c ON v.candidate_id = c.id
        ORDER BY v.timestamp DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def generate_report(results_df, neutral_votes, total_votes, winner_name, winner_votes, lang, title_suffix=""):
    t = lang_dict[lang]
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"{t['title']} {title_suffix}", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"{t['winner_text']} {winner_name} ({winner_votes} {t['votes_count']})", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(t["results_title"], styles['Heading3']))
    story.append(Spacer(1, 6))

    data = [[t["candidate_col"], t["party_col"], t["votes_col"], t["slogan_col"]]]
    for _, row in results_df.iterrows():
        data.append([row["name"], row["party"], str(row["votes"]), row["slogan"]])
    data.append([t["neutral"], "-", str(neutral_votes), "-"])
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
# Helper to save uploaded image
# -----------------------------
def save_uploaded_image(uploaded_file):
    if uploaded_file is not None:
        os.makedirs("candidate_images", exist_ok=True)
        ext = uploaded_file.name.split('.')[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join("candidate_images", filename)
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return filepath
    return None

# -----------------------------
# Demo candidates with HAITIAN images
# -----------------------------
def generate_demo_candidates():
    conn = sqlite3.connect("election.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM candidates")
    count = c.fetchone()[0]
    conn.close()
    if count == 0:
        candidates = [
            ("Jean-Claude Pierre", "Jean-Claude Pierre", "Jean-Claude Pierre", "Jean-Claude Pierre",
             "Unity Party", "Parti de l'Unité", "Partido de la Unidad", "Patri Inite",
             "For a united Haiti", "Pour un Haïti uni", "Por un Haití unido", "Pou yon Ayiti ini",
             "https://images.pexels.com/photos/2380796/pexels-photo-2380796.jpeg?auto=compress&cs=tinysrgb&w=400"),
            ("Marie-Louise Duval", "Marie-Louise Duval", "Marie-Louise Duval", "Marie-Louise Duval",
             "Hope Alliance", "Alliance Espoir", "Alianza Esperanza", "Ayans Espwa",
             "Hope for tomorrow", "L'espoir pour demain", "Esperanza para mañana", "Espwa pou demen",
             "https://images.pexels.com/photos/2380794/pexels-photo-2380794.jpeg?auto=compress&cs=tinysrgb&w=400"),
            ("Joseph Bernard", "Joseph Bernard", "Joseph Bernard", "Joseph Bernard",
             "Liberty Movement", "Mouvement Liberté", "Movimiento Libertad", "Mouvman Libète",
             "Freedom and justice", "Liberté et justice", "Libertad y justicia", "Libète ak jistis",
             "https://images.pexels.com/photos/3772629/pexels-photo-3772629.jpeg?auto=compress&cs=tinysrgb&w=400"),
            ("Anne-Sophie Michel", "Anne-Sophie Michel", "Anne-Sophie Michel", "Anne-Sophie Michel",
             "Green Leaf Party", "Parti Feuille Verte", "Partido Hoja Verde", "Patri Fey Vèt",
             "Ecology and progress", "Écologie et progrès", "Ecología y progreso", "Ekoloji ak pwogrè",
             "https://images.pexels.com/photos/2773895/pexels-photo-2773895.jpeg?auto=compress&cs=tinysrgb&w=400"),
            ("Luc Saint-Vil", "Luc Saint-Vil", "Luc Saint-Vil", "Luc Saint-Vil",
             "Peasant Front", "Front Paysan", "Frente Campesino", "Front Peyizan",
             "Land for all", "La terre pour tous", "Tierra para todos", "Tè pou tout moun",
             "https://images.pexels.com/photos/2552134/pexels-photo-2552134.jpeg?auto=compress&cs=tinysrgb&w=400"),
            ("Michele Delatour", "Michele Delatour", "Michele Delatour", "Michele Delatour",
             "Women's Power", "Pouvoir des Femmes", "Poder de la Mujer", "Pouvwa Fanm",
             "Strength in unity", "La force dans l'unité", "Fuerza en la unidad", "Fòs nan inite",
             "https://images.pexels.com/photos/4320592/pexels-photo-4320592.jpeg?auto=compress&cs=tinysrgb&w=400"),
            ("Pierre Richard", "Pierre Richard", "Pierre Richard", "Pierre Richard",
             "Workers' Party", "Parti des Travailleurs", "Partido de los Trabajadores", "Patri Travayè",
             "Dignity through work", "Dignité par le travail", "Dignidad a través del trabajo", "Diyite atravè travay",
             "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=400"),
            ("Claudette Jean", "Claudette Jean", "Claudette Jean", "Claudette Jean",
             "Education First", "Éducation d'abord", "Educación Primero", "Edikasyon an premye",
             "Knowledge is power", "Le savoir est pouvoir", "El conocimiento es poder", "Konesans se pouvwa",
             "https://images.pexels.com/photos/3825267/pexels-photo-3825267.jpeg?auto=compress&cs=tinysrgb&w=400"),
            ("Emmanuel Charles", "Emmanuel Charles", "Emmanuel Charles", "Emmanuel Charles",
             "New Deal", "Nouvelle Donne", "Nuevo Trato", "Nouvo Kontra",
             "A new beginning", "Un nouveau départ", "Un nuevo comienzo", "Yon nouvo kòmansman",
             "https://images.pexels.com/photos/2380790/pexels-photo-2380790.jpeg?auto=compress&cs=tinysrgb&w=400"),
            ("Rosemie Baptiste", "Rosemie Baptiste", "Rosemie Baptiste", "Rosemie Baptiste",
             "Social Justice", "Justice Sociale", "Justicia Social", "Jistis Sosyal",
             "Equality for all", "Égalité pour tous", "Igualdad para todos", "Egalite pou tout moun",
             "https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=400")
        ]
        for cand in candidates:
            add_candidate(*cand)

# -----------------------------
# Election deadline
# -----------------------------
def get_election_deadline():
    if "deadline" not in st.session_state:
        st.session_state.deadline = datetime.datetime.now() + datetime.timedelta(minutes=5)
    return st.session_state.deadline

def is_election_over():
    return datetime.datetime.now() >= get_election_deadline()

# -----------------------------
# Admin Dashboard (with password change)
# -----------------------------
def admin_dashboard(t, lang, current_app_pwd, current_private_pwd):
    st.markdown(f"## {t['admin_dashboard']}")
    st.info(t['admin_welcome'])

    # ---- LIVE MONITORING ----
    st.markdown(f"### {t['live_monitoring']}")
    col1, col2 = st.columns(2)
    with col1:
        results_live = get_results(lang)
        total_votes_live = get_total_votes()
        neutral_votes_live = get_neutral_votes()
        total_cast = total_votes_live + neutral_votes_live
        
        if not results_live.empty:
            leader = results_live.iloc[0]
            leader_name = leader["name"]
            leader_votes = leader["votes"]
            st.metric(t['current_leader'], f"{leader_name} – {leader_votes} {t['votes_count']}")
        else:
            st.metric(t['current_leader'], "No candidates")
        
        st.metric(t['total_votes_cast'], total_cast)
        st.metric(t['neutral_votes'], neutral_votes_live)
        
        deadline = get_election_deadline()
        now = datetime.datetime.now()
        st.write(f"**{t['election_end_time']}:** {deadline.strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**{t['current_time']}:** {now.strftime('%Y-%m-%d %H:%M:%S')}")
        if not is_election_over():
            remaining = deadline - now
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            seconds = remaining.seconds % 60
            st.info(f"{t['time_remaining']}: {hours:02d}h {minutes:02d}m {seconds:02d}s")
        else:
            st.warning(t['election_over'])
    
    with col2:
        if not results_live.empty:
            report_buffer = generate_report(results_live, neutral_votes_live, total_cast, leader_name, leader_votes, lang, title_suffix="(Progress Report)")
            st.download_button(
                t['quick_report'],
                data=report_buffer,
                file_name=f"progress_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
            st.caption(f"{t['last_refresh']}: {datetime.datetime.now().strftime('%H:%M:%S')}")
            if st.button(t['refresh_button']):
                st.rerun()
    
    if not results_live.empty:
        st.markdown("#### Current vote distribution")
        chart_data = results_live.set_index("name")["votes"]
        st.bar_chart(chart_data)
    
    st.divider()

    # ---- DETAILED VOTES ----
    st.markdown(f"### {t['detailed_votes']}")
    detailed_df = get_detailed_votes()
    if not detailed_df.empty:
        detailed_df_display = detailed_df.rename(columns={
            "voter_id": t['voter_id_col'],
            "department": t['department_col'],
            "timestamp": t['timestamp_col'],
            "candidate_name": t['candidate_voted']
        })
        st.dataframe(detailed_df_display)
        st.caption("Note: Voter IDs are hashed (SHA-256) to ensure anonymity. No personal information is stored.")
    else:
        st.write("No votes have been cast yet.")
    
    st.divider()

    # ---- PASSWORD CHANGE ----
    st.markdown(f"### {t['change_password']}")
    with st.expander(t['change_app_password']):
        email = st.text_input(t['email_placeholder'], value="deslandes78@gmail.com", key="app_email")
        new_pwd = st.text_input(t['new_password'], type="password", key="new_app_pwd")
        confirm_pwd = st.text_input(t['confirm_password'], type="password", key="confirm_app_pwd")
        if st.button(t['request_code'], key="req_app_code"):
            code = str(random.randint(100000, 999999))
            st.session_state.app_verification_code = code
            st.info(t['code_sent'].format(code=code))
        verif_code = st.text_input(t['verification_code'], key="app_verif")
        if st.button(t['submit_change'], key="change_app"):
            if verif_code != st.session_state.get("app_verification_code", ""):
                st.error(t['code_mismatch'])
            elif new_pwd != confirm_pwd:
                st.error(t['password_mismatch'])
            else:
                save_passwords(new_pwd, current_private_pwd)
                st.success(t['password_changed'])
                st.rerun()
    
    with st.expander(t['change_private_password']):
        email2 = st.text_input(t['email_placeholder'], value="deslandes78@gmail.com", key="private_email")
        new_pwd2 = st.text_input(t['new_password'], type="password", key="new_private_pwd")
        confirm_pwd2 = st.text_input(t['confirm_password'], type="password", key="confirm_private_pwd")
        if st.button(t['request_code'], key="req_private_code"):
            code2 = str(random.randint(100000, 999999))
            st.session_state.private_verification_code = code2
            st.info(t['code_sent'].format(code=code2))
        verif_code2 = st.text_input(t['verification_code'], key="private_verif")
        if st.button(t['submit_change'], key="change_private"):
            if verif_code2 != st.session_state.get("private_verification_code", ""):
                st.error(t['code_mismatch'])
            elif new_pwd2 != confirm_pwd2:
                st.error(t['password_mismatch'])
            else:
                save_passwords(current_app_pwd, new_pwd2)
                st.success(t['password_changed'])
                st.rerun()
    st.divider()

    # ---- ADD CANDIDATE ----
    with st.expander(t['admin_add_candidate']):
        with st.form("add_candidate_form"):
            col1, col2 = st.columns(2)
            with col1:
                name_en = st.text_input(t['admin_name_en'])
                name_fr = st.text_input(t['admin_name_fr'])
                name_es = st.text_input(t['admin_name_es'])
                name_ht = st.text_input(t['admin_name_ht'])
                party_en = st.text_input(t['admin_party_en'])
                party_fr = st.text_input(t['admin_party_fr'])
                party_es = st.text_input(t['admin_party_es'])
                party_ht = st.text_input(t['admin_party_ht'])
            with col2:
                slogan_en = st.text_input(t['admin_slogan_en'])
                slogan_fr = st.text_input(t['admin_slogan_fr'])
                slogan_es = st.text_input(t['admin_slogan_es'])
                slogan_ht = st.text_input(t['admin_slogan_ht'])
                symbol_url = st.text_input(t['admin_symbol_url'])
                uploaded_img = st.file_uploader(t['admin_upload_symbol'], type=["jpg", "jpeg", "png"])
            
            submitted = st.form_submit_button(t['admin_add_btn'])
            if submitted:
                symbol = symbol_url if symbol_url else ""
                if uploaded_img:
                    saved_path = save_uploaded_image(uploaded_img)
                    if saved_path:
                        symbol = saved_path
                if name_en and name_fr and name_es and name_ht:
                    add_candidate(name_en, name_fr, name_es, name_ht,
                                  party_en, party_fr, party_es, party_ht,
                                  slogan_en, slogan_fr, slogan_es, slogan_ht,
                                  symbol)
                    st.success(t['admin_add_success'])
                    st.rerun()
                else:
                    st.error("At least the name in all four languages is required.")

    # ---- LIST CANDIDATES ----
    st.subheader(t['admin_candidate_list'])
    df_admin = get_all_candidates_admin()
    if df_admin.empty:
        st.write("No candidates found.")
        return

    for idx, row in df_admin.iterrows():
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
            with col1:
                try:
                    st.image(row["symbol"], width=80)
                except:
                    st.image("https://via.placeholder.com/80?text=No+Image", width=80)
            with col2:
                st.markdown(f"**{row['name_en']}** (ID: {row['id']})")
                st.caption(f"Party: {row['party_en']}")
                st.caption(f"Slogan: {row['slogan_en']}")
                st.caption(f"Votes: {row['votes']}")
            with col3:
                st.markdown(f"**{t['admin_update_symbol']}**")
                new_url = st.text_input(t['admin_new_symbol_url'], key=f"url_{row['id']}")
                uploaded_file = st.file_uploader(t['admin_upload_image'], type=["jpg","jpeg","png"], key=f"upload_{row['id']}")
                if st.button(t['admin_update_btn'], key=f"update_{row['id']}"):
                    new_symbol = new_url if new_url else row['symbol']
                    if uploaded_file:
                        saved = save_uploaded_image(uploaded_file)
                        if saved:
                            new_symbol = saved
                    update_candidate_symbol(row['id'], new_symbol)
                    st.success(t['admin_update_success'])
                    st.rerun()
            with col4:
                if st.button(t['admin_delete'], key=f"del_{row['id']}"):
                    st.warning(t['admin_delete_confirm'])
                    if st.button(t['admin_delete_btn'], key=f"confirm_del_{row['id']}"):
                        delete_candidate(row['id'])
                        st.success(t['admin_delete_success'])
                        st.rerun()
            st.divider()

# -----------------------------
# Login screen
# -----------------------------
def login_screen(t):
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: auto;
            padding: 2rem;
            border-radius: 10px;
            background-color: #f9f9f9;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.image("https://flagcdn.com/w320/ht.png", width=100)
    st.markdown(f"## {t['login_title']}")
    st.markdown(f"### {t['title']}")
    st.markdown(f"*{t['login_subtitle']}*")
    pwd = st.text_input(t['app_password_label'], type="password")
    if st.button(t['login_button']):
        current_app, _ = load_passwords()
        if pwd == current_app:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error(t['wrong_app_password'])
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Main app
# -----------------------------
init_db()
migrate_db()
generate_demo_candidates()

# Language selector (visible even before login)
lang = st.sidebar.selectbox("🌐 Language", options=["en", "fr", "es", "ht"], format_func=lambda x: {"en":"English","fr":"Français","es":"Español","ht":"Kreyòl"}[x])
t = lang_dict[lang]

# Check authentication
if not st.session_state.get("authenticated", False):
    login_screen(t)
    st.stop()

# -----------------------------
# Authenticated user sees the full app
# -----------------------------

# Sidebar company info
st.sidebar.image("https://flagcdn.com/w320/ht.png", width=80)
st.sidebar.markdown(f"### {t['company_name']}")
st.sidebar.markdown(f"**{t['company_owner']}**")
st.sidebar.markdown(f"{t['company_contact']}")
st.sidebar.markdown(f"{t['company_email']}")
st.sidebar.markdown(f"*{t['company_rights']}*")
st.sidebar.markdown("---")
st.sidebar.markdown(f"💰 **{t['company_sale']}**")
st.sidebar.markdown(f"📢 {t['company_note']}")

# Main title and flag
col_title, col_flag = st.columns([3, 1])
with col_title:
    st.title(t["title"])
    st.markdown(f"### {t['subtitle']}")
with col_flag:
    st.image("https://flagcdn.com/w320/ht.png", width=120)

# Election deadline
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

# Voting interface (public)
voter_id = st.session_state.get("voter_id", None)
if voter_id is None:
    voter_id = str(uuid.uuid4())
    st.session_state.voter_id = voter_id

if has_voted(voter_id):
    st.warning(t["already_voted"])
elif is_election_over():
    st.error(t["election_over"])
else:
    col1, col2 = st.columns([2,1])
    with col1:
        department = st.selectbox(t["select_dept"], t["departments"])
    with col2:
        st.write("")
        st.write("")
        neutral_vote = st.checkbox(t["neutral"])

    candidates_df = get_candidates(lang)
    if not neutral_vote:
        st.subheader(t["choose_candidate"])
        cols = st.columns(3)
        for idx, row in candidates_df.iterrows():
            with cols[idx % 3]:
                try:
                    st.image(row["symbol"], width=100)
                except:
                    st.image("https://via.placeholder.com/100?text=No+Image", width=100)
                st.markdown(f"**{row['name']}**")
                st.caption(row["party"])
                st.caption(f"*{row['slogan']}*")
                if st.button(f"{t['vote_for']} {row['name']}", key=f"vote_{row['id']}"):
                    if record_vote(voter_id, department, row["id"]):
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

# Results after election
if is_election_over():
    st.markdown("---")
    st.header("📊 Election Results")
    results_df = get_results(lang)
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

        report_buffer = generate_report(results_df, neutral_votes, total_votes, winner_name, winner_votes, lang, title_suffix="(Final)")
        st.download_button(t["download_report"], data=report_buffer, file_name=f"election_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", mime="application/pdf")

# Private section (requires separate private password)
st.markdown("---")
with st.expander(t["private_section"]):
    st.markdown("---")
    st.info("""
    **Message from GlobalInternet.py:**  
    J'ai développé ce logiciel pour le gouvernement haïtien et il est à vendre à 2 000 $ US pour des élections présidentielles en ligne.  
    Quand ils seront prêts à expérimenter ce processus en ligne, chez GlobalInternet.py nous construisons des logiciels avec Python.  
    2 codes / Coordonnées : (509)-47385663 / courriel : deslandes78@gmail.com / Avril 2026
    """)
    private_pwd_input = st.text_input(t["private_password"], type="password")
    if st.button("Access Private Section"):
        _, current_private = load_passwords()
        if private_pwd_input == current_private:
            st.session_state.admin_auth = True
            st.rerun()
        else:
            st.error(t["invalid_password"])

# Show admin dashboard if private section unlocked
if st.session_state.get("admin_auth", False):
    current_app, current_private = load_passwords()
    admin_dashboard(t, lang, current_app, current_private)
    if st.button(t['change_logout']):
        st.session_state.admin_auth = False
        st.rerun()

st.markdown("---")
st.markdown(f"<center>{t['footer']}<br>{t['company_name']} – {t['company_owner']} – {t['company_contact']}</center>", unsafe_allow_html=True)

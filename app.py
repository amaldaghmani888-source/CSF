import streamlit as st
import pandas as pd
from datetime import date
from database import (
    init_db, add_patient, get_patients, get_patient, add_record,
    get_records, add_appointment, get_appointments, add_document,
    get_documents, add_screening, get_screenings
)

st.set_page_config(page_title="CSF Numérique", page_icon="🌸", layout="wide")
init_db()

T = {
    "fr": {
        "app":"CSF NUMÉRIQUE", "tag":"Carnet de Santé de la Femme",
        "language":"Langue", "role":"Espace", "woman":"Espace Femme",
        "doctor":"Médecin", "midwife":"Sage-femme", "nurse":"Infirmier / Infirmière",
        "admin":"Administration", "home":"Tableau de bord", "patients":"Patientes",
        "new_patient":"Nouveau dossier", "medical":"Dossier médical",
        "consult":"Consultation", "pregnancy":"Suivi de grossesse",
        "vaccines":"Vaccinations", "screening":"Dépistages",
        "appointments":"Rendez-vous", "documents":"Documents",
        "welcome":"Bienvenue dans votre carnet de santé",
        "select_patient":"Sélectionner une patiente", "no_patient":"Aucun dossier. Créez d'abord une patiente.",
        "name":"Nom", "first":"Prénom", "dob":"Date de naissance",
        "phone":"Téléphone", "cin":"CIN (facultatif)", "center":"Centre de santé",
        "blood":"Groupe sanguin", "allergies":"Allergies", "history":"Antécédents",
        "save":"Enregistrer", "saved":"Enregistrement effectué.",
        "required":"Le nom et le prénom sont obligatoires.",
        "reason":"Motif", "diagnosis":"Diagnostic / constat clinique",
        "treatment":"Conduite à tenir / traitement", "professional":"Professionnel",
        "date":"Date", "type":"Type", "result":"Résultat / observation",
        "ddr":"Date des dernières règles", "edd":"Date prévue d'accouchement",
        "notes":"Observations", "dose":"Dose", "vaccine":"Vaccin",
        "appointment_date":"Date du rendez-vous", "status":"Statut",
        "upcoming":"À venir", "done":"Effectué", "cancelled":"Annulé",
        "search":"Rechercher", "no_records":"Aucune donnée enregistrée.",
        "profile":"Profil", "history_tab":"Historique", "summary":"Synthèse",
        "total":"Dossiers enregistrés", "privacy":"Confidentialité",
        "demo":"Prototype de démonstration – données fictives uniquement.",
        "warning":"Ne pas saisir de données médicales réelles. Cette version n'est pas homologuée pour un usage clinique.",
        "export":"Télécharger la liste (CSV)", "choose":"Choisir une rubrique",
        "access":"Accès de démonstration", "access_note":"Le choix d'espace ci-dessous simule les rôles. Il ne constitue pas une authentification."
    },
    "ar": {
        "app":"دفتر صحة المرأة الرقمي", "tag":"Carnet de Santé de la Femme",
        "language":"اللغة", "role":"الفضاء", "woman":"فضاء المرأة",
        "doctor":"طبيب", "midwife":"قابلة", "nurse":"ممرض(ة)",
        "admin":"الإدارة", "home":"لوحة القيادة", "patients":"النساء",
        "new_patient":"ملف جديد", "medical":"الملف الصحي",
        "consult":"استشارة", "pregnancy":"تتبع الحمل",
        "vaccines":"التلقيحات", "screening":"الكشف المبكر",
        "appointments":"المواعيد", "documents":"الوثائق",
        "welcome":"مرحبا بك في دفتر صحتك",
        "select_patient":"اختيار المرأة", "no_patient":"لا يوجد ملف. يرجى إنشاء ملف أولا.",
        "name":"النسب", "first":"الاسم", "dob":"تاريخ الازدياد",
        "phone":"الهاتف", "cin":"رقم البطاقة (اختياري)", "center":"المركز الصحي",
        "blood":"فصيلة الدم", "allergies":"الحساسية", "history":"السوابق الطبية",
        "save":"حفظ", "saved":"تم الحفظ.",
        "required":"النسب والاسم إجباريان.",
        "reason":"سبب الاستشارة", "diagnosis":"التشخيص / الفحص السريري",
        "treatment":"العلاج / التوجيه", "professional":"المهني الصحي",
        "date":"التاريخ", "type":"النوع", "result":"النتيجة / الملاحظات",
        "ddr":"تاريخ آخر دورة شهرية", "edd":"التاريخ المتوقع للولادة",
        "notes":"ملاحظات", "dose":"الجرعة", "vaccine":"التلقيح",
        "appointment_date":"تاريخ الموعد", "status":"الحالة",
        "upcoming":"قادم", "done":"تم", "cancelled":"ملغى",
        "search":"بحث", "no_records":"لا توجد بيانات مسجلة.",
        "profile":"الملف الشخصي", "history_tab":"السجل", "summary":"ملخص",
        "total":"عدد الملفات", "privacy":"الخصوصية",
        "demo":"نموذج تجريبي – بيانات وهمية فقط.",
        "warning":"لا تدخلي أي بيانات صحية حقيقية. هذه النسخة غير معتمدة للاستعمال الطبي.",
        "export":"تحميل القائمة (CSV)", "choose":"اختيار قسم",
        "access":"ولوج تجريبي", "access_note":"اختيار الفضاء يحاكي الأدوار ولا يمثل نظام مصادقة حقيقيا."
    }
}

st.session_state.setdefault("lang", "fr")
lang_choice = st.sidebar.selectbox("Langue / اللغة", ["Français", "العربية"],
                                   index=0 if st.session_state.lang == "fr" else 1)
st.session_state.lang = "fr" if lang_choice == "Français" else "ar"
L = T[st.session_state.lang]
rtl = st.session_state.lang == "ar"

st.markdown("""
<style>
:root { --pink:#C94F83; --pink-dark:#A93668; --rose:#FFF1F6; }
.stApp { background:linear-gradient(180deg,#FFF8FB 0%,#FFFDFE 100%); }
[data-testid="stSidebar"] { background:#FCE8F0; }
h1,h2,h3 { color:#A93668 !important; }
.stButton>button, .stFormSubmitButton>button {
  background:#C94F83; color:white; border:0; border-radius:12px;
  padding:.55rem 1rem; font-weight:600;
}
.stButton>button:hover { background:#A93668; color:white; }
div[data-testid="stMetric"] { background:#FFFFFF; border:1px solid #F2D3E0;
  padding:14px; border-radius:14px; }
div[data-testid="stTabs"] button[aria-selected="true"] { color:#A93668; }
.csf-banner { background:linear-gradient(110deg,#B83E75,#E88BAF);
 color:white; padding:22px 25px; border-radius:18px; margin-bottom:15px; }
.small-note { color:#795565; font-size:13px; }
</style>
""", unsafe_allow_html=True)

if rtl:
    st.markdown("""<style>
    .main .block-container { direction:rtl; text-align:right; }
    [data-testid="stSidebar"] * { direction:rtl; text-align:right; }
    input, textarea { direction:rtl !important; text-align:right !important; }
    </style>""", unsafe_allow_html=True)

st.markdown(f'<div class="csf-banner"><h1 style="color:white!important;margin:0">🌸 {L["app"]}</h1><div>{L["tag"]}</div></div>', unsafe_allow_html=True)
st.warning(L["warning"])

role_labels = [L["woman"], L["doctor"], L["midwife"], L["nurse"], L["admin"]]
role = st.sidebar.selectbox(L["role"], role_labels)
st.sidebar.caption(L["access_note"])

df = get_patients()
patient_id = None
patient = None
if not df.empty:
    opts = {f'{r["first_name"]} {r["last_name"]} — CSF-{r["id"]:05d}': int(r["id"])
            for _, r in df.iterrows()}
    selected = st.sidebar.selectbox(L["select_patient"], list(opts.keys()))
    patient_id = opts[selected]
    patient = get_patient(patient_id)

st.sidebar.markdown("---")
st.sidebar.caption(L["demo"])

def show_df(data):
    if data.empty:
        st.info(L["no_records"])
    else:
        st.dataframe(data, use_container_width=True, hide_index=True)

def patient_form():
    st.subheader(L["new_patient"])
    with st.form("patient_form", clear_on_submit=True):
        c1,c2 = st.columns(2)
        with c1:
            last = st.text_input(L["name"])
            first = st.text_input(L["first"])
            dob = st.date_input(L["dob"], value=date(1990,1,1), min_value=date(1900,1,1))
            phone = st.text_input(L["phone"])
            cin = st.text_input(L["cin"])
        with c2:
            center = st.text_input(L["center"])
            blood = st.selectbox(L["blood"], ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            allergies = st.text_area(L["allergies"])
            history = st.text_area(L["history"])
        ok = st.form_submit_button(L["save"])
    if ok:
        if last.strip() and first.strip():
            add_patient(last, first, str(dob), phone, cin, center, blood, allergies, history)
            st.success(L["saved"])
            st.rerun()
        else:
            st.error(L["required"])

if role == L["admin"]:
    st.subheader(L["home"])
    a,b = st.columns(2)
    a.metric(L["total"], len(df))
    b.metric(L["patients"], len(df))
    show_df(df)
    if not df.empty:
        st.download_button(L["export"], df.to_csv(index=False).encode("utf-8-sig"),
                           "csf_demo_patientes.csv", "text/csv")
    patient_form()

elif role == L["woman"]:
    st.subheader(L["welcome"])
    if patient is None:
        st.info(L["no_patient"])
        patient_form()
    else:
        st.markdown(f"### 🌷 {patient['first_name']} {patient['last_name']}")
        tabs = st.tabs([L["profile"], L["medical"], L["appointments"], L["documents"]])
        with tabs[0]:
            c1,c2,c3 = st.columns(3)
            c1.metric("CSF ID", f"CSF-{patient_id:05d}")
            c2.metric(L["center"], patient["health_center"] or "—")
            c3.metric(L["blood"], patient["blood_group"] or "—")
            st.write(f"**{L['dob']} :** {patient['date_of_birth']}")
            st.write(f"**{L['phone']} :** {patient['phone'] or '—'}")
            st.write(f"**{L['allergies']} :** {patient['allergies'] or '—'}")
            st.write(f"**{L['history']} :** {patient['medical_history'] or '—'}")
        with tabs[1]:
            show_df(get_records(patient_id))
        with tabs[2]:
            show_df(get_appointments(patient_id))
        with tabs[3]:
            show_df(get_documents(patient_id))

else:
    st.subheader(f"{role} — {L['home']}")
    if role == L["doctor"]:
        menu_items = [L["home"], L["new_patient"], L["medical"], L["consult"],
                      L["pregnancy"], L["vaccines"], L["screening"], L["appointments"], L["documents"]]
    elif role == L["midwife"]:
        menu_items = [L["home"], L["new_patient"], L["medical"], L["consult"],
                      L["pregnancy"], L["vaccines"], L["appointments"], L["documents"]]
    else:
        menu_items = [L["home"], L["new_patient"], L["medical"], L["consult"],
                      L["vaccines"], L["screening"], L["appointments"], L["documents"]]
    menu = st.radio(L["choose"], menu_items, horizontal=True)

    if menu == L["home"]:
        x,y = st.columns(2)
        x.metric(L["total"], len(df))
        y.metric(L["patients"], len(df))
        show_df(df)

    elif menu == L["new_patient"]:
        patient_form()

    elif patient is None:
        st.info(L["no_patient"])

    elif menu == L["medical"]:
        st.subheader(f"{patient['first_name']} {patient['last_name']} — CSF-{patient_id:05d}")
        tabs = st.tabs([L["profile"], L["history_tab"], L["appointments"], L["documents"]])
        with tabs[0]:
            st.write(patient)
        with tabs[1]:
            show_df(get_records(patient_id))
        with tabs[2]:
            show_df(get_appointments(patient_id))
        with tabs[3]:
            show_df(get_documents(patient_id))

    elif menu == L["consult"]:
        st.subheader(L["consult"])
        with st.form("consult_form"):
            d = st.date_input(L["date"])
            reason = st.text_area(L["reason"])
            diagnosis = st.text_area(L["diagnosis"])
            treatment = st.text_area(L["treatment"])
            professional = st.text_input(L["professional"], value=role)
            ok = st.form_submit_button(L["save"])
        if ok:
            add_record(patient_id, "Consultation", str(d), reason, diagnosis, treatment, professional)
            st.success(L["saved"]); st.rerun()

    elif menu == L["pregnancy"]:
        with st.form("pregnancy_form"):
            ddr = st.date_input(L["ddr"])
            edd = st.date_input(L["edd"])
            notes = st.text_area(L["notes"])
            ok = st.form_submit_button(L["save"])
        if ok:
            add_record(patient_id, "Suivi grossesse", str(date.today()), f"DDR: {ddr}", f"DPA: {edd}", notes, role)
            st.success(L["saved"]); st.rerun()
        show_df(get_records(patient_id, "Suivi grossesse"))

    elif menu == L["vaccines"]:
        with st.form("vaccine_form"):
            d = st.date_input(L["date"])
            vaccine = st.text_input(L["vaccine"])
            dose = st.text_input(L["dose"])
            notes = st.text_area(L["notes"])
            ok = st.form_submit_button(L["save"])
        if ok and vaccine.strip():
            add_record(patient_id, "Vaccination", str(d), vaccine, dose, notes, role)
            st.success(L["saved"]); st.rerun()
        show_df(get_records(patient_id, "Vaccination"))

    elif menu == L["screening"]:
        with st.form("screen_form"):
            d = st.date_input(L["date"])
            kind = st.selectbox(L["type"], ["Dépistage cancer du sein", "Dépistage col de l'utérus", "Autre"])
            result = st.text_area(L["result"])
            notes = st.text_area(L["notes"])
            ok = st.form_submit_button(L["save"])
        if ok:
            add_screening(patient_id, str(d), kind, result, notes, role)
            st.success(L["saved"]); st.rerun()
        show_df(get_screenings(patient_id))

    elif menu == L["appointments"]:
        with st.form("appointment_form"):
            d = st.date_input(L["appointment_date"])
            purpose = st.text_input(L["reason"])
            status = st.selectbox(L["status"], [L["upcoming"], L["done"], L["cancelled"]])
            ok = st.form_submit_button(L["save"])
        if ok:
            add_appointment(patient_id, str(d), purpose, status)
            st.success(L["saved"]); st.rerun()
        show_df(get_appointments(patient_id))

    elif menu == L["documents"]:
        with st.form("document_form"):
            title = st.text_input(L["type"])
            doc_type = st.selectbox("Catégorie", ["Analyse", "Ordonnance", "Compte rendu", "Autre"])
            description = st.text_area(L["notes"])
            ok = st.form_submit_button(L["save"])
        if ok and title.strip():
            add_document(patient_id, title, doc_type, description)
            st.success(L["saved"]); st.rerun()
        show_df(get_documents(patient_id))

st.markdown("---")
st.caption("CSF Numérique • Prototype V2 • Données fictives uniquement")

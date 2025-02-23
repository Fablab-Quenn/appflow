import streamlit as st
import base64
import pandas as pd
import requests
from bs4 import BeautifulSoup
st.markdown("<h1 style='text-align: center; color: black;'>DATAFLOW </h1>", unsafe_allow_html=True)

# Injection de CSS personnalisé pour mettre le texte en blanc
def ajout_css():
    st.markdown(
        """
        <style>
            /* Change la couleur du texte en blanc */
            body {
                color: white !important;
            }
            /* Optionnel : Changement de couleur des titres */
            h1, h2, h3, h4, h5, h6, p {
                color: white !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Appeler la fonction dès le début de l'application
ajout_css()

# 🎨 Injection de CSS personnalisé
st.markdown(
    """
    
    <style>
    

        /* Couleur de fond rouge pour la barre latérale gauche */
        [data-testid="stSidebar"] {
            background-color: #18BC9C;
        }

        /* Styles personnalisés pour les boutons */
        button, .stButton > button {
            background-color: #C2C2C2 !important; /* Couleur de fond des boutons */
            border-radius: 5px !important; /* Rayon de bordure */
            padding: 0.5rem 1rem !important; /* Espacement intérieur */
        }

        /* Styles personnalisés pour les boutons de téléchargement */
        .stDownloadButton > button, .stDownloadButton > button:hover {
            background-color: #F0F0F0 !important; /* Couleur de fond des boutons de téléchargement */
            border: 2px solid black !important; /* Bordure noire */
            border-radius: 5px !important; /* Rayon de bordure */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def background_color(color):
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-color: {color};
                background-size: cover;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Appliquer une couleur d'arrière-plan
background_color("#C2C2C2") 





# 🌍 Présentation de l'application
st.markdown("""
Découvrez DataFlow, l'outil idéal pour explorer et analyser des données facilement. Téléchargez des jeux de données déjà nettoyées ou importez vos propres données brutes depuis le web. Avec l'intégration de Matplotlib, créez des visualisations professionnelles en quelques clics. Que vous soyez débutant ou expert, notre interface intuitive vous permet de manipuler vos données sans complexité. Boostez votre analyse et libérez tout le potentiel de vos informations.
* **Python libraries:** requests, pandas, beautifulsoup4, streamlit
* **Data source:** [sn.coinafrique](https://sn.coinafrique.com/).
""")


# 📂 Menu de navigation dans la barre latérale
st.sidebar.title("📂 Navigation")
menu_option = st.sidebar.radio(
    "📌 Sélectionnez une option :",
    ["Voir les datasets existants", "Remplir le formulaire", "À propos de moi"], index=0 )


# 📌 **Saisie du nombre de pages à scraper**
st.sidebar.write("### 📄 Nombre de pages à scraper")
num_pages = st.sidebar.number_input("Entrez le nombre de pages (entre 1 et 119) :", min_value=1, max_value=119, value=1, step=1)

# 📥 **Affichage du formulaire directement dans l'application**
if menu_option == "Remplir le formulaire":
    st.write("## 📝 Remplissez le formulaire")
    
    # Creation de formulaire d'evaluation avec kobotoolbox et google form
    form_choice = st.radio("🔍 Sélectionnez le formulaire à afficher :", ["KoboToolbox", "Google Forms"])
    
    # 1) Formulaires avec kobotoolbox
    if form_choice == "KoboToolbox":
        st.markdown(
            f'<div class="formulaire-iframe">'
            f'<iframe src="https://ee.kobotoolbox.org/i/6qWCbCZj" height="800" width="100%" frameborder="0" scrolling="yes"></iframe>'

            f'</div>',
            unsafe_allow_html=True
        #2) Formulaire avec google formes
        )
    elif form_choice == "Google Forms":
        st.markdown(
            f'<div class="formulaire-iframe">'
            f'<iframe src="https://docs.google.com/forms/d/e/1FAIpQLSdeC0f2k5jhyyP9SGYkdio2ZQ_IwJj3usg_AS7-GIjd5NrNmA/viewform?usp=header" height="800" width="100%" frameborder="0" scrolling="yes"></iframe>'
            f'</div>',
            unsafe_allow_html=True
        )
# 🕵️ **Fonction pour scraper les données**
def scrape_data(url, num_pages):
    list_habit = []
    
    for page in range(1, num_pages + 1):
        st.write(f"📡 Scraping page {page}...")
        response = requests.get(f"{url}?page={page}")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Recherche des conteneurs d'annonces
        boxes = soup.find_all('div', class_='col s6 m4 l3')  # Utilisation de la classe correspondante
        
        for vetement in boxes:
            # Extraction des données avec le format correct
            nom = vetement.find("p", class_="ad__card-description").text.strip() 
            adresse = vetement.find("p", class_="ad__card-location").text.replace("location_on", "").strip() 
            img = vetement.find("a", class_="card-image ad__card-image waves-block waves-light").img["src"] 
            
            # Création d'un dictionnaire avec les données extraites
            dict_habit = {"Type_habits" : Type_habits, "Prix" : Prix, "Adresse" : Adresse, "Image_link" : Image_link }

            list_habit.append(dict_habit)
    
    return pd.DataFrame(list_habit)

# 📥 **Fonction pour charger et afficher un dataset**

def load(file_path, dataset_name):
    df = pd.read_csv(file_path)
    max_rows = num_pages * 84
    displayed_df = df.head(max_rows)
    st.write(f"### 📊 Aperçu du jeu de données : {dataset_name}")
    st.write(f"🔢 Nombre de lignes affichées : {min(len(df), max_rows)}")
    st.dataframe(displayed_df)
    

# 🎯 **Voir les datasets existants**
if menu_option == "Voir les datasets existants":
    st.write("## 📂 Voir les datasets existants")
    
    # Création de deux colonnes pour afficher la catégorie et le dataset côte à côte
    col1, col2 = st.columns(2)
    
    with col1:
        # Sélection de la catégorie (Notebook ou Web)
        category_choice = st.selectbox("📂 Sélectionnez une catégorie :", ["Notebook", "Web"], key="category_select")
    
    with col2:
        # Mappage des fichiers selon la catégorie sélectionnée
        if category_choice == "Notebook":
            dataset_choice = st.selectbox("🔍 Sélectionnez un dataset Notebook :", 
                                          ["Chaussure NoteBook", "Vetement NoteBook"], key="notebook_dataset")
            file_mapping = {
                "Chaussure NoteBook": 'Chaussures_hommes_datas_clean.csv',
                "Vetement NoteBook": 'Vetements_hommes_datas_clean.csv'
            }
        elif category_choice == "Web":
            dataset_choice = st.selectbox("🔍 Sélectionnez un dataset Web :", 
                                          ["Chaussure Web", "Vetement Web"], key="web_dataset")
            file_mapping = {
                "Chaussure Web": 'Chaussures_hommes_datas_non_clean.csv',
                "Vetement Web": 'Vetements_hommes_datas_non_clean.csv'
            }
   
    # Charger et afficher le dataset sélectionné
    if dataset_choice in file_mapping:
        load(file_mapping[dataset_choice], dataset_choice)


# Section "À propos de moi"
if menu_option == "À propos de moi":
    st.write("## 👋 À propos de moi")
    
    # Image
    st.image(r"C:\Users\bmd tech\Desktop\AT\at2222.jpg", width=800)
    
    # Description personnelle
    st.write("""
    **Bonjour ! Je suis Anta NGOM🚀💡,**  
fondatrice de Linguere Fablab, passionnée par la technologie et l'innovation, et convaincue que l'inclusion des femmes et des jeunes filles dans les STEM est essentielle pour un avenir plus équitable et prospère. Mon travail se concentre sur la démocratisation de l'accès aux outils numériques et à la formation technique pour aider les communautés à se transformer grâce à la technologie.

Avec un parcours dans Big Data et l'IA, j'ai toujours eu pour mission de rendre la technologie accessible à tous, en particulier aux femmes et aux jeunes. Grâce à Linguere Fablab, j'ai initiée des programmes comme le Fablab Tour et le Smart Coders, qui permettent à des jeunes talents de découvrir l'univers numérique et d'explorer les carrières technologiques.

N'hésitez pas à me contacter pour échanger, collaborer ou partager des idées qui peuvent faire avancer notre communauté !



Mes Compétences
    - **Data Science** : Analyse de données, visualisation.
    - **Développement Web** : Streamlit, Django.
    - **Outils** : Python, Pandas, Matplotlib, Seaborn.

Contact
    - 📧 Email : [antalinguerefab@gmail.com]()
    - 🔗 LinkedIn : [www.linkedin.com/in/anta-ngom-🚀💡-325aa3246](https://)
    """)









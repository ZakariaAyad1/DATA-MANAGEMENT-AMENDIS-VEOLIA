import streamlit as st
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    body {
        background-color: #1a1a1d;
        font-family: 'Roboto', sans-serif;
        color: #ffffff;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    .main-title {
        font-size: 3em;
        color: #e94560;
        text-align: center;
        margin-top: 20px;
        text-shadow: 2px 2px #141414;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        letter-spacing: 3px;
    }
    .section-title {
        font-size: 2.5em;
        color: #0f3460;
        margin-top: 30px;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 1px 1px #141414;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
    }
    .btn {
        background: linear-gradient(45deg, #e94560, #0f3460);
        color: white;
        padding: 15px 30px;
        border: none;
        border-radius: 25px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 18px;
        margin: 20px 10px;
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .btn:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    .content {
        margin: 20px;
        padding: 30px;
        background: linear-gradient(135deg, #0f3460, #162447);
        border-radius: 20px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        color: #e94560;
        font-family: 'Roboto', sans-serif;
        font-size: 1.1em;
        line-height: 1.6;
    }
    .computer-info {
        font-size: 1.2em;
        margin-bottom: 20px;
        line-height: 1.8;
        font-family: 'Roboto', sans-serif;
        color: #f5f5f5;
    }
</style>


""", unsafe_allow_html=True)

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='veoliathursdaylaravel',
            user='root',
            password=''
        )
        if connection.is_connected():
            return connection
        else:
            st.error("Failed to connect to MySQL server")
            return None
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

def display_computers_by_type(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT c.numeroSerie, c.brandPc, c.description, e.Prenom, e.Nom, m.AnneeAcquisition
        FROM materiel m
        JOIN caracteristiquesordinateur c ON m.numeroSerie = c.numeroSerie
        LEFT JOIN employe e ON m.IdUtilisateur = e.IdUtilisateur
        ORDER BY c.brandPc
        """
        cursor.execute(query)
        computers = cursor.fetchall()

        st.markdown('<div class="section-title">Computers by Type</div>', unsafe_allow_html=True)
        for computer in computers:
            st.markdown(f"""
            <div class="content">
                <div class="computer-info"><strong>Numéro de Série:</strong> {computer['numeroSerie']}</div>
                <div class="computer-info"><strong>Computer Type:</strong> {computer['brandPc']}</div>
                <div class="computer-info"><strong>Description:</strong> {computer['description']}</div>
                <div class="computer-info"><strong>User:</strong> {computer['Prenom']} {computer['Nom']}</div>
                <div class="computer-info"><strong>Acquisition Year:</strong> {computer['AnneeAcquisition']}</div>
            </div>
            """, unsafe_allow_html=True)

    except Error as e:
        st.error(f"Error fetching data from MySQL: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            st.success('MySQL connection closed')
            
            
def display_top_5_oldest_computers(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT c.numeroSerie, c.brandPc, c.description, e.Prenom, e.Nom, m.AnneeAcquisition
        FROM materiel m
        JOIN caracteristiquesordinateur c ON m.numeroSerie = c.numeroSerie
        LEFT JOIN employe e ON m.IdUtilisateur = e.IdUtilisateur
        ORDER BY m.AnneeAcquisition ASC
        LIMIT 5
        """
        cursor.execute(query)
        computers = cursor.fetchall()

        st.markdown('<div class="section-title">Top 5 des Ordinateurs les Plus Anciens</div>', unsafe_allow_html=True)
        for computer in computers:
            st.markdown(f"""
            <div class="content">
                <div class="computer-info"><strong>Numéro de Série:</strong> {computer['numeroSerie']}</div>
                <div class="computer-info"><strong>Marque:</strong> {computer['brandPc']}</div>
                <div class="computer-info"><strong>Description:</strong> {computer['description']}</div>
                <div class="computer-info"><strong>Utilisateur:</strong> {computer['Prenom']} {computer['Nom']}</div>
                <div class="computer-info"><strong>Année d'Acquisition:</strong> {computer['AnneeAcquisition']}</div>
            </div>
            """, unsafe_allow_html=True)

    except Error as e:
        st.error(f"Error fetching data from MySQL: {e}")
    finally:
        if connection:
            cursor.close()
            
            
    
def search_computer_by_serial(connection, serial_number):
    
    try:
        cursor = connection.cursor(dictionary=True)
        #Lorsque vous appelez cursor.execute(query, (serial_number,)), le second argument est un tuple contenant les valeurs à insérer dans les espaces réservés %s. Dans ce cas, serial_number est inséré à la place du %s.
        query = """
        SELECT c.numeroSerie, c.brandPc, c.description,
               c.DisqueDurNumeroCapacite, c.UniteCapacite, c.DisqueDurType,
               c.processeur, c.PortableOuBureauOuAutre, c.RamNumeroCapacite,
               c.RamUnite, m.AnneeAcquisition ,
               e.Prenom, e.Nom
        FROM materiel m
        JOIN caracteristiquesordinateur c ON m.numeroSerie = c.numeroSerie
        LEFT JOIN employe e ON m.IdUtilisateur = e.IdUtilisateur
        
        WHERE c.numeroSerie = %s 
        """
        cursor.execute(query, (serial_number))
        computer = cursor.fetchone()

        if computer:
            st.markdown('<div class="section-title">Détails de l\'ordinateur</div>', unsafe_allow_html=True)
            st.markdown(f"""
                <div class="content">
                    <div class="computer-info"><strong>Numéro de Série:</strong> {computer['numeroSerie']}</div>
                    <div class="computer-info"><strong>Marque:</strong> {computer['brandPc']}</div>
                    <div class="computer-info"><strong>Description:</strong> {computer['description']}</div>
                    <div class="computer-info"><strong>Disque Dur Capacité:</strong> {computer['DisqueDurNumeroCapacite']} {computer['UniteCapacite']}</div>
                    <div class="computer-info"><strong>Type de Disque Dur:</strong> {computer['DisqueDurType']}</div>
                    <div class="computer-info"><strong>Processeur:</strong> {computer['processeur']}</div>
                    <div class="computer-info"><strong>Type d'Ordinateur:</strong> {computer['PortableOuBureauOuAutre']}</div>
                    <div class="computer-info"><strong>RAM Capacité:</strong> {computer['RamNumeroCapacite']} {computer['RamUnite']}</div>
                    <div class="computer-info"><strong>Utilisateur:</strong> {computer['Prenom']} {computer['Nom']}</div>
                    <div class="computer-info"><strong>Année d'Acquisition:</strong> {computer['AnneeAcquisition']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(f"Aucun ordinateur trouvé avec le numéro de série '{serial_number}'")

    except Error as e:
        st.error(f"Erreur lors de la recherche de l'ordinateur dans MySQL: {e}")
    finally:
        if connection:
            cursor.close()
            
 
def ajouterTous():
    numero_serie = st.text_input("Numéro de Série:")
    brand_pc = st.text_input("Marque:")
    description = st.text_input("Description:")
    disque_dur_capacite = st.number_input("Capacité du Disque Dur:", step=0.01)
    unite_capacite = st.selectbox("Unité de Capacité:", ["Go", "To", "Mo"])
    disque_dur_type = st.selectbox("Type de Disque Dur:", ["HDD", "SSD", "SSHD", "External HDD", "NAS", "NVMe", "M.2", "eMMC", "U.2", "mSATA"])
    processeur = st.text_input("Processeur:")
    type_ordi = st.selectbox("Type d'Ordinateur:", ["Portable", "Bureau", "Station"])
    ram_capacite = st.number_input("Capacité de RAM:", step=0.01)
    ram_unite = st.selectbox("Unité de RAM:", ["Go", "To", "Mo"])
    prenom = st.text_input("Prénom de l'Utilisateur:")
    nom = st.text_input("Nom de l'Utilisateur:")
    email = st.text_input("Email de l'Utilisateur:")
    telephone = st.text_input("Téléphone de l'Utilisateur:")
    site_geographique = st.selectbox("Site Géographique de l'Utilisateur:", ["Al Massira", "Al Youmne", "Azhar", "Azla", "Boujerrah", "BOUZAGHLAL", "CFC", "CHBAR", "DOP TE", "F'nideq", "G.Comptes", "Mandri", "Martil", "Matar", "M'diq", "Oued laou", "QODS", "STEP ALMENA", "STEP Oued laou", "STEP Z.industrielle"])
    direction = st.selectbox("Direction:", ["DAAI", "DCF", "DCL", "DEA", "DJCA", "DOP", "DRH", "DSC", "DSI", "DST"])
    numero_inventaire = st.text_input("Numéro d'Inventaire:")
    annee_selectionnee = st.selectbox("Sélectionnez une année :", [str(annee) for annee in range(2000, datetime.now().year + 1)])
    
    ville = st.text_input("Ville de l'Utilisateur:")
    rue = st.text_input("Rue de l'Utilisateur:")
    numero_rue = st.number_input("Numéro de Rue de l'Utilisateur:", step=1)
    pays = st.text_input("Pays de l'Utilisateur:")  

    if st.button("Ajouter l'Ordinateur"):
        try:
            connection = create_connection()
            if connection:
                cursor = connection.cursor()

                # Vérifier l'existence du pays
                select_country_query = "SELECT IdPays FROM pays WHERE nom = %s LIMIT 1"
                cursor.execute(select_country_query, (pays,))
                country = cursor.fetchone()
                
                if not country:
                    # Insérer le pays si n'existe pas
                    insert_country_query = "INSERT INTO pays (IdPays, nom) VALUES (UUID(), %s)"
                    cursor.execute(insert_country_query, (pays,))
                    cursor.execute(select_country_query, (pays,))
                    country = cursor.fetchone()
                
                id_pays = country[0]
                
                # Insérer l'adresse
                insert_address_query = """
                INSERT INTO adresse (idAdresse, ville, rue, numeroRue, IdPays)
                VALUES (UUID(), %s, %s, %s, %s)
                """
                cursor.execute(insert_address_query, (ville, rue, numero_rue, id_pays))

                # Obtenir l'idAdresse insérée
                select_address_query = "SELECT idAdresse FROM adresse WHERE ville = %s AND rue = %s AND numeroRue = %s AND IdPays = %s LIMIT 1"
                cursor.execute(select_address_query, (ville, rue, numero_rue, id_pays))
                id_adresse = cursor.fetchone()[0]
                
                # Insérer ou mettre à jour l'utilisateur
                insert_user_query = """
                INSERT INTO employe (IdUtilisateur, Prenom, Nom, email, telephon, IdSiteGeographique, idAdresse)
                VALUES (UUID(), %s, %s, %s, %s, (SELECT IdSiteGeographique FROM sitegeographique WHERE nom = %s LIMIT 1), %s)
                ON DUPLICATE KEY UPDATE
                    Prenom = VALUES(Prenom),
                    Nom = VALUES(Nom),
                    email = VALUES(email),
                    telephon = VALUES(telephon),
                    IdSiteGeographique = VALUES(IdSiteGeographique),
                    idAdresse = VALUES(idAdresse)
                """
                cursor.execute(insert_user_query, (prenom, nom, email, telephone, site_geographique, id_adresse))

                # Obtenir l'IdUtilisateur inséré ou mis à jour
                select_user_query = "SELECT IdUtilisateur FROM employe WHERE Prenom = %s AND Nom = %s LIMIT 1"
                cursor.execute(select_user_query, (prenom, nom))
                id_utilisateur = cursor.fetchone()[0]

                # Insérer dans la table materiel
                insert_materiel_query = """
                INSERT INTO materiel (numeroInventaire, AnneeAcquisition, IdDirection, numeroSerie, IdUtilisateur)
                VALUES (%s, %s, (SELECT IdDirection FROM direction WHERE nom = %s LIMIT 1), %s, %s)
                """
                cursor.execute(insert_materiel_query, (numero_inventaire, annee_selectionnee, direction, numero_serie, id_utilisateur))

                # Insérer les caractéristiques de l'ordinateur dans la table caracteristiquesordinateur
                insert_caracteristiques_query = """
                INSERT INTO caracteristiquesordinateur (numeroSerie, DisqueDurNumeroCapacite, UniteCapacite,
                                                        DisqueDurType, processeur, PortableOuBureauOuAutre,
                                                        RamNumeroCapacite, RamUnite, brandPc, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_caracteristiques_query, (numero_serie, disque_dur_capacite, unite_capacite,
                                                               disque_dur_type, processeur, type_ordi,
                                                               ram_capacite, ram_unite, brand_pc, description))

                # Valider la transaction et afficher un message de succès
                connection.commit()
                st.success("L'ordinateur a été ajouté avec succès!")

        except Exception as e:
            st.error(f"Erreur lors de l'ajout de l'ordinateur : {e}")
        finally:
            if connection:
                connection.close()
                
                

def get_computer_statistics(connection):
    try:
        query = """
        SELECT c.numeroSerie, c.brandPc, c.description, e.Prenom, e.Nom, m.AnneeAcquisition
        FROM materiel m
        JOIN caracteristiquesordinateur c ON m.numeroSerie = c.numeroSerie
        LEFT JOIN employe e ON m.IdUtilisateur = e.IdUtilisateur
        """
        df = pd.read_sql(query, connection)
        return df
    except Error as e:
        st.error(f"Error fetching data from MySQL: {e}")
        return None

def plot_oldest_computers(df):
    oldest_computers = df.sort_values(by='AnneeAcquisition').head(5)
    fig, ax = plt.subplots()
    sns.barplot(x='AnneeAcquisition', y='numeroSerie', data=oldest_computers, ax=ax)
    ax.set_title('Top 5 des Ordinateurs les Plus Anciens')
    ax.set_xlabel('Année d\'Acquisition')
    ax.set_ylabel('Numéro de Série')
    st.pyplot(fig)

def plot_computers_by_brand(df):
    brand_count = df['brandPc'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=brand_count.index, y=brand_count.values, ax=ax)
    ax.set_title('Nombre d\'Ordinateurs par Marque')
    ax.set_xlabel('Marque')
    ax.set_ylabel('Nombre d\'Ordinateurs')
    st.pyplot(fig)

def plot_acquisition_year_distribution(df):
    fig, ax = plt.subplots()
    sns.histplot(df['AnneeAcquisition'], bins=20, kde=True, ax=ax)
    ax.set_title('Distribution des Années d\'Acquisition')
    ax.set_xlabel('Année d\'Acquisition')
    ax.set_ylabel('Nombre d\'Ordinateurs')
    st.pyplot(fig)

###
#
#
#
#
# Fonction pour récupérer les données d'ordinateurs depuis la base de données
def fetch_computers_data():
    query = "SELECT * FROM materiel"
    df = pd.read_sql(query, con=connection)
    return df

# Fonction pour filtrer et trier les données d'ordinateurs
def filter_and_sort_computers_data(df, filter_criteria, sort_by):
    filtered_df = df.copy()
    
    # Filtrage par critères
    for critere, valeur in filter_criteria.items():
        if valeur and critere in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[critere] == valeur]
    
    # Tri par critère
    if sort_by and sort_by in filtered_df.columns:
        filtered_df = filtered_df.sort_values(by=sort_by)
    
    return filtered_df

# Fonction principale pour la section 'filtrage'
def filtrage_section():
    st.header("Filtrage des données d'ordinateurs")

    # Récupérer les données d'ordinateurs depuis la base de données
    computers_df = fetch_computers_data()

    # Liste des critères de filtrage disponibles
    filter_criteria = {
        'PortableOuBureauOuAutre': st.sidebar.selectbox('Type', options=['Portable', 'Bureau', 'Station', None]),
        'AnneeAcquisition': st.sidebar.number_input('Année d\'acquisition', min_value=1990, max_value=2024),
        'brandPc': st.sidebar.text_input('Marque'),
        # Ajouter d'autres critères de filtrage si nécessaire
    }

    # Tri par critère sélectionné
    sort_by = st.sidebar.selectbox('Trier par', options=['AnneeAcquisition', 'brandPc', None])

    # Filtrer et trier les données en fonction des critères sélectionnés
    filtered_df = filter_and_sort_computers_data(computers_df, filter_criteria, sort_by)

    # Afficher les données filtrées dans un tableau
    st.dataframe(filtered_df)

#
#
#




# Titre de la page d'accueil
st.markdown('<div class="main-title">Bienvenue sur le site de Amendis</div>', unsafe_allow_html=True)

# Présentation générale de l'entreprise
st.write("""
Filiale de Veolia Maroc, Amendis est un opérateur de services publics en charge depuis 2002 de la distribution d'eau potable et d'électricité, ainsi que de la collecte et du traitement des eaux usées pour 1,8 millions d'habitants de la région de Tanger-Tétouan.
""")



connection = create_connection()


# Liens vers les différentes fonctionnalités
st.subheader('Naviguer vers :')
section = st.selectbox("Choisissez une section", ("Accueil", "Liste des Ordinateurs", "Top 5 des Ordinateurs les Plus Anciens","rechercher a un ordinateur", "Ajout d'Ordinateurs", "Statistiques", "filtrage"))

if section == 'Liste des Ordinateurs':
    st.markdown('<div class="section-title">Affichage de la liste des ordinateurs...</div>', unsafe_allow_html=True)
    # Appel de la fonction pour afficher les ordinateurs par type
    
    if connection:
        display_computers_by_type(connection)

elif section == 'Top 5 des Ordinateurs les Plus Anciens':
    st.markdown('<div class="section-title">Affichage du top 5 des ordinateurs les plus anciens...</div>', unsafe_allow_html=True)
    # Code pour afficher le top 5 des ordinateurs les plus anciens
    if connection:
        display_top_5_oldest_computers(connection)
        connection.close()  # Fermer la connexion après utilisation
        
        
elif section == 'Ajout d\'Ordinateurs':
    st.markdown('<div class="section-title">Formulaire pour ajouter de nouveaux ordinateurs...</div>', unsafe_allow_html=True)
    if connection :
        ajouterTous()
   


elif section == 'Statistiques':
    st.markdown('<div class="section-title">Affichage des statistiques...</div>', unsafe_allow_html=True)
    if connection:
        df = get_computer_statistics(connection)
        if df is not None:
            st.markdown('<div class="section-title">Top 5 des Ordinateurs les Plus Anciens</div>', unsafe_allow_html=True)
            plot_oldest_computers(df)
            st.markdown('<div class="section-title">Nombre d\'Ordinateurs par Marque</div>', unsafe_allow_html=True)
            plot_computers_by_brand(df)
            st.markdown('<div class="section-title">Distribution des Années d\'Acquisition</div>', unsafe_allow_html=True)
            plot_acquisition_year_distribution(df)
        connection.close()
elif section == 'rechercher a un ordinateur':
    st.markdown('<div class="section-title">rechercher a un ordinateur...</div>', unsafe_allow_html=True)
    numeroSerie_search = st.text_input("Numéro de Série de l'ordinateur à rechercher:")
    
    if connection:
        search_computer_by_serial(connection, numeroSerie_search)
        connection.close()

elif section == 'filtrage' :
    st.markdown('<div class="section-title">filtrage ...</div>', unsafe_allow_html=True)
    if connection:
        filtrage_section()
        connection.close()


    

import streamlit as st
from datetime import datetime
from fonctions.ordinateur.connection import create_connection

def ajouterTous():
    st.header("Ajouter un Ordinateur et Utilisateur")

    with st.form(key="ajouter_form"):
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

        submit_button = st.form_submit_button(label="Ajouter l'Ordinateur")

    if submit_button:
        try:
            connection = create_connection()
            if connection:
                cursor = connection.cursor()

                cursor.execute("START TRANSACTION")

                cursor.execute("SELECT IdPays FROM pays WHERE nom = %s LIMIT 1", (pays,))
                country = cursor.fetchone()
                
                if country:
                    id_pays = country[0]
                    st.write(f"Pays '{pays}' trouvé avec Id: {id_pays}")
                else:
                    cursor.execute("INSERT INTO pays (nom) VALUES (%s)", (pays,))
                    id_pays = cursor.lastrowid
                    st.write(f"Pays '{pays}' ajouté avec Id: {id_pays}")

                cursor.execute("SELECT IdAdresse FROM adresse WHERE ville = %s AND rue = %s AND numeroRue = %s AND IdPays = %s LIMIT 1", (ville, rue, numero_rue, id_pays))
                address = cursor.fetchone()
                
                if address:
                    id_adresse = address[0]
                    st.write(f"Adresse existe déjà avec Id: {id_adresse}")
                else:
                    cursor.execute("INSERT INTO adresse (ville, rue, numeroRue, IdPays) VALUES (%s, %s, %s, %s)", (ville, rue, numero_rue, id_pays))
                    id_adresse = cursor.lastrowid
                    st.write(f"Adresse ajoutée avec Id: {id_adresse}")

                cursor.execute("SELECT IdDirection FROM direction WHERE nom = %s LIMIT 1", (direction,))
                direction_record = cursor.fetchone()
                
                if direction_record:
                    id_direction = direction_record[0]
                    st.write(f"Direction '{direction}' trouvée avec Id: {id_direction}")
                else:
                    cursor.execute("INSERT INTO direction (nom) VALUES (%s)", (direction,))
                    id_direction = cursor.lastrowid
                    st.write(f"Direction '{direction}' ajoutée avec Id: {id_direction}")

                # Check if the site exists
                cursor.execute("SELECT IdSiteGeographique FROM sitegeographique WHERE nom = %s LIMIT 1", (site_geographique,))
                site = cursor.fetchone()
                
                if site:
                    id_site = site[0]
                    st.write(f"Site géographique '{site_geographique}' trouvé avec Id: {id_site}")
                else:
                    cursor.execute("INSERT INTO sitegeographique (nom) VALUES (%s)", (site_geographique,))
                    id_site = cursor.lastrowid
                    st.write(f"Site géographique '{site_geographique}' ajouté avec Id: {id_site}")

                cursor.execute("INSERT INTO employe (Prenom, Nom, email, telephon, IdSiteGeographique, idAdresse) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE Prenom = VALUES(Prenom), Nom = VALUES(Nom), email = VALUES(email), telephon = VALUES(telephon), IdSiteGeographique = VALUES(IdSiteGeographique), idAdresse = VALUES(idAdresse)", (prenom, nom, email, telephone, id_site, id_adresse))
                
                cursor.execute("SELECT IdUtilisateur FROM employe WHERE Prenom = %s AND Nom = %s LIMIT 1", (prenom, nom))
                id_utilisateur = cursor.fetchone()
                if not id_utilisateur:
                    st.error("Erreur: Impossible de récupérer l'ID de l'utilisateur.")
                    connection.rollback()
                    return
                id_utilisateur = id_utilisateur[0]

                cursor.execute("INSERT INTO caracteristiquesordinateur (numeroSerie, DisqueDurNumeroCapacite, UniteCapacite, DisqueDurType, processeur, PortableOuBureauOuAutre, RamNumeroCapacite, RamUnite, brandPc, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (numero_serie, disque_dur_capacite, unite_capacite, disque_dur_type, processeur, type_ordi, ram_capacite, ram_unite, brand_pc, description))

                cursor.execute("INSERT INTO materiel (numeroInventaire, AnneeAcquisition, IdDirection, numeroSerie, IdUtilisateur) VALUES (%s, %s, %s, %s, %s)", (numero_inventaire, annee_selectionnee, id_direction, numero_serie, id_utilisateur))

                connection.commit()
                st.success("L'ordinateur et l'utilisateur ont été ajoutés avec succès.")

        except Exception as e:
            st.error(f"Erreur lors de l'ajout de l'ordinateur : {e}")
            if connection:
                connection.rollback()  
        finally:
            if connection:
                connection.close()

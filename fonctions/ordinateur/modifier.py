from imports import *
from fonctions.ordinateur.connection import create_connection

def load_computer_info(connection, serial_number):
    cursor = connection.cursor(dictionary=True)
    try:
        st.write(f"Chargement des informations pour le numéro de série : {serial_number}")
        cursor.execute("SELECT * FROM caracteristiquesordinateur WHERE numeroSerie = %s", (serial_number,))
        computer_info = cursor.fetchone()
        cursor.execute("SELECT * FROM materiel WHERE numeroSerie = %s", (serial_number,))
        materiel_info = cursor.fetchone()
        if not computer_info or not materiel_info:
            st.error(f"Aucune information trouvée pour le numéro de série: {serial_number}")
        else:
            st.write(f"Informations chargées : {computer_info}, {materiel_info}")
        cursor.close()
    except Exception as e:
        st.error(f"Erreur lors du chargement des informations: {e}")
        computer_info, materiel_info = None, None
    return computer_info, materiel_info

def update_computer_info(connection, serial_number, new_computer_info, new_materiel_info):
    cursor = connection.cursor()
    try:
        st.write(f"Mise à jour des informations pour le numéro de série : {serial_number}")
        cursor.execute("""
            UPDATE caracteristiquesordinateur SET 
                DisqueDurNumeroCapacite = %s,
                UniteCapacite = %s,
                DisqueDurType = %s,
                processeur = %s,
                PortableOuBureauOuAutre = %s,
                RamNumeroCapacite = %s,
                RamUnite = %s,
                brandPc = %s,
                description = %s
            WHERE numeroSerie = %s
        """, (
            new_computer_info['DisqueDurNumeroCapacite'],
            new_computer_info['UniteCapacite'],
            new_computer_info['DisqueDurType'],
            new_computer_info['processeur'],
            new_computer_info['PortableOuBureauOuAutre'],
            new_computer_info['RamNumeroCapacite'],
            new_computer_info['RamUnite'],
            new_computer_info['brandPc'],
            new_computer_info['description'],
            serial_number
        ))
        
        cursor.execute("""
            UPDATE materiel SET 
                AnneeAcquisition = %s,
                IdDirection = %s,
                IdUtilisateur = %s
            WHERE numeroSerie = %s
        """, (
            new_materiel_info['AnneeAcquisition'],
            new_materiel_info['IdDirection'],
            new_materiel_info['IdUtilisateur'],
            serial_number
        ))
        
        connection.commit()
        st.success(f"Les informations pour l'ordinateur avec le numéro de série {serial_number} ont été mises à jour avec succès.")
    except Exception as e:
        st.error(f"Erreur lors de la mise à jour de l'ordinateur : {e}")
    finally:
        cursor.close()
def modify_computer_info_ui():
    connection = create_connection()
    if connection is None:
        st.error("Échec de la connexion à la base de données.")
        return

    st.write("Connexion à la base de données réussie.")  # Message de débogage

    st.header("Modifier les informations d'un ordinateur")
    
    serial_number = st.text_input("Numéro de Série de l'ordinateur à modifier:")
    st.write(f"Numéro de série saisi : {serial_number}")  # Message de débogage

    if st.button("Charger les informations"):
        if serial_number:
            st.write("Chargement des informations...")  # Message de débogage
            computer_info, materiel_info = load_computer_info(connection, serial_number)
            if computer_info and materiel_info:
                st.success(f"Informations chargées pour l'ordinateur avec le numéro de série {serial_number}.")
                with st.form(key='update_form'):
                    DisqueDurNumeroCapacite = st.text_input("Capacité du Disque Dur", computer_info['DisqueDurNumeroCapacite'])
                    UniteCapacite = st.text_input("Unité de Capacité", computer_info['UniteCapacite'])
                    DisqueDurType = st.text_input("Type de Disque Dur", computer_info['DisqueDurType'])
                    processeur = st.text_input("Processeur", computer_info['processeur'])
                    PortableOuBureauOuAutre = st.text_input("Type (Portable/Bureau/Autre)", computer_info['PortableOuBureauOuAutre'])
                    RamNumeroCapacite = st.text_input("Capacité de la RAM", computer_info['RamNumeroCapacite'])
                    RamUnite = st.text_input("Unité de RAM", computer_info['RamUnite'])
                    brandPc = st.text_input("Marque", computer_info['brandPc'])
                    description = st.text_input("Description", computer_info['description'])
                    
                    AnneeAcquisition = st.text_input("Année d'Acquisition", materiel_info['AnneeAcquisition'])
                    IdDirection = st.text_input("ID de la Direction", materiel_info['IdDirection'])
                    IdUtilisateur = st.text_input("ID de l'Utilisateur", materiel_info['IdUtilisateur'])

                    submitted = st.form_submit_button("Mettre à jour")
                    st.write(f"Formulaire soumis : {submitted}")  # Message de débogage

                    if submitted:
                        st.write("Formulaire soumis pour mise à jour...")  # Message de débogage
                        new_computer_info = {
                            'DisqueDurNumeroCapacite': DisqueDurNumeroCapacite,
                            'UniteCapacite': UniteCapacite,
                            'DisqueDurType': DisqueDurType,
                            'processeur': processeur,
                            'PortableOuBureauOuAutre': PortableOuBureauOuAutre,
                            'RamNumeroCapacite': RamNumeroCapacite,
                            'RamUnite': RamUnite,
                            'brandPc': brandPc,
                            'description': description
                        }
                        new_materiel_info = {
                            'AnneeAcquisition': AnneeAcquisition,
                            'IdDirection': IdDirection,
                            'IdUtilisateur': IdUtilisateur
                        }
                        st.info("Enregistrement des nouvelles informations...")
                        try:
                            update_computer_info(connection, serial_number, new_computer_info, new_materiel_info)
                        except Exception as e:
                            st.error(f"Erreur lors de la mise à jour : {e}")
            else:
                st.error("Numéro de série non trouvé dans la base de données.")
        else:
            st.warning("Veuillez entrer un numéro de série.")

    connection.close()


import streamlit as st
from mysql.connector import Error

def display_top_5_oldest_computers(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT 
            c.numeroSerie, 
            c.brandPc, 
            c.description, 
            c.processeur, 
            c.RamNumeroCapacite, 
            c.RamUnite, 
            c.DisqueDurNumeroCapacite, 
            c.UniteCapacite, 
            c.DisqueDurType, 
            e.Prenom, 
            e.Nom, 
            m.AnneeAcquisition,
            a.ville AS AdresseVille,
            a.rue AS AdresseRue,
            a.numeroRue AS AdresseNumero,
            p.nom AS PaysNom,
            d.nom AS DirectionNom,
            s.nom AS SiteNom
        FROM materiel m
        JOIN caracteristiquesordinateur c ON m.numeroSerie = c.numeroSerie
        LEFT JOIN employe e ON m.IdUtilisateur = e.IdUtilisateur
        LEFT JOIN adresse a ON e.idAdresse = a.idAdresse
        LEFT JOIN pays p ON a.IdPays = p.IdPays
        LEFT JOIN direction d ON m.IdDirection = d.IdDirection
        LEFT JOIN sitegeographique s ON e.IdSiteGeographique = s.IdSiteGeographique
        ORDER BY m.AnneeAcquisition
        limit 5
        """
        cursor.execute(query)
        computers = cursor.fetchall()

        # Custom CSS for blue background, white text, and longer display boxes
        st.markdown("""
        <style>
        .computer-card {
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0; /* Add vertical margin for spacing between computers */
            background-color: #003366; /* Dark blue background */
            color: white; /* White text */
            height: auto; /* Adjust height based on content */
            overflow: auto; /* Enable scroll if content overflows */
        }
        .computer-info {
            margin: 10px 0;
            line-height: 1.5;
        }
        .section-title {
            font-size: 24px;
            font-weight: bold;
            color: #003366; /* Dark blue for section title */
            margin-bottom: 20px;
        }
        .computer-container {
            display: flex;
            flex-direction: column;
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-title">Computers by Type</div>', unsafe_allow_html=True)

        for computer in computers:
            # Replace None values with default message
            computer = {key: (value if value is not None else "Information not available") for key, value in computer.items()}
            
            # Handle address formatting
            address_components = [
                computer['AdresseVille'],
                computer['AdresseRue'],
                str(computer['AdresseNumero']) if computer['AdresseNumero'] != "Information not available" else ""
            ]
            if all(component == "Information not available" or component for component in address_components):
                address = ', '.join(address_components).strip(', ')
            else:
                address = "Information not available"

            with st.container():
                with st.expander(f"Details for {computer['numeroSerie']}", expanded=False):  # Set expanded=False to initially hide the content
                    st.markdown(f"""
                    <div class="computer-card">
                        <div class="computer-info"><strong>Numéro de Série:</strong> {computer['numeroSerie']}</div>
                        <div class="computer-info"><strong>Computer Type:</strong> {computer['brandPc']}</div>
                        <div class="computer-info"><strong>Description:</strong> {computer['description']}</div>
                        <div class="computer-info"><strong>Processor:</strong> {computer['processeur']}</div>
                        <div class="computer-info"><strong>RAM Capacity:</strong> {computer['RamNumeroCapacite']} {computer['RamUnite']}</div>
                        <div class="computer-info"><strong>Hard Disk Capacity:</strong> {computer['DisqueDurNumeroCapacite']} {computer['UniteCapacite']}</div>
                        <div class="computer-info"><strong>Hard Disk Type:</strong> {computer['DisqueDurType']}</div>
                        <div class="computer-info"><strong>User:</strong> {computer['Prenom']} {computer['Nom']}</div>
                        <div class="computer-info"><strong>Acquisition Year:</strong> {computer['AnneeAcquisition']}</div>
                        <div class="computer-info"><strong>Address:</strong> {address}</div>
                        <div class="computer-info"><strong>Country:</strong> {computer['PaysNom']}</div>
                        <div class="computer-info"><strong>Direction:</strong> {computer['DirectionNom']}</div>
                        <div class="computer-info"><strong>Site:</strong> {computer['SiteNom']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    except Error as e:
        st.error(f"Error fetching data from MySQL: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            st.success('MySQL connection closed')

from imports import *


def search_computer_by_serial(connection, serial_number):
    
    try:
        if connection is None:
            st.error("La connexion base de données n est pas etablie.")
            return

        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT c.numeroSerie, c.brandPc, c.description,
               c.DisqueDurNumeroCapacite, c.UniteCapacite, c.DisqueDurType,
               c.processeur, c.PortableOuBureauOuAutre, c.RamNumeroCapacite,
               c.RamUnite, m.AnneeAcquisition,
               e.Prenom, e.Nom
        FROM materiel m
        JOIN caracteristiquesordinateur c ON m.numeroSerie = c.numeroSerie
        LEFT JOIN employe e ON m.IdUtilisateur = e.IdUtilisateur
        WHERE c.numeroSerie = %s
        """
        cursor.execute(query, (serial_number,))
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
        if connection and cursor:
            cursor.close()     
         
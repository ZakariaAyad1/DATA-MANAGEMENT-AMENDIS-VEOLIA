from imports import *

def delete_computer_and_related_info(connection, serial_number):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            DELETE FROM observation 
            WHERE IdUtilisateur IN (
                SELECT IdUtilisateur FROM employe 
                WHERE IdUtilisateur IN (
                    SELECT IdUtilisateur FROM materiel 
                    WHERE numeroSerie = %s
                )
            )
        """, (serial_number,))

        cursor.execute("""
            DELETE FROM materiel 
            WHERE numeroSerie = %s
        """, (serial_number,))

        cursor.execute("""
            DELETE FROM caracteristiquesordinateur 
            WHERE numeroSerie = %s
        """, (serial_number,))

        cursor.execute("""
            DELETE FROM employe 
            WHERE IdUtilisateur IN (
                SELECT IdUtilisateur FROM materiel 
                WHERE numeroSerie = %s
            )
        """, (serial_number,))

        connection.commit()
        st.success(f"L'ordinateur avec le numéro de série {serial_number} a été supprimé avec succès.")
    except mysql.connector.Error as err:
        st.error(f"Erreur: {err}")
        connection.rollback() #est une méthode utilisée pour annuler les modifications effectuées dans la base de données au cours de la transaction en cours. 
    finally:
        cursor.close()
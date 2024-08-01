import streamlit as st
import pandas as pd
from imports import *
from fonctions.ordinateur.connection import create_connection
from fonctions.ordinateur.Ordinateurs import display_computers_by_type
from fonctions.ordinateur.ordinateurs_top5 import display_top_5_oldest_computers
from fonctions.ordinateur.Ajout import ajouterTous
from fonctions.ordinateur.rechercher import search_computer_by_serial
from fonctions.ordinateur.Statistiques import get_computer_statistics, plot_computers_by_brand, plot_acquisition_year_distribution, plot_computers_by_type, plot_top_brands, plot_ram_distribution
from fonctions.ordinateur.supprimer import delete_computer_and_related_info
from fonctions.ordinateur.filtrage import filtrage_avance
from fonctions.ordinateur.modifier import load_computer_info, update_computer_info, modify_computer_info_ui
# from fonctions.utilisateurs import add_user, modify_user, delete_user

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("style.css")

st.markdown('<div class="main-title">Bienvenue sur le site de Amendis</div>', unsafe_allow_html=True)

st.write("""
Filiale de Veolia Maroc, Amendis est un opérateur de services publics en charge depuis 2002 de la distribution d'eau potable et d'électricité, ainsi que de la collecte et du traitement des eaux usées pour 1,8 millions d'habitants de la région de Tanger-Tétouan.
""")

with st.sidebar:
    st.image('veoliaimage.png', use_column_width=True) 
    st.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)
    section = st.selectbox("Choisissez une section",
                           ["Accueil", "Liste des Ordinateurs", "Top 5 des Ordinateurs les Plus Anciens",
                            "Rechercher un Ordinateur", "Ajout d'Ordinateurs", "Statistiques", "Filtrage",
                            "Supprimer un Ordinateur", "Modifier un ordinateur", "Gestion des Utilisateurs"])

connection = create_connection()

if section == 'Accueil':
    st.markdown('<div class="section-title">Accueil</div>', unsafe_allow_html=True)
    st.write("Bienvenue sur le tableau de bord interactif de Amendis.")

elif section == 'Liste des Ordinateurs':
    st.markdown('<div class="section-title">Liste des Ordinateurs</div>', unsafe_allow_html=True)
    if connection:
        display_computers_by_type(connection)
        connection.close()

elif section == 'Top 5 des Ordinateurs les Plus Anciens':
    if connection:
        display_top_5_oldest_computers(connection)
        connection.close()

elif section == 'Ajout d\'Ordinateurs':
    st.markdown('<div class="section-title">Ajout d\'Ordinateurs</div>', unsafe_allow_html=True)
    if connection:
        ajouterTous()
        connection.close()

elif section == 'Statistiques':
    st.markdown('<div class="section-title">Statistiques</div>', unsafe_allow_html=True)
    
    if connection:
        df = get_computer_statistics(connection)
        
        if df is not None:
            with st.expander("Nombre d'Ordinateurs par Marque"):
                plot_computers_by_brand(df)
            
            with st.expander("Distribution des Années d'Acquisition"):
                plot_acquisition_year_distribution(df)
            
            with st.expander("Nombre d'Ordinateurs par Type"):
                plot_computers_by_type(df)
            
            with st.expander("Top 5 Marque d'Ordinateurs"):
                plot_top_brands(df)
            
            with st.expander("Distribution de la Capacité de RAM et de Stockage"):
                plot_ram_distribution(df)
        
        connection.close()

elif section == 'Rechercher un Ordinateur':
    st.markdown('<div class="section-title">Rechercher un Ordinateur</div>', unsafe_allow_html=True)
    numeroSerie_search = st.text_input("Numéro de Série de l'ordinateur à rechercher: ")
    if connection:
        search_computer_by_serial(connection, numeroSerie_search)
        connection.close()

elif section == 'Filtrage':
    filtrage_avance()

elif section == 'Supprimer un Ordinateur':
    st.markdown('<div class="section-title">Supprimer un Ordinateur</div>', unsafe_allow_html=True)
    serial_number_to_delete = st.text_input("Numéro de Série de l'ordinateur à supprimer:")
    if st.button("Supprimer"):
        if serial_number_to_delete:
            if connection:
                delete_computer_and_related_info(connection, serial_number_to_delete)
                connection.close()
        else:
            st.error("Veuillez entrer un numéro de série.")

elif section == 'Modifier un ordinateur':
    st.markdown('<div class="section-title">Modifier un ordinateur</div>', unsafe_allow_html=True)
    if connection:
        modify_computer_info_ui(connection)
        connection.close()
    else:
        st.error("La connexion à la base de données a échoué.")

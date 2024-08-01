from imports import *

def get_computer_statistics(connection):
    try:
        query = """
        SELECT c.numeroSerie, c.brandPc, c.description, e.Prenom, e.Nom, m.AnneeAcquisition, c.RamNumeroCapacite, c.RamUnite, c.DisqueDurNumeroCapacite, c.PortableOuBureauOuAutre
        FROM materiel m
        JOIN caracteristiquesordinateur c ON m.numeroSerie = c.numeroSerie
        LEFT JOIN employe e ON m.IdUtilisateur = e.IdUtilisateur
        """
        df = pd.read_sql(query, connection)
        return df
    except Error as e:
        st.error(f"Error fetching data from MySQL: {e}")
        return None

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
    sns.histplot(df['AnneeAcquisition'], bins=20, kde=False, ax=ax)
    ax.set_title('Distribution des Années d\'Acquisition')
    ax.set_xlabel('Année d\'Acquisition')
    ax.set_ylabel('Nombre d\'Ordinateurs')
    st.pyplot(fig)

def plot_computers_by_type(df):
    type_count = df['PortableOuBureauOuAutre'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=type_count.index, y=type_count.values, ax=ax)
    ax.set_title('Nombre d\'Ordinateurs par Type')
    ax.set_xlabel('Type d\'Ordinateur')
    ax.set_ylabel('Nombre d\'Ordinateurs')
    st.pyplot(fig)

def plot_top_brands(df):
    brand_count = df['brandPc'].value_counts()
    top_brands = brand_count.head(5)
    fig, ax = plt.subplots()
    sns.barplot(x=top_brands.index, y=top_brands.values, ax=ax)
    ax.set_title('Top 5 Marque d\'Ordinateurs')
    ax.set_xlabel('Marque')
    ax.set_ylabel('Nombre d\'Ordinateurs')
    st.pyplot(fig)

def convert_ram_to_gb(value, unit):
    if pd.isna(value):
        return None
    unit = unit.lower()
    if unit == 'go':
        return value
    elif unit == 'mo':
        return value / 1024
    elif unit == 'ko':
        return value / 1048576
    else:
        return None

def plot_ram_distribution(df):
    st.write("Colonnes disponibles dans le DataFrame :", df.columns)
    
    if 'RamNumeroCapacite' in df.columns and 'RamUnite' in df.columns:
        df['RamNumeroCapacite'] = pd.to_numeric(df['RamNumeroCapacite'], errors='coerce')
        
        # Convertir la capacité de RAM en Go en fonction de l'unité
        df['RamNumeroCapacite'] = df.apply(lambda row: convert_ram_to_gb(row['RamNumeroCapacite'], row['RamUnite']), axis=1)
        
        # Affichez les 20 premières lignes pour vérification
        st.write(df[['RamNumeroCapacite', 'RamUnite']].head(20))
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df['RamNumeroCapacite'].dropna(), kde=True, ax=ax)
        ax.set_title('Distribution de la Capacité de RAM')
        ax.set_xlabel('Capacité de RAM (Go)')
        ax.set_ylabel('Nombre d\'Ordinateurs')
        
        st.pyplot(fig)
    else:
        st.error("Les colonnes 'RamNumeroCapacite' et/ou 'RamUnite' sont manquantes dans les données.")

from imports import *
from fonctions.ordinateur.connection import create_connection

connection = create_connection()

def filtrage_avance():
    st.markdown('<div class="section-title">Filtrage</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Aperçu des données :")
        st.dataframe(df)

        columns = df.columns.tolist()
        
        selected_column = st.selectbox("Sélectionnez une colonne pour filtrer", columns)
        column_type = df[selected_column].dtype
        
        filtered_df = df
        
        if column_type == 'object':
            unique_values = df[selected_column].dropna().unique()
            selected_value = st.multiselect(f"Valeurs dans la colonne '{selected_column}'", unique_values)
            if selected_value:
                filtered_df = df[df[selected_column].isin(selected_value)]
        elif column_type == 'int64' or column_type == 'float64':
            min_value = df[selected_column].min()
            max_value = df[selected_column].max()
            if pd.isna(min_value) or pd.isna(max_value):
                st.error(f"La colonne '{selected_column}' contient des valeurs invalides.")
            else:
                selected_range = st.slider(f"Plage de valeurs pour '{selected_column}'", float(min_value), float(max_value), (float(min_value), float(max_value)))
                filtered_df = df[(df[selected_column] >= selected_range[0]) & (df[selected_column] <= selected_range[1])]
        elif column_type == 'datetime64[ns]':
            df[selected_column] = pd.to_datetime(df[selected_column], errors='coerce')
            min_date = df[selected_column].min()
            max_date = df[selected_column].max()
            if pd.isna(min_date) or pd.isna(max_date):
                st.error(f"La colonne '{selected_column}' contient des valeurs de date invalides.")
            else:
                date_range = st.date_input(f"Sélectionnez une plage de dates pour '{selected_column}'", 
                                           [min_date.date(), max_date.date()])
                if len(date_range) == 2:
                    start_date, end_date = date_range
                    filtered_df = df[(df[selected_column] >= pd.to_datetime(start_date)) & (df[selected_column] <= pd.to_datetime(end_date))]

        st.write("Données filtrées :")
        st.dataframe(filtered_df)

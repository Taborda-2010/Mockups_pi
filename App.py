# Se importan las libreías necesarias
import pandas as pd  #version: 2.1.1
import streamlit as st  #version: 1.27.2
import webbrowser

def cargar_dataset():
    '''Función para importar la base de datos
    de las 250 recetas'''
    df = pd.read_csv('db_reducida_spanish.csv')
    return df

# Cargar el conjunto de datos
df = cargar_dataset()

# Establecer estilo y formato personalizado
st.markdown('<h1 style="text-align: left; color: skyblue;">CulinaryCraft</h1>',\
             unsafe_allow_html=True)

# Crear una barra lateral para la tabla de contenidos
st.sidebar.title('Tabla de Contenido')
selected_option = st.sidebar.selectbox(
    'Selecciona una opción:',
    ['Inicio', 'Búsqueda de Recetas por Ingrediente', 'Búsqueda de Recetas por Filtrado']
)

# Interfaz de usuario
if selected_option == 'Inicio':
    st.write('Bienvenido a una aplicación que te ayudará"\
             " a descubrir nuevas recetas de cocina basadas"\
             " en tus ingredientes disponibles y tus preferencias culinarias."\
             " Además podrás filtrar las recetas por categorías y criterios de"\
             " busqueda para excluir ingredientes no deseados.')

elif selected_option == 'Búsqueda de Recetas por Ingrediente':
    st.markdown('<h3 id="busqueda" style="text-align: left; color: white;"\
                " font-style: italic;">Búsqueda de Recetas por Ingrediente</h3>',\
                      unsafe_allow_html=True)
    
    ingrediente = st.text_input('Ingresa un ingrediente:')
    if ingrediente:
        # Filtrar el DataFrame por ingredientes
        df_ingredientes = df[df['NER'].str.contains(ingrediente, case=False, na=False)]
        
        # Mostrar los nombres de las recetas
        if not df_ingredientes.empty:
            st.subheader('Recetas que contienen "{}":'.format(ingrediente))
            for idx, row in df_ingredientes.iterrows():
                st.write(row['título'])
        
elif selected_option == 'Búsqueda de Recetas por Filtrado':
    st.markdown('<h3 id="filtrado" style="text-align: left; color: white;"\
                " font-style: italic;">Búsqueda de Recetas por Filtrado</h3>',\
                      unsafe_allow_html=True)
   
    # Definir el ingrediente "azúcar" para buscar en las recetas
    ingrediente_azucar = "azúcar"

    # Cuadro de entrada para ingredientes a excluir
    ingredientes_a_excluir = st.text_input('Ingresa ingredientes a excluir (separados por comas):')

    # Opción para excluir recetas con azúcar
    excluir_azucar = st.checkbox('Excluir recetas con azúcar')

    if not df.empty:
        for idx, row in df.iterrows():
            mostrar_receta = True
            
            # Verificar si se debe excluir la receta debido a ingredientes excluidos
            if ingredientes_a_excluir:
                ingredientes_excluidos = [ingrediente.strip() for ingrediente in ingredientes_a_excluir.split(',')]
                for ingrediente in ingredientes_excluidos:
                    if ingrediente in row['NER']:
                        mostrar_receta = False
            
            # Verificar si se debe excluir la receta debido al azúcar
            if excluir_azucar and ingrediente_azucar in row['NER']:
                mostrar_receta = False
            
            # Mostrar la receta si no se excluye
            if mostrar_receta:
                receta = st.button(row['título'])
                st.write(row['Ingredientes'])
                
                if receta:
                    # Cuando se hace clic en el botón de la receta, abrir las direcciones en una nueva pestaña
                    webbrowser.open_new_tab(row['Direcciones'])





        

# Se importan las libreías necesarias
import pandas as pd  
# Versión: 2.1.1
import streamlit as st  
# Versión: 1.27.2
from tinydb import TinyDB, Query


def cargar_dataset():
    '''Función para importar la base de datos
    de las 250 recetas'''
    df = pd.read_csv('db_es.csv')
    return df

# NUEVO CÓDIGO
# INICIO ----------------------------------------------------------------

def cargar_dataset_nutricion():
    """
    Función para importar la base de datos
    de los valores nutricionales de los
    ingredientes
    """
    nutr_df = pd.read_csv('db_nutricion.csv', encoding="ISO-8859-1")
    return nutr_df

# Cargar datset de datos nutricionales
nutr_df = cargar_dataset_nutricion()

# FIN ----------------------------------------------------------------



# NUEVO CÓDIGO
# INICIO -------------------------------------------------------------

cf = TinyDB('cf.json')


            
def promedio(receta_nombre, nueva_calificacion):
    try:
        receta = Query()
        busqueda = cf.search(receta.receta == receta_nombre)

        if not busqueda:
            agregar_calificacion(receta_nombre, nueva_calificacion)
            promedio(receta_nombre, nueva_calificacion)
        else:
            # Extraer las calificaciones de la búsqueda
            calificaciones = [item['Calificación'] for item in busqueda]

            # Filtrar calificaciones válidas (números)
            calificaciones_validas = [float(cal) for cal in calificaciones if cal.replace(".", "", 1).isdigit()]

            # Verificar si hay calificaciones antes de calcular el promedio
            if calificaciones_validas:
                promedio_calificaciones = sum(calificaciones_validas) / len(calificaciones_validas)
                return promedio_calificaciones
            else:
                return None  # No hay calificaciones válidas para calcular el promedio
    except Exception as e:
        st.warning(f"Error en la función promedio: {e}")
        return None

def agregar_calificacion(receta_nombre, nueva_calificacion):
    #tabla = tabla_recetas
    receta = Query()
    
    cf.insert({'Título': receta_nombre,'Calificación':nueva_calificacion})
    #resultado = tabla_recetas.get(receta.Nombre == receta_nombre)
    
    



# Ejemplo de cómo agregar una calificación





# FIN ----------------------------------------------------------------

# Cargar el conjunto de datos
df = cargar_dataset()


# Establecer estilo y formato personalizado
st.markdown('<h1 style="text-align: left; color: skyblue;">CulinaryCraft</h1>',\
             unsafe_allow_html=True)

# Crear una barra lateral para la tabla de contenidos
st.sidebar.title('Tabla de Contenido')
selected_option = st.sidebar.selectbox(
    'Selecciona una opción:',
    ['Inicio', 'Búsqueda por Nombre de Receta','Búsqueda de Recetas por Ingrediente', 'Búsqueda de Recetas por Filtrado']
)

# VALOR NUTRICIONAL
# INICIO --------------------------------
# Crear nueva columna con los valores separados por & para que sea una lista
df['NER_separados'] = df['NER'].str.split('&')
nutr_df['name'] = nutr_df['name'].str.split('&')

# Realizar unión basada en la coincidencia de ingredientes
valor_nutricional = df.explode('NER_separados').merge(
    nutr_df.explode('name'),
    left_on = 'NER_separados',
    right_on = 'name',
    how = 'left'
)
# FIN ----------------------------------------------------------------


# Interfaz de usuario
if selected_option == 'Inicio':
    st.write('Bienvenido a una aplicación que te ayudará\
              a descubrir nuevas recetas de cocina basadas\
              en tus ingredientes disponibles y tus preferencias culinarias.\
              Además podrás filtrar las recetas por categorías y criterios de\
              busqueda para excluir ingredientes no deseados.')

    # Ventana tratamiento de datos
    st.markdown('<h3 style="text-align: left; color: skyblue;"\
        ">Política de Tratamiento de Datos Personales</h3>', unsafe_allow_html=True)
    
    # Ruta al archivo de texto
    archivo_txt = "Politica_tratamiento_de_datos.txt"
    with open(archivo_txt, "r") as file:
        contenido = file.read()
    st.write(contenido)

    # Crear dos columnas para los checkboxes
    col1, col2 = st.columns(2)

    # Opciones para aceptar o denegar
    aceptar = col1.checkbox("Acepto los términos y condiciones")
    denegar = col2.checkbox("Deniego los términos y condiciones")

    # Mensaje de confirmación o denegación
    # Mensaje de confirmación o denegación
    if aceptar:
        st.success("¡Has aceptado los términos y condiciones!")
    else:
        st.warning("Debes aceptar los términos y condiciones para continuar.")

    # Resto de la aplicación
    if aceptar:
        # Aquí puedes continuar con el resto de tu aplicación si el usuario acepta
        pass

# Sección de Búsqueda de Recetas por Ingrediente
elif selected_option == 'Búsqueda por Nombre de Receta':
    st.markdown('<h3 id="busqueda" style="text-align: left; color: white;"\
                " font-style: italic;">Búsqueda por Nombre de Receta</h3>',\
                      unsafe_allow_html=True)
    
    nombre = st.text_input('Ingresa el nombre:')
    if nombre:
        # Filtrar el DataFrame por ingredientes
        df_titulo = df[df['Título'].str.contains(nombre, case=False, na=False)]
        
         # Páginas de recetas
        recetas_por_pagina = 10  # Cantidad de recetas por página
        pagina = st.number_input('Página', min_value=1, value=1)

        # Mostrar los nombres de las recetas
        if not df_titulo.empty:
            st.subheader('Recetas que contienen "{}":'.format(nombre))
  
            # Filtrar recetas si es necesario (según ingredientes excluidos y opción de azúcar)
            recetas_filtradas = []
            for idx, row in df_titulo.iterrows():
                #mostrar_receta = True
                recetas_filtradas.append(row)

        # Calcular los índices de inicio y fin para la página actual
        inicio = (pagina - 1) * recetas_por_pagina
        fin = min(inicio + recetas_por_pagina, len(recetas_filtradas))

        if recetas_filtradas:
            st.write(f"Mostrando recetas {inicio + 1} - {fin} de {len(recetas_filtradas)}")
            for idx in range(inicio, fin):
                row = recetas_filtradas[idx]

                titulo = row['Título']

                # Mostrar la receta si no se excluye
                st.markdown(f'<h4 id="filtrado" style="text-align: left; color: skyblue;"\
                " font-style: italic;">{titulo}</h4>',\
                      unsafe_allow_html=True)

                # Agregar una sección de detalles emergente
                with st.expander(f'Detalles de la receta: {row["Título"]}', expanded=False):
                    # Impresion de Calificación
                    #####################################

                    # Consultar la calificación promedio de una receta
                    receta_consultada = row["Título"]
       
                    #####################################
                    # Impresion de ingredientes
                    ingredientes = row['Ingredientes'].split('&')

                    st.markdown(f'<h5 id="filtrado" style="text-align: left; color: skyblue;"\
                " font-style: italic;">Ingredientes:</h5>',\
                      unsafe_allow_html=True)

                    for i in range(len(ingredientes)):
                        st.write(i+1 , ingredientes[i] )

                    # Impresion de preparación
                    preparacion = row['Preparacion'].split('&')

                    st.markdown(f'<h5 id="filtrado" style="text-align: left; color: skyblue;"\
                " font-style: italic;">Preparación paso a paso:</h5>',\
                      unsafe_allow_html=True)

                    for i in range(len(preparacion)):
                        st.write(i+1 , preparacion[i] )


                    #Nueva calificación
                    #####################################
                    calificacion = st.number_input(f"¿Cuánto le pones a esta receta {row['Título']} del 1 al 5?:")

                    if calificacion:
                        agregar_calificacion(row['Título'], calificacion)

                        titulo = str(row['Título'])

                        prom = promedio(titulo,calificacion)
                        
                        imp = f'Tu calificación es {calificacion} y el promedio de calificación de esta receta es {prom} '
                        st.success(imp)

                    
                    #####################################

    cf.close()

# Sección de Búsqueda de Recetas por Ingrediente
elif selected_option == 'Búsqueda de Recetas por Ingrediente':
    st.markdown('<h3 id="busqueda" style="text-align: left; color: white;"\
                " font-style: italic;">Búsqueda de Recetas por Ingrediente</h3>',\
                      unsafe_allow_html=True)
    
    ingrediente = st.text_input('Ingresa un ingrediente:')
    if ingrediente:
        # Filtrar el DataFrame por ingredientes
        df_ingredientes = df[df['Ingredientes'].str.contains(ingrediente, case=False, na=False)]
        
         # Páginas de recetas
        recetas_por_pagina = 10  # Cantidad de recetas por página
        pagina = st.number_input('Página', min_value=1, value=1)

        # Mostrar los nombres de las recetas
        if not df_ingredientes.empty:
            st.subheader('Recetas que contienen "{}":'.format(ingrediente))
  
            # Filtrar recetas si es necesario (según ingredientes excluidos y opción de azúcar)
            recetas_filtradas = []
            for idx, row in df_ingredientes.iterrows():
                #mostrar_receta = True
                recetas_filtradas.append(row)

            # Calcular los índices de inicio y fin para la página actual
            inicio = (pagina - 1) * recetas_por_pagina
            fin = min(inicio + recetas_por_pagina, len(recetas_filtradas))

            if recetas_filtradas:
                st.write(f"Mostrando recetas {inicio + 1} - {fin} de {len(recetas_filtradas)}")
                for idx in range(inicio, fin):

                    # 'row' es la variable que guarda la receta actual
                    row = recetas_filtradas[idx]

                    titulo = row['Título']

                    # NUEVA VARIABLE PARA VALOR NUTRICIONAL
                    ingredientes_receta = row['NER'].split('&')

                    # Mostrar la receta si no se excluye
                    st.markdown(f'<h4 id="filtrado" style="text-align: left; color: skyblue;"\
                    " font-style: italic;">{titulo}</h4>',\
                        unsafe_allow_html=True)
                    
                    # INICIO ----------------------------------------------------------------

                    # Lista para almacenar el valor nutricional de cada ingrediente
                    nutricional = []

                    for ingrediente in ingredientes_receta:
                        info_nutricional = valor_nutricional[valor_nutricional['name'] == ingrediente]
                        calorias = info_nutricional['calories'].values[0] if not info_nutricional.empty else "No encontrado"

                        nutricional.append({'Ingrediente' : ingrediente, 'Calorías' : calorias})

                    # convirtiendo lista en un dataframe para mostrarlo como tabla
                    tabla_valor_nutricional = pd.DataFrame(nutricional)

                    # FIN ----------------------------------------------------------------

                    # Agregar una sección de detalles emergente
                    with st.expander(f'Detalles de la receta: {row["Título"]}', expanded=False):

                        # Impresion de ingredientes
                        ingredientes = row['Ingredientes'].split('&')

                        st.markdown(f'<h5 id="filtrado" style="text-align: left; color: skyblue;"\
                    " font-style: italic;">Ingredientes:</h5>',\
                        unsafe_allow_html=True)

                        for i in range(len(ingredientes)):
                            st.write(i+1 , ingredientes[i] )

                        # Impresion de preparación
                        preparacion = row['Preparacion'].split('&')

                        st.markdown(f'<h5 id="filtrado" style="text-align: left; color: skyblue;"\
                    " font-style: italic;">Preparación paso a paso:</h5>',\
                        unsafe_allow_html=True)

                        for i in range(len(preparacion)):
                            st.write(i+1 , preparacion[i] )

                        # Aquí colocamos la tabla del valor nutricional de los ingredientes
                        st.write(tabla_valor_nutricional)        
        else:
            st.write("No se encontraron resultados.")


           
# Sección Búsqueda de Recetas por Filtrado
elif selected_option == 'Búsqueda de Recetas por Filtrado':
    st.markdown('<h3 id="filtrado" style="text-align: left; color: white;"\
                " font-style: italic;">Búsqueda de Recetas por Filtrado</h3>',\
                      unsafe_allow_html=True)
   
    # Cuadro de entrada para ingredientes a excluir
    ingredientes_a_excluir = st.text_input('Ingresa ingredientes a excluir (separados por comas):')

    # Definir el ingrediente "azúcar" para buscar en las recetas
    ingrediente_azucar = "azúcar"

    # Opción para excluir recetas con azúcar
    excluir_azucar = st.checkbox('Excluir recetas con azúcar')

    # Definir la lista de ingredientes no vegetarianos
    ingredientes_no_vegetarianos = ["pollo", "carne", "pavo"]

    #FILTRO VEGETARIANO
    # Opción para excluir recetas no vegetarianas
    excluir_no_vegetarianas = st.checkbox('Excluir recetas no vegetarianas')

    # Páginas de recetas
    recetas_por_pagina = 10  # Cantidad de recetas por página
    pagina = st.number_input('Página', min_value=1, value=1)

    if not df.empty:
        # Filtrar recetas si es necesario (según ingredientes excluidos y opción de azúcar)
        recetas_filtradas = []
        for idx, row in df.iterrows():
            mostrar_receta = True

            # Verificar si se debe excluir la receta debido a ingredientes excluidos
            if ingredientes_a_excluir:
                ingredientes_excluidos = [ingrediente.strip() for ingrediente in ingredientes_a_excluir.split(',')]
                for ingrediente in ingredientes_excluidos:
                    if ingrediente in row['ingredientes']:
                        mostrar_receta = False

            # Verificar si se debe excluir la receta debido al azúcar
            if excluir_azucar and ingrediente_azucar in row['Ingredientes']:
                mostrar_receta = False

            # Verificar si se debe excluir la receta debido a ingredientes no vegetarianos
            if excluir_no_vegetarianas and ((ingredientes_no_vegetarianos[0] or ingredientes_no_vegetarianos[1] or ingredientes_no_vegetarianos[2]) in row['Ingredientes']):
                mostrar_receta = False

            # Agregar la receta a la lista si no se excluye
            if mostrar_receta:
                recetas_filtradas.append(row)

        # Calcular los índices de inicio y fin para la página actual
        inicio = (pagina - 1) * recetas_por_pagina
        fin = min(inicio + recetas_por_pagina, len(recetas_filtradas))

        if recetas_filtradas:
            st.write(f"Mostrando recetas {inicio + 1} - {fin} de {len(recetas_filtradas)}")
            for idx in range(inicio, fin):
                row = recetas_filtradas[idx]

                titulo = row['Título']

                # Mostrar la receta si no se excluye
                st.markdown(f'<h4 id="filtrado" style="text-align: left; color: skyblue;"\
                " font-style: italic;">{titulo}</h4>',\
                      unsafe_allow_html=True)

                # Agregar una sección de detalles emergente
                with st.expander(f'Detalles de la receta: {row["Título"]}', expanded=False):

                    # Impresion de ingredientes
                    ingredientes = row['Ingredientes'].split('&')

                    st.markdown(f'<h5 id="filtrado" style="text-align: left; color: skyblue;"\
                " font-style: italic;">Ingredientes:</h5>',\
                      unsafe_allow_html=True)

                    for i in range(len(ingredientes)):
                        st.write(i+1 , ingredientes[i] )

                    # Impresion de preparación
                    preparacion = row['Preparacion'].split('&')

                    st.markdown(f'<h5 id="filtrado" style="text-align: left; color: skyblue;"\
                " font-style: italic;">Preparación paso a paso:</h5>',\
                      unsafe_allow_html=True)

                    for i in range(len(preparacion)):
                        st.write(i+1 , preparacion[i] )

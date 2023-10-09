import streamlit as st

# Crear una barra superior personalizada con HTML


# Contenido de la aplicación
st.title("Mi Aplicación Streamlit")
st.write("Este es el contenido de la aplicación.")


# Datos de ejemplo de recetas con sus respectivos ingredientes
recetas = {
    'Pasta con salsa de tomate': ['pasta', 'tomate', 'queso'],
    'Ensalada César': ['lechuga', 'pollo', 'crutones', 'aderezo'],
    'Pizza Margarita': ['masa de pizza', 'tomate', 'mozzarella', 'albahaca'],
    'Pata con salsa alfredo': ['pasta', 'mantequilla', 'crema de leche', 'nuez moscada']
}

# Establecer estilo y formato personalizado
st.markdown('<h1 style="text-align: left; color: skyblue;">CulinaryCraft</h1>', unsafe_allow_html=True)

# Crear una barra lateral para la tabla de contenidos
st.sidebar.title('Tabla de Contenido')
selected_option = st.sidebar.selectbox(
    'Selecciona una opción:',
    ['Inicio', 'Búsqueda de Recetas por Ingrediente', 'Búsqueda de Recetas por Filtrado']
)

# Interfaz de usuario
if selected_option == 'Inicio':
    st.write('Bienvenido a una aplicación que te ayudará a descubrir nuevas recetas de cocina basadas en tus ingredientes disponibles y tus preferencias culinarias. Además podrás filtrar las recetas por categorías y criterios de busqueda para excluir ingredientes no deseados.')
    st.markdown("""
    <style>
        .custom-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #333;
            color: white;
            padding: 10px;
        }
        .logo {
            font-size: 24px;
            font-weight: bold;
        }
        .links {
            list-style-type: none;
            margin: 0;
            padding: 0;
            display: flex;
        }
        .links li {
            margin-right: 20px;
        }
        .links a {
            color: white;
            text-decoration: none;
        }
    </style>
    <div class="custom-bar">
        <div class="logo">Mi Aplicación Streamlit</div>
        <ul class="links">
            <li><a href="#">Inicio</a></li>
            <li><a href="#">Acerca de</a></li>
            <li><a href="#">Contacto</a></li>
        </ul>
    </div>
""", unsafe_allow_html=True)

elif selected_option == 'Búsqueda de Recetas por Ingrediente':
    st.markdown('<h2 id="busqueda" style="text-align: left; color: white; font-style: italic;">Búsqueda de Recetas por Ingrediente</h2>', unsafe_allow_html=True)
    
    ingredientes = st.text_input('Ingresa ingredientes separados por comas:')
    ingredientes = [ing.strip() for ing in ingredientes.split(',')]  # Convertir la entrada en una lista
    
    if ingredientes:
        st.write(f'Recetas que incluyen los siguientes ingredientes: {", ".join(ingredientes)}')
        for receta, ingredientes_receta in recetas.items():
            if all(ing.lower() in [ingr.lower() for ingr in ingredientes_receta] for ing in ingredientes):
                st.markdown(f'**{receta}**', unsafe_allow_html=True)
                st.write('Ingredientes:', ", ".join(ingredientes_receta))
                
elif selected_option == 'Búsqueda de Recetas por Filtrado':
    st.markdown('<h2 id="filtrado" style="text-align: left; color: white; font-style: italic;">Búsqueda de Recetas por Filtrado</h2>', unsafe_allow_html=True)
    st.write('Ingresa los ingredientes que deseas excluir:')
    ingredientes_excluir = st.text_input('Ingredientes a excluir (separados por comas):')
    
    # Convertir la entrada en una lista de ingredientes a excluir
    ingredientes_excluir = [ingrediente.strip() for ingrediente in ingredientes_excluir.split(',')]
    
    if ingredientes_excluir:
        st.write(f'Recetas que no contienen los siguientes ingredientes: {", ".join(ingredientes_excluir)}')
        for receta, ingredientes in recetas.items():
            if not any(ing.lower() in ingredientes_excluir for ing in ingredientes):
                st.markdown(f'**{receta}**', unsafe_allow_html=True)
                st.write('Ingredientes:', ", ".join(ingredientes))
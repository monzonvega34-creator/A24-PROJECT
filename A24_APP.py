import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="A24 STUDIO",
    page_icon="A24_LOGO.png",
    layout="wide"
)

@st.cache_data
def cargar_datos():
    a24 = pd.read_csv("A24.csv")
    a24.dropna(inplace=True)

    return a24
a24 = cargar_datos()

st.title("¿ESTÁ A24 STUDIO INVIRTIENDO EN LAS PELÍCULAS CORRECTAS?")
col1, col2, col3 = st.columns([10, 10, 10])
with col2:
    st.image("PANEL A24.png",width=2000)

st.markdown("""
<div style="font-size:20px; line-height:1.5; color:#1a1a1a; text-align:justify;">
<br><br>
<b>
 A24 es una productora de cine independiente fundada en 2012 en Nueva York por Daniel Katz, David Fenkel 
y John Hodges, tres ejecutivos con amplia experiencia en la industria del entretenimiento. En poco más de 
una década, la compañía ha distribuido más de 100 películas y 3 series originales, consolidándose como 
una de las casas productoras más influyentes y reconocibles del cine contemporáneo a nivel mundial.
<br><br>
Lo que distingue a A24 del resto de Hollywood no es solo su catálogo, sino su modelo de negocio: 
apuesta por presupuestos bajos, directores con visión autoral y géneros de nicho — terror psicológico, 
drama independiente y comedia oscura — que los grandes estudios suelen ignorar. Esta filosofía le ha 
permitido obtener un retorno de inversión (ROI) muy superior al promedio de la industria, convirtiendo 
películas de bajo costo en fenómenos culturales y taquilleros.
<br><br>
En términos de reconocimiento, A24 acumula múltiples premios Óscar, incluyendo Mejor Película con 
Moonlight (2017) y Everything Everywhere All at Once (2023), esta última con 7 estatuillas en una sola 
noche — la mayor cosecha en la historia de la compañía. Su catálogo incluye títulos de culto como 
Hereditary, Midsommar, The Lighthouse y Uncut Gems, que han redefinido géneros enteros.
<br><br>
En 2022, A24 captó la atención de Wall Street al cerrar una ronda de capital privado (Private Equity) 
valuada en más de 2,000 millones de dólares, según datos de Bloomberg Businessweek. Para 2024, 
su valuación ya superaba los 3,500 millones de dólares, respaldada por una nueva ronda liderada por 
Thrive Capital de Joshua Kushner. Esta entrada de capital institucional abre un debate estratégico 
central: ¿puede A24 escalar hacia el mainstream sin perder la identidad creativa que la hizo grande?
<br><br>
Este proyecto busca responder una pregunta concreta utilizando datos: ¿está A24 invirtiendo en las 
películas correctas? A través de la Matriz BCG como marco de análisis estratégico, se identifican 
los caballos ganadores del catálogo de A24 Studio, evaluando cada película en términos de presupuesto, 
taquilla mundial, género y reconocimiento en premios — para determinar dónde está el verdadero valor 
de su portafolio.
</b>
<br><br>
<br><br>      
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([10, 10, 10])
with col2:
    st.image("BLOOMBERG BUSINESSWEEK.jpg",width=1500)

st.divider()


# ────────────────────────────────────────
#  LIMPIEZA DE DATOS
# ─────────────────────────────────────────


# Gráfica 1 — Barras: Películas por año
df_año = (
    a24.groupby("AÑO ESTRENO")
    .size()
    .reset_index(name="total_peliculas")
    .sort_values("AÑO ESTRENO")
)
df_año["AÑO ESTRENO"] = df_año["AÑO ESTRENO"].astype(int)

# Gráfica 2 — Líneas: Presupuesto vs Taquilla por año
df_tiempo = (
    a24.groupby("AÑO ESTRENO")
    .agg(
        presupuesto=("PRESUPUESTO",      "sum"),
        taquilla   =("TAQUILLA MUNDIAL", "sum"),
    )
    .reset_index()
    .sort_values("AÑO ESTRENO")
)
df_tiempo["AÑO ESTRENO"] = df_tiempo["AÑO ESTRENO"].astype(int)

# Gráfica 3 — Treemap: Total por género
df_tree = (
    a24.groupby("GENERO")
    .size()
    .reset_index(name="total")
    .sort_values("total", ascending=False)
)

# Gráfica 4 — Burbujas: Películas ganadoras del Oscar

df_oscar = (
    a24[a24["OSCAR"] == "YES"]
    .sort_values("AÑO ESTRENO", ascending=True)
    .reset_index(drop=True)
)
# Gráfica 6 — Dispersión: Taquilla vs Presupuesto
df_scatter = a24.copy()
df_scatter["oscar_bool"] = df_scatter["OSCAR"] == "YES"


# ─────────────────────────────────────────
#  GRÁFICAS
# ─────────────────────────────────────────

# ── Gráfica 1: Películas por año ─────────────────────────────────────────────
st.markdown("""
<div style="font-size:20px; font-weight:bold; text-align: justify;">
</b><br><br>
A24 inició operaciones en 2013 con una presencia modesta de apenas 5 producciones, pero rápidamente consolidó su catálogo alcanzando su primer pico en 2016 con 18 títulos y su máximo histórico en 2019 con 20 producciones.  
<br><br>
La llegada de la pandemia en 2020 representó un freno abrupto, reduciendo su producción a solo 2 títulos. Sin embargo, este período de pausa forzada tuvo un efecto inesperado: mientras el mundo se refugiaba en plataformas de streaming, las audiencias jóvenes redescubrieron el catálogo de A24, consolidándola no como una productora más, sino como un referente cultural del cine de autor independiente.  
<br><br>
Este capital de marca acumulado durante la pandemia impulsó una recuperación sostenida desde 2021, llegando nuevamente a 15 producciones en 2022 — una señal clara de que A24 aprendió a operar en un ecosistema cinematográfico transformado.
</div></b><br><br>
""", unsafe_allow_html=True)

fig1 = go.Figure()

fig1.add_trace(
    go.Bar(
        x=df_año["AÑO ESTRENO"],
        y=df_año["total_peliculas"],
        marker=dict(
            color="#e8c832",
            line=dict(width=1, color="#e8c832"),
        ),
        text=df_año["total_peliculas"],
        textposition="outside",
        textfont=dict(color="#1a1a1a", size=20),          
        hovertemplate="<b>Año: %{x}</b><br>Películas: %{y}<extra></extra>",
    )
)

fig1.update_layout(
    title=dict(
        text="<b>PRODUCCIONES POR AÑO</b><br><sup>Total de producciones por año</sup>",
        font=dict(size=20, color="#1a1a1a", family="Arial Black"),  
        x=0.5, xanchor="center", y=0.97,
    ),
                                   
    xaxis=dict(
        title="Año de Estreno", color="#1a1a1a",           
        gridcolor="rgba(0,0,0,0.08)",                      
        tickmode="linear", tickangle=0, dtick=1,
        tickfont=dict(size=13),
        title_font=dict(size=14),
    ),
    yaxis=dict(
        title="Total de Películas", color="#1a1a1a",       
        gridcolor="rgba(0,0,0,0.1)",
        tickfont=dict(size=13),
        title_font=dict(size=14),                       
    ),
    font=dict(color="#1a1a1a"),                            
    margin={"r": 40, "t": 100, "l": 60, "b": 80},
    height=750,
)

st.plotly_chart(fig1)
st.divider()

# ── Gráfica 2: Presupuesto vs Taquilla por año ───────────────────────────────
st.markdown("""
<div style="font-size:20px; font-weight:bold; text-align: justify;">
</b><br><br>
A24 atravesó una etapa de inversión inicial (2013–2014) donde los presupuestos superaban los ingresos de taquilla. El punto de equilibrio llegó con el reconocimiento de la Academia: el Oscar a Mejores Efectos Visuales por Ex Machina en 2016 marcó el inicio de una etapa de madurez (2015–2019), donde la brecha entre presupuesto y taquilla comenzó a invertirse consistentemente a favor del estudio.  
<br><br>
El colapso de 2020 es contundente en la gráfica: la taquilla casi desaparece mientras los presupuestos también se contraen al mínimo. A partir de 2021, los ingresos crecen de forma sostenida mientras los presupuestos permanecen bajos, lo que apunta a una estrategia deliberada: apostar por producciones de bajo costo con alto potencial de retorno cultural y comercial.
</div></b><br><br>
""", unsafe_allow_html=True)

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=df_tiempo["AÑO ESTRENO"], y=df_tiempo["presupuesto"],
    name="Presupuesto", mode="lines+markers",
    line=dict(color="#c0152a", width=10),
    hovertemplate="<b>%{x}</b><br>Presupuesto: $%{y:,.0f}<extra></extra>",
))

fig2.add_trace(go.Scatter(
    x=df_tiempo["AÑO ESTRENO"], y=df_tiempo["taquilla"],
    name="Taquilla Mundial", mode="lines+markers",
    line=dict(color="#e8c832", width=10),
    hovertemplate="<b>%{x}</b><br>Taquilla: $%{y:,.0f}<extra></extra>",
))

fig2.update_layout(
    title=dict(
        text="<b>PRESUPUESTO VS TAQUILLA MUNDIAL POR AÑO</b><br><sup>Evolución financiera del estudio por año de estreno</sup>",
        font=dict(size=20, color="#1a1a1a", family="Arial Black"),  
        x=0.5, xanchor="center", y=0.97,
    ),
   
    xaxis=dict(
        title="Año de Estreno", color="#1a1a1a",           
        gridcolor="rgba(0,0,0,0.08)",
        tickmode="linear", tickangle=0, dtick=1,
        tickfont=dict(size=20),
        title_font=dict(size=20),
    ),
    yaxis=dict(
        title="Monto", color="#1a1a1a",  
        gridcolor="rgba(0,0,0,0.1)",
        type="log", tickformat="$,.0f", exponentformat="none",
        tickfont=dict(size=20),
        title_font=dict(size=20),
    ),
    legend=dict(
        orientation="v",
        x=1.12,
        xanchor="left",
        y=1,
        yanchor="top",
        font=dict(size=20),
    ),
    font=dict(color="#1a1a1a"),                            
    margin={"r": 40, "t": 100, "l": 80, "b": 80},
    height=750,
)

st.plotly_chart(fig2)
st.divider()

# ── Gráfica 3: BURBUJAS por género ────────────────────────────────────────────
# ── CÁLCULO DINÁMICO: % que representa Ne Zha II del total de taquilla 2025 ──
taquilla_2025 = a24[a24["AÑO ESTRENO"] == 2025]["TAQUILLA MUNDIAL"].sum()
nezha_taquilla = a24[a24["TITULO"].str.contains("Ne Zha", case=False, na=False)]["TAQUILLA MUNDIAL"].sum()
pct_nezha = (nezha_taquilla / taquilla_2025 * 100) if taquilla_2025 > 0 else 0

st.markdown(f"""
<div style="font-size:20px; font-weight:bold; text-align: justify;">
</b><br><br>
El tamaño de cada burbuja revela la cantidad de producciones por género, mientras su posición vertical muestra el retorno en taquilla.  
<br><br>
Drama, Horror y Comedia forman el núcleo productivo de A24 — los géneros donde el estudio ha construido su identidad y concentra la mayor parte de su catálogo.  
<br><br>
Animation aparece casi solitaria en las alturas, con más de $2,500 Billones en taquilla y una burbuja relativamente pequeña, lo que indica pocas películas con un retorno extraordinario. Este es el unicornio del portafolio de A24: <em>Ne Zha II</em>, un fenómeno cultural en China que capitalizó la profunda conexión de una nación de más de 1 billón de personas con su mitología y tradición religiosa.  
<br><br>
Solo este título representa aproximadamente el <b>{pct_nezha:.0f}%</b> de toda la taquilla acumulada de A24 en <b>2025</b>.
</div>
</b><br><br>
""", unsafe_allow_html=True)
df_bubble = (
    a24.groupby("GENERO")
    .agg(
        TOTAL_PELICULAS=("TITULO", "count"),
        TAQUILLA_TOTAL=("TAQUILLA MUNDIAL", "sum"),
    )
    .reset_index()
)
 
fig3 = go.Figure()
 
fig3.add_trace(go.Scatter(
    x=df_bubble["GENERO"],
    y=df_bubble["TAQUILLA_TOTAL"],
    mode="markers",
    name="Género",
    marker=dict(
        size=df_bubble["TOTAL_PELICULAS"] / df_bubble["TOTAL_PELICULAS"].max() * 50 + 60,
        color=df_bubble["TOTAL_PELICULAS"],                                 
        colorscale=[[0, "#2d6e3a"], [0.5, "#e8c832"], [1, "#c0152a"]],
        showscale=True,
        colorbar=dict(
            title=dict(text="Total de Películas", font=dict(size=15)),   
            tickfont=dict(size=15),
            x=1.02,
        ),
        line=dict(width=0),
        gradient=dict(type="radial", color="white"),
        opacity=1
    ),
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Taquilla Total: $%{y:,.0f}<br>"
        "Películas: %{customdata}<br>"
        "<extra></extra>"
    ),
    customdata=df_bubble["TOTAL_PELICULAS"],
))
 
fig3.update_layout(
    title=dict(
        text="<b>BURBUJAS POR GÉNERO</b><br><sup>Tamaño proporcional al número de películas</sup>",
        font=dict(size=25, color="#1a1a1a"),
        x=0.5, xanchor="center", y=0.97,
    ),
    xaxis=dict(
        title=dict(text="Género", font=dict(size=20)),
        tickfont=dict(size=20),
        tickangle=-45,
        showgrid=False,
        automargin=True,

    ),
    yaxis=dict(
        title=dict(text="Taquilla Total ($)", font=dict(size=20)),          
        tickfont=dict(size=20),
        gridcolor="rgba(0,0,0,0.1)",
        gridwidth=1,
        tickformat="$,.0f",                                                                  
    ),
    legend=dict(
        orientation="v",
        x=1.12,
        xanchor="left",
        y=1,
        yanchor="top",
        font=dict(size=10),
    ),
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    height=750,
)


st.plotly_chart(fig3)
st.divider()
 
 ##################### grafica de oscares ###########
st.markdown("""
<div style="font-size:20px; font-weight:bold; text-align: justify;">
</b><br><br>
Ex Machina (2016) ganó el Oscar a Mejores Efectos Visuales, superando a producciones de gran presupuesto como Mad Max: Fury Road, The Martian y Star Wars.  
<br><br>
Room (2016) le dio a Brie Larson el Oscar a Mejor Actriz, mientras que Amy ganó como Mejor Documental, consolidando la presencia de A24 en distintos géneros.  
<br><br>
Minari (2021) obtuvo el premio a Mejor Actriz de Reparto para Youn Yuh-jung, y The Whale (2023) marcó el regreso de Brendan Fraser con el Oscar a Mejor Actor.  
<br><br>
El punto culminante llegó con Everything Everywhere All at Once (2023), que ganó 7 premios Oscar, posicionando a A24 como uno de los estudios más relevantes de la industria.
</b><br><br>
</div>
""", unsafe_allow_html=True)




fig4 = go.Figure()
 
fig4.add_trace(go.Scatter(
    x=df_oscar["TITULO"], y=df_oscar["PRESUPUESTO"],
    mode="markers", name="Presupuesto",
    marker=dict(
        size=df_oscar["PRESUPUESTO"],
        sizemode="area",
        sizeref=2 * df_oscar["PRESUPUESTO"].max() / (50**2),
        sizemin=20,
        color="#c0152a",
        line=dict(width=0),
        gradient=dict(type="radial", color="white"),
        opacity=1       
    ),
    hovertemplate="<b>%{x}</b><br>Presupuesto: $%{y:,.0f}<extra></extra>",
))
 
fig4.add_trace(go.Scatter(
    x=df_oscar["TITULO"], y=df_oscar["TAQUILLA MUNDIAL"],
    mode="markers", name="Taquilla Mundial",
    marker=dict(
        size=df_oscar["TAQUILLA MUNDIAL"],
        sizemode="area",
        sizeref=2 * df_oscar["PRESUPUESTO"].max() / (50**2),
        sizemin=20,
        color="#e8c832",
        line=dict(width=0),
        gradient=dict(type="radial", color="white"),
        opacity=1,     
    ),
    hovertemplate="<b>%{x}</b><br>Taquilla: $%{y:,.0f}<extra></extra>",
))
 
fig4.update_layout(
    title=dict(
        text="<b>PELÍCULAS GANADORAS DEL ÓSCAR</b><br><sup>Presupuesto vs taquilla mundial de las películas premiadas</sup>",
        font=dict(size=20, color="#1a1a1a", family="Arial Black"),
        x=0.5, xanchor="center", y=0.97,
    ),
    xaxis=dict(
        title=dict(text="Película", font=dict(size=15)),
        tickfont=dict(size=15),
        color="#1a1a1a",
        tickangle=-45,
        automargin=True,
        gridcolor="rgba(0,0,0,0.08)",
        categoryorder="array",
        categoryarray=df_oscar["TITULO"].tolist(),
    ),
    yaxis=dict(
        title=dict(text="Monto", font=dict(size=15)),
        tickfont=dict(size=15),
        color="#1a1a1a",
        gridcolor="rgba(0,0,0,0.1)",
        tickformat="$,.0f",
        exponentformat="none",
    ),
    legend=dict(
        orientation="v",
        x=1.02, xanchor="left",
        y=1, yanchor="top",
        font=dict(size=25),
    ),
    font=dict(color="#1a1a1a"),
    margin=dict(r=150, t=100, l=60, b=100),
    height=800,
)
 
st.plotly_chart(fig4)
st.divider()

# ── Gráfica 7: Top 10 directores por ROI ─────────────────────────────────────

st.markdown("""
<div style="font-size:20px; font-weight:bold; text-align: justify;">
</b><br><br>
A24 no solo creció en ingresos, aprendió a invertir mejor. Durante sus primeros años, el estudio operaba con retornos modestos y variables, apostando por volumen para construir catálogo y reputación. El colapso de 2020 (0.22x) marcó el punto más bajo, pero también el punto de inflexión: a partir de 2021, los retornos comenzaron a escalar de forma sostenida, alcanzando 8.24x en 2023 y disparándose a 65.02x en 2025, impulsado en gran parte por el fenómeno <em>Ne Zha II</em> en el mercado chino.  
<br><br>
Animation lidera de forma aplastante con 126.23x — un resultado extraordinario que, como ya sabemos, está sostenido por el unicornio Ne Zha II. Sin embargo, lo más relevante está en los géneros que siguen: Drama (3.68x), Horror (3.15x) y Biographical Drama (2.83x) representan los motores reales y consistentes del portafolio.  
<br><br>
El Horror merece atención especial: con presupuestos naturalmente bajos y audiencias leales, es el género de mayor eficiencia operativa del catálogo. Por debajo de 1x aparecen géneros como Romance, Action y Mystery, territorios donde A24 ha explorado con libertad creativa, pero sin retorno consistente.  
<br><br>
A nivel de directores, Jiaozi (director de Ne Zha II) encabeza la lista con un ROI de 376x — un caso atípico que refleja el poder de conectar con las masas. Siguiendo Barry Jenkins (43.56x, Moonlight), los hermanos Philippou (20.43x, Talk to Me), y nombres como Darren Aronofsky, Greta Gerwig y Lulu Wang, todos por encima de 7x.  
<br><br>
Ne Zha II (376x) es el outlier evidente. Siguiendo Moonlight con 43.56x (con un presupuesto de apenas $4,000,000), Talk to Me con 20.43x, A Ghost Story con 19.52x, y referentes del horror como The Witch (10.11x) y Hereditary (8.02x).
</div>
</b><br><br>
""", unsafe_allow_html=True)


# ROI General por Año (serie de tiempo)
df_año = a24.copy()
df_año["ROI_IND"] = df_año["TAQUILLA MUNDIAL"] / df_año["PRESUPUESTO"]
df_año = (
    df_año.groupby("AÑO ESTRENO")
    .agg(
        ROI_SUMA=("ROI_IND", "sum"),
        NUM_PELICULAS=("TITULO", "count")
    )
    .reset_index()
)
df_año["ROI_GENERAL"] = df_año["ROI_SUMA"] / df_año["NUM_PELICULAS"]
df_año = df_año.sort_values("AÑO ESTRENO", ascending=True)

# ROI Promedio Género
df_genero = a24.copy()
df_genero["ROI_IND"] = df_genero["TAQUILLA MUNDIAL"] / df_genero["PRESUPUESTO"]
df_genero = (
    df_genero.groupby("GENERO")
    .agg(
        ROI_PROMEDIO=("ROI_IND", "mean"),
        NUM_PELICULAS=("TITULO", "count")
    )
    .reset_index()
)
df_genero = df_genero.sort_values("ROI_PROMEDIO", ascending=True)

# ROI por Director: (Taquilla Total / Presupuesto Total) / Películas dirigidas
df_director = a24.copy()
df_director = (
    df_director.groupby("DIRECTOR")
    .agg(
        TAQUILLA_TOTAL=("TAQUILLA MUNDIAL", "sum"),
        PRESUPUESTO_TOTAL=("PRESUPUESTO", "sum"),
        NUM_PELICULAS=("TITULO", "count")
    )
    .reset_index()
)
df_director["ROI_DIRECTOR"] = (df_director["TAQUILLA_TOTAL"] / df_director["PRESUPUESTO_TOTAL"]) / df_director["NUM_PELICULAS"]
df_director = df_director.nlargest(10, "ROI_DIRECTOR").sort_values("ROI_DIRECTOR", ascending=True)

# TOP 10 Películas por ROI Individual
df_peliculas = a24.copy()
df_peliculas["ROI_IND"] = df_peliculas["TAQUILLA MUNDIAL"] / df_peliculas["PRESUPUESTO"]
df_peliculas = df_peliculas.nlargest(10, "ROI_IND").sort_values("ROI_IND", ascending=True)


# =========================
# SLIDES: SELECCIÓN DE GRÁFICA
# =========================
SLIDES = [
    "📅 ROI por Año",
    "🎭 ROI por Género",
    "🎬 ROI por Director",
    "🎥 ROI por Película",
]

# Inicializar estado
if "slide_idx" not in st.session_state:
    st.session_state.slide_idx = 0

# Navegación con botones
col_prev, col_titulo, col_next = st.columns([1, 6, 1])

with col_prev:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("◀", use_container_width=True, disabled=st.session_state.slide_idx == 0):
        st.session_state.slide_idx -= 1
        st.rerun()

with col_titulo:
    # Indicadores de posición (puntos)
    puntos = ""
    for i, nombre in enumerate(SLIDES):
        if i == st.session_state.slide_idx:
            puntos += f"<span style='font-size:25px; color:#e8c832;'>●</span>&nbsp;&nbsp;"
        else:
            puntos += f"<span style='font-size:25px; color:#aaaaaa;'>○</span>&nbsp;&nbsp;"
    st.markdown(
        f"<div style='text-align:center; padding: 30px 0;'>{puntos}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<h2 style='text-align:center; color:#1a1a1a; font-size:25px;'>{SLIDES[st.session_state.slide_idx]}</h2>",
        unsafe_allow_html=True
    )

with col_next:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("▶", use_container_width=True, disabled=st.session_state.slide_idx == len(SLIDES) - 1):
        st.session_state.slide_idx += 1
        st.rerun()

slide_actual = st.session_state.slide_idx


# =========================
# SLIDE 1: ROI GENERAL POR AÑO
# =========================
if slide_actual == 0:
    fig_año = go.Figure()

    fig_año.add_trace(go.Bar(
        x=df_año["AÑO ESTRENO"].astype(str),
        y=df_año["ROI_GENERAL"],
        marker=dict(color="#e8c832"),
        text=df_año["ROI_GENERAL"].apply(lambda x: f"{x:.2f}x"),
        textposition="outside",
        customdata=list(zip(df_año["NUM_PELICULAS"])),
        hovertemplate=(
            "<b>Año %{x}</b><br>"
            "ROI General: %{y:.2f}x<br>"
            "Películas: %{customdata[0]}"
            "<extra></extra>"
        ),
    ))

    fig_año.update_layout(
        font=dict(color="#1a1a1a", size=25),
        xaxis=dict(
            title=dict(text="Año", font=dict(size=25)),
            tickfont=dict(size=25),
            showgrid=False,
            type="category",
        ),
        yaxis=dict(
            title=dict(text="ROI General", font=dict(size=25)),
            tickfont=dict(size=1),
            ticksuffix="x",
            gridcolor="rgba(0,0,0,0.15)",
            gridwidth=1,
            showgrid=True,
        ),
        margin=dict(t=100, l=20, r=80, b=60),
        height=750,
    )

    fig_año.update_traces(textfont=dict(size=20))
    st.plotly_chart(fig_año)


# =========================
# SLIDE 2: ROI POR GÉNERO
# =========================
elif slide_actual == 1:
    fig_genero = go.Figure()

    fig_genero.add_trace(go.Bar(
        x=df_genero["ROI_PROMEDIO"],
        y=df_genero["GENERO"],
        orientation="h",
        marker=dict(color="#e8c832"),
        text=df_genero["ROI_PROMEDIO"].apply(lambda x: f"{x:.2f}x"),
        textposition="outside",
        customdata=list(zip(df_genero["NUM_PELICULAS"])),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "ROI Promedio: %{x:.2f}x<br>"
            "Películas: %{customdata[0]}"
            "<extra></extra>"
        ),
    ))

    fig_genero.update_layout(
        font=dict(color="#1a1a1a", size=25),
        xaxis=dict(
            title=dict(text="ROI Promedio", font=dict(size=25)),
            tickfont=dict(size=25),
            ticksuffix="x",
            gridcolor="rgba(0,0,0,0.15)",
            gridwidth=1,
            showgrid=True,
            type="log",
            tickvals=[1, 2, 5, 10, 25, 50, 100, 250, 500],
            ticktext=["1x", "2x", "5x", "10x", "25x", "50x", "100x", "250x", "500x"],
        ),
        yaxis=dict(
            tickfont=dict(size=25),
            automargin=True,
            showgrid=False,
        ),
        margin=dict(t=100, l=20, r=120, b=60),
        height=750,
    )

    fig_genero.update_traces(textfont=dict(size=20))
    st.plotly_chart(fig_genero)


# =========================
# SLIDE 3: ROI POR DIRECTOR
# =========================
elif slide_actual == 2:
    fig_dir = go.Figure()

    fig_dir.add_trace(go.Bar(
        x=df_director["ROI_DIRECTOR"],
        y=df_director["DIRECTOR"],
        orientation="h",
        marker=dict(color="#e8c832"),
        text=df_director["ROI_DIRECTOR"].apply(lambda x: f"{x:.2f}x"),
        textposition="outside",
        customdata=list(zip(
            df_director["NUM_PELICULAS"],
            df_director["TAQUILLA_TOTAL"],
            df_director["PRESUPUESTO_TOTAL"],
        )),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "ROI por Director: %{x:.2f}x<br>"
            "Películas: %{customdata[0]}<br>"
            "Taquilla Total: $%{customdata[1]:,.0f}<br>"
            "Presupuesto Total: $%{customdata[2]:,.0f}"
            "<extra></extra>"
        ),
    ))

    fig_dir.update_layout(
        font=dict(color="#1a1a1a", size=25),
        xaxis=dict(
            title=dict(text="ROI por Director", font=dict(size=25)),
            tickfont=dict(size=25),
            ticksuffix="x",
            gridcolor="rgba(0,0,0,0.15)",
            gridwidth=1,
            showgrid=True,
            type="log",
            tickvals=[1, 2, 5, 10, 25, 50, 100, 250, 500],
            ticktext=["1x", "2x", "5x", "10x", "25x", "50x", "100x", "250x", "500x"],
        ),
        yaxis=dict(
            tickfont=dict(size=25),
            automargin=True,
            showgrid=False,
        ),
        margin=dict(t=100, l=20, r=120, b=60),
        height=750,
    )

    fig_dir.update_traces(textfont=dict(size=20))
    st.plotly_chart(fig_dir)


# =========================
# SLIDE 4: TOP 10 PELÍCULAS POR ROI
# =========================
elif slide_actual == 3:
    fig_pelis = go.Figure()

    fig_pelis.add_trace(go.Bar(
        x=df_peliculas["ROI_IND"],
        y=df_peliculas["TITULO"],
        orientation="h",
        marker=dict(color="#e8c832"),
        text=df_peliculas["ROI_IND"].apply(lambda x: f"{x:.2f}x"),
        textposition="outside",
        customdata=list(zip(
            df_peliculas["TAQUILLA MUNDIAL"],
            df_peliculas["PRESUPUESTO"],
            df_peliculas["DIRECTOR"]
        )),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "ROI: %{x:.2f}x<br>"
            "Taquilla: $%{customdata[0]:,.0f}<br>"
            "Presupuesto: $%{customdata[1]:,.0f}<br>"
            "Director: %{customdata[2]}"
            "<extra></extra>"
        ),
    ))

    fig_pelis.update_layout(
        font=dict(color="#1a1a1a", size=25),
        xaxis=dict(
            title=dict(text="ROI", font=dict(size=25)),
            tickfont=dict(size=25),
            ticksuffix="x",
            gridcolor="rgba(0,0,0,0.15)",
            gridwidth=1,
            showgrid=True,
            type="log",
            tickvals=[1, 2, 5, 10, 25, 50, 100, 250, 500],
            ticktext=["1x", "2x", "5x", "10x", "25x", "50x", "100x", "250x", "500x"],
        ),
        yaxis=dict(
            tickfont=dict(size=25),
            automargin=True,
            showgrid=False,
        ),
        margin=dict(t=100, l=20, r=120, b=60),
        height=750,
    )

    fig_pelis.update_traces(textfont=dict(size=20))
    st.plotly_chart(fig_pelis)

st.divider()

# ─────────────────────────────────────────
#  MATRIZ BCG
# ─────────────────────────────────────────
st.markdown("""
<div style="font-size:20px; font-weight:bold; text-align: justify;">
</b><br><br>
La Matriz BCG clasifica cada elemento según su Taquilla Mundial (eje Y) y su Presupuesto (eje X), 
dividiendo el cuadrante en cuatro zonas: <span style="color:#e8c832;">⭐ Estrellas</span> (alta taquilla, alto presupuesto), 
<span style="color:#1d4e28;">🐄 Vacas de Efectivo</span> (alta taquilla, bajo presupuesto), 
<span style="color:#8ab0c8;">❓ Interrogantes</span> (baja taquilla, alto presupuesto) y 
<span style="color:#c0152a;">🐕 Perros</span> (baja taquilla, bajo presupuesto).
<br><br>         
El portafolio de A24 se encuentra equilibrado: casi la mitad de sus títulos se clasifican como Estrellas o Vacas de Efectivo, lo que implica que más del 50% de sus producciones generan retornos positivos en taquilla. Para un estudio de cine independiente que asume riesgos creativos de manera deliberada, este es un resultado extraordinario.  
<br><br>
Los directivos de A24 no solo seleccionan proyectos con alto potencial narrativo, sino que también demuestran una clara capacidad estratégica para decidir en qué películas invertir, optimizando así el balance entre riesgo creativo y rentabilidad comercial.
</div>
</b><br><br>
""", unsafe_allow_html=True)

# Botón de selección de dimensión
dimension = st.radio(
    "Visualizar por:",
    options=["PELICULA", "DIRECTOR", "GENERO"],
    horizontal=True,
)

# ── Preparar datos según dimensión ───────────────────────────────────────────
if dimension == "PELICULA":
    df_bcg = a24[["TITULO", "PRESUPUESTO", "TAQUILLA MUNDIAL", "GENERO"]].copy()
    df_bcg = df_bcg.rename(columns={"TITULO": "ETIQUETA"})

elif dimension == "DIRECTOR":
    df_bcg = (
        a24.groupby("DIRECTOR")
        .agg(
            PRESUPUESTO      =("PRESUPUESTO",      "sum"),
            TAQUILLA_MUNDIAL =("TAQUILLA MUNDIAL",  "sum"),
        )
        .reset_index()
        .rename(columns={"DIRECTOR": "ETIQUETA", "TAQUILLA_MUNDIAL": "TAQUILLA MUNDIAL"})
    )
    df_bcg["GENERO"] = "Director"

else:  
    df_bcg = (
        a24.groupby("GENERO")
        .agg(
            PRESUPUESTO      =("PRESUPUESTO",      "sum"),
            TAQUILLA_MUNDIAL =("TAQUILLA MUNDIAL",  "sum"),
        )
        .reset_index()
        .rename(columns={"GENERO": "ETIQUETA", "TAQUILLA_MUNDIAL": "TAQUILLA MUNDIAL"})
    )
    df_bcg["GENERO"] = df_bcg["ETIQUETA"]

# ── Calcular medianas para dividir cuadrantes ────────────────────────────────
med_presupuesto = df_bcg["PRESUPUESTO"].median()
med_taquilla    = df_bcg["TAQUILLA MUNDIAL"].median()

# ── Asignar cuadrante BCG ────────────────────────────────────────────────────
def asignar_cuadrante(row):
    alto_taquilla    = row["TAQUILLA MUNDIAL"] >= med_taquilla
    alto_presupuesto = row["PRESUPUESTO"]      >= med_presupuesto
    if alto_taquilla and alto_presupuesto:
        return "Estrella"
    elif alto_taquilla and not alto_presupuesto:
        return "Vaca de Efectivo"
    elif not alto_taquilla and alto_presupuesto:
        return "Interrogante"
    else:
        return "Perro"

df_bcg["CUADRANTE"] = df_bcg.apply(asignar_cuadrante, axis=1)

color_map = {
    "Estrella"        : "#e8c832",
    "Vaca de Efectivo": "#1d4e28",
    "Interrogante"    : "#8ab0c8",
    "Perro"           : "#c0152a",
}


# ── Figura BCG ───────────────────────────────────────────────────────────────
fig_bcg = px.scatter(
    df_bcg,
    x="PRESUPUESTO",
    y="TAQUILLA MUNDIAL",
    color="CUADRANTE",
    color_discrete_map=color_map,
    hover_name="ETIQUETA",
    hover_data={
        "PRESUPUESTO"     : ":,.0f",
        "TAQUILLA MUNDIAL": ":,.0f",
        "CUADRANTE"       : True,
        "GENERO"          : True,
    },
    height=750,
)

fig_bcg.update_traces(marker=dict(size=20,line=dict(width=1),gradient=dict(type="radial", color="white")))
    

# Líneas de mediana (divisores de cuadrante)
fig_bcg.add_vline(
    x=med_presupuesto,
    line=dict(color="rgba(0,0,0,0.3)", width=2, dash="dash"),  
)
fig_bcg.add_hline(
    y=med_taquilla,
    line=dict(color="rgba(0,0,0,0.3)", width=2, dash="dash"),  
)

# Etiquetas de cuadrante
anotaciones_bcg = [
    dict(text="ESTRELLAS",         x=0.98, y=0.98, xanchor="right", yanchor="top"),
    dict(text="VACAS DE EFECTIVO", x=0.02, y=0.98, xanchor="left",  yanchor="top"),
    dict(text="INTERROGANTES",     x=0.98, y=0.02, xanchor="right", yanchor="bottom"),
    dict(text="PERROS",            x=0.02, y=0.02, xanchor="left",  yanchor="bottom"),
]

for a in anotaciones_bcg:
    fig_bcg.add_annotation(
        text=a["text"],
        x=a["x"], y=a["y"],
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=30, color="rgba(0,0,0,0.4)", family="Arial Black"),  
        xanchor=a["xanchor"], yanchor=a["yanchor"],
    )

fig_bcg.update_layout(
    title=dict(
        text=f"<b>MATRIZ BCG — {dimension}</b><br><sup>Mediana de presupuesto y taquilla como punto de corte</sup>",
        font=dict(size=30, color="#1a1a1a", family="Arial Black"),  
        x=0.5, xanchor="center", y=0.97,
    ),
    paper_bgcolor="#ffffff",                               
    plot_bgcolor="#ffffff",                               
    xaxis=dict(
        title="Presupuesto (USD)", color="#1a1a1a",        
        gridcolor="rgba(0,0,0,0.08)", tickformat="$,.0f",
        type="log", exponentformat="none",
    ),
    yaxis=dict(
        title="Taquilla Mundial (USD)", color="#1a1a1a",   
        gridcolor="rgba(0,0,0,0.08)", tickformat="$,.0f",
        type="log", exponentformat="none",
    ),
    legend=dict(
        title=dict(text="Cuadrante BCG", font=dict(color="#1a1a1a")),  
        font=dict(color="#1a1a1a", size=25),               
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor="rgba(0,0,0,0.2)", borderwidth=1,
        x=1.02, y=1, xanchor="left", yanchor="top",
    ),
    font=dict(color="#1a1a1a"),                            
    margin={"r": 200, "t": 100, "l": 80, "b": 60},
    height=750,
)

st.plotly_chart(fig_bcg)

# ── Tabla resumen por cuadrante ───────────────────────────────────────────────
st.subheader("Resumen por Cuadrante")
cols = st.columns(4)

etiquetas = {
    "Estrella"        : "⭐ Estrella",
    "Vaca de Efectivo": "🐄 Vaca de Efectivo",
    "Interrogante"    : "❓ Interrogante",
    "Perro"           : "🐕 Perro",
}

for i, cuadrante in enumerate(["Estrella", "Vaca de Efectivo", "Interrogante", "Perro"]):
    subset = df_bcg[df_bcg["CUADRANTE"] == cuadrante][["ETIQUETA", "PRESUPUESTO", "TAQUILLA MUNDIAL"]]
    with cols[i]:
        st.markdown(f"### {etiquetas[cuadrante]}")
        st.markdown(f"**{len(subset)}** elementos")
        st.dataframe(
            subset.rename(columns={
                "ETIQUETA"        : dimension.capitalize(),
                "PRESUPUESTO"     : "Presupuesto",
                "TAQUILLA MUNDIAL": "Taquilla",
            }).style.format({
                "Presupuesto": "${:,.0f}",
                "Taquilla"   : "${:,.0f}",
            }),
            use_container_width=True,
            hide_index=True,
        )

st.divider()

# cd C:/Users/monzo/Desktop/PAD/A24 python -m streamlit run A24_APP.py
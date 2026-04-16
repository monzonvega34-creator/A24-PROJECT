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
<div style="font-size:25px; line-height:1.5; color:#1a1a1a; text-align:justify;">
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
    .sort_values("PRESUPUESTO", ascending=False)
    .reset_index(drop=True)
)

# Gráfica 6 — Dispersión: Taquilla vs Presupuesto
df_scatter = a24.copy()
df_scatter["oscar_bool"] = df_scatter["OSCAR"] == "YES"


# ─────────────────────────────────────────
#  GRÁFICAS
# ─────────────────────────────────────────

# ── Gráfica 1: Películas por año ─────────────────────────────────────────────
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
    ),
    yaxis=dict(
        title="Total de Películas", color="#1a1a1a",       
        gridcolor="rgba(0,0,0,0.1)",                       
    ),
    font=dict(color="#1a1a1a"),                            
    margin={"r": 40, "t": 100, "l": 60, "b": 80},
    height=720,
)

st.plotly_chart(fig1)
st.divider()

# ── Gráfica 2: Presupuesto vs Taquilla por año ───────────────────────────────
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
        text="<b>PRESUPUESTO VS TAQUILLA MUNDIAL POR AÑO</b><br><sup>Ciclo economico de A24</sup>",
        font=dict(size=20, color="#1a1a1a", family="Arial Black"),  
        x=0.5, xanchor="center", y=0.97,
    ),
   
    xaxis=dict(
        title="Año de Estreno", color="#1a1a1a",           
        gridcolor="rgba(0,0,0,0.08)",
        tickmode="linear", tickangle=0, dtick=1,
    ),
    yaxis=dict(
        title="Monto", color="#1a1a1a",  
        gridcolor="rgba(0,0,0,0.1)",
        type="log", tickformat="$,.0f", exponentformat="none",
    ),
    legend=dict(
        orientation="v",
        x=1.12,
        xanchor="left",
        y=1,
        yanchor="top",
        font=dict(size=15),
    ),
    font=dict(color="#1a1a1a"),                            
    margin={"r": 40, "t": 100, "l": 80, "b": 80},
    height=650,
)

st.plotly_chart(fig2)
st.divider()

# ── Gráfica 3: BURBUJAS por género ────────────────────────────────────────────
# =========================
# PREPARACIÓN DE DATOS
# =========================
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
    y=df_bubble["TAQUILLA_TOTAL"],
    mode="markers+text",
    name="Género",
    text=df_bubble["GENERO"],
    textposition="top center",
    textfont=dict(size=10, color="#1a1a1a"),
    marker=dict(
        size=df_bubble["TOTAL_PELICULAS"] / df_bubble["TOTAL_PELICULAS"].max() * 50 + 60,
        color=df_bubble["TOTAL_PELICULAS"],                                 # ← color = películas
        colorscale=[[0, "#2d6e3a"], [0.5, "#e8c832"], [1, "#c0152a"]],
        showscale=True,
        colorbar=dict(
            title=dict(text="Total de Películas", font=dict(size=15)),     # ← label corregido
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
        font=dict(size=15, color="#1a1a1a"),
        x=0.5, xanchor="center", y=0.97,
    ),
    xaxis=dict(
        title=dict(text="Género", font=dict(size=10)),
        tickfont=dict(size=15),
        tickangle=0,
        showgrid=False,
    ),
    yaxis=dict(
        title=dict(text="Taquilla Total ($)", font=dict(size=10)),          # ← label actualizado
        tickfont=dict(size=10),
        gridcolor="rgba(0,0,0,0.1)",
        gridwidth=1,
        tickformat="$,.0f",                                                # ← formato dinero
        range=[-df_bubble["TAQUILLA_TOTAL"].max() * 0.05,
                df_bubble["TAQUILLA_TOTAL"].max() * 1.2],                  # ← espacio para etiquetas
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

# ── Gráfica 4: Burbujas — Películas ganadoras del Oscar ──────────────────────
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
        sizeref=2 * df_oscar["PRESUPUESTO"].max() / (50**2),  # ← mismo sizeref para comparar
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
        text="<b>PELÍCULAS GANADORAS DEL ÓSCAR</b>",
        font=dict(size=20, color="#1a1a1a", family="Arial Black"),
        x=0.5, xanchor="center", y=0.97,
    ),
    xaxis=dict(
        title=dict(text="Película", font=dict(size=20)),
        tickfont=dict(size=15),
        color="#1a1a1a",
        tickangle=-45,
        automargin=True,
        gridcolor="rgba(0,0,0,0.08)",
    ),
    yaxis=dict(
        title=dict(text="Monto", font=dict(size=25)),
        tickfont=dict(size=25),
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
# =========================
# PREPARACIÓN DE DATOS
# =========================

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
        title=dict(text="ROI POR AÑO", font=dict(size=25)),
        font=dict(color="#1a1a1a", size=25),
        xaxis=dict(
            title=dict(text="Año", font=dict(size=25)),
            tickfont=dict(size=25),
            showgrid=False,
            type="category",
        ),
        yaxis=dict(
            title=dict(text="ROI General", font=dict(size=25)),
            tickfont=dict(size=25),
            ticksuffix="x",
            gridcolor="rgba(0,0,0,0.15)",
            gridwidth=1,
            showgrid=True,
        ),
        margin=dict(t=100, l=20, r=80, b=60),
        height=750,
        width=2000,
    )

    fig_año.update_traces(textfont=dict(size=25))
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
        title=dict(text="ROI POR GÉNERO", font=dict(size=50)),
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
        width=2000,
    )

    fig_genero.update_traces(textfont=dict(size=50))
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
        title=dict(text="DIRECTORES POR ROI", font=dict(size=50)),
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
        width=2000,
    )

    fig_dir.update_traces(textfont=dict(size=50))
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
        title=dict(text="PELÍCULAS POR ROI", font=dict(size=25)),
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
        width=2000,
    )

    fig_pelis.update_traces(textfont=dict(size=50))
    st.plotly_chart(fig_pelis)

st.divider()



# ─────────────────────────────────────────
#  MATRIZ BCG
# ─────────────────────────────────────────
st.header("Matriz BCG — ¿Cuáles son los caballos ganadores de A24?")
st.write("""
La Matriz BCG clasifica cada elemento según su Taquilla Mundial (eje Y) y su Presupuesto (eje X),
dividiendo el cuadrante en cuatro zonas: **Estrellas** (alta taquilla, alto presupuesto),
**Vacas de Efectivo** (alta taquilla, bajo presupuesto), **Interrogantes** (baja taquilla, alto presupuesto)
y **Perros** (baja taquilla, bajo presupuesto).
""")

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

else:  # GENERO
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
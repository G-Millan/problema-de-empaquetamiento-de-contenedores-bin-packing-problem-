import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Calculadora de Cajas 📦",
    page_icon="📦",
    layout="wide"
)

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7fa;
    }
    .titulo {
        font-size:32px;
        font-weight:bold;
        color:#2C3E50;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        color: gray;
        font-size: 13px;
        padding: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNCIONES ---
def calcular_kits_por_caja(caja_kit, caja_embalaje):
    largo_kit, ancho_kit, alto_kit = caja_kit
    largo_emb, ancho_emb, alto_emb = caja_embalaje

    if (largo_kit > largo_emb or ancho_kit > ancho_emb or alto_kit > alto_emb):
        return 0, None

    orientaciones = [
        (largo_kit, ancho_kit, alto_kit),
        (ancho_kit, largo_kit, alto_kit),
        (largo_kit, alto_kit, ancho_kit),
        (alto_kit, ancho_kit, largo_kit),
        (ancho_kit, alto_kit, largo_kit),
        (alto_kit, largo_kit, ancho_kit)
    ]

    max_kits = 0
    mejor_orientacion = None
    mejor_distribucion = None

    for l, a, h in orientaciones:
        if l <= largo_emb and a <= ancho_emb and h <= alto_emb:
            en_largo = int(largo_emb // l)
            en_ancho = int(ancho_emb // a)
            en_alto = int(alto_emb // h)
            kits_total = en_largo * en_ancho * en_alto

            if kits_total > max_kits:
                max_kits = kits_total
                mejor_orientacion = (l, a, h)
                mejor_distribucion = (en_largo, en_ancho, en_alto)

    return max_kits, (mejor_orientacion, mejor_distribucion)

# --- INTERFAZ ---
st.markdown('<p class="titulo">📦 Calculadora de Cajas de Embalaje</p>', unsafe_allow_html=True)
st.write("Una herramienta sencilla para calcular cuántas cajas necesitas para tus kits.")

col1, col2 = st.columns([1,1])

with col1:
    st.header("👉 Datos de entrada")

    st.subheader("Caja del kit (pequeña)")
    largo_kit = st.number_input("Largo (cm)", min_value=1.0, value=10.0)
    ancho_kit = st.number_input("Ancho (cm)", min_value=1.0, value=10.0)
    alto_kit = st.number_input("Alto (cm)", min_value=1.0, value=10.0)

    st.subheader("Caja de embalaje (grande)")
    largo_emb = st.number_input("Largo (cm)", min_value=1.0, value=30.0)
    ancho_emb = st.number_input("Ancho (cm)", min_value=1.0, value=30.0)
    alto_emb = st.number_input("Alto (cm)", min_value=1.0, value=30.0)

    st.subheader("Cantidad de kits")
    cantidad_kits = st.number_input("¿Cuántos kits necesitas enviar?", min_value=1, value=10)

    calcular = st.button("📐 Calcular cajas", use_container_width=True)

with col2:
    st.header("📊 Resultados")
    if calcular:
        kits_por_caja, distribucion = calcular_kits_por_caja(
            (largo_kit, ancho_kit, alto_kit),
            (largo_emb, ancho_emb, alto_emb)
        )

        if kits_por_caja > 0:
            cajas_necesarias = -(-cantidad_kits // kits_por_caja)  # redondeo hacia arriba
            espacio_utilizado = (kits_por_caja * largo_kit * ancho_kit * alto_kit) / (largo_emb * ancho_emb * alto_emb) * 100

            st.success("✅ Cálculo exitoso")
            st.write(f"**Kits por caja de embalaje:** {kits_por_caja}")
            st.write(f"**Cajas necesarias:** {cajas_necesarias}")
            st.write(f"**Espacio utilizado:** {espacio_utilizado:.1f}%")

            orientacion, distrib = distribucion
            if orientacion and distrib:
                st.subheader("Distribución sugerida")
                st.write(f"• Orientación: {orientacion[0]} × {orientacion[1]} × {orientacion[2]} cm")
                st.write(f"• Distribución: {distrib[0]} a lo largo × {distrib[1]} a lo ancho × {distrib[2]} a lo alto")
                st.write(f"• Total: {kits_por_caja} kits/caja")
        else:
            st.error("❌ Las cajas del kit no caben en la caja de embalaje.")

# --- FOOTER CON TU NOMBRE ---
st.markdown('<div class="footer">Creado con ❤️ por Germán Millán</div>', unsafe_allow_html=True)

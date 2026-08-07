import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
from datetime import datetime, date
from decimal import Decimal
#df_historial
# ==========================================
# 1. CONFIGURACION E INICIALIZACION BD
# ==========================================
st.set_page_config(page_title="BizPilot", layout="centered")

# ==========================================
# 2. INYECCION DE CSS SUPER AVANZADO 
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800;900&display=swap');

    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    .block-container {
        max-width: 1500px !important;
        padding-top: 0rem !important;
        padding-bottom: 4rem !important;
    }

    [data-testid="stAppViewContainer"] {
        overflow-x: hidden;
    }

    .full-width-header {
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        background: linear-gradient(180deg, #E83E8C 0%, #E83E8C 50%, #FFFFFF 100%);
        padding: 4rem 0 4.5rem 0;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom-left-radius: 60px; 
        border-bottom-right-radius: 60px; 
    }
    
    .full-width-header h1 {
        font-family: 'Nunito', sans-serif !important;
        color: #FFFFFF !important;
        font-size: 7rem !important; 
        font-weight: 900;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.1;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.15);
    }
    
    .full-width-header p {
        color: #FFD1DC !important;
        font-size: 1.6rem !important; 
        font-weight: 700;
        margin: 0;
        padding: 0;
        margin-top: 5px;
    }

    div[data-testid="stTabs"] {
        width: 100%;
    }
    
    /* GHOST TABS */
    div[data-baseweb="tab-list"] {
        border-bottom: none !important;
        gap: 15px !important; 
    }
    div[data-baseweb="tab-highlight"] { display: none !important; }
    div[data-baseweb="tab-border"] { display: none !important; }
    
    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        flex: 1 !important; 
        background: transparent !important;
        border: none !important;
        border-radius: 50px !important; 
        padding-top: 15px !important;
        padding-bottom: 15px !important;
        box-shadow: none !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }
    
    div[data-testid="stTabs"] button[data-baseweb="tab"]:hover {
        background: linear-gradient(120deg, #FF87C3 0%, #E83E8C 100%) !important;
        transform: scale(1.05) !important; 
        box-shadow: 0px 10px 20px rgba(232, 62, 140, 0.2) !important;
    }
    
    div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        transform: scale(1.0) !important;
    }
    
    div[data-testid="stTabs"] button[data-baseweb="tab"] * {
        font-family: 'Nunito', sans-serif !important;
        color: #B0B0B0 !important; 
        font-weight: 900 !important; 
        font-size: 1.8rem !important; 
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stTabs"] button[data-baseweb="tab"]:hover * {
        color: #FFFFFF !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1) !important;
    }

    div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] * {
        color: #E83E8C !important;
    }
    
    div[role="tabpanel"] {
        padding-top: 3.5rem !important; 
        padding-bottom: 2rem !important;
        animation: slideFadeIn 0.5s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
    }
    
    @keyframes slideFadeIn {
        0% { opacity: 0; transform: translateX(40px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    
    hr {
        margin-top: 4rem !important;
        margin-bottom: 4rem !important;
        border-color: #F0F0F0 !important;
        border-width: 2px !important;
    }

    /* TIPOGRAFÍA AMPLIADA */
    h2 {
        font-family: 'Nunito', sans-serif !important;
        color: #111111 !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important; 
        letter-spacing: -0.5px !important;
    }
    
    h3 {
        font-family: 'Nunito', sans-serif !important;
        color: #111111 !important;
        font-weight: 800 !important;
        font-size: 1.8rem !important; 
        letter-spacing: -0.5px !important;
    }
    
    p, label {
        color: #333333 !important;
        font-size: 1.3rem !important; 
        font-weight: 600 !important;
    }

    div[data-testid="metric-container"] {
        background-color: #FFFFFF !important;
        border: 2px solid #FFF0F5 !important;
        border-radius: 25px !important;
        padding: 25px 15px !important;
        box-shadow: 0 10px 25px rgba(232, 62, 140, 0.08) !important;
        text-align: center !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 35px rgba(232, 62, 140, 0.15) !important;
    }
    div[data-testid="metric-container"] > div {
        justify-content: center !important; 
    }
    div[data-testid="stMetricValue"] > div {
        font-family: 'Nunito', sans-serif !important;
        font-size: 3.5rem !important; 
        font-weight: 900 !important;
        color: #E83E8C !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1.4rem !important; 
        font-weight: 800 !important;
        color: #666666 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stForm"] {
        border-radius: 30px !important; 
        border: 2px solid #F4F4F4 !important;
        padding: 2.5rem !important; 
        background-color: #FFFFFF !important;
        box-shadow: 0 12px 30px rgba(0,0,0,0.04) !important;
    }

    button[kind="primary"], button[kind="primaryFormSubmit"] {
        border-radius: 20px !important; 
        padding: 1.5rem 2rem !important; 
        font-family: 'Nunito', sans-serif !important;
        font-size: 1.4rem !important; 
        font-weight: 800 !important;
        box-shadow: 0 8px 20px rgba(232, 62, 140, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    button[kind="primary"]:hover, button[kind="primaryFormSubmit"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 25px rgba(232, 62, 140, 0.45) !important;
    }

    div.stAlert p { font-size: 1.3rem !important; }
    
    div.stAlert {
        border-radius: 20px !important;
        padding: 1.5rem !important;
        border: none !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.05) !important;
    }

    /* INPUTS Y SELECTBOX */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] > div {
        background-color: #F4F4F4 !important; 
        border-radius: 12px !important;
        border: 2px solid transparent !important;
        padding: 8px !important; 
    }
    
    input, textarea {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important; 
        font-size: 1.3rem !important; 
        font-weight: 600 !important;
        background-color: transparent !important;
    }
    
    div[data-baseweb="select"] span {
        color: #000000 !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
    }
    
    div[data-baseweb="popover"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1px solid #DDDDDD !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1) !important;
    }
    
    ul[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
    }

    ul[data-baseweb="menu"] li {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        font-family: 'Nunito', sans-serif !important;
        padding: 12px 15px !important;
        transition: background-color 0.2s ease, color 0.2s ease !important;
    }

    ul[data-baseweb="menu"] li:hover,
    ul[data-baseweb="menu"] li[aria-selected="true"] {
        background-color: #FFF0F5 !important;
        color: #E83E8C !important;
    }
    
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within {
        border-color: #E83E8C !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 0 0 3px rgba(232, 62, 140, 0.2) !important; 
    }

    /* TABLAS */
    [data-testid="stTable"] {
        border-radius: 20px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05) !important;
    }
    [data-testid="stTable"] > div > table {
        background-color: #FFFFFF !important;
    }
    [data-testid="stTable"] th {
        background-color: #FFF0F5 !important;
        color: #E83E8C !important;
        font-family: 'Nunito', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.3rem !important; 
        border: none !important;
        padding: 18px !important;
    }
    [data-testid="stTable"] td {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border-bottom: 1px solid #F0F0F0 !important;
        border-top: none !important;
        border-left: none !important;
        border-right: none !important;
        font-size: 1.25rem !important; 
        padding: 18px !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=st.secrets["database"]["host"],
        port=st.secrets["database"]["port"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        sslmode="require",
        connect_timeout=10
    )
    
conn = get_connection()

# ==========================================
# 3. ENCABEZADO PRINCIPAL FULL-WIDTH
# ==========================================
st.markdown(
    """
    <div class="full-width-header">
        <h1>GabyShop</h1>
        <p>by BizPilot</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# ==========================================
# 4. NAVEGACION SUPERIOR
# ==========================================
tab_inicio, tab_ventas, tab_almacen, tab_clientes, tab_envios, tab_cobranza, tab_dashboards = st.tabs([
    "Inicio", 
    "Ventas", 
    "Almacén", 
    "Clientes", 
    "Envíos", 
    "Cobranza",
    "Dashboards"
])

# ==========================================
# 5. VISTAS DEL ERP
# ==========================================

# --- INICIO ---
with tab_inicio:
    st.title("Resumen Operativo")
    
    c = conn.cursor()
    c.execute("SELECT SUM(total) FROM ventas WHERE fecha::date = (CURRENT_TIMESTAMP AT TIME ZONE 'America/Monterrey')::date")
    ventas_hoy = c.fetchone()[0] or 0.0
    c.execute("SELECT SUM(total) FROM ventas WHERE fecha::date = ((CURRENT_TIMESTAMP AT TIME ZONE 'America/Monterrey')::date - INTERVAL '1 day')::date")
    ventas_ayer = c.fetchone()[0] or 0.0
    c.execute("SELECT SUM(stock) FROM inventario")
    stock_total = c.fetchone()[0] or 0
    c.execute("SELECT COUNT(*) FROM inventario WHERE stock <= 3")
    alertas_stock = c.fetchone()[0] or 0
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ventas de Hoy", f"${ventas_hoy:,.2f}")
    c2.metric("Ventas de Ayer", f"${ventas_ayer:,.2f}")
    c3.metric("Artículos en Stock", stock_total)
    c4.metric("Alertas de Stock", alertas_stock)
    
    st.markdown("---")
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.subheader("Alertas de Inventario")
        df_alertas = pd.read_sql_query("SELECT sku, nombre, stock FROM inventario WHERE stock <= 3 ORDER BY stock ASC", conn)
        if not df_alertas.empty:
            st.table(df_alertas)
        else:
            st.success("Todo el inventario tiene existencias saludables (más de 3 piezas).")
            
    with col_der:
        st.subheader("Tareas Pendientes")
        st.checkbox("Revisar envíos pendientes")
        st.checkbox("Contactar a clientes frecuentes")
        st.checkbox("Revisar cuentas por cobrar")
        st.text_area("Notas Adicionales:")

# --- VENTAS (VENTA EXPRÉS) ---
with tab_ventas:
    st.title("Punto de Venta (TPV)")
    
    opciones_productos = ["+ Venta Rápida (Nuevo Producto)"]
    
    df_inv = pd.read_sql_query("SELECT sku, nombre, stock FROM inventario WHERE stock > 0", conn)
    if not df_inv.empty:
        df_inv['display'] = df_inv['sku'] + " - " + df_inv['nombre'] + " (Stock: " + df_inv['stock'].astype(str) + ")"
        opciones_productos.extend(df_inv['display'].tolist())
    else:
        st.info("💡 Tu inventario está vacío, pero puedes usar la 'Venta Rápida' para vender productos sobre la marcha.")
        
    with st.container(border=True):
        st.subheader("Registrar Nueva Venta")
        col1, col2 = st.columns(2)
        cliente = col1.text_input("Nombre del Cliente")
        
        producto_sel = col2.selectbox("Seleccionar Producto", opciones_productos)
        
        es_venta_rapida = (producto_sel == "+ Venta Rápida (Nuevo Producto)")
        
        if es_venta_rapida:
            nombre_nuevo = st.text_input("📝 Descripción del producto exprés (Ej: Labial Rosa M.A.C)")
            stock_disp = None 
            sku_sel = f"EXPRS-{int(datetime.now().timestamp())}"
        else:
            sku_sel = producto_sel.split(" - ")[0]
            stock_disp = int(df_inv[df_inv['sku'] == sku_sel]['stock'].iloc[0])
            nombre_nuevo = None
            
        col3, col4 = st.columns(2)
        cantidad = col3.number_input("Cantidad a vender", min_value=1, max_value=stock_disp if not es_venta_rapida else None, step=1)
        precio_venta = col4.number_input("Precio Acordado con Cliente ($)", min_value=0.0, step=50.0)
        
        total_venta = cantidad * precio_venta
        st.markdown(f"<h3 style='text-align: right; color: #E83E8C; font-size: 2.5rem !important;'>Total: ${total_venta:,.2f}</h3>", unsafe_allow_html=True)
        
        if st.button("Confirmar Venta", type="primary", use_container_width=True):
            if cliente and precio_venta > 0 and (not es_venta_rapida or nombre_nuevo):
                c = conn.cursor()
                
                if es_venta_rapida:
                    c.execute("""
                        INSERT INTO inventario (sku, nombre, precio_compra, tienda, categoria, stock) 
                        VALUES (%s, %s, 0, 'Venta Rápida', 'General', 0)
                    """, (sku_sel, nombre_nuevo))
                else:
                    c.execute("UPDATE inventario SET stock = stock - %s WHERE sku = %s", (cantidad, sku_sel))
                    
                c.execute("""
                    INSERT INTO ventas (fecha, cliente, total)
                    VALUES (CURRENT_TIMESTAMP AT TIME ZONE 'America/Monterrey', %s, %s)
                    RETURNING id
                """, (cliente, total_venta))
                venta_id = c.fetchone()[0]
                c.execute("INSERT INTO ventas_detalle (venta_id, sku, cantidad, precio_venta, subtotal) VALUES (%s, %s, %s, %s, %s)", 
                          (venta_id, sku_sel, cantidad, precio_venta, total_venta))
                
                conn.commit()
                st.success(f"✅ Venta registrada a {cliente} exitosamente.")
                if es_venta_rapida:
                    st.info(f"El producto '{nombre_nuevo}' se registró temporalmente en el sistema para tus reportes.")
            else:
                st.error("Por favor completa el nombre del cliente, describe el producto y asigna un precio válido.")

# --- ALMACÉN Y COMPRAS ---
with tab_almacen:
    st.title("Gestión de Almacén e Inversión")
    
    sub_opcion = st.selectbox("Selecciona una acción de Almacén:", ["Ingresar Mercancía", "Gastos Operativos", "Gestionar Inventario"])
    st.markdown("---")
    
    if sub_opcion == "Ingresar Mercancía":
        with st.form("form_compras"):
            c1, c2, c3 = st.columns(3)
            sku = c1.text_input("SKU / Código")
            nombre = c2.text_input("Nombre del Producto")
            categoria = c3.text_input("Categoría (ej. Ropa, Electrónica)")
            
            c4, c5, c6 = st.columns(3)
            tienda = c4.text_input("Tienda de Compra (ej. Ross, Target)")
            precio_compra = c5.number_input("Costo Unitario ($)", min_value=0.0)
            cantidad = c6.number_input("Cantidad Comprada", min_value=1, step=1)
            
            if st.form_submit_button("Guardar en Inventario", type="primary"):
                if sku and nombre and tienda:
                    c = conn.cursor()
                    c.execute("SELECT stock FROM inventario WHERE sku = %s", (sku,))
                    resultado = c.fetchone()
                    if resultado:
                        c.execute("UPDATE inventario SET stock = stock + %s, precio_compra = %s WHERE sku = %s", (cantidad, precio_compra, sku))
                    else:
                        c.execute("INSERT INTO inventario (sku, nombre, precio_compra, tienda, categoria, stock) VALUES (%s, %s, %s, %s, %s, %s)", 
                                  (sku, nombre, precio_compra, tienda, categoria, cantidad))
                    
                    total_compra = cantidad * precio_compra
                    c.execute("INSERT INTO compras (fecha, sku, cantidad, total_compra, tienda) VALUES (CURRENT_TIMESTAMP AT TIME ZONE 'America/Monterrey', %s, %s, %s, %s)",
                              (sku, cantidad, total_compra, tienda))
                    conn.commit()
                    st.success("Mercancía agregada al inventario y registrada en inversiones.")
                else:
                    st.error("Completa todos los campos principales.")
                    
        st.subheader("Catálogo de Inventario Actual")
        df_inventario = pd.read_sql_query("SELECT * FROM inventario", conn)
        if not df_inventario.empty:
            st.table(df_inventario)

    elif sub_opcion == "Gastos Operativos":
        with st.form("form_gastos"):
            col_g1, col_g2 = st.columns(2)
            concepto = col_g1.selectbox("Concepto de Gasto", ["Gasolina", "Casetas", "Comida", "Hospedaje", "Otros"])
            monto = col_g2.number_input("Monto Gastado ($)", min_value=0.0)
            if st.form_submit_button("Registrar Gasto"):
                c = conn.cursor()
                c.execute("INSERT INTO gastos (fecha, concepto, monto) VALUES (CURRENT_TIMESTAMP AT TIME ZONE 'America/Monterrey', %s, %s)", (concepto, monto))
                conn.commit()
                st.success("Gasto operativo registrado.")

    elif sub_opcion == "Gestionar Inventario":
        df_borrar = pd.read_sql_query("SELECT sku, nombre, stock FROM inventario", conn)
        if not df_borrar.empty:
            df_borrar['display'] = df_borrar['sku'] + " - " + df_borrar['nombre'] + " (Stock: " + df_borrar['stock'].astype(str) + ")"
            producto_a_borrar = st.selectbox("Selecciona el producto a eliminar", df_borrar['display'].tolist())
            sku_borrar = producto_a_borrar.split(" - ")[0]
            if st.button("Eliminar Producto", type="primary"):
                c = conn.cursor()
                c.execute("DELETE FROM inventario WHERE sku = %s", (sku_borrar,))
                conn.commit()
                st.success(f"Producto eliminado del catálogo correctamente.")
        else:
            st.info("No hay productos en el inventario.")

# --- CLIENTES ---
with tab_clientes:
    st.title("Historial y Ranking de Clientes")
    
    st.subheader("Top 5: Mejores Clientes")
    query_top = """
    SELECT
        v.cliente AS "Cliente",
        COUNT(DISTINCT v.id) AS "Visitas",
        SUM(d.cantidad) AS "Articulos_Comprados",
        SUM(v.total) AS "Dinero_Invertido"
        FROM ventas v
        JOIN ventas_detalle d ON v.id = d.venta_id
        GROUP BY v.cliente
        ORDER BY "Dinero_Invertido" DESC
        LIMIT 5
        """
    df_top = pd.read_sql_query(query_top, conn)
    if not df_top.empty:
        df_top['Dinero_Invertido'] = df_top['Dinero_Invertido'].apply(lambda x: f"${x:,.2f}")
        st.table(df_top)
    else:
        st.info("Aún no hay suficientes datos de ventas para generar el ranking.")
        
    st.markdown("---")
    st.subheader("Historial Completo de Ventas")
    df_historial = pd.read_sql_query("""
    SELECT
        fecha AS "Fecha",
        cliente AS "Cliente",
        total AS "Total"
    FROM ventas
    ORDER BY fecha DESC
    """, conn)

# --- ENVÍOS ---
with tab_envios:
    st.title("Control de Logística y Envíos")
    
    with st.container(border=True):
        st.subheader("Registrar Nuevo Envío")
        with st.form("form_envios"):
            c1, c2 = st.columns(2)
            cliente_envio = c1.text_input("Nombre del Cliente")
            destino = c2.text_input("Destino (Dirección o Ciudad)")
            productos = st.text_area("Productos a enviar")
            
            c3, c4 = st.columns(2)
            costo_envio = c3.number_input("Costo de Envío ($)", min_value=0.0)
            km_recorrido = c4.number_input("Kilómetros de Recorrido (km)", min_value=0.0)
            
            if st.form_submit_button("Guardar Envío", type="primary"):
                if cliente_envio and destino and productos:
                    c = conn.cursor()
                    c.execute("INSERT INTO envios (fecha, cliente, productos, destino, costo_envio, km_recorrido) VALUES (CURRENT_TIMESTAMP AT TIME ZONE 'America/Monterrey', %s, %s, %s, %s, %s)",
                              (cliente_envio, productos, destino, costo_envio, km_recorrido))
                    conn.commit()
                    st.success("Envío registrado exitosamente.")
                else:
                    st.error("Por favor completa los campos de cliente, destino y productos.")
                    
    st.subheader("Historial de Envíos")
    df_envios = pd.read_sql_query("""
        SELECT
            fecha AS "Fecha",
            cliente AS "Cliente",
            productos AS "Productos",
            destino AS "Destino",
            costo_envio AS "Costo",
            km_recorrido AS "Distancia_km"
        FROM envios
        ORDER BY id DESC
        """, conn)
    if not df_envios.empty:
        df_envios['Costo'] = df_envios['Costo'].apply(lambda x: f"${x:,.2f}")
        st.table(df_envios)
    else:
        st.info("Aún no hay envíos registrados.")

# --- COBRANZA Y GESTIÓN DE CUENTAS (CRM) ---
with tab_cobranza:
    st.title("Cobranza y Cuentas por Cobrar (CRM)")
    
    with st.container(border=True):
        st.subheader("Registrar Nueva Cuenta o Abono")
        
        c1, c2 = st.columns(2)
        cliente_cobro = c1.text_input("Nombre del Cliente (Cuenta)")
        tipo_compra = c2.selectbox("Tipo de Compra", ["Contado", "Crédito (Abonos)"])
        
        c3, c4, c5 = st.columns(3)
        if tipo_compra == "Crédito (Abonos)":
            plazos = c3.number_input("Cantidad de Plazos/Abonos", min_value=1, step=1)
        else:
            plazos = 0
            c3.write("") 
            
        metodo_pago = c4.selectbox("Método de Pago / Origen", ["Efectivo", "Transferencia", "Tarjeta", "Pendiente de Definir"])
        estado_pago = c5.selectbox("Estado del Pago", ["Pendiente", "Pagado"])
        
        total_pagar = st.number_input("Total a Pagar / Monto de la Deuda ($)", min_value=0.0, step=100.0)
        
        if st.button("Guardar Registro de Cobranza", type="primary", use_container_width=True):
            if cliente_cobro and total_pagar > 0:
                c = conn.cursor()
                c.execute("""
                    INSERT INTO cobranza (fecha_registro, cliente, estado_pago, metodo_pago, tipo_compra, plazos, total_pagar) 
                    VALUES (CURRENT_TIMESTAMP AT TIME ZONE 'America/Monterrey', %s, %s, %s, %s, %s, %s)
                """, (cliente_cobro, estado_pago, metodo_pago, tipo_compra, plazos, total_pagar))
                conn.commit()
                st.success(f"Cuenta de {cliente_cobro} registrada correctamente.")
            else:
                st.error("Ingresa el nombre del cliente y un monto válido.")
                
    st.markdown("---")
    
    st.subheader("Estado Actual de Cuentas")
    df_cobranza = pd.read_sql_query("""
        SELECT
            id,
            fecha_registro AS "Fecha",
            cliente AS "Cliente",
            tipo_compra AS "Tipo",
            plazos AS "Plazos",
            metodo_pago AS "Metodo",
            estado_pago AS "Estado",
            total_pagar AS "Total"
        FROM cobranza
        ORDER BY id DESC
        """, conn)
    
    if not df_cobranza.empty:
        df_mostrar = df_cobranza.copy()
        df_mostrar['Total'] = df_mostrar['Total'].apply(lambda x: f"${x:,.2f}")
        df_mostrar['Plazos'] = df_mostrar['Plazos'].apply(lambda x: f"{x} abonos" if x > 0 else "N/A")
        
        st.table(df_mostrar.drop(columns=['id']))
        
        st.markdown("### Actualizar Pagos Pendientes")
        df_pendientes = df_cobranza[df_cobranza['Estado'] == 'Pendiente']
        
        if not df_pendientes.empty:
            df_pendientes['display'] = df_pendientes['Cliente'] + " - Deuda: $" + df_pendientes['Total'].astype(str) + " (ID: " + df_pendientes['id'].astype(str) + ")"
            cuenta_a_saldar = st.selectbox("Selecciona la cuenta a marcar como Pagada:", df_pendientes['display'].tolist())
            
            id_saldar = cuenta_a_saldar.split("ID: ")[1].replace(")", "")
            
            if st.button("Marcar como Pagado"):
                c = conn.cursor()
                c.execute("UPDATE cobranza SET estado_pago = 'Pagado' WHERE id = %s", (id_saldar,))
                conn.commit()
                st.success("¡Cuenta actualizada a Pagado exitosamente!")
        else:
            st.info("¡Excelente! No hay cuentas pendientes por cobrar.")
    else:
        st.info("No hay registros de cobranza aún.")

# --- DASHBOARDS Y FINANZAS ---
with tab_dashboards:
    st.title("Inteligencia Financiera")
    
    c = conn.cursor()
    c.execute("SELECT SUM(total_compra) FROM compras")
    inv_mercancia = c.fetchone()[0] or Decimal("0.0")
    c.execute("SELECT SUM(monto) FROM gastos")
    inv_gastos = c.fetchone()[0] or Decimal("0.0")
    c.execute("SELECT SUM(costo_envio) FROM envios")
    inv_envios = c.fetchone()[0] or Decimal("0.0")
    
    inversion_total = inv_mercancia + inv_gastos + inv_envios
    
    c.execute("SELECT SUM(total) FROM ventas")
    ventas_brutas = c.fetchone()[0] or Decimal("0.0")
    
    c.execute("SELECT SUM(km_recorrido) FROM envios")
    km_totales = c.fetchone()[0] or Decimal("0.0")
    
    ganancia_neta = ventas_brutas - inversion_total
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Inversión Total", f"${inversion_total:,.2f}")
    kpi2.metric("Ventas Brutas", f"${ventas_brutas:,.2f}")
    kpi3.metric("Ganancia Neta", f"${ganancia_neta:,.2f}", 
                delta="Rentabilidad" if ganancia_neta > 0 else "Recuperando")
                
    st.markdown("---")
    
    st.subheader("Resumen de Logística")
    col_log1, col_log2 = st.columns(2)
    col_log1.info(f"Costo Total de Envíos: ${inv_envios:,.2f}")
    col_log2.info(f"Distancia Total Recorrida: {km_totales:,.1f} km")
    
    st.markdown("---")
    
    col_graf1, col_graf2 = st.columns(2)
    colores_rosa = ['#E83E8C', '#FF87C3', '#C2185B', '#F48FB1', '#AD1457']
    
    with col_graf1:
        st.subheader("Inversión por Tienda")
        df_tiendas = pd.read_sql_query("""
            SELECT
                tienda,
                SUM(total_compra) AS "Inversion"
            FROM compras
            GROUP BY tienda
        """, conn)
        if not df_tiendas.empty:
            fig_tiendas = px.pie(df_tiendas, values='Inversion', names='tienda', hole=0.4, color_discrete_sequence=colores_rosa)
            fig_tiendas.update_layout(
                paper_bgcolor="#FFFFFF", 
                plot_bgcolor="#FFFFFF",
                font=dict(color="#000000", family="Nunito", size=16)
            )
            st.plotly_chart(fig_tiendas, use_container_width=True)
        else:
            st.info("No hay datos de tiendas.")
            
    with col_graf2:
        st.subheader("Frecuencia de Clientes")
        df_freq = pd.read_sql_query("""
            SELECT
                cliente,
                COUNT(DISTINCT DATE(fecha)) AS "Dias_Comprados"
            FROM ventas
            GROUP BY cliente
            ORDER BY "Dias_Comprados" DESC
        """, conn)
        if not df_freq.empty:
            fig_freq = px.bar(df_freq, x='cliente', y='Dias_Comprados', color_discrete_sequence=["#E83E8C"])
            fig_freq.update_layout(
                xaxis_title="Cliente", 
                yaxis_title="Días de Compra", 
                paper_bgcolor="#FFFFFF", 
                plot_bgcolor="#FFFFFF",
                font=dict(color="#000000", family="Nunito", size=16)
            )
            st.plotly_chart(fig_freq, use_container_width=True)
        else:
            st.info("No hay datos de clientes.")

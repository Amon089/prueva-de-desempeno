#nunca borren un codigo a mitad del examen, no la remontan!!
#nos vemos el otro año ;_;


import uuid
from datetime import datetime

# DATOS GLOBALES (Mínimo requerido)
# Almacena productos.
productos = {} 

# Almacena las ventas. S
SALESS = [] 

# PRE-CARGA (Criterio: 5 productos)
def cargar_datos():
    # Carga productos inisiales
    initial = [
        {"titulo": "la bruja que se creia pupi", "autor": "el emo-roide","categoria":"bisarro", "precio": 9.99,"stok":20},
        {"titulo": "la conquista del pan", "autor": "pato pan","categoria":"historia", "precio": 8.69,"stok":12},
        {"titulo": "a toda velocidad", "autor": "caracol jnson","categoria":"deportes", "precio": 10.99,"stok":100},
        {"titulo": "el caballo que arraña", "autor": "cerdo stanly ","categoria":"comic", "precio": 2.69,"stok":1},
        {"titulo": "mi historia de vida (yisus)", "autor": "yisus  ","categoria":"religion", "precio": 100.0, "stok":600}
       
    ]
    for p in initial:
        ID = str(uuid.uuid4())
        p['id'] = ID
        productos[ID] = p

    print("Cargados 6 productos.")

# AYUDAS / LAMBDA (Cálculo ráIDo)
# Función lambda para calcular el ingreso neto.
calc_ingreso_neto = lambda precio, cant, descuento: (precio * cant) * (1 - descuento) 

def obtener_producto(ID):
    # Obtener productos por id.
    return productos.get(ID)

def obtener_entrada(prompt, tipo_func=str):
    # Entrada raIDa con manejo de error basico.
    while True:
        try:
            return tipo_func(input(prompt))
        except ValueError:
            print("Entrada invalida. intenta de nuebo.") 
        except EOFError:
            print("Saliendo de la entrada.")
            return None

#1: INVENTARIO

def registrar_productos(): 
    # Añadir un nuevo productos.
    print("\n-- nuevo produtos --")
    try:
        titulo = obtener_entrada("Titulo: ")
        autor = obtener_entrada("Autor: ")
        categoria = obtener_entrada("Categoria: ")
        precio = obtener_entrada("precio ($): ", float)
        stock = obtener_entrada("Stok: ", int) 

        if precio <= 0 or stock <= 0:
            raise ValueError("precio y stok deven ser positibos.") 

        ID = str(uuid.uuid4())
        productos[ID] = {
            'id': ID,
            'titulo': titulo, 'autor': autor, 'catgory': categoria, 'precio': precio, 'stok': stock 
        }
        print(f"productos '{titulo}' registrado con ID: {ID}")
    except Exception as e:
        print(f"error registrando productos: {e}")

def consultar_productos():
    # Mostrar todos los productos.
    print("\n-- todos los productos --")
    if not productos:
        print("Inventario basio.")
        return
    for ID, p in productos.items():
        print(f"ID: {ID[:]}... | {p['titulo']} por {p['autor']} | precio: ${p['precio']:.2f} | Stok: {p['stok']}") 

def actualizar_productos():
    # Actualizar productos existente.
    ID = obtener_entrada("\nIngresá ID de productos a actualizar: ")
    p = obtener_producto(ID)
    if not p:
        print("productos no encontrado.")
        return

    print(f"Titulo actual: {p['titulo']}")
    nuevo_precio = obtener_entrada("Nuevo precio (o Enter): ", str)
    if nuevo_precio.strip():
        try:
            nuevo_precio_float = float(nuevo_precio)
            if nuevo_precio_float > 0:
                p['precio'] = nuevo_precio_float 
                print("precio actualizado.")
            else:
                print("precio deve ser positibo.")
        except ValueError:
            print("Formato de precio invalido.")

    
    nuevo_titulo = obtener_entrada("Nuevo Titulo (o Enter): ", str)
    if nuevo_titulo.strip():
        p['titulo'] = nuevo_titulo.strip()
        print("Titulo actualizado.")

def borrar_productos():
    # Remover productos.
    ID = obtener_entrada("\nIngresa ID de productos a borrar: ")
    if ID in productos:
        del productos[ID]
        print(f"productos {ID[:]}... borrado.")
    else:
        print("productos no encontrado.")

# 2: VENTAS

def registrar_venta():
    # Registrar una venta y actualizar stok.
    print("\n-- NUEVA VENTA --")
    try:
        ID = obtener_entrada("ID de productos: ")
        cliente = obtener_entrada("Nombre del Cliente: ")
        cant = obtener_entrada("Cant vendida: ", int)
       # descuento= obtener_entrada("Descuento (0.0 a 1.0): ", float)

        p = obtener_producto(ID)
        if not p:
            print("productos no encontrado.")
            return

        if cant > p['stok']: 
            print(f"ERROR: No hay sufisiente stok. Solo {p['stok']} disponible.") 
            return
        if cant <= 0:
            print("Cant deve ser positiba.")
            return

        # Venta raIDa

        descuento = obtener_entrada("Descuento (0.0 a 1.0): ", float)

        neto = calc_ingreso_neto(p['precio'], cant,descuento) 
        bruto = p['precio'] * cant 

        # Actualiza el stok
        p['stok'] -= cant 

        SALESS.append({
            'cliente': cliente,
            'product_id': ID,
            'cant': cant,
            'fecha': datetime.now().strftime("%Y-%m-%d"),
            'descuento': descuento,
            'neto': neto,
            'bruto': bruto,
            'autor': p['autor'] 
        })
        print(f"Venta registrada. Ingreso Neto: ${neto:.2f}")

    except Exception as e:
        print(f"VENTA FALLIDA: {e}")

def consultar_saless():
    # Mostrar todas las ventas.
    print("\n-- TODAS LAS VENTAS --")
    if not SALESS:
        print("No hay ventas registradas.")
        return
    for s in SALESS:
        print(f"Fecha: {s['fecha']} | Cant: {s['cant']} de {s['product_id'][:4]}... | Cliente: {s['cliente']} | Neto: ${s['neto']:.2f}")

# 3: REPORTES

def menu_reportes():
    # Módulo de reportes.
    if not SALESS:
        print("\nNo hay datos de ventas para reportes.")
        return
    print("\n-- REPORTES --")
    print("1. Top 3 productos Vendidos") 
    print("2. ventas por autor") 
    print("3. neto vs bruto total")
    choice = obtener_entrada("elegi reporte: ", str)

    try:
        if choice == '1':
            # 3: Cuenta las cantidades vendidas
            counts = {}
            for s in SALESS:
                counts[s['product_id']] = counts.get(s['product_id'], 0) + s['cant']

            top3 = sorted(counts.items(), key=lambda item: item[1], reverse=True)[:3]

            print("\n--- TOP 3 ---")
            for i, (ID, total) in enumerate(top3):
                titulo = obtener_producto(ID)['titulo'] if obtener_producto(ID) else "DESCONOSIDO"
                print(f"{i+1}. {titulo} ({total} unidades)")

        elif choice == '2':
            # Ventas por Autor: Agrupa el ingreso neto
            ventas_autor = {}
            for s in SALESS:
                ventas_autor[s['autor']] = ventas_autor.get(s['autor'], 0.0) + s['neto'] 

            print("\n--- VENTAS POR AUTOR ---")
            for autor, total_neto in ventas_autor.items():
                print(f"{autor}: ${total_neto:,.2f}")

        elif choice == '3':
            # Ingreso Neto vs Bruto
            total_neto = sum(s['neto'] for s in SALESS)
            total_bruto = sum(s['bruto'] for s in SALESS)

            print("\n--- INGRESO TOTAL ---")
            print(f"BRUTO (sin descuento): ${total_bruto:,.2f}")
            print(f"NETO (con descuento): ${total_neto:,.2f}")
            print(f"Descuento total aplicado: ${total_bruto - total_neto:,.2f}")

        else:
            print("Opcion de reporte invalida.")

    except Exception as e:
        print(f"ERROR DE REPORTE: {e}")


#MENÚ PRINCIPAL 
def main():
    # Entrada principal del programa.
    cargar_datos()
    while True:
        print("\n===============================")
        print("  SISTEMA (PARA NADA ECHO DE AFAN)")
        print("===============================")
        print("1. entrar al inventario")
        print("2. Nueva Venta")
        print("3. Ver Ventas") 
        print("4. Reportes")
        print("0. Salir")

        choice = obtener_entrada("Ingresá opción: ", str)

        try:
            if choice == '1':
                # Flujo de inventario simplificado
                print("\n-- ACIONES DE INVENTARIO --")
                print("a. Registrar | b. Consultar | c. Actualizar | d. Borrar")
                accion = obtener_entrada("Acción: ", str).lower()
                if accion == 'a': registrar_productos()
                elif accion == 'b': consultar_productos()
                elif accion == 'c': actualizar_productos()
                elif accion == 'd': borrar_productos()
                else: print("Accion invalida.")
            elif choice == '2':
                registrar_venta()
            elif choice == '3':
                consultar_saless()
            elif choice == '4':
                menu_reportes()
            elif choice == '0':
                print("saliendo, adios, chaito")
                break
            else:
                print("Opcion mala.")
        except KeyboardInterrupt:
            print("\nInterrupción de usuario. Volviendo al menu.") 
        except Exception as e:
            print(f"ERROR CRITICO: {e}")

if __name__ == "__main__":
    main()

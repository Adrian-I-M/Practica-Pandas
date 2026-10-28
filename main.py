import datos

def main():
    while True:
        print("\nMenú Práctica Pandas")
        print("1. Generar informes CSV y JSON")
        print("2. Mostrar gráfico de medias")
        print("0. Salir")
        
        opcion = input("Elige una opción: ")
        
        if opcion == "0":
            break
            
        elif opcion == "1":
            try:
                informe = datos.preparar_datos()
                # Reemplazamos los NaN por "N/D" solo para la visualización en consola
                print(informe.astype(object).fillna("N/D").to_string(index=False))
                datos.guardar_informes(informe)
            except FileNotFoundError:
                print("Aviso: Revisa alumnos.csv o notas.csv. Faltan archivos.")
            except Exception as e:
                print(f"Aviso: Error al procesar los datos. {e}")
                
        elif opcion == "2":
            try:
                informe = datos.preparar_datos()
                datos.mostrar_grafico(informe)
            except FileNotFoundError:
                print("Aviso: Revisa alumnos.csv o notas.csv. Faltan archivos.")
            except Exception as e:
                print(f"Aviso: Error al procesar los datos. {e}")
                
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
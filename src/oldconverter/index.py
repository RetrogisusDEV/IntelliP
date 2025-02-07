import re
import os

def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.readlines()
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        return []
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []

def traducir_a_cpp(lineas):
    cpp_code = []
    cpp_code.append("#include <iostream>")
    cpp_code.append("#include <cstdlib>")  # Include for rand()
    cpp_code.append("#include <ctime>")    # Include for time()
    cpp_code.append("using namespace std;")
    cpp_code.append("int main() {")
    cpp_code.append("    srand(time(0));")  # Seed for random number generation

    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()

        # Ignorar líneas vacías y palabras clave de estructura
        if not linea or linea == 'inicio':
            i += 1
            continue

        if linea.startswith("entero"):
            var_name = linea.split()[-1]
            cpp_code.append(f"    int {var_name} = 0;")

        elif linea.startswith("texto"):
            var_name = linea.split()[-1]
            cpp_code.append(f'    string {var_name} = "i";')

        elif linea.startswith("flotante"):
            var_name = linea.split()[-1]
            cpp_code.append(f"    float {var_name} = 0.1;")

        elif linea.startswith("mostrar"):
            mensaje_match = re.findall(r'"(.*?)"', linea)
            if mensaje_match:
                mensaje = mensaje_match[0]
                cpp_code.append(f'    cout << "{mensaje}";')
            elif linea == "mostrar":
                cpp_code.append(f'    cout << "\n";')
            else:
                # Handle concatenation of strings and variables
                parts = linea.split("mostrar")[1].strip().split("+")
                cpp_code.append('    cout << ' + ' << " " << '.join(part.strip() for part in parts) + ' << endl;')

        elif linea.startswith("mientras"):
            condicion_match = re.search(r'mientras\s+(.+?):', linea)
            if condicion_match:
                condicion = condicion_match.group(1)
                cpp_code.append(f"    while ({condicion}) {{")
            else:
                print(f"No se pudo parsear la condición: {linea}")

        elif linea.startswith("si"):
            condicion_match = re.search(r'si\s+(.+?):', linea)
            if condicion_match:
                condicion = condicion_match.group(1)
                cpp_code.append(f"    if ({condicion}) {{")

                # Buscar el siguiente bloque
                i += 1
                while i < len(lineas):
                    next_line = lineas[i].strip()
                    if next_line == "sino":
                        cpp_code.append("    } else {")
                        i += 1
                        continue
                    elif next_line.startswith("f_si"):
                        cpp_code.append("    }")
                        break
                    elif next_line.startswith("mostrar"):
                        mensaje_match = re.findall(r'"(.*?)"', next_line)
                        if mensaje_match:
                        mensaje = mensaje_match[0]
                        cpp_code.append(f'    cout << "{mensaje}";')
                        elif next_line == "mostrar":
                        cpp_code.append(f'    cout << "\n";')
                        else:
                        # Handle concatenation of strings and variables
                        parts = next_line.split("mostrar")[1].strip().split("+")
                        cpp_code.append('    cout << ' + ' << " " << '.join(part.strip() for part in parts) + ' << endl;')
                        
                    else:
                        cpp_code.append(f"        {next_line}")
                    i += 1
            else:
                print(f"No se pudo parsear la condición: {linea}")

        elif linea.startswith("f_mientras"):
            cpp_code.append("    }")

        elif linea == "fin":
            # evitar que el compilador cierre el cmd 
            cpp_code.append('    system("pause");')
            cpp_code.append("    return 0;")
            cpp_code.append("}")

        elif linea.startswith("mrandom"):
            match = re.search(r'mrandom\((\d+),\s*(\d+)\)', linea)
            if match:
                min_val = match.group(1)
                max_val = match.group(2)
                cpp_code.append(f'    cout << rand() % ({max_val} - {min_val} + 1) + {min_val} << endl;')

        i += 1

    return "\n".join(cpp_code)

def escribir_archivo(nombre_archivo, contenido):
    # Ensure the output directory exists
    output_dir = os.path.dirname(nombre_archivo)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)
        print(f"Archivo '{nombre_archivo}' generado exitosamente.")
    except Exception as e:
        print(f"Error al escribir el archivo: {e}")

def main():
    print("Starting the conversion process...")

    lineas = leer_archivo("../main_program.ipce")  # Updated path
    if lineas:
        cpp_code = traducir_a_cpp(lineas)
        print("Conversion completed successfully.")

        escribir_archivo("cpp_output/output.cpp", cpp_code)
        print("Traducción completada. Código C++ generado en 'cpp_output/output.cpp'.")

if __name__ == "__main__":
    main()
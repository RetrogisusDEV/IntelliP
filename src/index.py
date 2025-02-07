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

def agregar_linea(cpp_code, line, indent_level):
    indent = '    ' * indent_level
    cpp_code.append(f"{indent}{line}")

def traducir_a_cpp(lineas):
    cpp_code = []
    agregar_linea(cpp_code, "#include <iostream>", 0)
    agregar_linea(cpp_code, "#include <cstdlib>", 0)
    agregar_linea(cpp_code, "#include <ctime>", 0)
    agregar_linea(cpp_code, "using namespace std;", 0)
    agregar_linea(cpp_code, "int main() {", 0)
    agregar_linea(cpp_code, "    srand(time(0));", 1)

    indent_level = 1
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()

        if not linea or linea == 'inicio':
            i += 1
            continue

        if linea.startswith("entero"):
            var_name = linea.split()[-1]
            agregar_linea(cpp_code, f"int {var_name} = 0;", indent_level)

        elif linea.startswith("texto"):
            var_name = linea.split()[-1]
            agregar_linea(cpp_code, f'string {var_name} = "";', indent_level)

        elif linea.startswith("flotante"):
            var_name = linea.split()[-1]
            agregar_linea(cpp_code, f"float {var_name} = 0.0f;", indent_level)

        elif linea.startswith("mostrar"):
            mensaje_match = re.findall(r'"(.*?)"', linea)
            if mensaje_match:
                mensaje = mensaje_match[0]
                agregar_linea(cpp_code, f'cout << "{mensaje}" << endl;', indent_level)
            elif linea == "mostrar":
                agregar_linea(cpp_code, 'cout << endl;', indent_level)
            else:
                parts = linea.split("mostrar")[1].strip().split("+")
                agregar_linea(cpp_code, 'cout << ' + ' << " " << '.join(part.strip() for part in parts) + ' << endl;', indent_level)

        elif linea.startswith("mientras"):
            condicion_match = re.search(r'mientras\s+(.+?):', linea)
            if condicion_match:
                condicion = condicion_match.group(1)
                agregar_linea(cpp_code, f"while ({condicion}) {{", indent_level)
                indent_level += 1
            else:
                print(f"No se pudo parsear la condición: {linea}")

        elif linea.startswith("si"):
            condicion_match = re.search(r'si\s+(.+?):', linea)
            if condicion_match:
                condicion = condicion_match.group(1)
                agregar_linea(cpp_code, f"if ({condicion}) {{", indent_level)
                indent_level += 1

                i += 1
                while i < len(lineas):
                    next_line = lineas[i].strip()
                    if next_line == "sino":
                        agregar_linea(cpp_code, "} else {", indent_level - 1)
                        indent_level += 1
                        i += 1
                        continue
                    elif next_line.startswith("f_si"):
                        agregar_linea(cpp_code, "}", indent_level - 1)
                        indent_level -= 1
                        break
                    elif next_line.startswith("mostrar"):
                        mensaje_match = re.findall(r'"(.*?)"', next_line)
                        if mensaje_match:
                            mensaje = mensaje_match[0]
                            agregar_linea(cpp_code, f'cout << "{mensaje}" << endl;', indent_level)
                        elif next_line == "mostrar":
                            agregar_linea(cpp_code, 'cout << endl;', indent_level)
                        else:
                            parts = next_line.split("mostrar")[1].strip().split("+")
                            agregar_linea(cpp_code, 'cout << ' + ' << " " << '.join(part.strip() for part in parts) + ' << endl;', indent_level)
                    else:
                        agregar_linea(cpp_code, next_line, indent_level)
                    i += 1
            else:
                print(f"No se pudo parsear la condición: {linea}")

        elif linea.startswith(" f_mientras"):
            agregar_linea(cpp_code, "}", indent_level - 1)
            indent_level -= 1

        elif linea == "fin":
            agregar_linea(cpp_code, 'system("pause");', indent_level)
            agregar_linea(cpp_code, "return 0;", indent_level)
            agregar_linea(cpp_code, "}", 0)

        elif linea.startswith("mrandom"):
            match = re.search(r'mrandom\((\d+),\s*(\d+)\)', linea)
            if match:
                min_val = match.group(1)
                max_val = match.group(2)
                agregar_linea(cpp_code, f'cout << rand() % ({max_val} - {min_val} + 1) + {min_val} << endl;', indent_level)

        i += 1

    return "\n".join(cpp_code)

def escribir_archivo(nombre_archivo, contenido):
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
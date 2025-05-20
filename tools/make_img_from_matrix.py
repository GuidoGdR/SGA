
import matplotlib.pyplot as plt

def make_img_from_matrix(path:str, data:list[list]):

    # Cubro error por si la lista(data) solo tiene los encabezados
    if data.__len__() == 1:
        data.append([])
        for i in data[0]:
            data[1].append("")
    
    fig, ax = plt.subplots()

    # Ocultar los ejes
    ax.axis('off')

    # Crear la tabla
    print(data[0])
    print(data[1:])
    table = ax.table(cellText=data[1:],  # Datos de las filas
                    colLabels=data[0],   # Encabezados de las columnas
                    loc='center')        # Ubicación de la tabla

    # Ajustar el tamaño de las celdas (opcional)
    #table.auto_set_font_size(False)
    #table.set_fontsize(10)
    #table.scale(1, 1.5)  # Ancho y alto de las celdas

    plt.savefig(path, bbox_inches='tight')
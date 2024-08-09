def reorder_list(original_list, order):
    """
    Reordena una lista según los valores especificados en otra lista.

    Parameters:
    original_list (list): La lista original a reordenar.
    order (list): Una lista de índices que indica el nuevo orden.

    Returns:
    list: La lista reordenada.
    """
    # Crear un diccionario para mapear índices a valores de la lista original
    index_to_value = {index: original_list[index] for index in range(len(original_list))}
    
    # Reordenar la lista original según los valores en 'order'
    reordered_list = [index_to_value[i] for i in order]
    return reordered_list

# Ejemplo de uso
original_list = ['a', 'b', 'c', 'd', 'e']
order = [2, 1, 0, 4, 3]  # Índices que indican el nuevo orden

reordered_list = reorder_list(original_list, order)
print(reordered_list)
# Salida: ['c', 'd', 'b', 'e', 'a']

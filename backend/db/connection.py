# Conexión a Supabase
import streamlit as st
import os
from dotenv import load_dotenv
import re
from .supabase_client import get_supabase_client

# Cargar variables de entorno
load_dotenv()

def execute_query(query, params=None, fetchone=False, commit=False):
    """
    Ejecuta una consulta usando la API de Supabase.
    
    Args:
        query: Consulta SQL a ejecutar
        params: Parámetros para la consulta (puede ser dict, tuple o list)
        fetchone: Si solo se debe devolver un resultado
        commit: Si se debe confirmar la transacción (ignorado en Supabase)
        
    Returns:
        Resultados de la consulta
    """
    return execute_supabase_query(query, params, fetchone)

def execute_supabase_query(query, params=None, fetchone=False):
    """
    Ejecuta una consulta SQL usando la API REST de Supabase con manejo mejorado de parámetros.
    """
    supabase = get_supabase_client()
    query_lower = query.strip().lower()
    
    try:
        # Consultas SELECT
        if query_lower.startswith("select"):
            return handle_select_query(supabase, query, params, fetchone)
            
        # Consultas INSERT
        elif query_lower.startswith("insert"):
            return handle_insert_query(supabase, query, params, fetchone)
            
        # Consultas UPDATE
        elif query_lower.startswith("update"):
            return handle_update_query(supabase, query, params)
            
        # Consultas DELETE
        elif query_lower.startswith("delete"):
            return handle_delete_query(supabase, query, params)
            
        # Otras consultas no soportadas directamente
        else:
            admin_client = get_supabase_client(admin=True)
            result = admin_client.rpc('execute_sql', {'sql_query': query, 'params': params_to_dict(params, query)})
            return result.data

    except Exception as e:
        print(f"Error en consulta Supabase: {str(e)}")
        raise e

def handle_select_query(supabase, query, params, fetchone):
    """Maneja consultas SELECT adaptándolas a la API de Supabase"""
    # Obtener nombre de tabla
    match = re.search(r'from\s+([^\s,;()]+)', query.lower())
    if not match:
        raise ValueError(f"No se pudo extraer el nombre de la tabla de la consulta: {query}")
        
    table_name = match.group(1).strip()
    
    # Crear consulta básica
    query_builder = supabase.table(table_name).select("*")
    
    # Extraer cláusulas WHERE
    where_match = re.search(r'where\s+(.*?)(?:order by|group by|limit|$)', query.lower())
    if where_match and params:
        # El manejo de WHERE es básico - necesita mejoras para consultas complejas
        where_clause = where_match.group(1).strip()
        
        # Convertir parámetros a diccionario si son tupla/lista
        param_dict = params_to_dict(params, where_clause)
        
        # Aplicar filtros
        for key, value in param_dict.items():
            query_builder = query_builder.eq(key, value)
    
    # Ejecutar consulta
    result = query_builder.execute()
    
    # Formatear resultado
    if fetchone:
        return result.data[0] if result.data else None
    return result.data

def handle_insert_query(supabase, query, params, fetchone):
    """Maneja consultas INSERT adaptándolas a la API de Supabase"""
    # Extraer nombre de tabla
    match = re.search(r'insert\s+into\s+([^\s(]+)', query.lower())
    if not match:
        raise ValueError(f"No se pudo extraer el nombre de la tabla: {query}")
    
    table_name = match.group(1).strip()
    
    # Convertir parámetros para Supabase
    if isinstance(params, dict):
        insert_data = params
    elif isinstance(params, (list, tuple)):
        # Extraer nombres de columnas de la consulta
        columns_match = re.search(r'\(([^)]+)\)', query)
        if columns_match:
            column_names = [c.strip() for c in columns_match.group(1).split(',')]
            
            # Si params es una lista/tupla plana, crear un solo diccionario
            if not any(isinstance(p, (list, tuple)) for p in params):
                insert_data = dict(zip(column_names, params))
            else:
                # Si params contiene múltiples conjuntos de valores
                raise ValueError("Inserciones múltiples no implementadas directamente")
        else:
            raise ValueError("No se pudieron extraer nombres de columnas para la inserción")
    else:
        insert_data = {}
    
    # Ejecutar inserción
    result = supabase.table(table_name).insert(insert_data).execute()
    
    # Devolver resultado
    if fetchone:
        return result.data[0] if result.data else None
    return result.data

def handle_update_query(supabase, query, params):
    """Maneja consultas UPDATE adaptándolas a la API de Supabase"""
    # Extraer nombre de tabla
    match = re.search(r'update\s+([^\s]+)', query.lower())
    if not match:
        raise ValueError(f"No se pudo extraer el nombre de la tabla: {query}")
    
    table_name = match.group(1).strip()
    
    # Extraer cláusula WHERE
    where_match = re.search(r'where\s+(.*?)$', query.lower())
    if not where_match:
        raise ValueError("Actualizaciones sin cláusula WHERE no están soportadas")
    
    where_clause = where_match.group(1).strip()
    
    # Extraer columnas a actualizar
    set_match = re.search(r'set\s+(.*?)\s+where', query.lower())
    if not set_match:
        raise ValueError("No se pudo extraer la cláusula SET")
    
    set_clause = set_match.group(1).strip()
    
    # Convertir parámetros a diccionario
    if isinstance(params, dict):
        update_data = params
        where_conditions = {}  # Esto necesitaría extracción más avanzada
    elif isinstance(params, (list, tuple)):
        # Dividir parámetros entre SET y WHERE
        # Esto es una simplificación y puede no funcionar para casos complejos
        set_parts = set_clause.split(',')
        num_set_params = len(set_parts)
        
        update_data = {}
        for i, part in enumerate(set_parts):
            if '=' in part:
                col = part.split('=')[0].strip()
                if i < len(params):
                    update_data[col] = params[i]
        
        # Construir condición WHERE
        where_conditions = {}
        id_match = re.search(r'(\w+)\s*=\s*\$', where_clause)
        if id_match and num_set_params < len(params):
            where_conditions[id_match.group(1)] = params[num_set_params]
    else:
        update_data = {}
        where_conditions = {}
    
    # Ejecutar actualización
    return supabase.table(table_name).update(update_data).eq(list(where_conditions.keys())[0], list(where_conditions.values())[0]).execute()

def handle_delete_query(supabase, query, params):
    """Maneja consultas DELETE adaptándolas a la API de Supabase"""
    # Extraer nombre de tabla
    match = re.search(r'delete\s+from\s+([^\s]+)', query.lower())
    if not match:
        raise ValueError(f"No se pudo extraer el nombre de la tabla: {query}")
    
    table_name = match.group(1).strip()
    
    # Extraer cláusula WHERE
    where_match = re.search(r'where\s+(.*?)$', query.lower())
    if not where_match:
        raise ValueError("Eliminaciones sin cláusula WHERE no están soportadas")
    
    where_clause = where_match.group(1).strip()
    
    # Convertir parámetros para Supabase
    if isinstance(params, dict):
        condition_key = list(params.keys())[0]
        condition_value = params[condition_key]
    elif isinstance(params, (list, tuple)) and len(params) > 0:
        # Extraer columna de condición
        condition_match = re.search(r'(\w+)\s*=', where_clause)
        if condition_match:
            condition_key = condition_match.group(1)
            condition_value = params[0]
        else:
            raise ValueError("No se pudo extraer condición para DELETE")
    else:
        raise ValueError("Se requieren parámetros para DELETE")
    
    # Ejecutar eliminación
    return supabase.table(table_name).delete().eq(condition_key, condition_value).execute()

def params_to_dict(params, query_part):
    """
    Convierte parámetros de lista/tupla a diccionario basándose en la consulta.
    
    Args:
        params: Parámetros en formato lista/tupla
        query_part: Parte de la consulta SQL que contiene referencias a parámetros
        
    Returns:
        dict: Parámetros en formato diccionario
    """
    if params is None:
        return {}
        
    if isinstance(params, dict):
        return params
        
    # Buscar parámetros en formato $1, $2, etc.
    param_refs = re.findall(r'(\w+)\s*=\s*\$\d+', query_part)
    
    # Si encontramos referencias a parámetros, crear diccionario
    if param_refs and len(param_refs) <= len(params):
        return {param_refs[i]: params[i] for i in range(len(param_refs))}
    
    # Si no hay suficiente información, intentar extraer de otra forma
    # Este es un caso de contingencia y puede no funcionar correctamente
    column_values = re.findall(r'(\w+)\s*=', query_part)
    if column_values and len(column_values) <= len(params):
        return {column_values[i]: params[i] for i in range(len(column_values))}
    
    return {}

def test_connection():
    """
    Prueba la conexión a Supabase.
    """
    try:
        supabase = get_supabase_client()
        # Probar una consulta simple
        result = supabase.table("categories").select("*", count='exact').execute()
        print(f"Conexión exitosa a Supabase. {len(result.data)} categorías encontradas.")
        return True
    except Exception as e:
        print(f"Error al conectar a Supabase: {e}")
        return False

if __name__ == "__main__":
    test_connection()
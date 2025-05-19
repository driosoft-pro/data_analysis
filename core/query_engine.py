import duckdb
import pandas as pd

class QueryEngine:
    """Motor de consultas SQL para DataFrames utilizando DuckDB"""
    
    def __init__(self, dataframe=None):
        self.dataframe = dataframe
        self.connection = duckdb.connect(database=':memory:', read_only=False)
        self.table_name = 'data_table'
        
        if dataframe is not None:
            self.register_dataframe(dataframe)
    
    def register_dataframe(self, dataframe, table_name='data_table'):
        """Registrar un DataFrame como tabla en DuckDB"""
        self.dataframe = dataframe
        self.table_name = table_name
        self.connection.register(table_name, dataframe)
        return True
    
    def execute_query(self, query):
        """Ejecutar una consulta SQL en DuckDB"""
        if self.dataframe is None:
            return None, "No hay datos cargados"
        
        try:
            result = self.connection.execute(query).fetchdf()
            return result, f"Consulta ejecutada correctamente. Filas: {len(result)}"
        except Exception as e:
            return None, f"Error al ejecutar la consulta: {str(e)}"
    
    def get_table_schema(self):
        """Obtener el esquema de la tabla registrada"""
        if self.dataframe is None:
            return None, "No hay datos cargados"
        
        try:
            schema_query = f"DESCRIBE {self.table_name}"
            schema = self.connection.execute(schema_query).fetchdf()
            return schema, "Esquema obtenido correctamente"
        except Exception as e:
            return None, f"Error al obtener el esquema: {str(e)}"
    
    def get_sample_queries(self):
        """Generar ejemplos de consultas SQL para el DataFrame cargado"""
        if self.dataframe is None:
            return None, "No hay datos cargados"
        
        column_names = self.dataframe.columns.tolist()
        numeric_columns = self.dataframe.select_dtypes(include=['number']).columns.tolist()
        categorical_columns = self.dataframe.select_dtypes(include=['object', 'category']).columns.tolist()
        
        sample_queries = []
        
        # Consulta básica para ver todas las columnas y filas
        sample_queries.append({
            "title": "Ver todos los datos",
            "query": f"SELECT * FROM {self.table_name} LIMIT 10;"
        })
        
        # Consulta para ver el número total de filas
        sample_queries.append({
            "title": "Contar filas",
            "query": f"SELECT COUNT(*) AS total_rows FROM {self.table_name};"
        })
        
        # Si hay columnas numéricas, generar consultas para estadísticas
        if numeric_columns:
            col = numeric_columns[0]
            sample_queries.append({
                "title": f"Estadísticas de {col}",
                "query": f"SELECT MIN({col}) as min_value, MAX({col}) as max_value, AVG({col}) as mean, STDDEV({col}) as std_dev FROM {self.table_name};"
            })
        
        # Si hay columnas categóricas, generar consultas para contar frecuencias
        if categorical_columns:
            col = categorical_columns[0]
            sample_queries.append({
                "title": f"Frecuencia de valores en {col}",
                "query": f"SELECT {col}, COUNT(*) as frequency FROM {self.table_name} GROUP BY {col} ORDER BY frequency DESC LIMIT 10;"
            })
        
        # Si hay al menos dos columnas numéricas, generar consulta para correlación
        if len(numeric_columns) >= 2:
            col1 = numeric_columns[0]
            col2 = numeric_columns[1]
            sample_queries.append({
                "title": f"Correlación entre {col1} y {col2}",
                "query": f"SELECT CORR({col1}, {col2}) as correlation FROM {self.table_name};"
            })
        
        # Consulta para filtrar datos
        if len(column_names) > 0:
            col = column_names[0]
            sample_queries.append({
                "title": f"Filtrar por condición en {col}",
                "query": f"SELECT * FROM {self.table_name} WHERE {col} IS NOT NULL ORDER BY {col} DESC LIMIT 10;"
            })
        
        return sample_queries, "Consultas de ejemplo generadas correctamente"
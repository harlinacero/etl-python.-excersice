import json
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

def extract(file_path):
    print("Extrayendo datos del archivo:", file_path)
    data = pd.read_csv(file_path, sep=';')
    return data

def convertir_tiempo(tiempo):
    try:
        tiempo = str(tiempo)  # Asegurarse de que tiempo sea una cadena
        if 'TRIMESTRE' in tiempo:
            if 'ANIOS' in tiempo:
                num_anios = int(tiempo.split('_')[0])
                return num_anios * 4
            else:
                num_trimestres = int(tiempo.split('_')[0])
                return num_trimestres
        elif 'TRIMESTRES' in tiempo:
            num_trimestres = int(tiempo.split('_')[0])
            return num_trimestres
        elif 'ANIOS' in tiempo:
            num_anios = int(tiempo.split('_')[0])
            return num_anios * 4
        else:
            return 0
    except (ValueError, IndexError):
        return 0

# Convertir los valores a cadenas antes de mapearlos
def transform_dimension_data(data, mappings):
    data = data.copy()
    data['Description'] = data.iloc[:, 0].astype(str).map(mappings).fillna('null')
    return data

def transform_fact_data(data, mappings, columns):
    data = data.copy()
    for column in columns:
        if column in data.columns:
            data[column] = data[column].astype(str).map(mappings).fillna('null')
    return data

def load(data, table_mappings, dimension_mappings, connection_string):
    print("Iniciando el proceso de carga de datos")
    
    data.columns = data.columns.str.strip().str.lower()
    table_mappings = {k.lower(): v for k, v in table_mappings.items()}

    # Crear el motor de conexión usando sqlalchemy
    engine = create_engine(connection_string)
    metadata = MetaData()    
   
    # Crear las tablas para los datos de las columnas    
    for column_name, table_name in table_mappings.items():
        column_name_normalized = column_name.strip().lower()
        
        if column_name_normalized not in data.columns:
            print(f"Advertencia: La columna '{column_name}' no existe en los datos.")
            continue

        print(f"Procesando columna '{column_name}' para la tabla '{table_name}'")
              
        column1_name = f'{table_name}_ID'
        column2_name = f'{table_name}_Name'
        if column_name in ['epareg_rel_act', 'epareg_ocu_sit_lab', 'relacion_actividad']:
            column2_name = column2_name.replace('Name', 'Description')
        
        if column_name in ['epareg_rel_act', 'epareg_ocu_sit_lab']:
            column2_name = column2_name.replace(f'EPAREG_', '')  
        
        table = Table(table_name, metadata,
                      Column(column1_name, Integer, primary_key=True, autoincrement=True),
                      Column(column2_name, String, unique=True),
                      Column('Description', String))
        
        metadata.create_all(engine)

        # Obtener los datos existentes de la tabla
        existing_data = pd.read_sql_table(table_name, con=engine)
        # Obtener el valor máximo actual de la columna ID
        max_id = existing_data[column1_name].max() if not existing_data.empty else 0
        
        # Preparar los datos para insertar
        column_data = data[[column_name_normalized]].dropna().drop_duplicates().reset_index(drop=True)
        column_data[column1_name] = column_data.index + 1 + max_id
        column_data.columns = [column2_name, column1_name]
        
        # Transformar los datos agregando la columna 'Descripción'
        column_data = transform_dimension_data(column_data, dimension_mappings.get(table_name, {}))
         
        # Filtrar los datos que ya existen
        new_data = column_data[~column_data[column2_name].isin(existing_data[column2_name])]
        
        if not new_data.empty:
            print(f"Datos nuevos para insertar en la tabla '{table_name}':\n{new_data}")
            # Insertar los datos nuevos en la tabla
            new_data.to_sql(table_name, con=engine, if_exists='append', index=False)
            print(f"Datos insertados en la tabla '{table_name}'")
        else:
            print(f"No hay datos nuevos para insertar en la tabla '{table_name}'")
        
    # Procesar la tabla Graduate
    print("Procesando datos para la tabla 'Graduate'")
    graduate_data = data[['titulacion', 'rama_ensenianza', 'nivel_academico', 'universidades', 'tiempo_egreso',
                          'time_period', 'sexo', 'lugar_residencia', 'epareg_rel_act', 'epareg_ocu_sit_lab', 'relacion_actividad',
                          'mat015_1', 'mat015_2', 'mat015_3', 'mat026_1', 'mat026_2', 'mat026_3']].dropna().drop_duplicates().reset_index(drop=True)
    graduate_data.columns = ['Degree_ID', 'Teaching_Field_ID', 'Academic_Level_ID', 'University_ID', 'End_Term', 
                           'Graduation_Term', 'Gender_ID', 'Residence_Place_ID', 'EPAREG_Activity_Relation_ID', 'EPAREG_Employment_Status_ID', 
                           'Activity_Relation_ID', 'Additional_Enrollment_ULL1', 'Additional_Enrollment_ULL2', 
                           'Additional_Enrollment_ULL3', 'Additional_Enrollment_ULPGC1', 'Additional_Enrollment_ULPGC2', 'Additional_Enrollment_ULPGC3']
    
    # Aplicar la función convertir_tiempo a las columnas End_Term y Graduation_Term
    graduate_data['End_Term'] = graduate_data['End_Term'].apply(convertir_tiempo)
    # graduate_data['Graduation_Term'] = graduate_data['Graduation_Term'].apply(convertir_tiempo)
    
    # Mapear los valores a los IDs correspondientes
    for column_name, table_name in {'Degree_ID': 'Degree',
                                    'Teaching_Field_ID': 'Teaching_Field', 
                                    'Academic_Level_ID': 'Academic_Level', 
                                    'University_ID': 'University',
                                    'Gender_ID': 'Gender',
                                    'Residence_Place_ID': 'Residence_Place',
                                    'EPAREG_Activity_Relation_ID': 'EPAREG_Activity_Relation',
                                    'EPAREG_Employment_Status_ID': 'EPAREG_Employment_Status',
                                    'Activity_Relation_ID': 'Activity_Relation'}.items():
        table_data = pd.read_sql_table(table_name, con=engine)
        id_column = f'{table_name}_ID'
        name_column = f'{table_name}_Name'
        
        if table_name in ['EPAREG_Activity_Relation', 'EPAREG_Employment_Status', 'Activity_Relation']:
            name_column = name_column.replace('Name', 'Description')
        
        if table_name in ['EPAREG_Activity_Relation', 'EPAREG_Employment_Status']:
            name_column = name_column.replace(f'EPAREG_', '') 
        
        mapping = dict(zip(table_data[name_column], table_data[id_column]))
        # Convertir los valores a cadenas antes de mapear
        graduate_data[column_name] = graduate_data[column_name].astype(str).map(mapping)
    
    
    graduate_data['Graduate_ID'] = graduate_data.index + 1
    
    additional_enrollment_mappings = dimension_mappings.get('Additional_Enrollment', {})
    columns_to_transform = [
        'Additional_Enrollment_ULL1', 
        'Additional_Enrollment_ULL2', 
        'Additional_Enrollment_ULL3', 
        'Additional_Enrollment_ULPGC1', 
        'Additional_Enrollment_ULPGC2', 
        'Additional_Enrollment_ULPGC3'
    ]
    graduate_data = transform_fact_data(graduate_data, additional_enrollment_mappings, columns_to_transform)
    
    graduate_data = graduate_data.drop_duplicates(subset=['Degree_ID', 'Teaching_Field_ID', 'Academic_Level_ID', 'University_ID',
                                                          'Gender_ID', 'Residence_Place_ID', 'EPAREG_Activity_Relation_ID', 'EPAREG_Employment_Status_ID',
                                                          'Activity_Relation_ID'])
    
    graduate_table = Table(
        'Graduate', metadata,
        Column('Graduate_ID', Integer, primary_key=True, autoincrement=True),
        Column('Degree_ID', Integer, ForeignKey('Degree.Degree_ID')),
        Column('Teaching_Field_ID', Integer, ForeignKey('Teaching_Field.Teaching_Field_ID')),
        Column('Academic_Level_ID', Integer, ForeignKey('Academic_Level.Academic_Level_ID')),
        Column('University_ID', Integer, ForeignKey('University.University_ID')),        
        Column('Gender_ID', Integer, ForeignKey('Gender.Gender_ID')),        
        Column('Residence_Place_ID', Integer, ForeignKey('Residence_Place.Residence_Place_ID')),        
        Column('EPAREG_Activity_Relation_ID', Integer, ForeignKey('EPAREG_Activity_Relation.EPAREG_Activity_Relation_ID')),        
        Column('EPAREG_Employment_Status_ID', Integer, ForeignKey('EPAREG_Employment_Status.EPAREG_Employment_Status_ID')),        
        Column('Activity_Relation_ID', Integer, ForeignKey('Activity_Relation.Activity_Relation_ID')),        
        Column('Additional_Enrollment_ULL1', Integer),
        Column('Additional_Enrollment_ULL2', Integer),
        Column('Additional_Enrollment_ULL3', Integer),
        Column('Additional_Enrollment_ULPGC1', Integer),
        Column('Additional_Enrollment_ULPGC2', Integer),
        Column('Additional_Enrollment_ULPGC3', Integer)
    )

    # Crear la tabla en la base de datos si no existe
    metadata.create_all(engine)
    graduate_data.to_sql('Graduate', con=engine, if_exists='append', index=False)
    
    print("Datos insertados en la tabla 'Graduate'")
    
    
def main():
    input_file_path = 'c00051a__microdatos_edatos_2012-2022_ckan.csv'
    connection_string = 'mssql+pyodbc://sa:hA1077033560@localhost:1434/InsertionJob?driver=ODBC+Driver+17+for+SQL+Server'
    
    # Leer el archivo JSON
    with open('dimension_mappings.json', 'r', encoding='utf-8') as file:
        dimension_mappings = json.load(file) 
    
    table_mappings = {
        'universidades': 'University',
        'rama_ensenianza': 'Teaching_Field',
        'nivel_academico': 'Academic_Level',
        'sexo': 'Gender',
        'lugar_residencia': 'Residence_Place',
        'epareg_rel_act': 'EPAREG_Activity_Relation',
        'epareg_ocu_sit_lab': 'EPAREG_Employment_Status',
        'relacion_actividad': 'Activity_Relation',
        'titulacion': 'Degree'        
    }   
    
    data = extract(input_file_path)
    load(data, table_mappings, dimension_mappings, connection_string)
    print("Proceso ETL completado")

main()


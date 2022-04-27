import pandas as pd

PROCESSED_DATA_PATH = 'data/processed/'


def clean_cedis(cedis_db_path: str):

    cedis_df = pd.read_excel(cedis_db_path, header=2)
    cedis_df.columns = cedis_df.columns.str.strip()
    cedis_df['CEDIS REG'] = cedis_df['CEDIS REG'].str.strip()
    cedis_df['DOMICILIO'] = cedis_df['DOMICILIO'].str.strip()
    cedis_df['COLONIA'] = cedis_df['COLONIA'].str.strip()
    cedis_df['CIUDAD'] = cedis_df['CIUDAD'].str.strip()
    cedis_df[['coord1', 'coord2']] = cedis_df['Coordenadas'].str.split(
        ',', expand=True)

    # Save to csv
    cedis_df.to_csv(PROCESSED_DATA_PATH + 'cedis.csv', index=False)


def clean_products(products_db_path: str):

    products_df = pd.read_excel(products_db_path, header=1)
    products_df.CATEGORIAS = products_df.CATEGORIAS.str.strip()
    products_df.Articulo = products_df.Articulo.str.strip()
    products_df.Marca = products_df.Marca.str.strip()
    products_df.Modelo = products_df.Modelo.str.strip()

    # Save to csv
    products_df.to_csv(PROCESSED_DATA_PATH + 'products.csv', index=False)


def clean_deliveries(deliveries_db_path: str):

    # Read the data
    deliveries_df = pd.read_csv(deliveries_db_path)
    deliveries_df.columns = deliveries_df.columns.str.strip()
    deliveries_df = deliveries_df.drop(columns=['Distribución'])

    # Converting dates to datetime
    deliveries_df['fechaventa'] = pd.to_datetime(
        deliveries_df['fechaventa'], infer_datetime_format=True)
    deliveries_df['fechaenrutada'] = pd.to_datetime(
        deliveries_df['fechaenrutada'], infer_datetime_format=True)

    # Keep only the latest deliveries
    deliveries_df = deliveries_df[deliveries_df['fechaenrutada']
                                  == deliveries_df['fechaenrutada'].max()]
    deliveries_df.dropna(inplace=True)

    # Proposed full address
    deliveries_df['full_address'] = deliveries_df['nombrecalle'].str.strip().str.lower() + ',' + \
        deliveries_df['numerodecasa'].astype(int).astype(str).str.strip() + ',' + \
        deliveries_df['departamento'].str.strip() + ',' + \
        deliveries_df['nombreciudad'].str.strip().str.lower() + ',' + \
        deliveries_df['num_codigopostal'].astype(int).astype(
            str).str.strip() + ',Nuevo León, México'

    # Keep only deliveries, not returns
    deliveries_df = deliveries_df[deliveries_df['cantidad'] > 0]

    # Save to csv
    deliveries_df.to_csv(PROCESSED_DATA_PATH +
                         'latest-deliveries.csv', index=False)


def clean_vehicles(vehicles_db_path: str):
    vehicles_df = pd.read_excel(vehicles_db_path)

    # Save it to csv
    vehicles_df.to_csv(PROCESSED_DATA_PATH + 'vehicles.csv', index=False)


def clean_all_data():

    clean_products('./data/raw/sku_DCF_Volumen.xls')
    clean_cedis('./data/raw/direcciones-Cedis-Coppel.xls')
    clean_deliveries('./data/raw/Monterrey-2021.csv')
    clean_vehicles('./data/raw/catalogo-unidades-enero-2022-Cedis.xls')


if __name__ == '__main__':
    print('Cleaning data...')
    clean_all_data()
    print('Done!')

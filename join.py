import pandas as pd

def join_excel_files(file_paths):
    dataframes = [pd.read_excel(file_path) for file_path in file_paths]
    combined_dataframe = pd.concat(dataframes, ignore_index=True)
    combined_dataframe.to_excel('combined_output.xlsx', index=False)

    print("Files joined successfully. Combined data written to:")

# List of file paths to the three Excel files you want to join
file_paths = ['C:/Users/joaop/Downloads/BRL/3PagamentoPendente.xls', 'C:/Users/joaop/Downloads/BRL/2PagamentoPendente.xls', 'C:/Users/joaop/Downloads/BRL/1PagamentoPendente.xls']

# Call the function with the list of file paths
join_excel_files(file_paths)

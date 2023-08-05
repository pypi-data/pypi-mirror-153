import subprocess as sp
from wsgiref import headers
import pandas as pd
import matplotlib.pyplot as plt
import sys,os 
import numpy as np

if os.path.exists('./WtoData_20220530175908.xlsx'):
    df = pd.read_excel('WtoData_20220530175908.xlsx', header=0, skiprows=2, usecols="B:H")
else:
    sp.call("wget https://github.com/noboru-knm/World-Trade-Visualization/raw/main/WtoData_20220530175908.xlsx",shell=True)
    df = pd.read_excel('WtoData_20220530175908.xlsx', header=0, skiprows=2, usecols="B:H")

new_df = df.replace(['MT2 - 01 - Animal products', 'MT2 - 02 - Dairy products', 'MT2 - 03 - Fruits, vegetables, plants', 'MT2 - 04 - Coffee, tea',
                    'MT2 - 05 - Cereals and preparations', 'MT2 - 06 - Oilseeds, fats and oils', 'MT2 - 07 - Sugars and confectionery',
                    'MT2 - 08 - Beverages and tobacco', 'MT2 - 09 - Cotton', 'MT2 - 10 - Other agricultural products', 'MT2 - 11 - Fish and fish products',
                    'MT2 - 12 - Minerals and metals', 'MT2 - 13 - Petroleum', 'MT2 - 14 - Chemicals', 'MT2 - 15 - Wood, paper, etc', 'MT2 - 16 - Textiles',
                    'MT2 - 17 - Clothing', 'MT2 - 18 - Leather, footwear, etc', 'MT2 - 19 - Non-electrical machinery', 'MT2 - 20 - Electrical machinery', 
                    'MT2 - 21 - Transport equipment', 'MT2 - 22 - Manufactures n.e.s.'],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])

product_dic = {1:"Animal products", 2:"Dairy products", 3:"Fruits, vegetables, plants", 4:"Coffee, tea", 5:"Cereals and preparations", 6:"Oilseeds, fats and oils",
            7:"Sugars and confectionery", 8:"Beverages and tobacco", 9:"Cotton",10:"Other agricultural products", 11:"Fish and fish products", 12:"Minerals and metals",
            13:"Petroleum", 14:"Chemicals", 15:"Wood, paper, etc", 16:"Textiles", 17:"Clothing", 18:"Leather", 19:"Non-electrical machinery",
            20:"Electrical machinery", 21:"Transport equipment", 22:"Manufactures n.e.s.",}

country = sys.argv[1]

def main():

    if len(sys.argv) == 2:

        drop_product_df = new_df.drop(columns=['Product/Sector'])
        sum_country = drop_product_df.groupby('Partner Economy', as_index=False).sum()
        retrieval_country = sum_country[sum_country['Partner Economy'] == f'{country}']

        left = np.array([2015, 2016, 2017, 2018, 2019])
        y_array = np.array([retrieval_country['2015'], retrieval_country['2016'], retrieval_country['2017'], retrieval_country['2018'], retrieval_country['2019']])
        y_list = y_array.tolist()
        height = sum(y_list, [])


        plt.bar(left, height)
        plt.xlabel('Years')
        plt.ylabel('Bilateral imports (US$)')
        plt.title(country)
        plt.savefig('result.png')
        plt.show()

    else:
        product = sys.argv[2]

        retrieval_df = new_df[(new_df['Partner Economy'] == f'{country}') & (new_df['Product/Sector'] == int(product))]
        df_y = retrieval_df.drop(columns=['Partner Economy', 'Product/Sector'])

        left = np.array([2015, 2016, 2017, 2018, 2019])
        y_array = np.array([df_y['2015'], df_y['2016'], df_y['2017'], df_y['2018'], df_y['2019']])
        y_list = y_array.tolist()
        height = sum(y_list, [])


        plt.bar(left, height)
        plt.xlabel('Years')
        plt.ylabel('Bilateral imports (US$)')
        plt.title(f'{country}' + f' ({product_dic[int(product)]})')
        plt.savefig('result.png')
        plt.show()
        
if __name__ == "__main__":
    main()
from gimbel_scraper import get_product_info

if __name__ == "__main__":
    '''Example of use'''
    URL = "https://gimbelmexicana.com/gimbel/store/articulo/16680"
    data = get_product_info(URL)
    print(data)

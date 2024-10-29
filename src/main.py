from crawler import StockeExchangeCrawler
from spreadsheet import Spreadsheet
from bs4 import BeautifulSoup
import argparse


def extrat_table_from_html(html_doc: str):
    soup = BeautifulSoup(html_doc, 'html.parser')

    table = soup.select_one("#scr-res-table > div:nth-of-type(1) > table")
    for tr in table.find_all('tr'):
        td = tr.find_all('td')
        if td == []:
            continue

        yield td[0].get_text(), td[1].get_text(), td[2].get_text()


def main(region: str, browser: str):
    print('start process...')

    crawler = StockeExchangeCrawler(browser)
    print('opening site')
    crawler.open_stock_exchange_page()

    print('removing filters')
    crawler.remove_filters()

    print(f'adding filter by region {region}')
    crawler.filter_region(region)

    print('setting max result per page')
    crawler.get_max_results_per_page()

    sheet = Spreadsheet()
    page = 1
    while True:
        print(f'getting html of page {page}', end='\r')
        html_table = crawler.get_html()

        for simbol, name, price in extrat_table_from_html(html_doc=html_table):
            sheet.add_row(simbol, name, price)

        if not crawler.next_page():
            break

        page += 1

    print('saving results...')
    sheet.save(f'stock_exchange-{region}', 'xlsx')

    print('end process!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Get the region argument from the command line.")

    # Define the --region argument
    parser.add_argument("--region", type=str, help="Specify the region.")
    parser.add_argument("--browser", type=str, help="Specify the browser.")

    # Parse the arguments
    args = parser.parse_args()

    # Access the region argument
    region = args.region
    browser = args.browser

    main(region, browser)

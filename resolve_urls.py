import csv
import requests
import pandas as pd
import click
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

def resolve_url(url):
    
    if not url.startswith(('http://', 'https://')):
            return (url, None, None, 'malformed_url', None)

    try:
        response = requests.head(url, timeout=5)
        resolved_url = response.url
        protocol = "https" if response.url.startswith("https") else "http"
        status = response.status_code

        base_url = urlparse(url).netloc
        resolved_base_url = urlparse(resolved_url).netloc
        base_url_changed = base_url != resolved_base_url
    
        # Check if the only difference is the addition or removal of 'www.'
        if base_url_changed:
            base_url_changed = not (
                (base_url.startswith('www.') and base_url[4:] == resolved_base_url) or
                (resolved_base_url.startswith('www.') and resolved_base_url[4:] == base_url)
            )
    
        return (url, resolved_url, protocol, status, int(base_url_changed))

    except requests.exceptions.RequestException as e:
        return (url, None, None, str(e), None)

@click.command()
@click.option('input_file', '-i', required=True, type=click.File('r'), help="Path to the input file containing URLs.")
@click.option('output_file', '-o', required=True, type=click.File('w'), help="Path to the output file containing URLs.")
def main(input_file, output_file):
    urls = [line.strip() for line in input_file]

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(resolve_url, urls))

    df = pd.DataFrame(results, columns=['original_url', 'resolved_url', 'protocol', 'status', 'base_url_changed'])
    df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)

if __name__ == '__main__':
    main()

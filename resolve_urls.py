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
        response = requests.get(url, timeout=5, allow_redirects=True)
        resolved_url = response.url.rstrip('/')
        protocol = "https" if response.url.startswith("https") else "http"
        status = response.status_code

        base_url = urlparse(url).netloc.replace('www.', '')
        resolved_base_url = urlparse(resolved_url).netloc.replace('www.', '')
        base_url_changed = base_url != resolved_base_url
        base_url_changed = base_url != resolved_base_url
    
        base_url_changed = int(base_url_changed)
        return (url, resolved_url, protocol, status, int(base_url_changed))

    except requests.exceptions.RequestException as e:
        return (url, None, None, 'failed', 0)

@click.command()
@click.option('input_file', '-i', required=True, type=click.File('r'), help="Path to the input file containing URLs.")
@click.option('output_file', '-o', required=True, type=click.File('w'), help="Path to the output file containing URLs.")
def main(input_file, output_file):
    urls = [line.strip() for line in input_file]

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(resolve_url, urls))

    df = pd.DataFrame(results, columns=['original_url', 'resolved_url', 'protocol', 'status', 'base_url_changed'])
    
    # Explicitly cast 'base_url_changed' to integer
    df['base_url_changed'] = df['base_url_changed'].astype(int)
    
    df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)

if __name__ == '__main__':
    main()

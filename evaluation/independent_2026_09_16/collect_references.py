"""Archive public reference pages separately from the chatbot's unchanged corpus."""
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent

def fetch(item):
    key, url = item
    try:
        response = httpx.get(url, follow_redirects=True, timeout=45, trust_env=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        main = BeautifulSoup(response.text, 'html.parser')
        for node in main.select('script,style,nav,header,footer,noscript'):
            node.decompose()
        main = main.select_one('main') or main
        return key, {'url': url, 'resolved_url': str(response.url), 'status': response.status_code,
                     'checked_at': datetime.now(timezone.utc).isoformat(),
                     'sha256': hashlib.sha256(response.content).hexdigest(),
                     'title': soup.title.get_text(' ', strip=True) if soup.title else key,
                     'text': main.get_text('\n', strip=True),
                     'links': [{'text': a.get_text(' ', strip=True), 'href': a.get('href')} for a in soup.select('a[href]')],
                     'images': [{'alt': a.get('alt'), 'src': a.get('src')} for a in soup.select('img[src]')]}
    except Exception as exc:
        return key, {'url': url, 'error': str(exc)}

if __name__ == '__main__':
    urls = json.loads((HERE / 'reference_urls.json').read_text(encoding='utf-8'))
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = dict(pool.map(fetch, urls.items()))
    (HERE / 'references.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    for key, result in results.items():
        print(key, result.get('status', result.get('error')), len(result.get('text', '')), flush=True)

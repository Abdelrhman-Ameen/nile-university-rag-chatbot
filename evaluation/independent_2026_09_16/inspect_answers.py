"""Read complete answers and returned evidence for manual AI review; no scoring."""
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('start', type=int)
p.add_argument('end', type=int)
p.add_argument('--all-evidence', action='store_true')
args = p.parse_args()
here = Path(__file__).resolve().parent
suite = {c['id']:c for c in json.loads((here/'suite.json').read_text(encoding='utf-8'))}
for line in (here/'responses.jsonl').read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    if not args.start <= int(row['id'][1:]) <= args.end: continue
    case = suite[row['id']]
    result = row.get('result',{})
    print('\n###',row['id'],row['status'],row['seconds'],case['question'])
    print('EXPECT:',case['expectation'])
    print('ANSWER:',result.get('answer',result or row.get('error')))
    print('ROUTE:',result.get('pipeline',{}).get('route'))
    for source in result.get('sources',[]):
        print('SOURCE',source['citation'],source.get('cited'),source['url'],source.get('asset_url',''))
        text = source.get('context',source.get('text',''))
        print(text if args.all_evidence or source.get('cited') else text[:300]+' [...]')

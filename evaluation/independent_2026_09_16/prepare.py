"""Build and audit this challenge set before observing any chatbot responses."""
import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def normalize(text):
    return re.sub(r'[^\w]+', ' ', unicodedata.normalize('NFKC', text).lower()).strip()

if __name__ == '__main__':
    assert not (HERE / 'freeze.json').exists(), 'Already frozen; do not rewrite suite.'
    cases = list(csv.DictReader((HERE / 'cases.tsv').open(encoding='utf-8'), delimiter='\t'))
    contexts = json.loads((HERE / 'contexts.json').read_text(encoding='utf-8'))
    for case in cases:
        case['references'] = case['references'].split(',') if case['references'] else []
        case['history'] = contexts.get(case['id'], [])
    assert len(cases) == 100 and len({normalize(c['question']) for c in cases}) == 100
    old = {}
    def add(q, p):
        if isinstance(q, str) and q.strip() and len(q) < 1500 and not q.lstrip().startswith('{'):
            old.setdefault(q, set()).add(str(p.relative_to(ROOT)).replace('\\','/'))
    def walk(x, p):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in {'question','utterance','query'}: add(v, p)
                if k == 'role' and v == 'user': add(x.get('content'), p)
                walk(v, p)
        elif isinstance(x, list):
            for v in x: walk(v, p)
    paths = list((ROOT / 'evaluation').rglob('*.json')) + list((ROOT / 'data').glob('*.json'))
    scanned = []
    for p in paths:
        if HERE in p.parents: continue
        try: obj = json.loads(p.read_text(encoding='utf-8'))
        except (ValueError, UnicodeError): continue
        scanned.append({'path': str(p.relative_to(ROOT)).replace('\\','/'), 'sha256': digest(p)})
        if p.name == 'intent_examples.json':
            for groups in obj.values():
                if isinstance(groups, dict):
                    for examples in groups.values():
                        if isinstance(examples, list):
                            for q in examples: add(q, p)
        else: walk(obj, p)
    prior = [{'question': q, 'files': sorted(fs)} for q, fs in sorted(old.items())]
    texts = [r['question'] for r in prior] + [c['question'] for c in cases]
    vectors = TfidfVectorizer(analyzer='char_wb', ngram_range=(3,5)).fit_transform(texts)
    scores = cosine_similarity(vectors[len(prior):], vectors[:len(prior)])
    audit = []
    for case, sim in zip(cases, scores):
        best = sim.argsort()[-3:][::-1]
        exact = normalize(case['question']) in {normalize(r['question']) for r in prior}
        assert not exact, case['id']
        audit.append({'id':case['id'], 'exact_match':exact, 'nearest_old':[
            {**prior[i], 'character_similarity': round(float(sim[i]),4)} for i in best],
            'manual_novelty_review': 'Distinct fact target or decision; broad domain overlap is allowed. See expectation.'})
    for name, obj in [('suite.json', cases), ('prior_questions.json', prior),
                      ('novelty.json', {'method':'Character TF-IDF triage plus semantic review; scores are not semantic proof.',
                                        'scanned_files': scanned, 'prior_unique_questions':len(prior), 'cases':audit})]:
        (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
    print('100 cases;', len(prior), 'prior questions; no normalized exact duplicates')
    for a in sorted(audit, key=lambda a:a['nearest_old'][0]['character_similarity'], reverse=True)[:15]:
        print(a['id'], a['nearest_old'][0]['character_similarity'], a['nearest_old'][0]['question'])

"""Aggregate the independently read, explicitly recorded per-case reviews."""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

def outcome(row):
    if 0 in [int(row[k]) for k in ['correctness','completeness','grounding']]: return 'fail'
    if all(int(row[k]) == 2 for k in ['correctness','completeness','grounding']) and row['language']=='1' and row['links'] in {'1','N/A'}: return 'pass'
    return 'partial'

def load(name):
    return json.loads((HERE/name).read_text(encoding='utf-8'))

def table(rows):
    keys = list(rows[0])
    return '\n'.join(['| '+' | '.join(keys)+' |','| '+' | '.join(['---']*len(keys))+' |']+
                     ['| '+' | '.join(str(row[k]).replace('|','/').replace('\n',' ') for k in keys)+' |' for row in rows])

if __name__ == '__main__':
    suite = {c['id']:c for c in load('suite.json')}
    responses = {r['id']:r for r in [json.loads(s) for s in (HERE/'responses.jsonl').read_text(encoding='utf-8').splitlines()]}
    reviews = list(csv.DictReader((HERE/'review.tsv').open(encoding='utf-8'),delimiter='\t'))
    assert len(reviews)==100 and len({r['id'] for r in reviews})==100
    assert set(suite)==set(responses)=={r['id'] for r in reviews}
    frozen, done = load('freeze.json'), load('completion.json')
    for filename, digest in frozen['hashes'].items():
        if filename.startswith('evaluation/independent_2026_09_16/'):
            assert hashlib.sha256((HERE/Path(filename).name).read_bytes()).hexdigest()==digest, filename
    assert hashlib.sha256((HERE/'responses.jsonl').read_bytes()).hexdigest()==done['responses_sha256']
    assert done['hashes_unchanged']
    for r in reviews:
        r.update(outcome=outcome(r),category=suite[r['id']]['category'],input_language=suite[r['id']]['language'])
    counts = Counter(r['outcome'] for r in reviews)
    http = Counter(str(r['status']) for r in responses.values())
    latency = np.array([r['seconds'] for r in responses.values()])
    breakdown = {}
    for field in ['category','input_language']:
        grouped = defaultdict(Counter)
        for r in reviews: grouped[r[field]][r['outcome']]+=1
        breakdown[field]=[{field:k,'pass':v['pass'],'partial':v['partial'],'fail':v['fail'],'total':sum(v.values())} for k,v in grouped.items()]
    stats = {'reviewed_at':datetime.now(timezone.utc).isoformat(), 'reviewer':'AI agent, not recruited human reviewers',
             'total':100,'outcomes':dict(counts),'http':dict(http),
             'latency_seconds':{'median':round(float(np.median(latency)),3),'p95':round(float(np.percentile(latency,95)),3),'max':round(float(latency.max()),3)},
             'breakdown':breakdown,'failure_types':dict(Counter(r['failure_type'] for r in reviews if r['outcome']!='pass')),
             'code_version':frozen['health']['code_version'],'app_commit':frozen['git_commit'],
             'run_started':frozen['frozen_at'],'run_finished':done['finished_at'],'frozen_assets_unchanged':True}
    (HERE/'summary.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
    (HERE/'review.json').write_text(json.dumps(reviews,ensure_ascii=False,indent=2),encoding='utf-8')
    sections = ['# All 100 answers and their reviews','AI-reviewed human-style challenge set. Scores and references were defined before execution. Every case is included, including failures. Full returned source passages and pipeline diagnostics are in `responses.jsonl`.']
    for r in reviews:
        c,x=suite[r['id']],responses[r['id']]
        sections += [f"## {r['id']} — {r['outcome'].upper()}", f"**Question ({c['language']}):** {c['question']}"]
        if c['history']: sections += ['**Authored history fixture:**\n\n'+'\n\n'.join(f"{h['role']}: {h['content']}" for h in c['history'])]
        sections += [f"**Expected:** {c['expectation']}",f"**HTTP:** {x['status']} · **Latency:** {x['seconds']} seconds",'**Answer:**\n\n'+x.get('result',{}).get('answer',str(x.get('result',x.get('error')))),
                     f"**Review:** {r['note']}",f"**Scores:** correctness {r['correctness']}/2; completeness {r['completeness']}/2; grounding {r['grounding']}/2; language {r['language']}/1; links {r['links']}. Evidence: {r['evidence']}."]
        cited = [s for s in x.get('result',{}).get('sources',[]) if s.get('cited')]
        if cited: sections += ['**Returned citations:**\n\n'+'\n'.join(f"- [{s['citation']}] [{s['title']}]({s['url']})" for s in cited)]
        urls = load('reference_urls.json')
        if c['references']: sections += ['**Reference:** '+', '.join(f'[{k}]({urls[k]})' for k in c['references'])]
    # Presentation-only whitespace cleanup; the raw response bytes are untouched.
    rendered = '\n'.join(line.rstrip() for line in '\n\n'.join(sections).splitlines())+'\n'
    (HERE/'ANSWERS.md').write_text(rendered,encoding='utf-8',newline='\n')
    report = f"""# Independent human-style query evaluation — 100 new queries

**{counts['pass']} pass · {counts['partial']} partial · {counts['fail']} fail.** These are AI-reviewed answers, not a human-reviewed benchmark or a production certification.

All 100 frozen target queries were submitted once through the actual local FastAPI chat endpoint. No chatbot code, prompt, model, corpus or index was changed during the run, and failed cases were not retried. Six requests used prewritten history fixtures; the other 94 began with empty history. The set was checked against {load('novelty.json')['prior_unique_questions']} distinct prior prompts, with no normalized exact matches, and reviewed for distinct fact targets. Topic families overlap; these are new decisions and facets rather than paraphrases of the old 100 scenarios.

The frozen app was commit `{frozen['git_commit'][:7]}`, code version `{frozen['health']['code_version']}`, using local `{frozen['health']['model']}` with CUDA retrieval, {frozen['health']['chunks']:,} chunks and {frozen['health']['sources']:,} source URLs. The run used port 8001 because an unrelated app occupied 8000. The reference snapshot was fetched independently from official NU Egypt sites and was not fed into the chatbot.

## Answer quality

{table(breakdown['category'])}

{table(breakdown['input_language'])}

Each response was read against the predeclared expectation, fresh reference snapshot and returned passages. Pass requires a correct, complete, grounded answer in the appropriate language with required links. Partial indicates a limited but nonfatal issue; fail includes material factual/grounding errors, unanswered answerable questions and HTTP failures. This is stricter than the previous keyword regression checks; the two pass rates are not directly comparable.

## Reliability and latency

HTTP outcomes: `{dict(http)}`. Sequential end-to-end latency across all 100 requests: median **{stats['latency_seconds']['median']:.2f}s**, p95 **{stats['latency_seconds']['p95']:.2f}s**, maximum **{stats['latency_seconds']['max']:.2f}s**. These measurements include planning, retrieval, generation and answer verification on a warmed local service. They do not measure browser rendering, SSE reconnects, concurrency or time to first token. HTTP 200 does not establish answer correctness.

Run: {stats['run_started']} through {stats['run_finished']}. Frozen-asset hashes matched at completion.

## Reproducibility and limitations

- [Failure examples and repair priorities](FINDINGS.md), including the scope of the post-response scientific-claim check.
- [Protocol](PROTOCOL.md), [100 frozen cases](suite.json), [novelty audit](novelty.json), [prior prompt inventory](prior_questions.json).
- [Every answer with its review](ANSWERS.md), [structured review](review.json), [raw HTTP responses and evidence](responses.jsonl).
- [Reference snapshots](references.json), [visually checked transport image facts](image_reference.json), [freeze manifest](freeze.json), [completion hashes](completion.json).

The author/reviewer is the same AI agent with implementation context, not an independent human panel. References and criteria were frozen before responses, but query selection was informed partly by available university pages; this is not a blinded population study. Source-page ambiguity, missing live inventories and unknown real-world service status remain limitations. Repeated broad subjects within the set test different facets; six contextual cases intentionally revisit a fact to test continuity. No claims about all university endpoints or production readiness follow from these 100 results.
"""
    (HERE/'REPORT.md').write_text(report,encoding='utf-8')
    print(json.dumps(stats,ensure_ascii=False,indent=2))

"""Freeze once, then issue each of the 100 target requests once. Never grade here."""
import argparse
import hashlib
import importlib.metadata
import json
import os
import subprocess
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def now():
    return datetime.now(timezone.utc).isoformat()

def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def hashes():
    paths = list((ROOT/'nu_chat').rglob('*.py')) + list((ROOT/'static').glob('*'))
    paths += [ROOT/'data'/n for n in ['documents.jsonl','ocr_documents.jsonl','index.npz','intent_classifier.npz']]
    paths += [HERE/n for n in ['suite.json','cases.tsv','contexts.json','references.json','reference_urls.json',
                               'image_reference.json','PROTOCOL.md','novelty.json','prior_questions.json','run.py','prepare.py']]
    return {str(p.relative_to(ROOT)).replace('\\','/'): digest(p) for p in paths if p.is_file()}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://127.0.0.1:8001')
    args = parser.parse_args()
    output = HERE/'responses.jsonl'
    assert not output.exists() and not (HERE/'freeze.json').exists(), 'Preserve first run; no rerun/overwrite.'
    suite = json.loads((HERE/'suite.json').read_text(encoding='utf-8'))
    assert len(suite) == 100
    with httpx.Client(timeout=360, trust_env=False) as client:
        health = client.get(args.url+'/api/health', timeout=15).json()
        assert health.get('ready') and health.get('model_ready') and health.get('index_ready'), health
        assert not health['queue']['active'] and not health['queue']['waiting'], health
        manifest = {'frozen_at':now(), 'base_url':args.url, 'git_commit':subprocess.check_output(
                    ['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(), 'health':health,
                    'ollama':client.get('http://127.0.0.1:11434/api/ps').json(), 'hashes':hashes(),
                    'python':subprocess.check_output([os.sys.executable,'--version'],text=True).strip(),
                    'dependencies':{n:importlib.metadata.version(n) for n in ['fastapi','uvicorn','httpx','torch','sentence-transformers']}}
        (HERE/'freeze.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
        print('FROZEN',manifest['frozen_at'],manifest['health']['code_version'],flush=True)
        with output.open('x',encoding='utf-8') as f:
            for case in suite:
                request_id = str(uuid.uuid4())
                body = {'question':case['question'],'history':case['history'],'language':'auto','request_id':request_id}
                started = time.perf_counter()
                row = {'id':case['id'], 'started_at':now(),'request':body}
                try:
                    response = client.post(args.url+'/api/chat',json=body)
                    row.update(status=response.status_code, result=response.json())
                except Exception as exc:
                    row.update(status=None,error=repr(exc))
                row.update(seconds=round(time.perf_counter()-started,3),finished_at=now())
                f.write(json.dumps(row,ensure_ascii=False)+'\n'); f.flush(); os.fsync(f.fileno())
                print(case['id'],row['status'],row['seconds'],flush=True)
        end_hashes = hashes()
        end = {'finished_at':now(),'health':client.get(args.url+'/api/health',timeout=15).json(),
               'hashes_unchanged':end_hashes == manifest['hashes'], 'end_hashes':end_hashes,
               'responses_sha256':digest(output)}
        (HERE/'completion.json').write_text(json.dumps(end,indent=2),encoding='utf-8')
        print('COMPLETE; unchanged=',end['hashes_unchanged'],flush=True)

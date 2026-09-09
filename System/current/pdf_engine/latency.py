from __future__ import annotations
import hashlib, json, subprocess, sys, time
from pathlib import Path
from .common import safe_artifact_path, sha256_file, write_json
from .state import primary_state

CACHE_DIR = '.runtime_cache'


def cache_dir(root: Path) -> Path:
    d = root / CACHE_DIR
    d.mkdir(exist_ok=True)
    return d


def semantic_primary_state(root: Path, state: dict) -> dict[str, str]:
    full = primary_state(root, state)
    return {k:v for k,v in full.items() if not k.lower().endswith('.pdf')}


def _load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return default

def run_generators_incremental(root: Path, state: dict, force: bool=False) -> dict:
    cache_path = cache_dir(root) / 'build_cache.json'
    cache = _load_json(cache_path, {})
    ran, skipped = [], []
    seen = set()
    for a in state.get('artifacts', []):
        gen = a.get('generator')
        if a.get('classification') != 'REQUIRED' or not gen or gen in seen:
            continue
        seen.add(gen)
        script = safe_artifact_path(root, gen)
        output = safe_artifact_path(root, a['path'])
        if not script.exists():
            raise RuntimeError(f'BLOCK: missing generator {gen}')
        dep_hash = sha256_file(script)
        key = f'{gen}->{a["path"]}'
        if not force and output.exists() and cache.get(key) == dep_hash:
            skipped.append(a['path'])
            continue
        subprocess.run([sys.executable, str(script)], check=True, cwd=str(root), stdout=subprocess.DEVNULL)
        cache[key] = dep_hash
        ran.append(a['path'])
    write_json(cache_path, cache)
    return {'ran': ran, 'skipped': skipped}

def refresh_context_files(root: Path, pdf_state: dict, runtime_cfg: dict, runtime_state: dict) -> None:
    policy = runtime_cfg.get('latency_policy', {})
    topics = policy.get('context_topics', {})
    index = {'version': runtime_cfg.get('release_version'), 'topics': topics}
    write_json(root / 'context_index.json', index)
    graph = {'version': runtime_cfg.get('release_version'), 'topics': {}}
    for name, spec in topics.items():
        graph['topics'][name] = {
            'files': spec.get('files', []),
            'tests': spec.get('tests', []),
            'artifacts': spec.get('artifacts', []),
            'depends_on': spec.get('depends_on', [])
        }
    write_json(root / 'dependency_graph.json', graph)
    trace = _load_json(root / 'mutation_trace.json', {})
    active = {
        'system_version': pdf_state.get('release', {}).get('version'),
        'runtime_version': runtime_cfg.get('runtime_version'),
        'current_profile': runtime_state.get('current_profile'),
        'active_directive': runtime_state.get('directive_id'),
        'phase': runtime_state.get('phase'),
        'last_mutation_target': trace.get('target_improvement'),
        'blockers': [],
        'context_tiers': policy.get('context_tiers', {}),
        'front_door': 'WORKSPACE.json'
    }
    write_json(root / 'active_context.json', active)

def record_latency(root: Path, metrics: dict) -> None:
    p = cache_dir(root) / 'latency_metrics.jsonl'
    metrics = dict(metrics)
    metrics['timestamp_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    with p.open('a', encoding='utf-8') as f:
        f.write(json.dumps(metrics, separators=(',', ':')) + '\n')


def recent_latency(root: Path, limit: int=20) -> list[dict]:
    p = cache_dir(root) / 'latency_metrics.jsonl'
    if not p.exists(): return []
    rows = []
    for line in p.read_text(encoding='utf-8').splitlines()[-limit:]:
        try: rows.append(json.loads(line))
        except Exception: pass
    return rows


def compact_topic_context(root: Path, topic: str) -> dict:
    idx = _load_json(root / 'context_index.json', {'topics': {}})
    active = _load_json(root / 'active_context.json', {})
    spec = idx.get('topics', {}).get(topic)
    if spec is None:
        raise KeyError(f'Unknown context topic: {topic}')
    return {'active_context': active, 'topic': topic, 'scope': spec}

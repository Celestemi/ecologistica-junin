"""Read-only source checks; writes only the three declared evidence manifests.

Video material is excluded before reading. Does not certify the whole machine,
dependency folders, .git internals or external deployments.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'AUDITORIA/CORRECCIONES_EVIDENCIAS'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8').strip('\n')


def included(name):
    return not (name.startswith('docs/05 Video proyecto/') or 'GUION_VIDEO' in name)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    baseline = json.loads((OUT / 'historicos-baseline.json').read_text(encoding='utf-8'))
    integrity = {}
    for group, rows in baseline.items():
        checked = [{**row, 'actual_sha256': sha(ROOT / row['path'])} for row in rows]
        integrity[group] = {'count': len(rows), 'unchanged': sum(r['sha256'] == r['actual_sha256'] for r in checked),
                            'mismatches': [r for r in checked if r['sha256'] != r['actual_sha256']]}
    integrity['head'] = git('rev-parse', 'HEAD')
    integrity['branch'] = git('branch', '--show-current')
    integrity['limits'] = 'Only listed historical files, original audits and residual. Excludes video/dependencies/.git/external environment.'
    save('integridad-final.json', integrity)
    names = [n for n in git('ls-files', '--cached', '--others', '--exclude-standard', '-z').split('\0') if n and included(n)]
    links, broken = [], []
    for name in names:
        if name != 'README.md' and not (name.startswith('docs/') and name.endswith('.md')):
            continue
        path = ROOT / name
        for raw in re.findall(r'!?\[[^\]]*\]\((<[^>]*>|[^)]+)\)', path.read_text(encoding='utf-8-sig')):
            value = unquote(raw.strip('<>').split('#')[0])
            if not value or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', value):
                continue
            dest = (path.parent / value).resolve()
            try:
                rel = dest.relative_to(ROOT).as_posix()
            except ValueError:
                rel = str(dest)
            if not included(rel):
                continue
            row = {'source': name, 'target': rel, 'exists': dest.exists()}
            links.append(row)
            if not row['exists']:
                broken.append(row)
    save('links-final.json', {'scope': 'README + Markdown docs, video excluded; occurrences including repeats',
        'checked': len(links), 'broken': broken, 'missing_destinations': sorted({r['target'] for r in broken})})
    modified = [n for n in git('diff', '--name-only', '-z').split('\0') if n and included(n)]
    new = [n for n in git('ls-files', '--others', '--exclude-standard', '-z').split('\0') if n and included(n)]
    preexisting = {r['path'] for r in baseline['protected_files']} | {'CODEX_PLAN_CORRECCIONES_POST_AUDITORIA.md'}
    outputs = {'AUDITORIA/CORRECCIONES_EVIDENCIAS/' + n for n in ['manifest-final.json', 'integridad-final.json', 'links-final.json']}
    manifest = {'head': integrity['head'], 'branch': integrity['branch'], 'working_tree': 'uncommitted authorized corrections',
        'modified_tracked': [{'path': n, 'sha256': sha(ROOT / n)} for n in sorted(modified)],
        'created_this_task': [{'path': n, 'sha256': sha(ROOT / n)} for n in sorted(set(new) - preexisting - outputs)],
        'preexisting_untracked_preserved': sorted(set(new) & preexisting),
        'ignored_runtime': 'AUDITORIA/CORRECCIONES_EVIDENCIAS/runtime/; dependency caches excluded from this inventory',
        'preexisting_ignored_residual': '.vitest/json/output.json (hash in integridad-final.json)',
        'excluded_self_updating_outputs': sorted(outputs), 'video': 'excluded before reading'}
    save('manifest-final.json', manifest)
    print(json.dumps({'integrity': integrity, 'links_checked': len(links), 'broken_occurrences': len(broken),
        'missing_destinations': len({r['target'] for r in broken}), 'modified_tracked': len(modified),
        'created_files': len(manifest['created_this_task'])}, ensure_ascii=True))
    return 1 if any(integrity[group]['mismatches'] for group in baseline) else 0


if __name__ == '__main__':
    raise SystemExit(main())

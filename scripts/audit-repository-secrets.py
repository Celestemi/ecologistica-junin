"""AF-29: escaneo local acotado de patrones, jamás imprime valores coincidentes.

No certifica ausencia absoluta ni revisa credenciales del despliegue externo.
"""

import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
RULES = {
    'private-key': re.compile(rb'^-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', re.M),
    'aws-access-key': re.compile(rb'\bAKIA[0-9A-Z]{16}\b'),
    'github-token': re.compile(rb'\bgh[pousr]_[A-Za-z0-9]{36,}\b'),
    'stripe-live': re.compile(rb'\bsk_live_[A-Za-z0-9]{20,}\b'),
    'slack-token': re.compile(rb'\bxox[baprs]-[A-Za-z0-9-]{20,}\b'),
}
TEXT_SUFFIXES = {'.py','.ts','.tsx','.js','.mjs','.json','.md','.txt','.toml','.yml','.yaml','.sql','.ps1','.sh','.conf','.example','.ini'}


def applicable(name):
    if name.startswith('docs/05 Video proyecto/') or 'GUION_VIDEO' in name:
        return False
    path = Path(name)
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in {'.gitignore','Dockerfile','.env'}


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)


def main():
    findings, checked, skipped = [], 0, 0
    objects = {}
    for line in git('-c','core.quotepath=false','rev-list','--objects','--all').decode('utf-8').splitlines():
        identifier, _, name = line.partition(' ')
        if name and applicable(name):
            objects.setdefault(identifier,name)
    batch = subprocess.run(['git','cat-file','--batch'],cwd=ROOT,
        input=''.join(key+'\n' for key in objects).encode(),stdout=subprocess.PIPE,check=True).stdout
    offset = 0
    for identifier, name in objects.items():
        end = batch.index(b'\n',offset)
        header = batch[offset:end].split()
        length = int(header[2]); data = batch[end+1:end+1+length]; offset=end+length+2
        if header[1] != b'blob' or length > 4_000_000:
            skipped += 1; continue
        checked += 1
        for rule, pattern in RULES.items():
            if pattern.search(data): findings.append({'path':name,'blob':identifier,'rule':rule})
    working = 0
    for name in git('ls-files','--cached','--others','--exclude-standard','-z').decode('utf-8').split('\0'):
        if not name or not applicable(name): continue
        path = ROOT/name
        if not path.is_file() or path.stat().st_size > 4_000_000: continue
        working += 1; data=path.read_bytes()
        for rule, pattern in RULES.items():
            if pattern.search(data): findings.append({'path':name,'revision':'working-tree','rule':rule})
    report = {'head':git('rev-parse','HEAD').decode().strip(),'historical_blobs_checked':checked,
        'working_files_checked':working,'large_or_non_blob_skipped':skipped,'findings':findings,
        'limits':'Pattern scan only, not entropy/full credential validation. Deployment and private local environment not certified. No matching values reported.'}
    destination=ROOT/'AUDITORIA/CORRECCIONES_EVIDENCIAS/secret-scan.json'
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True))
    return 1 if findings else 0


if __name__ == '__main__':
    raise SystemExit(main())

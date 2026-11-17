"""SCA de dependencias Python instaladas usando API pública OSV, sin instalar.

Solo transmite nombres/versiones públicos de dependencias declaradas/transitivas;
nunca código, .env, tokens, rutas o credenciales. No detecta exposición efectiva.
"""

from datetime import datetime, timezone
from importlib import metadata
import json
from pathlib import Path
import tomllib
from urllib.request import Request, urlopen

from packaging.requirements import Requirement


def main():
    config=tomllib.loads(Path('pyproject.toml').read_text(encoding='utf-8'))['project']
    queue=[Requirement(value) for value in config['dependencies']+config.get('optional-dependencies',{}).get('dev',[])]
    visited=set(); packages={}; missing=[]
    while queue:
        requirement=queue.pop(); key=(requirement.name.lower(),tuple(sorted(requirement.extras)))
        if key in visited: continue
        visited.add(key)
        try: packages[requirement.name]=metadata.version(requirement.name)
        except metadata.PackageNotFoundError:
            missing.append(requirement.name); continue
        for value in metadata.requires(requirement.name) or []:
            child=Requirement(value)
            if child.marker is None or any(child.marker.evaluate({'extra':extra}) for extra in (requirement.extras or {''})):
                queue.append(child)
    queries=[{'package':{'ecosystem':'PyPI','name':name},'version':version} for name,version in sorted(packages.items())]
    result={'date':datetime.now(timezone.utc).isoformat(),'source':'https://api.osv.dev/v1/querybatch',
        'scope':'Installed declared Python runtime/dev dependencies and their active transitive requirements; no application exploit analysis',
        'packages':queries,'missing_dependencies':missing}
    try:
        request=Request(result['source'],data=json.dumps({'queries':queries}).encode(),
            headers={'Content-Type':'application/json','User-Agent':'local-security-audit'})
        with urlopen(request,timeout=30) as response: data=json.load(response)
        result['status']='EXECUTED'
        result['findings']=[{'package':query['package']['name'],'version':query['version'],
            'advisories':[v['id'] for v in answer.get('vulns',[])]} for query,answer in zip(queries,data['results']) if answer.get('vulns')]
    except Exception as exc:
        result['status']='NOT_VERIFIED'; result['error_type']=type(exc).__name__
    target=Path('AUDITORIA/CORRECCIONES_EVIDENCIAS/python-osv.json')
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({key:result.get(key) for key in ['date','status','findings','error_type','missing_dependencies']}))
    return 0 if result['status']=='EXECUTED' and not result['findings'] and not missing else 1


if __name__=='__main__': raise SystemExit(main())

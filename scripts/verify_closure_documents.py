"""Contraste reproducible de estructura HTML/nombres/retornos, NO de aceptación."""

import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote


class Text(HTMLParser):
    def __init__(self): super().__init__();self.lines=[]
    def handle_data(self,value):
        if value.strip(): self.lines.append(value.strip())


def norm(value):
    return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',value.casefold()).encode('ascii','ignore').decode()).strip()


def links(text): return [unquote(value.strip('<>').split('#')[0]) for value in re.findall(r'!?\[[^\]]*\]\((<[^>]*>|[^)]+)\)',text)]


def main():
    source=Path(sys.argv[1]); parser=Text();parser.feed(source.read_text(encoding='utf-8'))
    lines=parser.lines; root=Path.cwd(); readme=(root/'README.md').read_text(encoding='utf-8')
    sections=[next(index for index,line in enumerate(lines) if line.startswith(f'5.{n} Archivo:')) for n in range(1,8)]+[len(lines)]
    rows=[]
    for index in range(7):
        part=lines[sections[index]:sections[index+1]]
        filename=next(line for line in part if 'docs/04 Cierre/' in line and '.md' in line).split('docs/04 Cierre/',1)[1].split('.md',1)[0]+'.md'
        path=root/'docs/04 Cierre'/filename
        text=path.read_text(encoding='utf-8') if path.is_file() else ''
        normalized=norm(text); fields=[]
        for line in part:
            if line.startswith(f'5.{index+1} Archivo:') or '[ ? ]' in line or 'docs/04 Cierre/' in line or 'Volver al README' in line or '../../README' in line or line in {'(',')','Imagen'}:continue
            value=norm(line)
            if value and value not in fields: fields.append(value)
        missing=[field for field in fields if field not in normalized]
        outgoing=any((root/value).resolve()==path.resolve() for value in links(readme) if value and '://' not in value)
        returning=any((path.parent/value).resolve()==(root/'README.md').resolve() for value in links(text) if value and '://' not in value)
        rows.append({'file':filename,'exists':path.is_file(),'checked_fields':len(fields),'missing_fields':missing,
            'markers':len(re.findall(r'\[\s*\?\s*\]',text)), 'readme_to_document':outgoing,'document_to_readme':returning,
            'version_1_0_0':'1.0.0' in text,'revision_history':'Historial de revisiones' in text})
    report={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'documents':rows,
        'limits':'Structural presence only. Missing real values/graphs/acceptance remain evaluated separately.'}
    target=root/'AUDITORIA/CORRECCIONES_EVIDENCIAS/closure-validation.json'
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True))
    return 0 if all(row['exists'] and not row['missing_fields'] and not row['markers'] and row['readme_to_document'] and row['document_to_readme'] for row in rows) else 1


if __name__=='__main__':raise SystemExit(main())

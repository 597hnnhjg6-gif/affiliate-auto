"""Validate affiliate offer records before publishing."""
import csv
import datetime as dt
import pathlib
import re
from urllib.parse import urlsplit
import ipaddress

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED = ('id', 'name', 'category', 'description', 'benefits', 'cautions', 'price_note', 'affiliate_url', 'official_url', 'verified_at', 'enabled')

def check():
    errors, warnings, ids, affiliate_urls = [], [], set(), set()
    with (ROOT / 'data/offers.csv').open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        missing = set(REQUIRED) - set(reader.fieldnames or [])
        if missing:
            return [f'Missing CSV columns: {sorted(missing)}'], []
        for n, r in enumerate(reader, 2):
            if r['enabled'].strip().lower() not in ('true', 'false'):
                errors.append(f'Row {n}: enabled must be true/false')
            key = (r.get('id') or '').strip()
            if key in ids:
                errors.append(f'Row {n}: duplicate id')
            ids.add(key)
            if r['enabled'].strip().lower() != 'true':
                continue
            key = r['id'].strip()
            if key == 'sample' or any('ここに' in (r.get(field) or '') for field in ('description','benefits','cautions','price_note')):
                errors.append(f'Row {n}: placeholder content cannot be published')
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', key):
                errors.append(f'Row {n}: invalid id')
            for field in REQUIRED:
                if field != 'enabled' and not (r.get(field) or '').strip():
                    errors.append(f'Row {n}: missing {field}')
            if len((r.get('description') or '').strip()) < 30:
                warnings.append(f'Row {n}: description is short; verify usefulness and accuracy')
            if (r.get('affiliate_url') or '').strip() == (r.get('official_url') or '').strip():
                warnings.append(f'Row {n}: affiliate and official URLs are identical; confirm tracking')
            aff = (r.get('affiliate_url') or '').strip()
            if aff in affiliate_urls:
                warnings.append(f'Row {n}: affiliate URL is duplicated')
            affiliate_urls.add(aff)
            for field in ('affiliate_url', 'official_url'):
                url = (r.get(field) or '').strip()
                try:
                    parts = urlsplit(url)
                except ValueError:
                    errors.append(f'Row {n}: {field} has an invalid URL')
                    continue
                try:
                    valid_port = parts.port in (None, 443)
                except ValueError:
                    valid_port = False
                if parts.scheme != 'https' or not parts.hostname or parts.username or parts.password or not valid_port:
                    errors.append(f'Row {n}: {field} must be a valid HTTPS URL')
                if parts.hostname:
                    host = parts.hostname.lower().rstrip('.')
                    try:
                        ipaddress.ip_address(host)
                        errors.append(f'Row {n}: {field} cannot use an IP address')
                    except ValueError:
                        if host == 'localhost' or '.' not in host or host.endswith(('.local', '.internal', '.test', '.invalid', '.example')):
                            errors.append(f'Row {n}: {field} must use a public hostname')
            try:
                verified = dt.date.fromisoformat((r.get('verified_at') or '').strip())
                age = (dt.date.today() - verified).days
                if age > 90:
                    warnings.append(f'Row {n}: information last verified {age} days ago')
                if age < 0:
                    errors.append(f'Row {n}: verification date is in the future')
            except ValueError:
                errors.append(f'Row {n}: invalid verified_at (YYYY-MM-DD)')
    return errors, warnings

if __name__ == '__main__':
    errors, warnings = check()
    for message in warnings: print('WARNING:', message)
    for message in errors: print('ERROR:', message)
    print(f'Validation: {len(errors)} errors, {len(warnings)} warnings')
    raise SystemExit(bool(errors))

"""Validate affiliate offer records before publishing."""
import csv
import datetime as dt
import pathlib
import re
from urllib.parse import urlsplit

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED = ('id', 'name', 'category', 'description', 'benefits', 'cautions', 'price_note', 'affiliate_url', 'official_url', 'verified_at', 'enabled')

def check():
    errors, warnings, ids = [], [], set()
    with (ROOT / 'data/offers.csv').open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        missing = set(REQUIRED) - set(reader.fieldnames or [])
        if missing:
            return [f'Missing CSV columns: {sorted(missing)}'], []
        for n, r in enumerate(reader, 2):
            if r['enabled'].strip().lower() not in ('true', 'false'):
                errors.append(f'Row {n}: enabled must be true/false')
            if r['enabled'].strip().lower() != 'true':
                continue
            key = r['id'].strip()
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', key):
                errors.append(f'Row {n}: invalid id')
            if key in ids:
                errors.append(f'Row {n}: duplicate id')
            ids.add(key)
            for field in REQUIRED:
                if field != 'enabled' and not (r.get(field) or '').strip():
                    errors.append(f'Row {n}: missing {field}')
            for field in ('affiliate_url', 'official_url'):
                url = (r.get(field) or '').strip()
                parts = urlsplit(url)
                if parts.scheme != 'https' or not parts.hostname or parts.username or parts.password:
                    errors.append(f'Row {n}: {field} must be a valid HTTPS URL')
            try:
                verified = dt.date.fromisoformat(r['verified_at'].strip())
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

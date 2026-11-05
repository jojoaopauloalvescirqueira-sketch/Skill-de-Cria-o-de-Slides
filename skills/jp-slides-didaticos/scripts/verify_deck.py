#!/usr/bin/env python3
"""Conservative OOXML structural checks, stdlib only. Exit 0 PASS / 2 FAIL.

Receipt hashes bind checks to bytes; they are not a signature or tamper proof.
No visual, semantic, pedagogical, accessibility or clinical efficacy claim.
"""
import argparse
import hashlib
import io
import json
import posixpath
from pathlib import Path
import struct
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
import zipfile
import zlib

P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
NS = {'p': P, 'a': A, 'r': R}
SCHEMA = 'jp-slides-structural-v2'
LIMITATIONS = [
    'Structural checks only; no visual, semantic, learning or clinical validation.',
    'SHA256 detects changed bytes; receipt is unsigned and is not tamper proof.',
    'Logo must be one explicit slide picture with approved PNG bytes; inherited logos are not counted.',
    'Grouped, rotated, flipped, tiled or nonrectangular logos are not certified.',
    'No full OOXML schema validation, rendering, readability, contrast or overlap review.',
    'Notes presence proves nonempty body text, not useful speech or study guidance.',
    'Explicit slide pictures require native nonblank descriptions, including the logo; description meaning and assistive reading order are not validated.',
    'Logo size/corner placement, image effects and actual visibility require rendered inspection.',
    'Aspect check allows only integer EMU rounding; PNG chunks/CRC are checked without pixel decoding.',
]


class Invalid(ValueError):
    pass


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    data = path.read_bytes()
    return {'path': str(path.resolve()), 'sha256': sha(data)}, data


def png_size(data):
    if data[:8] != b'\x89PNG\r\n\x1a\n' or data[8:16] != b'\0\0\0\rIHDR':
        raise Invalid('approved_logo_not_png')
    pos, kinds = 8, []
    while pos < len(data):
        length = struct.unpack('>I', data[pos:pos+4])[0]
        end = pos + 12 + length
        kind, value = data[pos+4:pos+8], data[pos+8:pos+8+length]
        if end > len(data) or zlib.crc32(kind + value) & 0xffffffff != struct.unpack('>I', data[end-4:end])[0]:
            raise Invalid('incomplete_or_corrupt_png_chunk')
        kinds.append(kind)
        pos = end
    pixels = struct.unpack('>II', data[16:24])
    if not all(pixels) or b'IDAT' not in kinds or kinds[-1:] != [b'IEND']:
        raise Invalid('incomplete_png')
    return pixels


def add(report, name, ok, slide=None):
    row = {'name': name, 'status': 'PASS' if ok else 'FAIL'}
    if slide is not None:
        row['slide'] = slide
    report['checks'].append(row)


def target(part, value):
    if not value or urlsplit(value).scheme or urlsplit(value).netloc:
        raise Invalid('unsupported_relationship_target')
    name = posixpath.normpath(posixpath.join(posixpath.dirname(part), unquote(value)))
    if value.startswith('/'):
        name = posixpath.normpath(unquote(value).lstrip('/'))
    if name.startswith('../') or name == '..' or '\\' in name:
        raise Invalid('invalid_relationship_target')
    return name


def relationships(xmls, part):
    folder, name = posixpath.split(part)
    relpart = posixpath.join(folder, '_rels', name + '.rels') if part else '_rels/.rels'
    root = xmls[relpart]
    if root.tag != '{' + PKG + '}Relationships':
        raise Invalid('invalid_relationships')
    rows = {}
    for item in root:
        rid = item.get('Id')
        if not rid or rid in rows:
            raise Invalid('duplicate_or_missing_relationship_id')
        rows[rid] = item
    return rows


def related(part, relation):
    if relation.get('TargetMode') == 'External':
        raise Invalid('external_required_part')
    return target(part, relation.get('Target'))


def has_text(root):
    for shape in root.findall('.//p:sp', NS):
        ph = shape.find('./p:nvSpPr/p:nvPr/p:ph', NS)
        if ph is not None and ph.get('type', 'obj') not in ('body', 'obj', 'title', 'ctrTitle', 'subTitle'):
            continue
        if any((text.text or '').strip() for text in shape.findall('./p:txBody//a:t', NS)):
            return True
    return any((text.text or '').strip() for text in root.findall('.//a:tbl//a:t', NS))


def logo_geometry(pic, parents, width, height, pixels):
    ancestor = parents.get(pic)
    while ancestor is not None:
        if ancestor.tag == '{' + P + '}grpSp':
            return False, False, False
        ancestor = parents.get(ancestor)
    xfrm = pic.find('./p:spPr/a:xfrm', NS)
    geom = pic.find('./p:spPr/a:prstGeom', NS)
    if xfrm is None or geom is None or geom.get('prst') != 'rect':
        return False, False, False
    off, ext = xfrm.find('a:off', NS), xfrm.find('a:ext', NS)
    if off is None or ext is None:
        return False, False, False
    x, y, cx, cy = [int(el.get(key, '0')) for el, key in ((off,'x'),(off,'y'),(ext,'cx'),(ext,'cy'))]
    direct = int(xfrm.get('rot', '0')) % 21600000 == 0 and not any(xfrm.get(key) in ('1','true') for key in ('flipH','flipV'))
    crops = pic.findall('./p:blipFill/a:srcRect', NS) + pic.findall('./p:blipFill/a:stretch/a:fillRect', NS)
    uncropped = not any(int(rect.get(key, '0')) != 0 for rect in crops for key in ('l','t','r','b'))
    uncropped = uncropped and pic.find('./p:blipFill/a:tile', NS) is None
    aspect = cx > 0 and cy > 0 and abs(cx * pixels[1] - cy * pixels[0]) <= sum(pixels)
    inside = cx > 0 and cy > 0 and x >= 0 and y >= 0 and x + cx <= width and y + cy <= height
    return direct and aspect, direct and uncropped, direct and inside


def verify(deck, logo, expected=None):
    report = {'schema': SCHEMA, 'status': 'FAIL', 'checks': [], 'slide_count': 0,
              'slide_order': [], 'expect_slides': expected, 'limitations': LIMITATIONS}
    try:
        report['deck'], data = identity(deck)
        report['logo'], logo_data = identity(logo)
        pixels = png_size(logo_data)
        report['logo'].update(width_px=pixels[0], height_px=pixels[1])
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            names = archive.namelist()
            if len(set(names)) != len(names) or archive.testzip() is not None:
                raise Invalid('duplicate_or_corrupt_zip_parts')
            xmls = {name: ET.fromstring(archive.read(name)) for name in names if name.endswith(('.xml', '.rels'))}
            if xmls['[Content_Types].xml'].tag != '{http://schemas.openxmlformats.org/package/2006/content-types}Types':
                raise Invalid('invalid_content_types')
            office = [r for r in relationships(xmls, '').values() if r.get('Type') == R + '/officeDocument']
            if len(office) != 1:
                raise Invalid('missing_presentation_relationship')
            presentation = related('', office[0])
            root, links = xmls[presentation], relationships(xmls, presentation)
            if root.tag != '{' + P + '}presentation':
                raise Invalid('invalid_presentation')
            size = root.find('p:sldSz', NS)
            width, height = int(size.get('cx')), int(size.get('cy'))
            if width <= 0 or height <= 0:
                raise Invalid('invalid_canvas')
            slides = root.findall('./p:sldIdLst/p:sldId', NS)
            report['slide_count'] = len(slides)
            add(report, 'nonzero_slides', bool(slides))
            add(report, 'expected_slide_count', expected is None or len(slides) == expected)
            seen = set()
            for index, item in enumerate(slides, 1):
                relation = links[item.get('{' + R + '}id')]
                if relation.get('Type') != R + '/slide':
                    raise Invalid('invalid_slide_relationship')
                part = related(presentation, relation)
                if part in seen:
                    raise Invalid('duplicate_slide_reference')
                seen.add(part)
                report['slide_order'].append(part)
                slide, rels = xmls[part], relationships(xmls, part)
                if slide.tag != '{' + P + '}sld':
                    raise Invalid('invalid_slide_root')
                add(report, 'editable_text', has_text(slide), index)
                notes = [r for r in rels.values() if r.get('Type') == R + '/notesSlide']
                note_ok = len(notes) == 1
                if note_ok:
                    note = xmls[related(part, notes[0])]
                    note_ok = note.tag == '{' + P + '}notes' and has_text(note)
                add(report, 'nonempty_notes_body', note_ok, index)
                matches = []
                for pic in slide.findall('.//p:pic', NS):
                    props = pic.find('./p:nvPicPr/p:cNvPr', NS)
                    described = props is not None and bool(props.get('descr', '').strip())
                    add(report, 'picture_description_present', described, index)
                    report['checks'][-1]['object_id'] = props.get('id') if props is not None else None
                    for blip in pic.findall('./p:blipFill/a:blip', NS):
                        rid = blip.get('{' + R + '}embed')
                        if rid in rels and rels[rid].get('Type') == R + '/image':
                            if sha(archive.read(related(part, rels[rid]))) == report['logo']['sha256']:
                                matches.append(pic)
                add(report, 'exactly_one_approved_logo', len(matches) == 1, index)
                if len(matches) == 1:
                    parents = {child: parent for parent in slide.iter() for child in parent}
                    geometry = logo_geometry(matches[0], parents, width, height, pixels)
                    for name, ok in zip(('logo_aspect_ratio','logo_uncropped','logo_inside_canvas'), geometry):
                        add(report, name, ok, index)
        add(report, 'ooxml_package_readable', True)
    except (OSError, ValueError, KeyError, AttributeError, TypeError, struct.error, ET.ParseError, zipfile.BadZipFile, RuntimeError):
        add(report, 'readable_supported_package_and_logo', False)
    report['status'] = 'PASS' if report['checks'] and all(c['status'] == 'PASS' for c in report['checks']) else 'FAIL'
    return report


def check_receipt(path):
    report = {'schema': SCHEMA, 'mode': 'check-receipt', 'status': 'FAIL', 'checks': [], 'limitations': LIMITATIONS}
    try:
        saved = json.loads(path.read_text(encoding='utf-8'))
        checks = saved.get('checks')
        valid = saved.get('schema') == SCHEMA and saved.get('status') == 'PASS'
        valid = valid and isinstance(checks, list) and bool(checks) and all(isinstance(c, dict) and c.get('name') and c.get('status') == 'PASS' for c in checks)
        add(report, 'receipt_contains_only_passing_nonempty_results', valid)
        for kind in ('deck', 'logo'):
            current, _ = identity(Path(saved[kind]['path']))
            add(report, kind + '_sha256_matches', current['sha256'] == saved[kind]['sha256'])
        if all(c['status'] == 'PASS' for c in report['checks']):
            fresh = verify(Path(saved['deck']['path']), Path(saved['logo']['path']), saved.get('slide_count'))
            add(report, 'current_structural_checks_pass', fresh['status'] == 'PASS')
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        add(report, 'readable_receipt_and_current_files', False)
    report['status'] = 'PASS' if report['checks'] and all(c['status'] == 'PASS' for c in report['checks']) else 'FAIL'
    return report


class Parser(argparse.ArgumentParser):
    def error(self, message):
        print(json.dumps({'status': 'FAIL', 'checks': [{'name': 'valid_cli_arguments', 'status': 'FAIL'}]}))
        raise SystemExit(2)


def main():
    parser = Parser(description=__doc__)
    parser.add_argument('deck', type=Path, nargs='?')
    parser.add_argument('--logo', type=Path)
    parser.add_argument('--receipt', type=Path)
    parser.add_argument('--expect-slides', type=int)
    parser.add_argument('--check-receipt', type=Path)
    args = parser.parse_args()
    if args.check_receipt:
        if args.deck or args.logo or args.receipt or args.expect_slides is not None:
            parser.error('exclusive mode')
        report = check_receipt(args.check_receipt)
    else:
        if not args.deck or not args.logo or not args.receipt:
            parser.error('deck, logo and receipt required')
        if args.deck.resolve() == args.receipt.resolve() or args.logo.resolve() == args.receipt.resolve():
            parser.error('receipt must not overwrite input')
        report = verify(args.deck, args.logo, args.expect_slides)
        try:
            args.receipt.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        except OSError:
            add(report, 'receipt_written', False)
            report['status'] = 'FAIL'
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report['status'] == 'PASS' else 2


if __name__ == '__main__':
    sys.exit(main())

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))


def test_v4_data_products_exist_and_parse():
    for name in ['technology_catalog.json', 'risks.json', 'mass_space.json']:
        p = ROOT / 'data' / name
        assert p.exists(), name
        json.loads(p.read_text(encoding='utf-8'))


def test_electrolyzer_shortlist_has_ten_candidates():
    catalog = load('technology_catalog.json')
    electrolysis = [x for x in catalog['items'] if x['category'] == 'electrolysis']
    assert len(electrolysis) >= 10
    for x in electrolysis:
        assert x['vendor'] and x['model'] and x['manufacturer_url'].startswith('https://')
        assert x['datasheet_url'].startswith('https://')
        assert 'score' in x and set(x['score']) >= {
            'scale_fit','dynamic_fit','maturity','offshore_integration','pressure_or_integration','evidence'
        }
        # Named vendor entries must not pretend to contain a commercial quote.
        assert 'price_eur' not in x and 'vendor_price' not in x


def test_technology_source_ids_are_traceable():
    source_ids = {x['id'] for x in load('sources.json')}
    catalog = load('technology_catalog.json')
    for item in catalog['items']:
        for sid in item.get('source_ids', []):
            assert sid in source_ids, (item['id'], sid)


def test_mass_register_reconciles_thesis_table_8():
    mass = load('mass_space.json')
    total = sum(x['mass_t'] for x in mass['items'])
    moment = sum(x['moment_tm'] for x in mass['items'])
    assert total == 24000
    assert moment == 505757
    assert abs(moment / total - 21.07) < 0.01
    assert mass['reported_total_mass_t'] == total
    assert mass['reported_total_moment_tm'] == moment


def test_risk_register_is_nontrivial_and_bilingual():
    risks = load('risks.json')
    assert len(risks) >= 18
    assert len({x['id'] for x in risks}) == len(risks)
    for r in risks:
        assert 1 <= r['probability'] <= 5
        assert 1 <= r['impact'] <= 5
        assert r['title'] and r['title_es']
        assert r['mitigation'] and r['mitigation_es']


def test_v4_interactions_are_present_in_html():
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    for token in [
        'id="langEn"', 'id="langEs"', 'id="geoMap"', 'id="technology"',
        'id="mass-budget"', 'id="risk"', 'id="scenarioComparison"', 'id="decisionGrid"',
        'Open in Google Maps', 'technology_catalog.json'
    ]:
        # technology_catalog.json is loaded from JS, not necessarily HTML
        if token.endswith('.json'):
            continue
        assert token in html, token
    js = (ROOT / 'assets/app.js').read_text(encoding='utf-8')
    assert 'technology_catalog.json' in js
    assert 'mass_space.json' in js
    assert 'risks.json' in js
    assert 'tile.openstreetmap.org' in js
    assert 'World_Imagery' in js
    assert 'google.com/maps/search/?api=1&query=' in js


def test_no_external_javascript_runtime_dependency():
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    scripts = re.findall(r'<script[^>]+src="([^"]+)"', html)
    assert scripts == ['assets/app.js']


def test_every_vendor_candidate_has_traceable_public_source():
    source_ids = {x['id'] for x in load('sources.json')}
    catalog = load('technology_catalog.json')
    for item in catalog['items']:
        assert item.get('source_ids'), item['id']
        assert set(item['source_ids']).issubset(source_ids), item['id']
        assert item['manufacturer_url'].startswith('https://')
        assert item['datasheet_url'].startswith('https://')


def test_configuration_selection_is_category_based_and_exported():
    js = (ROOT / 'assets/app.js').read_text(encoding='utf-8')
    assert "chosenTech={electrolysis:null,methanol:null,dac:null,water:null}" in js
    assert "selectedTechnologyPayload()" in js
    assert "quote required" in js.lower()
    assert "Selection is recorded without inventing" in js


def test_bilingual_interface_covers_major_sections():
    js = (ROOT / 'assets/app.js').read_text(encoding='utf-8')
    for spanish in [
        'Diseña la molécula offshore',
        'Analiza el Cantábrico antes de dimensionar acero',
        'Compara tecnologías reales',
        'presupuesto de pesos y espacio',
        'registro de riesgos conceptual',
        'De hipótesis de TFG a software de ingeniería auditable',
    ]:
        assert spanish.lower() in js.lower()


def test_v4_final_map_and_comparison_controls_present():
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    js = (ROOT / 'assets/app.js').read_text(encoding='utf-8')
    css = (ROOT / 'assets/styles.css').read_text(encoding='utf-8')
    for token in ['id="centerSelectedSite"','id="copySiteCoords"','id="techComparison"','id="clearTechCompare"','EXECUTIVE DECISION SNAPSHOT']:
        assert token in html
    for token in ['saveTechCompare','renderTechComparison','methanor-tech-compare','Coordinates copied','technology_comparison:techCompare']:
        assert token in js
    assert '.map-site-pin{width:30px;height:30px' in css
    assert '.map-site-pin.custom::after' in css


def test_v4_export_version_is_current():
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    js = (ROOT / 'assets/app.js').read_text(encoding='utf-8')
    assert '<meta name="version" content="4.1"' in html
    assert "version:'4.2'" in js
    assert "methanor-scenario-v4.2.json" in js


def test_site_names_and_clicked_point_are_bilingual_and_rerender_map():
    sites = load('sites.json')
    assert all(s.get('name_es') for s in sites)
    js = (ROOT / 'assets/app.js').read_text(encoding='utf-8')
    assert 'function siteDisplayName' in js
    assert "name_es:'Punto seleccionado'" in js
    assert "poem_alignment_es:'Requiere comprobación SIG oficial'" in js
    assert 'renderMap();renderSiteDetail();renderTechnology()' in js


def test_html_ids_anchors_and_local_assets_are_consistent():
    from html.parser import HTMLParser

    class Collector(HTMLParser):
        def __init__(self):
            super().__init__()
            self.ids = []
            self.hrefs = []
            self.assets = []
        def handle_starttag(self, tag, attrs):
            a = dict(attrs)
            if a.get('id'):
                self.ids.append(a['id'])
            if tag == 'a' and a.get('href'):
                self.hrefs.append(a['href'])
            for key in ('src', 'href'):
                value = a.get(key)
                if value and not value.startswith(('http://','https://','#','data:','mailto:','tel:')):
                    self.assets.append(value)

    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    parser = Collector(); parser.feed(html)
    assert len(parser.ids) == len(set(parser.ids)), 'duplicate HTML id detected'
    targets = set(parser.ids)
    missing_anchors = sorted({h for h in parser.hrefs if h.startswith('#') and len(h) > 1 and h[1:] not in targets})
    assert not missing_anchors, missing_anchors
    missing_assets = []
    for rel in parser.assets:
        rel = rel.split('?', 1)[0].split('#', 1)[0]
        if not (ROOT / rel).exists():
            missing_assets.append(rel)
    assert not missing_assets, missing_assets


def test_all_json_data_files_parse_and_release_has_social_metadata():
    for p in (ROOT / 'data').glob('*.json'):
        json.loads(p.read_text(encoding='utf-8'))
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    for token in [
        'property="og:title"', 'property="og:description"',
        'property="og:image" content="assets/social-preview.png"',
        'name="twitter:card" content="summary_large_image"',
        'id="appError"', '<noscript>'
    ]:
        assert token in html
    assert (ROOT / 'assets/social-preview.png').exists()


def test_final_release_has_no_stale_v3_branding_outside_history():
    paths = [ROOT/'index.html', ROOT/'assets/app.js', ROOT/'engine/methanor.py', ROOT/'README.md', ROOT/'PROJECT_STATUS.md']
    for p in paths:
        text = p.read_text(encoding='utf-8')
        assert 'MethaNor V3' not in text
        assert 'engine v3.0' not in text


def test_v41_bilingual_vendor_and_source_governance():
    catalog = load('technology_catalog.json')
    for item in catalog['items']:
        for field in ['capacity','purity','turndown','startup','footprint','maturity']:
            if item.get(field):
                assert item.get(field + '_es'), (item['id'], field)
    sources = load('sources.json')
    for source in sources:
        assert source.get('use_es'), source['id']
        assert source.get('accessed') == '2026-09-13', source['id']
        assert source.get('date_basis') in {'published_or_reference_year','live_page_accessed'}, source['id']


def test_v41_portfolio_fit_method_is_explicit_and_consistent():
    catalog = load('technology_catalog.json')
    weights = catalog['meta']['score_weights']
    assert abs(sum(weights.values()) - 1.0) < 1e-12
    assert set(catalog['meta']['score_labels']) == set(weights)
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    js = (ROOT / 'assets/app.js').read_text(encoding='utf-8')
    assert 'id="techScoreMethod"' in html
    assert 'id="techScoreWeights"' in html
    assert 'function renderTechScoreMethod' in js
    assert 'not a procurement recommendation' in catalog['meta']['score_explainer']


def test_v41_final_polish_has_single_break_even_solver_and_conceptual_branding():
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    js = (ROOT / 'assets/app.js').read_text(encoding='utf-8')
    assert js.count('function bisect(') == 1
    assert 'Conceptual Offshore e-Methanol Digital Twin' in html
    for translated_fragment in [
        "'Design the':'Diseña la'",
        "'Synthesis':'Síntesis'",
        "'Remote':'Remoto'",
        "'Methodology ↗':'Metodología ↗'",
    ]:
        assert translated_fragment in js

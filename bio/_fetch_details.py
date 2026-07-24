#!/usr/bin/env python3
"""Fetch detailed article content from key URLs for better summaries."""
import urllib.request, re, html, json, sys

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

urls = [
    'https://www.sciencedaily.com/releases/2026/07/260719230608.htm',
    'https://www.news-medical.net/news/20260722/SuperAgers-retain-exceptional-memory-through-mechanisms-beyond-genetics.aspx',
    'https://www.sciencedaily.com/releases/2026/07/260722032108.htm',
    'https://www.sciencedaily.com/releases/2026/07/260719035951.htm',
    'https://www.news-medical.net/news/20260724/Microglia-found-to-drive-sleep-loss-in-Alzheimere28099s.aspx',
    'https://www.news-medical.net/news/20260724/Spontaneous-brain-state-fluctuations-influence-real-time-memory-formation.aspx',
    'https://www.news-medical.net/news/20260724/Emerging-non-endocytic-transmembrane-delivery-strategies-for-precision-medicine.aspx',
]

results = {}
for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='replace')
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
        title = html.unescape(re.sub(r'<[^>]+>', '', h1.group(1))).strip() if h1 else ''
        meta = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]+)"', content)
        desc = html.unescape(meta.group(1)).strip() if meta else ''
        lead = re.search(r'class="lead"[^>]*>(.*?)</div>', content, re.DOTALL)
        lead_text = html.unescape(re.sub(r'<[^>]+>', '', lead.group(1))).strip()[:500] if lead else ''
        pars = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
        clean_pars = []
        for p in pars:
            c = html.unescape(re.sub(r'<[^>]+>', '', p)).strip()
            if len(c) > 100 and not any(s in c.lower() for s in ['copyright', 'all rights reserved', 'subscribe', 'journal reference', 'story source']):
                clean_pars.append(c)
        results[url.split('/')[-1][:50]] = {
            'title': title[:200],
            'desc': desc[:500],
            'lead': lead_text[:400],
            'body': clean_pars[0][:500] if clean_pars else '',
        }
    except Exception as e:
        results[url.split('/')[-1][:50]] = {'error': str(e)}

print(json.dumps(results, ensure_ascii=False, indent=2))

export const config = { runtime: 'edge' };

/* Internet se (free + non-free) item ki photo dhundhna.
   GET /api/img-search?q=<naam>        -> [{t: thumb, u: full, src:'Web'}]
   GET /api/img-search?p=<image url>   -> image bytes (CORS ke liye proxy, crop/upload ke kaam aata hai) */
const ALLOWED_ORIGINS = ['https://kiranabillgenerator.vercel.app'];
const UA = 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36';

function originOk(req) {
  const origin = req.headers.get('origin') || '', referer = req.headers.get('referer') || '';
  return ALLOWED_ORIGINS.some(o => origin.indexOf(o) === 0 || referer.indexOf(o) === 0);
}
function json(obj, status) {
  return new Response(JSON.stringify(obj), { status: status || 200, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
}
function safeUrl(u) {
  try {
    const x = new URL(u);
    if (x.protocol !== 'https:') return null;
    const h = x.hostname.toLowerCase();
    if (!h.includes('.') || h === 'localhost' || /^\d+\.\d+\.\d+\.\d+$/.test(h) || h.includes(':') || h.endsWith('.local') || h.endsWith('.internal')) return null;
    return x.toString();
  } catch (e) { return null; }
}
const dec = s => s.replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');

export default async function handler(req) {
  if (req.method !== 'GET') return json({ error: 'Method not allowed' }, 405);
  if (!originOk(req)) return json({ error: 'Origin not allowed' }, 403);
  const url = new URL(req.url);

  const p = url.searchParams.get('p');
  if (p) {
    const target = safeUrl(p);
    if (!target) return json({ error: 'Bad url' }, 400);
    try {
      const r = await fetch(target, { headers: { 'User-Agent': UA, 'Accept': 'image/*' }, redirect: 'follow' });
      const ct = r.headers.get('content-type') || '';
      if (!r.ok || !/^image\/(jpeg|png|webp)/.test(ct)) return json({ error: 'Not an image' }, 415);
      const len = parseInt(r.headers.get('content-length') || '0', 10);
      if (len > 8 * 1024 * 1024) return json({ error: 'Too large' }, 413);
      const buf = await r.arrayBuffer();
      if (buf.byteLength > 8 * 1024 * 1024) return json({ error: 'Too large' }, 413);
      return new Response(buf, { headers: { 'Content-Type': ct.split(';')[0], 'Cache-Control': 'public, max-age=3600' } });
    } catch (e) { return json({ error: 'Fetch failed' }, 502); }
  }

  const q = (url.searchParams.get('q') || '').trim().slice(0, 100);
  if (!q) return json({ results: [] });
  try {
    const r = await fetch('https://www.bing.com/images/async?q=' + encodeURIComponent(q) + '&first=0&count=30&mmasync=1&adlt=moderate', {
      headers: { 'User-Agent': UA, 'Accept-Language': 'en-IN,en;q=0.9' }
    });
    const html = await r.text();
    const out = [], seen = new Set();
    const re = /\sm="([^"]+)"/g; let m;
    while ((m = re.exec(html)) && out.length < 24) {
      try {
        const o = JSON.parse(dec(m[1]));
        const t = safeUrl(o.turl), u = safeUrl(o.murl);
        if (t && u && !seen.has(u)) { seen.add(u); out.push({ t, u, src: 'Web' }); }
      } catch (e) { /* skip */ }
    }
    return json({ results: out });
  } catch (e) { return json({ results: [], error: 'Search failed' }); }
}

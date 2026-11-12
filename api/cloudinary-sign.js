export const config = { runtime: 'edge' };

/* Cloudinary signed-upload: app ko sirf signature milta hai, API secret kabhi bahar nahi jata. */
const ALLOWED_ORIGINS = ['https://kiranabillgenerator.vercel.app'];
const FIREBASE_WEB_KEY = 'AIzaSyDQ-fm6-_bs728n6rcUS-XS9Zl-hqbIQhA'; // public web key (app mein bhi hai)

function json(obj, status) {
  return new Response(JSON.stringify(obj), { status: status || 200, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
}
function originOk(req) {
  const origin = req.headers.get('origin') || '', referer = req.headers.get('referer') || '';
  return ALLOWED_ORIGINS.some(o => origin.indexOf(o) === 0 || referer.indexOf(o) === 0);
}
async function sha1Hex(str) {
  const buf = await crypto.subtle.digest('SHA-1', new TextEncoder().encode(str));
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}

export default async function handler(req) {
  if (req.method !== 'POST') return json({ error: 'Method not allowed' }, 405);
  if (!originOk(req)) return json({ error: 'Origin not allowed' }, 403);

  const cloud = process.env.CLOUDINARY_CLOUD_NAME, key = process.env.CLOUDINARY_API_KEY, secret = process.env.CLOUDINARY_API_SECRET;
  if (!cloud || !key || !secret) return json({ error: 'Cloudinary server par set nahi hai' }, 500);

  let body = {};
  try { body = await req.json(); } catch (e) {}
  const idToken = String(body.idToken || '');
  if (!idToken) return json({ error: 'Login zaroori hai' }, 401);

  // Sirf logged-in (anonymous nahi) user ko permission
  let uid = '';
  try {
    const r = await fetch('https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=' + FIREBASE_WEB_KEY, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ idToken })
    });
    const d = await r.json();
    const u = d && d.users && d.users[0];
    if (!r.ok || !u) return json({ error: 'Login check fail' }, 401);
    const anon = !(u.providerUserInfo && u.providerUserInfo.length);
    // Anonymous sirf Staff display ke item-photo scope ke liye allowed (alag folder mein)
    if (anon && body.scope !== 'staff') return json({ error: 'Anonymous login se upload nahi hota' }, 403);
    uid = anon ? 'staff' : String(u.localId || '').replace(/[^A-Za-z0-9_-]/g, '').slice(0, 40);
  } catch (e) { return json({ error: 'Login check fail' }, 401); }

  const timestamp = Math.floor(Date.now() / 1000);
  const folder = 'mittu-items/' + uid;
  const allowed = 'jpg,png,webp';
  // Cloudinary: params alphabetical order mein, "&" se jode, phir secret
  const signature = await sha1Hex('allowed_formats=' + allowed + '&folder=' + folder + '&timestamp=' + timestamp + secret);
  return json({ cloudName: cloud, apiKey: key, timestamp, folder, allowed_formats: allowed, signature });
}

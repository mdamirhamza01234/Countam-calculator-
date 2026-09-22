export const config = { runtime: 'edge' };

const ALLOWED_MODELS = [
  'gemini-3.5-flash',
  'gemini-3-flash-preview',
  'gemini-3.1-flash-lite',
  'gemini-2.5-flash'
];

const ALLOWED_ORIGINS = [
  'https://kiranabillgenerator.vercel.app'
];

function corsCheck(req) {
  const origin = req.headers.get('origin') || '';
  const referer = req.headers.get('referer') || '';
  return ALLOWED_ORIGINS.some(function(o) {
    return origin.indexOf(o) === 0 || referer.indexOf(o) === 0;
  });
}

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: { message: 'Method not allowed' } }), { status: 405 });
  }

  if (!corsCheck(req)) {
    return new Response(JSON.stringify({ error: { message: 'Origin not allowed' } }), { status: 403 });
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return new Response(JSON.stringify({ error: { message: 'Server par GEMINI_API_KEY set nahi hai.' } }), { status: 500 });
  }

  const url = new URL(req.url);
  const model = url.searchParams.get('model') || '';
  if (ALLOWED_MODELS.indexOf(model) === -1) {
    return new Response(JSON.stringify({ error: { message: 'Model allowed nahi hai: ' + model } }), { status: 400 });
  }
  const stream = url.searchParams.get('stream') === '1';

  const googleUrl = 'https://generativelanguage.googleapis.com/v1beta/models/' + model +
    (stream ? ':streamGenerateContent?alt=sse' : ':generateContent');

  const body = await req.text();

  let googleResp;
  try {
    googleResp = await fetch(googleUrl, {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-goog-api-key': apiKey },
      body: body
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: { message: 'Google Gemini tak pahunch nahi paye.' } }), { status: 502 });
  }

  return new Response(googleResp.body, {
    status: googleResp.status,
    headers: { 'content-type': googleResp.headers.get('content-type') || 'application/json' }
  });
}

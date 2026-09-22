api/gemini.js — Vercel Edge Function
//
// Ye function browser aur Google Gemini API ke beech ek "proxy" hai.
// GEMINI_API_KEY ab is file mein bhi nahi likhi — Vercel Dashboard ke
// Environment Variable se aati hai, jo browser ko kabhi bhejta hi nahi.
// Isliye ab "View Page Source" karke koi bhi key nahi churaa sakta.
//
// Client (index.html) ab seedha Google ko nahi, balki apni hi site ke
// "/api/gemini" address par request bhejta hai. Ye function wahi request
// asli key laga kar Google ko forward karta hai aur jawab wapas de deta hai.

export const config = { runtime: 'edge' };

// Sirf inhi models ko allow karo (jo app use karti hai) — koi bhi random
// model name daal kar ispe se paisa/quota na uda sake.
const ALLOWED_MODELS = [
  'gemini-3.5-flash',
  'gemini-3-flash-preview',
  'gemini-3.1-flash-lite',
  'gemini-2.5-flash'
];

// >>> Apni asli deployed domain(s) yahan likhein. Jitni bhi domain se ye
// app khulti hai (production URL, custom domain agar ho), sabko yahan
// add karein — warna wahan se AI kaam nahi karega. <<<
const ALLOWED_ORIGINS = [
  'https://kiranabillgenerator.vercel.app'
];

function corsCheck(req) {
  const origin = req.headers.get('origin') || '';
  const referer = req.headers.get('referer') || '';
  return ALLOWED_ORIGINS.some(o => origin.startsWith(o) || referer.startsWith(o));
}

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: { message: 'Method not allowed' } }), { status: 405 });
  }

  // Basic abuse-guard: sirf apni hi website se aayi request allow karo.
  // (Ye foolproof nahi hai, lekin random bots/curl scripts ko rok deta hai —
  // asli suraksha ye hai ki key ab kabhi client code mein hai hi nahi.)
  if (!corsCheck(req)) {
    return new Response(JSON.stringify({ error: { message: 'Origin not allowed' } }), { status: 403 });
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return new Response(JSON.stringify({ error: { message: 'Server par GEMINI_API_KEY set nahi hai. Vercel > Settings > Environment Variables mein add karein.' } }), { status: 500 });
  }

  const url = new URL(req.url);
  const model = url.searchParams.get('model') || '';
  if (!ALLOWED_MODELS.includes(model)) {
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
      body
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: { message: 'Google Gemini tak pahunch nahi paye: ' + (e && e.message) } }), { status: 502 });
  }

  // Google ka response (status + body, SSE stream ho ya plain JSON) waisa hi
  // wapas bhej do — client ka existing code (401/403 check, JSON parse,
  // stream reader) bina kisi badlaav ke kaam karta rahega.
  return new Response(googleResp.body, {
    status: googleResp.status,
    headers: { 'content-type': googleResp.headers.get('content-type') || 'application/json' }
  });
  }

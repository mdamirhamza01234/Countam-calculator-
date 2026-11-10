#!/usr/bin/env python3
"""Mittu Associated Retailer app = billing app (index.html) ka retailer version.
Ye script root index.html se retailer/index.html banati hai. Billing app mein badlav ke baad dobara chalayein:
    python3 scripts/build-retailer.py
"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
s = (root / 'index.html').read_text()

def rep(old, new, cnt=1):
    global s
    assert old in s, 'nahi mila: ' + old[:70]
    s = s.replace(old, new, cnt)

# ---------- head ----------
rep('<title>Mittu Wholesaler & Retailer</title>',
    '<title>Mittu Associated Retailer</title>\n<link rel="manifest" href="manifest.webmanifest">\n<meta name="theme-color" content="#0d6e4e">\n<link rel="apple-touch-icon" href="icon-192.png">')
SHIM = r'''<script>
/* Retailer app: apna alag storage (main billing app se mix na ho) + retailer profile helpers */
window.RETAILER_APP = true;
(function(){
  try {
    var real = window.localStorage, P = 'rt_';
    var wrap = {
      getItem: function(k){ return real.getItem(P + k); },
      setItem: function(k, v){ return real.setItem(P + k, v); },
      removeItem: function(k){ return real.removeItem(P + k); },
      clear: function(){ Object.keys(real).filter(function(k){ return k.indexOf(P) === 0; }).forEach(function(k){ real.removeItem(k); }); },
      key: function(i){ var ks = Object.keys(real).filter(function(k){ return k.indexOf(P) === 0; }); return ks[i] == null ? null : ks[i].slice(P.length); },
      get length(){ return Object.keys(real).filter(function(k){ return k.indexOf(P) === 0; }).length; }
    };
    Object.defineProperty(window, 'localStorage', { value: new Proxy(wrap, { get: function(t, k){ var v = t[k]; return typeof v === 'function' ? v.bind(t) : v; }, set: function(t, k, v){ t.setItem(k, v); return true; }, deleteProperty: function(t, k){ t.removeItem(k); return true; }, ownKeys: function(){ return Object.keys(real).filter(function(k){ return k.indexOf(P) === 0; }).map(function(k){ return k.slice(P.length); }); }, getOwnPropertyDescriptor: function(t, k){ return real.getItem(P + k) == null ? undefined : { value: real.getItem(P + k), enumerable: true, configurable: true, writable: true }; } }), configurable: true });
  } catch(e){}
  window.RT_PROFILE = function(){ try { return JSON.parse(localStorage.getItem('retailer_profile') || 'null') || {}; } catch(e){ return {}; } };
  window.RT_NAME = function(){ return (window.RT_PROFILE().name || 'Mittu Associated Retailer'); };
  window.RT_UPI = function(){ return (window.RT_PROFILE().upi || ''); };
})();
</script>
</head>'''
rep('</head>', SHIM)

# ---------- branding ----------
rep('<span class="cart-glow">🛒</span> Mittu Wholesaler</span><span class="tb-sub">&amp; Retailer</span>',
    '<span class="cart-glow">🛒</span> <span class="rt-name">Mittu Associated</span></span><span class="tb-sub">Retailer</span>')
rep('<span class="cart-glow">🛒</span> Mittu Wholesaler & Retailer</span>', '<span class="cart-glow">🛒</span> <span class="rt-name">Mittu Associated Retailer</span></span>')
s = s.replace('</svg> Mittu Wholesaler & Retailer</div>', '</svg> <span class="rt-name-full">Mittu Associated Retailer</span></div>')
s = s.replace('<div style="color:#ffd54f; font-weight:900; font-size:20px; letter-spacing:1px;">MITTU WHOLESALER & RETAILER</div>', '<div class="rt-name-up" style="color:#ffd54f; font-weight:900; font-size:20px; letter-spacing:1px;">MITTU ASSOCIATED RETAILER</div>')
s = s.replace('<p style="color:#e6d5c2; font-size:13px; margin:2px 0 0 0;">UPI ID: 7303714309@axl</p>', '<p style="color:#e6d5c2; font-size:13px; margin:2px 0 0 0;">UPI ID: <span class="rt-upi"></span></p>')
s = s.replace('MITTU<br>WHOLESALER & RETAILER</div>', '<span class="rt-name-up">MITTU ASSOCIATED RETAILER</span></div>')
s = s.replace('<div class="inv-company">Mittu Wholesaler & Retailer</div>', '<div class="inv-company rt-name-full">Mittu Associated Retailer</div>')
s = s.replace('<div class="inv-addr-line">Rangra, Bhagalpur, Bihar, 853204, India.</div>', '<div class="inv-addr-line rt-addr"></div>')
s = s.replace('<div class="inv-addr-line">Mobile: +91 9540125307</div>', '<div class="inv-addr-line">Mobile: <span class="rt-phone"></span></div>')
s = s.replace('<div>For Mittu Wholesaler & Retailer</div>', '<div>For <span class="rt-name-full">Mittu Associated Retailer</span></div>')
s = s.replace("3. Subject to 'Bhagalpur' Jurisdiction only.", "3. Subject to local Jurisdiction only.")
# JS strings
s = s.replace("pdf.text('Mittu Wholesaler & Retailer', ", "pdf.text(RT_NAME(), ")
s = s.replace("pdf.text('Mittu Wholesaler & Retailer - Stock Purchase Entry', ", "pdf.text(RT_NAME() + ' - Stock Purchase Entry', ")
s = s.replace("pdf.text('Mittu Wholesaler & Retailer - Customer Record', ", "pdf.text(RT_NAME() + ' - Customer Record', ")
s = s.replace("subject: 'Mittu Wholesaler & Retailer Invoice'", "subject: RT_NAME() + ' Invoice'")
s = s.replace("m += `🛒 *MITTU WHOLESALER & RETAILER* 🛒\\n`;", "m += `🛒 *${RT_NAME().toUpperCase()}* 🛒\\n`;")
s = s.replace("m += `Mittu Wholesale se kharidari", "m += `${RT_NAME()} se kharidari")
s = s.replace("m += `— Team Mittu Wholesale`;", "m += `— ${RT_NAME()}`;")
s = s.replace("m += `*+91-9540125307*\\n`;", "m += `*${RT_PROFILE().phone ? '+91-' + RT_PROFILE().phone : ''}*\\n`;")
s = s.replace("m += `📍 Rangra, Bhagalpur, Bihar - 853204\\n\\n`;", "m += (RT_PROFILE().addr ? `📍 ${RT_PROFILE().addr}\\n\\n` : '\\n');")
s = s.replace('<div class="shop">Mittu Wholesaler & Retailer</div>', '<div class="shop">${RT_NAME()}</div>')
s = s.replace('<div class="center">Rangra, Bhagalpur, Bihar, 853204, India.</div>', '<div class="center">${RT_PROFILE().addr || \'\'}</div>')
s = s.replace('<div class="center">Mobile: +91 9540125307</div>', '<div class="center">Mobile: ${RT_PROFILE().phone ? \'+91 \' + RT_PROFILE().phone : \'\'}</div>')
s = s.replace('<div class="center small">For Mittu Wholesaler & Retailer</div>', '<div class="center small">For ${RT_NAME()}</div>')
s = s.replace("name: 'Mittu Wholesaler & Retailer',\n      address: 'Rangra, Bhagalpur, Bihar, 853204, India.',\n      mobile: '+91 9540125307'",
              "name: RT_NAME(),\n      address: RT_PROFILE().addr || '',\n      mobile: RT_PROFILE().phone ? '+91 ' + RT_PROFILE().phone : ''")
# UPI
rep("const upiId = '7303714309@axl';\n  const payeeName = 'MITTU WHOLESALER & RETAILER';", "const upiId = RT_UPI();\n  const payeeName = RT_NAME().toUpperCase();")
# ---------- Firebase paths ----------
rep("onValue(ref(fbDb, 'shopOrders'), (snap) => {", "onValue(ref(fbDb, 'retailerOrders/' + user.uid), (snap) => {")
rep("Database rules mein shopOrders ka read allow karein.", "Firebase Database rules mein retailerOrders wale rules Publish karein.")
rep("if(it.imageUrl && /^https:\\/\\//.test(it.imageUrl)) o.i = it.imageUrl;", "if(it.imageUrl && /^https:\\/\\//.test(it.imageUrl)) o.i = it.imageUrl;\n        if(it.category) o.c = String(it.category).slice(0, 40);")
rep("await set(ref(fbDb, 'publicShop/stock'), out);",
    "await set(ref(fbDb, 'retailers/' + user.uid + '/stock'), out);\n      if (typeof window.rtPublishIndex === 'function') await window.rtPublishIndex(user);")
# profile/index publish helper inside the module (needs set/ref)
rep("  // Turant publish karta hai aur result {ok, count, msg} deta hai",
    """  // Retailer ki dukaan Mittu Online Shop ke 'Store' list mein dikhane ke liye
  window.rtPublishIndex = async function(user){
    user = user || window.currentFirebaseUser || fbAuth.currentUser;
    const p = (typeof RT_PROFILE === 'function') ? RT_PROFILE() : {};
    if(!user || user.isAnonymous || !p.name || !p.type) return;
    await set(ref(fbDb, 'retailerIndex/' + user.uid), { name: String(p.name).slice(0, 60), type: String(p.type).slice(0, 60), upi: String(p.upi || ''), ts: Date.now() });
    await set(ref(fbDb, 'retailerProfiles/' + user.uid), { name: p.name, type: p.type, phone: p.phone || '', upi: p.upi || '', addr: p.addr || '', ts: Date.now() });
  };
  window.addEventListener('mittuFirebaseUserReady', () => { setTimeout(() => { try { window.rtPublishIndex(); } catch(e){} }, 2500); });
  // Turant publish karta hai aur result {ok, count, msg} deta hai""")
# ---------- stock category ----------
rep('''    <div class="field">
      <label id="stockQtyLabel">Quantity</label>''', '''    <div class="field">
      <label>Category (online shop mein is naam se dikhega)</label>
      <input type="text" id="stockItemCategory" list="stockCatList" placeholder="jaise: Meetha Pani Machli" autocomplete="off">
      <datalist id="stockCatList"></datalist>
    </div>
    <div class="field">
      <label id="stockQtyLabel">Quantity</label>''')
rep("    document.getElementById('stockItemHindi').value = item.hindiName || '';", "    document.getElementById('stockItemHindi').value = item.hindiName || '';\n    document.getElementById('stockItemCategory').value = item.category || '';")
rep("['stockItemName','stockItemHindi','stockItemQty',", "['stockItemName','stockItemHindi','stockItemCategory','stockItemQty',")
rep("    hindiName: hindiClean(document.getElementById('stockItemHindi').value) || hindiFromDict(name),", "    hindiName: hindiClean(document.getElementById('stockItemHindi').value) || hindiFromDict(name),\n    category: document.getElementById('stockItemCategory').value.trim().slice(0, 40),")
rep("  overlay.style.display = 'flex';\n}\nfunction closeStockItemModal(){", "  if(typeof rtFillCatList === 'function') rtFillCatList();\n  overlay.style.display = 'flex';\n}\nfunction closeStockItemModal(){")

# ---------- retailer onboarding + runtime ----------
GROUPS = [
 ("Restaurant", ["Restaurant","Biryani Restaurant"]),
 ("Khane-Peene aur Daily Needs", ["Grocery Store","Vegetable Store","Fruit Store","Fish Store","Chicken & Meat Store","Milk & Dairy Store","Sweet & Snacks Store","Bakery & Cake Store","Dry Fruits & Spice Store","Pan & Mouth Freshener Store"]),
 ("Kapde aur Fashion", ["Clothing / Apparel Store","Readymade Garments Store","Designer Boutique Store","Footwear Store","Cosmetic & Beauty Store","Jewellery Store","Bangles & Accessories Store"]),
 ("Padhai aur Sehat", ["Medical Store / Pharmacy","Book Store","Stationery Store","Optical Store","Surgical & Health Equipment Store"]),
 ("Ghar aur Construction", ["Hardware Store","Sanitary & Plumbing Store","Electrical Store","Paint Store","Utensil Store","Furniture Store","Home Decor Store"]),
 ("Electronics aur Gadgets", ["Mobile & Gadget Store","Mobile Repairing & Accessories Store","Electronic Appliance Store","Computer & Laptop Store","Camera & Photo Studio Store"]),
 ("Khel, Entertainment aur Gifts", ["Toy Store","Gift & Greeting Store","Sports Goods Store","Pooja Samagri Store","Pet Food & Care Store"]),
]
opts = ''.join('<optgroup label="%s">%s</optgroup>' % (g, ''.join('<option>%s</option>' % t.replace('&', '&amp;') for t in ts)) for g, ts in GROUPS)
CATSUG = {
 "Fish Store": ["Meetha Pani Machli", "Samudri Machli", "Jhinga / Prawn", "Sukhi Machli", "Machli ke Bachche"],
 "Vegetable Store": ["Sabzi", "Hari Patte", "Kand / Jadein", "Masala Sabzi"],
 "Fruit Store": ["Mausami Phal", "Seasonal Phal", "Dry / Imported Phal"],
 "Chicken & Meat Store": ["Chicken", "Mutton", "Anda", "Frozen Meat"],
 "Milk & Dairy Store": ["Doodh", "Dahi / Lassi", "Paneer / Cheese", "Ghee / Makkhan"],
 "Sweet & Snacks Store": ["Mithai", "Namkeen", "Samosa / Kachori", "Gift Box"],
 "Bakery & Cake Store": ["Bread", "Cake", "Biscuit / Cookies", "Pastry"],
 "Dry Fruits & Spice Store": ["Dry Fruits", "Sabut Masale", "Pisa Masale", "Mix Masale"],
 "Medical Store / Pharmacy": ["Tablet / Capsule", "Syrup", "Ointment", "Surgical", "Health Drink"],
 "Stationery Store": ["Copy / Notebook", "Pen / Pencil", "Colour / Art", "Office Saman"],
 "Footwear Store": ["Gents", "Ladies", "Kids", "Chappal"],
 "Clothing / Apparel Store": ["Gents", "Ladies", "Kids", "Saree / Suit"],
}
import json
RUNTIME = '''
<style>
#rtOnb{position:fixed;inset:0;z-index:2147483000;background:linear-gradient(160deg,#0b5a3f,#1b9d6a);display:none;align-items:flex-start;justify-content:center;overflow:auto;padding:18px 14px}
#rtOnb .card{background:#fff;border-radius:20px;padding:22px 18px;width:min(96vw,430px);margin:auto;box-shadow:0 18px 60px rgba(0,0,0,.35)}
#rtOnb h2{margin:0 0 4px;color:#0d6e4e;font-size:22px}
#rtOnb p.sub{margin:0 0 14px;color:#555;font-size:13.5px}
#rtOnb label{display:block;font-weight:700;font-size:13px;margin:12px 0 5px;color:#333}
#rtOnb input,#rtOnb select{width:100%;padding:13px 12px;border:1.5px solid #cfd8e3;border-radius:12px;font-size:16px;background:#fff;box-sizing:border-box}
#rtOnb .go{margin-top:18px;width:100%;padding:15px;border:0;border-radius:13px;background:#0d6e4e;color:#fff;font-size:17px;font-weight:800}
#rtOnb .err{color:#b3261e;font-size:13px;min-height:16px;margin-top:8px}
</style>
<div id="rtOnb"><div class="card">
  <button type="button" id="rtBack" aria-label="Wapas" style="display:none;border:0;background:#eef3f0;border-radius:50%;width:42px;height:42px;font-size:22px;color:#0d6e4e;margin:-6px 0 8px -4px;cursor:pointer">←</button>
  <h2>🛒 Mittu Associated Retailer</h2>
  <p class="sub">Apni dukaan ki jaankari bharein. Isi ke hisaab se aapka stock, bill aur online shop banega.</p>
  <label>Dukaan / Retailer ka naam</label><input id="rtName" maxlength="50" placeholder="jaise: Rahim Machli Dukan" autocomplete="off">
  <label>Dukaan ka type</label>
  <button type="button" id="rtTypeBtn" style="width:100%;text-align:left;padding:13px 12px;border:1.5px solid #cfd8e3;border-radius:12px;font-size:16px;background:#fff;box-sizing:border-box;display:flex;justify-content:space-between;align-items:center"><span id="rtTypeTxt" style="color:#777">— Type chunein —</span><span>🔍</span></button>
  <select id="rtType" style="display:none"><option value="">— Type chunein —</option>__OPTS__<option value="__other">Mere type ki dukaan list mein nahi hai (khud likhein)</option></select>
  <input id="rtTypeOther" maxlength="40" placeholder="Apni dukaan ka type likhein" style="display:none;margin-top:8px">
  <label>Mobile number</label><input id="rtPhone" type="tel" inputmode="numeric" maxlength="10" placeholder="10 digit mobile">
  <label>UPI ID (payment lene ke liye)</label><input id="rtUpi" placeholder="jaise: name@okaxis" autocapitalize="off" autocomplete="off">
  <label>Dukaan ka pata (optional)</label><input id="rtAddr" maxlength="120" placeholder="gaon / mohalla / shahar">
  <div class="err" id="rtErr"></div>
  <button class="go" id="rtGo">Aage badhein ›</button>
</div></div>
<script>
(function(){
  var CATSUG = __CATSUG__;
  var $ = function(id){ return document.getElementById(id); };
  function applyBrand(){
    var p = RT_PROFILE(), n = p.name || 'Mittu Associated Retailer';
    document.querySelectorAll('.rt-name').forEach(function(e){ e.textContent = p.name || 'Mittu Associated'; });
    document.querySelectorAll('.rt-name-full').forEach(function(e){ e.textContent = n; });
    document.querySelectorAll('.rt-name-up').forEach(function(e){ e.textContent = n.toUpperCase(); });
    document.querySelectorAll('.rt-upi').forEach(function(e){ e.textContent = p.upi || ''; });
    document.querySelectorAll('.rt-phone').forEach(function(e){ e.textContent = p.phone ? '+91 ' + p.phone : ''; });
    document.querySelectorAll('.rt-addr').forEach(function(e){ e.textContent = p.addr || ''; });
    var sub = document.querySelector('.tb-sub'); if(sub) sub.textContent = 'Mittu Associated Retailer';
  }
  window.rtApplyBrand = applyBrand;
  window.rtFillCatList = function(){
    var p = RT_PROFILE(), set = {}, out = [];
    (CATSUG[p.type] || []).forEach(function(c){ set[c] = 1; });
    try { (typeof getStockList === 'function' ? getStockList() : []).forEach(function(it){ if(it && it.category) set[it.category] = 1; }); } catch(e){}
    Object.keys(set).forEach(function(c){ out.push('<option value="' + c.replace(/"/g, '&quot;') + '">'); });
    var dl = $('stockCatList'); if(dl) dl.innerHTML = out.join('');
  };
  function show(prefill){
    var p = RT_PROFILE(), o = $('rtOnb');
    if(prefill){
      $('rtName').value = p.name || ''; $('rtPhone').value = p.phone || ''; $('rtUpi').value = p.upi || ''; $('rtAddr').value = p.addr || '';
      var sel = $('rtType'), has = Array.prototype.some.call(sel.options, function(x){ return x.value === p.type || x.text === p.type; });
      if(p.type && has) sel.value = p.type; else if(p.type){ sel.value = '__other'; $('rtTypeOther').style.display = 'block'; $('rtTypeOther').value = p.type; }
    }
    $('rtBack').style.display = prefill ? 'block' : 'none';
    if(window.rtSyncType) window.rtSyncType();
    o.style.display = 'flex';
  }
  $('rtBack').addEventListener('click', function(){ $('rtOnb').style.display = 'none'; $('rtErr').textContent = ''; });
  window.rtOpenProfile = function(){ show(true); };
  $('rtType').addEventListener('change', function(){ $('rtTypeOther').style.display = this.value === '__other' ? 'block' : 'none'; window.rtSyncType(); });
  // App ka apna searchable Store-type picker (phone ka dropdown nahi)
  window.rtSyncType = function(){
    var v = $('rtType').value, t = $('rtTypeTxt');
    t.textContent = !v ? '— Type chunein —' : (v === '__other' ? 'Khud likhein (list mein nahi)' : v); t.style.color = v ? '#111' : '#777';
  };
  (function(){
    var pk = document.createElement('div'); pk.id = 'rtPick';
    pk.style.cssText = 'display:none;position:fixed;inset:0;z-index:2147483100;background:rgba(0,0,0,.55);align-items:flex-end;justify-content:center';
    pk.innerHTML = '<div style="width:100%;max-width:480px;height:82vh;background:#fff;border-radius:20px 20px 0 0;display:flex;flex-direction:column;padding-bottom:env(safe-area-inset-bottom,0px)">'
      + '<div style="display:flex;align-items:center;gap:8px;padding:14px 14px 8px"><b style="flex:1;font-size:18px;color:#0d6e4e">Dukaan ka type chunein</b><button type="button" id="rtPickX" style="border:0;background:#eef3f0;border-radius:50%;width:36px;height:36px;font-size:18px">✕</button></div>'
      + '<div style="padding:0 14px 8px"><input id="rtPickQ" placeholder="🔍 Search: jaise Biryani, Mobile, Dawai…" autocomplete="off" style="width:100%;padding:12px;border:1.5px solid #cfd8e3;border-radius:12px;font-size:16px;box-sizing:border-box"></div>'
      + '<div id="rtPickList" style="flex:1;overflow:auto;padding:0 14px 14px"></div></div>';
    document.body.appendChild(pk);
    function build(q){
      q = (q || '').trim().toLowerCase(); var h = '', sel = $('rtType'), any = false;
      Array.prototype.forEach.call(sel.querySelectorAll('optgroup'), function(g){
        var items = Array.prototype.filter.call(g.querySelectorAll('option'), function(o){ return !q || o.textContent.toLowerCase().indexOf(q) > -1 || g.label.toLowerCase().indexOf(q) > -1; });
        if(!items.length) return; any = true;
        h += '<div style="font-weight:800;color:#0d6e4e;font-size:13px;margin:12px 0 4px">' + g.label + '</div>' + items.map(function(o){
          var on = sel.value === o.textContent;
          return '<div data-v="' + o.textContent.replace(/"/g, '&quot;') + '" style="padding:13px 12px;border-radius:12px;margin:3px 0;font-size:16px;background:' + (on ? '#e3f6ec' : '#f6f8f7') + ';font-weight:' + (on ? '800' : '500') + '">' + o.textContent + (on ? ' ✓' : '') + '</div>';
        }).join('');
      });
      var oth = !q || 'khud likhein list mein nahi other'.indexOf(q) > -1;
      if(oth){ any = true; h += '<div data-v="__other" style="padding:13px 12px;border-radius:12px;margin:12px 0 3px;font-size:16px;background:#fff6e0;font-weight:700">✏️ Mere type ki dukaan list mein nahi hai (khud likhein)</div>'; }
      if(!any) h = '<div style="padding:24px;text-align:center;color:#777">Kuch nahi mila</div>';
      $('rtPickList').innerHTML = h;
    }
    $('rtTypeBtn').addEventListener('click', function(){ $('rtPickQ').value = ''; build(''); pk.style.display = 'flex'; });
    $('rtPickX').addEventListener('click', function(){ pk.style.display = 'none'; });
    pk.addEventListener('click', function(e){ if(e.target === pk) pk.style.display = 'none'; });
    $('rtPickQ').addEventListener('input', function(){ build(this.value); });
    $('rtPickList').addEventListener('click', function(e){
      var d = e.target.closest ? e.target.closest('[data-v]') : null; if(!d) return;
      $('rtType').value = d.getAttribute('data-v'); $('rtType').dispatchEvent(new Event('change')); pk.style.display = 'none';
      if(d.getAttribute('data-v') === '__other') setTimeout(function(){ $('rtTypeOther').focus(); }, 50);
    });
  })();
  $('rtPhone').addEventListener('input', function(){ this.value = this.value.replace(/\\D/g, '').slice(0, 10); });
  $('rtGo').addEventListener('click', function(){
    var name = $('rtName').value.trim(), sel = $('rtType').value, type = sel === '__other' ? $('rtTypeOther').value.trim() : sel,
        phone = $('rtPhone').value.replace(/\\D/g, ''), upi = $('rtUpi').value.trim(), addr = $('rtAddr').value.trim(), err = $('rtErr');
    if(name.length < 2){ err.textContent = 'Dukaan ka naam likhein.'; return; }
    if(!type){ err.textContent = 'Dukaan ka type chunein (ya khud likhein).'; return; }
    if(!/^[6-9]\\d{9}$/.test(phone)){ err.textContent = 'Sahi 10 digit mobile number likhein.'; return; }
    if(!/^[A-Za-z0-9._-]{2,}@[A-Za-z][A-Za-z0-9]{1,}$/.test(upi)){ err.textContent = 'UPI ID sahi likhein (jaise name@okaxis).'; return; }
    try { localStorage.setItem('retailer_profile', JSON.stringify({ name: name, type: type, phone: phone, upi: upi, addr: addr })); } catch(e){}
    $('rtOnb').style.display = 'none'; err.textContent = '';
    applyBrand();
    try { if(typeof window.rtPublishIndex === 'function') window.rtPublishIndex(); } catch(e){}
  });
  document.addEventListener('DOMContentLoaded', function(){ applyBrand(); });
  if(!RT_PROFILE().name) show(false); else applyBrand();
  setTimeout(applyBrand, 800);
})();
</script>
<style>
/* Retailer app: display/delivery/staff wale features yahan nahi */
button[onclick="sendListToStaff()"],.rt-hide{display:none !important}
</style>
'''
RUNTIME = RUNTIME.replace('__OPTS__', opts).replace('__CATSUG__', json.dumps(CATSUG, ensure_ascii=False))
# WhatsApp bill (online order): saman ready + delivery partner ki jaankari (sirf retailer app)
s = s.replace("m += `— ${RT_NAME()}`;", "if(window._billOrder){ const dn = ((document.getElementById('dpName') || {}).value || '').trim(), dp = ((document.getElementById('dpPhone') || {}).value || '').trim(); m += `✅ *Aapka saman ready hai!*\\n`; if(dn || dp) m += `🛵 Delivery Partner: *${dn || 'Delivery Partner'}*${dp ? ' (📞 ' + dp + ')' : ''} jaldi aapke paas pahunchega.\\n\\n`; else m += `\\n`; }\n  m += `— ${RT_NAME()}`;", 1)
# Delivery partner (retailer ke liye): staff display ki jagah seedha delivery partner ke app par jaata hai
rep("window._billOrder ? ' Thermal Print + Staff ko Order List' : ' Print Bill Directly on Thermal Printer'", "window._billOrder ? ' Thermal Print + Delivery Partner ko Bhejein' : ' Print Bill Directly on Thermal Printer'")
rep('<span class="ai-bill-spark">🧾</span> Staff ko Saman List Bhejein + Bill Print', '<span class="ai-bill-spark">🧾</span> Delivery Partner ko Bhejein + Bill Print')
rep("alert('✅ Online order ki saman list Mittu Staff Display par bhej di gayi hai.');", "alert('✅ Order Delivery Partner ke app par bhej diya gaya hai.');")
s = s.replace("Mittu Staff Display se connection abhi available nahi hai.", "Delivery se connection abhi available nahi hai.")
# Fix Amount DQR: retailer ke apne DQR Retailer display par (mobile number se jud-ta hai)
rep("const billRef = ref(fbDb, 'currentBill');", "const billRefNow = () => ref(fbDb, 'retailerDisplay/' + ((typeof RT_PROFILE === 'function' && RT_PROFILE().phone) || '_none') + '/currentBill');")
s = s.replace("update(billRef, { billNo, amount, upiUrl, status: 'pending', ts: Date.now() })", "update(billRefNow(), { billNo, amount, upiUrl, shopName: RT_NAME(), status: 'pending', ts: Date.now() })")
s = s.replace("update(billRef, { status: 'paid', ts: Date.now() })", "update(billRefNow(), { status: 'paid', ts: Date.now() })")
s = s.replace("remove(billRef)", "remove(billRefNow())")
assert 'billRef,' not in s and 'billRef)' not in s
s = s.replace("alert('Mittu DQR Display se connection abhi available nahi hai.');", "alert('DQR Retailer display se connection abhi available nahi hai.');")
s = s.replace("✅ Mittu DQR Display par QR bhej diya", "✅ DQR Retailer display par QR bhej diya")
# customer review (owner ka) retailer app mein nahi
rep("const customerReqRef = ref(fbDb, 'customerRequest');", "const customerReqRef = ref(fbDb, 'retailerDisplay/_none/customerRequest');")
# delivery jobs: retailer ka apna path (owner ke Staff Display mein na mile)
rep("""    const key = String(payload.orderId || '').replace(/[.#$\\[\\]\\/]/g, '_');
    const newRef = key ? ref(fbDb, 'staffOrders/' + key) : push(staffOrdersRef);
    window.__lastStaffPath = 'staffOrders/' + (key || newRef.key);
    return set(newRef, Object.assign({}, payload, { checked: {}, ts: Date.now() }))""",
    """    const ph = String((payload.deliveryPartner || {}).phone || '').replace(/\\D/g, '').slice(-10);
    if(!ph) return Promise.resolve();
    const key = String(payload.orderId || '').replace(/[.#$\\[\\]\\/]/g, '_') || push(staffOrdersRef).key;
    window.__lastStaffPath = 'deliveryJobs/' + ph + '/' + key;
    return set(ref(fbDb, 'deliveryJobs/' + ph + '/' + key), Object.assign({}, payload, { noChecklist: true, shop: { name: RT_NAME(), phone: RT_PROFILE().phone || '' }, ts: Date.now() }))""")
# login screen branding + Google error ka madad-message
s = s.replace('<h1 class="login-title">Welcome to Mittu Billing</h1>', '<h1 class="login-title">Welcome to Mittu Associated Retailer</h1>')
s = s.replace("errorEl.textContent = 'Login nahi ho paya: ' + (err?.message || 'Unknown error');", "errorEl.textContent = 'Login nahi ho paya: ' + (err?.message || 'Unknown error') + (/credential/i.test(err?.message || '') ? ' — Google login abhi taiyaar nahi hai, neeche Email aur password se login karein (naya account apne aap ban jayega).' : '');")
# drawer: Shop profile item (retailer profile edit)
GEAR = '<svg class="pro-icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>'
rep('<div class="drawer-recents-title">Recents</div>', '<div class="drawer-item" onclick="closeDrawer(); rtOpenProfile();" style="border-top:1px solid #eee;"><span class="drawer-icon">' + GEAR + '</span> Dukaan ki jaankari</div>\n    <div class="drawer-recents-title">Recents</div>')
# retailer app mein Mittu wholesale splash nahi
rep("(function(){\n  try { if(!(window.Capacitor", "(function(){\n  return;\n  try { if(!(window.Capacitor")
# onboarding sabse upar (login se bhi pehle)
rep('<body>', '<body>' + RUNTIME, 1)

out = root / 'retailer' / 'index.html'
out.write_text(s)
left = [m.group(0)[:80] for m in re.finditer(r'.{0,30}(Mittu Wholesal|MITTU WHOLESAL|7303714309@|9540125307|Rangra).{0,30}', s)]
print('baaki (check):', left)

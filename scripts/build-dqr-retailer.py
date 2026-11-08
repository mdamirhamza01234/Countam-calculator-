#!/usr/bin/env python3
"""DQR Retailer display = dqr-display ka retailer version (retailer ke mobile number ke hisaab se QR aata hai).
    python3 scripts/build-dqr-retailer.py"""
import pathlib, json, shutil
root = pathlib.Path(__file__).resolve().parent.parent
s = (root / 'dqr-display' / 'index.html').read_text()
def rep(old, new):
    global s
    assert old in s, old[:60]
    s = s.replace(old, new, 1)
rep('<title>Mittu DQR Display</title>', '<title>DQR Retailer</title>')
rep('<meta name="theme-color" content="#16325c">', '<meta name="theme-color" content="#0d6e4e">')
rep('        🛒 MITTU WHOLESALER &amp; RETAILER <br>', '        <span id="shopNameW">🛒 DQR Retailer</span> <br>')
rep('<div class="shop-name">MITTU WHOLESALER &amp; RETAILER</div>', '<div class="shop-name" id="shopNameQ">DQR Retailer</div>')
rep('<p style="color:#7f8c8d; font-size:15px; font-weight: bold; margin-top: 15px;">Scan &amp; Pay via any UPI App</p>',
    '<p style="color:#7f8c8d; font-size:15px; font-weight: bold; margin-top: 15px;">Scan &amp; Pay via any UPI App</p>\n        <p id="upiTxt" style="color:#16325c; font-size:14px; margin-top:4px;"></p>')
SETUP = '''
    <style>
      #setup{position:fixed;inset:0;z-index:99999;background:linear-gradient(160deg,#0b5a3f,#1b9d6a);display:none;align-items:center;justify-content:center;padding:18px;overflow:auto}
      #setup .card{background:#fff;border-radius:20px;padding:24px 18px;width:min(94vw,400px);box-shadow:0 18px 60px rgba(0,0,0,.35)}
      #setup h2{margin:0 0 4px;color:#0d6e4e}#setup p{margin:0 0 12px;color:#555;font-size:13.5px}
      #setup label{display:block;font-weight:700;font-size:13px;margin:12px 0 5px;color:#333}
      #setup input{width:100%;padding:14px 12px;border:1.5px solid #cfd8e3;border-radius:12px;font-size:17px;box-sizing:border-box}
      #setup button{margin-top:18px;width:100%;padding:15px;border:0;border-radius:13px;background:#0d6e4e;color:#fff;font-size:17px;font-weight:800}
      #setup .err{color:#b3261e;font-size:13px;min-height:16px;margin-top:8px}
      #chg{position:fixed;right:8px;bottom:8px;z-index:50;background:rgba(0,0,0,.08);border:0;color:#555;font-size:11px;border-radius:8px;padding:4px 8px}
    </style>
    <div id="setup"><div class="card">
      <h2>🛒 DQR Retailer</h2>
      <p>Apna mobile number aur UPI ID likhein. Yahi number Retailer Billing app ki dukaan ke profile mein hona chahiye — tabhi Fix Amount QR is display par aayega.</p>
      <label>Retailer ka mobile number</label><input id="sPhone" type="tel" inputmode="numeric" maxlength="10" placeholder="10 digit mobile">
      <label>UPI ID</label><input id="sUpi" placeholder="jaise: name@okaxis" autocapitalize="off" autocomplete="off">
      <div class="err" id="sErr"></div>
      <button id="sGo">Next ›</button>
    </div></div>
    <button id="chg">⚙ Number / UPI badlein</button>
'''
rep('<body>\n', '<body>\n' + SETUP)
rep("        const dbRef = ref(database, 'currentBill/');\n        function startListening(){\n        onValue(dbRef, (snapshot) => {",
"""        let prof = {};
        try { prof = JSON.parse(localStorage.getItem('dqr_retailer') || '{}') || {}; } catch(e){}
        const $ = id => document.getElementById(id);
        function applyName(){
            const n = (prof.shopName || 'DQR Retailer');
            $('shopNameW').textContent = '🛒 ' + n; $('shopNameQ').textContent = n;
            $('upiTxt').textContent = prof.upi ? 'UPI: ' + prof.upi : '';
        }
        applyName();
        function showSetup(){ $('sPhone').value = prof.phone || ''; $('sUpi').value = prof.upi || ''; $('setup').style.display = 'flex'; }
        $('chg').onclick = showSetup;
        $('sPhone').oninput = function(){ this.value = this.value.replace(/\\D/g, '').slice(0, 10); };
        let unsub = null;
        function startListening(){
        if (unsub) { try { unsub(); } catch(e){} unsub = null; }
        if (!prof.phone) return;
        const dbRef = ref(database, 'retailerDisplay/' + prof.phone + '/currentBill');
        unsub = onValue(dbRef, (snapshot) => {""")
rep("                lastStatus = data.status || 'pending';", "                lastStatus = data.status || 'pending';\n                if (data.shopName && data.shopName !== prof.shopName) { prof.shopName = data.shopName; try { localStorage.setItem('dqr_retailer', JSON.stringify(prof)); } catch(e){} applyName(); }")
rep("""        let started = false;
        onAuthStateChanged(auth, (user) => { if (user && !started) { started = true; startListening(); } });
        signInAnonymously(auth).catch((err) => {
            console.warn('Anonymous sign-in failed, trying without login:', err);
            if (!started) { started = true; startListening(); }
        });""", """        let started = false, authed = false;
        $('sGo').onclick = () => {
            const ph = $('sPhone').value.replace(/\\D/g, ''), up = $('sUpi').value.trim();
            if (!/^[6-9]\\d{9}$/.test(ph)) { $('sErr').textContent = 'Sahi 10 digit mobile number likhein.'; return; }
            if (!/^[A-Za-z0-9._-]{2,}@[A-Za-z][A-Za-z0-9]{1,}$/.test(up)) { $('sErr').textContent = 'UPI ID sahi likhein (jaise name@okaxis).'; return; }
            if (prof.phone !== ph) prof.shopName = '';
            prof.phone = ph; prof.upi = up;
            try { localStorage.setItem('dqr_retailer', JSON.stringify(prof)); } catch(e){}
            $('sErr').textContent = ''; $('setup').style.display = 'none'; applyName(); showScreen('welcome');
            if (authed) startListening();
        };
        if (!prof.phone) showSetup();
        onAuthStateChanged(auth, (user) => { if (user) { authed = true; if (!started) { started = true; startListening(); } } });
        signInAnonymously(auth).catch((err) => {
            console.warn('Anonymous sign-in failed, trying without login:', err);
            authed = true; if (!started) { started = true; startListening(); }
        });""")
rep("welcomeScreen.innerHTML = '🛒 MITTU WHOLESALER &amp; RETAILER<br>", "welcomeScreen.innerHTML = '🛒 DQR Retailer<br>")
out = root / 'dqr-retailer'; out.mkdir(exist_ok=True)
(out / 'index.html').write_text(s)
m = json.loads((root / 'dqr-display' / 'manifest.webmanifest').read_text())
m.update({'name': 'DQR Retailer', 'short_name': 'DQR Retailer', 'theme_color': '#0d6e4e', 'background_color': '#0d6e4e'})
(out / 'manifest.webmanifest').write_text(json.dumps(m, indent=2))
shutil.copy(root / 'retailer' / 'icon-192.png', out / 'icon-192.png'); shutil.copy(root / 'retailer' / 'icon-512.png', out / 'icon-512.png')
print('ok')

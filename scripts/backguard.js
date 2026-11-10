/* BACKGUARD: Android side-swipe / back button se sirf ek screen peeche jaye, poora app band na ho. */
(function(){
  if(window.__backGuard) return; window.__backGuard = 1;
  var SKIP = {loginScreen:1, setPasswordOverlay:1, rtOnb:1};
  function vis(el){
    if(!el) return false;
    var r = el.getBoundingClientRect(); if(r.width < 2 || r.height < 2) return false;
    var cs = getComputedStyle(el);
    return cs.display !== 'none' && cs.visibility !== 'hidden' && cs.opacity !== '0';
  }
  function zi(el){ var z = parseInt(getComputedStyle(el).zIndex, 10); return isNaN(z) ? 0 : z; }
  var SEL = '[id$="Overlay"],[id$="Modal"],[id$="Sheet"],[id$="Screen"],[id$="Viewer"],[id$="Popup"],[id$="Dialog"],.page.show,.modal.show,#donePage.show,#drawerPanel.open';
  var BTN = '[data-back],[data-close],.close,.back,[aria-label*="ack" i],[aria-label*="lose" i],[id*="Back" i],[id*="Close" i],[id*="Cancel" i],[onclick*="close" i],[onclick*="hide" i],[onclick*="back" i],.stock-modal-cancel,.ph button';
  function closeEl(el){
    if(el.id === 'drawerPanel' && typeof window.closeDrawer === 'function'){ window.closeDrawer(); return true; }
    var b = el.querySelector(BTN);
    if(b){ try{ b.click(); }catch(e){} }
    setTimeout(function(){
      if(vis(el) && getComputedStyle(el).position !== 'static'){
        el.classList.remove('show','open','active'); el.style.display = 'none';
      }
    }, 150);
    return true;
  }
  function closeTop(){
    if(typeof window.__bgExtra === 'function'){ try{ if(window.__bgExtra()) return true; }catch(e){} }
    var best = null, bz = -1e9, bi = -1;
    var list = document.querySelectorAll(SEL);
    for(var i = 0; i < list.length; i++){
      var el = list[i];
      if(SKIP[el.id] || !vis(el)) continue;
      if(el.id === 'drawerOverlay') continue;
      var pos = getComputedStyle(el).position;
      if(pos !== 'fixed' && pos !== 'absolute') continue;
      var z = zi(el);
      if(z >= bz){ bz = z; best = el; bi = i; }
    }
    if(best) return closeEl(best);
    if(typeof window.__bgHome === 'function'){ try{ if(window.__bgHome()) return true; }catch(e){} }
    return false;
  }
  var exitArmed = false;
  function exitToast(){
    if(!document.body) return;
    toast('App band karne ke liye dobara back dabayein');
  }
  function toast(t){
    var d = document.createElement('div');
    d.textContent = t;
    d.style.cssText = 'position:fixed;left:50%;bottom:90px;transform:translateX(-50%);background:rgba(0,0,0,.82);color:#fff;padding:10px 16px;border-radius:20px;font:600 13px sans-serif;z-index:2147483647;pointer-events:none';
    document.body.appendChild(d); setTimeout(function(){ d.remove(); }, 1800);
  }
  /* 1) Native (Capacitor App plugin) - sabse pakka tareeka */
  var nativeOn = false;
  function tryNative(){
    if(nativeOn) return true;
    var A = window.Capacitor && window.Capacitor.Plugins && window.Capacitor.Plugins.App;
    if(!A || typeof A.addListener !== 'function') return false;
    nativeOn = true;
    A.addListener('backButton', function(){
      if(closeTop()) return;
      if(exitArmed){ try{ A.exitApp(); }catch(e){} return; }
      exitArmed = true; exitToast(); setTimeout(function(){ exitArmed = false; }, 1800);
    });
    return true;
  }
  /* 2) Fallback: browser history (user touch ke baad hi push - warna Android WebView use skip kar deta hai) */
  var armedOnce = false;
  function arm(){ try{ history.pushState({bg: 1}, ''); }catch(e){} }
  function firstTouch(){
    if(armedOnce || nativeOn) return; armedOnce = true;
    try{ history.replaceState({bg: 0}, ''); }catch(e){}
    arm();
  }
  ['touchstart', 'pointerdown', 'click', 'keydown'].forEach(function(ev){ window.addEventListener(ev, firstTouch, {capture: true, once: true, passive: true}); });
  window.addEventListener('popstate', function(){
    if(nativeOn) return;
    if(closeTop()){ arm(); return; }
    if(!exitArmed){
      exitArmed = true; exitToast();
      setTimeout(function(){ exitArmed = false; arm(); }, 1800);
    }
  });
  if(!tryNative()){ var n = 0, iv = setInterval(function(){ if(tryNative() || ++n > 10) clearInterval(iv); }, 500); }
})();

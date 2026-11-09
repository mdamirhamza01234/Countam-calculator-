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
  function arm(){ try{ history.pushState({bg: 1}, ''); }catch(e){} }
  function toast(t){
    var d = document.createElement('div');
    d.textContent = t;
    d.style.cssText = 'position:fixed;left:50%;bottom:90px;transform:translateX(-50%);background:rgba(0,0,0,.82);color:#fff;padding:10px 16px;border-radius:20px;font:600 13px sans-serif;z-index:2147483647;pointer-events:none';
    document.body.appendChild(d); setTimeout(function(){ d.remove(); }, 1800);
  }
  try{ history.replaceState({bg: 0}, ''); }catch(e){}
  arm();
  window.addEventListener('popstate', function(){
    if(closeTop()){ arm(); return; }
    if(!window.__bgExit){
      window.__bgExit = 1; toast('App band karne ke liye dobara back dabayein');
      setTimeout(function(){ window.__bgExit = 0; arm(); }, 1800);   // 1.8s baad dobara guard lagao
    }
  });
})();

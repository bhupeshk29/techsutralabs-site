document.documentElement.classList.add("js");
(function(){
  var header=document.querySelector('.site-header'),t=document.querySelector('.nav-toggle'),l=document.getElementById('primary-nav');
  function setMenu(open){l.classList.toggle('open',open);t.setAttribute('aria-expanded',open);t.setAttribute('aria-label',open?'Close menu':'Open menu');}
  if(t&&l){
    t.addEventListener('click',function(){setMenu(!l.classList.contains('open'))});
    l.addEventListener('click',function(e){if(e.target.closest('a'))setMenu(false)});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&l.classList.contains('open')){setMenu(false);t.focus();}});
  }
  var path=location.pathname.split('/').pop()||'index.html';
  document.querySelectorAll('.nav-links a:not(.btn)').forEach(function(a){if(a.getAttribute('href')===path)a.setAttribute('aria-current','page')});
  if(header){var onS=function(){header.classList.toggle('scrolled',window.scrollY>8)};window.addEventListener('scroll',onS,{passive:true});onS();}
  var y=document.getElementById('year');if(y)y.textContent=new Date().getFullYear();
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.08});
    document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});
  } else document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')});

  // Copy-email buttons
  document.querySelectorAll('[data-copy]').forEach(function(b){
    b.addEventListener('click',function(){
      var v=b.getAttribute('data-copy'),done=function(){var o=b.textContent;b.textContent='Copied';setTimeout(function(){b.textContent=o},1600)};
      if(navigator.clipboard)navigator.clipboard.writeText(v).then(done,function(){});
    });
  });

  // Contact form: validates, then opens the visitor's mail app with the enquiry pre-filled (works on any static host).
  var f=document.getElementById('contact-form');
  if(f){
    var k=new URLSearchParams(location.search).get('topic');
    if(k){var o=f.querySelector('#topic option[data-key="'+k+'"]');if(o)o.selected=true;}
    f.addEventListener('submit',function(e){
      e.preventDefault();
      if(!f.checkValidity()){f.reportValidity();return;}
      if(f.website&&f.website.value)return; // honeypot
      var d=new FormData(f),to=f.dataset.to;
      var body='Name: '+d.get('name')+'\nEmail: '+d.get('email')+'\nPhone: '+(d.get('phone')||'-')+'\nCompany: '+(d.get('company')||'-')+'\nInterested in: '+d.get('topic')+'\n\n'+d.get('message');
      location.href='mailto:'+to+'?subject='+encodeURIComponent('Website enquiry: '+d.get('topic')+' - '+d.get('name'))+'&body='+encodeURIComponent(body);
      document.getElementById('form-status').innerHTML='Your email app should now open with your message ready to send. If nothing happens, email us directly at <a href="mailto:'+to+'">'+to+'</a>.';
    });
  }
})();

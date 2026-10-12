(function(){
  var hdr=document.querySelector('header.site');
  var burger=document.querySelector('.burger');
  if(burger){burger.addEventListener('click',function(){
    var open=hdr.classList.toggle('nav-open');
    burger.setAttribute('aria-expanded',open?'true':'false');
  });}
  var forms=document.querySelectorAll('form.req');
  for(var i=0;i<forms.length;i++){forms[i].addEventListener('submit',function(e){
    e.preventDefault();
    var d=e.target.querySelector('.done'); if(d) d.hidden=false;
  });}
})();

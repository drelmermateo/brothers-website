
document.addEventListener('DOMContentLoaded', function(){
  document.querySelectorAll('.platform-btn').forEach(function(btn){
    btn.addEventListener('click', function(e){
      e.preventDefault();
      btn.classList.add('loading');
      var icon = btn.querySelector('i');
      if(icon) icon.style.opacity = '0.2';
      setTimeout(function(){ window.location = btn.getAttribute('href'); }, 250);
    });
  });
  document.querySelectorAll('form').forEach(function(form){
    form.addEventListener('submit', function(e){
      var btn = form.querySelector('button[type=submit]');
      if(btn){ btn.classList.add('loading'); }
    });
  });
});

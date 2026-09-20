document.querySelectorAll('.case-nav a').forEach(a=>a.addEventListener('click',()=>{document.querySelectorAll('.case-nav a').forEach(x=>x.removeAttribute('aria-current'));a.setAttribute('aria-current','location')}));

const workMenu = document.querySelector('.work-menu');
if (workMenu) {
  document.addEventListener('click', event => {
    if (!workMenu.contains(event.target)) workMenu.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && workMenu.open) {
      workMenu.open = false;
      workMenu.querySelector('summary').focus();
    }
  });
  workMenu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    workMenu.open = false;
  }));
}

function startLoading(){
  const btn = document.querySelector('.btn');
  if(btn){
    btn.disabled = true;
    const original = btn.textContent;
    btn.dataset.original = original;
    btn.textContent = 'Generating...';
  }
  return true;
}

window.addEventListener('scroll', function() {
  var scrollDistance = window.pageYOffset;

  if (scrollDistance > 100) {
    document.querySelector('.scroll-to-top').style.display = 'block';
  } else {
    document.querySelector('.scroll-to-top').style.display = 'none';
  }
});

document.querySelector('.scroll-to-top').addEventListener('click', function(e) {
  e.preventDefault();
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
});

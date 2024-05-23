var swiper = null

function initSwiper() {
  let slides = null;
  if (window.innerWidth > 1200) {
    slides = 2
  } else {
    slides = 1
  }
  if (swiper !== null) {
    swiper.destroy()
  }
  if (window.innerWidth > 480) {
    swiper = new Swiper('.swiper', {
      // Optional parameters
      direction: 'horizontal',
      loop: true,
      slidesPerView: slides,
      spaceBetween: 32,
    
      // Navigation arrows
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
    });
  } else {
    swiper = new Swiper('.swiper', {
      // Optional parameters
      direction: 'horizontal',
      loop: true,
      slidesPerView: slides,
      spaceBetween: 32,
    
      // Navigation arrows
      pagination: {
        el: '.swiper-pagination'
      },
    });
  }
}

window.onload = initSwiper
window.onresize = initSwiper
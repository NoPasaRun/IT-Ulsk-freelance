var swiper = null

function initSwiper() {
  let slides = null;
  if (window.innerWidth > 1000) {
    slides = 3
  } else if (window.innerWidth > 650) {
    slides = 2
  } else {
    slides = 1
  }
  if (swiper !== null) {
    swiper.destroy()
  }
  swiper = new Swiper('.swiper', {
    // Optional parameters
    direction: 'horizontal',
    loop: true,
    slidesPerView: slides,
    spaceBetween: 27,
  
    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  });
}

window.onload = initSwiper
window.onresize = initSwiper
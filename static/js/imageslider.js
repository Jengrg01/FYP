let items = document.querySelectorAll('.slider .list .item');
let thumbnails = document.querySelectorAll('.slider .thumbnail .item');
let next = document.getElementById('next');
let prev = document.getElementById('prev');

let countItem = items.length;
let itemActive = 0;

function showSlider() {
  document.querySelector('.slider .list .item.active').classList.remove('active');
  document.querySelector('.slider .thumbnail .item.active').classList.remove('active');

  items[itemActive].classList.add('active');
  thumbnails[itemActive].classList.add('active');

  clearInterval(refreshInterval);
  refreshInterval = setInterval(() => {
    next.click();
  }, 3000);
}

next.onclick = () => {
  itemActive = (itemActive + 1) % countItem;
  showSlider();
};

prev.onclick = () => {
  itemActive = (itemActive - 1 + countItem) % countItem;
  showSlider();
};

// Thumbnails click
thumbnails.forEach((thumb, index) => {
  thumb.addEventListener('click', () => {
    itemActive = index;
    showSlider();
  });
});

// Auto slide
let refreshInterval = setInterval(() => {
  next.click();
}, 3000);

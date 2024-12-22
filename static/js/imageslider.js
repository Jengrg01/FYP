let items = document.querySelectorAll('.slider .list .item');
let next = document.getElementById('next');
let prev = document.getElementById('prev');
let thumbnails = document.querySelectorAll('.thumbnail .item');

//configuring param

let countItem = items.length;
let itemActive = 0;
//event next click
next.onclick = function(){
    itemActive = itemActive +1;
    if(itemActive>=countItem){
        itemActive=0;
    }
    showSlider();
}
//previous button
prev.onclick = function(){
    itemActive = itemActive-1;
    if(itemActive < 0){
        itemActive = countItem-1;
    }
    showSlider();
}

//auto slide run
let refreshInterval = setInterval(()=>{
    next.click();
},3000)

function showSlider(){
    //remove old item active
    let itemActiveOld = document.querySelector('.slider .list .item.active');
    let thumbnailActiveOld = document.querySelector('.thumbnail .item.active');
    itemActiveOld.classList.remove('active');
    thumbnailActiveOld.classList.remove('active');
    // new active item
    items[itemActive].classList.add('active');
    thumbnails[itemActive].classList.add('active');
    //to clear the time on run slider
    clearInterval(refreshInterval);
    refreshInterval=setInterval(()=>{
        next.click();
    },3000)
}

//clicking thumbnails

thumbnails.forEach((thumbnail, index) =>{
    thumbnail.addEventListener('click',()=>{
        itemActive = index;
        showSlider();
    })
})
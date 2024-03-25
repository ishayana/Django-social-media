function changeImage() {
    var image = document.getElementById('postlike');
    // Change the image source to the new image
    image.src = "{% static 'userprofile/img/post/liked.png' %}";
}


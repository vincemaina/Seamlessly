var background = document.getElementById('page-stretcher')

window.onscroll = function(ev) {
    if ((window.innerHeight + Math.ceil(window.pageYOffset + 1)) >= document.body.offsetHeight - 500) {
        let oldHeight = background.style.height
        let newHeight = parseInt(oldHeight) + 5000 + 'px;'
        var oldStyle = document.getElementById('page-stretcher').getAttribute("style")

        document.getElementById('page-stretcher').setAttribute("style",`height:${newHeight}; width: 100vw;`);
    }
};

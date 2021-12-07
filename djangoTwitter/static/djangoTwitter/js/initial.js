
// function hideLoader() {
//   $('#loading').hide();
//   masonry_go();
// };
// $(document).ready(function () {
//   setTimeout(function () { masonry_go(); }, 1000);
// });
$(window).resize(function () {
  // jQuery
  masonry_go();;
});
function masonry_go() {
  $('.grid').masonry({
    // options
    itemSelector: '.tweets',
    columnWidth: '.sizer',
    percentPosition: true,
  });
}
setTimeout(()=>{
  masonry_go();
}, 1000);

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {  masonry_go(); };
masonry_go();

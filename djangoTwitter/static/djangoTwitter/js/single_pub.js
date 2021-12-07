$(".menu").click(function(e){
  // $("#sidebar").removeClass('toc')
  $(".toc").toggleClass("show-menu")
})

var path = location.href;
var slug = path.split('/')
slug.pop()
slug = slug.at(-1)
jQuery(function($) {
 $('ul a').each(function() {
  if (this.href === path) {
   $(this).addClass('active');
  }
 });
});


$('#add-comment').click(function (e) {
  e.preventDefault()
  var comment = document.getElementById("comment").value
  $.ajax({
    url: '/add-comment/',
    method: 'POST',
    data: {
        comment :comment,
        slug:slug
    },
    success: function (e) {
        document.getElementById("comment").value=''
      console.log('sent')
    }
  })
})

$(document).ready(function(){
  $("button").click(function(){
    $("p").toggleClass("main");
  });
});

$(document).ready(function(){
    $('.content').find('img').each(function(){this.style.width='100%';this.style.height='100%'})
})

// window.dataLayer = window.dataLayer || [];
// function gtag() { dataLayer.push(arguments); }
// gtag('js', new Date());

// gtag('config', 'G-MBHHXFH1MX');


// var height = $('.footer-sec').css('height')
// console.log(height)
// $('body').css('padding-bottom', height)
// $(window).on("resize", function () {
//   explore = $('.footer-sec').css("height");
//   $('body').css('padding-bottom', explore)
// });
// $('#send').click(function (e) {
//   e.preventDefault()
//   var firstname = document.getElementById("form_name").value
//   var lastname = document.getElementById("form_lastname").value
//   var email = document.getElementById("form_email").value
//   var message = document.getElementById("form_message").value
//   $.ajax({
//     url: '/sendmessage/',
//     method: 'POST',
//     data: {
//       name: firstname,
//       surname: lastname,
//       email: email,
//       message: message,
//     },
//     success: function (e) {
//       $('#send').remove()
//       $('.alert-success').removeClass('d-none')
//       document.getElementById("form_name").value = ''
//       document.getElementById("form_lastname").value = ''
//       document.getElementById("form_email").value = ''
//       document.getElementById("form_message").value = ''
//     }
//   })
// })


function kFormatter(num1) {
  var num = parseInt(num1);
  return Math.abs(num) > 999 ? Math.sign(num)*((Math.abs(num)/1000).toFixed(1)) + 'k' : Math.sign(num)*Math.abs(num)
}
window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', 'G-MBHHXFH1MX');
// var height = $('.footer-sec').css('height')
// $('body').css('padding-bottom', height)
// $(window).on("resize", function () {
//   explore = $('.footer-sec').css("height");
//   console.log(explore)
//   $('body').css('padding-bottom', explore)
// });
$('#send').click(function (e) {
  e.preventDefault()
  var firstname = document.getElementById("form_name").value
  var lastname = document.getElementById("form_lastname").value
  var email = document.getElementById("form_email").value
  var message = document.getElementById("form_message").value
  $.ajax({
    url: '/sendmessage/',
    method: 'POST',
    data: {
      name: firstname,
      surname: lastname,
      email: email,
      message: message,
    },
    success: function (e) {
      $('#send').remove()
      $('.alert-success').removeClass('d-none')
      document.getElementById("form_name").value = ''
      document.getElementById("form_lastname").value = ''
      document.getElementById("form_email").value = ''
      document.getElementById("form_message").value = ''
    }
  })
})
//Get the button
var mybutton = document.getElementById("backToTop");
mybutton.addEventListener('click', function () {
  topFunction();
})
function scrollFunction() {
  if (document.body.scrollTop > 400 || document.documentElement.scrollTop > 400) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}
window.onscroll =    function  ()  {masonry_go(); scrollFunction();}
// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}
document.querySelectorAll(".notify-card").forEach(element => {
  element.addEventListener('click', (e) => {
    e.preventDefault();
    $.ajax({
      url: '/inbox/notifications/mark-all-as-read/',
      method: 'GET',
      success: function (e) {
        window.location.replace('/publications')
      }
    })
  })
});
document.addEventListener("DOMContentLoaded", function () {
  var lazyloadImages;
  if ("IntersectionObserver" in window) {
    lazyloadImages = document.querySelectorAll(".lazy");
    var imageObserver = new IntersectionObserver(function (entries, observer) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var image = entry.target;
          image.src = image.dataset.src;
          image.classList.remove("lazy");
          imageObserver.unobserve(image);
        }
      });
    });
    lazyloadImages.forEach(function (image) {
      imageObserver.observe(image);
    });
  } else {
    var lazyloadThrottleTimeout;
    lazyloadImages = document.querySelectorAll(".lazy");
    function lazyload() {
      if (lazyloadThrottleTimeout) {
        clearTimeout(lazyloadThrottleTimeout);
      }
      lazyloadThrottleTimeout = setTimeout(function () {
        var scrollTop = window.pageYOffset;
        lazyloadImages.forEach(function (img) {
          if (img.offsetTop < (window.innerHeight + scrollTop)) {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
          }
        });
        if (lazyloadImages.length == 0) {
          document.removeEventListener("scroll", lazyload);
          window.removeEventListener("resize", lazyload);
          window.removeEventListener("orientationChange", lazyload);
        }
      }, 20);
    }
    document.addEventListener("scroll", lazyload);
    window.addEventListener("resize", lazyload);
    window.addEventListener("orientationChange", lazyload);
  }
})
let cookies = localStorage.getItem('cookies');
if (cookies) {
  $(".cookiealert").hide();
}
$(".acceptcookies").click(() => {
  localStorage.setItem('cookies', true);
  $(".cookiealert").hide();
})



$("#inputGroupSelect04").on("change",(e)=>{
    $(".tweets").each(function(index){
    if ($( this ).attr('country') !== selected){
      $(this).removeClass('country-filter')
    }
  })
  var selected = $('#inputGroupSelect04').find(":selected").text();
  $(".tweets").each(function(index){
    if(selected=="All Countries"){
      $(".tweets").each(function(index){
        if ($( this ).attr('country') !== selected){
        $(this).removeClass('country-filter')
        }
      })
    }
    if ($( this ).attr('country') !== selected){
      $(this).addClass('country-filter')
    }
  })
  window.scrollBy(0, 1);
})



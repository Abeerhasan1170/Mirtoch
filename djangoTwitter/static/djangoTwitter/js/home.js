  $(".grid").masonry({
    itemSelector: '.tweets',
    columnWidth: '.sizer',
    percentPosition: true,


})

$('#filter').click(function(e){
  e.preventDefault()
  var p = document.getElementById("inputGroupSelect04").value
  console.log(p)
  $.ajax({
    type: "POST",
    url: 'filter/',
    data: {'profile':p},
    success: function(e){
      p = JSON.parse(e)
      if (p.length==0){
        $('.grid').html('No profile')
      }
      else{
      t = $(".tweets")
        for(j of t){
          if(p.includes(j.classList[1])){
            $(j).css('display','block')
          }
          else{
            $(j).css('display','none')
          }
        }
      $('.grid').masonry({
    itemSelector: '.tweets',
    columnWidth: '.sizer',
    percentPosition: true,


})
    }
  }
  });

})

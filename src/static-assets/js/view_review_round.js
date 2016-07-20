//Script for view_review_round.html template

var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].onclick = function(){
        this.classList.toggle("active");
        this.nextElementSibling.classList.toggle("show");
    }
}

  function confirm_function() {
      var agree=confirm("All review assignments in this round of review will be deleted. Are you sure you want to cancel this review round?");

      if (agree){
        return true;
      } else {
        return false;
      }
  }
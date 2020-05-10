function capacityChanged(){
  capacityVal = document.getElementById('capacity-filter').value
  var x = document.getElementsByClassName("car");
  for (var i = 0; i < x.length; i++) {
    var capacity = x[i].querySelectorAll(".capacity-value")[0].innerHTML.substring(9)
    if (parseInt(capacity) < parseInt(capacityVal)){
      x[i].style.display = "none";
    } else {
      x[i].style.display = "inline-block";
    }
  }
}

function colorFilter(){
  colourVal = document.getElementById('colour-filter').value
  var x = document.getElementsByClassName("car");
  for (var i = 0; i < x.length; i++) {
    var colour = x[i].querySelectorAll(".colour-value")[0].innerHTML.substring(8)
    if (colour != colourVal){
      x[i].style.display = "none";
    } else {
      x[i].style.display = "inline-block";
    }
  }
}

function makeFilter(){
  makeVal = document.getElementById('make-filter').value
  var x = document.getElementsByClassName("car");
  for (var i = 0; i < x.length; i++) {
    var make = x[i].querySelectorAll(".make-value")[0].innerHTML
    if (!make.includes(makeVal)){
      x[i].style.display = "none";
    } else {
      x[i].style.display = "inline-block";
    }
  }
}

function yearFilter(){
  yearVal = document.getElementById('year-filter').value
  var x = document.getElementsByClassName("car");
  for (var i = 0; i < x.length; i++) {
    var make = x[i].querySelectorAll(".make-value")[0].innerHTML
    if (!make.includes(yearVal)){
      x[i].style.display = "none";
    } else {
      x[i].style.display = "inline-block";
    }
  }
}

function filter() {
  yearVal = document.getElementById('year-filter').value
  makeVal = document.getElementById('make-filter').value
  colourVal = document.getElementById('colour-filter').value
  capacityVal = document.getElementById('capacity-filter').value
  searchVal = document.getElementById('search-box').value
  console.log(searchVal)

  var x = document.getElementsByClassName("car");
  for (var i = 0; i < x.length; i++) {
    var make = x[i].querySelectorAll(".make-value")[0].innerHTML
    var colour = x[i].querySelectorAll(".colour-value")[0].innerHTML.substring(8)
    var capacity = x[i].querySelectorAll(".capacity-value")[0].innerHTML.substring(9)
    if ((!make.toLowerCase().includes(searchVal.toLowerCase()) && searchVal != "") || (!make.includes(makeVal) && makeVal != 'All' )|| (!make.includes(yearVal) && yearVal != 'All' ) || (colour != colourVal && colourVal != 'All' ) || parseInt(capacity) < parseInt(capacityVal)){
      x[i].style.display = "none";
    } else {
      x[i].style.display = "inline-block";
    }
  }
}
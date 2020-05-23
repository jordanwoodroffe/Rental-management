function update_capacity_range(){
  minLabel = document.getElementById('min-capacity');
  maxLabel = document.getElementById('max-capacity');
  minSelect = document.getElementById('capacity-filter-min');
  maxSelect = document.getElementById('capacity-filter-max');
  for (var i = 0; i < minSelect.options.length; i++) {
    if (parseInt(minSelect[i].value) > parseInt(maxSelect.value)){
      minSelect[i].disabled = true;
    } else {
      minSelect[i].disabled = false;
    }
  }
  for (var i = 0; i < maxSelect.options.length; i++) {
    if (parseInt(maxSelect[i].value) < parseInt(minSelect.value)){
      maxSelect[i].disabled = true;
    } else {
      maxSelect[i].disabled = false;
    }

  }
  minLabel.innerHTML = minSelect.value;
  maxLabel.innerHTML = maxSelect.value;
  filter();
}

function update_cost_range(){
  minLabel = document.getElementById('min-cost');
  maxLabel = document.getElementById('max-cost');
  minSelect = document.getElementById('cost-filter-min');
  maxSelect = document.getElementById('cost-filter-max');
  for (var i = 0; i < minSelect.options.length; i++) {
    if (parseInt(minSelect[i].value) > parseInt(maxSelect.value)){
      minSelect[i].disabled = true;
    } else {
      minSelect[i].disabled = false;
    }
  }
  for (var i = 0; i < maxSelect.options.length; i++) {
    if (parseInt(maxSelect[i].value) < parseInt(minSelect.value)){
      maxSelect[i].disabled = true;
    } else {
      maxSelect[i].disabled = false;
    }

  }
  minLabel.innerHTML = minSelect.value;
  maxLabel.innerHTML = maxSelect.value;
  filter();
}

function update_load_index_range(){
  minLabel = document.getElementById('min-load-index');
  maxLabel = document.getElementById('max-load-index');
  minSelect = document.getElementById('load-index-filter-min');
  maxSelect = document.getElementById('load-index-filter-max');
  for (var i = 0; i < minSelect.options.length; i++) {
    if (parseInt(minSelect[i].value) > parseInt(maxSelect.value)){
      minSelect[i].disabled = true;
    } else {
      minSelect[i].disabled = false;
    }
  }
  for (var i = 0; i < maxSelect.options.length; i++) {
    if (parseInt(maxSelect[i].value) < parseInt(minSelect.value)){
      maxSelect[i].disabled = true;
    } else {
      maxSelect[i].disabled = false;
    }

  }
  minLabel.innerHTML = minSelect.value;
  maxLabel.innerHTML = maxSelect.value;
  filter();
}

function update_clearance_range(){
  minLabel = document.getElementById('min-clearance');
  maxLabel = document.getElementById('max-clearance');
  minSelect = document.getElementById('clearance-filter-min');
  maxSelect = document.getElementById('clearance-filter-max');
  for (var i = 0; i < minSelect.options.length; i++) {
    if (parseInt(minSelect[i].value) > parseInt(maxSelect.value)){
      minSelect[i].disabled = true;
    } else {
      minSelect[i].disabled = false;
    }
  }
  for (var i = 0; i < maxSelect.options.length; i++) {
    if (parseInt(maxSelect[i].value) < parseInt(minSelect.value)){
      maxSelect[i].disabled = true;
    } else {
      maxSelect[i].disabled = false;
    }

  }
  minLabel.innerHTML = minSelect.value;
  maxLabel.innerHTML = maxSelect.value;
  filter();
}

var filter = function() {
  yearVal = document.getElementById('year-filter').value
  makeVal = document.getElementById('make-filter').value
  colourVal = document.getElementById('colour-filter').value
  capacityMax = document.getElementById('capacity-filter-max').value
  capacityMin = document.getElementById('capacity-filter-min').value
  searchVal = document.getElementById('search-box').value
  costMax = document.getElementById('cost-filter-max').value
  costMin = document.getElementById('cost-filter-min').value
  transmissionVal = document.getElementById('transmission-filter').value
  loadIndexMax = document.getElementById('load-index-filter-max').value
  loadIndexMin = document.getElementById('load-index-filter-min').value
  clearanceMax = document.getElementById('clearance-filter-max').value
  clearanceMin = document.getElementById('clearance-filter-min').value  

  var x = document.getElementsByClassName("car");
  for (var i = 0; i < x.length; i++) {
    var make = x[i].querySelectorAll(".make-value")[0].innerHTML
    var colour = x[i].querySelectorAll(".colour-value")[0].innerHTML.substring(8)
    var transmission = x[i].querySelectorAll(".transmission-value")[0].innerHTML
    var capacity = x[i].querySelectorAll(".capacity-value")[0].innerHTML.substring(9)
    var cost = x[i].querySelectorAll(".cost-value")[0].innerHTML.substr(7, x[i].querySelectorAll(".cost-value")[0].innerHTML.indexOf(' '))
    var loadIndex = x[i].querySelectorAll(".load-index-value")[0].innerHTML
    var clearance = x[i].querySelectorAll(".clearance-value")[0].innerHTML

    if ((transmission != transmissionVal && transmissionVal != 'All' ) || (!make.toLowerCase().includes(searchVal.toLowerCase()) && searchVal != "") || (!make.includes(makeVal) && makeVal != 'All' )|| (!make.includes(yearVal) && yearVal != 'All' ) || (colour != colourVal && colourVal != 'All' ) || !((parseInt(capacity) <= parseInt(capacityMax)) && (parseInt(capacity) >= parseInt(capacityMin))) || !((parseInt(cost) <= parseInt(costMax)) && (parseInt(cost) >= parseInt(costMin))) || !((parseInt(loadIndex) <= parseInt(loadIndexMax)) && (parseInt(loadIndex) >= parseInt(loadIndexMin))) || !((parseInt(clearance) <= parseInt(clearanceMax)) && (parseInt(clearance) >= parseInt(clearanceMin))) ){
      x[i].style.display = "none";
    } else {
      x[i].style.display = "inline-block";
    }
  }
}

function capacityDropdown() {
  document.getElementById("select-capacity-container").classList.toggle("show");
}

function costDropdown() {
  document.getElementById("select-cost-container").classList.toggle("show");
}

function loadIndexDropdown() {
  document.getElementById("select-load-index-container").classList.toggle("show");
}

function clearanceDropdown() {
  document.getElementById("select-clearance-container").classList.toggle("show");
}


window.addEventListener("click", function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("select-capacity-container");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
    var dropdowns = document.getElementsByClassName("select-cost-container");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
})
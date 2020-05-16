
updateList = function() {
    var input = document.getElementById('image');
    var output = document.getElementById('imageList');
    var label = document.getElementById('listLabel')
    var children = "";
    for (var i = 0; i < input.files.length; ++i) {
        children += '<li>' + input.files.item(i).name + '</li>';
    }
    output.innerHTML = '<ul>'+children+'</ul>';
}
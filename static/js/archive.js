//Various functions
function expandContent(element,data){
	$(element).append("<div>" + data + "</div>");
}

function loadForm(url,callback) {
    $.get(url, function(response) { 
    	callback("#actions",response);
    });
}


//Scripting for archive controller
$(function() {
    console.log("starting script");
    $(".btn").one('click',function() {
	    loadForm( $(this).attr("href"), expandContent);
     });
});


function createXHR(){
	try {
		return new XMLHttpRequest();
  	} catch (e)  {
		try {
			return new ActiveXObject("Microsoft.XMLHTTP");
 		} catch (e) {
			return new ActiveXObject("Msxml2.XMLHTTP");
		}
	}
}


$(document).ready(function(){
	//create xmlhttprequestobhect
	var searchXHR=  createXHR();

	var relevantXHR= createXHR();

	searchXHR.onreadystatechange=function(){
 		if (searchXHR.readyState==4 && searchXHR.status==200){
   			card=JSON.parse(searchXHR.responseText);	
    		}
  	}


	relevantXHR.onreadystatechange=function(){
 		if (relevantXHR.readyState==4 && relevantXHR.status==200){
   			card=JSON.parse(relevantXHR.responseText);
			$("#paper-journal").html(card.journal)
			$("#paper-authors").html(card.author)
			$("#paper-title").html(card.title)
			$("#paper-abstract").html(card.abstract)

			
    		}
  	}
	
	$("#main-search").submit(function(e){
		post=JSON.stringify($("#main-search").serializeArray()[0]);
		searchXHR.open("POST","main-search",true);
		searchXHR.setRequestHeader("Content-type","application/json");
		searchXHR.send(post);
		console.log(post);
		e.preventDefault();
	});

	$("#relevant").click(function(){
		relevantXHR.open("POST","relevant",true);
		relevantXHR.setRequestHeader("Content-type", "application/json");
		relevantXHR.send(JSON.stringify({"state":"relevant","id":$("#paper-title").innerHTML}));
		//relevent//notrelavent//skip
	});
	$("#irrelevant").click(function(){
		relevantXHR.open("POST","relevant",true);
		relevantXHR.setRequestHeader("Content-type", "application/json");
		relevantXHR.send(JSON.stringify({"state":"irrelevant","id":$("#paper-title").innerHTML}));
		//relevent//notrelavent//skip
	});
	$("#skip").click(function(){
		relevantXHR.open("POST","relevant",true);
		relevantXHR.setRequestHeader("Content-type", "application/json");
		relevantXHR.send(JSON.stringify({"state":"skip","id":$("#paper-title").innerHTML}));
		//relevent//notrelavent//skip
	});



});


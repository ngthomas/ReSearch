liked_counter=0

card_colors=['#FFF6D3','#FFEBD3','#D6D1F6','#CDE6F4','#DEE','#DDD']
function randomColor(){
	return card_colors[Math.floor(Math.random()* card_colors.length)]
}

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

function fadeOutPaper(n){
	$("#paper-journal").fadeOut(n)
	$("#paper-authors").fadeOut(n)
	$("#paper-title").fadeOut(n)
	$("#paper-abstract").fadeOut(n)
}
function fadeInPaper(n){
	$("#paper-journal").fadeIn(n)
	$("#paper-authors").fadeIn(n)
	$("#paper-title").fadeIn(n)
	$("#paper-abstract").fadeIn(n)
}

$(document).ready(function(){
	$("#card").css('background', randomColor())

	//create xmlhttprequestobhect
	var searchXHR=  createXHR();

	var relevantXHR= createXHR();

    var papersXHR = createXHR();


	searchXHR.onreadystatechange=function(){
 		if (searchXHR.readyState==4 && searchXHR.status==200){
   			card=JSON.parse(searchXHR.responseText);
			//console.log(card)
			setTimeout(function(){
				$("#paper-journal").html(card.journal)
				$("#paper-authors").html(card.Author)
				$("#paper-title").html(card.title)
				$("#paper-abstract").html(card.Excerpt)
				$("#card").css('background', randomColor())
   				$("#buttons").fadeIn("400");
				fadeInPaper("fast")

			},100);

    		}
  	}


	relevantXHR.onreadystatechange=function(){
 		if (relevantXHR.readyState==4 && relevantXHR.status==200){
			$("#liked").html("Papers (" + liked_counter + ")")
			setTimeout(function(){
   				card=JSON.parse(relevantXHR.responseText);
				$("#paper-journal").html(card.journal)
				$("#paper-authors").html(card.author)
				$("#paper-title").html(card.title)
				$("#paper-abstract").html(card.abstract)
				$("#card").css('background', randomColor())
				fadeInPaper("fast")
			},100);
			
    		}
  	}
	
	papersXHR.onreadystatechange=function() {
		if (papersXHR.readyState == 4 && papersXHR.status == 200) {
			$("#papers-page").fadeIn("400")
    	}
    }

    $("#liked").click(function() {
    	if (current_page == "main") {
			$("#main-page").fadeOut("400");
    	}
		papersXHR.open("POST","papers",true);
		papersXHR.setRequestHeader("Content-type","application/json");
		papersXHR.send(post);
    })
	
	$("#main-search").submit(function(e){
		post=JSON.stringify($("#main-search").serializeArray()[0]);
		searchXHR.open("POST","main-search",true);
		searchXHR.setRequestHeader("Content-type","application/json");
		searchXHR.send(post);
		//console.log(post);
		e.preventDefault();
	});

	$("#relevant").click(function(){
		fadeOutPaper("fast")
		relevantXHR.open("POST","relevant",true);
		relevantXHR.setRequestHeader("Content-type", "application/json");
		relevantXHR.send(JSON.stringify({"state":"relevant","id":$("#paper-title").innerHTML}));
		liked_counter= liked_counter+1;
		//relevent//notrelavent//skip
	});
	$("#irrelevant").click(function(){
		fadeOutPaper("fast")
		relevantXHR.open("POST","relevant",true);
		relevantXHR.setRequestHeader("Content-type", "application/json");
		relevantXHR.send(JSON.stringify({"state":"irrelevant","id":$("#paper-title").innerHTML}));
		//relevent//notrelavent//skip
	});
	$("#skip").click(function(){
		fadeOutPaper("fast")
		relevantXHR.open("POST","relevant",true);
		relevantXHR.setRequestHeader("Content-type", "application/json");
		relevantXHR.send(JSON.stringify({"state":"skip","id":$("#paper-title").innerHTML}));
		//relevent//notrelavent//skip
	});



});


viewed_counter = 0;

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

function updateTags(tags) {
	var content = ""
	for (index in tags) {
		tag = tags[index]
		console.log(tag)
		content += '<span class="label label-default">' + tag + '</span>'
	}
	$("#tags").html(content)
}

$(document).ready(function(){
	$("#card").css('background', randomColor())

	//create xmlhttprequestobhect
	var searchXHR=  createXHR();

	var relevantXHR= createXHR();

	var papersXHR = createXHR();

	var currentCARD = {"Journal": "University of California at Santa Cruz", 
		"Title": "reSearch: the paper recommendation app",
		"Authors": "Brian Lin, Thomas Ng, Robert Shelansky, Adrian Bivol",
		"Excerpt": "<b>reSearch</b> is an app that helps scientists find relevant papers using a recommendation system. Enter a search query, and you'll have the opportunity to tell us whether the results are relevant or not. Build a station that learns your preferences and subscribe to updates in your field."
	}

	searchXHR.onreadystatechange=function(){
 		if (searchXHR.readyState==4 && searchXHR.status==200){
			console.log(searchXHR.responseText)
   			card=JSON.parse(searchXHR.responseText);
			currentCARD = card
			//console.log(card)
			setTimeout(function(){
				$("#paper-journal").html(card.Journal)
				$("#paper-authors").html(card.Author)
				$("#paper-title").html(card.Title)
				$("#paper-abstract").html(card.Excerpt)
				$("#card").css('background', randomColor())
   				$("#buttons").fadeIn("400");
				fadeInPaper("fast")
				updateTags(card.tags)
			},100);

    		}
  	}


	relevantXHR.onreadystatechange=function(){
 		if (relevantXHR.readyState==4 && relevantXHR.status==200){
			$("#liked").html("Papers (" + viewed_counter + ")")
			card=JSON.parse(relevantXHR.responseText);
			currentCARD = card
			setTimeout(function(){
   				$("#paper-journal").html(card.Journal)
				$("#paper-authors").html(card.Author)
				$("#paper-year").html(card.Year)
				$("#paper-title").html(card.Title)
				$("#paper-abstract").html(card.Excerpt)
				$("#card").css('background', randomColor())
				fadeInPaper("fast")
				updateTags(card.tags)
			},100);
    	}
  	}
	
	papersXHR.onreadystatechange=function() {
		if (papersXHR.readyState == 4 && papersXHR.status == 200) {
	    	setTimeout(function(){
				$("#papers-page").fadeIn("200")
			},200);
			viewed_papers = JSON.parse(papersXHR.responseText);
			$('#papers-table > tbody').html("");
			var content = ""
			for (index in viewed_papers) {
				paper = JSON.parse(viewed_papers[index])
				if (paper.State == 1) {
					content += '<tr class="success">'
				} else if (paper.State == -1) {
					content += '<tr class="danger">'
				} else if (paper.State == 0) {
					content += '<tr class="info">'
				} else {
					content += '<tr>'
				}
				content += "<td><a href='" + paper.URL + "'>"+ paper.Title + "</a></td>"
				content += "<td>" + paper.Author + "</td>"
				content += "<td>" + paper.Journal + "</td>"
				content += "<td>" + paper.Year + "</td>"
				content += "</tr>"
			}
			$('#papers-table > tbody:last').append(content)
    	}
    }

    $("#liked").click(function() {
    	$("#main-page").fadeOut("200");
		papersXHR.open("GET","papers",true);
		papersXHR.setRequestHeader("Content-type","application/json");
		papersXHR.send();
    });

    $("#return-main").click(function() {
    	$("#papers-page").fadeOut("200");
    	setTimeout(function(){
    	$("#main-page").fadeIn("200");
			},300);
    });

    $("#brand").click(function() {
    	location.reload();
    });
	
	$("#main-search").submit(function(e){
		post=JSON.stringify($("#main-search").serializeArray()[0]);
		// console.log(post);
		searchXHR.open("POST","main-search",true);
		searchXHR.setRequestHeader("Content-type","application/json");
		searchXHR.send(post);
		e.preventDefault();
	});

	$("#relevant").click(function(){
		fadeOutPaper("fast")
		relevantXHR.open("POST","relevant",true);
		relevantXHR.setRequestHeader("Content-type", "application/json");
		currentCARD.State = 1
		relevantXHR.send(JSON.stringify(currentCARD));
		viewed_counter= viewed_counter+1;
		//relevent//notrelavent//skip
	});
	$("#irrelevant").click(function(){
		fadeOutPaper("fast")
		relevantXHR.open("POST","relevant",true);
		relevantXHR.setRequestHeader("Content-type", "application/json");
		currentCARD.State = -1
		relevantXHR.send(JSON.stringify(currentCARD));
		viewed_counter= viewed_counter+1;
		//relevent//notrelavent//skip
	});
	$("#skip").click(function(){
		fadeOutPaper("fast")
		relevantXHR.open("POST","relevant",true);
		relevantXHR.setRequestHeader("Content-type", "application/json");
		currentCARD.State = 0
		relevantXHR.send(JSON.stringify(currentCARD));
		viewed_counter= viewed_counter+1;
		//relevent//notrelavent//skip
	});



});


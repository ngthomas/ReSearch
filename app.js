var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var process = require('child_process');
var express = require('express');
var app = express();

//used for testing
var stack= new Array();
stack.push({journal:"Journal of lies",title:"I AM AWSOME",author:"Robert Shelansky, John Smith",abstract:"This is about me"})
stack.push({journal:"Journal of truth",title:"",author:"",abstract:""})
stack.push({journal:"Journal of lopsided lollipops",title:"",author:"",abstract:""})



// uncomment after placing your favicon in /public
//app.use(favicon(__dirname + '/public/favicon.ico'));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));


/*ROUTES*/
app.get('/', function(req, res) {
  //res.render('index', { title: 'Express' });
	res.sendFile('/home/ec2-user/reSearch/public/index.html')
});

var rated_data=    new Array();
var search_data=   new Array();
var keywords_data= new Array();


app.post('/relevant', function(req, res) {
	console.log("STUBB: " + JSON.stringify(req.body))
	article=stack.pop()
	console.log(article)
	res.json(article)
});

function main_search(req,res){
	keywords= req.body.value;

	process.exec("/usr/bin/python /home/ec2-user/reSearch/search/search_core.py -q '" + keywords+"'", function (error,stdout,stderr){
		out=JSON.parse(stdout);
		console.log("arts"+out)
		for (x in out.articles){
			console.log("search.out" + out.articles[x])
			search_data.push(out.articles[x]);
		}
		if(error !== null){
			console.log('exec error', stderr)
		}
		console.log("array"  + search_data.length);
		res.json(search_data.pop());
	});

//	var python = process.spwan('echo', "/home/robert/local/reSearch/search/adrian.py");
//	python.stdout.on('data', function(){output += data});
//	python.on('close', function(code){
//		if (code !== 0) {  
//			console.log("NOOOOO!!!!")
//		}
//		console.log(output)
//	});
	
}



app.post('/main-search', function(req, res) {
	console.log("SEARCH: " + JSON.stringify(req.body));
	console.log("query is " + req.body.value);
	main_search(req,res);
});

app.post('/papers', function(req, res) {
	console.log("Requested papers");
	var papers = {"nice things": "HI I AM PAPERS"};
	res.json(papers);
})

app.set('view engine', 'jade')

// catch 404 and forward to error handler
app.use(function(req, res, next) {
    res.send("404 error")
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.send(err.status)
    
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.send('error', {
        message: err.message,
        error: {}
    });
});


module.exports = app;

var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var exec = require('child_process').exec;
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

var rated=    new Array();
var search=   new Array();
var keywords= new Array();


app.post('/relevant', function(req, res) {
	console.log("STUBB: " + JSON.stringify(req.body))
	article=stack.pop()
	console.log(article)
	res.json(article)
});

function search(keywords){
	exec("echo 'I AM THE MAN'",function(error, stdout,stderr) {
		console.log("SEARCH: " + JSON.stringify(req.body))
		console.log("query is " + req.body.value)
		if (error !== null) {
			console.log('exec error: ' + error);
		}
	});

}

app.post('/main-search', function(req, res) {
	res.json(req.body)
});

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

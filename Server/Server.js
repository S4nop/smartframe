// code from https://github.com/codeforgeek/File-upload-in-Node/
// Tutorial link : http://wp.me/p4ISPV-cq
var express = require('express');
var multer = require('multer');
var app = express();
var fs = require('fs');
var done = false;

app.post('/api/send', multer({dest: './tmp/'}).single('userFile'), 
    svUploaded
);

app.get('/idcheck', function(req, res){
    console.log(req.query);
    var id = req.query.id;
    fs.readdir('./' + id, function(error, filelist){ 
        fs.readFile('./' + id + '.udate', 'utf8', function(err, data){
            res.send(data + '&!&' + filelist);
        })
    });
});

app.get('/getPhoto', function(req, res){
    var id = req.query.id;
    var picName = req.query.picName;
    res.sendfile('./' + id + '/' + picName);
});

app.get('/', function (req, res) {
    res.sendfile('index.html');
});



app.listen(2905, function () {
    console.log("[[[[Server On :: Port 2905]]]]");
});

app.use('/users', express.static('uploads'));

function udate(id){
    fs.readdir('./' + id, function(error, filelist){ 
        fs.writeFile('./' + id + '.udate', Date.now(), 'utf8', function(err){
            console.log(id + " :: Time updated")
        })
    });
}

function svUploaded(req, res){
    var id = req.body.id;
    var fName = req.file.originalname;
    
    console.log(id);
    console.log(fName);
    fs.renameSync('./tmp/' + req.file.filename, './' + id + '/' + fName);
    res.end("File uploaded.\n" + JSON.stringify(id + '/' + fName));
    udate(id);
}

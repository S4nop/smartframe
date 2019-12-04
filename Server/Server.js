// code from https://github.com/codeforgeek/File-upload-in-Node/
// Tutorial link : http://wp.me/p4ISPV-cq
var express = require('express');
var multer = require('multer');
var app = express();
var fs = require('fs');
var done = false;

app.use(multer({
    dest: './tmp/',
    rename: function (fieldname, filename) {
        return Date.now();
    },
    onFileUploadStart: function (file) {
        console.log(file.originalname + ' is starting ...')
    },
    onFileUploadComplete: function (file) {
        console.log(file.fieldname + ' uploaded to  ' + file.path)
        done = true;
    }
}));

app.post('/idcheck', function(req, res){
    var id = req.body.id;
    fs.readdir('./' + id, function(error, filelist){ 
        fs.readFile('./' + id + '/' + 'udate', 'utf8', function(err, data){
            res.send(data + '&!&' + filelist);
        })
    });
});

app.post('/getPicture', function(req, res){
    var id = req.body.id;
    var picName = req.body.picName;
    res.sendfile('./' + id + '/' + picName);
});

app.post('/udateid', function(req, res){
    var id = req.body.id;
    var now = req.body.now;
    fs.readdir('./' + id, function(error, filelist){ 
        fs.writeFile('./' + id + '/' + 'udate', now, 'utf8', function(err){
            console.log(id + " :: Time updated")
        })
    });
});

app.get('/', function (req, res) {
    res.sendfile('index.html');
});

app.post('/api/photo', function (req, res) {
    if (done == true) {
        var id = req.body.id;
        var fName = req.files.userPhoto.name;
        console.log(id);
        console.log(req.files);
        fs.renameSync('./tmp/' + fName, './' + id + '/' + fName);
        res.end("File uploaded.\n" + JSON.stringify(id + '/' + fName));
    }
});


app.listen(2905, function () {
    console.log("[[[[Server On :: Port 2905]]]]");
});

app.use('/users', express.static('uploads'));

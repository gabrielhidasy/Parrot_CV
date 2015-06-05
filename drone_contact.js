var application_root = __dirname;
var express = require("express");
var path = require("path");
var arDrone = require('ar-drone');
var http = require('http')
var client  = arDrone.createClient();
//require('ar-drone-png-stream')(client, {port:8001});
var img = 0;
var updateImg = function(imgi) {
	img = imgi;
};
var pngStream = client.getPngStream();
pngStream.on('data', updateImg);
var app = express();
var drone = {
	takeoff: function(req, res) {
		client.takeoff();
		console.log("taking off");
		res.send("Express");
		},
	land: function(req, res) {
		client.land();
		console.log("landing");
		res.send("Express");
	},
	up: function(req, res) {
		var speed = 0.5;
		var time = 500;
		if(req.param('speed')) {
			speed = req.param('speed')
		}
		if(req.param('time')) {
			time = req.param('time')
		}
		client.up(speed);
		console.log("going up at ",speed," for ",time);
		setTimeout(function() {client.stop();},time);
		res.send("Going up");
	},
	down: function(req, res) {
		var speed = 0.5;
		var time = 500;
		if(req.param('speed')) {
			speed = req.param('speed')
		}
		if(req.param('time')) {
			time = req.param('time')
		}
		client.down(speed);
		console.log("going down at",speed," for ",time);
		setTimeout(function() {client.stop();},time);
		res.send("Going down");
	},
	front: function(req, res) {
		var speed = 0.5;
		var time = 500;
		if(req.param('speed')) {
			speed = req.param('speed')
		}
		if(req.param('time')) {
			time = req.param('time')
		}
		client.front(speed);
		console.log("front");
		setTimeout(function() {client.stop();},time);
		res.send("Front");
	},
	back: function(req, res) {
		var speed = 0.5;
		var time = 500;
		if(req.param('speed')) {
			speed = req.param('speed')
		}
		if(req.param('time')) {
			time = req.param('time')
		}
		client.back(speed);
		console.log("back");
		setTimeout(function() {client.stop();},time);
		res.send("Back");
	},
	left: function(req, res) {
		var speed = 0.5;
		var time = 500;
		if(req.param('speed')) {
			speed = req.param('speed')
		}
		if(req.param('time')) {
			time = req.param('time')
		}
		client.left(speed);
		console.log("left");
		setTimeout(function() {client.stop();},time);
		res.send("Left");
	},
	right: function(req, res) {
		var speed = 0.5;
		var time = 500;
		if(req.param('speed')) {
			speed = req.param('speed')
		}
		if(req.param('time')) {
			time = req.param('time')
		}
		client.right(speed);
		console.log("right");
		setTimeout(function() {client.stop();},time);
		res.send("Right");
	},
	rotatel: function(req, res) {
		var speed = 0.5;
		var time = 500;
		if(req.param('speed')) {
			speed = req.param('speed')
		}
		if(req.param('time')) {
			time = req.param('time')
		}
		client.clockwise(speed);
		console.log("rotateL");
		setTimeout(function() {client.stop();},time);
		res.send("rotateL");
	},
	rotater: function(req, res) {
		var speed = 0.5;
		var time = 500;
		if(req.param('speed')) {
			speed = req.param('speed')
		}
		if(req.param('time')) {
			time = req.param('time')
		}
		client.counterClockwise(speed);
		console.log("rotater");
		setTimeout(function() {client.stop();},time);
		res.send("rotateR");
	},
	stop: function(req, res) {
		client.stop(1);
		console.log("STOP");
		res.send("Express");
	},
	uou: function(req, res) {
		client.animate("flipAhead",1000);
		console.log("UOU");
		res.send("Express");
	},
	getimg: function(req, res) {
		console.log("Getting Image")
		res.send(img);
	}
};
//speed and time ware 300 and 0.1
app.get('/takeoff', drone.takeoff);
app.get('/land', drone.land);
app.get('/up', drone.up);
app.get('/down', drone.down);
app.get('/front', drone.front);
app.get('/back', drone.back);
app.get('/left', drone.left);
app.get('/right', drone.right);
app.get('/rotatel', drone.rotatel);
app.get('/rotater', drone.rotater);
app.get('/stop', drone.stop);
app.get('/uou', drone.uou);
app.get('/img.jpg', drone.getimg);
app.listen(8002);
client.createRepl();

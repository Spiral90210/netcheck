
const express = require("express");
const app = express();
const speedtest = require("speedtest-net");
const path = require("path");
require('dotenv').config()

const bytesToMbitsFactor = 8 / 1000000;

let speedResult = {
	downloadMbits: -1,
	uploadMbits: -1
};


const doTest = (schedule) => {
	console.log("Starting test...");
	speedtest({
		acceptGdpr: true,
		acceptLicense: true
	}).catch((e) => {
		console.error(e);
	}).then((result) => {
		if (result === undefined) {
			console.warn("Undefined result");
			return;
		}
		/*
		Bandwidth is in BYTES! So, need to convert to bits to match the result on
		the website! So, (x*8) / (1 000 000) to get Mbps (or just /8 to get MBps)
		*/
		console.log("Test finished")
		speedResult.uploadMbits =
			(result.upload.bandwidth * bytesToMbitsFactor).toFixed(2);
		speedResult.downloadMbits =
			(result.download.bandwidth * bytesToMbitsFactor).toFixed(2);
		console.log(`Result: ${result.result.url}`);

	}).finally(() => {
		if (schedule) {
			console.log("Scheduling test interval...");
			setInterval(() => {
				doTest(false);
			}, 5 * 60000);
		}
	});
}

doTest(true);


app.get("/result.json", function (req, res) {
	res.header('Cache-Control', 'private, no-cache, no-store, must-revalidate');
	res.header('Expires', '-1');
	res.header('Pragma', 'no-cache');
	res.send(speedResult)
});

app.use(express.static(path.join(__dirname, 'public')));

app.get('*', function (req, res) {
	res.redirect('/index.html');
});


const port = ('PORT' in process.env)
	? process.env.PORT
	: 0;
const server = app.listen(port);

console.log(`http://localhost:${port}/index.html`);
console.log(`http://localhost:${port}/result.json`);

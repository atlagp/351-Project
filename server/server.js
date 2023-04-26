const express = require("express");
const spawn = require("child_process").spawn;
const fs = require("fs");
const requestID = import("express-request-id");
const app = express();
const port = 8080;
requestID.then( (reqid) => {	
	app.use(reqid.default());

	app.post("/birdcall", express.raw({type : "audio/wave", limit : "50mb"}), (req, res) => {
		const filename = req.id + "-out.wav";

		const buffer = req.body;
		fs.writeFile(filename, buffer, (err) => {
			if (err) {
				res.status(500)
				res.render("error", {
					message : err.message,
					error : {}
				})
			}
			else {
				python = spawn(
					"python",
					["../main.py", "-m", "test", "match", filename]
				);
				python.stdout.on("data", (data) => {
					console.log(data);
					res.json({
						"bird_id" : data
					})
				});
			}
		});

	})

	app.listen(port, () => {
		console.log("] starting api");
	})

})

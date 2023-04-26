import React, { useState } from 'react';
import logo from './logo.svg';
import Recorder from './rec.js';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import './App.css';

	var recorder; 

function App() {
	const audioContext =  new (window.AudioContext || window.webkitAudioContext)();

	const [status, setState] = useState("init");



	function startRecording() {
		recorder =  new Recorder(audioContext, {
			// An array of 255 Numbers
			// You can use this to visualize the audio stream
			// If you use react, check out react-wave-stream
			micConfig : {
				sampleRate : 44100,
				numChannels : 1
			},
		});

		navigator.mediaDevices.getUserMedia({audio: true})
			.then(stream => recorder.init(stream))
			.then(() => recorder.start())
			.then(() => {setState("recording")})
			.catch(err => console.log('Uh oh... unable to get stream...', err));

	}

	function stopRecording() {
		recorder.stop()
			.then(({blob, buffer}) => {
				Recorder.download(blob, 'my-audio-file');
				setState("init");
			});
	}

	const elts = {
		//some error ocurred, refresh
		error : () => {
			return (
				<div className="error">
				</div>
			)
		},
		//uploading and waiting for response
		upload : () => {
			return(
				<div className="loading">
				</div>
			)

		},
		//recording panel
		recording : () => {
			return (
				<div>
					<Button variant="outlined" onClick={stopRecording}>save</Button>
				</div>
			)
		},
		//result panel
		result : (bird_id) => {
			
		},
		init : () => {
			return (
				<div>
					<Button variant="outlined" onClick={startRecording}>record</Button>
				</div>
			)
		}
	}

	return (
		<div className="App">
			
			<img src={logo} className="App-logo" alt="logo" />
			<Grid
			{elts[status]()}
			<p>
				Edit <code>src/App.js</code> {status}and save to reload.
			</p>
			
		</div>
	);
}

export default App;

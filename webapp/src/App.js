import logo from './logo.svg';
import Recorder from './rec.js';
import Button from '@mui/material/Button';
import './App.css';

const audioContext =  new (window.AudioContext || window.webkitAudioContext)();
var recorder; 

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
		.catch(err => console.log('Uh oh... unable to get stream...', err));

}

function stopRecording() {
	recorder.stop()
		.then(({blob, buffer}) => {
			Recorder.download(blob, 'my-audio-file');
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
	recording  :() => {
				<Button onClick={stopRecording}>save</Button>
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

var status = "init";
function App() {
  return (
    <div className="App">
			<img src={logo} className="App-logo" alt="logo" />
			{elts[status]()}
			<p>
				Edit <code>src/App.js</code> and save to reload.
			</p>
				
		</div>
	);
}

export default App;

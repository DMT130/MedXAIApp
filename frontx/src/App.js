import './App.css';
import React, { useState } from "react"
//import axios from "axios";

const preditURL = "https://medxaiapp-v2-fc2s4lwtyq-uc.a.run.app/file/"

function App() {
	const [selectedFile, setSelectedFile] = useState();
	const [isFilePicked, setIsFilePicked] = useState(false);
	const [getResponse, setResponse] = useState([]);
	const [byteimg, setbyteimg] = useState([]);
	const deaseses = []

	const changeHandler = (event) => {
		setSelectedFile(event.target.files[0]);
		setIsFilePicked(true);
	};

	const handleSubmission = async () => {
		const formData = new FormData();

		formData.append('file', selectedFile, selectedFile.name);
    	const requestOptions = {
      	method: 'POST',
	  	mode: "cors",
      	body: formData, // Also tried selectedFile
	  //headers: {'Content-Type': 'multipart/form-data'}
    };
	try {
    const response = await fetch(preditURL, requestOptions);
	const data = await response.json();
	//const data2 = await JSON.stringify(response)
	setResponse(data["classes"])
	setbyteimg(data["image"])
	console.log(getResponse)
		} catch(error) {
			console.error('Error:', error);
		};
	};
	getResponse.forEach((data, index) => {
		deaseses.push(<p key={index}>{data}</p>)
	})

	return(
   		<div>
			<div>
				<div className="text-center">
					<input type="file"
					onChange={changeHandler} />
				</div>
				<br/>
				<div className="text-center">
					<button type="button" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4"
					onClick={handleSubmission}>Predict</button>
				</div>
			</div>
			<div className="grid grid-cols-1 md:grid-cols-6 gap-4 max-w-md md:max-w-6xl mx-auto">
				<div className="...">
				<div>
					<div className="block p-6 max-w-sm bg-white rounded-lg border border-gray-200 shadow-md hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
						{isFilePicked ? (
							<div>
								<div>Filename: {selectedFile.name}</div>
								<div>Filetype: {selectedFile.type}</div>
								<div>Size in bytes: {selectedFile.size}</div>
								<div>lastModifiedDate:{' '}{selectedFile.lastModifiedDate.toLocaleDateString()}</div>
								<br/>
								<p>Predicted Deseases</p>
								<div className='list-outside'>
								{deaseses}
								</div>
							</div>
						) : (
							<div>
								<p className="text-justify ...">Select a file to show details. It's recommended to upload DICOM files but png, jpg e jpeg files can also be used</p>
								<br></br>
								<p className="text-justify ...">Instructions: Select an image and press the Predict button, wait up to 15 seconds, the uploaded image will be posted bellow. Please note, the application does not save any image</p>
								<br></br>
								<p className="text-justify ...">This application can identiy the following deseases in torax XRAR images:</p>
								<ol className="list-disc">
									<li>Cardiomegaly</li>
									<li>Aortic enlargement</li>
									<li>Pleural thickening</li>
									<li>ILD</li>
									<li>Nodule/Mass</li>
									<li>Pulmonary fibrosis</li>
									<li>Lung Opacity</li>
									<li>Atelectasis</li>
									<li>Other lesion</li>
									<li>Infiltration</li>
									<li>Pleural effusion</li>
									<li>Calcification</li>
									<li>Consolidation</li>
									<li>Pneumothorax</li>
								</ol>
							</div>
						)}
					</div>
				</div>
				</div>
				<div className="col-span-5 ...">
						{byteimg ? (
							<img className="max-w-full h-auto" src={`data:image/jpeg;base64,${byteimg}`} alt="" />
						) : (
							<div>No Predictions</div>
						)}
				</div>
			</div>
			
		</div>
	)
}

export default App

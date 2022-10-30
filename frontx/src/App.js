import './App.css';
import React, { useState } from "react"
//import axios from "axios";

const preditURL = "http://localhost:8000/file/"

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
		deaseses.push(<p key={index} className="ml-3">{data}</p>)
	})

	return(
   		<div>
			<div className="container mx-auto px-8 flex flex-col ...">
				<div>
					<input className="block w-full text-sm text-gray-800 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400" aria-describedby="file_input_help" id="file_input" type="file"
					onChange={changeHandler} />
				</div>
				<div>
					<button type="button" class="block w-full text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700"
					onClick={handleSubmission}>Predict</button>
				</div>
			</div>
			<div class="flex ...">
				<div class="flex-none w-30 h-14 ...">
				<div>
					<div>
						{isFilePicked ? (
							<div className="flex flex-col ...">
								<div>Filename: {selectedFile.name}</div>
								<div>Filetype: {selectedFile.type}</div>
								<div>Size in bytes: {selectedFile.size}</div>
								<div>lastModifiedDate:{' '}{selectedFile.lastModifiedDate.toLocaleDateString()}</div>
							</div>
						) : (
							<div>Select a file to show details</div>
						)}
					</div>
				</div>
				</div>
				<div class="grow h-14 ...">
						{byteimg ? (
							<img className="max-w-full h-auto" src={`data:image/jpeg;base64,${byteimg}`} alt="" />
						) : (
							<div>No Predictions</div>
						)}
				</div>
				<div class="flex-none w-30 h-14 ...">
					{deaseses}
				</div>
			</div>
			
		</div>
	)
}

export default App

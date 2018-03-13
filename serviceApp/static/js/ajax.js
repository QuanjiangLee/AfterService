function createRequest(){
var request = null;
try {
	request = new XMLHttpRequest();	
} catch (trymicrosoft) {
	try {
		request = new ActiveXObject("Msxm12.XMLHTTP");
	} catch (othermicrosoft) {
		try {
			request = new ActiveXObject("Microsoft.XMLHTTP");
		} catch (failed) {
			request = null;
		}
	}
}
if (request == null){
	alert("Error creating request object!");
} else {
    return request;
    }
}


//data type like "hello='world'&hi=56
function getRequest(url, data, type, func){
   // request.onreadystatechange = 
	let request = createRequest();
	var urlArgs = url + "?" + data;
	//alert(urlArgs)
	request.open("GET",urlArgs,type);
	request.onreadystatechange = function(){
		if (request.readyState == 4){
		if (request.status == 200){
			let response = request.responseText;
			//var response = request.responseXML;
			if (func != false){
				func(response);
					}
				} else {
					alert("Error! Request status is " + request.status);
				}
			}   
		} 
	request.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	//request.setRequestHeader("Content-Type","text/xml");
	//request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
	//request.setRequestHeader("Content-Type","application/json;charset=UTF-8");
	request.send(null);
    }

function postRequest(url, data, type, func) {
 	// body...
 	let request = createRequest();
	request.open("POST",url,type);
	request.onreadystatechange = function(){
		if (request.readyState == 4){
		if (request.status == 200){
			//var response = request.responseXML;
			let response = request.responseText;
			if (func != false){
				func(JSON.parse(response));
					}
				} else {
					alert("Error! Request status is " + request.status);
				}
			}   
		} 
	//request.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	//request.setRequestHeader("Content-Type","text/xml");
	//request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
	request.setRequestHeader("Content-Type","application/json;charset=UTF-8");
	request.send(JSON.stringify(data));
 }
function httpGet(theUrl)
{
    var xmlHttp = createRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}
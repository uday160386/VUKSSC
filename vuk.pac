/*



*/

function FindProxyForURL(url,host)
{

	url=url.toLowerCase();
	host=host.toLowerCase();
	myip=myIpAddress();
	hostip=dnsResolve(host);

	if		(
		shExpMatch(host, "d-sm07064.dom1.e-ssi.net") || 				// Webhosting
		isInNet(hostip,"10.86.64.100", "255.255.255.224")|| 			// 3rd party access new Adacor
		shExpMatch(host, "10.86.64.100")|| 					// 3rd party access EIT GiGroup
		shExpMatch(host, "10.86.64.100")					// 3rd party access  EIT GiGroup
			)
		return "PROXY 217.37.67.180:8080";
	
	
	else	
		return "PROXY 10.156.50.99:8080";
}

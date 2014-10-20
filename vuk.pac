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
			)
		return "PROXY 10.86.64.79:3128";
	
	
	else	
		return "PROXY 10.80.108.91:3128";
}

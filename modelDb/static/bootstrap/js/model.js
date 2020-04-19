function setDateUp(){
				var d = new Date();
				document.getElementsByName('fy').value=d.getFullYear();
				document.getElementsByName('fm').value=(d.getMonth()+1);
				document.getElementsByName('fd').value=d.getDate();
				// alert(document.getElementsByName('fd').value)
			}
function setDateDown(){
				var d = new Date();
				document.getElementsByName('ty').value=d.getFullYear();
				document.getElementsByName('tm').value=(d.getMonth()+1);
				document.getElementsByName('td').value=d.getDate();
			}

function pageup(){
	p = document.getElementById('nowpage').value;
	max = document.getElementById('pagemax').value;
	alert(p);
	if (parseInt(p) > 1) {
		document.getElementById('nowpage').value=(parseInt(p)-1);
	}
	document.getElementById('datesub').click();
	
}
function pagedown(){
	p = document.getElementById('nowpage').value;
	max = document.getElementById('pagemax').value;
	 
	 alert(p)
	if (parseInt(p) < parseInt(max)) {
		document.getElementById('nowpage').value=(parseInt(p)+1);
	}
	document.getElementById('datesub').click();
}
function getQueryVariable(variable){
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return(false);
}

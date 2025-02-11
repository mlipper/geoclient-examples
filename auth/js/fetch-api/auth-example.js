 // Define the /search endpoint URL
 const url = new URL("https://api.nyc.gov/geoclient/v2/search");

 function doSearch() {
     var locationParam = document.getElementById("loco").value;
     url.searchParams.append("input", locationParam);
     fetch(url, {
         method: "GET",
         headers: {
             // REPLACE WITH YOUR ACTUAL SUBSCRIPTION KEY
             "Ocp-Apim-Subscription-Key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
             "Cache-Control": "no-cache",
             "Content-Type": "application/json"
         }
     })
         .then(response => {
             if (!response.ok) {
                 throw new Error(`HTTP error! status: [${response.status}] ${response.statusText}`);
             }
             return response.json();
         })
         .then(data => {
            // Pretty print result in the console
             console.log(JSON.stringify(data, null, 2));

            // Pretty print result in an HTML element
             //document.getElementById("myDomElement").textContent = JSON.stringify(data, null, 2);
         })
         .catch(error => {
            // Log error to the console
            console.log("[ERROR]", error);

            // Show error in an HTML element
            //document.getElementById("myDomElement").innerHTML = error
        });
 }

function goToENVRIHUB(){

    const envrihub_base_url = 'https://envri-hub.envri.eu';
    var envrihub_path = '';
    var queryParams = new URLSearchParams(window.location.search);
    if (queryParams.has('envrihub')){
        if (queryParams.get("envrihub")==="sdemonstrators") {
            envrihub_path = "sciencedemonstrators";
        }
    }
    window.location.href = envrihub_base_url + '/' + envrihub_path;
    return 0;
}
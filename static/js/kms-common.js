function goToENVRIHUB(){

    const envrihub_base_url = 'https://envrihub.vm.fedcloud.eu';
    var queryParams = new URLSearchParams(window.location.search);
    if (queryParams.has('envrihub')){
        sourcepage = queryParams.get("envrihub");

        if (sourcepage.trim()==="main" || sourcepage.trim()==="main#"  || sourcepage.trim()==="null"  || sourcepage.trim()===null){
            window.location.href = envrihub_base_url + '/';
            return 0;
        }

        window.location.href = envrihub_base_url + '/' + sourcepage;

    }
    else{
        window.location.href = envrihub_base_url + '/';
    }

}
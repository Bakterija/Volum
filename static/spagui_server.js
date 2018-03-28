console.log('Loading spagui_server.js');

class PulseAudioInterface{
    constructor(){
        this.data = null;
        this.last_update = Date.now();
        console.log('PulseAudioInterface: init')
    }

    pa_info_callback(text){
        this.last_update = Date.now();
        this.data = JSON.parse(text);
    }

    DoubleCallback(callback) {
        var obj = this;
        return function(text){
            obj.pa_info_callback(text);
            callback(text);
        }
    }

    update_all(callback=null){
        var xhttp = new XMLHttpRequest();
        var pa_obj = this;
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4){
                if (this.status == 200) {
                    pa_obj.pa_info_callback(this.responseText);
                }
            }
        }
        xhttp.open("GET", 'pa_data.json', true);
        xhttp.send();
    }
}
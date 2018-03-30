console.log('Loading spagui_server.js');

class PulseAudioInterface{
    constructor(){
        this.data = null;
        this.last_update = Date.now();
        console.log('PulseAudioInterface: init')
    }

    set_sink_volume(id, volume){
        var xhttp = new XMLHttpRequest();
        var pa_obj = this;
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4){
                if (this.status == 200) {
                }
            }
        }
        let data = JSON.stringify({method: 'set_sink_volume', id: id, value: volume});
        xhttp.open("POST", 'pa_control', true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.send(data);
    }

    get_sink_volume(id){
        var val = this.data['sinks'][id]['volume']['front-left']['percent'];
        val = val.replace(' ', '');
        val = val.slice(0, val.length - 1);
        return val;
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
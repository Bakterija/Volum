console.log('Loading spagui_server.js');

class PulseAudioInterfaceServer extends PulseAudioInterface{
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
        super.set_sink_volume(id, volume);
        xhttp.send(data);
    }

    set_input_volume(id, volume){
        var xhttp = new XMLHttpRequest();
        var pa_obj = this;
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4){
                if (this.status == 200) {
                }
            }
        }
        let data = JSON.stringify({method: 'set_input_volume', id: id, value: volume});
        xhttp.open("POST", 'pa_control', true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        super.set_input_volume(id, volume);
        xhttp.send(data);
    }

    update_all(callback=null){
        if (this.is_updating) return;

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
        this.is_updating = true;
    }
}
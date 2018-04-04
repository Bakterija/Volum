console.log('Loading spagui_server.js');

class PulseAudioInterfaceServer extends PulseAudioInterface{
    post_pa_control(data, callback=null){
        var xhttp = new XMLHttpRequest();
        var pa_obj = this;
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4){
                if (callback){
                    callback(this);
                }
            }
        }
        xhttp.open("POST", 'pa_control', true);
        xhttp.setRequestHeader('Content-Type', 'application/json');
        xhttp.send(data);
    }

    set_sink_volume(id, volume){
        let data = JSON.stringify({method: 'set_sink_volume', id: id, value: volume});
        this.post_pa_control(data);
        super.set_sink_volume(id, volume);
    }

    set_input_volume(id, volume){
        let data = JSON.stringify({method: 'set_input_volume', id: id, value: volume});
        this.post_pa_control(data);
        super.set_input_volume(id, volume);
    }

    move_all_inputs(sink_id){
        var input_id;
        for (var i in this.data['sink input indexes']){
            input_id = this.data['sink input indexes'][i];
            let data = JSON.stringify(
                {method: 'move_sink_input', sink_id: sink_id, input_id: input_id});
            this.post_pa_control(data);
        }
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
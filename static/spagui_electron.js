console.log('Loading spagui_electron.js');

var remote = require('electron').remote;
var exec = require('child_process').exec;
function execute(command, callback){
    exec(command, function(error, stdout, stderr){
        callback(stdout);
    })
}

class PulseAudioInterfaceElectron extends PulseAudioInterface{
    init(){

    }

    set_sink_volume_callback(text){
        console.log("pacmd response: " + text);
    }

    set_input_volume(id, volume){
        var cmd = 'pacmd set-sink-input-volume ' + id + ' ' + volume * 655;
        execute(cmd, this.set_sink_volume_callback.bind(this));
        super.set_input_volume(id, volume);
    }

    set_sink_volume(id, volume){
        var cmd = 'pacmd set-sink-volume ' + id + ' ' + volume * 655;
        execute(cmd, this.set_sink_volume_callback.bind(this));
        super.set_sink_volume(id, volume);
    }

    set_default_sink(id){
        console.log('this.set_default_sink', id);
        var cmd = 'pacmd set-default-sink ' + id;
        execute(cmd, this.set_sink_volume_callback.bind(this));
    }

    move_all_inputs(sink_id){
        console.log('this.move_all_inputs', sink_id);
        var input_id, cmd;
        for (var i in this.data['sink input indexes']){
            input_id = this.data['sink input indexes'][i];
            cmd = 'pacmd move-sink-input ' + input_id + ' ' + sink_id;
            execute(cmd, this.set_sink_volume_callback.bind(this));
        }
    }

    update_all(callback=null){
        var cmd = 'python3 pacmd_handler.py sinks sink-inputs';
        if (callback){
            execute(cmd, this.DoubleCallback(callback));
        } else {
            execute(cmd, this.pa_info_callback.bind(this));
        }
    }
}

// var spag = remote.getGlobal('spagui');
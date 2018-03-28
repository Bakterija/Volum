console.log('Loading spagui_electron.js');

var remote = require('electron').remote;
var exec = require('child_process').exec;
function execute(command, callback){
    exec(command, function(error, stdout, stderr){
        callback(stdout);
    })
}

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

    update_sinks(callback=null){
        var cmd = 'python3 pacmd_parser.py sink-inputs nice-format';
        execute(cmd, this.pa_info_callback.bind(this));
    }

    update_sink_inputs(callback=null){
        var cmd = 'python3 pacmd_parser.py sink-inputs';
        execute(cmd, this.pa_info_callback.bind(this));
    }

    update_all(callback=null){
        var cmd = 'python3 pacmd_parser.py sinks sink-inputs';
        if (callback){
            execute(cmd, this.DoubleCallback(callback));
        } else {
            execute(cmd, this.pa_info_callback.bind(this));
        }
    }
}

// var spag = remote.getGlobal('spagui');
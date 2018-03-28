function load_js(url){
    var script = document.createElement("script");
    script.src = url;
    document.head.appendChild(script);
}

if (navigator.userAgent.search('Electron') == -1){
    const IS_ELECTRON = false;
    load_js('static/spagui_server.js');
} else {
    const IS_ELECTRON = true;
    load_js('static/spagui_electron.js');
}

function on_key_down(e){
    if (e.key == 'r'){
        location.reload();
    }
}

function on_key_up(e){
    if (e.key == '`'){
        slide_console();
    }
}

function slide_console(){
    var el = document.getElementById('console_div');
    var cl_a = 'console_div_outside';
    var cl_b = 'console_div_inside';
    
    if (el.classList.contains(cl_a)){
        el.classList.remove(cl_a);
        el.classList.add(cl_b);
    } else {
        el.classList.remove(cl_b);
        el.classList.add(cl_a);
    }
    el.style.display = 'block';
}

function addZero(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}

function write_console(text){
    var el = document.getElementById('cmsg');
    var clone = el.cloneNode(true);
    clone.innerHTML = text;
    clone.style.display = 'block';

    var d = new Date();
    var h = addZero(d.getHours());
    var m = addZero(d.getMinutes());
    var s = addZero(d.getSeconds());
    clone.innerHTML = h + ":" + m + ":" + s + '   ' + text;
    document.getElementById('console_div').appendChild(clone);
}

function init(){
    var loadevent = window.performance.timing.domContentLoadedEventEnd;
    var navstartevent = window.performance.timing.navigationStart;
    var loadTime = loadevent - navstartevent;
    write_console('Page rendered: in ' + loadTime + 'ms');
    pa_interface = new PulseAudioInterface();
    pa_interface.update_all(function(text){console.log(text);});
    window.setInterval(update, 200);
}

function update(){
    try{
        interval_counter += 1;
        if (interval_counter == 5){
            interval_counter = 0;
            var el = document.getElementById('HA1');
            el.innerHTML = "Update";
        }
        pa_interface.update_all();
        update_react();
    } catch (error){
        write_console(error.stack);
        throw(error);
    }
}

function sidebar_click(button_name){
    write_console('sidebar_click: ' + button_name);
}

function a_or_b(a, b){
    if (a){
        return a;
    }
    return b;
}

function get_sink_name(sink_data){
    var has_properties = sink_data.hasOwnProperty('properties');
    if (has_properties){
        if (sink_data.properties.hasOwnProperty('alsa.card_name')){
            return sink_data['properties']['alsa.card_name'];
        }
        if (sink_data.properties.hasOwnProperty('device.ladspa.name')){
            return sink_data['properties']['device.ladspa.name'];
        }
    }
    return ''
}

window.onload = init;
interval_counter = 0;
window.onkeydown = on_key_down;
window.onkeyup = on_key_up;
// globalShortcut.register('F5', location.reload);
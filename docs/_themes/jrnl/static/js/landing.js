var phrases = [
    ["", "today: Started writing my memoirs. On the command line. Like a boss.", ""],
    ["", "yesterday 2pm: used jrnl to keep track of accomplished tasks. The done.txt for my todo.txt", ""],
    ["-from 2009 -until may", "", "(Displays all entries from January 2009 to last may)"],
    ["", "A day on the beach with @beth and @frank. Taggidy-tag-tag.", ""],
    ["--tags", "", "@idea    7<br />@beth    5"],
    ["--export json", "", "(Exports your entire journal to json)"],
    ["--encrypt", "", "(256 bit AES encryption. Crack this, NSA.)"]
]

var args = document.getElementById("args");
var input = document.getElementById("input");
var output = document.getElementById("output");
var current = 0
var timer = null;
var fadeInTimer = null;
var fadeOutTimer = null;
var letterTimer = null;
var unletterTimer = null;

var next = function() {
    current = (current + 1) % phrases.length;
    reveal(current);
    timer = setTimeout(next, 5000);
}

var prev = function() {
    current = (current === 0) ? phrases.length - 1 : current - 1;
    reveal(current);
    timer = setTimeout(next, 5000);
}

var reveal = function(idx) {
    var args_text      = phrases[idx][0];
    var input_text     = phrases[idx][1];
    var output_text    = phrases[idx][2];
    var old_dix = idx == 0 ? phrases.length - 1 : idx - 1;
    console.log(idx, old_dix, "++++++++++++")
    var old_args_text   = args.innerHTML;
    var old_input_text  = input.innerHTML;
    var old_output_text = output.innerHTML;
    console.log(args_text, input_text, output_text)
    console.log(old_args_text, old_input_text, old_output_text)
    var s4 = function() {fadeIn(output_text, output);}
    var s3 = function() {letter(input_text, input, s4);}
    var s2 = function() {letter(args_text, args, s3);}
    var s1 = function() {unletter(old_args_text, args, s2);}
    var s0 = function() {unletter(old_input_text, input, s1);}
    fadeOut(old_output_text, output, s0, 10);
}

var fadeIn = function(text, element, next, step) {
    step = step || 0
    var nx = function() { fadeIn(text, element, next, ++step); }
    if (step==0) {
        element.innerHTML = "";
        fadeInTimer = setTimeout(nx, 550);
        return;
    }
    if (step==1) {element.innerHTML = text;}
    if (step>10 || !text) { if (next) {next(); return;} else return;}
    element.style.opacity = (step-1)/10;
    element.style.filter = 'alpha(opacity=' + (step-1)*10 + ')';
    fadeInTimer = setTimeout(nx, 50);
}

var fadeOut = function(text, element, next, step) {
    if (step===10) element.innerHTML = text;
    if (step<0 || !text) {
        element.innerHTML = "";
        if (next) {next(); return;}
        else return;
    }
    element.style.opacity = step/10;
    element.style.filter = 'alpha(opacity=' + step*10 + ')';
    var nx = function() { fadeOut(text, element, next, --step); }
    fadeOutTimer = setTimeout(nx, 50);
}

var unletter = function(text, element, next, timeout, index) {
    timeout = timeout||10;
    if (index==null) index = text.length;
    if (index==-1 || !text.length) { if (next) {next(); return;} else return;}
    element.innerHTML = text.substring(0, index);
    var nx = function() { unletter(text, element, next, timeout, --index); }
    unletterTimer = setTimeout(nx, timeout);
}

var letter = function(text, element, next, timeout, index) {
    timeout = timeout||35;
    index = index||0;
    if (index > text.length || !text.length) { if (next) {next(); return;} else return;}
    element.innerHTML = text.substring(0, index);
    var nx = function() { letter(text, element, next, timeout, ++index); }
    letterTimer = setTimeout(nx, timeout);
}

var reset = function() {
    var timers = [timer, fadeInTimer, fadeOutTimer, letterTimer, unletterTimer];
    timers.forEach(function (t) {
      clearTimeout(t);
    });

    args.innerHTML = "";
    input.innerHTML = "";
    output.innerHTML = "";
}

timer = setTimeout(next, 3000);

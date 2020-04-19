const apiurl = "/api/tts/aifab_01";

$(function () {
    function render(a) {
        if (Array.isArray(a)) {
            //return a.map(function (v) { return v; }).join(', ');
            return `Length: ${a.length}`
        } else {
            return a;
        }
    }
    $.get(apiurl, function (data) {
        const tts = JSON.parse(data);
        result = `<h1>${tts['name']}</h1>\n`
        result += Object.keys(tts).map(function (key) {
            console.log(tts[key]);
            return `<tr><td>${key}</td><td>${render(tts[key])}</td></tr>`;
        }).join('\n');
        $("#root").html(`<table class="table">${result}</table>`);
    });
});
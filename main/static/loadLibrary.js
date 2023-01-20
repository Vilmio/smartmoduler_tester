function loadLibrary() {
    var t = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
    "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css", 
    "https://cdn.jsdelivr.net/gh/gitbrent/bootstrap-switch-button@1.1.0/css/bootstrap-switch-button.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"];
    for (var e in t) {
        var r = e;
        if (!document.getElementById(r)) {
            var i = document.getElementsByTagName("head")[0],
                s = document.createElement("link");
            (s.id = r), (s.rel = "stylesheet"), (s.type = "text/css"), (s.href = t[e]), (s.media = "all"), i.appendChild(s);
        }
    }
    appendLibrary("main/static/cached-webpgr.js"),
        whenAvailable("requireScript", function (t) {
            requireScript("jquery", "3.5.1", "https://code.jquery.com/jquery-3.5.1.min.js"),
            requireScript("moment", "1.0.0", "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.0/moment.min.js"),
            whenAvailable("$", function () {
                requireScript("bootstrap", "0.0.0", "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.min.js"),
                requireScript("bootstrap_switch_button", "1.1.0", "https://cdn.jsdelivr.net/gh/gitbrent/bootstrap-switch-button@1.1.0/dist/bootstrap-switch-button.min.js"),
                appendLibrary("main/static/func.js");
            });
        });
}
function whenAvailable(i, n) {
    window.setTimeout(function () {
        window[i] ? n(window[i]) : whenAvailable(i, n);
    }, 10);
}
function appendLibrary(i) {
    (e = document.createElement("script")), (e.defer = !0), (e.type = "text/javascript"), (e.src = i), document.getElementsByTagName("head")[0].appendChild(e);
}
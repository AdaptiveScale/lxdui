
var HTML = {
    set: function (setId, htmlId, cb) {
        $('#' + setId).load('/static/templates/components.html #' + htmlId, function (response, status, xhr) {
            cb(status);
        });
    }
};
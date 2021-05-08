! function (a) {
    "use strict";
    a.fn.anarchytip = function (b) {
        var c = a.extend({
            xOffset: -25,
            yOffset: -100
        }, b);
        return this.each(function () {
            var b = a(this);
            b.hover(function (b) {
                this.t = this.title, this.title = "";
                var d = "" != this.t ? "<br/>" + this.t : "";
                a("body").append("<p id='preview'><img src='" + this.src + "' alt='Image preview' style='width: 400px'/>" + d + "</p>"), a("#preview").css({
                    top: b.pageY - c.xOffset + "px",
                    left: b.pageX + c.yOffset + "px"
                }).fadeIn()
            }, function () {
                this.title = this.t, a("#preview").remove()
            }), b.mousemove(function (b) {

                a("#preview").css("top", b.pageY - c.xOffset + "px").css("left", b.pageX + c.yOffset + "px")
            })
        })
    }
}(jQuery);
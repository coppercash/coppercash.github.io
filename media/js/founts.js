/**
 * Created by Will on 12/24/14.
 */

var founts = new function() {

    function appendCSSTag(parent, href, media) {
        var link = document.createElement('link');
        link.rel  = 'stylesheet';
        link.type = 'text/css';
        link.media = media;
        link.href = href;
        parent.appendChild(link);
    }

    function importFonts(fonts, media) {
        media = typeof media !== 'undefined' ? media : 'all';

        var head = document.getElementsByTagName('head')[0];
        var fontsCount = fonts.length;
        for (var index = 0; index < fontsCount; index++) {
            var font = fonts[index];
            var href = 'http://fonts.googleapis.com/css?family=' + font;
            appendCSSTag(head, href, media);
        }
    }

    this.importFonts = importFonts;
};
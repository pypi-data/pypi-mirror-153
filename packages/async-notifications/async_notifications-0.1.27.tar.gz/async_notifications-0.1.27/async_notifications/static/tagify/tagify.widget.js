
window.addEventListener("load", function(event) {
    if (typeof document.tagify == "undefined") {

        document.tagify = {};
        var divs = document.querySelectorAll('.djtagify');
        [].forEach.call(divs, function(tag) {
           document.tagify[tag.name] = new Tagify(tag, {whitelist:[],

                 pattern: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)*[a-zA-Z]{2,}))$/,
           });
           var  controller; // for aborting the call

            var tagify=document.tagify[tag.name];
            tagify.on('input', onInput)

            function onInput( e ){
              var value = e.detail.value
              tagify.whitelist = null // reset the whitelist

              // https://developer.mozilla.org/en-US/docs/Web/API/AbortController/abort
              controller && controller.abort()
              controller = new AbortController()

              // show loading animation and hide the suggestions dropdown
              tagify.loading(true).dropdown.hide()

              fetch(tag.dataset.href+'?value=' + value, {signal:controller.signal})
                .then(RES => RES.json())
                .then(function(newWhitelist){
                  tagify.whitelist = newWhitelist // update whitelist Array in-place
                  tagify.loading(false).dropdown.show(value) // render the suggestions dropdown
                });
            }
            });
    }
});

function init() {
    var app = new Vue({
        el: '#project',
        data: {
            words : "",
            suggestions : [],
            is_active : true,
            is_searching : false
        },
        watch:{
            words : function () {
                app.is_searching = true;
                fetch("http://127.0.0.1:5000/suggest/" + app.words).then(function (result) {
                    app.is_searching = false;
                    if (result.ok){
                        result.json().then(function (data) {
                            app.is_active = true;
                            var words = data;
                            console.log(words);
                            app.suggestions = words;
                        })
                    }
                }).catch(function () {this.is_searching = false});
            }
        },
        methods:{
            update_words: function (word) {
                app.words = word;
                app.is_active = false;
            }
        }
    });
}

window.addEventListener('load', function () {
    init();
});

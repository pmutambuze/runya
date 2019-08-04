let app;
let app2;
let editor;

const FETCHING = 'FETCHING';
const FAILED = 'FAILED';
const SUCCESS = 'SUCCESS';

function strip(html){
   let doc = new DOMParser().parseFromString(html, 'text/html');
   return doc.body.textContent || "";
}

function onTextChange(event) {
    console.log(event);
    const text = strip(editor.getData());
    const words = text.trim().split(' ');
    app2.spellCheck(words);
}

function init() {
    app = new Vue({
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
                fetch("/suggest/" + language + "/" + app.words).then(function (result) {
                    app.is_searching = false;
                    if (result.ok){
                        result.json().then(function (data) {
                            app.is_active = true;
                            let words = data;
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
            },
        }
    });
    app2 = new Vue({
        el: '#spell-check',
        data: {
            isKnown: {},
            suggestions: {},
            incorrectlySpelled: [],
            wordInfo: {},
        },
        methods:{
            spellCheck: function (words) {
                console.log(words);
                let wordInfo = {};
                words.forEach(word => {
                    if (app2.isKnown[word] === undefined || app2.isKnown[word] === FAILED){
                        // app2.$set(app2.isKnown, word.substr(0, word.length - 1), undefined);
                        app2.$set(app2.isKnown, word, FETCHING);
                        fetch("/is-known/" + language + "/" + word).then(response => {
                            if(response.ok){
                                response.json().then(data => {
                                    app2.$set(app2.isKnown, word, data.isKnown);
                                })
                            } else {
                                // todo handle request failure
                                app2.$set(app2.isKnown, word, FAILED);
                            }
                        }).catch(_ => {app2.$set(app2.isKnown, word, FAILED);})
                    } else if (app2.isKnown[word] !== FETCHING) {
                        wordInfo[word] = app2.isKnown[word];
                    }
                });
                app2.wordInfo = wordInfo;
            },
        },
        watch: {
            wordInfo: function () {
                console.log('watcher');
                let incorrectlySpelledWords = [];
                if (!app2) return incorrectlySpelledWords;
                Object.keys(app2.wordInfo).forEach(
                    key => {
                        if(app2.isKnown[key] === false) incorrectlySpelledWords.push(key)
                    }
                );
                app2.incorrectlySpelled = incorrectlySpelledWords;
            }
        }
    });
}

window.addEventListener('load', function () {
    init();
    ClassicEditor
        .create( document.querySelector( '#editor' ), {

        } )
        .then(ckEditor => {
            editor = ckEditor;
            editor.editing.view.change( writer => { writer.setAttribute( 'spellcheck', 'false', editor.editing.view.document.getRoot() ); } );
            editor.model.document.on('change:data', eventInfo => {
                onTextChange(eventInfo);
            })
        })
        .catch( error => {
            console.error( error );
        } );
});

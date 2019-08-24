String.prototype.replaceAll = function(s1, s2) {
    return this.replace(
        new RegExp(  s1.replace(/[.^$*+?()[{\|]/g, '\\$&'),  'g'  ),
        s2
    );
};

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

function onTextChange() {
    localStorage.setItem('data', editor.getData());
    let text = strip(editor.getData());
    ['.', ',', '!', '?'].forEach(symbol => {
        text = text.replaceAll(symbol, '');
    });
    const words = text.trim().split(' ');
    app2.spellCheck(words);
}

function init() {
    app2 = new Vue({
        el: '#spell-check',
        data: {
            isKnown: {},
            suggestionsFor: '__________',
            suggestions: [],
            suggestionsFetching: false,
            suggestionsVisible: false,
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
                                    console.log(data);
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
            suggest: function (word) {
                app2.toggleSuggestionList(true);
                app2.suggestions = [];
                app2.suggestionsFor = word;
                app2.suggestionsFetching = true;

                fetch("/suggest/" + language + "/" + word).then(function (result) {
                    if (result.ok){
                        result.json().then(function (data) {
                            app2.suggestions = (data.length === 1 && data[0] === word) ? [] : data;
                        })
                    }
                    app2.suggestionsFetching = false;
                }).catch(function () {app2.suggestionsFetching = false;});
            },
            toggleSuggestionList: function (visible) {
                app2.suggestionsVisible = visible;
            },
            replace: function (word, suggestion) {
                editor.setData(editor.getData().replaceAll(word, suggestion));
            },
            retry: function () {
                onTextChange();
            }
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
        .create( document.querySelector( '#editor' ))
        .then(ckEditor => {
            editor = ckEditor;
            editor.editing.view.change( writer => { writer.setAttribute( 'spellcheck', 'false', editor.editing.view.document.getRoot() ); } );
            editor.model.document.on('change:data', eventInfo => {
                onTextChange();
            });
            const data = localStorage.getItem('data');
            editor.setData(data ? data : '');
            setTimeout(() => {onTextChange();}, 2000);
        })
        .catch( error => {
            console.error( error );
        } );
});

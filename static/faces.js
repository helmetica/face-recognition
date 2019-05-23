var app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        items: []  
    },
    filters: {
    },
    methods: {
        openFaceEditor: function(event) {
            display = document.getElementById('faceEditor').style.display;

            if (display == 'none' || display == '') {
                document.getElementById('faceEditor').style.display='block';
            } else {
                document.getElementById('faceEditor').style.display='none';
            }
        },
        uploadPhoto: function(event) {
            console.log('upload');
        }
    },
});

fetch('/faces_data').then(responce => {
    return responce.json()
}).then(data => {  
    app.items = data;
});
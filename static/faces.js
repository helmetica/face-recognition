var app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        items: []
    },
    filters: {
    },
    methods: {
        toogleFaceEditor: function(event) {
            display = document.getElementById('faceEditor').style.display;

            if (display == 'none' || display == '') {
                document.getElementById('faceEditor').style.display = 'block';
            } else {
                document.getElementById('faceEditor').style.display = 'none';

                $('#upload-photo').attr('src', '../static/img/avatar.png');
                document.getElementById('uploadPhotoBtn').style.display = 'block';
                document.getElementById('saveBtn').style.display = 'none';
                document.getElementById('input-lastname').value = '';
                document.getElementById('input-name').value = '';
                document.getElementById('input-fathername').value = '';
            }
        },
        uploadPhoto: function(event) {
            var file_input = document.getElementById('file-input');

            file_input.onchange = e => { 
                var file = e.target.files[0];

                if (file) {
                    var reader = new FileReader();
                    $(reader).load(function(e) { 
                        $('#upload-photo').attr('src', e.target.result);
                    });
                    reader.readAsDataURL(file);
                    document.getElementById('uploadPhotoBtn').style.display = 'none';
                    document.getElementById('saveBtn').style.display = 'block';
                }
            }

            file_input.click();
        },
        save: function(event) {

        }
    },
});

fetch('/faces_data').then(responce => {
    return responce.json()
}).then(data => {  
    app.items = data;
});
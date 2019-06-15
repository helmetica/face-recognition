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
                // document.getElementById('saveBtn').style.display = 'none';
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
                    // document.getElementById('uploadPhotoBtn').style.display = 'none';
                    // document.getElementById('saveBtn').style.display = 'block';
                }
            }

            file_input.click();
        },
        save: function(event) {

        },
        deleteFaceById: function(data) {
            var ids = data && data[0];
            if (ids && ids[0]) {
                var id = ids[0],
                    body_json = JSON.stringify({face_id: id});

                fetch('/delete_face', {
                    method: 'post',  
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }, 
                    body: body_json
                }).then(responce => {
                    return responce.text();
                }).then(data => {  
                    if (data) {
                        var i = null;
                        app.items.forEach((item, index) => { 
                            if (item['face_id'] === id) {
                                i = index;
                            }
                        })
                        if (i) {
                            app.items.splice(i, 1);
                        }
                    }
                });
            }
        }
    },
});

fetch('/faces_data').then(responce => {
    return responce.json()
}).then(data => {  
    app.items = data;
});
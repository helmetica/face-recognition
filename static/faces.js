var app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        items: [],
        lastname: null,
        name: null,
        fathername: null,
        isLastnameEmpty: false,
        isNameEmpty: false,
        isPhotoEmpty: false
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
                app.name = null;
                app.lastname = null;
                app.fathername = null;
                app.isLastnameEmpty = false;
                app.isNameEmpty = false;
                app.isPhotoEmpty = false;
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
                }
            }

            file_input.click();
        },
        checkForm: function(event) {
            var isAvatar = $('#upload-photo').attr('src') == '../static/img/avatar.png';
            app.isNameEmpty = false;
            app.isLastnameEmpty = false;
            app.isPhotoEmpty = false;

            if (!app.name || !app.lastname || isAvatar) {
                app.isNameEmpty = !app.name;
                app.isLastnameEmpty = !app.lastname;
                app.isPhotoEmpty = isAvatar;

                event.preventDefault();
            }
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
                        if (i || i === 0) {
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
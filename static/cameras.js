var app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        items: []  
    },
    filters: {
    }
});

fetch('/cameras_data').then(responce => {
    return responce.json()
}).then(data => {  
    app.items = data;
});
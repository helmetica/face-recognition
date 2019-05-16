var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    items: []  
  }
});

fetch('/events').then(responce => {
  return responce.json()
}).then(data => {  
  app.items = data;
});

var eventSource = new EventSource('/stream');

eventSource.onmessage = function(e) {
  var data_obj = '';

  try {
    data_obj = JSON.parse(e.data);
  } catch(e) {

  }

  if (data_obj) {
    app.items.unshift(data_obj);
  }   
};
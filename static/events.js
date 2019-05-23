function appendLeadingZeroes(n){
  if (n <= 9) {
    return "0" + n;
  }
  return n
}

var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    items: []  
  },
  filters: {
    getTime: function (value) {
      var date = new Date(value);
      return appendLeadingZeroes(date.getHours()) + ':' + appendLeadingZeroes(date.getMinutes()) + ':' +  appendLeadingZeroes(date.getSeconds());
    },
    getDate: function (value) {
      var date = new Date(value);
      return appendLeadingZeroes(date.getDate()) + '.' + appendLeadingZeroes((date.getMonth() + 1)) + '.' + appendLeadingZeroes(date.getFullYear());
    },
  },
  methods: {
    clearAll: function(event) {
      app.items = [];
      fetch('/events_clear');
    }
  }
});

fetch('/events_data').then(responce => {
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
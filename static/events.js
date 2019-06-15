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
    }
  },
  methods: {
    clearAll: function(event) {
      app.items = [];
      fetch('/events_clear');
    },
    deleteEventById: function(data) {
      var ids = data && data[0];
      if (ids && ids[0]) {
          var id = ids[0],
              body_json = JSON.stringify({event_id: id});

          fetch('/delete_event', {
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
                      if (item['event_id'] === id) {
                          i = index;
                      }
                  });
                  if (i || i === 0) {
                      app.items.splice(i, 1);
                  }
              }
          });
      }
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
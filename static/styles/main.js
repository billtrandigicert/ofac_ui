$(document).ready(function () {
  var dataTable = $('#ofac-table').DataTable();
  
  $('#ofac-table').editable({
      container: 'body',
      selector: 'td.disposition',
      url: '/update_list',
      title: 'disposition',
      type: 'POST',
      source: [
        {value: 'greylist', text: 'greylist'},
        {value: 'whitelist', text: 'whitelist'},
        {value: 'blacklist', text: 'blacklist'}
     ],
      validate:function(value) {
          if($.trim(value) == '')
          {
              return 'This field is required';
          }
      }
  });
});
$(document).ready(function () {
  var dataTable = $('#ofac-table').DataTable();
  $.fn.editable.defaults.mode = 'inline';

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

  $('#ofac-table').editable({
      container: 'body',
      selector: 'td.comment',
      url: '/update_list',
      title: 'comment',
      type: 'POST'
  });
  
  $("#button").click(function() {   
    var $order_id = $(this).closest("tr")  
                      .find(".order_id")     
                      .text(); 
    
    var $cert_serial_number = $(this).closest("tr")  
                      .find(".cert_serial_number")     
                      .text(); 

    var $disposition = $(this).closest("tr")  
                      .find(".disposition")     
                      .text();    
                       
    var $comment = $(this).closest("tr")  
                      .find(".comment")     
                      .text();     

    var res = {};
    res.order_id = $order_id;
    res.cert_serial_number = $cert_serial_number;
    res.disposition = $disposition;
    res.comment = $comment;
    console.log(res);
  });
});
  
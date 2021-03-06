$(document).ready(function () {
  var dataTable = $('#ofac-table').DataTable({
    "stateSave": true,
  });
  $.fn.editable.defaults.mode = 'inline';

  $('#ofac-table').editable({
      container: 'body',
      selector: 'td.disposition',
      url: '/updating_list',
      title: 'disposition',
      type: 'POST',
      send: 'always',
      source: [
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


  $('#ofac-table tbody').on('click', '.btn', function() {   
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

    var result = {
      order_id: $order_id,
      cert_serial_number: $cert_serial_number,
      disposition: $disposition,
      comment: $comment
    };

    // if ($disposition == 'greylist') {
    //   alert('Please choose disposition as whitelist or blacklist before submitting');
    // } else {
    //   $.post (
    //     url = "/update_list",
    //     result = result
    //   )
    // }

    $.post (
      url = "/update_list",
      result = result
    )
  });
});


  
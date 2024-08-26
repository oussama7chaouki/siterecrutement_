// function getCookie(name) {
//   let cookieValue = null;
//   if (document.cookie && document.cookie !== '') {
//       const cookies = document.cookie.split(';');
//       for (let i = 0; i < cookies.length; i++) {
//           const cookie = cookies[i].trim();
//           // Does this cookie string begin with the name we want?
//           if (cookie.substring(0, name.length + 1) === (name + '=')) {
//               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//               break;
//           }
//       }
//   }
//   return cookieValue;
// }
// let csrftoken = getCookie('csrftoken');
$('.accept').click(function() {
  var row = $(this).closest('tr');
  var decisionCell = row.find('.decision');
    var id_candidature = $(this).data('id_candidature');
    var user_id = $(this).data('user_id');
    console.log(id_candidature);
    console.log(user_id);


    // Call AJAX endpoint to accept candidate
    $.ajax({
      url: '/recruter/api/accept_candidature',
      headers: {'X-CSRFToken': csrftoken},
      type: 'POST',
      data: { id_candidature: id_candidature,user_id:user_id},
    dataType: 'json',
      success: function(response) {
        // Display success message
        if(response.status==200){
          decisionCell.text('Accepted');
        }
        console.log(response);
        // Update decision in table
        // $('button[data-id="' + candidateId + '"]').closest('tr').find('.decision').text('Accepted');
      },
      error: function(xhr, status, error) {
        // Display error message
        console.log('Error: ' + error);
        console.log(response.message);

      }
    });
  });
  
  $('.reject').click(function() {
    var row = $(this).closest('tr');
    var decisionCell = row.find('.decision');
    var id_candidature = $(this).data('id_candidature');
    var user_id = $(this).data('user_id');
        // Call AJAX endpoint to reject candidate
    $.ajax({
      url: '/recruter/api/reject_candidature',
      type: 'POST',
      headers: {'X-CSRFToken': csrftoken},
      data: { id_candidature: id_candidature,user_id:user_id},
       dataType: 'json',
      success: function(response) {
        // Display success message
        // $('#myTable4').load(location.href+ " #myTable4");
        if(response.status==200){
          decisionCell.text('Rejected');
        }
        console.log(response);
        // Update decision in table
        // $('button[data-id="' + candidateId + '"]').closest('tr').find('.decision').text('Rejected')

      },
      error: function(xhr, status, error) {
        // Display error message
        console.log('Error: ' + error);
      }
    });
  });


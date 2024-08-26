
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
$(document).on('submit', '#savejob', function (e) {
    e.preventDefault();
    var formData = new FormData(this);
    console.log([ ...formData ])

    $.ajax({
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        url: "api/job",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            console.log(response);
            var res = response;
            if(res.status == 400) {
                $('#errorMessage').removeClass('d-none');
                $('#errorMessage').text("fill required fileds");

            }else if(res.status == 201){


                $('#errorMessage').addClass('d-none');
                // $('#jobAddModal').removeClass('fade');
                
                // $('#jobAddModal').modal('hide');    
                const truck_modal = document.querySelector('#jobAddModal');
                const modal = bootstrap.Modal.getInstance(truck_modal);    
                modal.hide();
                
                $('#savejob')[0].reset();

                alertify.set('notifier','position', 'top-right');
                alertify.success("job created");

                $('#myTable').load(location.href + " #myTable");
                
                $('#navigationpage').load(location.href + " #navigationpage");

            }else if(res.status == 500) {
                alert(res.message);
            }
        }
    });

});

$(document).on('click', '.editjobBtn', function () {
    // ('#view_skillreq').tokenfield({
    // });
    var job_id = $(this).val();
    
    $.ajax({
        type: "GET",
        url: "api/getjob/" + job_id+"/",
        success: function (response) {
            console.log(response);
            var res = response;
            if(res.status == 404) {

                alert(res.message);
            }else if(res.status == 200){

                $('#job_id').val(res.data.id_job);
                $('#editjob_title').val(res.data.job_title);
                $('#editjob_description').val(res.data.job_description);
                $('#editjob_salaire').val(res.data.job_salaire);
                $('#editdomain').val(res.data.domain);
                $('#editformationreq').val(res.data.formationreq);
                $('#editexpreq').val(res.data.expreq);
                // $('#editskillreq').val(res.data.skillreq);
                $('#editskillreq').tokenfield('setTokens',res.data.skillreq.split(','));

                $('#jobEditModal').modal('show');
            }

        }
    });

});

$(document).on('submit', '#updatejob', function (e) {
    e.preventDefault();
    var job_id = $('#job_id').val();
    var formData = new FormData(this);
    // formData.append("update_job", true);
    console.log([ ...formData ])
    $.ajax({
        type: "PUT",
        headers: {'X-CSRFToken': csrftoken},
        url: "api/getjob/" + job_id+"/",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            
            var res = response;
            console.log(res);
            if(res.status == 400) {
                $('#errorMessageUpdate').removeClass('d-none');
                $('#errorMessageUpdate').text(res.message);

            }else if(res.status == 201){

                $('#errorMessageUpdate').addClass('d-none');

                alertify.set('notifier','position', 'top-right');
                alertify.success("job updated succefuly");
                
                $('#jobEditModal').modal('hide');
                $('#updatejob')[0].reset();

                $('#myTable').load(location.href + " #myTable");

            }
        }
    });

});

$(document).on('click', '.viewjobBtn', function () {
    // ('#editskillreq').tokenfield({
    // });
    var job_id = $(this).val();
    $.ajax({
        type: "GET",
        url: "api/getjob/" + job_id+"/",
        success: function (response) {

            var res = response;
            if(res.status == 404) {

                alert(res.message);
            }else if(res.status == 200){
console.log(res.data);

bac=["bac","bac+2","bac+3","bac+5","bac+8"]

                $('#view_job_title').text(res.data.job_title);
                $('#view_job_description').text(res.data.job_description);
                $('#view_job_salaire').text(res.data.job_salaire);
                $('#view_domain').text(res.data.domain);
                $('#view_formationreq').text(bac[res.data.formationreq]);
                $('#view_expreq').text(res.data.expreq);
                // $('#view_skillreq').text(res.data.skillreq);
$('#view_skillreq').tokenfield('setTokens',res.data.skillreq.split(','));
                $('#jobViewModal').modal('show');
            }
        }
    });
});

$(document).on('click', '.deletejobBtn', function (e) {
    e.preventDefault();

    if(confirm('Are you sure you want to delete this data?'))
    {
        var job_id = $(this).val();
        $.ajax({
            type: "DELETE",
            headers: {'X-CSRFToken': csrftoken},
            url: "api/getjob/" + job_id+"/",
            data: {
                'delete_job': true,
                'job_id': job_id
            },
            success: function (response) {

                var res = response;
                if(res.status == 500) {

                    alert(res.message);
                }else if(res.status == 204){
                    alertify.set('notifier','position', 'top-right');
                    alertify.success("deleted succefuly");

                    $('#myTable').load(location.href + " #myTable");
                    $('#navigationpage').load(location.href + " #navigationpage");

                }
            }
        });
    }
});

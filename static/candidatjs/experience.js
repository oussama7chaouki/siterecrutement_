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
  let csrftoken = getCookie('csrftoken');
$(document).on('submit', '#saveexperience', function (e) {
            e.preventDefault();
            var formData = new FormData(this);
            console.log([ ...formData ])

            $.ajax({
                type: "POST",
                url: "/candidat/api/create_experiences",
                headers: {'X-CSRFToken': csrftoken},
                data: formData,
                processData: false,
                contentType: false,
                success: function (response) {
                    
                    var res = response;
                    if(res.status == 422) {
                        $('#errorMessage1').removeClass('d-none');
                        $('#errorMessage1').text(res.message);

                    }else if(res.status == 200){

                        $('#errorMessage1').addClass('d-none');
                        $('#experienceAddModal').modal('hide');
                        $('#saveexperience')[0].reset();

                        alertify.set('notifier','position', 'top-right');
                        alertify.success(res.message);

                        $('#myTable1').load(location.href + " #myTable1");

                    }else if(res.status == 500) {
                        alert(res.message);
                    }
                }
            });

        });

        $(document).on('click', '.editexperienceBtn', function () {

            var experience_id = $(this).val();
            
            $.ajax({
                type: "GET",
                url: "/candidat/api/get_experiences/" + experience_id,
                headers: {'X-CSRFToken': csrftoken},
                success: function (response) {

                    var res = response;
                    if(res.status == 404) {

                        alert(res.message);
                    }else if(res.status == 200){

                        $('#experience_id').val(res.data.id_experience);
                        $('#experience').val(res.data.experience);
                        $('#company').val(res.data.company);
                        $('#startyear1').val(res.data.startyear);
                        $('#endyear1').val(res.data.endyear);

                        $('#experienceEditModal').modal('show');
                    }

                }
            });

        });

        $(document).on('submit', '#updateexperience', function (e) {
            e.preventDefault();
            experience_id = document.getElementById("experience_id").value;
            var formData = new FormData(this);
            console.log([ ...formData ])
            $.ajax({
                type: "PUT",
                url: "/candidat/api/update_experiences/"+experience_id,
                headers: {'X-CSRFToken': csrftoken},
                data: formData,
                processData: false,
                contentType: false,
                success: function (response) {
                    
                    var res = response;
                    if(res.status == 422) {
                        $('#errorMessageUpdate1').removeClass('d-none');
                        $('#errorMessageUpdate1').text(res.message);

                    }else if(res.status == 200){

                        $('#errorMessageUpdate1').addClass('d-none');

                        alertify.set('notifier','position', 'top-right');
                        alertify.success(res.message);
                        
                        $('#experienceEditModal').modal('hide');
                        $('#updateexperience')[0].reset();

                        $('#myTable1').load(location.href + " #myTable1");

                    }else if(res.status == 500) {
                        alert(res.message);
                    }
                }
            });

        });

        $(document).on('click', '.viewexperienceBtn', function () {

            var experience_id = $(this).val();
            $.ajax({
                type: "GET",
                url: "/candidat/api/get_experiences/" + experience_id,
                headers: {'X-CSRFToken': csrftoken},

                success: function (response) {

                    var res = response;
                    if(res.status == 404) {

                        alert(res.message);
                    }else if(res.status == 200){

                        $('#view_experience').text(res.data.experience);
                        $('#view_company').text(res.data.company);
                        $('#view_startyear1').text(res.data.startyear);
                        $('#view_endyear1').text(res.data.endyear);

                        $('#experienceViewModal').modal('show');
                    }
                }
            });
        });

        $(document).on('click', '.deleteexperienceBtn', function (e) {
            e.preventDefault();

            if(confirm('Are you sure you want to delete this data?'))
            {
                var experience_id = $(this).val();
                $.ajax({
                    type: "DELETE",
                    url: "/candidat/api/delete_experiences/"+experience_id,
                    headers: {'X-CSRFToken': csrftoken},
                    success: function (response) {

                        var res = response;
                        if(res.status == 500) {

                            alert(res.message);
                        }else{
                            alertify.set('notifier','position', 'top-right');
                            alertify.success(res.message);

                            $('#myTable1').load(location.href + " #myTable1");
                        }
                    }
                });
            }
        });


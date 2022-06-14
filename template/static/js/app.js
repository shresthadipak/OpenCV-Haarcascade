$(document).ready(function(){
    console.log('Ready!');
    $('#cel_res').hide();
    $('#cel_prob').hide();
    $('#error_msg').hide();
});


$('#submitbtn').click(function(e) {
    e.preventDefault()

    var formData = new FormData()

    var image_file = $('input[name=img_file]')[0].files[0]

    formData.append('img_file', image_file)

    $.ajax({
        type: 'POST',
        url: '/uploadimg',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
            console.log(data);
            if(data == null){
                $('#error_msg').show();
                $('#cel_res').hide();
                $('#cel_prob').hide();
            }else{
                $('#cel_res').show();
                $('#cel_prob').show();
                $('#error_msg').hide();
                $('#classify_cel').html(data[0]['class']);
                $('#classify_img').html('<img src="/static/images/'+ data[0]['class'].toLowerCase()+'.jpg" width="100" class="rounded-circle">');
                $('#amir').html(data[0]['class_probability'][0]+ '%')
                $('#prabhas').html(data[0]['class_probability'][1]+ '%')
                $('#salman').html(data[0]['class_probability'][2]+ '%')
                $('#shahrukh').html(data[0]['class_probability'][3]+ '%')
                $('#yash').html(data[0]['class_probability'][4]+ '%')
            }

        }
    });
});
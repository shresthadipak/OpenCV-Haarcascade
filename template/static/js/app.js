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
                var getMaxValue=Math.max.apply(this,data[0]['class_probability']);
                var getindex= $.inArray(getMaxValue,data[0]['class_probability']);
                // console.log(getindex);
                // console.log(data[0]['class_dictionary'])
                $.each(data[0]['class_dictionary'], function (key, record) {
                    if(record == getindex)
                    {
                        $('#classify_cel').html(key);
                        $('#classify_img').html('<img src="/static/images/'+ key.toLowerCase()+'.jpg" width="100" class="rounded-circle">');
                    }
                });

                $('#cel_res').show();
                $('#cel_prob').show();
                $('#error_msg').hide();
                // $('#classify_cel').html(data[0]['class']);
                //$('#classify_img').html('<img src="/static/images/'+ data[0]['class'].toLowerCase()+'.jpg" width="100" class="rounded-circle">');
                $('#amir').html(data[0]['class_probability'][0]+ '%')
                $('#prabhas').html(data[0]['class_probability'][1]+ '%')
                $('#salman').html(data[0]['class_probability'][2]+ '%')
                $('#shahrukh').html(data[0]['class_probability'][3]+ '%')
                $('#yash').html(data[0]['class_probability'][4]+ '%')
            }

        }
    });
});
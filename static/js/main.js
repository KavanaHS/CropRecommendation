$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.image-section-out').hide();
    $('.loader').hide();
    $('#result').hide();
	$('#btn-recipe').hide();
    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
                 $('.image-section-out').hide();
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
         $('.image-section-out').hide();
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-values')[0]);


        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',	   
            contentType: false,
            cache: false,
            data: form_data,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(data);
                $('#btn-recipe').fadeIn(600);





                console.log('Success!');
		
            },
        });
    });

$('#btn-recipe').click(function () {

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/video_feed',
            contentType: "image/png",
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#recipe').fadeIn(600);
                $('.image-section-out').html('<img src="data:image/png;base64,' + base64encode(data) + '" />');
                $('.image-section-out').show();
                console.log('Success!');
            },
        });
    });	

});
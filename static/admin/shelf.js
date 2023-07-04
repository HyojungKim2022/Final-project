$(document).ready(function () {
    var video = document.getElementById('camera-stream');
    function playVideo() {
        video.src = "grid_video_start/";
    }
    playVideo();    
});

// $(document).ready(function(){
//     $("select[name=shelf_no]").change(function () {
//         console.log($("#shelf_no").val);
//         $("#shelf_no").submit();
//     });
// });

$(document).ready(function() {
    // Capture the change event of the select element
    $('#shelf_no_select').change(function() {
        // Get the selected value
        var selectedValue = $(this).val();
        
        // Send an AJAX request to the server
        $.ajax({
            url: 'init_shelf_no', // Replace with the actual URL endpoint of your views.py file
            method: 'GET', // or 'GET' depending on your needs
            data: {
                'shelf_no': selectedValue
            },
            success: function(response) {
                // Handle the response from the server
                console.log(response);
            },
            error: function(xhr, errmsg, err) {
                // Handle any errors that occur during the AJAX request
                console.log(errmsg);
            }
        });
    });
});
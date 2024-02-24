function processData() {
    var formData = new FormData($('#data-form')[0]);
    console.log("Submitting form data:", formData); // Log the data being submitted
    $.ajax({
        url: '/process',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
            var html = '';
            console.log("Received response:", response); // Log the response received from the server
            response.forEach(function (entry) {
                html += entry.Name + '<br>';
            });
            $('#results').html(html);
        },
        error: function(error) {
            console.log("Error processing data:", error); // Log any errors encountered during the request
        }
    });
}

function downloadData() {
    console.log("Initiating download of processed data."); 
    window.location.href = '/download-txt';
}

document.getElementById('data-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
    console.log("Form submission prevented."); // Log the prevention 
    processData(); 
    this.reset(); // Reset the form fields after submission
    console.log("Form reset after submission."); // Log the form reset
});

// Preventing Enter from creating a new line in textarea and submitting the form instead
$('textarea').keydown(function(event) {
    if(event.keyCode == 13) { // 13 is the Enter key
        event.preventDefault(); // Prevent going to a new line
        console.log("Enter key pressed in textarea. Preventing new line and processing data."); // Log the prevention and action
        processData(); 
        $('#data-form')[0].reset(); // Reset the form fields after submission
    }
});


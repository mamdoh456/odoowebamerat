odoo.define('website_custom.appointment_booking_staff', function (require) {
    "use strict";
    $(document).ready(function(){





    });
    //end document ready

});
//end odoo define



        function send_form_staff(coiffure_id){
            var form_staff = document.getElementById("form_staff");
            $('#js_coiffure_id').val(coiffure_id);
            console.log('Button Clcked',coiffure_id);
            var action = form_staff.getAttribute("action");
            console.log("action===",action);
//            var action = $('#form_staff').att('action');
            form_staff.setAttribute('action',action+'/'+coiffure_id);
            form_staff.submit();
        }
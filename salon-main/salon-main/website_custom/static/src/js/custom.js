odoo.define('website_custom.appointment_booking', function(require) {
    "use strict";

    const utils = require('web.utils');
var session = require('web.session');

    $(document).ready(function() {

     console.log("session=====",session);

        // Gets the video src from the data-src on each button
        var $videoSrc;
        $('#video-btn').click(function() {
            $videoSrc = document.getElementById("video-btn").getAttribute("data-src");
        });


        // when the modal is opened autoplay it
        $('#modalVideoAbout').on('shown.bs.modal', function(e) {
            // set the video src to autoplay and not to show related video. Youtube related video is like a box of chocolates... you never know what you're gonna get
            $("#video").attr('src', $videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
        })


        // stop playing the youtube video when I close the modal
        $('#modalVideoAbout').on('hide.bs.modal', function(e) {
            // a poor man's stop video
            $("#video").attr('src', '');
        })

        $('#scrollTabs').scrollTabs();

        // Add id product in action form book (step 1)
        function changeActionFormBook(allProductSelectedIds) {
            var actionForm = $('#form_book').attr('action');
            var actionFormArray = actionForm.split("/");
            if (parseInt(actionFormArray[actionFormArray.length-1])){
                actionFormArray[actionFormArray.length-1]=allProductSelectedIds[0];
            }else{
                actionFormArray.push(allProductSelectedIds[0]);
            }
            $('#form_book').attr('action',actionFormArray.join('/'))
        }

        function getProductsSelected() {
            var allProductSelectedIds = [];

            $("input:checkbox[name^=checkboxProduct]:checked").each(function() {
                allProductSelectedIds.push($(this).val());
            });

            if (allProductSelectedIds.length) {
                changeActionFormBook(allProductSelectedIds);
                $('.js_no_service_selected').hide();
                $('.js_box_action_book').addClass('show');
            } else {
                $('.js_no_service_selected').show();
                $('.js_box_action_book').removeClass('show');
            }
            let myjson = {
                params: {
                    products_ids: allProductSelectedIds
                }
            };
            jQuery.ajax({
                type: "POST",
                url: "/get/products/invoice/book",
                dataType: "json",
                async: true,
                data: JSON.stringify(myjson),
                contentType: "application/json; charset=utf-8",
                success: function(data) {
                    let parsed_data = JSON.parse(data["result"]);
                    var list_product_html = '';
                    parsed_data[0].products.forEach(function(item) {
                        list_product_html += '<li>' +
                            '<div class="d-flex align-items-start">' +
                            '<div class="box_info_product">' +
                            '<p class="mb-1">' + item.name + '</p>' +
//                            '<p class="text-muted m-0">'+ item.time +'</p>' +
                            '</div>' +
                            '<div class="box_price_product ml-auto text-right">SAR ' + item.list_price + '</div>' +
                            '</div>' +
                            '</li>'
                    });
                    if (list_product_html != '') {
                        list_product_html = '<ul class="list_product_invoice_book">' + list_product_html + '</ul>';
                    }
                    document.getElementById('js_list_product_invoice_book').innerHTML = list_product_html;
                    document.getElementById('js_total_invoice_book').innerHTML = parsed_data[0].total;
                    document.getElementById('js_total_invoice_book_2').innerHTML = parsed_data[0].total;
                    if(parsed_data[0].products.length>1){
                        document.getElementById('js_nbr_product_invoice_book').innerHTML = parsed_data[0].products.length.toString() + ' services';
                    }else{
                        document.getElementById('js_nbr_product_invoice_book').innerHTML = parsed_data[0].products.length.toString() + ' service';
                    }
                },
                failure: function(data) {
                    console.log(JSON.stringify(data));
                },
            });

        }
        $('input[name^="checkboxProduct"]').click(function() {
            getProductsSelected();
        });
        const formBook = document.getElementById("form_book");
        if(formBook){
            getProductsSelected();
        }
        // Show alert availibility staff
        $('.form-check.disabled').click(function() {
            $('#availablityStaffModal').modal('show')
        });



        // onLoadScrollTabs
        function onLoadScrollTabs() {
            // time
            var st = $('#timeScrollTabs').scrollTabs({
                left_arrow_size: 64,
                right_arrow_size: 64,
                click_callback: function(e) {
                    var rel = $(this).attr('rel');
                    document.querySelectorAll('.card-box').forEach(function(el) {
                        $(".card-box").removeClass("active");
                        $("#" + rel).addClass("active");
                    });
                }
            });
            if (st) {
                var first_element = $('#timeScrollTabs .scroll_tab_first')
                var rel = first_element.attr('rel');
                var slot_data = $("input[name='slot_date']").val();
                if (slot_data) {
                    $('#timeScrollTabs .scroll_tab_inner a[rel="slot' + slot_data + '"]').addClass('tab_selected');
                    $("#slot" + slot_data).addClass("active");
                } else {
                    $('#timeScrollTabs .scroll_tab_first').addClass('tab_selected');
                    $("#" + rel).addClass("active");
                }
                setTimeout(function() {
                    $('.js_loading').hide();
                    $('.js_tabs_scroll').removeClass('d-none');
                }, 2000);
            }
        }
        window.onload = onLoadScrollTabs();
        // end onLoadScrollTabs

        // fom time
        $('.js_appointment_slot').click(function() {
            var slotdate_id = $(this).parent().data('slotdate-id');
            var slotline_id = $(this).data('slotline-id');
            $("input[name='slot_date']").val(slotdate_id);
            $("input[name='schedule_slot_id']").val(slotline_id);
            $('#form_time').submit();
        });
        //end form time



        //prev_step_booking
        $('.prev_step_booking').click(function() {
            const pathname = window.location.pathname;
            const arrayPath = pathname.split("/");
            const activePage = arrayPath[arrayPath.length - 1];
            if (activePage == 'personaldata') {
                var path = pathname.replace('/personaldata', '/time');
                var form = document.getElementById('form_personal_data');
                form.action = path;
                form.submit();
            } else if (activePage == 'time') {
                var path = pathname.replace('/time', '/staff');
                var form = document.getElementById('form_time');
                form.action = path;
                form.submit();
            } else if (activePage == 'staff') {
                var path = pathname.replace('/staff', '');
                var form = document.getElementById('form_staff');
                form.action = path;
                form.submit();
            } else if (activePage == 'booking') {
                var path = pathname.replace('/booking', '/services');
                window.location.href = path;
            }
        });
        //end prev_step_booking

        function validateMobile(thisObj) {
          let fieldValue = thisObj.val();
          let pattern = /^(009665|9665|\+9665|05|5)(5|0|3|6|4|9|1|8|7)([0-9]{7})$/;
          if (pattern.test(fieldValue)) {
              $(thisObj).removeClass('is-invalid');
    //        $(thisObj).addClass('is-valid');
          } else {
    //          $(thisObj).removeClass('is-valid');
            $(thisObj).addClass('is-invalid');
          }
        }
        $('#phone input').on('change', function () {
            validateMobile($(this))
        })
        $('#phone input').on('keydown', function (event) {
            return ( event.ctrlKey || event.altKey
                    || (47<event.keyCode && event.keyCode<58 && event.shiftKey==false)
                    || (95<event.keyCode && event.keyCode<106)
                    || (event.keyCode==8) || (event.keyCode==9)
                    || (event.keyCode>34 && event.keyCode<40)
                    || (event.keyCode==46) )
        })

        $('#birthday').datetimepicker({
            format: "YYYY/MM/DD",
            timepicker:false,
            maxDate: new Date(),
            minDate: moment({ y: 1920 }),
        });


    });
    //end document ready
});
//end odoo define




$(function() {


    $('#scrollTabs a[href^="#"]').click(function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html,body').animate({
                    scrollTop: target.offset().top
                }, 1000);
                $("#scrollTabs a").removeClass("tab_selected");
                $(this).addClass("tab_selected");
                return false;
            }
        }
    });
    document.getElementById('wrapwrap').addEventListener('scroll', function() {
        $("section").each(function() {
            if (ScrollView($(this))) {
                var id = $(this).attr("id");
                $("#scrollTabs a").removeClass("tab_selected");
                $("#scrollTabs a[href='#" + id + "']").addClass("tab_selected");
            }
        });
    }, false);

    function ScrollView(element) {
        var win = $(window);
        var winTop = win.scrollTop();
        var winBottom = winTop + win.height();
        var elementTop = element.offset().top;
        var elementBottom = elementTop + element.height();

        if ((elementBottom <= winBottom) && (elementTop >= winTop)) {
            return true;
        }
        return false;
    }
});



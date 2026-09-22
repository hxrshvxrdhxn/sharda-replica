/***
 * Javascript For All Sharda Pages
 * 
 * This script is intended to provide all client side functionality 
 * required for Techgig Project
 * 
 * Author   : Arun George
 * Created  : 20 Aug, 2018
 */
Sharda_CommonFunction = new function () {
    var $instance = this;

    $instance.init = function () {

        $('[data-toggle="tooltip"]').tooltip();

        $("#apply-to-sharda .more-info").click(function () {
            //$("#apply-to-sharda .overlay").css("opacity", "1");
            $("#apply-to-sharda .overlay").show();
        });
        $("#apply-to-sharda .close-overlay").click(function () {
            //$("#apply-to-sharda .overlay").css("opacity", "0");
            $("#apply-to-sharda .overlay").hide();
        });

        $(window).on('scroll', function (e) {
            var left = $(this).scrollLeft();
            $('.scrolling-menu').css('left', -left);
        });
        $(".journal-main-menu").click(function () {
            $(this).toggleClass("active");
            $("#" + this.id + " .journal-sub-menu").toggle("500");
        });
		
		$("#notification .bell-icon").click(function () {
            $("#notification .content").toggleClass("active");
        });
		$("#notification .content header .close").click(function () {
            $("#notification .content").removeClass("active");
        });

        //$("#banner").height($("#banner .banner-video").height()); 

        // $(document).ready(function() {

        //     var divHeight = $('#banner').height();

        //     $('#banner .banner-video').css('min-height', divHeight + 'px');
        //     $('#banner').css('min-height', divHeight + 'px');

        // });


        /***
        $('#banner .playpause').click(function () {
			
			$("#playerID").empty();
			$("#playerID").replaceWith('<div class="modal-body" id="playerID"><iframe width="970" height="450" src="https://www.youtube.com/embed/bA4-FRJ5afc?autoplay=1" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>');
			$("#banner .video").get(0).play();
			$('.video').attr('loop','loop');
			$(this).fadeOut();
		});
		$('#closeVideo').click(function() {
			 $("#playerID").empty();
			 $("#playerID").replaceWith('<div class="modal-body" id="playerID"><iframe width="970" height="450" src="https://www.youtube.com/embed/bA4-FRJ5afc" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe></div>');
			 
		});
				
		 */
        $('#banner .playpause').click(function () {
            var mediaVideo = $("#banner video").get(0);
            if (mediaVideo.paused) {
                mediaVideo.play();
            } else {
                mediaVideo.pause();
            }
            $("#banner .playpause").toggleClass("active");
        });

        $("#live-events .live-events-placeholder").click(function () {
            $("#live-events").toggleClass("active");
        });

        $('body').click(function () {
            $('#live-events').removeClass("active");
        });

        $('#live-events').click(function (event) {
            event.stopPropagation();
        });

       /* $(window).scroll(function () {
            var scroll = $(window).scrollTop();
            if (scroll) {
                $("#live-events").removeClass("active");
            }
        });
		*/
        $(".smooth-scroll").click(function () {
            var href = $(this).attr('href');
            $(".smooth-scroll").parent().removeClass("active");
            $(this).parent().addClass("active");

            $('html, body').animate({
                scrollTop: $(href).offset().top - 30
            }, 1000);

        });

        $(".section-scroll").click(function () {
            var href = $(this).attr('href');
            $(".section-scroll").parent().removeClass("active");
            $(this).parent().addClass("active");

            $('html, body').animate({
                scrollTop: $(href).offset().top - 50
            }, 1000);

        });

        $(document).on("click", "#scroll-top-icon", function () {
            $("html, body").animate({ scrollTop: 0 }, 1000);
        });
		$(window).scroll(function () {
            var windowScroll = $(window).scrollTop();
            var topScroll = 0;

            if (windowScroll > 700) {
                $("#scroll-top-icon").addClass('active'); 
               
            } else {
                $("#scroll-top-icon").removeClass('active');
            }
            
			var href = document.location.href;
			var lastPathSegment = href.substr(href.lastIndexOf('/') + 1);
			if(lastPathSegment=='') {
				
				if (windowScroll > 200) {
				   $("#live-events").removeClass('active');
				} else {
					 $("#live-events").addClass('active');
				}
            
			}  else {
				$("#live-events").removeClass('active');
			}
        });

        $('#main-navigation .menu-btn').click(function () {
            $(this).toggleClass("active");
            $('#main-navigation > ul').slideToggle();
            $('body').toggleClass("non-scroll");
        });



        if ($(window).width() < 767) {
            $("#main-navigation .accordion").on("click", function () {
                $(this).parent().toggleClass("active");
                $(this).parent().find("#main-navigation .dropdown").slideToggle();
                return false;
            });

        }

        $(".smooth_scroll").click(function () {
            var href = $(this).attr('href');
            $(".smooth_scroll").parent().removeClass("active");
            $(this).parent().addClass("active");

            $('html, body').animate({
                scrollTop: $(href).offset().top - 100
            }, 1000);

        });

        // Show hide content on Para 
        $(document).on("click", ".read-more", function () {
            var moretext = "Read More <i class='icon-arrow-down-circle icons'></i>";
            var lesstext = "Read Less <i class='icon-arrow-up-circle icons'></i>";

            if ($(this).hasClass("less")) {
                $(this).removeClass("less");
                $(this).html(moretext);
            } else {
                $(this).addClass("less");
                $(this).html(lesstext);
            }
            $(this).parent().find('.hidden-txt').toggle();
            //$(this).parent().find('.dotted').toggle();
            return false;
        });

        $(document).on("click", ".form1 .btn-group .select-option", function () {

            $(this).parent().find(".select-option").removeClass("active");

            if ($(this).hasClass("active")) {
                $(this).removeClass("active");
            } else {
                $(this).addClass("active");
            }
        });
		
		$(window).scroll(function () {
            var windowScroll = $(window).scrollTop();
            var onScrollSpace1 = ($("#header").innerHeight()); 
            if (windowScroll >= onScrollSpace1) {
                $("#page-head.sticky").addClass('dark');
                

            } else {
                $("#page-head.sticky").removeClass('dark');
               
            }

        });


        $(window).scroll(function () {
            var windowScroll = $(window).scrollTop();
            var onScrollSpace1 = ($("#header").innerHeight() + $("#secondary-banner").innerHeight() + $("#breadcrumbs").innerHeight());
            if (windowScroll >= onScrollSpace1) {
                $(".school-nav").addClass('fixed');

            } else {
                $(".school-nav").removeClass('fixed');
            }

        });

        $(window).scroll(function () {
            var windowScroll = $(window).scrollTop();
            var onScrollSpace1 = ($("#header").innerHeight() + $("#school-banner").innerHeight() + $("#breadcrumbs").innerHeight());
            if (windowScroll >= onScrollSpace1) {
                $(".school-detail-nav").addClass('fixed');

            } else {
                $(".school-detail-nav").removeClass('fixed');
            }

        });

        $(window).scroll(function () {
            var windowScroll = $(window).scrollTop();
            var onScrollSpace1 = ($("#header").innerHeight() + $(".int-banner").innerHeight() + $("#breadcrumbs").innerHeight());
            if (windowScroll >= onScrollSpace1) {
                $(".global-nav").addClass('fixed');

            } else {
                $(".global-nav").removeClass('fixed');
            }

        });

        $(window).scroll(function () {
            var windowScroll = $(window).scrollTop();
            var onScrollSpace1 = ($("#header").innerHeight() + $("#faculty-banner").innerHeight());
            if (windowScroll >= onScrollSpace1) {
                $("#filters").addClass('fixed');

            } else {
                $("#filters").removeClass('fixed');
            }

        });

        $(window).scroll(function () {
            if ($(window).scrollTop() <= 30) {
                $('#header').addClass('dark');
            } else {
                $('#header').removeClass('dark');
            }
        });

        $(window).scroll(function () {
            var windowScroll = $(window).scrollTop();

            var onScrollSpace1 = ($("#header").innerHeight() + $("#secondary-banner").innerHeight() + $("#breadcrumbs").innerHeight());

            if (windowScroll >= onScrollSpace1) {
                $("#campus-overview .campus-tab").addClass('fixed');

            } else {
                $("#campus-overview .campus-tab").removeClass('fixed');
            }
        });

        $(window).scroll(function () {
            var windowScroll = $(window).scrollTop();

            var onScrollSpace1 = ($("#header").innerHeight() + $("#secondary-banner").innerHeight() + $("#breadcrumbs").innerHeight() + $(".course-short-info").innerHeight() + 55);

            if (windowScroll >= onScrollSpace1) {
                $(".course-info-nav").addClass('fixed');

            } else {
                $(".course-info-nav").removeClass('fixed');
            }
        });



        $(".custom-selectbox input").change(function () {

            if ($(this).attr('type') == 'checkbox') {

                var checkVal = $($(this).parents(".custom-selectbox").find("input:checkbox:checked")).map(function () {
                    return this.value;
                })
                    .get()
                    .join(", ");

                $(this).parents(".custom-selectbox").find(".btn").text(checkVal);

                if ($(this).parents(".custom-selectbox").find("input:checkbox:checked").length == 0 && !this.checked) {
                    this.checked = true;
                    $(this).parents(".custom-selectbox").find(".btn").text($(this).val());
                }

            } else if ($(this).attr('type') == 'radio') {
                $(this).parents(".custom-selectbox").find(".btn").text($(this).val());
                $(this).parents(".custom-selectbox").find(".btn").addClass("selected");
            }
        });

        function setHeight() {
            windowHeight = $(window).innerHeight();
            $('#apply-to-sharda .left-panel').css('min-height', windowHeight);
            $('#apply-to-sharda .right-panel').css('min-height', windowHeight);
        }
        setHeight();

        $(window).resize(function () {
            setHeight();
        });

        $("#address").focus(function () {
            $("#msform ul li").removeClass("hide");
        });

        $(document).on("click", "#page-header .category-menu-btn", function () {
            var moretext = '<i class="fa fa-chevron-circle-down" aria-hidden="true"></i>';
            var lesstext = '<i class="fa fa-chevron-circle-up" aria-hidden="true"></i>';

            if ($(this).hasClass("less")) {
                $(this).removeClass("less");
                $(this).html(moretext);
            } else {
                $(this).addClass("less");
                $(this).html(lesstext);
            }
            $(this).prev('#page-header ul').slideToggle();
            return false;
        });

        // Show hide content on skilltest banner
        $(document).on("click", ".skill-show-hide-lnk", function () {
            var moretext = "Read More";
            var lesstext = "Read Less";

            if ($(this).hasClass("less")) {
                $(this).removeClass("less");
                $(this).html(moretext);
                /*$("html, body").animate({ scrollTop: 0 }, 1000);*/

            } else {
                $(this).addClass("less");
                $(this).html(lesstext);
                /*$("html, body").animate({ scrollTop: 100 }, 1000);*/
            }

            $(this).parent().find('.hidden-txt').toggle();
            $(this).parent().find('.dotted').toggle();
            return false;
        });
    };

    $instance.round_slider = function () {
        // impact
        $('#impact .slider').on('init', function (slick) {
            // number/symbol animation
            $('#impact .numbers.slide1').removeClass('inactive');
            var slideCount = 0;
            $('#impact .numbers').each(function () {
                slideCount++;
                var numberCount = 0;
                $(this).find('.number, .symbol').each(function () {
                    numberCount++;
                    if ($(this).hasClass('number')) {
                        var elName = 'slide' + slideCount.toString() + '-number' + numberCount.toString();
                        var varName = 'slide' + slideCount + '-number' + numberCount;
                    }
                    if ($(this).hasClass('symbol')) {
                        var elName = 'slide' + slideCount.toString() + '-symbol';
                        var varName = 'slide' + slideCount + '-symbol';
                    };
                    window[varName] = new SVGMorpheus(document.querySelector('#' + elName));
                    if (slideCount == 1) {
                        var startName = elName + '-group';
                        window[varName].to(startName, { rotation: 'none', duration: 500, easing: 'quart-in-out' });
                    } else {
                        var startName = elName + '-circle';
                        window[varName].to(startName, { rotation: 'none', duration: 500, easing: 'quart-in-out' });
                    }
                });
            });
            // backgrounds		
            $('#impact .backgrounds [data-position="top"]').addClass('background-1-active');
            $('#impact .backgrounds [data-position="bottom"]').addClass('background-2-active');
        });
        $('#impact .slider').slick({
            dots: true,
            arrows: false,
            infinite: true,
            fade: true,
            autoplay: true,
            arrows: true,
            prevArrow: '<div class="icon arrow left"></div>',
            nextArrow: '<div class="icon arrow right"></div>',
            appendArrows: '#impact .slider-arrows',
            appendDots: '#impact .slider-dots',
            customPaging: function (slider, i) {
                var thumb = $(slider.$slides[i]).data('thumb');
                return '<a>' + thumb + '</a>';
            },
            speed: 300,
            autoplaySpeed: 5000,
            slidesToShow: 1,
            slidesToScroll: 1,
            responsive: [{
                breakpoint: 768,
                settings: {}
            }],
        });
        $('#impact .slider').on('beforeChange', function (event, slick, currentSlide, nextSlide) {
            // current/next slide
            currentSlide = currentSlide + 1;
            nextSlide = nextSlide + 1;
            // number/symbol animation
            $('#impact .numbers').addClass('inactive');
            $('#impact .numbers.slide' + nextSlide).removeClass('inactive');
            $('#impact .numbers.slide' + currentSlide).each(function () {
                var numberCount = 0;
                $(this).find('.number, .symbol').each(function () {
                    numberCount++;
                    if ($(this).hasClass('number')) {
                        var elName = 'slide' + currentSlide.toString() + '-number' + numberCount.toString() + '-circle';
                        var varName = 'slide' + currentSlide + '-number' + numberCount;
                    }
                    if ($(this).hasClass('symbol')) {
                        var elName = 'slide' + currentSlide.toString() + '-symbol-circle';
                        var varName = 'slide' + currentSlide + '-symbol';
                    }
                    window[varName].to(elName, { rotation: 'none', duration: 100 });
                });
            });
            $('#impact .numbers.slide' + nextSlide).each(function () {
                var numberCount = 0;
                $(this).find('.number, .symbol').each(function () {
                    numberCount++;
                    if ($(this).hasClass('number')) {
                        var elName = 'slide' + nextSlide.toString() + '-number' + numberCount.toString() + '-group';
                        var varName = 'slide' + nextSlide + '-number' + numberCount;
                    }
                    if ($(this).hasClass('symbol')) {
                        var elName = 'slide' + nextSlide.toString() + '-symbol-group';
                        var varName = 'slide' + nextSlide + '-symbol';
                    }
                    window[varName].to(elName, { rotation: 'none', duration: 650, easing: 'quart-in-out' });
                });
            });
            // backgrounds
            if (currentSlide == 1) {
                $('#impact .backgrounds [data-position="bottom"]').removeClass();
                $('#impact .backgrounds [data-position="bottom"]').addClass('background-1-active');
            }
            if (currentSlide == 2) {
                $('#impact .backgrounds [data-position="bottom"]').removeClass();
                $('#impact .backgrounds [data-position="bottom"]').addClass('background-2-active');
            }
            if (currentSlide == 3) {
                $('#impact .backgrounds [data-position="bottom"]').removeClass();
                $('#impact .backgrounds [data-position="bottom"]').addClass('background-3-active');
            }
            if (currentSlide == 4) {
                $('#impact .backgrounds [data-position="bottom"]').removeClass();
                $('#impact .backgrounds [data-position="bottom"]').addClass('background-4-active');
            }
            if (currentSlide == 5) {
                $('#impact .backgrounds [data-position="bottom"]').removeClass();
                $('#impact .backgrounds [data-position="bottom"]').addClass('background-5-active');
            }
            if (currentSlide == 6) {
                $('#impact .backgrounds [data-position="bottom"]').removeClass();
                $('#impact .backgrounds [data-position="bottom"]').addClass('background-1-active');
            }
            if (nextSlide == 1) {
                $('#impact .backgrounds [data-position="top"]').removeClass();
                $('#impact .backgrounds [data-position="top"]').addClass('background-1-active');
            }
            if (nextSlide == 2) {
                $('#impact .backgrounds [data-position="top"]').removeClass();
                $('#impact .backgrounds [data-position="top"]').addClass('background-2-active');
            }
            if (nextSlide == 3) {
                $('#impact .backgrounds [data-position="top"]').removeClass();
                $('#impact .backgrounds [data-position="top"]').addClass('background-3-active');
            }
            if (nextSlide == 4) {
                $('#impact .backgrounds [data-position="top"]').removeClass();
                $('#impact .backgrounds [data-position="top"]').addClass('background-4-active');
            }
            if (nextSlide == 5) {
                $('#impact .backgrounds [data-position="top"]').removeClass();
                $('#impact .backgrounds [data-position="top"]').addClass('background-5-active');
            }
            if (nextSlide == 6) {
                $('#impact .backgrounds [data-position="top"]').removeClass();
                $('#impact .backgrounds [data-position="top"]').addClass('background-2-active');
            }
        });
    };


    $instance.sharda_nav = function () {
        $.getScript("https://sharda.ac.in/assets/js/onepagenav.js")
            .done(function () {
                $('.school-nav ul,.campus-tab ul').onePageNav({
                    currentClass: 'active',
                    scrollOffset: 70,
                    //scrollThreshold: 0.10,
                    changeHash: false,
                    filter: ':not(.external)'
                });

            })
            .fail(function () {
                console.log('OnePageNav not loaded');
            });
    };

    $instance.mansonry = function () {
        $.getScript("https://sharda.ac.in/assets/js/mansonry.js")
            .done(function () {

                $('.grid').masonry({
                    itemSelector: '.grid-item',
                    isAnimated: true,
                    //columnWidth: 160 
                });
            })
            .fail(function () {
                console.log('Mansonary not loaded');
            });
    };

    //jQuery time
    var current_fs, next_fs, previous_fs; //fieldsets
    var left, opacity, scale; //fieldset properties which we will animate
    var animating; //flag to prevent quick multi-click glitches

    $(".next").click(function () {
        if (animating) return false;
        animating = true;

        current_fs = $(this).parent();
        next_fs = $(this).parent().next();

        //activate next step on progressbar using the index of next_fs
        $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

        //show the next fieldset
        next_fs.show();
        //hide the current fieldset with style
        current_fs.animate({ opacity: 0 }, {
            step: function (now, mx) {
                //as the opacity of current_fs reduces to 0 - stored in "now"
                //1. scale current_fs down to 80%
                scale = 1 - (1 - now) * 0.2;
                //2. bring next_fs from the right(50%)
                left = (now * 50) + "%";
                //3. increase opacity of next_fs to 1 as it moves in
                opacity = 1 - now;
                current_fs.css({
                    'transform': 'scale(' + scale + ')',
                    'position': 'relative'

                });
                next_fs.css({ 'left': left, 'opacity': opacity });
            },
            duration: 800,
            complete: function () {
                current_fs.hide();
                animating = false;
            },
            //this comes from the custom easing plugin
            easing: 'easeInOutBack'
        });
    });

    $(".previous").click(function () {
        if (animating) return false;
        animating = true;

        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();

        //de-activate current step on progressbar
        $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

        //show the previous fieldset
        previous_fs.show();
        //hide the current fieldset with style
        current_fs.animate({ opacity: 0 }, {
            step: function (now, mx) {
                //as the opacity of current_fs reduces to 0 - stored in "now"
                //1. scale previous_fs from 80% to 100%
                scale = 0.8 + (1 - now) * 0.2;
                //2. take current_fs to the right(50%) - from 0%
                left = ((1 - now) * 50) + "%";
                //3. increase opacity of previous_fs to 1 as it moves in
                opacity = 1 - now;
                current_fs.css({ 'left': left });
                previous_fs.css({ 'transform': 'scale(' + scale + ')', 'opacity': opacity });

            },
            duration: 800,
            complete: function () {
                current_fs.hide();
                animating = false;
            },
            //this comes from the custom easing plugin
            easing: 'easeInOutBack'
        });
    });

    $(".submit").click(function () {
        return false;
    });

    $instance.set_slider_list = function (container_id, content_width, display_count, scroll_count, duration_val, auto_val, scroll_direction) {

        content_width = (typeof content_width === "undefined") ? 270 : content_width;
        display_count = (typeof display_count === "undefined") ? 3 : display_count;
        scroll_count = (typeof scroll_count === "undefined") ? 1 : scroll_count;
        duration_val = (typeof duration_val === "undefined") ? 500 : duration_val;
        scroll_direction = (typeof scroll_direction === "undefined") ? 'left' : duration_val;
        auto_val = (typeof auto_val === "undefined") ? false : auto_val;

        $.getScript("https://sharda.ac.in/assets/js/carouFredSel-6.0.5-packed.js")
            .done(function () {
                $('#' + container_id + ' ul').carouFredSel({
                    responsive: true,
                    width: '100%',
                    circular: true,
                    infinite: false,
                    direction: scroll_direction,
                    auto: auto_val,
                    scroll: {
                        items: scroll_count,
                        duration: duration_val
                    },
                    prev: '#' + container_id + ' .previous-btn',
                    next: '#' + container_id + ' .next-btn',
                    items: {
                        width: content_width,
                        height: 'variable',
                        visible: {
                            min: 1,
                            max: display_count
                        }
                    },
                    pagination: '#' + container_id + ' .controls'
                });

                var sliderHeight = $('#' + container_id + ' ul li').height();
                $('#' + container_id + ' .caroufredsel_wrapper').height(sliderHeight);

                $('#' + container_id + ' .previous-btn,#' + container_id + ' .next-btn').show();
            })
            .fail(function () {
                console.log('carouFredSel not loaded');
            });


    };



};

function setSlider(container_id, content_width, display_count, scroll_count, duration_val, auto_val, scroll_direction) {

    content_width = (typeof content_width === "undefined") ? 270 : content_width;
    display_count = (typeof display_count === "undefined") ? 3 : display_count;
    scroll_count = (typeof scroll_count === "undefined") ? 1 : scroll_count;
    duration_val = (typeof duration_val === "undefined") ? 500 : duration_val;
    scroll_direction = (typeof scroll_direction === "undefined") ? 'left' : duration_val;
    auto_val = (typeof auto_val === "undefined") ? false : auto_val;


    $('#' + container_id + ' ul').carouFredSel({
        responsive: true,
        width: '100%',
        circular: true,
        infinite: false,
        direction: scroll_direction,
        auto: auto_val,
        scroll: {
            items: scroll_count,
            duration: duration_val
        },
        prev: '#' + container_id + ' .previous-btn',
        next: '#' + container_id + ' .next-btn',
        items: {
            width: content_width,
            height: 'variable',
            visible: {
                min: 1,
                max: display_count
            }
        },
        pagination: '#' + container_id + ' .controls'
    });

    var sliderHeight = $('#' + container_id + ' ul li').height();
    $('#' + container_id + ' .caroufredsel_wrapper').height(sliderHeight);

    $('#' + container_id + ' .previous-btn,#' + container_id + ' .next-btn').show();



}


/***
 * Javascript For All Sharda Pages
 * 
 * This script is intended to provide all client side functionality 
 * required for Techgig Project
 * 
 * Author   : Amit
 * Created  : 07 03, 2018
 */

$(document).ready(function (lat, long) {
    $('#search_faclty').on('keyup', function (e) {
        var q = e.target.value.replace('.', '').toLowerCase();

        $('div.staff-container').each(function () {
            var name = this.children[0].textContent.replace('.', '').toLowerCase();
            if (name.search(q) < 0) {
                $(this).hide();
                $('.first-letter').hide();
            } else {
                $(this).show();
                $('.first-letter').show();
            }

        });
    });

    $('#country').change(function () {
        var country_code = $(this).val();
        if (country_code) {
            $.ajax({

                url: $('body').attr('data-base-url') + 'contact/getcountrycode',
                method: 'post',
                data: {
                    id: $(this).attr('data-src'),
                    country_code: country_code
                }
            }).done(function (response) {
                $('#country_code').val(response);
                return false;
            });
        }
    });


    $('#school_id').on('change', function () {
        this.form.submit();
    });

    $('#department').on('change', function () {
        this.form.submit();
    });

    $("#back_step_one").on("click", function (e) {
        $('#undergraduate-lnk').addClass('active');
        $('#discipline-lnk').removeClass('active');
    });

    $("#back_step_two").on("click", function (e) {
        $('#discipline-lnk').addClass('active');
        $('#select-course-lnk').removeClass('active');
    });

    $("#mob_department_link").on("click", function (e) {
        $('#school-lnk').addClass('active');
        $('#deparement-lnk').removeClass('active');
    });

    /*
     * Onchange Get Newsletter details
     */
    $('#school_newsletters').change(function () {
        var school_id = $(this).val();
        $.ajax({

            url: $('body').attr('data-base-url') + 'connect/getNewsletters',
            method: 'post',
            data: {
                id: $(this).attr('data-src'),
                school_id: school_id
            }
        }).done(function (response) {
            $('.download-newsletter').html('');
            $('.download-newsletter').html(response);

        });
    });

    $('#school_gallery').on('change', function () {
        this.form.submit();
    });
    /*
     * Onchange Get Newsletter details
     */
    $('#sharda_experience, #country_id').change(function () {
        this.form.submit();
    });

    /*
     * Onchange Get Newsletter details
     */
    $('#school_results').change(function () {
        var school_id = $(this).val();
        $.ajax({

            url: $('body').attr('data-base-url') + 'admissions/getExamResults',
            method: 'post',
            data: {
                id: $(this).attr('data-src'),
                school_id: school_id
            }
        }).done(function (response) {
            $('.download-results').html('');
            $('.download-results').html(response);

        });
    });

    /*
     * Onchange Get Examination Schedule
     */
    $('#school_schedule').change(function () {
        var school_id = $(this).val();
        $.ajax({

            url: $('body').attr('data-base-url') + 'admissions/getExamSchedule',
            method: 'post',
            data: {
                id: $(this).attr('data-src'),
                school_id: school_id
            }
        }).done(function (response) {
            $('.download-results').html('');
            $('.download-results').html(response);

        });
    });

    /*
     * Onchange Get Course details
     */

    $('#programmecourse').change(function () {
        var programme_id = $(this).val();
        $.ajax({

            url: $('body').attr('data-base-url') + 'apply/getProgrammeDiscipline',
            method: 'post',
            data: {
                id: $(this).attr('data-src'),
                programme_id: programme_id
            }
        }).done(function (response) {

            $('#disciplinecourse').html('');
            $('#disciplinecourse').append($('<option>').text(' -- Select Discipline -- ').attr('value', ''));
            $.each(response, function (i, value) {
                $('#disciplinecourse').append($('<option>').text(value).attr('value', i));

            });
        });
    });

    $('#disciplinecourse').change(function () {
        var programme_id = $("#programmecourse").val();
        var discipline_id = $(this).val();
        $.ajax({

            url: $('body').attr('data-base-url') + 'admissions/getdisciplinecourse',
            method: 'post',
            data: {
                id: $(this).attr('data-src'),
                programme_id: programme_id,
                discipline_id: discipline_id
            }
        }).done(function (response) {
            $('#pagination_div').hide();
            $('.course-response').html('');
            $('.course-response').html(response);

        });
    });

    $('#globalprogrammecourse').change(function () {
        var programme_id = $(this).val();
        $.ajax({

            url: $('body').attr('data-base-url') + 'admissions/getProgrammeDiscipline',
            method: 'post',
            data: {
                id: $(this).attr('data-src'),
                programme_id: programme_id
            }
        }).done(function (response) {

            $('#globaldisciplinecourse').html('');
            $('#globaldisciplinecourse').append($('<option>').text(' -- Select Discipline -- ').attr('value', ''));
            $.each(response, function (i, value) {
                $('#globaldisciplinecourse').append($('<option>').text(value).attr('value', i));

            });
        });
    });

    $('#globaldisciplinecourse').change(function () {
        var programme_id = $("#globalprogrammecourse").val();
        var discipline_id = $(this).val();
        $.ajax({

            url: $('body').attr('data-base-url') + 'international/getdisciplinecourse',
            method: 'post',
            data: {
                id: $(this).attr('data-src'),
                programme_id: programme_id,
                discipline_id: discipline_id
            }
        }).done(function (response) {
            feePagination(response);
        });
    });


    /*  course fee page by ashutosh */


    $('#globalprogrammecourse_fee').change(function () {
        var programme_id = $(this).val();
     	$.ajax({
			url: $('body').attr('data-base-url') + 'admissions/getincProgrammeDiscipline',
			type: 'POST',
			dataType: 'json',
			data: {
				id: $(this).attr('data-src'),
				programme_id: programme_id
			},
			success: function(response) {

				$('#globaldisciplinecourse_fee').html('');
				$('#globaldisciplinecourse_fee').append(
					$('<option>').val('').text('-- Select Discipline --')
				);

				// response is now array [{id:'17', name:'...'}]
				$.each(response, function(index, item) {
					$('#globaldisciplinecourse_fee').append(
						$('<option>').val(item.id).text(item.name)
					);
				});

			},
			error: function(xhr, status, error) {
				console.log('AJAX Error:', error);
			}
		});
    });

    $('#globaldisciplinecourse_fee').change(function () {
        var programme_id = $("#globalprogrammecourse_fee").val();
        var discipline_id = $(this).val();
        $.ajax({

            url: $('body').attr('data-base-url') + 'international/getdisciplinecourse',
            method: 'post',
            data: {
                id: $(this).attr('data-src'),
                programme_id: programme_id,
                discipline_id: discipline_id
            },
            dataType: "json"
        }).done(function (response) {
            feePagination(response);
        });
    });

    $('#programmecourse_fee').change(function () {
     var programme_id = $(this).val();
     $.ajax({
			url: $('body').attr('data-base-url') + 'admissions/getincProgrammeDiscipline',
			type: 'POST',
			dataType: 'json',
			data: {
				id: $(this).attr('data-src'),
				programme_id: programme_id
			},
			success: function(response) {

				$('#disciplinecourse_fee').html('');
				$('#disciplinecourse_fee').append(
					$('<option>').val('').text('-- Select Discipline --')
				);

				// response is now array [{id:'17', name:'...'}]
				$.each(response, function(index, item) {
					$('#disciplinecourse_fee').append(
						$('<option>').val(item.id).text(item.name)
					);
				});

			},
			error: function(xhr, status, error) {
				console.log('AJAX Error:', error);
			}
		});
    });

    $('#disciplinecourse_fee').change(function () {
        var programme_id = $("#programmecourse_fee").val();
        var discipline_id = $(this).val();
        $.ajax({
            url: $('body').attr('data-base-url') + 'admissions/getdisciplinecourse',
            method: 'post',
            data: {
                id: $(this).attr('data-src'),
                programme_id: programme_id,
                discipline_id: discipline_id
            },
            dataType: "json"
        }).done(function (response) {
            feePagination(response);
        });
    });

    $('#search_faclty_fee').on('keyup', function (e) {
        var q = e.target.value.replace('.', '').toLowerCase();
        if (q == "") {
            feePagination(allCourses);
        }
        else {
            feePagination(allCourses.filter(obj => {
                if (obj.course_name.replace('.', '').toLowerCase().includes(q) > 0) {
                    return true;
                }
                else {
                    return false;
                }
            }));
        }

        // $('div.staff-container').each(function () {
        //     var name = this.children[0].textContent;
        //     if (name.search(q) < 0) {
        //         $(this).hide();
        //         $('.first-letter').hide();
        //     } else {
        //         $(this).show();
        //         $('.first-letter').show();
        //     }

        // });
    });

    /* course fee page end */



    $('#programme').change(function () {
        var programme_id = $(this).val();
        $.ajax({

            url: $('body').attr('data-base-url') + 'admissions/getProgrammeDiscipline',
            method: 'post',
            data: {
                id: $(this).attr('data-src'),
                programme_id: programme_id
            }
        }).done(function (response) {
            $('#discipline').html('');
            $('#discipline').append($('<option>').text(' -- Select Discipline -- ').attr('value', ''));
            $.each(response, function (i, value) {
                $('#discipline').append($('<option>').text(value).attr('value', i));

            });
        });
    });

    $('#discipline').change(function () {
        var programme_id = $("#programme").val();
        var discipline_id = $(this).val();
        $.ajax({

            url: $('body').attr('data-base-url') + 'international/getDisciplinenCourse',
            method: 'post',
            data: {
                id: $(this).attr('data-src'),
                programme_id: programme_id,
                discipline_id: discipline_id
            }
        }).done(function (response) {
            $('#course').html('');
            $('#course').append($('<option>').text(' -- Select Course -- ').attr('value', ''));
            $.each(response, function (i, value) {
                $('#course').append($('<option>').text(value).attr('value', i));

            });

        });
    });

    $(".footer").on("click", ".modalButtonViewCourse", function (e) {
        var id = $(this).attr('data-src');
        var programme_id = $(this).attr('data-value');

        $.ajax({

            url: $('body').attr('data-base-url') + 'academics/getCoursePopup',
            method: 'post',
            data: {
                id: $(this).attr('data-src'),
                programme_id: programme_id
            }
        }).done(function (response) {
            $('#courseModal').find('.modal-body').html(response);
            $('#courseModal').modal('show');
        });
    });


    /*
     *
     * Onclick : scholarship-form
     */
    $("#websearch").on("click", function () {
        $('#global-search .fa-search').hide();

    });


    /*
     *Onclick :  getdetails
     */
    $("#websearch").on("click", function () {
        $('#global-search .fa-search').hide();
    });

    $(".getapplydetails").on("click", function () {
        $('.havesuEdage').show();
        $('.apply-form').hide();
    });

    $("#findpeople").on("click", function () {
        $('#global-search .fa-search').show();

    });
	
		 /*
     *
     * Onclick : inc_apply_now
     */
    $("#inc_apply_now").on("click", function (e) {
		// Custom Values
        var full_name = $("#full_name").val();
        var email_id = $("#email_id").val();
        var phone_number = $("#phone_number").val();
        var country = $("#country").val();
        var programme_name = $("#programme_name").val();
        var emailReg = /^[a-z0-9]+([-._][a-z0-9]+)*@([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,4}$/;
        $("#email_id_msg").remove();
        $("#full_name_msg").remove();
        $("#phone_number_msg").remove();
        $("#state_msg").remove();
        $("#country_msg").remove();
        $("#programme_name_msg").remove();
        $("#email_id").parent().removeClass('has-error');
        $("#full_name").parent().removeClass('has-error');
        $("#phone_number").parent().removeClass('has-error');
        $("#country_row").parent().removeClass('has-error');
        $("#programme_name_row").parent().removeClass('has-error');
      
		$('.submit_info').show();
        var error_flag = 'N';
        if (full_name == '') {
            $("<span style='color:red;' id='full_name_msg'>Please enter full name.</span>").insertAfter("#full_name");
            $("#full_name").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (email_id == '') {
            $("<span style='color:red;' id='email_id_msg'>Please enter your email id.</span>").insertAfter("#email_id");
            $("#email_id").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (email_id != '' && !emailReg.test(email_id)) {
            $("<span style='color:red;' id='email_id_msg'>Please enter your email id.</span>").insertAfter("#email");
            $("#email").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (country == '') {
            $("<span style='color:red;' id='country_msg'>Please select your country name</span>").insertAfter("#country_row");
            $("#country_row").parent().addClass('has-error');
            error_flag = 'Y';
        }


        if (phone_number == '') {
            $("<span style='color:red;' id='phone_number_msg'>Please enter 10 digit valid mobile number.</span>").insertAfter("#phone_number");
            $("#phone_number").parent().addClass('has-error');
            error_flag = 'Y';
        } else if (!phone_number.match('[0-9]{10}')) {
            $("<span style='color:red;' id='mobile_msg'>Please enter 10 digit valid mobile number.</span>").insertAfter("#phone_number");
            $("#phone_number").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (programme_name == '') {
            $("<span style='color:red;' id='programme_name_msg'>Please select your programme.</span>").insertAfter("#programme_name_row");
            $("#programme_name_row").parent().addClass('has-error');
            error_flag = 'Y';
        }

          if (error_flag == 'N') {
            
            $.ajax({

                url: $('body').attr('data-base-url') + 'international/addEnquiry',
                method: 'post',
                data: {
                    full_name: full_name,
                    email_id: email_id,
                    phone_number: phone_number,
                    country: country,
                    programme_name: programme_name
                }
            }).done(function (response) {
				$('.submit_info').hide();
				if(response=='SUCCESS') {
					$("#full_name").val('');
					$("#email_id").val('');
					$("#phone_number").val('');
					$("#programme_name").val('');
					$("#country").val('');
					$('.submit_info').hide();
					var response = '<p style="color:green;">We have received your request. We will contact you shortly.</p>';
				}
                $("#request_success").html(response);
                setTimeout(function () { $('#request_success').slideUp("slow"); }, 5000);
                return false;
            });
        } else {
			$('.submit_info').hide();
			return false;
		}
	
    });
    /*
     *
     * Onclick : scholarship-form
     */
    $(".scholarship-form").on("click", function (e) {

        // Custom Values
        var name = $("#name").val();
        var email_id = $("#email").val();
        var mobile = $("#mobile").val();
        var country = $("#country").val();
        var city = $("#city").val();
        var emailReg = /^[a-z0-9]+([-._][a-z0-9]+)*@([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,4}$/;
        // Hoidden values
        var programme = $("#programme").val();
        var discipline = $("#discipline").val();
        var course = $("#course").val();

        $("#email_id_msg").remove();
        $("#full_name_msg").remove();
        $("#mobile_msg").remove();
        $("#state_msg").remove();
        $("#country_msg").remove();
        $("#programme_msg").remove();
        $("#discipline_msg").remove();
        $("#course_msg").remove();
        $("#email").parent().removeClass('has-error');
        $("#name").parent().removeClass('has-error');
        $("#mobile").parent().removeClass('has-error');
        $("#country_row").parent().removeClass('has-error');
        $("#city_row").parent().removeClass('has-error');
        $("#programme_row").parent().removeClass('has-error');
        $("#discipline_row").parent().removeClass('has-error');
        $("#course_row").parent().removeClass('has-error');

        var error_flag = 'N';
        if (name == '') {
            $("<span style='color:red;' id='full_name_msg'>Please enter full name.</span>").insertAfter("#name");
            $("#name").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (email_id == '') {
            $("<span style='color:red;' id='email_id_msg'>Please enter your email id.</span>").insertAfter("#email");
            $("#email").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (email_id != '' && !emailReg.test(email_id)) {
            $("<span style='color:red;' id='email_id_msg'>Please enter your email id.</span>").insertAfter("#email");
            $("#email").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (country == '') {
            $("<span style='color:red;' id='country_msg'>Please select your country name</span>").insertAfter("#country_row");
            $("#country_row").parent().addClass('has-error');
            error_flag = 'Y';
        }


        if (mobile == '') {
            $("<span style='color:red;' id='mobile_msg'>Please enter 10 digit valid mobile number.</span>").insertAfter("#mobile");
            $("#mobile").parent().addClass('has-error');
            error_flag = 'Y';
        } else if (!mobile.match('[0-9]{10}')) {
            $("<span style='color:red;' id='mobile_msg'>Please enter 10 digit valid mobile number.</span>").insertAfter("#mobile");
            $("#mobile").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (city == '') {
            $("<span style='color:red;' id='city_msg'>Please enter your city.</span>").insertAfter("#city");
            $("#city").parent().addClass('has-error');
            error_flag = 'Y';
        }


        if (programme == '') {
            $("<span style='color:red;' id='programme_msg'>Please select programme.</span>").insertAfter("#programme_row");
            $("#programme_row").parent().addClass('has-error');
            error_flag = 'Y';
        }
        if (discipline == '') {
            $("<span style='color:red;' id='discipline_msg'>Please select programme discipline.</span>").insertAfter("#discipline_row");
            $("#discipline_row").parent().addClass('has-error');
            error_flag = 'Y';
        }
        if (course == '') {
            $("<span style='color:red;' id='course_msg'>Please select course.</span>").insertAfter("#course_row");
            $("#course_row").parent().addClass('has-error');
            error_flag = 'Y';
        }
        if (error_flag == 'Y') {
            return false;
        }

    });

    /*
     * onclick : getintouch
     */
    $(".getintouch").on("click", function (e) {

        // Custom Values
        var name = $("#name").val();
        var email = $("#email").val();
        var mobile = $("#mobile").val();
        var country_code = $("#country_code").val();
        var remarks = $("#remarks").val();
        var country = $("#country").val();
        var emailReg = /^[a-z0-9]+([-._][a-z0-9]+)*@([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,4}$/;

        $("#email_msg").parent().remove();
        $("#name_msg").parent().remove();
        $("#mobile_msg").parent().remove();
        $("#country_msg").parent().remove();
        $("#remarks_msg").parent().remove();

        var error_flag = 'N';
        if (name == '') {
            $("<span style='color:red;' id='name_msg'>Please enter full name.</span>").insertAfter("#name");
            $("#name").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (email == '') {
            $("<span style='color:red;' id='email_msg'>Please enter your email id.</span>").insertAfter("#email");
            $("#email").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (email != '' && !emailReg.test(email)) {
            $("<span style='color:red;' id='email_msg'>Please enter your email id.</span>").insertAfter("#email");
            $("#email").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (mobile == '') {
            $("<span style='color:red;' id='mobile_msg'>Please enter 10 digit valid mobile number.</span>").insertAfter("#mobile");
            $("#mobile").parent().addClass('has-error');
            error_flag = 'Y';
        } else if (!mobile.match('[0-9]{10}')) {
            $("<span style='color:red;' id='mobile_msg'>Please enter 10 digit valid mobile number.</span>").insertAfter("#mobile");
            $("#mobile").parent().addClass('has-error');
            error_flag = 'Y';
        }
        if (country == '') {
            $("<span style='color:red;' id='country_msg'>Please select your country.</span>").insertAfter("#country_row");
            $("#country_row").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (remarks == '') {
            $("<span style='color:red;' id='remarks_msg'>Please enter your remarks</span>").insertAfter("#remarks");
            $("#remarks_row").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (error_flag == 'N') {
            $('.submit_info').show();
            $.ajax({

                url: $('body').attr('data-base-url') + 'contact/addEnquiry',
                method: 'post',
                data: {
                    name: name,
                    email: email,
                    mobile: mobile,
                    country: country,
                    country_code: country_code,
                    remarks: remarks,
                    enquiry_source: 'Get in Touch'
                }
            }).done(function (response) {
                $("#name").val('');
                $("#email").val('');
                $("#mobile").val('');
                $("#remarks").val('');
                $("#country").val('');
                $('.submit_info').hide();
                $("#request_success").html('<p ng-bind="callbackopt_success_message">' + response + '</p>');
               // setTimeout(function () { $('#request_success').slideUp("slow"); }, 5000);
				var redUrl = $('body').attr('data-base-url')+'contact/thanks';
				window.setTimeout(function(){ window.location.href = redUrl; }, 5000);  
				
                return false;
            });
        }
        return false;


    });


/*
     *
     * Onclick : scholarship-form
     */
    $(".malawi-scholarship-form").on("click", function (e) {

        // Custom Values
        var name = $("#name").val();
        var email_id = $("#email").val();
        var mobile = $("#mobile").val();
        var country = $("#country").val();
        var city = $("#city").val();
        var emailReg = /^[a-z0-9]+([-._][a-z0-9]+)*@([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,4}$/;
        // Hoidden values
        var programme = $("#programme").val();
        var discipline = $("#discipline").val();
        var course = $("#course").val();

        $("#email_id_msg").remove();
        $("#full_name_msg").remove();
        $("#mobile_msg").remove();
        $("#state_msg").remove();
        $("#country_msg").remove();
        $("#programme_msg").remove();
        $("#discipline_msg").remove();
        $("#course_msg").remove();
        $("#email").parent().removeClass('has-error');
        $("#name").parent().removeClass('has-error');
        $("#mobile").parent().removeClass('has-error');
        $("#country_row").parent().removeClass('has-error');
        $("#city_row").parent().removeClass('has-error');
        $("#programme_row").parent().removeClass('has-error');
        $("#discipline_row").parent().removeClass('has-error');
        $("#course_row").parent().removeClass('has-error');

        var error_flag = 'N';
        if (name == '') {
            $("<span style='color:red;' id='full_name_msg'>Please enter full name.</span>").insertAfter("#name");
            $("#name").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (email_id == '') {
            $("<span style='color:red;' id='email_id_msg'>Please enter your email id.</span>").insertAfter("#email");
            $("#email").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (email_id != '' && !emailReg.test(email_id)) {
            $("<span style='color:red;' id='email_id_msg'>Please enter your email id.</span>").insertAfter("#email");
            $("#email").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (country == '') {
            $("<span style='color:red;' id='country_msg'>Please select your country name</span>").insertAfter("#country_row");
            $("#country_row").parent().addClass('has-error');
            error_flag = 'Y';
        }


        if (mobile == '') {
            $("<span style='color:red;' id='mobile_msg'>Please enter valid mobile number.</span>").insertAfter("#mobile");
            $("#mobile").parent().addClass('has-error');
            error_flag = 'Y';
        } /*else if (!mobile.match('[0-9]{10}')) {
            $("<span style='color:red;' id='mobile_msg'>Please enter 10 digit valid mobile number.</span>").insertAfter("#mobile");
            $("#mobile").parent().addClass('has-error');
            error_flag = 'Y';
        }*/

        if (city == '') {
            $("<span style='color:red;' id='city_msg'>Please enter your city.</span>").insertAfter("#city");
            $("#city").parent().addClass('has-error');
            error_flag = 'Y';
        }


        if (programme == '') {
            $("<span style='color:red;' id='programme_msg'>Please select programme.</span>").insertAfter("#programme_row");
            $("#programme_row").parent().addClass('has-error');
            error_flag = 'Y';
        }
        if (discipline == '') {
            $("<span style='color:red;' id='discipline_msg'>Please select programme discipline.</span>").insertAfter("#discipline_row");
            $("#discipline_row").parent().addClass('has-error');
            error_flag = 'Y';
        }
        if (course == '') {
            $("<span style='color:red;' id='course_msg'>Please select course.</span>").insertAfter("#course_row");
            $("#course_row").parent().addClass('has-error');
            error_flag = 'Y';
        }
        if (error_flag == 'Y') {
            return false;
        }

    });

/*
     * onclick : ccdc_getintouch
     */
    $(".ccdc_getintouch").on("click", function (e) {

        // Custom Values
        var name = $("#name").val();
        var email = $("#email").val();
        var mobile = $("#mobile").val();
        var remarks = $("#remarks").val();
        var emailReg = /^[a-z0-9]+([-._][a-z0-9]+)*@([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,4}$/;

        $("#email_msg").parent().remove();
        $("#name_msg").parent().remove();
        $("#mobile_msg").parent().remove();
        $("#remarks_msg").parent().remove();

        var error_flag = 'N';
        if (name == '') {
            $("<span style='color:red;' id='name_msg'>Please enter full name.</span>").insertAfter("#name");
            $("#name").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (email == '') {
            $("<span style='color:red;' id='email_msg'>Please enter your email id.</span>").insertAfter("#email");
            $("#email").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (email != '' && !emailReg.test(email)) {
            $("<span style='color:red;' id='email_msg'>Please enter your email id.</span>").insertAfter("#email");
            $("#email").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (mobile == '') {
            $("<span style='color:red;' id='mobile_msg'>Please enter 10 digit valid mobile number.</span>").insertAfter("#mobile");
            $("#mobile").parent().addClass('has-error');
            error_flag = 'Y';
        } else if (!mobile.match('[0-9]{10}')) {
            $("<span style='color:red;' id='mobile_msg'>Please enter 10 digit valid mobile number.</span>").insertAfter("#mobile");
            $("#mobile").parent().addClass('has-error');
            error_flag = 'Y';
        }
        
        if (remarks == '') {
            $("<span style='color:red;' id='remarks_msg'>Please enter your remarks</span>").insertAfter("#remarks");
            $("#remarks_row").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (error_flag == 'N') {
            $('.submit_info_div').show();
            $.ajax({

                url: $('body').attr('data-base-url') + 'ccdc/addEnquiry',
                method: 'post',
                data: {
                    name: name,
                    email: email,
                    mobile: mobile,
                    remarks: remarks,
                    enquiry_source: 'CCDC Get in Touch'
                }
            }).done(function (response) {
                $("#name").val('');
                $("#email").val('');
                $("#mobile").val('');
                $("#remarks").val('');
                $('.submit_info_div').hide();
                $("#request_success").html('<p style="color:green;">' + response + '</p>');
                setTimeout(function () { $('#request_success').slideUp("slow"); }, 5000);
                return false;
            });
        }
        return false;


    });
    // save school enquiry_source

    $(".schoolEnquiry").on("click", function (e) {

        // Custom Values
        var name = $("#name").val();
        var email = $("#email").val();
        var mobile = $("#mobile").val();
        var country = $("#country").val();
        var country_code = $("#country_code").val();
        var state = $("#state").val();
        var course_discipline = $("#source").val();
        var gender = $('input:radio[name=gender]:checked').val();
        if (typeof gender == 'undefined') { gender = ''; }

        var emailReg = /^[a-z0-9]+([-._][a-z0-9]+)*@([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,4}$/;

        $("#email_msg").remove();
        $("#name_msg").remove();
        $("#mobile_msg").remove();
        $("#country_msg").remove();
        $("#state_msg").remove();
        $("#gender_msg").remove();
        $("#name").parent().removeClass('has-error');
        $("#email").parent().removeClass('has-error');
        $("#mobile").parent().removeClass('has-error');
        $("#gender_row").parent().removeClass('has-error');
        $("#country_row").parent().removeClass('has-error');
        $("#state").parent().removeClass('has-error');
        var error_flag = 'N';
        if (name == '') {
            $("<span style='color:red;' id='name_msg'>Please enter full name.</span>").insertAfter("#name");
            $("#name").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (email == '') {
            $("<span style='color:red;' id='email_msg'>Please enter your email id.</span>").insertAfter("#email");
            $("#email").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (email != '' && !emailReg.test(email)) {
            $("<span style='color:red;' id='email_msg'>Please enter your email id.</span>").insertAfter("#email");
            $("#email").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (mobile == '') {
            $("<span style='color:red;' id='mobile_msg'>Please enter 10 digit valid mobile number.</span>").insertAfter("#mobile");
            $("#mobile").parent().addClass('has-error');
            error_flag = 'Y';
        } else if (!mobile.match('[0-9]{10}')) {
            $("<span style='color:red;' id='mobile_msg'>Please enter 10 digit valid mobile number.</span>").insertAfter("#mobile");
            $("#mobile").parent().addClass('has-error');
            error_flag = 'Y';
        }


        if (gender == '') {
            $("<span style='color:red;' id='gender_msg'>Please select your gender.</span>").insertAfter("#gender_grup");
            $("#gender_row").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (country == '') {
            $("<span style='color:red;' id='country_msg'>Please select your country.</span>").insertAfter("#country_row");
            $("#country_row").parent().addClass('has-error');
            error_flag = 'Y';
        }


        if (state == '') {
            $("<span style='color:red;' id='state_msg'>Please enter state.</span>").insertAfter("#state");
            $("#state").parent().addClass('has-error');
            error_flag = 'Y';
        }


        if (error_flag == 'N') {
            $('.submit_info').show();
            $.ajax({

                url: $('body').attr('data-base-url') + 'contact/addEnquiry',
                method: 'post',
                data: {
                    name: name,
                    email: email,
                    mobile: mobile,
                    country: country,
                    country_code: country_code,
                    state: state,
                    course_discipline: course_discipline,
                    enquiry_source: 'School Enquiry'
                }
            }).done(function (response) {
                $('.submit_info').hide();
                $('#schoolform')[0].reset();
                $("#request_success").html('<p ng-bind="callbackopt_success_message">' + response + '</p>');
                setTimeout(function () { $('#request_success').slideUp("slow"); }, 5000);
                return false;
            });
        }
        return false;


    });

    $("#request_info").on("click", function (e) {

        // Custom Values
        var name = $("#name").val();
        var email = $("#email").val();
        var mobile = $("#mobile").val();
        var country = $("#country").val();
        var country_code = $("#country_code").val();
        var state = $("#state").val();
        var marks_10 = $("#marks_10").val();
        var marks_12 = $("#marks_12").val();
        var user_type = $('input:radio[name="user_type"]:checked').val();
        var gender = $('input:radio[name=gender]:checked').val();

        if (typeof user_type == 'undefined') { user_type = ''; }

        if (typeof gender == 'undefined') { gender = ''; }

        var emailReg = /^[a-z0-9]+([-._][a-z0-9]+)*@([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,4}$/;
        // Hoidden values
        var course_type = $("#course_type").val();
        var course_discipline = $("#course_discipline").val();
        var course_name = $("#course_name").val();

        $("#email_msg").remove();
        $("#name_msg").remove();
        $("#mobile_msg").remove();
        $("#gender_msg").remove();
        $("#user_type_msg").remove();
        $("#state_msg").remove();
        $("#country_msg").remove();
        $("#email").parent().removeClass('has-error');
        $("#name").parent().removeClass('has-error');
        $("#mobile").parent().removeClass('has-error');
        $("#country_row").parent().removeClass('has-error');
        $("#state_row").parent().removeClass('has-error');
        $("#user_type_row").parent().removeClass('has-error');
        $("#gender_row").parent().removeClass('has-error');

        var error_flag = 'N';

        if (email == '') {
            $("<span style='color:red;' id='email_msg'>Please enter your email id.</span>").insertAfter("#email");
            $("#email").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (email != '' && !emailReg.test(email)) {
            $("<span style='color:red;' id='email_msg'>Please enter your email id.</span>").insertAfter("#email");
            $("#email").parent().addClass('has-error');
            error_flag = 'Y';
        }
        if (name == '') {
            $("<span style='color:red;' id='name_msg'>Please enter full name.</span>").insertAfter("#name");
            $("#name").parent().addClass('has-error');
            error_flag = 'Y';
        }


        if (mobile == '') {
            $("<span style='color:red;' id='mobile_msg'>Please enter 10 digit valid mobile number.</span>").insertAfter("#mobile");
            $("#mobile").parent().addClass('has-error');
            error_flag = 'Y';
        } else if (!mobile.match('[0-9]{10}')) {
            $("<span style='color:red;' id='mobile_msg'>Please enter 10 digit valid mobile number.</span>").insertAfter("#mobile");
            $("#mobile").parent().addClass('has-error');
            error_flag = 'Y';
        }


        if (country == '') {
            $("<span style='color:red;' id='country_msg'>Please select your country name</span>").insertAfter("#country_row");
            $("#country_row").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (state == '') {
            $("<span style='color:red;' id='state_msg'>Please select your state.</span>").insertAfter("#state_row");
            $("#state_row").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (user_type == '') {
            $("<span style='color:red;' id='user_type_msg'>Please select your type.</span>").insertAfter("#user_type_row");
            $("#user_type_row").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (gender == '') {
            $("<span style='color:red;' id='gender_msg'>Please select your gender.</span>").insertAfter("#gender_row");
            $("#gender_row").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (error_flag == 'N') {
            $('.submit_info').show();
            $.ajax({

                url: $('body').attr('data-base-url') + 'requestinfo/addRequestInfo',
                method: 'post',
                data: {
                    name: name,
                    email: email,
                    mobile: mobile,
                    country: country,
                    country_code: country_code,
                    state: state,
                    marks_10: marks_10,
                    marks_12: marks_12,
                    user_type: user_type,
                    gender: gender,
                    course_type: course_type,
                    course_discipline: course_discipline,
                    course_name: course_name
                }
            }).done(function (response) {
                $('#requestinfo')[0].reset();
                $("#request_success").html('');
                $('.submit_info').hide();
                $("#request_success").html(response);
                setTimeout(function () { $('#request_success').slideUp("slow"); }, 15000);
                return false;
            });
        }
        return false;


    });

	$("#dsw_registration").on("click", function (e) {

        // Custom Values
        $(".alert").hide();
		$("#loading").show();
        var applied_game = $("#applied_game").val();
        var name = $("#name").val();
        var email = $("#email_id").val();
        var mobile = $("#contact_number").val();
        var country_code = $("#country_code").val();
        var father_name = $("#father_name").val();
        var enrollment_no = $("#enrollment_no").val();
        var school_name = $("#school_name").val();
        var profile_photo = $("#profile_photo").val();
        var emailReg = /^[a-z0-9]+([-._][a-z0-9]+)*@([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,4}$/;
        $("#submit_info").show();
        $("#applied_game_msg").remove();
        $("#enrollment_no_msg").remove();
        $("#school_name_msg").remove();
        $("#email_msg").remove();
        $("#name_msg").remove();
        $("#mobile_msg").remove();
        $("#profile_photo_msg").remove();
        $("#father_name_msg").remove();
        $("#contact_number_msg").remove();
        $("#email").parent().removeClass('has-error');
        $("#name").parent().removeClass('has-error');
        $("#contact_number").parent().removeClass('has-error');
        $("#father_name").parent().removeClass('has-error');
        $("#school_name").parent().removeClass('has-error');
        $("#enrollment_no").parent().removeClass('has-error');
        $("#profile_photo_row").parent().removeClass('has-error');
       
        var error_flag = 'N';
		if (applied_game == '') {
            $("<span style='color:red;' id='applied_game_msg'>Please select game.</span>").insertAfter("#applied_row");
            $("#applied_row").parent().addClass('has-error');
            error_flag = 'Y';
        }
		if (father_name == '') {
            $("<span style='color:red;' id='father_name_msg'>Please enter father name.</span>").insertAfter("#father_name");
            $("#father_name").parent().addClass('has-error');
            error_flag = 'Y';
        }
		if (school_name == '') {
            $("<span style='color:red;' id='school_name_msg'>Please enter father name.</span>").insertAfter("#school_row");
            $("#school_row").parent().addClass('has-error');
            error_flag = 'Y';
        }
        if (email == '') {
            $("<span style='color:red;' id='email_msg'>Please enter your email id.</span>").insertAfter("#email_id");
            $("#email_id").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (email != '' && !emailReg.test(email)) {
            $("<span style='color:red;' id='email_msg'>Please enter your email id.</span>").insertAfter("#email_id");
            $("#email_id").parent().addClass('has-error');
            error_flag = 'Y';
        }
        if (name == '') {
            $("<span style='color:red;' id='name_msg'>Please enter full name.</span>").insertAfter("#name");
            $("#name").parent().addClass('has-error');
            error_flag = 'Y';
        }


        if (mobile == '') {
            $("<span style='color:red;' id='mobile_msg'>Please enter 10 digit valid mobile number.</span>").insertAfter("#contact_number");
            $("#contact_number").parent().addClass('has-error');
            error_flag = 'Y';
        } else if (!mobile.match('[0-9]{10}')) {
            $("<span style='color:red;' id='mobile_msg'>Please enter 10 digit valid mobile number.</span>").insertAfter("#contact_number");
            $("#contact_number").parent().addClass('has-error');
            error_flag = 'Y';
        }


        if (enrollment_no == '') {
            $("<span style='color:red;' id='enrollment_no_msg'>Please enter enrollment number</span>").insertAfter("#enrollment_no");
            $("#enrollment_no").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (profile_photo == '') {
            $("<span style='color:red;' id='profile_photo_msg'>Please upload profile photo.</span>").insertAfter("#profile_photo_row");
            $("#profile_photo_row").parent().addClass('has-error');
            error_flag = 'Y';
        }

        if (error_flag == 'Y') {
			$("#submit_info").hide();
			$("#loading").hide();
			return false;
			
        }
        
    });
    /*
     * Go Back section
     */
    $(".gobackstep1").on("click", function (e) {
        $("#step2").hide();
        $("#step1").show();
        $("#applystep2").removeClass('active');
        $("#applystep2a").removeClass('active');
        $("#applystep3").removeClass('active');
        $("#applystep4").removeClass('active');
        return false;
    });

    /*
     * Go Back section
     */
    $(".gobackstep2").on("click", function (e) {
        $("#step3").hide();
        $("#step2").show();
        $("#applystep3").removeClass('active');
        $("#applystep4").removeClass('active');
        return false;
    });

    /*
     * Go Back section
     */
    $(".gobackstep3").on("click", function (e) {
        $("#step4").hide();
        $("#step3").show();
        $("#applystep4").removeClass('active');
        return false;
    });

    /* Onclick : getUserDetails
     *
     */
    $("#getUserDetails").on("click", function (e) {
        var suedgeid = $("#su_edge_id").val();
        $("#suedge_div").parent().removeClass('has-error');
        var error_flag = 'N';
        if (suedgeid == '') {
            $("#suedge_div").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (error_flag == 'N') {
            $.ajax({
                url: $('body').attr('data-base-url') + 'apply/getapplicationdetails',
                method: 'post',
                data: {
                    su_edge_id: suedgeid
                }
            }).done(function (response) {
                var arrresponse = response.split('=');

                if (arrresponse[0] > 0) {
                    $(".havesuEdage").hide();
                    $(".apply-form").show();
                    $("#step1").hide();
                    $("#step2").show();
                    $("#regis_id").val(arrresponse[0]);
                    $("#name").val(arrresponse[2]);
                    $("#email").val(arrresponse[3]);
                    $("#mob").val(arrresponse[4]);
                    $("#user_otp").val(arrresponse[16]);
                    $("#address").val(arrresponse[5]);
                    $("#city").val(arrresponse[6]);
                    $("#state").val(arrresponse[7]);
                    $("#pincode").val(arrresponse[8]);
                    $('input:radio[name=gender][value=' + arrresponse[10] + ']').attr('checked', true);
                    $('#dateofbirth').val(arrresponse[9]);
                    var programme_id = arrresponse[11];
                    var discipline_id = arrresponse[12];
                    var course_id = arrresponse[13];
                    showProgrammeDiscipline(programme_id, discipline_id);
                    showDisciplineCourse(programme_id, discipline_id, course_id);
                    $('#programme  option[value="' + programme_id + '"]').prop("selected", true);
                    return false;
                } else if (arrresponse[0] == 0) {
                    $("#step1").hide();
                    $("#step2").hide();
                    $("#step3").hide();
                    $("#step4").hide();
                    $("#step5").hide();
                    $(".havesuEdage").hide();
                    $(".apply-form").show();
                    $("#step6").show();
                    return false;
                } else {
                    $(".havesuEdage").hide();
                    $(".apply-form").show();
                    $("#step1").show();
                    $("#regis_id").val('');
                    $("#name").val('');
                    $("#email").val('');
                    $("#mob").val('');
                    $("#step6").hide();
                    return false;
                }
            });
        }
        return false;
    });


    /*
     * Onclick step1 validate and check current status
     */
    $("#globalform").on("click", function (e) {

        var name = $("#name").val();
        var email = $("#email").val();
        var country = $("#country").val();
        var mobile = $("#mob").val();
        var discipline = $("#discipline").val();
        var programme = $("#programme").val();
        var course = $("#course").val();


        if (typeof name == 'undefined') { name = ''; }
        if (typeof mobile == 'undefined') { mobile = ''; }
        if (typeof email == 'undefined') { email = ''; }
        if (typeof country == 'undefined') { country = ''; }
        if (typeof discipline == 'undefined') { discipline = ''; }
        if (typeof programme == 'undefined') { programme = ''; }
        if (typeof course == 'undefined') { course = ''; }

        var emailReg = /^[a-z0-9]+([-._][a-z0-9]+)*@([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,4}$/;
        $("#name").parent().removeClass('has-error');
        $("#country_div").parent().removeClass('has-error');
        $("#mob").parent().removeClass('has-error');
        $("#email").parent().removeClass('has-error');
        $("#programme_div").parent().removeClass('has-error');
        $("#course_div").parent().removeClass('has-error');
        $("#discipline_div").parent().removeClass('has-error');

        var error_flag = 'N';

        if (name == '') {
            $("#name").parent().addClass("has-error");
            error_flag = 'Y';
        }

        if (email == '') {
            $("#email").parent().addClass("has-error");
            error_flag = 'Y';
        }

        if (email != '' && !emailReg.test(email)) {
            $("#email").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (country == '') {
            $("#country_div").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (mobile == '') {
            $("#mob").parent().addClass("has-error");
            error_flag = 'Y';
        } else if (!mobile.match('[0-9]{10}')) {
            $("#mob").parent().addClass("has-error");
            error_flag = 'Y';
        }

        if (programme == '') {
            $("#programme_div").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (discipline == '') {
            $("#discipline_div").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (course == '') {
            $("#course_div").parent().addClass("has-error");
            error_flag = 'Y';
        }

        if (error_flag == 'N') {
            return true;
        }
        return false;
    });


    /*
     * Onclick step1 validate and check current status
     */
    $("#sendverificationotp").on("click", function (e) {
        $('ul').removeClass('has-error');
        var name = $("#name").val();
        var email = $("#email").val();
        var country = $("#country").val();
        var mobile = $("#mob").val();

        if (typeof name == 'undefined') { name = ''; }
        if (typeof mobile == 'undefined') { mobile = ''; }
        if (typeof email == 'undefined') { email = ''; }

        var emailReg = /^[a-z0-9]+([-._][a-z0-9]+)*@([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,4}$/;
        $("#name").parent().removeClass('has-error');
        $("#country").parent().removeClass('has-error');
        $("#mob").parent().removeClass('has-error');
        $("#email").parent().removeClass('has-error');
        $("#user_otp").parent().removeClass('has-error');

        var error_flag = 'N';
        if (name == '') {
            $("#name").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (country == '') {
            $("#country").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (email == '') {
            $("#email").parent().addClass("has-error");
            error_flag = 'Y';
        }

        if (email != '' && !emailReg.test(email)) {
            $("#email").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (mobile == '') {
            $("#mob").parent().addClass("has-error");
            error_flag = 'Y';
        } else if (!mobile.match('[0-9]{10}')) {
            $("#mob").parent().addClass("has-error");
            error_flag = 'Y';
        }

        if (error_flag == 'N') {
            $('.submit_info').show();
            // Send OTP request to api to save the step1 data
            $.ajax({
                url: $('body').attr('data-base-url') + 'apply/sendVerificationSMS',
                method: 'post',
                data: {
                    name: name,
                    email: email,
                    mob: mobile,
                    country: country
                }
            }).done(function (response) {
                $('.submit_info').hide();
                $('#resend_otp').html('');
                $('#resend_otp').html('<span id="resend_otp">Resend OTP</span>');
                $("<p style='color:green;' id='msg_div'>OTP send successfully</p>").insertAfter("#submit_info");
                setTimeout(function () { $('#msg_div').slideUp("slow"); }, 4000);
                return false;

            });
        }
        return false;
    });



    /*
     * Onclick step1 validate and check current status
     */
    $(".step1").on("click", function (e) {

        var name = $("#name").val();
        var email = $("#email").val();
        var country = $("#country").val();
        var mobile = $("#mob").val();
        var user_otp = $("#user_otp").val();

        if (typeof name == 'undefined') { name = ''; }
        if (typeof mobile == 'undefined') { mobile = ''; }
        if (typeof email == 'undefined') { email = ''; }

        var emailReg = /^[a-z0-9]+([-._][a-z0-9]+)*@([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,4}$/;
        $('ul').parent().removeClass('has-error');
        $("#name").parent().removeClass('has-error');
        $("#country").parent().removeClass('has-error');
        $("#mob").parent().removeClass('has-error');
        $("#email").parent().removeClass('has-error');
        $("#user_otp").parent().removeClass('has-error');

        var error_flag = 'N';
        if (name == '') {
            $("#name").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (country == '') {
            $("#country").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (email == '') {
            $("#email").parent().addClass("has-error");
            error_flag = 'Y';
        }

        if (email != '' && !emailReg.test(email)) {
            $("#email").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (mobile == '') {
            $("#mob").parent().addClass("has-error");
            error_flag = 'Y';
        } else if (!mobile.match('[0-9]{10}')) {
            $("#mob").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (user_otp == '') {
            $("#user_otp").parent().addClass("has-error");
            error_flag = 'Y';
        }

        if (error_flag == 'N') {
            $('.submit_info').show();
            $("#divname_msg").remove();
            $("#divmobile_msg").remove();
            $("#divemail_msg").remove();

            // Send request to api to save the step1 data
            $.ajax({
                url: $('body').attr('data-base-url') + 'apply/applyStepOne',
                method: 'post',
                data: {
                    name: name,
                    email: email,
                    mob: mobile,
                    user_otp: user_otp,
                    country: country
                }
            }).done(function (response) {
                var responsevalue = response.split('=');
                $('.submit_info').hide();
                if (responsevalue[0] > 0) {
                    if (responsevalue[1] == 'SUCCESS') {
                        $("#step1").hide();
                        $("#step2").hide();
                        $("#step3").hide();
                        $("#step4").hide();
                        $("#step5").hide();
                        $(".havesuEdage").hide();
                        $(".apply-form").show();
                        $("#step6").show();
                        return false;
                    } else if (responsevalue[1] == 'FAIL') {
                        $("#step1").hide();
                        $("#step2").show();
                        $("#regis_id").val(responsevalue[0]);
                        $("#name").val(responsevalue[2]);
                        $("#email").val(responsevalue[3]);
                        $("#mob").val(responsevalue[4]);
                        $("#address").val(responsevalue[5]);
                        $("#user_otp").val(responsevalue[16]);
                        $("#city").val(responsevalue[6]);
                        $("#state").val(responsevalue[7]);
                        $("#pincode").val(responsevalue[8]);
                        $('input:radio[name=gender][value=' + responsevalue[10] + ']').attr('checked', true);
                        $('#dateofbirth').val(responsevalue[9]);

                        var programme_id = responsevalue[11];
                        var discipline_id = responsevalue[12];
                        var course_id = responsevalue[13];
                        showProgrammeDiscipline(programme_id, discipline_id);
                        showDisciplineCourse(programme_id, discipline_id, course_id);
                        $('#programme  option[value="' + programme_id + '"]').prop("selected", true);

                        return false;
                    } else {
                        $("#step1").hide();
                        $("#step2").show();
                        $("#regis_id").val(response);
                        $("#applystep2").addClass('active');
                        $("#applystep2a").addClass('active');
                        return false;
                    }

                } else if (responsevalue[0] == 'Invalid OTP') {
                    $("<p style='color:red; font-size:11px;' id='msg_div'>Invalid OTP. Please Enter 6 Digit Valid OTP.</p>").insertAfter("#submit_info");
                    setTimeout(function () { $('#msg_div').slideUp("slow"); }, 4000);
                    return false;
                } else {
                    var obj = jQuery.parseJSON(response);
                    if (obj.name) {
                        $("<span style='color:red;' id='divname_msg'>" + obj.name + "</span>").insertAfter("#name");
                    }
                    if (obj.mobile) {
                        $("<span style='color:red;' id='divmobile_msg'>" + obj.mobile + "</span>").insertAfter("#mob");
                    }
                    if (obj.email) {
                        $("<span style='color:red;' id='divemail_msg'>" + obj.email + "</span>").insertAfter("#email");
                    }
                }

                return false;
            });


        }
        return false;
    });

    /*
     * Onclick step2 validation
     */
    $(".step2").on("click", function (e) {

        var dob = $("#dateofbirth").val();
        var gender = $('input:radio[name=gender]:checked').val();
        var city = $("#city").val();
        var state = $("#state").val();
        var pincode = $("#pincode").val();
        var address = $("#address").val();
        var regis_id = $("#regis_id").val();

        if (typeof dob == 'undefined') { dob = ''; }
        if (typeof gender == 'undefined') { gender = ''; }
        if (typeof city == 'undefined') { city = ''; }
        if (typeof state == 'undefined') { state = ''; }
        if (typeof pincode == 'undefined') { pincode = ''; }
        if (typeof address == 'undefined') { address = ''; }

        $("#dateofbirth").parent().removeClass('has-error');
        $("#gender").parent().removeClass('has-error');
        $("#address").parent().removeClass('has-error');
        $("#city").parent().removeClass('has-error');
        $("#state").parent().removeClass('has-error');
        $("#pincode").parent().removeClass('has-error');

        var error_flag = 'N';
        if (dob == '') {
            $("#dateofbirth").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (gender == '') {
            $("#gender").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (address == '') {
            $("#address").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (city == '') {
            $("#city").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (state == '') {
            $("#state").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (pincode == '') {
            $("#pincode").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (error_flag == 'N') {
            $("#divdob_msg").remove();
            $("#divgender_msg").remove();
            $("#divaddress_msg").remove();
            $("#divcity_msg").remove();
            $("#divstate_msg").remove();
            $("#divpincode_msg").remove();

            // Send request to api to save the step1 data
            $.ajax({
                url: $('body').attr('data-base-url') + 'apply/applyStepTwo',
                method: 'post',
                data: {
                    regis_id: regis_id,
                    dob: dob,
                    gender: gender,
                    address: address,
                    city: city,
                    state: state,
                    pincode: pincode
                }
            }).done(function (response) {
                if (response > 0) {
                    $("#step2").hide();
                    $("#step3").show();
                    $("#applystep3").addClass('active');
                    return false;
                } else {
                    var obj = jQuery.parseJSON(response);
                    if (obj.dob) {
                        $("<span style='color:red;' id='divdob_msg'>" + obj.dob + "</span>").insertAfter("#dateofbirth");
                    }
                    if (obj.gender) {
                        $("<span style='color:red;' id='divgender_msg'>" + obj.gender + "</span>").insertAfter("#gender");
                    }
                    if (obj.address) {
                        $("<span style='color:red;' id='divaddress_msg'>" + obj.address + "</span>").insertAfter("#address");
                    }
                    if (obj.city) {
                        $("<span style='color:red;' id='divcity_msg'>" + obj.city + "</span>").insertAfter("#city");
                    }
                    if (obj.state) {
                        $("<span style='color:red;' id='divstate_msg'>" + obj.state + "</span>").insertAfter("#state");
                    }
                    if (obj.pincode) {
                        $("<span style='color:red;' id='divepincode_msg'>" + obj.pincode + "</span>").insertAfter("#pincode");
                    }
                }

                return false;
            });


        }
        return false;
    });

    /*
     * Onclick step3 validation
     */
    $(".step3courseprogramme").on("click", function (e) {

        var programme = $("#programme").val();
        var discipline = $("#discipline").val();
        var course = $("#course").val();
        var regis_id = $("#regis_id").val();

        if (typeof programme == 'undefined') { programme = ''; }
        if (typeof discipline == 'undefined') { discipline = ''; }
        if (typeof course == 'undefined') { course = ''; }

        $(".programme").parent().removeClass('has-error');
        $(".discipline").parent().removeClass('has-error');
        $(".course").parent().removeClass('has-error');

        var error_flag = 'N';
        if (programme == '') {
            $(".programme").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (discipline == '') {
            $(".discipline").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (course == '') {
            $(".course").parent().addClass("has-error");
            error_flag = 'Y';
        }
        if (error_flag == 'N') {
            $("#divProgramme_msg").remove();
            $("#divcourse_msg").remove();
            $("#divdiscipline_msg").remove();

            // Send request to api to save the step1 data
            $.ajax({
                url: $('body').attr('data-base-url') + 'apply/applyStepThree',
                method: 'post',
                data: {
                    program: programme,
                    discipline: discipline,
                    course: course,
                    regis_id: regis_id
                }
            }).done(function (response) {
                if (response > 0) {
                    $("#applystep4").addClass('active');
                    $("#step3").hide();
                    $("#step4").show();
                    return false;

                } else {
                    var obj = jQuery.parseJSON(response);

                    if (obj.programme) {
                        $("<span style='color:red;' id='divprogramme_msg'>" + obj.programme + "</span>").insertAfter("#programme");
                    }
                    if (obj.discipline) {
                        $("<span style='color:red;' id='divdiscipline_msg'>" + obj.discipline + "</span>").insertAfter("#discipline");
                    }
                    if (obj.course) {
                        $("<span style='color:red;' id='divcourse_msg'>" + obj.course + "</span>").insertAfter("#mob");
                    }

                }

            });
            return false;
        }
    });
});

// Perform onclick event for 
function showDiscipline(programme_value) {
    var programme_id = $('input:radio[name=programme_name]:checked').val();
    $.ajax({

        url: $('body').attr('data-base-url') + 'search/getProgrammeDiscipline',
        method: 'post',
        data: {
            id: $(this).attr('data-src'),
            programme_id: programme_id
        }
    }).done(function (response) {
        $('.search-programme').html('');
        $('.search-programme').html(programme_value);
        $('#search_discipline').html('');
        $('#search_discipline').html(response);
        $("#discipline-lnk").addClass('active');
        $("#discipline").addClass('active');
        $("#programme").removeClass('active');
        $("#programme").addClass('selected');
        $("#undergraduate-lnk").removeClass('active');
        return false;
    });
}

// Perform onclick event to populateCourse 
function populateCourse(discipline_value) {
    var programme_id = $('input:radio[name=programme_name]:checked').val();
    var discipline = $('input:radio[name=discipline]:checked').val();
    $.ajax({

        url: $('body').attr('data-base-url') + 'search/getDisciplineCourse',
        method: 'post',
        data: {
            id: $(this).attr('data-src'),
            programme_id: programme_id,
            discipline: discipline
        }
    }).done(function (response) {
        $('.search-discipline').html('');
        $('.search-discipline').html(discipline_value);
        $('#search_course').html('');
        $('#search_course').html(response);
        $("#course").addClass('active');
        $("#select-course-lnk").addClass('active');
        $("#discipline-lnk").removeClass('active');
        $("#discipline").removeClass('active');
        $("#discipline").addClass('selected');
        $("#programme").removeClass('active');
        $("#undergraduate-lnk").removeClass('active');
        return false;
    });
}

// Show Department list

function showDepartment(school_name) {
    var school_id = $('input:radio[name=school]:checked').val();
    $.ajax({

        url: $('body').attr('data-base-url') + 'search/getSchoolDeparements',
        method: 'post',
        data: {
            id: $(this).attr('data-src'),
            school_id: school_id
        }
    }).done(function (response) {
        $('#select_school').html('');
        $('#select_school').html(school_name);
        $('#deparement-block').html('');
        $('#deparement-block').html(response);
        $("#deparement-lnk").addClass('active');
        //$("#department_div").addClass('active');
        $("#school_div").addClass('active');
        $("#school_div").addClass('selected');
        $("#school-lnk").removeClass('active');
        return false;
    });
}

function AddReadMore() {
    //This limit you can set after how much characters you want to show Read More.
    var carLmt = 280;
    // Text to show when text is collapsed
    var readMoreTxt = " ... Read More <i class='icon-arrow-down-circle icons'></i>";
    // Text to show when text is expanded
    var readLessTxt = " Read Less <i class='icon-arrow-up-circle icons'></i>";


    //Traverse all selectors with this class and manupulate HTML part to show Read More
    $(".addReadMore").each(function () {
        if ($(this).find(".firstSec").length)
            return;

        var allstr = $(this).text();
        if (allstr.length > carLmt) {
            var firstSet = allstr.substring(0, carLmt);
            var secdHalf = allstr.substring(carLmt, allstr.length);
            var strtoadd = firstSet + "<span class='SecSec'>" + secdHalf + "</span><span class='readMore'  title='Click to Show More'>" + readMoreTxt + "</span><span class='readLess' title='Click to Show Less'>" + readLessTxt + "</span>";
            $(this).html(strtoadd);
        }

    });
    //Read More and Read Less Click Event binding
    $(document).on("click", ".readMore,.readLess", function () {
        $(this).closest(".addReadMore").toggleClass("showlesscontent showmorecontent");
    });
}

//Email Subscribe
function checkEmailField() {

    var email_id = $("#subscribeEmail").val();
    $("#subscribeEmail").removeClass('has-error');
    var emailReg = /^[a-z0-9]+([-._][a-z0-9]+)*@([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,4}$/;
    $("#subscribeEmail_msg").remove();
    if (email_id == '') {

        $("#subscribeEmail").addClass('has-error');
        $("<span style='color:red;' id='subscribeEmail_msg'>Please enter valid email id.</span>").insertAfter("#subscribe_div");
        return false;
    } else {

        if (emailReg.test(email_id)) {

            $.ajax({
                type: "POST",
                url: $('body').attr('data-base-url') + 'requestinfo/subscribedNow',
                data: { email_id: email_id },
                success: function (data) {

                    if (data > 0) {

                        $("<span style='color:#fff;' id='subscribeEmail_msg'>You have subscribed for sharda university updates successfully.</span>").insertAfter("#subscribe_div");
                        $("#subscribeEmail").val('');
                        setTimeout(function () { $('#subscribeEmail_msg').slideUp("slow"); }, 8000);
                        return false;
                    } else if (data == 'Already subscribed') {
                        $("<span style='color:red;' id='subscribeEmail_msg'>You have already subscribed for sharda university updates.</span>").insertAfter("#subscribe_div");
                        $("#subscribeEmail").val('');
                        setTimeout(function () { $('#subscribeEmail_msg').slideUp("slow"); }, 8000);
                        return false;
                    } else {
                        $("<span style='color:red;' id='subscribeEmail_msg'>Invalid Request</span>").insertAfter("#subscribe_div");
                        setTimeout(function () { $('#subscribeEmail_msg').slideUp("slow"); }, 4000);
                        return false;

                    }
                }
            });

        } else {
            $("#subscribeEmail").addClass('has-error');
            $("<span style='color:red;' id='subscribeEmail_msg'>Please enter valid email id.</span>").insertAfter("#subscribe_div");
            return false;
        }
    }
    return false;

}


function showProgrammeDiscipline(programme_id, discipline_id) {

    $.ajax({

        url: $('body').attr('data-base-url') + 'admissions/getProgrammeDiscipline',
        method: 'post',
        data: {
            id: $(this).attr('data-src'),
            programme_id: programme_id
        }
    }).done(function (response) {
        $('#discipline').html('');
        $('#discipline').append($('<option>').text(' -- Select Discipline -- ').attr('value', ''));
        $.each(response, function (i, value) {

            $('#discipline').append($('<option>').text(value).attr('value', i));
            if (value == discipline_id) {
                $('#discipline').append($('<option>').text('selected').attr('selected', i));

            }
        });
    });
}

function showDisciplineCourse(programme_id, discipline_id, course_id) {

    $.ajax({

        url: $('body').attr('data-base-url') + 'apply/getDisciplineCourse',
        method: 'post',
        data: {
            id: $(this).attr('data-src'),
            programme_id: programme_id,
            discipline_id: discipline_id
        }
    }).done(function (response) {
        $('#course').html('');
        $('#course').append($('<option>').text(' -- Select Course -- ').attr('value', ''));
        $.each(response, function (i, value) {

            $('#course').append($('<option>').text(value).attr('value', i));
            if (value == course_id) {
                $('#course').append($('<option>').text('selected').attr('selected', i));
            }





        });

    });
}

function close_pop() {
    setCookie('hide', true, 1);
    return false;
}

function getCookie(c_name) {
    var c_value = document.cookie;
    var c_start = c_value.indexOf(" " + c_name + "=");
    if (c_start == -1) {
        c_start = c_value.indexOf(c_name + "=");
    }
    if (c_start == -1) {
        c_value = null;
    } else {
        c_start = c_value.indexOf("=", c_start) + 1;
        var c_end = c_value.indexOf(";", c_start);
        if (c_end == -1) {
            c_end = c_value.length;
        }
        c_value = unescape(c_value.substring(c_start, c_end));
    }
    return c_value;
}

function setCookie(c_name, value, exdays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value = escape(value) + ((exdays == null) ? "" : "; expires=" + exdate.toUTCString());
    document.cookie = c_name + "=" + c_value;
}

/*
 * Function : validateglobalapplication
 */

function validateglobalapplication() {
    var dob = $("#datepicker").val();
    var father_name = $("#father_name").val();
    var mother_name = $("#mother_name").val();
    var gender = $("#gender").val();
    var passport_num = $("#passport_num").val();
    var country = $("#country").val();
    var address = $("#address").val();
    var city = $("#city").val();
    var sec_year = $("#sec_year").val();
    var sec_result = $("#sec_result").val();
    var sec_board = $("#sec_board").val();
    var sec_school = $("#sec_school").val();
    var sec_city = $("#sec_city").val();
    var sec_country = $("#sec_country").val();
    var sec_cgpa = $("#sec_cgpa").val();
    var sec_file = $("#sec_file").val();

    if (typeof dob == 'undefined') { dob = ''; }
    if (typeof father_name == 'undefined') { father_name = ''; }
    if (typeof mother_name == 'undefined') { mother_name = ''; }
    if (typeof gender == 'undefined') { gender = ''; }
    if (typeof passport_num == 'undefined') { passport_num = ''; }
    if (typeof country == 'undefined') { country = ''; }
    if (typeof address == 'undefined') { address = ''; }
    if (typeof city == 'undefined') { city = ''; }
    if (typeof sec_year == 'undefined') { sec_year = ''; }
    if (typeof sec_result == 'undefined') { sec_result = ''; }
    if (typeof sec_board == 'undefined') { sec_board = ''; }
    if (typeof sec_school == 'undefined') { sec_school = ''; }
    if (typeof sec_city == 'undefined') { sec_city = ''; }
    if (typeof sec_country == 'undefined') { sec_country = ''; }
    if (typeof sec_cgpa == 'undefined') { sec_cgpa = ''; }
    if (typeof sec_file == 'undefined') { sec_file = ''; }

    // Remove has-error class
    $("#datepicker").parent().removeClass('has-error');
    $("#father_name").parent().removeClass('has-error');
    $("#mother_name").parent().removeClass('has-error');
    $("#gender_div").parent().removeClass('has-error');
    $("#passport_num").parent().removeClass('has-error');
    $("#country_div").parent().removeClass('has-error');
    $("#address").parent().removeClass('has-error');
    $("#city").parent().removeClass('has-error');
    $("#sec_year").parent().removeClass('has-error');
    $("#sec_result_div").parent().removeClass('has-error');
    $("#sec_board").parent().removeClass('has-error');
    $("#sec_school").parent().removeClass('has-error');
    $("#sec_city").parent().removeClass('has-error');
    $("#sec_country").parent().removeClass('has-error');
    $("#sec_cgpa").parent().removeClass('has-error');
    $("#sec_file_div").parent().removeClass('has-error');

    var error_flag = 'N';
    if (dob == '') {
        $("#datepicker").parent().addClass("has-error");
        error_flag = 'Y';
        $('#dob').focus();
    }

    if (father_name == '') {
        $("#father_name").parent().addClass("has-error");
        error_flag = 'Y';
        $('#father_name').focus();
    }
    if (mother_name == '') {
        $("#mother_name").parent().addClass("has-error");
        error_flag = 'Y';
        $('#mother_name').focus();
    }

    if (gender == '') {
        $("#gender_div").parent().addClass("has-error");
        error_flag = 'Y';
        $('#gender').focus();
    }

    if (passport_num == '') {
        $("#passport_num").parent().addClass("has-error");
        error_flag = 'Y';
        $('#passport_num').focus();
    }
    if (country == '') {
        $("#country_div").parent().addClass("has-error");
        error_flag = 'Y';
    }
    if (address == '') {
        $("#address").parent().addClass("has-error");
        error_flag = 'Y';
    }
    if (city == '') {
        $("#city").parent().addClass("has-error");
        error_flag = 'Y';
    }

    if (sec_year == '') {
        $("#sec_year").parent().addClass("has-error");
        error_flag = 'Y';
        $('#sec_year').focus();
    }
    if (sec_result == '') {
        $("#sec_result_div").parent().addClass("has-error");
        error_flag = 'Y';
    }
    if (sec_board == '') {
        $("#sec_board").parent().addClass("has-error");
        error_flag = 'Y';
    }

    if (sec_school == '') {
        $("#sec_school").parent().addClass("has-error");
        error_flag = 'Y';
    }
    if (sec_city == '') {
        $("#sec_city").parent().addClass("has-error");
        error_flag = 'Y';
    }
    if (sec_country == '') {
        $("#sec_country").parent().addClass("has-error");
        error_flag = 'Y';
    }
    if (sec_cgpa == '') {
        $("#sec_cgpa").parent().addClass("has-error");
        error_flag = 'Y';
    }
    if (sec_file == '') {
        $("#sec_file_div").parent().addClass("has-error");
        error_flag = 'Y';
    }

    if (error_flag == 'Y') {
        return false;
    }


}

$('.journal-list').click(function () {
    var target = $(this).attr("id");
	$('.journal-list').removeClass('active');
	$(this).addClass('active');
    $('.right-panel .research-journals').addClass('hide');
    $('.right-panel .research-journals').removeClass('show');
    $(target).addClass('show');
});


$(document).ready(function () {  
	$('#linkIncrease').click(function () {  
		modifyFontSize('increase');  
	});  

	$('#linkDecrease').click(function () {  
		modifyFontSize('decrease');  
	});  

	$('#linkReset').click(function () {  
		modifyFontSize('reset');  
	})  

	function modifyFontSize(flag) {  
		var divElement = $('#divContent');  
		var currentFontSize = parseInt($("div").css('font-size'));  

		if (flag == 'increase')  
			currentFontSize += 5;  
		else if (flag == 'decrease')  
			currentFontSize -= 5;  
		else  
			currentFontSize = 16;  

		$("div").css({"font-size":currentFontSize}); 
	}  
}); 

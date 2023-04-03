$(document).ready(function(){
    $('.moblie_manu').hide();
    $('.moblie_sub_manu').hide();
    $('.icon_bars').click(function(){
        $('.moblie_manu').slideToggle();

    })

    $('.moblie_manu > li > a').click(function(){
        $(this).next('.moblie_sub_manu').slideToggle();
        
    })

    $('.minus').click(function(){
        $('.moblie_sub_manu').slideToggl();
    })


    $('#slider').owlCarousel({
        loop:true,
        margin:10,
        nav:false,
        margin:50,
        autoplay:true,
        // pullDrag:false,
        responsive:{
            0:{
                items:1
            },

            600:{
                items:2
            },
            992:{
                items:2
            },
            1200:{
                items:3
            }
        }
    })
});

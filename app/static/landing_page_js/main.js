$(function() {

	// $('.owl-1').owlCarousel({

 //    loop:true,
 //    margin:0,
 //    nav:true,
 //    items: 1,
 //    smartSpeed: 1000,
 //    autoplay: true,
 //    autoplayHoverPause: true,
 //    navText: ['<span class="icon-keyboard_arrow_left">', '<span class="icon-keyboard_arrow_right">']
	// })


    if ( $('.slide-one-item').length > 0 ) {
            $('.slide-one-item').owlCarousel({
            items: 1,
            loop: true,
                stagePadding: 0,
            margin: 0,
            autoplay: true,
            animateOut: 'slideOutDown',
            animateIn: 'fadeIn',
            pauseOnHover: false,
            nav: true,
            navText: ['<span class="icon-arrow_back">', '<span class="icon-arrow_forward">']
          });
      }


	
})
$( function() {
 var $cardcontainer = $('#cards').isotope({
    itemSelector: '.element-item',
    layoutMode: 'fitrows',
  });
  
  // init Isotope
  var $container = $('.isotope').isotope({
    itemSelector: '.articleItem',
    layoutMode: 'fitRows',
  });
  // bind filter button click
  $('#filters').on( 'click', 'btn', function() {
    var filterValue = $( this ).attr('data-filter');
    $container.isotope({ 
		filter: function () {
		  if(filterValue=='*'){
			return true
		  };
		  var cat = $(this).find('.articleInfo').text();
		  return cat.match( filterValue );
		}
	});
  });
	// filter element with category
// filter functions
 
  // change is-checked class on buttons
  $('.button-group').each( function( i, buttonGroup ) {
    var $buttonGroup = $( buttonGroup );
    $buttonGroup.on( 'click', 'button', function() {
      $buttonGroup.find('.is-checked').removeClass('is-checked');
      $( this ).addClass('is-checked');
    });
  });
  
});

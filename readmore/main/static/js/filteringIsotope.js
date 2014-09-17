$( function(){
    var $cardcontainer = $('#cards').isotope({
        itemSelector: '.element-item',   
    });
});

var $container = $('#articles');
$( function() {
    // init Isotope
    var qsRegex;
    $container.isotope({
        itemSelector: '.articleTile',
        layoutMode: 'fitRows',
        sortBy: 'random',
        filter: function() {
            var variable = qsRegex ? $(this).text().match( qsRegex ) : true;
            return variable ;
        }
    });
  
    // bind filter button click
    $('#filters').on( 'click', 'button', function() {
        var filterValue = $( this ).attr('data-filter');
        if(filterValue=='*'){ 
            qsRegex=null;
        } else {
            qsRegex = new RegExp( filterValue, 'gi' );
        }
        $container.isotope();
    });
    // use value of search field to filter
    var $quicksearch = $('#quicksearch').keyup( debounce( function() {
        qsRegex = new RegExp( $quicksearch.val(), 'gi' );
        $container.isotope();
    }, 200 ) );
});
// debounce so filtering doesn't happen every millisecond
function debounce( fn, threshold ) {
    var timeout;
    return function debounced() {
        if ( timeout ) {
            clearTimeout( timeout );
        }
        function delayed() {
            fn();
        timeout = null;
    }
    timeout = setTimeout( delayed, threshold || 100 );
    }
}
/*
$container.isotope({ 
		filter: function () {
		  if(filterValue=='*'){
			return true
		  };
		  var cat = $(this).find('.articleInfo').text();
		  return cat.match( filterValue );
		}
	});

  // change is-checked class on buttons
  $('.button-group').each( function( i, buttonGroup ) {
    var $buttonGroup = $( buttonGroup );
    $buttonGroup.on( 'click', 'button', function() {
      $buttonGroup.find('.is-checked').removeClass('is-checked');
      $( this ).addClass('is-checked');
    });
  });
	*/

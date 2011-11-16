$(document).ready(function() {

/* next/prev links */
function switchUL(hidenode, shownode, event, context) {
	var wrapper = $(context).parent().parent();
	$(hidenode, wrapper).fadeOut('fast', function() {
		$(hidenode, wrapper).removeClass('active');
		$(hidenode, wrapper).css('display', 'none');
		$(shownode, wrapper).fadeIn();
		$(shownode, wrapper).addClass('active');
	})
	event.preventDefault();
};
$("a.forward").click(function(event) {
	event.preventDefault();
	switchUL('.page1', '.page2', event, this)
});
$("a.backward").click(function(event) {
	event.preventDefault();
	switchUL('.page2', '.page1', event, this)
});
/* pop link */
$('a.anchor_pop').click(function(event) {
	event.preventDefault();
	var unit = $(this).parents('.unit')
	var active_view = $(".active", unit).clone();
	active_view.addClass('view_pop')
	
	var clone = $('#niftyclone');
	clone.hide();
	$('*', clone).remove();
	clone.append(active_view);
	$('*', clone).removeClass('hidden');
	
	$.facebox({ div: '#niftyclone' })
});
/* page link */
$('a.anchor_page').click(function(event) {
	event.preventDefault();
	var unit = $(this).parents('.unit')
	var active_view = $(".active", unit).clone();
	active_view.addClass('view_page');
	
	var backlink = '<a href="javascript:void(0);" class="anchor_back red">Exit View</a><hr />';
	
	var clone = $('#niftyclone');
	clone.hide();
	$('*', clone).remove();
	clone.append(backlink);
	clone.append(active_view);
	clone.append(backlink);
	$('.anchor_back', clone).click(function() {
		clone.fadeOut('fast');
		$('*', clone).remove();
		$('#niftyurls').fadeIn('fast');
	});
	$('#niftyurls').fadeOut('fast');
	clone.fadeIn('fast');
	$('*', clone).removeClass('hidden');
});

/* cufon actions */
Cufon.replace('h2.niftyurls', {
	fontFamily : 'Museo 500'
});
Cufon.now();
});
if(!window.console)
    window.console = {};
if(!window.console.firebug || !window.console.log)
    window.console.log = function() {};

$(document).ready(function(){
	$(".wikitcalendar .ticket").draggable({revert: "invalid"});
	$(".wikitcalendar .day, .wikitcalendar .today").droppable({
		hoverClass: "ui-state-hover",
		drop: function(event, ui) {
			ui.draggable.css({
				position: "auto",
				left: null,
				top: null
			});
			
			if(ui.draggable.parent()[0] == this)
				return;
			
			ui.draggable.appendTo(this);
			
			var ticket_field = $("table.wicketcalendar").attr("data-duedatefield");
			var ticket_number = ui.draggable.attr("data-ticketid");
			var new_value = $(this).attr("data-date");
            console.log("Changing "+ticket_field+" for #"+ticket_number+" to "+new_value+".");
            var url = $('link[rel="search"]').attr('href').replace(/\/search/, '');
            url += '/gridmod/update';
            var data = {'ticket': ticket_number};
            data[ticket_field] = new_value;
            var chromePath = $("script[src*='wikicalendar']").attr("src").replace("wikicalendar/wikicalendar.js", "gridmod/");
            var image = ui.draggable.find("img").get(0) || document.createElement('img');
            image.src = chromePath + 'loading.gif';
            $(image).appendTo(ui.draggable).fadeIn();
            $.ajax({
                // Although semantically this should be POST, that doesn't seem to work.
                'type': "GET",
                'url': url,
                'data': data,
                'success': function(){
                    console.log('Updated #'+ticket_number+'.');
                    image.src = chromePath + 'ok.png';
                    setTimeout(function(){$(image).fadeOut()}, 5000);
                },
                'error': function(){
                    console.log('Failed to update #'+ticket_number+'.');
                    image.src = chromePath + 'error.png';
                }
            });
		}
	});	
});

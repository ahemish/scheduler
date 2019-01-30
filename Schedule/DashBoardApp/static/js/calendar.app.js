var addEvent = function (patientName, appointmentColour, appointmentType, appointmentType  , start , end) {
    // var html = $('<li><span class="' + priority + '" data-description="' + description + '" data-icon="' + icon + '" data-start="' + start + '" data-end="' + end +'">' + title + '</span></li>').prependTo('ul#external-events').hide().fadeIn();
    var html = $('<li><span class="bg-color-darken txt-color-white" data-description="app" data-icon="dd" data-start="' + start + '" data-end="' + end +'">hello</span></li>').prependTo('ul#external-events').hide().fadeIn();

    $("#event-container").effect("highlight", 800);

};

var aEvent;


/*------------------------ Hide Patient Name ------------------------ */
function hideEvents()
    		{
    		
    			
 				$( '.fc-title' ).toggle();
    		}

/*------------------------ Hide Patient Name End ------------------------ */



       
        /*------------------------ Add Appointment ------------------------ */

	    function addAppointment () {
	        var patientName = $('#title').val(),
	            appointmentType = $('input:radio[name=iconselect]:checked').val(),
	            start = $('#start').val(),
	            end = $('#end').val(),
	            allDay = false,
	            phoneNumber = $("#phoneNumber").val(),
	            email = $("#email").val(),
	            notes = $("#notes").val();

				if(appointmentType == "New Patient")
				{
					var appointmentColour = "bg-color-darken txt-color-white";
				}
				else
				{
					var appointmentColour = "bg-color-blue txt-color-white";
					
				}
			var event;
	        addEvent(patientName, appointmentColour, appointmentType, appointmentType , start , end);
	       if (patientName) {
			   			//Used to render Event on fullcalendar Key Names are important
			             new_appointement =   {
									"title": patientName,
			                        "start": start,
			                        "end": end,
			                        "allDay": allDay,
			                        "className": appointmentColour,
									"appointment_type" : appointmentType,
									"phoneNumber": phoneNumber,
									"notes" : notes,
									"email" : email,             
			                    };
								
			                    
			                   
			                
			            
			            //console.log(event);
			            $.ajax({
    						type : "POST",
    						url : "/addAppointment",
    						data: JSON.stringify({
									"patientName": patientName,
									"phoneNumber": phoneNumber,
									"notes" : notes,
									"email" : email,
			                        "start": start,
			                        "end": end,
			                        "allDay": allDay,
			                        "appointmentColour": appointmentColour,
									"appointmentType" : appointmentType,
			                        "canceled" : false
			                    }),
    						contentType: 'application/json',
    						success: function(result) {
							new_appointement['id'] = result['id']
							$('#calendar').fullCalendar('renderEvent', new_appointement, true);
    						}
						});
				dialog.dialog( "close" );
		   }
	        
	        
	    };
	    
	    
	    /* ------------------------ Add Appointment End ------------------------ */


        		 /*------------------------ Update Appointment ------------------------ */

	     function updateAppointment (aEvent)
	     {
			var patientName = $('#appointmentTitle').text(),
	            appointmentType = $('input:radio[name=appointmentIconselect]:checked').val(),
	            start = $('#appointmentStart').val(),
	            end = $('#appointmentEnd').val(),
	            allDay = false,
	            phoneNumber = $("#appointmentPhoneNumber").val(),
	            email = $("#appointmentEmail").val(),
	            notes = $("#appointmentNotes").val();

				if(appointmentType == "New Patient")
				{
					var appointmentColour = "bg-color-darken txt-color-white";
				}
				else
				{
					var appointmentColour = "bg-color-blue txt-color-white";
					
				}     
	    var event;
	     
			             update_appointment = {
									"title": patientName,
			                        "start": start,
			                        "end": end,
			                        "allDay": allDay,
			                        "className": appointmentColour,
									"appointment_type" : appointmentType              
			                    };
			
				$.ajax({
    						type : "POST",
    						url : "{{ url_for('updateAppointment') }}",
    						data: JSON.stringify({
									"id" : aEvent.id,
									"patientName": patientName,
									"phoneNumber": phoneNumber,
									"notes" : notes,
									"email" : email,
			                        "start": start,
			                        "end": end,
			                        "allDay": allDay,
			                        "appointmentColour": appointmentColour,
									"appointmentType" : appointmentType,
			                        "canceled" : false
			                    }),
    						contentType: 'application/json',
    						success: function(result) {
								$('#calendar').fullCalendar( 'removeEvents' , aEvent._id);
								$('#calendar').fullCalendar('renderEvent', update_appointment, true);
    						}
						});
						
						appointmentDialog.dialog( "close" );
						
	     
	     
	
	    }
		/*------------------------ Update Appointment End ------------------------ */





        		/* ------------------------ Delete Appointment ------------------------ */


	     function deleteEvent () {
            $('#calendar').fullCalendar( 'removeEvents' , aEvent._id);
            $.ajax({
                           type : "POST",
                           url : "{{ url_for('deleteAppointment') }}",
                           data: JSON.stringify({"id": aEvent.id}),
                           contentType: 'application/json;charset=UTF-8',
                           success: function(result) {
                           //console.log(result);
                           }
                       });
             appointmentDialog.dialog( "close" );
        
        }
        
        /* ------------------------ Delete Appointment End ------------------------ */

     
        
            /* initialize the external events
             -----------------------------------------------------------------*/
        
            $('#external-events > li').each(function () {
                initDrag($(this));
            });
            
            /* added functions 
            ----------------------------------------------------------------*/
          
            
           
            // dialog = $( "#newEvent" ).dialog({
            //       autoOpen: false,
            //       height: 700,
            //       width: 350,
            //       modal: true,
            //       cache: false,
                  
            //       //dialogClass: "ui-dialog-titlebar ui-widget-header",
                  
            //     buttons: {
            //         "Add Event": addAppointment(),
            //         Cancel: function() {
            //           dialog.dialog( "close" );
                  
            //         }
            //         }
            //     });
                window.onload = function () {    
            var addEventButton = document.getElementById("addEvent")
                
            addEventButton.addEventListener('click', function() {
                addAppointment();
            }, false);
        }
            var typeOfAppointment = document.getElementsByClassName("appointment-type")
            $(".appointment-type").on('click', function(event) {
                event.preventDefault();
                console.log(this.text);
                console.log(event)
            });
         
        //  $( "#addEvent" ).button().on( "click", function() {
        //   dialog.dialog( "open" );
        // });
        
           
        //         appointmentDialog = $( "#appointment" ).dialog({
        //           autoOpen: false,
        //           height: 700,
        //           width: 350,
        //           modal: true,
        //           cache: false,
                  
                  
        //         buttons: {
        //             "update Event": updateAppointment(),
        //             "Delete Event": deleteEvent,
        //             Cancel: function() {
        //               appointmentDialog.dialog( "close" );
                  
        //             }
        //             }
        //         });
                
 

$(function nameSerach() {
    $("#title").autocomplete({
        source:function(request, response) {
            $.getJSON("/autocomplete",{
                q: request.term, // in flask, "q" will be the argument to look for using request.args
            }, function(data) {
                response(data.matching_results);
               // matching_results from jsonify
            });
        },
        minLength: 1,
        select: function(event, ui) {
        	
            $.post("{{url_for('getPatient')}}",{"data" : ui.item.value}, function(results, status){
        		
        		$('#notes').val(results[0].notes)
        		$('#email').val(results[0].email)
        		$('#phoneNumber').val(results[0].phoneNumber)
   			 });
        }
    });
});

function timeSelector(startTime , endTime , endpoint)
{

  
    if(typeof startTime != 'undefined' && typeof endTime != 'undefined')
    {

    }

    var hoursSelector = '<div class="dropdown d-inline"><button class="btn btn-secondary dropdown-toggle" type="button" id="appointmentMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
    hoursSelector = hoursSelector + '1</button><ul class="dropdown-menu scrollable-menu" role="menu">'

    for(i=1; i < 25; i ++)
    {
        hoursSelector = hoursSelector + '<li><a class="dropdown-item timeSelector" name="iconselect" value="" id="" href="#">'+i+'</a></li>'
    }
    hoursSelector = hoursSelector + '</ul></div></div>'

    var minutesSelector = '<div class="dropdown d-inline "><button class="btn btn-secondary dropdown-toggle" type="button" id="appointmentMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
    minutesSelector = minutesSelector + '0</button><ul class="dropdown-menu scrollable-menu" role="menu">'

    for(i=0; i < 60; i +=15)
    {
        minutesSelector = minutesSelector + '<li><a class="dropdown-item timeSelector" name="iconselect" value="" id="" href="#">'+i+'</a></li>'
    }
    minutesSelector = minutesSelector + '</ul></div></div>'

    selectors = '<label class="d-inline">Start </label>&nbsp;' + hoursSelector + '<strong> : </strong>' + minutesSelector + '&nbsp;&nbsp;&nbsp;<strong> - </strong>&nbsp;&nbsp;&nbsp;' +'<label class="d-inline">End </label>&nbsp;' + hoursSelector + '<strong> : </strong>' + minutesSelector
    return selectors;
    
}

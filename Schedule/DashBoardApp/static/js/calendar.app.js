function timeSelector()
{

    selectors = '<label class="d-inline">Start </label>&nbsp;' + hourMinutes("start") + '&nbsp;&nbsp;&nbsp;<strong> - </strong>&nbsp;&nbsp;&nbsp;' +'<label class="d-inline">End </label>&nbsp;' + hourMinutes("end")
    return selectors;
    
}



function hourMinutes(startOrEnd)
{

    var hoursSelector = '<div class="dropdown d-inline"><button class="btn btn-secondary dropdown-toggle" type="button" id="'+startOrEnd+'HoursSelectorButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
    hoursSelector = hoursSelector + '01</button><ul class="dropdown-menu scrollable-menu" role="menu">'

    for(i=1; i < 25; i ++)
    {
        if(i < 10)
        {
            var time = "0"+i;
        }
        else{
            time = i;
        }
        hoursSelector = hoursSelector + '<li><a class="dropdown-item timeSelector" name="iconselect" value="" id="" href="#">'+time+'</a></li>'
        
    }
    hoursSelector = hoursSelector + '</ul></div></div>'

    var minutesSelector = '<div class="dropdown d-inline "><button class="btn btn-secondary dropdown-toggle" type="button" id="'+startOrEnd+'MinutesSelectorButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
    minutesSelector = minutesSelector + '00</button><ul class="dropdown-menu scrollable-menu" role="menu">'

    for(i=0; i < 60; i +=15)
    {
        if(i < 10)
        {
           var time = "0"+i;
        }
        else{
            time = i;
        }
        minutesSelector = minutesSelector + '<li><a class="dropdown-item timeSelector" name="iconselect" value="" id="" href="#">'+time+'</a></li>'
        
    }
    minutesSelector = minutesSelector + '</ul></div></div>'

    selectors =  hoursSelector + '<strong> : </strong>' + minutesSelector
    return selectors;
    
}


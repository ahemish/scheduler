function timeSelector(startTime , endTime, startDate, endDate)
{

    selectors = '<label class="d-inline">Start </label>&nbsp;' + hourMinutes("start",startTime, startDate) + '&nbsp;&nbsp;&nbsp;<strong> - </strong>&nbsp;&nbsp;&nbsp;' +'<label class="d-inline">End </label>&nbsp;' + hourMinutes("end",endTime,endDate)
    return selectors;
    
}



function hourMinutes(startOrEnd,dateTime)
{
    var hours = dateTime.getHours();
    var minutes = dateTime.getMinutes();
    date = dateTime.getFullYear() +'-'+ (("0" + (dateTime.getMonth() + 1)).slice(-2))+'-'+(("0" + (dateTime.getDate() + 1)).slice(-2));
    if(hours < 10)
    {
        hours = "0" + hours;
    }
    if (minutes < 10)
    {
        minutes = "0"+minutes;
    }
    var hoursSelector = '<div class="dropdown d-inline"><button class="btn btn-secondary dropdown-toggle" type="button" id="'+startOrEnd+'HoursSelectorButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-date="'+date+'">'
    hoursSelector = hoursSelector + hours +'</button><ul class="dropdown-menu scrollable-menu" role="menu">'
    
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

    var minutesSelector = '<div class="dropdown d-inline "><button class="btn btn-secondary dropdown-toggle" type="button" id="'+startOrEnd+'MinutesSelectorButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-date="'+date+'">'
    minutesSelector = minutesSelector + minutes +'</button><ul class="dropdown-menu scrollable-menu" role="menu">'

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


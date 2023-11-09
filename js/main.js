/* UPDATE ALL 20 SECONDS */

function diffTimeToStr(time) {
	var seconds = time % 60;
	var minutes = Math.floor(time%3600 / 60);
	console.log(minutes);
	console.log(seconds);
	if (minutes > 0) {
		return (minutes);
	}
	else if (minutes >= 0) {
		return "< 1";
	}
	else {
		return "TIME ERROR (minutes < 0)";
	}
}

document.addEventListener("DOMContentLoaded", function() {
    // This code will run after the HTML content has fully loaded
    var lefttime_elm = document.getElementsByClassName("lefttime");
    let now = new Date();
    let elm_to_remove = [];

    for (var i = 0; i < lefttime_elm.length; i++) {
        var text_content_date = lefttime_elm[i].textContent;
        console.log(text_content_date)

        // Parse the text content into a Date object
        var date = new Date(text_content_date);

        var diff = Math.floor((date.getTime() - now.getTime())/1000);
        //diff += 60;
        
        console.log(diff);
        diff_time_str = diffTimeToStr(diff);
        if (diff <= 60 && diff >= 0) {
            lefttime_elm[i].textContent = "";
            lefttime_elm[i].classList.add("icon-now");
        }
        else if (diff < 0) {
            if (document.getElementById(i).classList == "message") {
                lefttime_elm[i].textContent = "";
            }
            else {
                elm_to_remove.push(document.getElementById(i));
            }
        }
        else {
            lefttime_elm[i].textContent = diff_time_str;
        }
    }

    // Remove elements outside of the loop
    elm_to_remove.forEach(function(element) {
        element.remove();
    });
  });
  
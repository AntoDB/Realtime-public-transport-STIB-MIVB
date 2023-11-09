/* UPDATE ALL 10 SECONDS */

// ====== Function so sort the data table in function of the lefttime (ASC) ===== //
function sortTableByLefttime() {
    // Get all elements with class "lefttime"
    var lefttime_elm = document.getElementsByClassName("lefttime");

    // Create an array to hold the elements and their corresponding "lefttime" values
    var elementsWithTime = [];

    // Get the current time
    var now = new Date();

    // Loop through the "lefttime" elements and calculate the time difference
    for (var i = 0; i < lefttime_elm.length; i++) {
        var text_content_date = lefttime_elm[i].textContent;

        // Parse the text content into a Date object
        var date = new Date(text_content_date);

        // Calculate the time difference in seconds
        var diff = Math.floor((date.getTime() - now.getTime()) / 1000);

        // Add the element and its "lefttime" value to the array
        elementsWithTime.push({ element: lefttime_elm[i], timeDifference: diff });
    }

    // Sort the elements based on the "lefttime" value
    elementsWithTime.sort(function(a, b) {
        return a.timeDifference - b.timeDifference;
    });

    // Remove all elements from the DOM
    /*elementsWithTime.forEach(function(elementWithTime) {
        elementWithTime.element.remove();
    });*/

    // Append the sorted elements back to the table
    var table = document.querySelector("table");

    elementsWithTime.forEach(function(elementWithTime) {
        table.appendChild(elementWithTime.element.parentElement.parentElement);
    });
}

// ====== Display the hour into the timeleft minute and removing the vehicule that aren't comming if there are any alert/message ===== //
function displayTimeleft() {
    // Get all elements with class "lefttime"
    var lefttime_elm = document.getElementsByClassName("lefttime");

    // Create an array to hold the elements that must be remove (passed time without alert/message)
    let elm_to_remove = [];

    // Get the current time
    var now = new Date();

    // Loop through the "lefttime" elements and calculate the time difference
    for (var i = 0; i < lefttime_elm.length; i++) {
        var text_content_date = lefttime_elm[i].textContent;

        // Parse the text content into a Date object
        var date = new Date(text_content_date);

        // Calculate the time difference in seconds
        var diff = Math.floor((date.getTime() - now.getTime()) / 1000);
        //diff += 60;

        // If the difference is less than one minute
        if (diff <= 60 && diff >= 0) {
            lefttime_elm[i].textContent = "";
            lefttime_elm[i].classList.add("icon-now");
        }

        // If the time is passed
        else if (diff < 0) {
            let getTrParent = lefttime_elm[i].parentElement.parentElement;
        
            // Check if the parent row has the "message" class
            // If the vehicule contain an alert/message, just remove the passed time, else remove parent row
            if (getTrParent.classList == "message") {
                lefttime_elm[i].textContent = "";
            }
            else {
                elm_to_remove.push(getTrParent);
            }
        }

        // If the difference of time is more than one minute
        else {
            lefttime_elm[i].textContent = Math.floor(diff / 60);
        }
    }

    // Remove elements outside of the loop
    elm_to_remove.forEach(function(element) {
        element.remove();
    });
}

document.addEventListener("DOMContentLoaded", function() {
    // This code will run after the HTML content has fully loaded
    //sortTableByLefttime();
    displayTimeleft();
  });
  
var nRobotInControl = null;

var signalMotor1 = 0, signalMotor2 = 0, signalMotor3 = 0;

function setControl(e) {
    
    if (nRobotInControl != null) {
        setStyleControl(2);
    }

    var buttonSelected = $(e);
    var valButton = buttonSelected.val();
    nRobotInControl = buttonSelected.parent();

    if (valButton == "to Control") {
        buttonSelected.val("Controling...");
        setStyleControl();
    }
    else {
        buttonSelected.val("to Control");
        setStyleControl(2);
        nRobotInControl = null;
    }

    /*
    var server_data = [
        {"QTc": "batata"},
        {"prolonged": "nois"},
        {"HR": "eu"},
        {"QT": "sim"},
        {"Sex": "sou"}
      ];

    $.ajax({
        type: "POST",
        url: "/process_qtc",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json' ,
    }).done(function(data) {
        console.log(data);
    });
    */

}

function setStyleControl(type = 1) {
    if (type == 1) {
        nRobotInControl.css("background-color", "rgb(191, 201, 228)");
    }
    else {
        nRobotInControl.css("background-color", "rgb(245, 245, 245)");
    }
}


var keyA, keyW, keyS, keyD, keyLeft, keyRight;

$(document).ready( function() {
    $("body").keydown(function(e) {  
        switch(e.keyCode) {
                
            case 37: keyLeft = true;
                break;
                
            case 39: keyRight = true;
                break;

            case 65: keyA = true;
                break;
                
            case 68: keyD = true;
                break;
                
            case 83: keyS = true;
                break;
                
            case 87: keyW = true;
                break;
                
            default:;
        }
    }); 

    $("body").keyup(function(e) {  
        switch(e.keyCode) {
                
            case 37: keyLeft = false;
                break;
                
            case 39: keyRight = false;
                break;

            case 65: keyA = false;
                break;
                
            case 68: keyD = false;
                break;
                
            case 83: keyS = false;
                break;
                
            case 87: keyW = false;
                break;
                
            default:;
        }
    }); 
});

window.setInterval(function(){
    if (nRobotInControl != null) {
        var element = $("." + nRobotInControl.attr("class") + " " + ".back_joystick ").children();
        var posX, posY, posArrow;

        if (keyW) 
            posY = -50
        else if (keyS) 
            posY = 50
        else 
            posY = 0

        if (keyA) 
            posX = -50
        else if (keyD) 
            posX = 50
        else 
            posX = 0
        
        if (posX != 0 && posY != 0) {
            posX = 50 * Math.sign(posX) / Math.sqrt(2);
            posY = 50 * Math.sign(posY) / Math.sqrt(2);
        }

        if (keyLeft)  {
            posArrow = -100;
            $("." + nRobotInControl.attr("class") + " input:nth-child(1)").css("background-color", "rgb(166, 191, 255)");
            $("." + nRobotInControl.attr("class") + " input:nth-child(2)").css("background-color", "white");
        }
        else if (keyRight) {
            posArrow = 100;
            $("." + nRobotInControl.attr("class") + " input:nth-child(2)").css("background-color", "rgb(166, 191, 255)");
            $("." + nRobotInControl.attr("class") + " input:nth-child(1)").css("background-color", "white");
        }
        else {
            $("." + nRobotInControl.attr("class") + " input:nth-child(1)").css("background-color", "white");
            $("." + nRobotInControl.attr("class") + " input:nth-child(2)").css("background-color", "white");
            posArrow = 0;
        }

        element.css("left", (posX + 50) + "px");
        element.css("top", (posY + 50) + "px");

        signalMotor1 = -1 * posX * 100.0 / 50;
        signalMotor2 = -1 * posY * 100.0 / 50;
        signalMotor3 = -1 * posArrow;
    }
    else {
        signalMotor3 = 0;
        signalMotor2 = 0;
        signalMotor1 = 0;
    }
}, 50);

var voiceAjax = 0;

window.setInterval(function(){
    voiceAjax++;

    if (voiceAjax == 4)
        voiceAjax = 1;

    if (nRobotInControl != null) {
        if (voiceAjax == 1) {
            $.ajax({
                type: "POST",
                url: "/motor",
                data: JSON.stringify( {"val" : "Cm1_" + Math.round(signalMotor1 * 10) / 10 + "@",
                                "indexSocket" :  $("." + nRobotInControl.attr("class") + " input[name='socketNumber']").val()} ),
                contentType: "application/json",
                dataType: 'json' ,
            });
        }
        else if (voiceAjax == 2) {
            $.ajax({
                type: "POST",
                url: "/motor",
                data: JSON.stringify( {"val" : "Cm2_" + Math.round(signalMotor2 * 10) / 10 + "@",
                                "indexSocket" :  $("." + nRobotInControl.attr("class") + " input[name='socketNumber']").val()} ),
                contentType: "application/json",
                dataType: 'json' ,
            });
        }
        else if (voiceAjax == 3) {
            $.ajax({
                type: "POST",
                url: "/motor",
                data: JSON.stringify( {"val" : "Cm3_" + Math.round(signalMotor3 * 10) / 10 + "@",
                                "indexSocket" :  $("." + nRobotInControl.attr("class") + " input[name='socketNumber']").val()} ),
                contentType: "application/json",
                dataType: 'json' ,
            });
        }
    }
}, 45);

window.setInterval(function(){
    var iframe = document.getElementById('camera1');
    iframe.src = iframe.src;
}, 500);



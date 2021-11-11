var nRobotInControl = null;
var lIpConnections = [];

var signalMotor1 = 0, signalMotor2 = 0, signalMotor3 = 0;

function setConnexion(e) {
    var ipToConnect = $(e).prev().val();
    var nameClassConnect = $(e).parent().parent().attr("class");

    $("." + nameClassConnect + " input[name='socketIp']").val(ipToConnect)
}

window.setInterval(function(){

    $.ajax({
        type: "POST",
        url: "/getConnexions",
        contentType: "application/json",
        dataType: 'json' ,
    }).done( function(data) {
        var lIpConnected = data["ipConnected"];

        $("input[name='socketIp']").each(function(index) {

            if ($.inArray($(this).val(), lIpConnected) > -1) {
                $(this).parent().css("background-color", "rgb(157, 255, 148)");
                $(this).next().show();
            }
            else {
                $(this).parent().css("background-color", "rgb(245, 245, 245)");
                $(this).next().hide();
            }
        });

    });

}, 300);

function setControl(e) {

    var buttonSelected = $(e);
    var valButton = buttonSelected.val();
    nRobotInControl = buttonSelected.parent();

    if (valButton == "to Control") {
        buttonSelected.val("Controling...");
    }
    else {
        buttonSelected.val("to Control");
        nRobotInControl = null;
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
            $("." + nRobotInControl.attr("class") + " .joystick input:nth-child(1)").css("background-color", "rgb(166, 191, 255)");
            $("." + nRobotInControl.attr("class") + " .joystick input:nth-child(2)").css("background-color", "white");
        }
        else if (keyRight) {
            posArrow = 100;
            $("." + nRobotInControl.attr("class") + " .joystick input:nth-child(2)").css("background-color", "rgb(166, 191, 255)");
            $("." + nRobotInControl.attr("class") + " .joystick input:nth-child(1)").css("background-color", "white");
        }
        else {
            $("." + nRobotInControl.attr("class") + " .joystick input:nth-child(1)").css("background-color", "white");
            $("." + nRobotInControl.attr("class") + " .joystick input:nth-child(2)").css("background-color", "white");
            posArrow = 0;
        }

        element.css("left", (posX + 50) + "px");
        element.css("top", (posY + 50) + "px");

        signalMotor1 = -1 * Math.sign(posX) * 70.0;
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
        valSetMotor = "";
        if (voiceAjax == 1) {
            valSetMotor = "Cm1_" + Math.round(signalMotor1 * 10) / 10 + "@";
        }
        else if (voiceAjax == 2) {
            valSetMotor = "Cm2_" + Math.round(signalMotor2 * 10) / 10 + "@";
        }
        else if (voiceAjax == 3) {
            valSetMotor = "Cm3_" + Math.round(signalMotor3 * 10) / 10 + "@";
        }

        if (valSetMotor != "") {
            
            $.ajax({
                type: "POST",
                url: "/setMotor",
                data: JSON.stringify( {"val" : valSetMotor,
                                "socketIp" :  $("." + nRobotInControl.attr("class") + " input[name='socketIp']").val()} ),
                contentType: "application/json",
                dataType: 'json' ,
            });
        }
    }
}, 70);

window.setInterval(function(){

    $("input[name='socketIp']").each(function(index) {

        try {
            $.getJSON("http://" + $(this).val() + "/Client", function(data) {
                $("#imgCameraCart1").attr('src', 'data:image/png;charset=utf8;base64,' + data.image);
            });
        } catch {
            
        }
        
    });
}, 70);



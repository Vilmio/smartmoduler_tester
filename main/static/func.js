var version = "0.0"

const rgb2hex = (rgb) => `#${rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/).slice(1).map(n => parseInt(n, 10).toString(16).padStart(2, '0')).join('')}`

function updateData() {
    $.ajax({ url: "/updateData" }).done(function (t) {
        $("#voltageL1").text(t.U1) 
        $("#voltageL2").text(t.U2)
        $("#voltageL3").text(t.U3)
        $("#currentL1").text((t.I1/100).toFixed(2))
        $("#currentL2").text((t.I2/100).toFixed(2))
        $("#currentL3").text((t.I3/100).toFixed(2))
        $("#evState").text(t.evState)
        $("#rfidCounter").text(t.rfidCounter)
        $("#rfidLength").text(t.rfidLength)
        $("#rfidID").text(t.rfidID)
        $("#evseMaxCurrent").text(t.evseMaxCurrent)
        if(t.serialStatus === true){
            $("#serial").text(t.serial)
            $("#serial").css("color","#9acd32")
        }
        else{
            $("#serial").text(t.serial)
            $("#serial").css("color","red")
        }
        if(rgb2hex($("#state").css("color")) === "#9acd32"){
            $("#state").css("color","red")
            $("#state").text("Reading ...")
        }else{
            $("#state").css("color","#9acd32")
            $("#state").text("Reading OK")
        }
    })
}


$(function () {
    $("div.mainContainer").load("overview", function () {
        $(".loader").hide(100);
        $.ajax({
            type: "POST",
            url: "/test",
            async: !0,
            data: JSON.stringify({ cmd: "get_firmware_version"}),
            success: function (e) {
                version = e.Status
                testerVersion = e.Tester
                $("#testerVersion").text(testerVersion)
            },
        });
        setInterval(function () {
            $.ajax({ url: "/updateData" }).done(function (t) {
                updateData(t)
            });
        }, 2e3);
    })
});

$(document).on("click", "#refresh", function () {
    location.reload();
})

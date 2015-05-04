function drawRoom(canvasCtx, roomString, mod) {
    'use strict';
        var i, x1, y1, x2, y2, state = 1;
    
        for (i = 0; i < roomString.length; i + 1) {
            console.log(i);
        if (roomString[i] === ',' && state === 1) {
            state = 2;
        } else if (roomString[i] === ',' && state === 3) {
            state = 4;
        } else if (roomString[i] === '-' && state === 2) {
            state = 3;
        } else if (roomString[i] === ';' && state === 4) {
            state = 1;
            canvasCtx.moveTo(x1 * mod, y1 * mod);
            canvasCtx.lineTo(x2 * mod, y2 * mod);
            canvasCtx.stroke();
            x1 = "";
            y1 = "";
            x2 = "";
            y2 = "";
        } else {

            switch (state) {
            case 1:
                if (x1 === undefined) {
                    x1 = roomString[i];
                } else {
                    x1 += roomString[i];
                }
                break;
            case 2:
                if (y1 === undefined) {
                    y1 = roomString[i];
                } else {
                    y1 += roomString[i];
                }
                break;
            case 3:
                if (x2 === undefined) {
                    x2 = roomString[i];
                } else {
                    x2 += roomString[i];
                }
                break;
            case 4:
                if (y2 === undefined) {
                    y2 = roomString[i];
                } else {
                    y2 += roomString[i];
                }
                break;
            }
        }

    }
}

function draw() {
    'use strict';
    var a = document.getElementById("a");
    var b = a.getContext("2d");

    var mydiv = document.getElementById("canvascont");

    b.canvas.width  = mydiv.offsetWidth;
    b.canvas.height = mydiv.offsetHeight;
    b.translate(0, a.height);
    b.scale(1, -1);
    
    var lwrHall = "0,0-0,116;0,0-8,0;8,0-8,116;";
    var upperHall = "0,116-0,232;0,232-8,232;8,232-8,116;";
    var lab = "8,96-30,96;30,96-30,48;8,48-30,48;";
    var mod = 3;

    b.lineWidth = 2;
    b.translate(50, 50);

    drawRoom(b, lwrHall, mod);
    //drawRoom(b, upperHall, mod);
    //drawRoom(b, lab, mod);


}

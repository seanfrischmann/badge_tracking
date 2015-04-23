<!DOCTYPE html xmlns ="http://www.w3.org/1999/xhtml">
    <head>
        <title>Mauraduer's Map</title>                

        <link href="css/styles.css" media="screen" rel="stylesheet" type="text/css"/>
<!--
                //<link href="css/jquery.dynatable.css" media="screen" rel="stylesheet" type="text/css"/>
-->

        <script src="scripts/canvaszoomscroll.js"></script>

        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
        <script src="scripts/jquery.dynatable.js"></script>
               
        
        
        
        

        

        
        <script>
        
                   
                   
                   
                   
                   
                   
function drawRoom(canvasCtx, roomString, mod) {
    'use strict';
        var i, x1, y1, x2, y2, state = 1;
    
        for (i = 0; i < roomString.length; i++) {
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
            
         
            
            

function draw(canvas, ctx, transX, transY, factor) {
    'use strict';

    var mydiv = document.getElementById("canvascont");

    ctx.canvas.width  = mydiv.offsetWidth;
    ctx.canvas.height = mydiv.offsetHeight;
    ctx.translate(0, a.height);
    ctx.scale(factor, -factor);
    
    var lwrHall = "0,0-0,116;0,0-8,0;8,0-8,116;";
    var upperHall = "0,116-0,232;0,232-8,232;8,232-8,116;";
    var lab = "8,96-30,96;30,96-30,48;8,48-30,48;";
    var mod = 3;

    ctx.lineWidth = 2;
    //ctx.translate(50, 50);
    ctx.translate(transX,transY);

    //drawRoom(ctx, lwrHall, mod);
    //drawRoom(ctx, upperHall, mod);
    //drawRoom(ctx, lab, mod);
    
    var img = document.getElementById("scream");
    ctx.drawImage(img, 10, 10);
    
/*
    for (var x = 0.5; x < ctx.canvas.width; x += 10) {
  ctx.moveTo(x, 0);
  ctx.lineTo(x, 381);
}

for (var y = 0.5; y < ctx.canvas.height; y += 10) {
  ctx.moveTo(0, y);
  ctx.lineTo(500, y);
}

ctx.moveTo(0,0);
ctx.lineTo(380,380);

ctx.strokeStyle = "#000";
ctx.stroke();
*/

    
    
    
    

    //ctx.fillStyle = "#00FF00";

    //ctx.fillRect(0,0,20,20);

}
                
                   
 function test(canvas, ctx){
     var lastX;
     var lasyY;
     var clickedX; 
     var clickedY;
     var dragStart;
     var dragged;
     var coordX = 0;
     var coordY = 0;
     var saveX = 0;
     var saveY = 0;
     var scaleFactor = 1.0;
    canvas.addEventListener('mousedown',function(evt){

        console.log("mousedown: " + evt.offsetX);
        document.body.style.mozUserSelect = document.body.style.webkitUserSelect = document.body.style.userSelect = 'none';
        clickedX = evt.offsetX || (evt.pageX - canvas.offsetLeft);
        clickedY = evt.offsetY || (evt.pageY - canvas.offsetTop);
/*        dragStart = ctx.transformedPoint(lastX,lastY);
                dragStart = (lastX,lastY);

        dragged = false;*/
                //console.log(clickedX + ", " + clickedY);
        dragStart = true;


          
    },false);
    canvas.addEventListener('mousemove',function(evt){
        lastX = evt.offsetX || (evt.pageX - canvas.offsetLeft);
        lastY = evt.offsetY || (evt.pageY - canvas.offsetTop);
        //dragged = true;
                    console.log("mousemove: ");


        if (dragStart){
            saveX = coordX-(clickedX - event.offsetX)/scaleFactor;
            saveY = coordY+(clickedY - event.offsetY)/scaleFactor;
            draw(canvas, ctx, saveX, saveY, scaleFactor);


            //console.log(event.offsetX);
        }
    },false);
    canvas.addEventListener('mouseup',function(evt){
        lastX = evt.offsetX || (evt.pageX - canvas.offsetLeft);
        lastY = evt.offsetY || (evt.pageY - canvas.offsetTop);
        
        dragStart = null;
        clickedX = 0;
        clickedY = 0;
        coordX = saveX;
        coordY = saveY;
        //clickedY = evt.offsetY || (evt.pageY - canvas.offsetTop);
     //   if (!dragged) zoom(evt.shiftKey ? -1 : 1 );
    },false);
     
     
     
     
     
  /*  var zoom = function(clicks){
        //var pt = ctx.transformedPoint(lastX,lastY);
        ctx.translate(lastX,lastY);
        factor = Math.pow(scaleFactor,clicks);
        //ctx.scale(factor,factor);
        ctx.translate(-lastX,-lastY);
        draw(canvas, ctx, coordX, coordY, factor);
    }*/

    var curZoom;
    var handleScroll = function(evt){
        //console.log(evt.wheelDelta);
        //var delta = evt.wheelDelta ? evt.wheelDelta/40 : evt.detail ? -evt.detail : 0;
        
        //console.log(delta);

        //if (delta) zoom(delta);
        
        
        if(evt.wheelDelta > 0){
            scaleFactor = scaleFactor + .1;

        }
        else if(evt.wheelDelta < 0){
            scaleFactor = scaleFactor - .1;
        }
        else{
            
        }
        
                    coordX = coordX -( (coordX - lastX)/scaleFactor + lastX*scaleFactor);
        ctx.translate(100,400);

        //coordY = coordY - lastY + lastY*scaleFactor;
         console.log("=" + coordX);

        draw(canvas, ctx, coordX, coordY, scaleFactor);

        return evt.preventDefault() && false;
    };
    canvas.addEventListener('DOMMouseScroll',handleScroll,false);
    canvas.addEventListener('mousewheel',handleScroll,false);
     
     
     
     
     
     
     
     
     
                
 }
                   
                   
        
        </script>
        
        
        
        <script>
            
$(document).ready(function(){
    $.dynatableSetup({
        features: {
            search: false,
            paginate: false, 
            perPageSelect: false},
      table: {
    defaultColumnIdStyle: 'camelCase'
  }});
    
    
              $("#content").load("livemap.php", function () {    // this line changed
              //draw();                                        // this line changed
             
                });   

    
     $("#livemap").click(function(){         

          $("#content").load("livemap.php", function () {    // this line changed
                    var canvas = document.getElementById("a");
                    var ctx = a.getContext("2d");  
                    test(canvas, ctx);
              
                    draw(canvas, ctx, 0, 0, 1);                                        // this line changed
              
                });                                                // this line changed

    });
    
    $("#employees").click(function(){
        
        $("#content").load("employees.php",function () {    // this line changed

            $.getJSON("sample_json/employees.json", function(data) {

                $("#employeetable").dynatable({
                    dataset: {
                        records: data.employees
                    }
                });
                
                
            });

        });
        
    });
    
    
     $("#settings").click(function(){
        $("#content").load("settings.php");

        
    });
    
    
        
     $("#moreinfo").click(function(){
         
         var res = confirm("Are you sure you want to leave the page?");
         if(res){
            window.location.href='http://www.acsu.buffalo.edu/~rrwasmer/cse_453/index.html';
         }
         else{
         }
    });
    
         $("#logout").click(function(){
             
             
             alert("Logging out!");
         });
    
    

    
});
            
    
</script>

        
    </head>

    <body>
        <div id="container">
                <div id="content">


          
                    
                </div>

                <div id="header">   
                    <div class="whitecolor">

                        <span class="helper"></span><img  id="headerImg" src="images/title.png" />

                        <div id="nav"
                            <ul>
                                <li><a id="livemap"><img  src ="images/icons/1429420112_icon-map-128.png"/>Map</a>
                                <li><a id="employees" ><img src ="images/icons/1429420194_user-256.png"/>Employees</a>
                                <li><a id="settings"><img  src ="images/icons/1429420260_settings-24-256.png"/>Settings</a>
                                <li><a id="moreinfo" ><img src ="images/icons/1429420271_circle_info_more-information_detail_-256.png"/>More Info</a>
                            </ul>
                        </div>
                        <a id="logout" href=""></a>
                    </div>
                </div>


    
        </div>
<img id="scream" width="220" height="277" src="images/dtown.png" alt="The Scream" style="display:none">
    </body
        
</html>
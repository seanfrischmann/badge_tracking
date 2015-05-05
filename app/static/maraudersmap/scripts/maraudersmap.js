/*GLOBAL VARS*/
var employees = [];
var selectedEmployeeIndex;

var canvas;
var ctx;
var transX;
var transY;
var factor;

function drawRoom(canvasCtx, roomString, mod) {
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
            
function drawBuilding(ctx) {

    var obrien = "20,0-20,138;20,138-69,138;69,138-69,250;77,250-77,129;77,129-28,129;28,129-28,0;28,0-20,0;";
    var baldy = "69,250-69,482;69,482-77,482;77,482-77,129;";
    var lab = "77,394-107,394;107,394-107,298;107,298-77,298;";
    var mod = 1;

    ctx.lineWidth = 1;

    drawRoom(ctx, obrien, mod);
    drawRoom(ctx, baldy, mod);
    drawRoom(ctx, lab, mod);
}

function drawEmployee(ctx, x, y){
    var radius = 5;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, 2 * Math.PI, false);
    ctx.fillStyle = '#0931c3';
    ctx.fill();
    ctx.lineWidth = 1;
    ctx.strokeStyle = '#062388';
    ctx.stroke();
}

//Main draw function, calls other draw functions
function draw(){
    var mydiv = document.getElementById("canvascont");
    ctx.canvas.width  = mydiv.offsetWidth;
    ctx.canvas.height = mydiv.offsetHeight;
    ctx.translate(0, a.height);
    ctx.scale(factor, -factor);
    ctx.translate(transX,transY);


    drawBuilding(ctx);
    console.log(selectedEmployeeIndex);
    if(selectedEmployeeIndex >= 0){
        console.log(employees[selectedEmployeeIndex][4])
        if(employees[selectedEmployeeIndex][3] == null || employees[selectedEmployeeIndex][4] == null ||
            employees[selectedEmployeeIndex][3] == "null" || employees[selectedEmployeeIndex][4] == "null"){
            drawEmployee(ctx, 0,0);
        }
        else{
            drawEmployee(ctx, parseInt(employees[selectedEmployeeIndex][3]),parseInt(employees[selectedEmployeeIndex][4]));
        }
    }
    else{
        var i = 0;
        for(i=0; i < employees.length; i++){
            if(employees[selectedEmployeeIndex][3] == null || employees[selectedEmployeeIndex][4] == null ||
              employees[selectedEmployeeIndex][3] == "null" || employees[selectedEmployeeIndex][4] == "null"){
                drawEmployee(ctx, 0,0);
            }
            else{
                drawEmployee(ctx, parseInt(employees[selectedEmployeeIndex][3]),parseInt(employees[selectedEmployeeIndex][4]));
            }        
        }
    }
}
               
function initOnAction(canvas, ctx){
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
    factor = 1.0;
    canvas.addEventListener('mousedown',function(evt){
        document.body.style.mozUserSelect = document.body.style.webkitUserSelect = document.body.style.userSelect = 'none';
        clickedX = evt.offsetX || (evt.pageX - canvas.offsetLeft);
        clickedY = evt.offsetY || (evt.pageY - canvas.offsetTop);
        dragStart = true;     
    },false);

    canvas.addEventListener('mousemove',function(evt){
        lastX = evt.offsetX || (evt.pageX - canvas.offsetLeft);
        lastY = evt.offsetY || (evt.pageY - canvas.offsetTop);
        if (dragStart){
            saveX = coordX-(clickedX - event.offsetX)/factor;
            saveY = coordY+(clickedY - event.offsetY)/factor;
            transX = saveX;
            transY = saveY;
            
            draw();
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
    },false);

    var curZoom;
    var handleScroll = function(evt){
        if(evt.wheelDelta > 0){
            factor = factor + .1;

        }
        else if(evt.wheelDelta < 0){
            factor = factor - .1;
        }
        else{
            
        }
        draw();
        return evt.preventDefault() && false;
    };

    canvas.addEventListener('DOMMouseScroll',handleScroll,false);
    canvas.addEventListener('mousewheel',handleScroll,false);       

 }

function myFunc() {
    var obj = $(this);
    //make all other li regular
    $(".highlightedItem").removeClass("highlightedItem");
    
    //highlight current li
    obj.addClass("highlightedItem");
    //display employee on map(needs to refresh)
    //alert(obj.data("id"));

    selectedEmployeeIndex = obj.data("index");
    draw();
}


function fillEmployees(){

    $("#mapsidebar ul").empty();

    if(selectedEmployeeIndex == -1){
        var insert = "<li data-index='-1' class='highlightedItem'><b>ALL EMPLOYEES</b></li>";
        $("#mapsidebar ul").append(insert);
    }
    else{
        var insert = "<li data-index='-1'><b>ALL EMPLOYEES</b></li>";
        $("#mapsidebar ul").append(insert);
    }

    var i = 0;
    for(i = 0; i< employees.length; i++){
        if(employees[i][1] == selectedEmployeeIndex){
            var insert = "<li data-index='"+i + "' + class='highlightedItem'>" +  employees[i][0] + "</li>";
            $("#mapsidebar ul").append(insert);
        }
        else{
            var insert = "<li data-index='"+i + "'>" +  employees[i][0] + "</li>";
            $("#mapsidebar ul").append(insert);
        }
    }
    
    $('#mapsidebar ul').delegate('li', 'click', myFunc);


}  

function fetchEmployees(){
    $.getJSON("http://marauder.homeip.net/get_employeeList", function(data) {
        employees = data.empList;
    });
}  

            
$(document).ready(function(){
    $.dynatableSetup({
        features: {
            search: false,
            paginate: false, 
            perPageSelect: false},
      table: {
    defaultColumnIdStyle: 'camelCase'
  }});
            
            fetchEmployees();

              $("#content").load("livemap.html", function () {    // this line changed
                    canvas = document.getElementById("a");
                    ctx = a.getContext("2d");  
                    initOnAction(canvas, ctx);
                    fetchEmployees();
                    fillEmployees();
                    //draw();
                    setInterval(function(){
                        fetchEmployees();
                        fillEmployees();
                        //draw();
                    }, 5000);
                });   

    
     $("#livemap").click(function(){         

          $("#content").load("livemap.html", function () {    // this line changed
                    canvas = document.getElementById("a");
                    ctx = a.getContext("2d");  
                    initOnAction(canvas, ctx);
                    fetchEmployees();
                    fillEmployees();
                    draw();
                    setInterval(function(){
                        fetchEmployees();
                        fillEmployees();
                        draw();
                    }, 5000);                                       // this line changed
              
                });                                                // this line changed

    });
    
    $("#employees").click(function(){
       

        $("#content").load("employees.html",function () {    // this line changed
            console.log("dogs");

            //name id location
            $("#employeetable").empty();
            var insert = "<thead><tr><th>Name</th><th>ID</th><th>Department</th></tr></thead><tbody>";
            var i = 0;
            for(i=0; i< employees.length; i++){
                insert += "<tr><td>" + employees[i][0] + "</td>";
                insert += "<td>" + employees[i][1] + "</td>";
                insert += "<td>" + employees[i][2] + "</td></tr>";
            }
            insert += "</tbody>";

            $("#employeetable").append(insert);
            

        });





            /*$.getJSON("sample_json/employees.json", function(data) {

                $("#employeetable").dynatable({
                    dataset: {
                        records: data.employees
                    }
                });
                
                
            });

        });*/
        
    });
    
    
     $("#settings").click(function(){
        $("#content").load("settings.html");

        
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
            

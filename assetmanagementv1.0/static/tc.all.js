//全局变量
var isedit = false;
var isfromstationid = false;
var areaeng;
var issave=false;
var isadd = false;
var addcount =0;
var isdel = false;

//弹出关键字查询结果
function popWin(obj){
	var _z=9000;//新对象的z-index
	var _mv=false;//移动标记
	var _x,_y;//鼠标离控件左上角的相对位置		
	var _obj= $("#"+obj);
	var _wid= _obj.width();
	var _hei= _obj.height();
	var _tit= _obj.find(".tit");
	var docE =document.documentElement;
	var left=($(document).width()-_obj.width())/2;
	var top =(docE.clientHeight-_obj.height())/2;
	_obj.css({	"left":left,"top":top,"display":"block","z-index":_z-(-1)});
			
	_tit.mousedown(function(e){
		_mv=true;
		_x=e.pageX-parseInt(_obj.css("left"));//获得左边位置
		_y=e.pageY-parseInt(_obj.css("top"));//获得上边位置
		_obj.css({	"z-index":_z-(-1)}).fadeTo(50,.5);//点击后开始拖动并透明显示	
	});
	$(document).mouseup(function(){
		if(_mv) {
            _mv = false;
            _obj.fadeTo("fast", 1);//松开鼠标后停止移动并恢复成不透明
        }
	});
	
	$(document).mousemove(function(e){
		if(_mv){
			var x=e.pageX-_x;//移动时根据鼠标位置计算控件左上角的绝对位置
			if(x<=0){x=0};
			x=Math.min(docE.clientWidth-_wid,x)-5;
			var y=e.pageY-_y;
			if(y<=0){y=0};
			y=Math.min(docE.clientHeight-_hei,y)-5;
			_obj.css({
				top:y,left:x
			});//控件新位置
		}
	});
    //双击页面可编辑
    // _obj.dblclick(function () {
    //     _obj.find("td").attr("contentEditable","true");
    //
    // })

	$('<div id="maskLayer"></div>').appendTo("body").css({
		"background":"#000","opacity":".4","top":0,"left":0,"position":"absolute","zIndex":"8000"
	});
	reModel();
	$(window).bind("resize",function(){reModel();});
	$(document).keydown(function(event) {
		if (event.keyCode == 27) {
			$("#maskLayer").remove();
			_obj.hide();
		}
	});
	function reModel(){
		var b = docE? docE : document.body,
		height = b.scrollHeight > b.clientHeight ? b.scrollHeight : b.clientHeight,
		width = b.scrollWidth > b.clientWidth ? b.scrollWidth : b.clientWidth;
		$("#maskLayer").css({
			"height": height,"width": width
		});
	};

};
//点击主资产号弹出资产详情
function queryinfo(obj, areaid){
    // $(this).parent().index();
    areaeng=areaid.substr(0,2);
    isfromstationid = false;
    HTMLinfo=$.ajax({type:"GET",url:"/queryinfo",data:{
        "aid":obj.text,"areaid":areaid},async:false,success: function(data){
       if(data[0] === "n" && data[1]==="o"){
            $("<div id='tempmsg' style='z_index:10000;'><p>未查询到资产详细信息。</p></div>").appendTo(obj).fadeOut("slow");
            window.setTimeout("$('#tempmsg').remove()",1000);
        }
        else {
            var row = document.createElement("tr"); //创建行
            row.setAttribute('id', 'inforow');
            for (var i = 0; i < data.length; i++) {
                var td111 = document.createElement("td"); //创建单元格
                td111.setAttribute('contentEditable', 'false');
                td111.setAttribute('class', 'newtdclass');
                td111.appendChild(document.createTextNode(data[i])); //为单元格添加内容
                row.appendChild(td111); //将单元格添加到行内
            }
            $("#infobody").append(row);
            popWin("Layer2");
        }},
		error:function(e){
		alert("没有取得数据");}
});};
//点击基站ID弹出基站所有的资产
function stationinfo(obj){
    isfromstationid = true;
    areaeng=obj.text.substr(0,2);
 	$.ajax({type:"GET",url:"/assetfromID",data:{
        "stationid":obj.text},async:false,success: function(data){
        if(data[0] === "n" && data[1]==="o"){
            $("<div id='tempmsg' style='z_index:10000;'><p>未查询到基站的资产详细信息。</p></div>").appendTo(obj).fadeOut("slow");
            window.setTimeout("$('#tempmsg').remove()",1000);
        }
 	    else{
            for(var i=0;i<data.length;i+=4) {
                var row=document.createElement("tr"); //创建行
                row.setAttribute('id','inforow');
                for (var j = 0; j < 4; j++) {
                    var td111 = document.createElement("td"); //创建单元格
                    td111.setAttribute('contentEditable', 'false');
                    td111.setAttribute('class', 'newtdclass');
                    td111.appendChild(document.createTextNode(data[i+j])); //为单元格添加内容
                    row.appendChild(td111); //将单元格添加到行内
                }
                $("#infobody").append(row);
            }
        popWin("Layer2");
        }},
		error:function(data){
		alert("没有取得数据");}
});};

function editinfo(obj) {
        isedit = true;
        issave = false;
    // $(obj).siblings("#exitinfo").attr("disabled","true");
    // $(obj).attr("disabled","true");
    $("#infobody tr td").attr("contentEditable","true");
    $("#infobody tr").each(function() { $(this).find("td").eq(0).attr("contentEditable","false"); } );
    $("#exitinfo").hide();
    $(obj).hide();
    // $("#exitinfo").attr("disabled","true");
    $("<div id='editdiv' style='text-align:center;background-color:lightblue'>").appendTo("#Layer2");
    if(isfromstationid) {
        $('<input type="button" id="add" value="增加" onclick="addinfo(this)"/>').appendTo("#editdiv");
        $('<input type="button" id="delete" value="删除" onclick="delinfo(this)"/>').appendTo("#editdiv");
    }
    $('<input type="button" id="save" value="保存" onclick="saveinfo(this)" />').appendTo("#editdiv");
    $('<input type="button" id="back" value="退出" onclick="backedit(this)" />').appendTo("#editdiv");
};

function exitinfo(obj){ //退出详细页面
    var oo = $(obj).parent().parent();
    oo.hide();
    $(obj).parent().parent().siblings("#maskLayer").remove();
    $(obj).parent().parent().find("#infobody").attr("contentEditable","false");
    // document.getElementById("infobody").deleteRow(0);
    $("#infobody tr").remove();      //移除表格
    $("#editdiv").remove();
    isfromstationid = false;
    isedit = false;
    addcount=0;
    if(isadd || isdel) {
        isadd = false;
        isdel = false;
        window.location.reload();
        //window.location.href=document.referrer;
    }
};

function addinfo(obj) {
    isedit = true;
    isadd = true;
    addcount +=1;
    var $tdnew = $("#inforow").clone();       //增加一行,克隆第一个对象
    $("#infobody").append($tdnew);
    $("#infobody tr:last").find("td").text("");   //将尾行的值清空
    $("#infobody tr:last").find("td").attr("contentEditable","true");
};

function delinfo(obj) {
    isdel =true;
    if(addcount >0 ){
        addcount -=1;
         $("#infobody tr:not(:first):last").remove();      //移除最后一行,并且保留前两行
    }
    else{
        alert("不支持删除原有资产。")
    }
};

function saveinfo(obj) {
    // isedit = false;
    issave = true;
    // $(obj).parent().remove();
    // document.getElementById("exitinfo").removeAttribute("disabled");
    // document.getElementById("editinfo").removeAttribute("disabled");
    var savestr={};
    savestr[2]=1;
    if(!isfromstationid){
        savestr[2]=0;
    }
    $("#infobody tr").each(function (j) {
        savestr[0]=j;
        savestr[1]=areaeng;
        $(this).find("td").each(function(i){
            savestr [i+3]= $(this).text();
        })
        $.ajax({type:"post",url:"/saveinfo",data:JSON.stringify(savestr),
             contentType: 'application/json; charset=UTF-8',async:false,success: function(data){
        },error:function(e){alert(data)}})
        })
};

function backedit(obj) {
    var saveflag = false;
    if (!issave){
        var statu =confirm("是否不保存退出?");
        if(statu){
            saveflag = true;
        }
    }
    if(issave || saveflag) {
        $("#editdiv").remove();
        $("#exitinfo").show();
        $("#editinfo").show();
        // $("#exitinfo").removeAttribute("disabled");
        $("#infobody tr td").attr("contentEditable", "false");
    }
};//退出编辑


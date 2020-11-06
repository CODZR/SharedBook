//================================
//js方式打开url
//参数：当前对象,被打开的url地址
//================================
function openurl(str,url){
	str.href="#";
	window.location.href=url;
}


//================================
//分页组件中的跳转
//参数：当前对象
//================================
function acc_page(obj,typeid,key) {
	var f_a=obj.options[obj.selectedIndex].value;
	if (f_a!=""){
		window.location.href="?page="+f_a+"&type_id="+typeid+"&key="+key+"";
   	}

}


//========================================
//url:打开的页面url,add:框架地址如minFrame
//========================================
function mainopen(url,add){
	window.top.frames[add].document.location.href=url;
}


//========================================
//自定义出错信息
//========================================
	//window.onerror=function(){
	//	alert("出错啦!");
	//	return true;
	//	}
  
var  flag=false;  
function  DrawImage(ImgD,width,height){  
     var  image=new Image();  
     image.src=ImgD.src;  
     if(image.width>0  &&  image.height>0){  
       flag=true;  
       if(image.width/image.height>=  width/height){  
         if(image.width>width){      
         ImgD.width=width;  
         ImgD.height=(image.height*width)/image.width;  
         }else{  
         ImgD.width=image.width;      
         ImgD.height=image.height;  
         }  
         //ImgD.alt=image.width+"×"+image.height;  
         }  
       else{  
         if(image.height>height){      
         ImgD.height=height;  
         ImgD.width=(image.width*height)/image.height;            
         }else{  
         ImgD.width=image.width;      
         ImgD.height=image.height;  
         }  
         //ImgD.alt=image.width+"×"+image.height;  
         }  
       }  
}    

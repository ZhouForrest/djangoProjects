/**
 * 获取元素只读样式
 */
function getStyle(elem){
	return window.getComputedStyle ? window.getComputedStyle(elem):elem.currentStyle;
};
/**
 * 根据元素id获取地址
 */
var cache = {};
function $(id){
	if (!cache[id]){
		cache[id] = document.getElementById(id);
	}
	return cache[id];	
}
/**
 * 根据类名获取地址
 */
function cls(cls){
	return document.getElementsByClassName(cls);
}
function unbind(elem, en, fn) {
	if (elem.removeEventListener) {
		elem.removeEventListener(en, fn);
	} else {
		elem.detachEvent('on' + en, fn);
	}
}
/**
 * 给元素绑定事件回调函数
 */
function bind(elem, en, fn) {
	if (elem.addEventListener) {
		elem.addEventListener(en, fn, true);
		//第三个参数默认为flase为事件冒泡-从内向外,定义为true为事件捕获-从外向里
	} else {
		elem.attachEvent('on' + en, fn);
	}
}
/**
 *将使用了固定定位的元素变成可拖拽元素
 * @param{HTMLElement} elem 使用了固定定位的元素
 */
function makeDraggable(elem) {
	elem.isMouseDown = false;
	elem.originleft = 0;
	elem.origintop = 0;
	elem.mousex = 0;
	elem.mousey = 0;
	bind(elem, 'mousedown', function(evt) {
		evt = evt || window.event;
		elem.isMouseDown = true;
		var divStyle = getStyle(elem);
		elem.originleft = parseInt(divStyle.left);
		elem.origintop = parseInt(divStyle.top);
		elem.mousex = evt.clientX;
		elem.mousey = evt.clientY;
	});
	bind(elem, 'mouseup', function() {
		elem.isMouseDown = false;
	});
	bind(elem, 'mouseout', function() {
		elem.isMouseDown = false;
	});
	bind(elem, 'mousemove', function(evt) {
		if(!elem.isMouseDown) return;
		evt = evt || window.event;
		var dx = evt.clientX - elem.mousex;
		var dy = evt.clientY - elem.mousey;
		elem.style.left = (elem.originleft + dx) + 'px';
		elem.style.top = (elem.origintop + dy) + 'px';
	});
}
/**
 * 处理事件对象,解决兼容性问题
 */
function handleEvent(evt){
	evt || event;	
	evt.preventDefault = evt.preventDefault() || 
		function(){
			this.returnValue = false;
		};
	evt.stopPropagation = evt.stopPropagation() ||
		function(){
			this.cancelBubble = true;
		};
	return evt;	
}

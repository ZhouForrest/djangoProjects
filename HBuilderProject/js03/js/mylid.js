//缓存:牺牲空间节约时间
var cache = {};

function $(id) {
	if(!cache[id]) {
		cache[id] = document.getElementById(id);
	}
	return cache[id];
}
/**
 * 给元素绑定事件
 */
function bind(elem, en, fn) {
	if(elem.addEventListener) {
		elem.addEventListener(en, fn);
	} else {
		elem.attachEvent('on' + en, fn);
	}
}

function unbind(elem, en, fn) {
	if(elem.removeEventListener) {
		elem.removeEventListener(en, fn);
	} else {
		elem.detachEvent('on' + en, fn);
	}
}

function getStyle(elem) {
	return window.getComputedStyle ? window.getComputedStyle(elem) : elem.currentStyle;
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
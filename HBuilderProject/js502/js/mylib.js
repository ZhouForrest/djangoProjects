//缓存:牺牲空间节约时间
var cache = {};
function $(id){
	if (!cache[id]){
		cache[id] = document.getElementById(id);
	}
	return cache[id];	
}

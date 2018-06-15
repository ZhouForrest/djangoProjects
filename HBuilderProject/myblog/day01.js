//variable - 变量
function foo() {
	var name = window.prompt('please input your name')
	console.log(typeof(name));
	if(name && name != 'null') {
		window.alert('hello ' + name + '!');
	} else {
		window.alert('what?')
		window.alert('hello everybody!')
	}
}
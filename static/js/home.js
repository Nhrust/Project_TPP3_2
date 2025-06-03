socket = io();

const checkbox_html = "<path d=\"M7 19h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2z\"/>";
const checkbox_checked_html = "<path d=\"M7 5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2H7zm4 10.414-2.707-2.707 1.414-1.414L11 12.586l3.793-3.793 1.414 1.414L11 15.414z\" stroke-linejoin=\"round\"/>";
const checkbox_minus_html = "<path d=\"M17 5H7a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zm-1 8H8v-2h8z\"/>";

var selected = Array();
var hidden = Array();

function filter() {
	document.querySelectorAll(".product").forEach(element => {
		const category = element.querySelector("metaD").className;
		if (selected.length != 0 && !selected.includes(category)) {
			element.style.display = "none";
		}
		else if (hidden.includes(category)) {
			element.style.display = "none";
		}
		else {
			element.style.display = "block";
		}
	})
};

filter();

console.log("Home");

document.querySelectorAll("svg").forEach(element => {
	element.innerHTML = checkbox_html;
});

document.querySelectorAll(".product > btn").forEach(element => {
	element.textContent = element.textContent + "$";
});

document.querySelectorAll(".category").forEach(element => {
	element.addEventListener("click", () => {
		const svg = element.querySelector("svg");
		const v = element.attributes.getNamedItem("v");
		const category = element.querySelector("p").textContent;
		var type = (Number(v.value) + 1);
		
		if (type == 1) {
			svg.innerHTML = checkbox_checked_html;
			selected.push(category);
		}
		else if (type == 2) {
			svg.innerHTML = checkbox_minus_html;
			selected.splice(selected.indexOf(category), 1);
			hidden.push(category);
		}
		else if (type == 3) {
			type = 0;
			svg.innerHTML = checkbox_html;
			hidden.splice(hidden.indexOf(category), 1);
		}
		v.nodeValue = type;
		filter();
	})
});

document.querySelectorAll(".product btn").forEach(element => {
	element.addEventListener("click", () => {
		socket.emit("add_to_cart", element.parentNode.querySelector("metaD").id);
	})
});

socket.on("cart", (cart_string) => {
	const cart = JSON.parse(cart_string);

	for (const key in cart) {
		const product = document.getElementById(key).parentNode;
		product.querySelector("btn").textContent = " В корзине: " + cart[key];
	}
});

socket.emit("get_cart");

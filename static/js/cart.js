socket = io();

document.querySelectorAll("buttons btn.add").forEach(element => {
	element.addEventListener("click", () => {
		console.log("add");
		socket.emit("add_to_cart", element.parentNode.parentNode.querySelector("metaD").id);
	})
});

document.querySelectorAll("buttons btn.remove").forEach(element => {
	element.addEventListener("click", () => {
		socket.emit("remove_from_cart", element.parentNode.parentNode.querySelector("metaD").id);
	})
});

socket.on("cart", (cart_string) => {
	const cart = JSON.parse(cart_string);

	for (const key in cart) {
		const product = document.getElementById(key).parentNode;

		product.querySelector("buttons > p").textContent = " В корзине: " + cart[key];
	}

	document.querySelectorAll(".product").forEach(element => {
		if (!(element.querySelector("metaD").id in cart)) {
			element.parentNode.removeChild(element);
		}
	});
});

socket.emit("get_cart");

document.querySelector(".pay_field .btn").addEventListener("click", () => {
	const video = document.querySelector(".main-image video");
	video.muted = false;
	document.querySelector(".main-image video source").src = "../static/assets/vid2.mp4";
	console.log(document.querySelector(".main-image video source").src);
	video.load();
	video.play();
});

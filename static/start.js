
document.getElementById('mainButton').addEventListener('click', function () {
    window.location.href = "/BLC/";
});

const open = () => {
    document.querySelector(".modal").classList.remove("hidden");
}

const close = () => {
    document.querySelector(".modal").classList.add("hidden");
}

document.querySelector(".payment").addEventListener("click", open);
document.querySelector(".close").addEventListener("click", close);
document.querySelector(".bg").addEventListener("click", close);


$(document).ready(function () {
    var video = document.getElementById('camera-stream');
    var items_list = $('#items_list');
    var total_quantity = $('#total_quantity');
    var total_amount = $('#total_amount');
    var totalQuantity = 0;
    var num = 0;
    function playVideo() {
        video.src = "video_start/";
    }

    function updateAmount(totalAmount, eachAmount) {
        items_list.empty();
        total_amount.empty();
        total_quantity.empty();
        total_amount.append(totalAmount + ' 원');
        totalQuantity = 0;
        num = 0;
        var itemList = $('<ul></ul>');
        for (var key in eachAmount) {
            num+=1
            var price = eachAmount[key][0];
            var quantity = eachAmount[key][1];
            itemList.append('<li>' + num + ' ' + key + ': ' + quantity + '개' + "\\" + price + '</li>');
            totalQuantity += quantity;
        };
        total_quantity.append(totalQuantity);
        items_list.append(itemList);
    }
    
    playVideo();

    setInterval(function () {
        $.ajax({
            url: 'get_amount/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                var totalAmount = data.total_amount;
                var eachAmount = data.each_amount;
                updateAmount(totalAmount, eachAmount);
            }
        });
    }, 1000);
});

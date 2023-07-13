
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
document.querySelector('.bg').addEventListener("click", close);

const open2 = () => {
    document.querySelector(".modal2").classList.remove("hidden2");
    setTimeout(close2, 2000);
}

const close2 = () => {
    document.querySelector(".modal2").classList.add("hidden2");
    document.querySelector(".modal").classList.add("hidden");
}

document.querySelector('.Yes').addEventListener("click", open2);
document.querySelector('.bg2').addEventListener("click", close2);


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

    playVideo();
    
    function updateAmount(totalAmount, eachAmount) {
        items_list.empty();
        total_amount.empty();
        total_quantity.empty();
        total_amount.append(totalAmount + ' 원');
        totalQuantity = 0;
        num = 0;
        var itemList = $('<td></td>');
        for (var key in eachAmount) {
            num += 1
            var price = eachAmount[key][0];
            var quantity = eachAmount[key][1];
            itemList.append('<tr>' + '<td class="num">' + num + '</td>' + '<td class="name">' + key + '</td>' + '<td class="quantity">' + quantity + '</td>' + '<td class="price">\\' + price + '</td>' + '</tr>');
            totalQuantity += quantity;
        };
        total_quantity.append(totalQuantity);
        items_list.append(itemList);
    }

    var intervalId = setInterval(function () {
        $.ajax({
            url: 'get_amount/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                var totalAmount = data.total_amount;
                var eachAmount = data.each_amount;
                updateAmount(totalAmount, eachAmount);
            },
            error: function (xhr, status, error) {
                // Django 서버가 다운되었을 때 처리할 작업을 여기에 추가합니다.
                clearInterval(intervalId);  // Interval을 중지합니다.
                console.log("Django 서버가 다운되었습니다. JavaScript 함수를 중지합니다.");
            }
        });
    }, 1000);
});



// 결재버튼시
document.querySelector('.payment').addEventListener("click", function(){
    $.ajax({
        url: 'pause_video/',
        type: 'GET',
        data:{'data':0}
    })
});
// 취소시
document.querySelector('.close').addEventListener("click", function(){
    $.ajax({
        url: 'pause_video/',
        type: 'GET',
        data:{'data':1}
    })
});

document.querySelector('.Yes').addEventListener("click", function() {
    $.ajax({
        url: 'process_payment/',
        type: 'POST',
        dataType: 'json',
        success: function(response) {
            // 결제 완료 메시지 출력 등 원하는 동작 수행
            console.log(response.message);

            setTimeout(() => {
                window.location.href = '/BLC/'                
            }, 2000);
            
        }
    });
});
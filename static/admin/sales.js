let salesData = {}
fetch('/BLC/get_daily_sales/')
  .then(response => response.json())
  .then(data => {
    salesData = data;
    renderCalendar();
  })
  .catch(error => {
    console.error('Error:', error);
});

// Get Current Date
const currentDate = new Date();
let currentMonth = currentDate.getMonth();
let currentYear = currentDate.getFullYear();

// DOM Elements
const prevMonthBtn = document.getElementById('prev-month-btn');
const nextMonthBtn = document.getElementById('next-month-btn');
const monthYearLabel = document.getElementById('month-year');
const daysContainer = document.querySelector('.days');
const modal = document.getElementById('sales-modal');
const modal2 = document.getElementById('detail-sales-modal');
const modalDate = document.getElementById('modal-date');
const modalSales = document.getElementById('modal-sales');
const closeModalBtn = document.getElementsByClassName('close')[0];
const closeModalBtn2 = document.getElementsByClassName('close2')[0];
const totalSalesAmount = document.getElementById('total-sales-amount');

// Event Listeners
prevMonthBtn.addEventListener('click', showPrevMonth);
nextMonthBtn.addEventListener('click', showNextMonth);
closeModalBtn.addEventListener('click', closeModal);
closeModalBtn2.addEventListener('click', closeModal2);

// Function to Render Calendar
function renderCalendar() {
  // Clear Days Container
  daysContainer.innerHTML = '';

  // Set Month and Year Label
  const monthYearString = new Date(currentYear, currentMonth).toLocaleString('default', {
    month: 'long',
    year: 'numeric',
  });
  monthYearLabel.textContent = monthYearString;

  // Add Day Names
  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat'];
  for (let i = 0; i < dayNames.length; i++) {
    const dayNameElement = document.createElement('div');
    dayNameElement.classList.add(dayNames[i]);
    dayNameElement.textContent = dayNames[i];
    daysContainer.appendChild(dayNameElement);
  }

  // Get First Day and Last Day of the Month
  const firstDay = new Date(currentYear, currentMonth, 1);
  const lastDay = new Date(currentYear, currentMonth + 1, 0);

  // Fill Previous Month Days
  const prevMonthDays = firstDay.getDay();
  for (let i = prevMonthDays; i > 0; i--) {
    const day = new Date(currentYear, currentMonth, -i + 1);
    createDayElement(day, 'prev-month');
  }

  // Fill Current Month Days
  for (let i = 1; i <= lastDay.getDate(); i++) {
    const day = new Date(currentYear, currentMonth, i);
    createDayElement(day, 'current-month');
  }

  // Fill Next Month Days
  const nextMonthDays = 6 - lastDay.getDay();
  for (let i = 1; i <= nextMonthDays; i++) {
    const day = new Date(currentYear, currentMonth + 1, i);
    createDayElement(day, 'next-month');
  }

  // Show Total Sales for the Month
  showTotalSales();
}

// Function to Create Day Element
function createDayElement(date, className) {
  const dayElement = document.createElement('div');
  dayElement.classList.add('day', className);
  dayElement.textContent = date.getDate();

  // Check if Sales Data exists for the day
  const salesKey = getDateString(date);
  if (salesData[salesKey]) {
    dayElement.classList.add('has-sales');

    const salesAmountElement = document.createElement('div');
    salesAmountElement.classList.add('sales-amount');
    salesAmountElement.textContent = salesData[salesKey].toLocaleString('ko-kr');
    dayElement.appendChild(salesAmountElement);
  }

  // Classify the date under the day of the week
  const dayOfWeek = date.getDay();
  switch (dayOfWeek) {
    case 0:
      dayElement.classList.add('Sun');
      break;
    case 6:
      dayElement.classList.add('Sat');
      break;
    default:
      dayElement.classList.add('weekday');
      break;
  }

  dayElement.addEventListener('click', () => openModal(date));

  daysContainer.appendChild(dayElement);
}
// Function to Show Total Sales for the Month
function showTotalSales() {
  let totalSales = 0;

  for (const key in salesData) {
    const date = new Date(key);
    if (date.getMonth() === currentMonth && date.getFullYear() === currentYear) {
      totalSales += salesData[key];
    }
  }

  totalSalesAmount.textContent = totalSales.toLocaleString('ko-kr');
}

// Function to Show Previous Month
function showPrevMonth() {
  if (currentMonth === 0) {
    currentMonth = 11;
    currentYear--;
  } else {
    currentMonth--;
  }
  renderCalendar();
}

// Function to Show Next Month
function showNextMonth() {
  if (currentMonth === 11) {
    currentMonth = 0;
    currentYear++;
  } else {
    currentMonth++;
  }
  renderCalendar();
}

function openModal(date) {
  const salesKey = getDateString(date);
  const salesUrl = `/BLC/get_sales/${salesKey}/`;
  
  fetch(salesUrl)
    .then(response => response.json())
    .then(data => {
      const modalDate = document.getElementById('modal-date');

      let salesHTML = '';
      salesHTML += `<h1>BLC</h1>`
      salesHTML += `<table class=date><thead><tr><th class='sale_date'>일자</th><th class='sale_id'>판매번호</th><th class='sale_price'>총 판매액</th></tr></thead><tbody>`
      data.sales.forEach(sale => {
        salesHTML += `<tr><td class='sale_date'>${sale.sale_date}</td>`;
        salesHTML += `<td class='sale_id' onclick='openModalOnSaleId(${sale.sale_id})'>${sale.sale_id}</td>`;
        salesHTML += `<td class='sale_price'>\\${sale.total_price.toLocaleString('ko-kr')}</td></tr>`;
      });
      salesHTML += `</tbody></table>`;

      modalDate.innerHTML = salesHTML;
      
      modal.style.display = 'flex';
    })
    .catch(error => console.log(error));
}

function openModalOnSaleId(saleId) {
  const saleDetailsUrl = `/BLC/get_detail_sales/${saleId}/`;
  
  fetch(saleDetailsUrl)
    .then(response => response.json())
    .then(data => {
      const modalSales = document.getElementById('modal-sales');
      let salesHTML = ``;
      salesHTML += `<h2>판매번호 : ${saleId}</h2>`
      salesHTML += `<table class=detail><thead><tr><th class='item_id'>id</th><th class='item_name'>품명</th><th class='item_quantity'>개수</th><th class='unit_price'>가격(\\)</th><th class='item_price'>총 가격(\\)</th></tr></thead><tbody>`;
      data.detail_sales.forEach(detail_sale => {
        salesHTML += `<tr><td class='item_id'>${detail_sale.item}</td>`;
        salesHTML += `<td class='item_name'>${detail_sale.item__item_name}</td>`;
        salesHTML += `<td class='item_quantity'>${detail_sale.quantity}</td>`;
        salesHTML += `<td class='unit_price'>${(detail_sale.unit_price/detail_sale.quantity).toLocaleString('ko-kr')}</td>`
        salesHTML += `<td class='item_price'>${detail_sale.unit_price.toLocaleString('ko-kr')}</td></tr>`;
      });
      salesHTML += `</tbody></table>`;

      modalSales.innerHTML = salesHTML;
      modal2.style.display = 'flex';
    })
    .catch(error => console.log(error));
}


// Function to Close Modal
function closeModal() {
  modal.style.display = 'none';
}
// Function to Close Modal2
function closeModal2() {
  modal2.style.display = 'none';
}


// Helper Function to Get Date String in "YYYY-MM-DD" Format
function getDateString(date) {
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  return `${year}-${month}-${day}`;
}

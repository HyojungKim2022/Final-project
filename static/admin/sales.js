// Calendar Data
const salesData = {
  '2023-07-01': 1500000,
  '2023-07-04': 200,
  '2023-07-10': 100,
  '2023-07-15': 300,
  '2023-07-20': 250,
  '2023-07-25': 180,
};

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
const modalDate = document.getElementById('modal-date');
const modalSales = document.getElementById('modal-sales');
const closeModalBtn = document.getElementsByClassName('close')[0];
const totalSalesAmount = document.getElementById('total-sales-amount');

// Event Listeners
prevMonthBtn.addEventListener('click', showPrevMonth);
nextMonthBtn.addEventListener('click', showNextMonth);
closeModalBtn.addEventListener('click', closeModal);

// Initial Calendar Render
renderCalendar();

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

// Function to Open Modal and Show Sales Details
//   function openModal(date) {
//     modalDate.textContent = getDateString(date);
//     const salesKey = getDateString(date);
//     modalSales.textContent = `Sales: ${salesData[salesKey] ? salesData[salesKey] : 'No sales'}`;

//     modal.style.display = 'flex';
//   }

function openModal(date) {
  const salesKey = getDateString(date);
  const salesUrl = `/get_sales_details/${salesKey}/`;

  fetch(salesUrl)
    .then(response => response.text())
    .then(data => {
      modal.innerHTML = data;
      modal.style.display = 'flex';
    })
    .catch(error => console.log(error));
}

// Function to Close Modal
function closeModal() {
  modal.style.display = 'none';
}

// Helper Function to Get Date String in "YYYY-MM-DD" Format
function getDateString(date) {
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  return `${year}-${month}-${day}`;
}

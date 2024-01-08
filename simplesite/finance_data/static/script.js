const chartCtx = document.getElementById('myChart');
let financeChart, portfolioChart;
let headlinesData, headlinesCount; // global variables for headlines
let portfolio;
let companies;
let selectedTicker;
let allTickersData = {};

function loadChart(data) {
    if (financeChart) {
        financeChart.destroy();
    }
    financeChart = new Chart(chartCtx, {
        type: 'line',
        data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    });
}

async function updateAllTickersData() {
    for (const item of portfolio) {
        const financeData = await fetchFinanceData(item.Ticker);
        allTickersData[item.Ticker] = financeData;
    }

}

async function loadPortfolioChart() {
    if (portfolioChart) {
        portfolioChart.destroy();
    }
    
    let labels;
    const chartData = {
        datasets: Object.keys(allTickersData).map((ticker, i) => {
            if (!labels) {
                labels = allTickersData[ticker].map(d => d.Date);
            }
            return {
                label: ticker,
                data: allTickersData[ticker].map(d => d.Close),
                type: 'line',
                borderColor: `hsl(${i * 360 / Object.keys(allTickersData).length}, 100%, 50%)`,
                backgroundColor: `hsla(${i * 360 / Object.keys(allTickersData).length}, 100%, 50%, 0.1)`,
                borderWidth: 1
            }
        })
    }
    chartData.labels = labels;
    const portfolioChartCtx = document.getElementById('portfolio-chart');
    portfolioChart = new Chart(portfolioChartCtx, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    });
}

async function loadPortfolioTable() {
    // Show the portfolio table
    const tableBody = document.getElementById('portfolio-table-body');
    tableBody.innerHTML = '';

    portfolio.forEach(item => {
        const row = document.createElement('tr');
        const tickerCell = document.createElement('td');
        const nameCell = document.createElement('td');
        const highestCell = document.createElement('td');
        const lowestCell = document.createElement('td');
        const removeCell = document.createElement('td');

        tickerCell.innerText = item.Ticker;
        nameCell.innerText = companies.find(company => company.Ticker === item.Ticker).Name;
        highestCell.innerText = allTickersData[item.Ticker].reduce((acc, d) => {
            if (acc == null || d.High > acc) {
                acc = d.High;
            }
            return acc;
        }, null);
        lowestCell.innerText = allTickersData[item.Ticker].reduce((acc, d) => {
            if (acc == null || d.Low < acc) {
                acc = d.Low;
            }
            return acc;
        }, null);

        removeCell.appendChild((() => {
            const button = document.createElement('button');
            button.innerText = 'Remove';
            button.addEventListener('click', async () => {
                await addOrRemovePortfolio(item.Ticker, true)
                portfolio = await fetchUserPortfolio();
                await updateAllTickersData();
                await loadPortfolioChart();
                await loadPortfolioTable();
            });
            return button;
        })());

        row.appendChild(tickerCell);
        row.appendChild(nameCell);
        row.appendChild(highestCell);
        row.appendChild(lowestCell);
        row.appendChild(lowestCell);
        row.appendChild(removeCell);

        tableBody.appendChild(row);
    });
}

async function fetchFinanceData(ticker) {
    try {
        const response = await fetch(`/api/finance_data/${ticker}`);
        const data = (await response.json()).results;
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

async function fetchHeadlines() {
    try {
        const response = await fetch('/api/headlines');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function groupHeadlinesByDate(headlinesData) {
    const headlinesByDate = headlinesData.reduce((acc, headline) => {
        const date = headline.Date;
        if (!acc[date]) {
            acc[date] = 0;
        }
        acc[date]++;
        return acc;
    }, {})
    return headlinesByDate;
}

async function loadInitialCompanies() {
    try {
        const response = await fetch('/api/companies');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function updateSelectOptions(companies) {
    const selectElement = document.getElementById('stock-select');

    companies.forEach(company => {
        const optionElement = document.createElement('option');
        optionElement.value = company.Ticker;
        optionElement.innerText = company.Name;
        selectElement.appendChild(optionElement);
    });
}

function seraliseDataWithHeadlines(data, headlinesByDate = []) {
    const chartData = {
        labels: data.map(d => d.Date),
        datasets: [
            {
                label: 'Finance Data',
                data: data.map(d => d.Close),
                type: 'line',
                borderColor: 'blue',
                backgroundColor: 'rgba(0, 0, 255, 0.1)',
                borderWidth: 1
            },
            {
                label: 'Headlines Count',
                data: data.map((d, i) => headlinesByDate[d.Date] || 0),
                type: 'bar',
                borderColor: 'red',
                backgroundColor: 'rgba(255, 0, 0, 0.1)',
                borderWidth: 1
            }
        ]
    }

    return chartData;
}

function checkExistingPortfolio(ticker) {
    // if current selected item is in portfolio, change add to portfolio button to remove from portfolio
    const addToPortfolioButton = document.getElementById('add-to-portfolio');
    if (portfolio.find(item => item.Ticker === ticker)) {
        addToPortfolioButton.innerText = 'Remove from Portfolio';
    } else {
        addToPortfolioButton.innerText = 'Add to Portfolio';
    }
}

async function onSelectChange(event) {
    selectedTicker = event.target.value;
    const data = await fetchFinanceData(selectedTicker);
    const searlisedData = seraliseDataWithHeadlines(data, headlinesCount)
    loadChart(searlisedData);
    checkExistingPortfolio(selectedTicker);
}

async function fetchUserPortfolio() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/api/user_portfolio', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        // Logout if token is invalid
        if (response.status === 401) {
            logout();
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function loadHeadlineToTable(headlines) {
    const tableBody = document.getElementById('headlines-table-body');
    headlines.forEach(headline => {
        const row = document.createElement('tr');
        const dateCell = document.createElement('td');
        const headlineCell = document.createElement('td');
        dateCell.innerText = headline.Date;
        headlineCell.innerText = headline.Headlines;
        row.appendChild(dateCell);
        row.appendChild(headlineCell);

        tableBody.appendChild(row);
    });
}

// Post to /user_portfolio with { ticker: ticker }
async function addOrRemovePortfolio(ticker, remove = false) {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/api/user_portfolio', {
            method: remove ? 'DELETE' : 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify({ ticker })
        });

        if (response.status === 401) {
            logout();
        }

        const data = await response.text();
        alert(data);
    } catch (error) {
        alert('Error adding to portfolio:', error);
    }
}

function logout() {
    console.log('logout');
    localStorage.removeItem('token');
    window.location.href = '/';
}

$(document).ready(async function () {
    // If logged in
    if (window.location.pathname.includes('/app')) {
        portfolio = await fetchUserPortfolio();
        companies = await loadInitialCompanies();
    }

    if (window.location.pathname.includes('/app/ticker')) {
        updateSelectOptions(companies);

        headlinesData = await fetchHeadlines();
        headlinesCount = groupHeadlinesByDate(headlinesData);
        loadHeadlineToTable(headlinesData);

        // fetch the first company and load chart
        const firstCompany = companies[0];
        checkExistingPortfolio(firstCompany.Ticker);
        const financeData = await fetchFinanceData(firstCompany.Ticker);
        const searlisedData = seraliseDataWithHeadlines(financeData, headlinesCount)
        loadChart(searlisedData);

        // Select on change listener
        const selectElement = document.getElementById('stock-select');
        selectElement.addEventListener('change', onSelectChange);

        // add-to-portfolio on click listener
        const addToPortfolioButton = document.getElementById('add-to-portfolio');
        addToPortfolioButton.addEventListener('click', async (e) => {
            await addOrRemovePortfolio(selectElement.value, e.target.innerText === 'Remove from Portfolio')
            // Reload portfolio
            portfolio = await fetchUserPortfolio();
            checkExistingPortfolio(selectedTicker);
        });

    } else if (window.location.pathname.includes('/app/portfolio')) {
        portfolio = await fetchUserPortfolio();

        await updateAllTickersData()
        await loadPortfolioChart();
        await loadPortfolioTable();
    }
});

const sortState = {};
document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
    initializeTabs();
    initializeTableSorting();
    initializeContactButtons();
    initializeResponsive();
});
function initializeSidebar() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarExpand = document.getElementById('sidebarExpand');
    const sidebar = document.getElementById('sidebar');
    const sidebarIndicator = document.getElementById('sidebarIndicator'); 
    let sidebarOpen = true;
    function toggleSidebar() {
        sidebarOpen = !sidebarOpen;
        if (window.innerWidth <= 768) {
            if (sidebarOpen) {
                sidebar.classList.add('open');
                sidebar.classList.remove('collapsed');
                if (sidebarIndicator) {
                    sidebarIndicator.style.display = 'none';
                }
                showOverlay();
            } else {
                sidebar.classList.remove('open');
                sidebar.classList.add('collapsed');
                if (sidebarIndicator) {
                    sidebarIndicator.style.display = 'flex';
                }
                hideOverlay();
            }
        } else {
            if (sidebarOpen) {
                sidebar.classList.remove('collapsed');
                if (sidebarIndicator) {
                    sidebarIndicator.style.display = 'none';
                }
            } else {
                sidebar.classList.add('collapsed');
                if (sidebarIndicator) {
                    sidebarIndicator.style.display = 'flex';
                }
            }
        }
        updateToggleIcon();
        localStorage.setItem('sidebarOpen', sidebarOpen);
    }
    function updateToggleIcon() {
        const toggleIcon = document.querySelector('.toggle-icon');
        if (toggleIcon) {
            toggleIcon.textContent = sidebarOpen ? '≪' : '≫';
            if (sidebarToggle) {
                sidebarToggle.title = sidebarOpen ? 'Collapse Sidebar' : 'Expand Sidebar';
            }
        }
    }
    function showOverlay() {
        if (window.innerWidth <= 768) {
            let overlay = document.querySelector('.sidebar-overlay');
            if (!overlay) {
                overlay = document.createElement('div');
                overlay.className = 'sidebar-overlay';
                document.body.appendChild(overlay);           
                overlay.addEventListener('click', function() {
                    if (sidebarOpen) {
                        toggleSidebar();
                    }
                });
            }
            overlay.classList.add('active');
        }
    }
    function hideOverlay() {
        const overlay = document.querySelector('.sidebar-overlay');
        if (overlay) {
            overlay.classList.remove('active');
        }
    }
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }
    if (sidebarExpand) {
        sidebarExpand.addEventListener('click', toggleSidebar);
    }
    const savedState = localStorage.getItem('sidebarOpen');
    if (savedState !== null) {
        const shouldBeOpen = savedState === 'true';
        if (shouldBeOpen !== sidebarOpen) {
            sidebarOpen = shouldBeOpen;
            toggleSidebar();
        }
    }
    updateToggleIcon();
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && window.innerWidth <= 768 && sidebarOpen) {
            toggleSidebar();
        }
    });
    window.toggleSidebar = toggleSidebar;
    window.hideOverlay = hideOverlay;
    window.sidebarOpen = sidebarOpen;
    window.updateToggleIcon = updateToggleIcon;
}
function initializeTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');   
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.style.display = 'none');
            this.classList.add('active');
            const targetContent = document.getElementById(targetTab);
            if (targetContent) {
                targetContent.style.display = 'block';
            }
        });
    });
}
function initializeTableSorting() {
    const tables = document.querySelectorAll('.market-table');
    tables.forEach(table => {
        const tableId = table.id;
        if (tableId) {
            sortState[tableId] = {};
            const headers = table.querySelectorAll('th.sortable');
            headers.forEach((header, index) => {
                sortState[tableId][index] = { direction: 'none' };
            });
        }
    });
}
function initializeContactButtons() {
    const contactBtns = document.querySelectorAll('.btn-contact');
    contactBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const phone = this.getAttribute('data-phone');
            if (phone) {
                copyToClipboard(phone).then(() => {
                    showToast('Phone number copied to clipboard!');
                }).catch(() => {
                    showToast('Failed to copy phone number');
                });
            }
        });
    });
}
function initializeResponsive() {
    window.addEventListener('resize', function() {
        if (window.hideOverlay) {
            window.hideOverlay();
        }       
        const sidebar = document.getElementById('sidebar');
        const sidebarIndicator = document.getElementById('sidebarIndicator');
        if (window.innerWidth > 768 && sidebar && sidebarIndicator) {
            sidebar.classList.remove('open');
            if (window.sidebarOpen) {
                sidebar.classList.remove('collapsed');
                sidebarIndicator.style.display = 'none';
            } else {
                sidebar.classList.add('collapsed');
                sidebarIndicator.style.display = 'flex';
            }
        } else if (sidebar && sidebarIndicator && window.sidebarOpen) {
            sidebar.classList.add('open');
            sidebarIndicator.style.display = 'none';
        }
        if (window.updateToggleIcon) {
            window.updateToggleIcon();
        }
    });
}
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(text);
    } else {
        return new Promise((resolve, reject) => {
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();           
            try {
                document.execCommand('copy');
                document.body.removeChild(textArea);
                resolve();
            } catch (err) {
                document.body.removeChild(textArea);
                reject(err);
            }
        });
    }
}
function showToast(message) {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');   
    if (toast && toastMessage) {
        toastMessage.textContent = message;
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
}
function sortTable(columnIndex, tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;   
    const tbody = table.querySelector('tbody');
    const headers = table.querySelectorAll('th.sortable');
    if (!tbody || !headers[columnIndex]) return;
    const currentState = sortState[tableId][columnIndex];
    headers.forEach((header, index) => {
        const indicator = header.querySelector('.sort-indicator');
        if (indicator && index !== columnIndex) {
            indicator.textContent = '↕';
            sortState[tableId][index].direction = 'none';
        }
    });
    let newDirection;
    if (currentState.direction === 'none' || currentState.direction === 'desc') {
        newDirection = 'asc';
    } else {
        newDirection = 'desc';
    }
    sortState[tableId][columnIndex].direction = newDirection;
    const indicator = headers[columnIndex].querySelector('.sort-indicator');
    if (indicator) {
        indicator.textContent = newDirection === 'asc' ? '↑' : '↓';
    }
    const rows = Array.from(tbody.querySelectorAll('tr'));
    rows.sort((rowA, rowB) => {
        const cellA = rowA.cells[columnIndex];
        const cellB = rowB.cells[columnIndex];
        if (!cellA || !cellB) return 0;
        let valueA = cellA.textContent.trim();
        let valueB = cellB.textContent.trim();
        const numericA = parseNumericValue(valueA);
        const numericB = parseNumericValue(valueB);
        let compareResult = 0;
        if (!isNaN(numericA) && !isNaN(numericB)) {
            compareResult = numericA - numericB;
        } else if (isDuration(valueA) && isDuration(valueB)) {
            compareResult = parseDuration(valueA) - parseDuration(valueB);
        } else {
            compareResult = valueA.localeCompare(valueB, undefined, { 
                numeric: true, 
                sensitivity: 'base' 
            });
        }
        return newDirection === 'asc' ? compareResult : -compareResult;
    });
    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));
}
function parseNumericValue(text) {
    const cleaned = text.replace(/[^\d.-]/g, '');
    const parsed = parseFloat(cleaned);
    return isNaN(parsed) ? NaN : parsed;
}
function isDuration(text) {
    return /^\d+d \d+h \d+m/.test(text) || text === '--';
}
function parseDuration(durationStr) {
    if (durationStr === '--') return 0;    
    let totalMinutes = 0;
    const days = durationStr.match(/(\d+)d/);
    const hours = durationStr.match(/(\d+)h/);
    const minutes = durationStr.match(/(\d+)m/);
    if (days) totalMinutes += parseInt(days[1]) * 24 * 60;
    if (hours) totalMinutes += parseInt(hours[1]) * 60;
    if (minutes) totalMinutes += parseInt(minutes[1]);
    return totalMinutes;
}
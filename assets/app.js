// État de l'application
let allFoods = [];
let filteredFoods = [];
let currentFilter = 'all';
let currentCategory = 'all';
let currentSeason = 'all';
let currentDigestibility = 'all';
let myList = [];

// Éléments DOM
const searchInput = document.getElementById('searchInput');
const foodList = document.getElementById('foodList');
const resultCount = document.getElementById('resultCount');
const filterBtns = document.querySelectorAll('.filter-btn');
const categoryFilter = document.getElementById('categoryFilter');
const seasonBtns = document.querySelectorAll('.season-btn');
const digestibilityBtns = document.querySelectorAll('.digestibility-btn');
const resetBtn = document.getElementById('resetFilters');

// Charger les données au démarrage
document.addEventListener('DOMContentLoaded', () => {
    loadMyList();
    loadFoods();
    setupEventListeners();
});

// Charger les aliments depuis le JSON
async function loadFoods() {
    try {
        const response = await fetch('foods.json');
        allFoods = await response.json();
        filteredFoods = allFoods;
        
        // Peupler le sélecteur de catégories
        populateCategoryFilter();
        
        displayFoods(filteredFoods);
        updateResultCount();
    } catch (error) {
        console.error('Erreur lors du chargement des données:', error);
        foodList.innerHTML = '<div class="no-results">Erreur lors du chargement des données</div>';
    }
}

// Peupler le sélecteur de catégories
function populateCategoryFilter() {
    const categories = [...new Set(allFoods.map(f => f.category))].filter(c => c).sort();
    
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        categoryFilter.appendChild(option);
    });
}

// Configuration des écouteurs d'événements
function setupEventListeners() {
    // Recherche en temps réel
    searchInput.addEventListener('input', () => {
        filterAndDisplay();
    });

    // Filtres rapides (histamine, libérateur, etc.)
    filterBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            filterBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentFilter = e.target.dataset.filter;
            filterAndDisplay();
        });
    });

    // Filtre par catégorie
    categoryFilter.addEventListener('change', (e) => {
        currentCategory = e.target.value;
        filterAndDisplay();
    });

    // Filtres par saison
    seasonBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            seasonBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentSeason = e.target.dataset.season;
            filterAndDisplay();
        });
    });

    // Filtres par digestibilité
    digestibilityBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            digestibilityBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentDigestibility = e.target.dataset.digestibility;
            filterAndDisplay();
        });
    });

    // Bouton reset
    resetBtn.addEventListener('click', () => {
        resetAllFilters();
    });
}

// Réinitialiser tous les filtres
function resetAllFilters() {
    // Reset recherche
    searchInput.value = '';
    
    // Reset filtre rapide
    currentFilter = 'all';
    filterBtns.forEach(b => b.classList.remove('active'));
    filterBtns[0].classList.add('active');
    
    // Reset catégorie
    currentCategory = 'all';
    categoryFilter.value = 'all';
    
    // Reset saison
    currentSeason = 'all';
    seasonBtns.forEach(b => b.classList.remove('active'));
    
    // Reset digestibilité
    currentDigestibility = 'all';
    digestibilityBtns.forEach(b => b.classList.remove('active'));
    digestibilityBtns[0].classList.add('active');
    
    filterAndDisplay();
}

// Filtrer et afficher les aliments
function filterAndDisplay() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    
    filteredFoods = allFoods.filter(food => {
        // 1. Filtrer par recherche texte
        const matchesSearch = !searchTerm || food.name.toLowerCase().includes(searchTerm);
        if (!matchesSearch) return false;
        
        // 2. Filtrer par catégorie
        const matchesCategory = currentCategory === 'all' || food.category === currentCategory;
        if (!matchesCategory) return false;
        
        // 3. Filtrer par filtre rapide (histamine, libérateur, etc.)
        let matchesQuickFilter = true;
        switch(currentFilter) {
            case 'all':
                matchesQuickFilter = true;
                break;
            case 'high-histamine':
                matchesQuickFilter = food.histamine && (food.histamine === '2' || food.histamine === '1' || food.histamine.includes('H'));
                break;
            case 'liberator':
                matchesQuickFilter = food.liberator && (food.liberator === 'L' || food.liberator.includes('L'));
                break;
            case 'inhibitor':
                matchesQuickFilter = food.inhibitor && (food.inhibitor === 'I' || food.inhibitor.includes('I'));
                break;
        }
        if (!matchesQuickFilter) return false;
        
        // 4. Filtrer par saison
        let matchesSeason = true;
        if (currentSeason !== 'all') {
            if (food.seasons && food.seasons.length > 0) {
                matchesSeason = food.seasons.includes(currentSeason);
            } else {
                // Si pas de données de saison, ne pas afficher avec filtre actif
                matchesSeason = false;
            }
        }
        if (!matchesSeason) return false;
        
        // 5. Filtrer par digestibilité
        let matchesDigestibility = true;
        if (currentDigestibility !== 'all') {
            matchesDigestibility = food.digestibility === currentDigestibility;
        }
        if (!matchesDigestibility) return false;
        
        return true;
    });
    
    displayFoods(filteredFoods);
    updateResultCount();
}

// Afficher les aliments
function displayFoods(foods) {
    if (foods.length === 0) {
        foodList.innerHTML = '<div class="no-results">Aucun aliment trouve</div>';
        return;
    }
    
    foodList.innerHTML = foods.map(food => createFoodCard(food)).join('');
}

// Créer une carte d'aliment
function createFoodCard(food) {
    const hasRemarks = food.remarks && food.remarks.trim() !== '';
    const hasSeasons = food.seasons && food.seasons.length > 0;
    const isInList = myList.includes(food.name);
    
    return `
        <div class="food-card" data-name="${food.name}">
            <div class="food-header">
                <div class="food-name">${food.name}</div>
                <button class="add-to-list-btn ${isInList ? 'in-list' : ''}" 
                        onclick="toggleFoodInList('${food.name.replace(/'/g, "\\'")}')">
                    ${isInList ? '✓' : '+'}
                </button>
            </div>
            <div class="food-badges">
                ${food.category ? `<span class="food-category">${food.category}</span>` : ''}
                ${hasSeasons ? createSeasonBadges(food.seasons) : ''}
            </div>
            
            <div class="food-properties">
                ${createProperty('Histamine', food.histamine, 'histamine')}
                ${createProperty('Liberateur', food.liberator, 'liberator')}
                ${createProperty('Inhibiteur', food.inhibitor, 'inhibitor')}
                ${createProperty('Digestibilite', food.digestibility, 'digestibility')}
                ${createProperty('Autres amines', food.other_amines, 'amines')}
            </div>
            
            ${hasRemarks ? `<div class="food-remarks">${food.remarks}</div>` : ''}
        </div>
    `;
}

// Créer les badges de saison
function createSeasonBadges(seasons) {
    const seasonNames = {
        'printemps': 'Printemps',
        'ete': 'Ete',
        'automne': 'Automne',
        'hiver': 'Hiver',
        'toute_annee': 'Toute annee'
    };
    
    return seasons.map(season => 
        `<span class="season-badge ${season}">${seasonNames[season] || season}</span>`
    ).join('');
}

// Créer une propriété
function createProperty(label, value, type) {
    if (!value || value.trim() === '') return '';
    
    let valueClass = '';
    
    // Déterminer la classe CSS selon le type et la valeur
    if (type === 'histamine') {
        if (value === '2' || value.includes('2')) valueClass = 'high';
        else if (value === '1' || value.includes('1')) valueClass = 'medium';
        else if (value === '0' || value.includes('0')) valueClass = 'low';
    } else if (type === 'liberator') {
        if (value.includes('L')) valueClass = 'liberator';
    } else if (type === 'inhibitor') {
        if (value.includes('I')) valueClass = 'inhibitor';
    } else if (type === 'digestibility') {
        if (value === '2') valueClass = 'high';
        else if (value === '1') valueClass = 'medium';
        else if (value === '0') valueClass = 'low';
    }
    
    return `
        <div class="property">
            <span class="property-label">${label}:</span>
            <span class="property-value ${valueClass}">${value}</span>
        </div>
    `;
}

// Mettre à jour le compteur de résultats
function updateResultCount() {
    resultCount.textContent = filteredFoods.length;
}

// Gestion de la liste personnalisée
function loadMyList() {
    const saved = localStorage.getItem('samaMyList');
    if (saved) {
        myList = JSON.parse(saved);
    }
    updateListCount();
}

function saveMyList() {
    localStorage.setItem('samaMyList', JSON.stringify(myList));
    updateListCount();
}

function toggleFoodInList(foodName) {
    const index = myList.indexOf(foodName);
    if (index > -1) {
        myList.splice(index, 1);
    } else {
        myList.push(foodName);
    }
    saveMyList();
    displayFoods(filteredFoods); // Rafraîchir l'affichage
}

function removeFromList(foodName) {
    const index = myList.indexOf(foodName);
    if (index > -1) {
        myList.splice(index, 1);
        saveMyList();
        displayMyList();
        displayFoods(filteredFoods);
    }
}

function clearList() {
    if (confirm('Voulez-vous vraiment vider votre liste ?')) {
        myList = [];
        saveMyList();
        displayMyList();
        displayFoods(filteredFoods);
    }
}

function displayMyList() {
    const listContainer = document.getElementById('myListItems');
    
    if (myList.length === 0) {
        listContainer.innerHTML = '<div class="empty-list">Aucun aliment dans votre liste</div>';
        return;
    }
    
    listContainer.innerHTML = myList.map(foodName => `
        <div class="list-item">
            <span class="list-item-name">${foodName}</span>
            <button class="remove-btn" onclick="removeFromList('${foodName.replace(/'/g, "\\'")}')">×</button>
        </div>
    `).join('');
}

function updateListCount() {
    const counter = document.getElementById('listCount');
    if (counter) {
        counter.textContent = myList.length;
    }
}

function toggleSidebar() {
    const sidebar = document.getElementById('listSidebar');
    sidebar.classList.toggle('open');
    displayMyList();
}

function exportList(format) {
    if (myList.length === 0) {
        alert('Votre liste est vide !');
        return;
    }
    
    const foodsInList = allFoods.filter(f => myList.includes(f.name));
    
    if (format === 'json') {
        const dataStr = JSON.stringify(foodsInList, null, 2);
        downloadFile('ma-liste-sama.json', dataStr, 'application/json');
    } else if (format === 'csv') {
        const csv = generateCSV(foodsInList);
        downloadFile('ma-liste-sama.csv', csv, 'text/csv');
    } else if (format === 'txt') {
        const txt = foodsInList.map(f => f.name).join('\n');
        downloadFile('ma-liste-sama.txt', txt, 'text/plain');
    }
}

function generateCSV(foods) {
    const headers = ['Nom', 'Categorie', 'Histamine', 'Liberateur', 'Inhibiteur', 'Digestibilite', 'Autres amines', 'Remarques'];
    const rows = foods.map(f => [
        f.name,
        f.category || '',
        f.histamine || '',
        f.liberator || '',
        f.inhibitor || '',
        f.digestibility || '',
        f.other_amines || '',
        (f.remarks || '').replace(/"/g, '""')
    ]);
    
    const csvContent = [
        headers.join(','),
        ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');
    
    return csvContent;
}

function downloadFile(filename, content, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// Exposer les fonctions pour les tests
window.testAPI = {
    getAllFoods: () => allFoods,
    getFilteredFoods: () => filteredFoods,
    searchFoods: (term) => {
        searchInput.value = term;
        filterAndDisplay();
    },
    setFilter: (filter) => {
        currentFilter = filter;
        filterAndDisplay();
    }
};

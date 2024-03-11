let searchable = [
    "book",
    "horror books",
    "comic books",
    "comedy books",
    "manga books",
    "Harry Potter and the Goblet of Fire",
    "The hunter games",
    "One Hundred Years of Solitude",
    "To Kill a Mockingbird",
    "Slaughterhouse Five",
    "wings of fire",
    "life at work",
    "The alchemist",
    "The psychology of money",
    "a song of ice and fire",
];

const searchInput = document.getElementById('search');
const searchWrapper = document.querySelector('.wrapper');
const resultsWrapper = document.querySelector('.results');

searchInput.addEventListener('keyup', () => {
    let results = [];
    let input = searchInput.value;
    if (input.length) {
        results = searchable.filter((item) => {
            return item.toLowerCase().includes(input.toLowerCase());
        });
    }
    renderResults(results);
});

function renderResults(results) {
    if (!results.length) {
        return searchWrapper.classList.remove('show');
    }


    let content = results
        .map((item) => {
            return `<li><a href='#'>${item}</a></li>`;
        })
        .join('');
    searchWrapper.classList.add('show');
    resultsWrapper.innerHTML = `<ul>${content}</ul>`
}
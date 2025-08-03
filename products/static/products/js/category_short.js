 document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.getElementById('id_category');
    const subCategorySelect = document.getElementById('id_subCategory');

    function filterSubCategories() {
      const selectedCategory = categorySelect.value;
      for (const option of subCategorySelect.options) {
        // uvijek pokaži praznu opciju
        if (!option.value) {
          option.style.display = '';
          continue;
        }
        if (option.getAttribute('data-category') === selectedCategory) {
          option.style.display = '';
        } else {
          option.style.display = 'none';
        }
      }
      // Resetuj podkategoriju kad se promijeni kategorija
      subCategorySelect.value = '';
    }

    categorySelect.addEventListener('change', filterSubCategories);

    // pozovi odmah da inicijalno filtrira podkategorije po trenutno odabranoj kategoriji (ako ima)
    filterSubCategories();
  });
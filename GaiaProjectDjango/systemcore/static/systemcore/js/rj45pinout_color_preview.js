document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('select[name$="color_code"]').forEach(function(select) {
    function updatePreview() {
      const color = select.options[select.selectedIndex].textContent.toLowerCase().replace(/\s/g, '-');
      const preview = select.closest('tr').querySelector('.color-preview');
      // Simple color mapping (customize as needed)
      const colorMap = {
        'white-orange': '#fff4e6',
        'orange': '#ff9900',
        'white-green': '#e6ffe6',
        'green': '#33cc33',
        'blue': '#3399ff',
        'white-blue': '#e6f0ff',
        'white-brown': '#f5e6cc',
        'brown': '#996633'
      };
      preview.style.backgroundColor = colorMap[color] || '#eee';
    }
    select.addEventListener('change', updatePreview);
    updatePreview();
  });
});